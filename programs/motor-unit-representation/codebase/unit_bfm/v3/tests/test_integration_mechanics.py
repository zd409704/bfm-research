"""Independent geometric and actuator checks, not copied force extraction formulas."""
import unittest
import numpy as np
import mujoco


class MechanicalIntegrationTests(unittest.TestCase):
    def test_rotated_world_and_reverse_tree_obey_same_local_geometry(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        from unit_bfm.v3.features import tip_kinematics
        for side in ('P','D'):
            for tilt in (0.,1.1,-2.3):
                env=UnitEnv(make_scene(seed=5,fixed_side=side,tilt=tilt,initial_q=.4))
                try:
                    points=[]
                    h=1e-5; q=.4; dq=1.3; ddq=-.8
                    for t in (-h,0,h):
                        a=q+dq*t+.5*ddq*t*t
                        env.data.qpos[env.qadr]=env.tree_sign*a
                        mujoco.mj_forward(env.model,env.data)
                        O,R=env._frame(); points.append(R.T@(env._tip('D')-O))
                    got_v=(points[2]-points[0])/(2*h)
                    got_a=(points[2]-2*points[1]+points[0])/(h*h)
                    v,a=tip_kinematics(env.config.lengths[1],q,dq,ddq)
                    np.testing.assert_allclose(got_v[[0,2]],v,atol=1e-8)
                    np.testing.assert_allclose(got_a[[0,2]],a,atol=2e-5)
                    np.testing.assert_allclose(points[1],[-env.config.lengths[1]*np.sin(q),0,-env.config.lengths[1]*np.cos(q)],atol=1e-12)
                finally: env.close()

    def test_actual_substep_integral_against_drive_closed_form(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        for side in ('P','D'):
            for delay in (0,5,10):
                c=make_scene(seed=21,fixed_side=side,delay_ms=delay,response_s=.01,capacity_multiplier=1.,drive_error=False,load_force=0.)
                env=UnitEnv(c)
                try:
                    b=env.reset(); tau=[]
                    # Step command starts at tick 0, so a delay d activates at tick d.
                    for k in range(30):
                        active=max(0,k+1-delay)
                        tau.append(min(c.capacity_nominal,1.25*c.capacity_nominal*.6)*(1-np.exp(-active*.001/.01)))
                    for j in range(3):
                        b=env.step(.6)
                        self.assertAlmostEqual(b['tau_endpoint'],tau[10*j+9],places=10)
                        self.assertAlmostEqual(b['tau_integral'],sum(tau[10*j:10*j+10])*.001,places=10)
                        self.assertAlmostEqual(env.data.qfrc_applied[env.vadr]*env.data.qvel[env.vadr],b['tau_endpoint']*b['dq'],places=10)
                finally: env.close()

if __name__=='__main__': unittest.main()
