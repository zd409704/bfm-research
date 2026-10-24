"""Revision regressions from coordinator/core counterexamples; CPU only."""
import unittest
import numpy as np
import mujoco
from dataclasses import replace
from unit_bfm.v3.physics import UnitEnv,make_scene,PhysicallyInvalidTransition
from unit_bfm.v3.privileged import INDEX,SCALES


class RevisionPhysics(unittest.TestCase):
    def test_reset_support_and_ground_observable(self):
        c=make_scene(scene='E1',seed=81)
        a=UnitEnv(c);b=UnitEnv(replace(c,support_k=(180.,450.,4.)))
        self.assertGreater(np.max(abs(a.reset()['p']-b.reset()['p'])),1e-4)
        self.assertEqual(a.reset()['p'][INDEX['controller.fixture'+c.fixed_side+'.present']],1.)
        c=make_scene(scene='E2',seed=81)
        a=UnitEnv(c);b=UnitEnv(c)
        j=b.model.joint('root_z').id;b.data.qpos[b.model.jnt_qposadr[j]]+=.2
        mujoco.mj_forward(b.model,b.data)
        self.assertGreater(abs(a._boundary(False)['p'][INDEX['floor.offset']]-b._boundary(False)['p'][INDEX['floor.offset']]),.1)

    def test_snapshot_exact_successor_and_new_episode_clock(self):
        for side in ('P','D'):
            c=make_scene(scene='E4',fixed_side=side,fixture_mode='both',neighbour_sides='both',duration=.1,load_start=0.,load_end=.2)
            a,b=UnitEnv(c),UnitEnv(c)
            for _ in range(4):a.step(.1)
            snap=a.snapshot();restored=b.restore(snap,episode_id='restored')
            self.assertFalse(restored['interval_valid']);self.assertEqual(restored['tau_integral'],0.)
            self.assertFalse(restored['diagnostics']['solve_valid']);self.assertAlmostEqual(restored['time'],.04)
            x,y=a.step(-.1),b.step(-.1)
            np.testing.assert_allclose(x['p'],y['p'],atol=1e-12,rtol=0)
            self.assertAlmostEqual(x['q'],y['q'],14)
            for _ in range(9):y=b.step(0.)
            self.assertTrue(y['truncated']);self.assertAlmostEqual(y['diagnostics']['episode_elapsed_s'],.1)
            wrong=UnitEnv(replace(c,lengths=(.4,.4)))
            with self.assertRaises(ValueError):wrong.restore(snap)

    def test_invalid_never_normal_terminal(self):
        e=UnitEnv(make_scene());e.step(0.)
        e.data.warning[mujoco.mjtWarning.mjWARN_BADQACC].number=1
        b=e._boundary(True)
        self.assertFalse(b['valid']);self.assertFalse(b['terminated']);self.assertFalse(b['diagnostics']['solver_valid'])
        with self.assertRaises(PhysicallyInvalidTransition) as caught:e.step(.1)
        self.assertFalse(caught.exception.boundary['terminated'])
        self.assertFalse(caught.exception.boundary['valid'])
        with self.assertRaises(RuntimeError):e.step(0.)
        e.reset();e.step(0.);e._solve['qacc'][:]=np.nan
        self.assertFalse(e._boundary(True)['valid'])

    def test_stable_catalog_independent_episode_conditions(self):
        configs=[make_scene(seed=100+i,geometry_id=8,limit_id=2,episode_id=i,variant_id=i) for i in range(160)]
        self.assertEqual(len({c.lengths for c in configs}),1)
        self.assertEqual({c.encoder_sign for c in configs},{-1,1})
        self.assertEqual({c.load_side for c in configs},{'P','D'})
        self.assertEqual({c.load_frame for c in configs},{'world','body'})
        self.assertEqual({c.load_point_bin for c in configs},set(range(5)))
        self.assertEqual({c.load_direction_bin for c in configs},set(range(8)))
        self.assertGreater(len({c.ballast_ratios for c in configs}),150)
        for c in configs:self.assertLessEqual(c.load_force,.5*sum(c.masses)*(c.density_multiplier if c.mass_error else 1.)*9.81)
        envs=[UnitEnv(configs[i]) for i in (0,9,19)]
        self.assertEqual(len({e.limits for e in envs}),1)

    def test_topology_variants_and_repeated_events(self):
        configs=[make_scene(scene='E4',variant_id=i) for i in range(12)]
        self.assertEqual(sum(c.fixture_mode=='both' for c in configs),3)
        for side in ('P','D'):
            for adjacent,count in [('P',1),('D',1),('both',2)]:
                e=UnitEnv(make_scene(scene='E3',fixed_side=side,neighbour_sides=adjacent))
                self.assertEqual(len(e.neighbours),count)
                self.assertEqual(e.metadata['actual_tags']['neighbour_count'],count)
        e=UnitEnv(make_scene(scene='E0',load_mode='repeated',load_start=.02,load_end=.06,load_period=.40,load_repeats=3))
        phases=[]
        for _ in range(100):phases.append(e.step(0.)['diagnostics']['load_active'])
        self.assertEqual(sum(a and not b for a,b in zip(phases[1:],phases[:-1])),3)
        self.assertEqual(sum(b and not a for a,b in zip(phases[1:],phases[:-1])),3)

    def test_wide_reset_and_si_diagnostics(self):
        for mode in ('xi','velocity'):
            for seed in range(10):
                for side in ('P','D'):
                    e=UnitEnv(make_scene(seed=200+seed,scene='E4',fixed_side=side,geometry_id=seed,reset_mode=mode),seed=seed)
                    self.assertGreaterEqual(e._scene_distance(),-1e-5)
        e=UnitEnv(make_scene(scene='E4',fixture_mode='both',load_start=0.,load_end=1.))
        b=e.step(.1);d=b['diagnostics']
        for key in ('contact_normal_force_N','adjacent_max_abs_dq','adjacent_max_abs_tau_Nm','adjacent_declared_capacity_Nm','fixture_P_force_N','fixture_D_force_N','fixture_P_torque_Nm','fixture_D_torque_Nm','applied_load_norm_N','solver_valid'):
            self.assertIn(key,d)
        self.assertAlmostEqual(d['applied_load_norm_N'],e.config.load_force)
        self.assertTrue(d['interval_all_solver_valid']);self.assertEqual(d['interval_solve_count'],10)

    def test_random_initialization_probe(self):
        # Exact original 100 configuration identities; independently validate all pairs.
        for seed in range(10):
            for scene in ('E0','E1','E2','E3','E4'):
                for side in ('P','D'):
                    e=UnitEnv(make_scene(seed=100+seed,geometry_id=seed,limit_id=seed%4,scene=scene,fixed_side=side))
                    self.assertGreaterEqual(e._scene_distance(),-1e-5,(seed,scene,side))
                    for t in range(30):self.assertTrue(e.step(.25 if t<15 else -.25)['valid'])

if __name__=='__main__':unittest.main()
