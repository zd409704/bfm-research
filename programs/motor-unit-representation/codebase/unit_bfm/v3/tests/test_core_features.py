import unittest
import numpy as np
from unit_bfm.v3.features import FeatureHistory, tip_kinematics
from unit_bfm.v3.schema import (CoordinateMap, G_SCALES, SLOW_SCALES, FAST_SCALES,
                               MEMORY_DIM, concatenate_privileged, registry)


def known():
    return dict(lengths=np.array([.3,.4]),limits=np.array([-2.,2.]),
                rigid=np.array([1,0,.15,.02,1,0,-.2,.03]),rigid_valid=np.ones(8),
                drive=np.array([7.5,-6,6,.01,.005,.03,.02,.003]),drive_valid=np.ones(8))


def boundary(i):
    t = i*.01
    return dict(time=t,q=.2+2*t+1.5*t*t,dq=2+3*t,tau_endpoint=100+i,
                u_previous=.1,tau_integral=.01*(2*i+.3),u_integral=.01*.2,
                interval_dt=.01 if i else 0.,interval_valid=bool(i),valid=True,
                p=np.array([i]),diagnostics={'world_pose':[99,99]})


class FeatureTests(unittest.TestCase):
    def history(self,n):
        h=FeatureHistory(); h.reset(boundary(0),known())
        for i in range(1,n+1): h.append(boundary(i))
        return h

    def test_registry_shapes_scales_and_padding(self):
        r=registry()
        self.assertEqual([len(r[k]) for k in ('g','x','memory')],[13,137,MEMORY_DIM])
        for rows in r.values():
            self.assertEqual(len({f['name'] for f in rows}),len(rows))
            self.assertTrue(all(f['scale']>0 and f['units'] and f['source'] and f['time'] and f['reference'] for f in rows))
        f=self.history(0).features()
        np.testing.assert_array_equal(f['x'][45:105].reshape(10,6)[:,4],1)
        np.testing.assert_array_equal(f['x'][105:].reshape(8,4)[:,2],1)
        np.testing.assert_array_equal(f['g'][9:13],0)
        self.assertAlmostEqual(f['g'][4]*6,100,places=4)
        p=concatenate_privileged(np.array([8.,9.]),f['memory'])
        np.testing.assert_array_equal(p[:2],[8,9])
        self.assertEqual(p.shape,(2+MEMORY_DIM,))

    def test_causal_fit_and_tip_finite_differences(self):
        h=self.history(4); g=h.features()['g']*G_SCALES
        self.assertAlmostEqual(g[9],3.,places=5); self.assertEqual(g[12],1)
        q,dq,ddq=.4,.8,-1.2; L=.4; dt=1e-4
        pos=lambda t: np.array([-L*np.sin(q+dq*t+.5*ddq*t*t),-L*np.cos(q+dq*t+.5*ddq*t*t)])
        v,a=tip_kinematics(L,q,dq,ddq)
        np.testing.assert_allclose(v,(pos(dt)-pos(-dt))/(2*dt),atol=1e-8)
        np.testing.assert_allclose(a,(pos(dt)+pos(-dt)-2*pos(0))/dt**2,atol=1e-8)
        # Fit quadratic velocity: slope is acceleration at window center, not endpoint.
        h=FeatureHistory()
        for i in range(5):
            b=boundary(i); b['dq']=(i*.01)**2
            h.reset(b,known()) if i==0 else h.append(b)
        self.assertAlmostEqual(float(h.features()['g'][9]*200),.04,places=6)

    def test_odd_even_true_integrals_age_and_rollover(self):
        h=self.history(20)
        a=h.features()['x'][45:105].reshape(10,6)*SLOW_SCALES
        self.assertTrue(np.all(a[:,4]==0))
        self.assertAlmostEqual(a[-1,2],39.3,places=5)
        self.assertAlmostEqual(a[-1,3],.2,places=6)
        self.assertNotAlmostEqual(a[-1,2],(119+120)/2)
        h.append(boundary(21)); b=h.features()['x'][45:105].reshape(10,6)*SLOW_SCALES
        np.testing.assert_allclose(a[:,:5],b[:,:5]); np.testing.assert_allclose(b[:,5]-a[:,5],.01,atol=2e-8)
        self.assertAlmostEqual(b[0,5],.19,places=6)
        fast=h.features()['x'][105:].reshape(8,4)*FAST_SCALES
        self.assertAlmostEqual(fast[0,3],.07,places=6)
        self.assertAlmostEqual(fast[-1,1],121.,places=4)
        h.append(boundary(22))
        self.assertEqual(len(h.state_dict()['rows']),22)

    def test_memory_reconstructs_every_phase_and_next_feature(self):
        for n in (0,1,4,19,20,21,22,23,46,47):
            h=self.history(n); f=h.features()
            clone=FeatureHistory.from_memory(f['memory'],known(),current_time=n*.01)
            np.testing.assert_allclose(clone.features()['x'],f['x'],atol=3e-6)
            h.append(boundary(n+1)); clone.append(boundary(n+1))
            for key in ('g','x','memory'):
                np.testing.assert_allclose(clone.features()[key],h.features()[key],atol=4e-6)

    def test_compressed_history_counterexample_retained_in_memory(self):
        # Equal x and current slope can hide odd-step dq needed by next fit.
        histories=[]
        for velocities in ([0,0,0,0,0],[0,.1,0,.1,0]):
            h=FeatureHistory()
            for i,dq in enumerate(velocities):
                b=boundary(i); b['q']=0.; b['dq']=dq
                h.reset(b,known()) if i==0 else h.append(b)
            histories.append(h)
        left,right=histories
        np.testing.assert_allclose(left.features()['x'],right.features()['x'],atol=1e-8)
        self.assertFalse(np.array_equal(left.features()['memory'],right.features()['memory']))
        for h in histories:
            b=boundary(5); b['q']=0.; b['dq']=0.; h.append(b)
        self.assertAlmostEqual(float(left.features()['g'][9]*200),0.)
        self.assertAlmostEqual(float(right.features()['g'][9]*200),-2.,places=6)

    def test_missing_invalid_reset_and_snapshot_isolation(self):
        h=self.history(3); b=boundary(4); b['valid']=False; b['interval_valid']=False
        h.append(b); f=h.features()
        self.assertEqual(f['g'][12],0); self.assertEqual(f['x'][-2],1)
        self.assertEqual(f['x'][45:105].reshape(10,6)[-1,4],1)
        with self.assertRaises(ValueError): h.append(boundary(6))
        h.reset(boundary(0),known()); self.assertEqual(h.features()['g'][12],0)
        b=boundary(1); k=known(); h.append(b,k); before=h.features()
        b['q']=999; k['lengths'][:]=999; before['x'][:]=999
        self.assertLess(h.features()['g'][0],2)
        with self.assertRaises(ValueError): h.reset(boundary(1),known())

    def test_privileged_and_declared_parameter_input_isolation(self):
        a,b=self.history(5),self.history(5)
        raw=boundary(6); changed=boundary(6); changed['p']*=1000000; changed['diagnostics']['world_pose']=[-9,-9]
        a.append(raw); b.append(changed)
        for key in ('x','g','memory'): np.testing.assert_array_equal(a.features()[key],b.features()[key])
        k=known(); k['drive'][0]=11.25
        b.append(boundary(7),k); a.append(boundary(7))
        np.testing.assert_array_equal(a.features()['g'],b.features()['g'])
        self.assertFalse(np.array_equal(a.features()['x'],b.features()['x']))
        k['rigid_valid'][0]=0; k['rigid'][0]=99
        b.append(boundary(8),k); self.assertEqual(b.features()['x'][13],0)

    def test_coordinate_equivalence_power_limits_and_no_wrap(self):
        q,dq,tau=3.6,.7,-2.
        for sign in (-1,1):
            for beta in (-1.1,.8):
                c=CoordinateMap(sign,beta)
                rawq=(q-beta)/sign; rawdq=dq/sign; rawtau=tau/sign
                np.testing.assert_allclose(c.canonical(rawq,rawdq,rawtau),(q,dq,tau))
                self.assertAlmostEqual(rawdq*rawtau,dq*tau)
                self.assertAlmostEqual(float(c.request(.8,7.5)),sign*.8)
                self.assertAlmostEqual(float(c.request(.8,7.5,6)),sign)
                self.assertTrue(np.all(np.diff(c.limits([-2.,1.]))>=0))
        self.assertNotEqual(float(CoordinateMap(1,.2).canonical(0,0,0)[0]),float(CoordinateMap(1,.8).canonical(0,0,0)[0]))
        with self.assertRaises(ValueError): CoordinateMap(calibration_valid=False).canonical(0,0,0)

if __name__=='__main__': unittest.main()
