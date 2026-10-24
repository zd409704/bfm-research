import copy
import json
import unittest
import numpy as np
import mujoco
from unit_bfm.v3.physics import UnitEnv,make_scene,Drive
from unit_bfm.v3.privileged import PHYSICS_SCHEMA,INDEX,SCALES


def fixture(**kw):
    base=dict(tilt=0.,lengths=(.3,.3),masses=(.6,.6),mass_error=False,drive_error=False,
              load_force=2.,load_side='D',load_couple=0.,load_mode='single',load_repeats=1,fixture_mode='auto',neighbour_sides='both',support_frequency=.5,support_angle_motion=0.,support_horizontal_preload=0.,support_torque_preload=0.,object_speed=0.,support_k=(80.,250.,1.),support_damping_ratio=.7,support_preload=.5,support_motion=.02,
              neighbour_amplitude=.3,neighbour_frequency=.7,neighbour_phase=0.,neighbour_kp=8.,neighbour_kd=.5,neighbour_capacity=3.6,object_mass=.5,object_radius=.04,capacity_multiplier=1.,response_s=.01,delay_ms=5)
    base.update(kw);return make_scene(**base)


class PhysicsCPU(unittest.TestCase):
    def test_all_templates_schema_and_episode_contract(self):
        for scene in ('E0','E1','E2','E3','E4'):
            for side in ('P','D'):
                with self.subTest(scene=scene,side=side):
                    env=UnitEnv(fixture(scene=scene,fixed_side=side,duration=.06))
                    reset=env.reset(4);saved=reset['p'].copy()
                    self.assertFalse(reset['interval_valid']);self.assertEqual(reset['p'].shape,(env.p_dim,))
                    self.assertFalse(reset['p'].flags.writeable)
                    json.dumps(env.metadata);json.dumps(env.config.to_dict())
                    for _ in range(6):b=env.step(.2)
                    self.assertTrue(b['truncated']);self.assertFalse(b['terminated']);self.assertTrue(b['valid'])
                    self.assertAlmostEqual(b['time'],.06,12);self.assertAlmostEqual(b['u_integral'],.002)
                    self.assertTrue(np.isfinite(b['p']).all());np.testing.assert_array_equal(reset['p'],saved)
                    with self.assertRaises(RuntimeError):env.step(0.)
                    self.assertTrue(all(set(('name','scale','source','units','time','reference'))<=set(f) for f in env.physics_schema))
                    self.assertEqual(env.physics_schema,list(PHYSICS_SCHEMA))
                    self.assertGreater(env.metadata['geometry_gate']['min_distance'],1e-5)
                    self.assertTrue(env.model.opt.disableflags & mujoco.mjtDisableBit.mjDSBL_FILTERPARENT)

    def test_geometry_family_independent_wide_gate_and_random_streams(self):
        for g in range(36):
            for side in ('P','D'):
                env=UnitEnv(make_scene(geometry_id=g,fixed_side=side,initial_fraction=.5))
                self.assertLess(env.limits[0],-1.2);self.assertGreater(env.limits[1],1.2)
                gate=env.metadata['geometry_gate']
                self.assertGreater(gate['min_distance'],gate['continuous_bound_m'])
                self.assertGreater(len(gate['pairs']),48)
        a=UnitEnv(fixture(reset_mode='stratified'),seed=123)
        b=UnitEnv(fixture(reset_mode='stratified'),seed=123)
        np.testing.assert_array_equal(a.reset(27)['p'],b.reset(27)['p'])
        self.assertNotEqual(a.reset(28)['q'],b.reset(27)['q'])
        c=UnitEnv(fixture(ballast_ratios=(.2,.2),ballast_fractions=(.8,.8)))
        d=UnitEnv(fixture(ballast_ratios=(.2,.2),ballast_fractions=(.2,.2)))
        self.assertNotAlmostEqual(c.known['rigid'][7],d.known['rigid'][7])

    def test_drive_capacity_delay_and_true_integral(self):
        for C in (3.,6.,9.):
            for ratio in (.8,1.2):
                env=UnitEnv(fixture(capacity_nominal=C,capacity_multiplier=ratio,response_s=.01,delay_ms=7))
                b=env.step(1.);expected=C*ratio*(1-np.exp(-np.arange(1,4)*.001/.01))
                self.assertAlmostEqual(b['tau_endpoint'],expected[-1],12)
                self.assertAlmostEqual(b['tau_integral'],sum(expected)*.001,12)
                self.assertNotAlmostEqual(b['tau_integral'],b['tau_endpoint']*.01,7)
                for _ in range(20):b=env.step(1.)
                self.assertAlmostEqual(b['tau_endpoint'],C*ratio,7)
                self.assertTrue(b['diagnostics']['saturated'])
        d=Drive(7.5,6,.01,10)
        self.assertTrue(all(d.advance(1)==0 for _ in range(10)))
        self.assertGreater(d.advance(1),0)
        np.testing.assert_array_equal(d.queue,np.full(11,7.5))

    def test_fixed_D_identity_geometry_power_and_encoder_equivalence(self):
        for side in ('P','D'):
            a=UnitEnv(fixture(fixed_side=side,initial_q=.6,initial_dq=.2,encoder_sign=1,beta_encoder=0.))
            b=UnitEnv(fixture(fixed_side=side,initial_q=.6,initial_dq=.2,encoder_sign=-1,beta_encoder=1.2))
            O,R=a._frame();np.testing.assert_allclose(R.T@(a._tip('P')-O),[0,0,.3],atol=1e-12)
            np.testing.assert_allclose(R.T@(a._tip('D')-O),[-.3*np.sin(.6),0,-.3*np.cos(.6)],atol=1e-12)
            for _ in range(10):
                x=a.step(.25);y=b.step(.25)
                self.assertAlmostEqual(x['q'],y['q'],12);np.testing.assert_allclose(x['p'],y['p'],atol=1e-12)
                self.assertAlmostEqual(a.data.qfrc_applied[a.vadr]*a.data.qvel[a.vadr],x['tau_endpoint']*x['dq'],12)
            zero=UnitEnv(fixture(fixed_side=side,initial_q=1.2,encoder_sign=-1,beta_encoder=1.2))
            self.assertAlmostEqual(zero.reset()['diagnostics']['raw_encoder_q'],0)
            Oz,Rz=zero._frame();Oa,Ra=a._frame()
            self.assertGreater(np.linalg.norm(Rz.T@(zero._tip('D')-Oz)-Ra.T@(a._tip('D')-Oa)),1e-2)

    def test_rigid_force_and_angular_momentum_balance(self):
        # Independent analytic acceleration of a body rotating about a fixed hinge.
        for side in ('P','D'):
            env=UnitEnv(fixture(fixed_side=side,initial_q=.5,initial_dq=.2,load_force=0.,friction=0.))
            env.step(.4);s=env._solve;m,d=env.model,env.data
            d.qpos[:]=s['q'];d.qvel[:]=s['dq'];mujoco.mj_forward(m,d);mujoco.mj_rnePostConstraint(m,d)
            b=env.body_ids['D' if side=='P' else 'P'];O,R=env._frame()
            omega=d.xaxis[env.motor]*d.qvel[env.vadr];alpha=d.xaxis[env.motor]*d.qacc[env.vadr]
            r=d.xipos[b]-O;acc=np.cross(alpha,r)+np.cross(omega,np.cross(omega,r))
            T,F=d.cfrc_int[b,:3],d.cfrc_int[b,3:];C=d.subtree_com[m.body_rootid[b]]
            np.testing.assert_allclose(F,m.body_mass[b]*(acc-m.opt.gravity),atol=1e-9)
            rot=d.ximat[b].reshape(3,3);I=rot@np.diag(m.body_inertia[b])@rot.T
            np.testing.assert_allclose(T+np.cross(C-d.xipos[b],F),I@alpha+np.cross(omega,I@omega),atol=1e-9)
            np.testing.assert_allclose(s['connections']['D' if side=='P' else 'P'][1:4],R.T@F,atol=1e-9)
            np.testing.assert_allclose(s['connections']['D' if side=='P' else 'P'][4:],R.T@(T+np.cross(C-O,F)),atol=1e-9)

    def test_contact_same_solve_global_linear_balance(self):
        env=UnitEnv(fixture(scene='E4'))
        for _ in range(180):
            env.step(.1)
            if env._solve['contacts']:break
        m=env.model;s=env._solve;d=mujoco.MjData(m)
        d.qpos[:]=s['q'];d.qvel[:]=s['dq'];mujoco.mj_forward(m,d)
        eps=1e-6;plus=mujoco.MjData(m);minus=mujoco.MjData(m)
        for scratch,sign in ((plus,1),(minus,-1)):
            scratch.qpos[:]=s['q'];mujoco.mj_integratePos(m,scratch.qpos,s['dq'],sign*eps)
            mujoco.mj_kinematics(m,scratch);mujoco.mj_comPos(m,scratch)
        inertial=np.zeros(3)
        for b in range(1,m.nbody):
            J=np.zeros((3,m.nv));Jp=J.copy();Jm=J.copy();rot=J.copy()
            mujoco.mj_jacBodyCom(m,d,J,rot,b);mujoco.mj_jacBodyCom(m,plus,Jp,rot,b);mujoco.mj_jacBodyCom(m,minus,Jm,rot,b)
            acc=J@s['qacc']+(Jp-Jm)@(s['dq'])/(2*eps)
            inertial+=m.body_mass[b]*(acc-m.opt.gravity)
        external=env.data.xfrc_applied[:, :3].sum(axis=0)
        # World-referenced slide damping is an external force, not a contact.
        for j in range(m.njnt):
            if m.jnt_type[j]==mujoco.mjtJoint.mjJNT_SLIDE and m.body_parentid[m.jnt_bodyid[j]]==0:
                va=m.jnt_dofadr[j];external+=d.xaxis[j]*(-m.dof_damping[va]*s['dq'][va])
        for row in s['contacts']:
            b0,b1=m.geom_bodyid[int(row[1])],m.geom_bodyid[int(row[2])]
            if b0==0:external+=s['rotation']@np.array(row[10:13])
            elif b1==0:external-=s['rotation']@np.array(row[10:13])
        np.testing.assert_allclose(inertial,external,atol=2e-5,rtol=1e-6)
        self.assertGreater(len(s['contacts']),0)

    def test_same_solve_snapshot_not_refreshed_with_next_action(self):
        env=UnitEnv(fixture(scene='E4',initial_q=.2,initial_dq=1.))
        b=env.step(.5);snapshot=copy.deepcopy(env._solve)
        self.assertAlmostEqual(b['time']-snapshot['time'],.001,12)
        self.assertGreater(np.linalg.norm(snapshot['q']-env.data.qpos),0)
        p=b['p'].copy();env.step(-.5);np.testing.assert_array_equal(b['p'],p)
        self.assertAlmostEqual(p[INDEX['clock.solve_time']]*10,snapshot['time'])
        # A currently configured deterministic generator must be distinguishable before onset.
        # Future independent stochastic events are not used by this template.
        a=UnitEnv(fixture(load_start=2.,load_end=3.));c=UnitEnv(fixture(load_start=4.,load_end=7.))
        self.assertGreater(np.max(abs(a.reset()['p']-c.reset()['p'])),0.)
        self.assertAlmostEqual(a.step(0)['q'],c.step(0)['q'])

    def test_sustained_E4_contact_bilateral_neighbour_and_release(self):
        for side in ('P','D'):
            env=UnitEnv(fixture(scene='E4',fixed_side=side,load_start=.2,load_end=1.2))
            run=longest=0;max_contact=0.;release=False;loaded=False
            for _ in range(180):
                b=env.step(.1);d=b['diagnostics'];self.assertTrue(b['valid'])
                simultaneous=d['contact_active'] and d['bilateral_active'] and d['neighbour_active']
                run=run+1 if simultaneous else 0;longest=max(longest,run)
                max_contact=max(max_contact,d['contact_force']);loaded|=d['load_active'];release|=d['released']
                self.assertLess(d['max_penetration'],.02)
            self.assertGreaterEqual(longest,50,(side,longest))
            self.assertGreater(max_contact,.1);self.assertTrue(loaded and release)
            self.assertTrue(all(abs(drive.tau)>1e-4 for drive in env.drives[1:]))

    def test_applied_load_moment_point_and_no_hidden_known(self):
        env=UnitEnv(fixture(load_start=0,load_end=1,load_side='D',load_angle=0,load_fraction=.8,load_force=2,initial_q=.4))
        env.step(0.);s=env._solve;row=s['loads'][0]
        np.testing.assert_allclose(row[9:12],np.cross(row[3:6],row[6:9]),atol=1e-12)
        base=UnitEnv(fixture(mass_error=True,drive_error=True,density_multiplier=.8,capacity_multiplier=.8))
        alt=UnitEnv(fixture(mass_error=True,drive_error=True,density_multiplier=1.2,capacity_multiplier=1.2))
        for key in base.known:np.testing.assert_allclose(base.known[key],alt.known[key],atol=1e-12)
        self.assertNotEqual(base.reset()['p'][INDEX['body.P.mass']],alt.reset()['p'][INDEX['body.P.mass']])
        with self.assertRaises(ValueError):make_scene(weld=True)

if __name__=='__main__':unittest.main()
