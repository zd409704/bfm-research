"""Causal SI-to-network feature construction, with no physics imports."""
from collections import deque
import copy
import numpy as np
from .schema import (CONTROL_DT, RING_SIZE, MEMORY_DIM, MEMORY_WIDTH, G_SCALES,
                     RIGID_SCALES, DRIVE_SCALES, SLOW_SCALES, FAST_SCALES, MEMORY_SCALES)

RAW_KEYS = ('time','q','dq','tau_endpoint','u_previous','tau_integral','u_integral',
            'interval_dt','interval_valid','valid')


def tip_kinematics(length,q,dq,ddq):
    s,c = np.sin(q),np.cos(q)
    return np.array([-length*c*dq,length*s*dq]), np.array([
        length*s*dq*dq-length*c*ddq,length*c*dq*dq+length*s*ddq])


def _known(known):
    out = {}
    for key,n in [('lengths',2),('limits',2),('rigid',8),('rigid_valid',8),('drive',8),('drive_valid',8)]:
        a = np.array(known[key],dtype=np.float64,copy=True)
        if a.shape != (n,) or not np.isfinite(a).all():
            raise ValueError(f'Invalid known {key}')
        out[key] = a
    for k in ('rigid_valid','drive_valid'):
        if not np.isin(out[k],[0,1]).all():
            raise ValueError('Validity masks must be binary')
    if np.any(out['lengths'] <= 0) or out['limits'][0] >= out['limits'][1]:
        raise ValueError('Positive lengths and ordered finite limits required')
    return out


def _boundary(boundary):
    b = {k:float(boundary[k]) for k in RAW_KEYS}
    if not all(np.isfinite(v) for v in b.values()):
        raise ValueError('Nonfinite boundary; isolate invalid physical transitions')
    if b['interval_dt'] < 0 or any(b[k] not in (0,1) for k in ('valid','interval_valid')):
        raise ValueError('Invalid boundary validity/dt')
    return b


class FeatureHistory:
    """Oldest-to-newest histories. Padding=1; padded values/ages are zero.

    Reset is a real motion endpoint but has no completed execution interval.
    Inputs are already canonical; p/diagnostics/metadata are never read.
    """
    def __init__(self):
        self._ring = deque(maxlen=RING_SIZE)
        self._step = 0
        self._known = None

    def reset(self,boundary,known):
        b = _boundary(boundary)
        if b['interval_valid']:
            raise ValueError('Reset cannot have a valid previous interval')
        k = _known(known)
        self._ring.clear()
        self._ring.append(b)
        self._step,self._known = 0,k

    def append(self,boundary,known=None):
        if not self._ring:
            raise RuntimeError('Call reset before append')
        b = _boundary(boundary)
        elapsed = b['time']-self._ring[-1]['time']
        if not np.isclose(elapsed,CONTROL_DT,atol=1e-8,rtol=1e-5):
            raise ValueError('Expected consecutive 100 Hz boundaries; mark missing records invalid')
        if b['interval_valid'] and not np.isclose(b['interval_dt'],elapsed,atol=1e-8,rtol=1e-5):
            raise ValueError('Interval duration must match true boundary timestamps')
        k = self._known if known is None else _known(known)
        self._ring.append(b)
        self._known = k
        self._step += 1

    def features(self):
        if not self._ring:
            raise RuntimeError('Call reset before features')
        rows = list(self._ring)
        b,k = rows[-1],self._known
        fit = rows[-5:]
        acc_valid = len(fit)==5 and all(r['valid'] for r in fit)
        ddq = 0.
        if acc_valid:
            t = np.array([r['time'] for r in fit]); t -= t.mean()
            ddq = float(t @ np.array([r['dq'] for r in fit]) / (t @ t))
        v,a = tip_kinematics(k['lengths'][1],b['q'],b['dq'],ddq)
        if not acc_valid:
            a[:] = 0.
        g = np.array([*k['lengths'],b['q'],b['dq'],b['tau_endpoint'],*k['limits'],
                      *v,ddq,*a,float(acc_valid)]) / G_SCALES
        fast = np.zeros((8,4)); fast[:,2] = 1.
        slow = np.zeros((10,6)); slow[:,4] = 1.
        start = self._step-len(rows)+1
        def row(i):
            return rows[i-start] if start <= i <= self._step else None
        for j,i in enumerate(range(self._step-7,self._step+1)):
            r = row(i)
            if i >= 1 and r and r['valid'] and r['interval_valid']:
                fast[j] = [r['u_previous'],r['tau_endpoint'],0,b['time']-r['time']]
        last_even = self._step-self._step%2
        for j,i in enumerate(range(last_even-18,last_even+1,2)):
            r,prev = row(i),row(i-1)
            if i >= 2 and r and prev and all(vv['valid'] and vv['interval_valid'] for vv in (prev,r)):
                dt = prev['interval_dt']+r['interval_dt']
                slow[j] = [r['q'],r['dq'],(prev['tau_integral']+r['tau_integral'])/dt,
                           (prev['u_integral']+r['u_integral'])/dt,0,b['time']-r['time']]
        x = np.concatenate((g,k['rigid']*k['rigid_valid']/RIGID_SCALES,k['rigid_valid'],
                            k['drive']*k['drive_valid']/DRIVE_SCALES,k['drive_valid'],
                            (slow/SLOW_SCALES).ravel(),(fast/FAST_SCALES).ravel()))
        mem = np.zeros((RING_SIZE,MEMORY_WIDTH))
        for j,r in enumerate(rows,start=RING_SIZE-len(rows)):
            mem[j] = [r['q'],r['dq'],r['tau_endpoint'],r['u_previous'],r['tau_integral'],
                      r['u_integral'],r['interval_dt'],r['interval_valid'],b['time']-r['time'],r['valid'],1]
        memory = np.r_[(mem/MEMORY_SCALES).ravel(),self._step%2]
        out = {'g':g.astype(np.float32),'x':x.astype(np.float32),'memory':memory.astype(np.float32)}
        if not all(np.isfinite(a).all() for a in out.values()):
            raise ValueError('Nonfinite derived features; isolate this physical record')
        return out

    @classmethod
    def from_memory(cls,memory,known,current_time=0.):
        """Rebuild updater from F's memory plus current known context.

        Absolute episode time is supplied by the caller; features use ages only.
        """
        memory = np.asarray(memory,dtype=np.float64)
        if memory.shape != (MEMORY_DIM,) or not np.isfinite(memory).all():
            raise ValueError('Invalid feature memory')
        if memory[-1] not in (0,1):
            raise ValueError('Invalid slow phase')
        rows = memory[:-1].reshape(RING_SIZE,MEMORY_WIDTH)*MEMORY_SCALES
        present = rows[:,10]
        if not np.isin(present,[0,1]).all() or np.any(np.diff(present)<0) or present[-1]!=1:
            raise ValueError('Memory present mask must be a nonempty suffix')
        obj = cls(); obj._known = _known(known)
        for r in rows[present==1]:
            obj._ring.append(_boundary(dict(zip(RAW_KEYS,[current_time-r[8],*r[:8],r[9]]))))
        # Once the ring is full the absolute step is irrelevant; parity is sufficient.
        obj._step = len(obj._ring)-1
        if obj._step%2 != int(memory[-1]):
            if len(obj._ring)<RING_SIZE:
                raise ValueError('Startup phase incompatible with memory length')
            obj._step += 1
        return obj

    def state_dict(self):
        return copy.deepcopy({'rows':list(self._ring),'step':self._step,'known':self._known})
