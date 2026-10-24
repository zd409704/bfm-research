"""Cross-audit regressions: distinguish physically different successors in F."""
import copy
import unittest
from dataclasses import replace
import numpy as np
import mujoco

class InputSufficiencyRegressionTests(unittest.TestCase):
    def test_support_parameters_visible_before_first_solve(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        base=make_scene(seed=81,scene='E1',initial_q=0.,initial_fraction=None,initial_dq=0.,reset_mode='configured')
        a=UnitEnv(base);b=UnitEnv(replace(base,support_k=(180.,450.,4.)))
        try:
            pa=a.reset()['p'];pb=b.reset()['p']
            self.assertGreater(np.max(abs(pa-pb)),1e-6,'support entity parameters must exist before first solve')
        finally:a.close();b.close()

    def test_ground_distance_visible_in_privileged_state(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        base=make_scene(seed=81,scene='E2',initial_q=0.,initial_fraction=None,initial_dq=0.,reset_mode='configured',load_force=0.)
        es=[UnitEnv(base),UnitEnv(base)];bs=[]
        try:
            for e,extra in zip(es,[0.,.2]):
                m,d=e.model,e.data
                bottom=min(d.geom_xpos[i,2]-m.geom_rbound[i] for i in range(m.ngeom) if m.geom_bodyid[i]!=0)
                shift=.002-bottom+extra
                for name in ('root_z','object_z'):
                    j=m.joint(name).id;d.qpos[m.jnt_qposadr[j]]+=shift;d.qvel[m.jnt_dofadr[j]]=-1.
                for v in e._anchors.values():v[2]+=shift
                e._object_base[2]+=shift
                mujoco.mj_forward(m,d);bs.append(e._boundary(False))
            self.assertGreater(np.max(abs(bs[0]['p']-bs[1]['p'])),1e-4,'pre-contact geometry must distinguish floor separation')
        finally:
            for e in es:e.close()

    def test_raw_invalid_cannot_be_overridden_by_explicit_valid(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        from unit_bfm.v3.collect import collect_episode
        env=UnitEnv(make_scene(seed=81,duration=.1))
        try:ep=collect_episode(env,'invalid_mask',max_steps=10)
        finally:env.close()
        ep.raw[3]['valid']=False;ep.valid=np.ones(len(ep),bool)
        try:ep.validate()
        except ValueError:return
        self.assertFalse(ep.valid[2] or ep.valid[3],'invalid raw boundary was sampled as valid transition')

    def test_strict_distribution_rejects_missing_expected_configuration(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        from unit_bfm.v3.collect import collect_episode
        from unit_bfm.v3.replay import Replay,EmptyReplayGroup
        from tempfile import TemporaryDirectory
        env=UnitEnv(make_scene(seed=81,duration=.1))
        try:ep=collect_episode(env,'strict_missing',max_steps=10)
        finally:env.close()
        ep.config_id='present';other=copy.deepcopy(ep);other.source='policy'
        with TemporaryDirectory() as tmp:
            r=Replay(tmp,scene_weights={'E0':1.},expected_configs={'E0':['present','missing']},strict=True)
            r.episodes=[ep,other]
            with self.assertRaises(EmptyReplayGroup):r.distribution()

if __name__=='__main__':unittest.main()
