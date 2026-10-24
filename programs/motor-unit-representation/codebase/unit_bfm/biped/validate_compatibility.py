"""Check structural/observation/drive compatibility and frozen V2 integration.

These are assembly checks, not a walking or low-level capability acceptance.
"""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

import mujoco
import numpy as np
import torch

from unit_bfm.biped.runtime import Biped, FrozenBiped, HERE
from unit_bfm.biped.inspect_model import read_model, forward
from unit_bfm.mechanics import Structure
from unit_bfm.interface import FrozenUnit


def inertia_tensor(model, body):
    rotation = np.empty(9)
    mujoco.mju_quat2Mat(rotation, model.body_iquat[body])
    rotation = rotation.reshape(3, 3)
    return rotation @ np.diag(model.body_inertia[body]) @ rotation.T


def run():
    torch.set_num_threads(1)
    b = Biped(); m, d = b.model, b.data
    assert m.nq == m.nv == 7 and m.nu == 4
    np.testing.assert_allclose(m.body_mass.sum(), 2.5, atol=1e-12)
    rows = []
    for i, (u, pair) in enumerate(zip(b.units, b.bodies)):
        p, distal = (b.config['links'][u[k]] for k in ('P', 'D'))
        source = Structure(0, 0, lp=p['length_m'], ld=distal['length_m'],
                           mp=p['mass_kg'], md=distal['mass_kg'])
        expected = source.nominal()
        np.testing.assert_allclose(b.m[i], expected, rtol=0, atol=1e-7)
        sm = source.compile()
        # The entire COM inertia tensor and physical rod section match, not only
        # independently bounded scalar entries. Principal axes are canonical here.
        for body, name in zip(pair, ('P', 'D')):
            ref = sm.body(name).id
            np.testing.assert_allclose(inertia_tensor(m, body), inertia_tensor(sm, ref), atol=1e-12)
            np.testing.assert_allclose(m.body_mass[body], sm.body_mass[ref], atol=1e-12)
            actual_geom = m.geom(u[name]+'_box').id
            ref_geom = sm.geom(name+'_box').id
            assert m.geom_type[actual_geom] == sm.geom_type[ref_geom]
            np.testing.assert_allclose(m.geom_size[actual_geom], sm.geom_size[ref_geom], atol=1e-12)
        assert .15 <= source.lp <= .4 and .25 <= source.ld <= .45
        assert .4 <= source.mp <= 2 and .15 <= source.md <= .6
        rows.append(dict(joint=u['joint'], P=u['P'], D=u['D'],
                         local_rod_geometry_and_inertia_match=True,
                         P_COM_along_joint_axis_offset_m=float(m.body_ipos[pair[0], 1]-u['xyz'][1]),
                         m28_max_error=float(np.max(np.abs(b.m[i]-expected))),
                         normalized_m28=b.m[i].tolist()))
    for j, v in zip(b.joints, b.vids):
        np.testing.assert_allclose(m.jnt_range[j], [-1.2, 1.2], atol=1e-12)
        np.testing.assert_allclose([m.dof_damping[v], m.dof_frictionloss[v], m.dof_armature[v], m.jnt_margin[j]],
                                   [.03, .02, .003, .03], atol=1e-12)
    assert np.array_equal(m.actuator_trnid[:, 0], b.joints)
    assert m.opt.timestep == .001

    # Cross-check the companion dynamic scene against the actual URDF tree.
    urdf = read_model(); rng = np.random.default_rng(41004)
    fk_error = 0.
    for q in rng.uniform(-1.1, 1.1, (24, 4)):
        b.reset(q)
        poses = forward(urdf, dict(zip([u['joint'] for u in b.units], q)))
        root_pos = d.xpos[m.body('pelvis').id].copy()
        for name, pose in poses.items():
            body = m.body(name).id
            fk_error = max(fk_error, float(np.max(np.abs(d.xpos[body]-root_pos-pose[:3, 3]))))
            np.testing.assert_allclose(d.xmat[body].reshape(3, 3), pose[:3, :3], atol=1e-12)
    assert fk_error < 1e-12

    # Along-axis layer spacing changes collision separation, but not the
    # unconstrained planar mass matrix/gravity. This is not a 3D equivalence.
    root = ET.parse(HERE/'models/biped_4dof.xml').getroot()
    for name in ('left_thigh', 'right_thigh'):
        root.find(f'.//body[@name="{name}"]').set('pos', '0 0 0')
    colocated = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding='unicode'))
    cd = mujoco.MjData(colocated)
    mass_error = 0.
    for _ in range(8):
        d.qpos[:] = rng.uniform(-.4, .4, m.nq); d.qvel[:] = rng.uniform(-1, 1, m.nv)
        cd.qpos[:] = d.qpos; cd.qvel[:] = d.qvel
        mujoco.mj_forward(m, d); mujoco.mj_forward(colocated, cd)
        # qM is the packed inertia matrix with identical topology/order.
        mass_error = max(mass_error, float(np.max(np.abs(d.qM-cd.qM))))
        np.testing.assert_allclose(d.qM, cd.qM, atol=1e-12)
        np.testing.assert_allclose(d.qfrc_bias, cd.qfrc_bias, atol=1e-10)

    # Confirm velocity fields by independent finite differences of body COM FK.
    b.reset(); d.qvel[:] = rng.uniform(-1, 1, m.nv); mujoco.mj_forward(m, d)
    observed = b.observe(); before = d.xipos.copy(); qbefore = d.qpos.copy()
    eps = 1e-7
    mujoco.mj_integratePos(m, d.qpos, d.qvel, eps); mujoco.mj_forward(m, d)
    velocity = (d.xipos-before)/eps
    com_error = 0.
    for i, pair in enumerate(b.bodies):
        for side, body in enumerate(pair):
            err = np.max(np.abs(observed[i, 4+5*side:6+5*side]*2-velocity[body, [0, 2]]))
            com_error = max(com_error, float(err))
    assert com_error < 2e-6
    d.qpos[:] = qbefore; mujoco.mj_forward(m, d)

    b.reset(); b.step(np.ones(4))
    expected_tau = 6*(1-np.exp(-.01/.01))
    np.testing.assert_allclose(b.tau, expected_tau, atol=1e-12)
    assert b.clock == 10 and abs(d.time-.01) < 1e-12
    np.testing.assert_allclose(d.qfrc_actuator[b.vids], b.tau, atol=1e-12)
    np.testing.assert_allclose(d.qfrc_actuator[:3], 0., atol=1e-12)
    b.config['drive']['delay_ms'] = 5
    b.reset(); b.step(np.ones(4))
    np.testing.assert_allclose(b.tau, 6*(1-np.exp(-.005/.01)), atol=1e-12)

    # Let the passive body settle: ground contact is physical, not a display line.
    contact_env = Biped(); contact_seen = False
    for _ in range(40):
        o = contact_env.step(np.zeros(4))
        assert np.isfinite(o).all()
        contact_seen |= bool(o[:, 14:16].any())
    assert contact_seen

    external_env = Biped()
    external_env.reset(clearance=1.)
    external_env.data.xfrc_applied[external_env.model.body('left_thigh').id] = [1., 0., 2., 0., 3., 0.]
    external_env.step(np.zeros(4))
    np.testing.assert_allclose(external_env.wrench[0, 1], [1., 2., 3.], atol=1e-12)
    np.testing.assert_allclose(external_env.wrench[1, 0], [1., 2., 3.], atol=1e-12)
    np.testing.assert_allclose(external_env.wrench[[2, 3]], 0., atol=1e-12)
    assert not external_env.contact.any()

    bundle = HERE.parent/'artifacts/rf_v2_full/candidate_unit_with_schema.pt'
    bundle_hash = hashlib.sha256(bundle.read_bytes()).hexdigest()
    robot = FrozenBiped(bundle)
    individuals = [FrozenUnit(bundle, nworld=1) for _ in range(4)]
    o = robot.physics.observe()
    for i, unit in enumerate(individuals):
        unit.reset(torch.from_numpy(o[i:i+1]), torch.from_numpy(robot.physics.m[i:i+1]))
    generator = torch.Generator().manual_seed(61004)
    z = torch.randn(4, 16, generator=generator)
    action_error = 0.
    feedback_error = 0.
    for step in range(100):
        if step in (4, 12, 50): z = torch.randn(4, 16, generator=generator)
        expected_actions = torch.cat([unit.act(z[i:i+1]) for i, unit in enumerate(individuals)])
        actual_actions = robot.policy.act(z)
        action_error = max(action_error, float((expected_actions-actual_actions).abs().max()))
        # CPU batched GEMM and single-row GEMM can accumulate FP32 sums in
        # different orders; compare numerically while recording actual errors.
        torch.testing.assert_close(actual_actions, expected_actions, atol=1e-5, rtol=1e-4)
        feedback = robot.step(z)
        assert feedback.shape == (4, 197) and torch.isfinite(feedback).all()
        o = robot.physics.observe()
        for i, unit in enumerate(individuals): unit.observe(torch.from_numpy(o[i:i+1]))
        expected_feedback = torch.cat([unit.feedback() for unit in individuals])
        feedback_error = max(feedback_error, float((feedback-expected_feedback).abs().max()))
        torch.testing.assert_close(feedback, expected_feedback, atol=1e-5, rtol=1e-4)
        assert bool((robot.policy.history.n == step+1).all())
    assert all(not p.requires_grad and p.grad is None for p in robot.policy.actor.parameters())
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == bundle_hash
    report = dict(design_version=b.config['version'],
        urdf_sha256=hashlib.sha256((HERE/'models/biped_4dof.urdf').read_bytes()).hexdigest(),
        mjcf_sha256=hashlib.sha256((HERE/'models/biped_4dof.xml').read_bytes()).hexdigest(),
        local_generator_contract_passed=True, units=rows,
        root=dict(free_coordinates=['x', 'z', 'pitch'], direct_actuation=False, nq=7, nu=4),
        urdf_mjcf_fk_cases=24, urdf_mjcf_fk_max_error_m=fk_error,
        along_axis_spacing_planar_mass_matrix_max_error=mass_error,
        observation_COM_velocity_finite_difference_max_error_m_s=com_error,
        nominal_drive_10ms_torque_Nm=float(expected_tau), delay_5ms_check_passed=True,
        physical_ground_contact_observed=contact_seen,
        shared_body_explicit_wrench_mapping_passed=True,
        frozen_V2=dict(bundle=str(bundle.resolve()), sha256=bundle_hash, control_steps=100,
                       simulated_seconds=float(robot.physics.data.time), feedback_shape=[4, 197],
                       independent_histories_verified=True, batch_vs_single_action_max_error=action_error,
                       batch_vs_single_feedback_max_error=feedback_error,
                       parameters_unchanged=True),
        limitations=['Generator-compatible local parameters are not exact replayed structures from the finite training bank.',
                     'Biped branching, simultaneous ground contact and neighboring learned controllers remain a new composition.',
                     'The along-axis spacing equivalence applies to planar inertial/gravity terms, not unrestricted 3D dynamics or identical collision sets.',
                     'The 1 s frozen-policy run tests integration and finite signals, not standing or walking.'],
        full_training_distribution_match=False, walking_validated=False)
    (HERE/'compatibility.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'units'}, ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    run()
