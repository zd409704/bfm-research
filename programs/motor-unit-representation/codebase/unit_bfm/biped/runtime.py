"""CPU assembly adapter for four frozen V2 units; no upper policy or training."""
from pathlib import Path
import json

import mujoco
import numpy as np
import torch

from unit_bfm.interface import FrozenUnit
from unit_bfm.schema import NOMINAL_SCALES

HERE = Path(__file__).resolve().parent


class Biped:
    def __init__(self):
        self.config = json.loads((HERE/'design.json').read_text())
        self.model = mujoco.MjModel.from_xml_path(str(HERE/'models/biped_4dof.xml'))
        self.data = mujoco.MjData(self.model)
        self.units = self.config['units']
        self.joints = [self.model.joint(u['joint']).id for u in self.units]
        self.qids = np.array([self.model.jnt_qposadr[j] for j in self.joints])
        self.vids = np.array([self.model.jnt_dofadr[j] for j in self.joints])
        self.bodies = np.array([[self.model.body(u['P']).id, self.model.body(u['D']).id] for u in self.units])
        self.actuators = np.array([self.model.actuator(u['joint']+'_drive').id for u in self.units])
        self.m = self.nominal()
        self.reset()

    def nominal(self):
        rows = []
        m = self.model
        for u, j, (p, d) in zip(self.units, self.joints, self.bodies):
            # URDF/MJCF origin is a frame choice. Express COM relative to this
            # joint, in its corresponding P/D link axes, not relative to root.
            assert np.allclose(m.body_quat[d], [1, 0, 0, 0])
            joint_in_parent = m.body_pos[d] + m.jnt_pos[j]
            pc = m.body_ipos[p] - joint_in_parent
            dc = m.body_ipos[d] - m.jnt_pos[j]
            inertias = []
            for body in (p, d):
                rotation = np.empty(9)
                mujoco.mju_quat2Mat(rotation, m.body_iquat[body])
                rotation = rotation.reshape(3, 3)
                inertias.append(float((rotation @ np.diag(m.body_inertia[body]) @ rotation.T)[1, 1]))
            row = [self.config['links'][u['P']]['length_m'], self.config['links'][u['D']]['length_m'],
                   m.body_mass[p], m.body_mass[d], *inertias, pc[0], pc[2], dc[0], dc[2],
                   *m.jnt_range[j], self.config['drive']['nominal_request_Nm'], self.config['drive']['response_time_s']]
            rows.append(np.r_[np.asarray(row)/NOMINAL_SCALES, np.ones(14)])
        return np.asarray(rows, np.float32)

    def reset(self, q=(-.25, .5, -.25, .5), clearance=.001):
        values = np.asarray(q, float)
        if values.shape != (4,) or not np.isfinite(values).all():
            raise ValueError('Four finite joint angles required')
        if np.any(values < self.model.jnt_range[self.joints, 0]) or np.any(values > self.model.jnt_range[self.joints, 1]):
            raise ValueError('Initial joint angles exceed physical limits')
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[self.qids] = values
        mujoco.mj_forward(self.model, self.data)
        bottoms = []
        for name in self.config['links']:
            g = self.model.geom(name+'_box').id
            radius_z = np.abs(self.data.geom_xmat[g].reshape(3, 3)[2]) @ self.model.geom_size[g]
            bottoms.append(self.data.geom_xpos[g, 2]-radius_z)
        self.data.qpos[int(self.model.joint('root_z').qposadr[0])] += clearance-min(bottoms)
        mujoco.mj_forward(self.model, self.data)
        self.u = np.zeros(4); self.tau = np.zeros(4)
        self.ring = np.zeros((11, 4)); self.clock = 0
        self.wrench = np.zeros((4, 2, 3)); self.contact = np.zeros((4, 2))
        return self.observe()

    def observe(self):
        m, d = self.model, self.data
        o = np.zeros((4, 24), np.float32)
        q = d.qpos[self.qids]
        o[:, 0] = q/1.2; o[:, 1] = d.qvel[self.vids]/6.
        for i, pair in enumerate(self.bodies):
            for side, body in enumerate(pair):
                rot = d.xmat[body].reshape(3, 3)
                cv = d.cvel[body]
                velocity = cv[3:] + np.cross(cv[:3], d.xipos[body]-d.subtree_com[m.body_rootid[body]])
                o[i, 2+5*side:7+5*side] = [rot[0, 2], rot[0, 0], velocity[0]/2, velocity[2]/2, cv[1]/6]
        o[:, 12] = self.tau/6.; o[:, 13] = self.u
        o[:, 14:16] = self.contact
        o[:, 16] = (q-self.model.jnt_range[self.joints, 0])/2.4
        o[:, 17] = (self.model.jnt_range[self.joints, 1]-q)/2.4
        o[:, 18:] = (self.wrench/np.array([20., 20., 6.])).reshape(4, 6)
        return o

    def step(self, commands):
        commands = np.asarray(commands, float)
        if commands.shape != (4,) or not np.isfinite(commands).all():
            raise ValueError('Four finite normalized requests required')
        self.u = np.clip(commands, -1, 1)
        cfg = self.config['drive']; dt = cfg['physics_dt_s']
        nsub = round(cfg['control_dt_s']/dt)
        self.wrench.fill(0); self.contact.fill(0)
        for _ in range(nsub):
            mujoco.mj_forward(self.model, self.data)
            self.ring[self.clock % 11] = cfg['nominal_request_Nm']*self.u
            delayed = self.ring[(self.clock-cfg['delay_ms']) % 11]
            target = np.clip(delayed, -cfg['capacity_Nm'], cfg['capacity_Nm'])
            self.tau += (1-np.exp(-dt/cfg['response_time_s']))*(target-self.tau)
            self.data.ctrl[self.actuators] = self.tau
            mujoco.mj_step(self.model, self.data)
            # Explicit world-frame forces/torques at each COM follow V2's
            # xfrc contract. Gravity and internal joint reactions are excluded.
            self.wrench += self.data.xfrc_applied[self.bodies][..., [0, 2, 4]]/nsub
            for ci in range(self.data.ncon):
                c = self.data.contact[ci]
                b0, b1 = self.model.geom_bodyid[c.geom]
                force6 = np.empty(6)
                mujoco.mj_contactForce(self.model, self.data, ci, force6)
                force = c.frame.reshape(3, 3).T @ force6[:3]
                moment = c.frame.reshape(3, 3).T @ force6[3:]
                for i, pair in enumerate(self.bodies):
                    if {b0, b1} == set(pair): continue
                    for side, body in enumerate(pair):
                        sign = 1 if b1 == body else (-1 if b0 == body else 0)
                        if sign:
                            f = sign*force
                            torque = sign*moment+np.cross(c.pos-self.data.xipos[body], f)
                            self.wrench[i, side] += np.array([f[0], f[2], torque[1]])/nsub
                            self.contact[i, side] = 1
            self.clock += 1
        mujoco.mj_forward(self.model, self.data)
        return self.observe()


class FrozenBiped:
    """Four rows share V2 weights while retaining four independent histories."""
    def __init__(self, bundle):
        self.physics = Biped()
        self.policy = FrozenUnit(bundle, nworld=4, device='cpu')
        self.reset()

    def reset(self, q=(-.25, .5, -.25, .5)):
        o = self.physics.reset(q)
        self.policy.reset(torch.from_numpy(o), torch.from_numpy(self.physics.m))
        return self.policy.feedback()

    @torch.no_grad()
    def step(self, z):
        z = torch.as_tensor(z, dtype=torch.float32)
        if z.shape != (4, 16) or not torch.isfinite(z).all():
            raise ValueError('Expected four finite 16-dimensional z commands')
        commands = self.policy.act(z)[:, 0].numpy()
        o = self.physics.step(commands)
        self.policy.observe(torch.from_numpy(o))
        return self.policy.feedback()
