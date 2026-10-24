"""Check causal perturbation/command replay physics, not learned policy quality."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
from unit_bfm.eval_web import data
from unit_bfm.eval_web.live import Experiment, config, pulse_config, pulse_mean


class TestPolicy:
    # Deliberately simple feedback policy to test the three-copy harness.
    def actor(self, x, z):
        return (.4*(.3-x[:,0]*1.2)-.1*x[:,1]*6).clamp(-1,1)[:,None]


class TestLearner:
    net=TestPolicy()
    def encode(self, alpha):
        z=torch.zeros(len(alpha),16);z[:,0]=4
        return z


class LiveEvaluationTest(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/'fake.pt').write_bytes(b'test-only checkpoint')
        self.mock_root=patch.object(data,'ARTIFACTS',self.root)
        self.mock_root.start()

    def tearDown(self):
        self.mock_root.stop();self.tmp.cleanup()

    def experiment(self,name,role=0):
        return Experiment(TestLearner(),config(dict(role=role,duration=5)),self.root/name,'fake.pt')

    def test_undisturbed_copies_are_identical_and_pulse_does_not_leak_to_reference(self):
        e=self.experiment('perturbed');control=self.experiment('control')
        for _ in range(30):
            r=e.advance();control.advance()
            np.testing.assert_array_equal(r['y'][0],r['y'][1])
            np.testing.assert_array_equal(r['y'][1],r['y'][2])
        e.inject(dict(fx=4,duration=.25))
        for _ in range(80):
            r=e.advance();c=control.advance()
            np.testing.assert_array_equal(r['y'][2],c['y'][2])
        self.assertGreater(np.max(np.abs(np.array([r['y'][1,0]-r['y'][2,0] for r in e.records]))),.01)
        self.assertGreater(np.max(np.abs(np.array([r['y'][0,13]-r['y'][1,13] for r in e.records]))),.001)

    def test_force_on_fixed_parent_is_absorbed_without_inventing_motor_motion(self):
        e=self.experiment('fixed')
        e.inject(dict(side='P',fx=4,my=1))
        for _ in range(50):
            r=e.advance()
            np.testing.assert_array_equal(r['y'][0,:14],r['y'][2,:14])
        self.assertGreater(max(float(r['y'][0,18]) for r in e.records),0)

    def test_pulse_is_causal_and_view_uses_interval_mean(self):
        e=self.experiment('causal')
        for _ in range(10):e.advance()
        p=e.inject(dict(fx=4,duration=.25))
        self.assertAlmostEqual(p['start'],.1)
        self.assertFalse(any(r['perturbations'] for r in e.records))
        row=e.advance()
        expected=4*pulse_mean(p,.11)
        self.assertAlmostEqual(row['perturbations'][0]['fx'],expected)
        self.assertAlmostEqual(float(row['y'][0,21])*20,expected,places=6)
        self.assertAlmostEqual(float(row['y'][1,21])*20,expected,places=6)
        self.assertEqual(float(row['y'][2,21]),0)

    def test_invalid_force_does_not_change_state(self):
        e=self.experiment('invalid')
        for bad in ({'fx':float('nan')},{'side':'X'},{'duration':0},{'fraction':-1}):
            with self.assertRaises(ValueError):e.inject(bad)
        self.assertEqual(e.events,[])
        self.assertEqual(len(e.units[0].s['pulses']),0)
        with self.assertRaises(ValueError):config({'role':1.5})

    def test_paused_single_step_advances_exactly_one_control_interval(self):
        e=self.experiment('single_step');e.inject(dict(fx=4,duration=.25))
        e.control('step')
        self.assertEqual(len(e.records),1)
        self.assertEqual(int(e.units[0].s['clock']),10)
        self.assertEqual(e.status,'paused')
        self.assertTrue(e.records[0]['perturbations'])

    def test_stop_while_paused_saves_all_three_branches(self):
        e=self.experiment('web_evaluations/saved');e.launch();e.control('pause')
        for _ in range(10):e.advance()
        e.control('stop');e.thread.join(timeout=3)
        self.assertFalse(e.thread.is_alive())
        for name in ('feedback','replay','reference'):
            with np.load(e.folder/name/'R0_100.npz',allow_pickle=False) as a:
                self.assertEqual(a['y'].shape,(1,len(e.records),25))
        self.assertTrue((e.folder/'job.json').is_file())
        result=data.trajectory('web_evaluations/saved/feedback','R0_100.npz',0)
        self.assertEqual(len(result['comparison']['time']),len(e.records))
        self.assertEqual(len(result['perturbations']),len(e.records))

    def test_custom_physics_updates_actual_model_but_keeps_hidden_parameters_hidden(self):
        import mujoco
        p=dict(lp=.32,ld=.42,mp=1.3,md=.4,bp=.1,bd=.2,density_p=1.15,
               density_d=.85,damping=.06,friction=.04,armature=.005,
               cap=5,tm=.017,delay=7,lower=-.6,upper=.9,tilt=.2)
        e=Experiment(TestLearner(),config(dict(physics=p)),self.root/'custom','fake.pt')
        m=e.units[0].model;j=m.joint('motor').id;dof=m.jnt_dofadr[j]
        np.testing.assert_allclose(m.jnt_range[j],[-.6,.9])
        self.assertAlmostEqual(m.body_mass[m.body('P').id],1.3*1.1*1.15)
        self.assertAlmostEqual(m.body_mass[m.body('D').id],.4*1.2*.85)
        self.assertAlmostEqual(float(e.m[0,2])*2,1.3*1.1,places=6)
        self.assertAlmostEqual(m.dof_damping[dof],.06)
        self.assertAlmostEqual(m.dof_frictionloss[dof],.04)
        self.assertAlmostEqual(m.dof_armature[dof],.005)
        self.assertEqual(int(e.units[0].s['delay']),7)
        self.assertEqual(float(e.units[0].s['cap']),5)
        np.testing.assert_allclose(e.m[0,10:12].numpy()*1.2,[-.6,.9],atol=1e-7)
        for _ in range(20):row=e.advance()
        q=float(row['y'][0,0])*1.2
        np.testing.assert_allclose(row['y'][0,16:18],[(q+.6)/2.4,(.9-q)/2.4],atol=1e-7)
        e.save()
        restored=mujoco.MjModel.from_xml_path(str(e.folder/'feedback/R0_100.xml'))
        for name in ('body_mass','body_inertia','body_ipos','dof_damping','dof_frictionloss','dof_armature','jnt_range'):
            np.testing.assert_allclose(getattr(m,name),getattr(restored,name))
        view=data.decode(e.folder/'feedback/R0_100.npz',dict(np.load(e.folder/'feedback/R0_100.npz')),0,'live')
        np.testing.assert_allclose(view['joint_limits'],[-.6,.9])

    def test_limit_is_a_physical_constraint_not_just_display(self):
        class PushPolicy:
            def actor(self,x,z):return torch.ones((len(x),1))
        learner=TestLearner();learner.net=PushPolicy()
        e=Experiment(learner,config(dict(physics=dict(lower=-.4,upper=.5),target=1.5)),self.root/'limit','fake.pt')
        for _ in range(150):e.advance()
        q=np.array([r['y'][0,0]*1.2 for r in e.records])
        self.assertLess(q[-50:].max(),.55)  # MuJoCo limits are compliant constraints.
        self.assertGreater(q[-50:].mean(),.35)
        self.assertTrue(e.meta['target_outside_limits'])
        self.assertIn('exceeds the physical limit',e.goal['description'])
        with self.assertRaises(ValueError):config(dict(physics=dict(lower=.2,upper=.8)))

    def test_seeded_randomization_and_external_events_are_reproducible(self):
        from unit_bfm.eval_web import parameters
        for role in range(4):
            p=parameters.sample(42,role)
            self.assertEqual(p,parameters.sample(42,role))
            self.assertEqual(parameters.outside_training(p,role),[])
            self.assertEqual((p['lower'],p['upper']),(-1.2,1.2))
            parameters.validate(p)
        opts=config(dict(seed=42,auto_pulses=True))
        e=Experiment(TestLearner(),opts,self.root/'seed1','fake.pt')
        f=Experiment(TestLearner(),opts,self.root/'seed2','fake.pt')
        self.assertEqual(e.events,f.events)
        np.testing.assert_array_equal(e.units[0].s['pulses'],e.units[1].s['pulses'])
        self.assertEqual(len(e.units[2].s['pulses']),0)


if __name__=='__main__':unittest.main()
