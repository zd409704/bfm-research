"""Protect evaluation meaning when translating saved arrays into a web view."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
from unit_bfm.eval_web import data


class EvaluationViewTest(unittest.TestCase):
    def make_data(self):
        y=np.zeros((1,500,25),np.float32)
        y[0,:,0]=.3/1.2
        y[0,:,1]=.2/6
        return dict(y=y,targets=np.array([.5],np.float32))

    def test_random_direction_has_no_invented_target_or_tracking_score(self):
        result=self.make_data()
        self.assertEqual(data.targets_for(result,0,'random_z.npz'),{})
        self.assertFalse(any('Hold' in m['label'] or 'Track' in m['label']
                             for m in data.physical_stats(result,0,'random_z.npz')))

    def test_hold_uses_terminal_second_and_physical_radians(self):
        result=self.make_data()
        result['y'][0,:400,0]=1.0/1.2
        metrics=data.physical_stats(result,0,'reward_query.npz')
        self.assertEqual(metrics[0]['label'],'RMSE, hold at last one second.')
        self.assertAlmostEqual(metrics[0]['value'],.2,places=6)

    def test_switching_uses_full_trajectory_and_requested_phase(self):
        result=self.make_data()
        result['q_target']=np.r_[np.full(250,-.6),np.full(250,.6)][None]
        metrics=data.physical_stats(result,0,'R0_100.npz')
        self.assertEqual(metrics[0]['label'],'Follow RMSE all the way.')
        self.assertAlmostEqual(metrics[0]['value'],np.sqrt((.9**2+.3**2)/2),places=6)

    def test_velocity_metric_does_not_include_limit_zone(self):
        result=self.make_data()
        result.pop('targets')
        result['alpha']=np.array([[1,2,0,0,0]])
        result['y'][0,:250,0]=1.15/1.2
        result['y'][0,:250,1]=10/6
        self.assertAlmostEqual(data.physical_stats(result,0,'R0_000.npz')[0]['value'],1.8,places=5)

    def test_custom_limits_control_velocity_ramp_and_limit_statistics(self):
        result=self.make_data();result.pop('targets')
        result['joint_limits']=np.array([[-.4,.4]])
        result['alpha']=np.array([[1,2,0,0,0]])
        result['y'][0,:,0]=.35/1.2
        target=data.targets_for(result,0,'R0_100.npz')['dq']
        np.testing.assert_allclose(target,2*(1/3)**2*(3-2/3),atol=1e-6)
        metrics=data.physical_stats(result,0,'R0_100.npz')
        self.assertIsNone(metrics[0]['value'])
        self.assertEqual(next(m['value'] for m in metrics if m['label']=='Distance from current limit < 0.1 Rad'),100)

    def test_paths_cannot_escape_through_parent_or_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'artifacts';root.mkdir()
            (root/'alias').symlink_to(Path(temp),target_is_directory=True)
            for value in ('../outside','alias/outside'):
                with self.assertRaises(ValueError):data.confined(root,value)

    def test_random_query_has_no_target_channels(self):
        result=self.make_data()
        goal=data.goal_for(Path('random_z.npz'),result,0,{})
        self.assertEqual(goal['kind'],'random')
        self.assertEqual(goal['channels'],[])

    def test_compliance_target_uses_actual_state_not_desired_posture(self):
        result=self.make_data();result.pop('targets')
        result['alpha']=np.array([[3,.5,2,.1,-.2]])
        target=data.targets_for(result,0,'R0_000.npz')
        np.testing.assert_allclose(target['tau'],-.2+2*(.5-.3)-.1*.2,atol=1e-6)
        goal=data.goal_for(Path('R0_000.npz'),result,0,target)
        self.assertEqual(goal['kind'],'compliance')
        self.assertEqual([r['key'] for r in goal['channels']],['tau'])
        self.assertNotIn('q',target)

    def test_old_switch_origin_requires_known_panel_or_explicit_metadata(self):
        result=self.make_data();result['q_target']=np.full((1,500),.6)
        path=Path('/tmp/nonexistent_unit_bfm_panel/R0_100.npz')
        # With no provenance there is no reason to assert point vs reward query.
        targets=data.targets_for(result,0,path.name)
        self.assertEqual(data.goal_for(path,result,0,targets)['query'],'unknown')
        self.assertNotIn('dq',targets)
        # The catalog separately records the provenance of the old reward panel.
        targets=data.targets_for(result,0,path.name)
        self.assertEqual(data.goal_for(path,result,0,targets,'switch_reward')['query'],'reward')

    def test_reference_pose_changes_only_motor_not_root_or_neighbours(self):
        import mujoco
        from unit_bfm.mechanics import Structure
        with tempfile.TemporaryDirectory() as temp:
            for role in (1,3):
                path=Path(temp)/f'R{role}.xml';path.write_text(Structure(role,0).xml())
                m=mujoco.MjModel.from_xml_path(str(path))
                qpos=np.tile(np.arange(m.nq)*.1,(3,1))
                target=np.array([-.6,.6,-.2])
                desired=data.desired_qpos(path,qpos,target)
                j=m.jnt_qposadr[m.joint('motor').id]
                np.testing.assert_array_equal(desired[:,j],target)
                np.testing.assert_array_equal(np.delete(desired,j,axis=1),np.delete(qpos,j,axis=1))
                np.testing.assert_array_equal(qpos,np.tile(np.arange(m.nq)*.1,(3,1)))
                pose=data.poses(path,desired);pidx=next(i for i,l in enumerate(pose['links']) if l['name']=='P')
                didx=next(i for i,l in enumerate(pose['links']) if l['name']=='D')
                for i,frame in enumerate(pose['frames']):
                    p,d=frame[pidx],frame[didx]
                    # Positive y-hinge rotation appears clockwise in screen x/z.
                    angle=lambda r:np.arctan2(-(r[2]-r[0]),-(r[3]-r[1]))
                    self.assertAlmostEqual(angle(d)-angle(p),target[i],places=6)

    def test_point_goal_reproduces_static_bias_and_switch_target(self):
        from unit_bfm.mechanics import Structure
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'R0_100.npz';path.with_suffix('.xml').write_text(Structure(0,100).xml())
            (path.parent/'metrics.json').write_text('{"nominal_query":"goal"}')
            result=self.make_data();result['phase']=np.r_[np.zeros(250,int),np.ones(250,int)][None]
            result['q_target']=np.where(result['phase']==0,-.6,.6)
            targets=data.targets_for(result,0,path.name);goal=data.goal_for(path,result,0,targets)
            self.assertEqual(goal['query'],'point')
            np.testing.assert_array_equal(goal['phase'],result['phase'][0])
            np.testing.assert_array_equal(targets['q'],result['q_target'][0])
            np.testing.assert_array_equal(targets['dq'],np.zeros(500))
            expected=.25*9.81*.35/2*np.sin(.6)
            self.assertAlmostEqual(targets['tau'][-1],expected,places=6)
            self.assertAlmostEqual(targets['tau'][0],-expected,places=6)


if __name__=='__main__':unittest.main()
