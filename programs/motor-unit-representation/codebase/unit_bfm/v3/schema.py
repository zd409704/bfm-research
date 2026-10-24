"""Frozen V3 SI feature registry. Physics owns its separate, generated registry."""
from dataclasses import asdict, dataclass
import hashlib
import json
import math
import numpy as np

VERSION = 'LOCAL_RESPONSE_ASYM_FB_V3'
SCHEMA_VERSION = 'v3-core-si-1'
ESTIMATOR_VERSION = 'causal-5point-linear-dq-1'
G_DIM, X_DIM, Z_DIM = 13, 137, 16
CONTROL_DT, PHYSICS_DT = .01, .001
RING_SIZE = 22

@dataclass(frozen=True)
class Field:
    name: str
    scale: float
    units: str
    source: str
    time: str = 'current_boundary'
    reference: str = 'canonical_output/M'


def field(name, scale, units, source, time='current_boundary'):
    return Field(name, scale, units, source, time)

G_SCHEMA = tuple(field(*v) for v in [
    ('length_P', .4, 'm', 'known'), ('length_D', .4, 'm', 'known'),
    ('q', math.pi, 'rad', 'telemetry'), ('dq', 6., 'rad/s', 'telemetry'),
    ('tau_endpoint', 6., 'N*m', 'privileged_exact_axis_telemetry'),
    ('q_min', math.pi, 'rad', 'known'), ('q_max', math.pi, 'rad', 'known'),
    ('v_tip_x', 3., 'm/s', 'local_kinematics'), ('v_tip_z', 3., 'm/s', 'local_kinematics'),
    ('ddq_hat', 200., 'rad/s^2', 'causal_5point_fit'),
    ('a_tip_x', 100., 'm/s^2', 'causal_5point_fit'),
    ('a_tip_z', 100., 'm/s^2', 'causal_5point_fit'), ('acc_valid', 1., 'bool', 'estimator')])
G_SCHEMA = tuple(Field(f.name,f.scale,f.units,f.source,
                       'causal_5_endpoints/40ms_fit' if f.name in ('ddq_hat','a_tip_x','a_tip_z','acc_valid') else f.time,
                       f.reference) for f in G_SCHEMA)
RIGID_SCHEMA = tuple(field(f'{side}.{name}', scale, units, 'known')
    for side in ('P', 'D') for name, scale, units in
    [('mass', 2., 'kg'), ('COM_x', .4, 'm'), ('COM_z', .4, 'm'), ('I_yy', .1, 'kg*m^2')])
DRIVE_SCHEMA = tuple(field(name, scale, units, 'known') for name, scale, units in [
    ('request_scale', 6., 'N*m'), ('lower', 6., 'N*m'), ('upper', 6., 'N*m'),
    ('T_s', .01, 's'), ('delay_s', .01, 's'), ('damping', .08, 'N*m*s/rad'),
    ('friction', .08, 'N*m'), ('armature', .006, 'kg*m^2')])
SLOW_SCHEMA = tuple(field(n,s,u,'telemetry','even_endpoint/preceding_2_intervals') for n,s,u in
    [('q',math.pi,'rad'),('dq',6.,'rad/s'),('tau_mean',6.,'N*m'),
     ('u_mean',1.,'1'),('padding',1.,'bool'),('age',.2,'s')])
FAST_SCHEMA = tuple(field(n,s,u,'telemetry','preceding_interval_endpoint') for n,s,u in
    [('u_previous',1.,'1'),('tau_endpoint',6.,'N*m'),('padding',1.,'bool'),('age',.08,'s')])
MEMORY_ROW_SCHEMA = tuple(field(n,s,u,'feature_memory','boundary_age/preceding_interval') for n,s,u in
    [('q',math.pi,'rad'),('dq',6.,'rad/s'),('tau_endpoint',6.,'N*m'),('u_previous',1.,'1'),
     ('tau_integral',.06,'N*m*s'),('u_integral',.01,'s'),('interval_dt',.01,'s'),
     ('interval_valid',1.,'bool'),('age',.22,'s'),('valid',1.,'bool'),('present',1.,'bool')])
MEMORY_WIDTH = len(MEMORY_ROW_SCHEMA)
MEMORY_DIM = RING_SIZE * MEMORY_WIDTH + 1

def _expanded(rows, count, prefix):
    return tuple(Field(f'{prefix}[{i}].{f.name}',f.scale,f.units,f.source,f.time,f.reference)
                 for i in range(count) for f in rows)

def _masks(rows):
    return tuple(field(f'{f.name}.valid',1.,'bool','known') for f in rows)

X_SCHEMA = (G_SCHEMA + RIGID_SCHEMA + _masks(RIGID_SCHEMA) + DRIVE_SCHEMA + _masks(DRIVE_SCHEMA)
            + _expanded(SLOW_SCHEMA,10,'slow') + _expanded(FAST_SCHEMA,8,'fast'))
MEMORY_SCHEMA = _expanded(MEMORY_ROW_SCHEMA,RING_SIZE,'memory') + (field('slow_phase',1.,'bool','feature_memory'),)
G_SCALES = np.array([f.scale for f in G_SCHEMA])
RIGID_SCALES = np.array([f.scale for f in RIGID_SCHEMA])
DRIVE_SCALES = np.array([f.scale for f in DRIVE_SCHEMA])
SLOW_SCALES = np.array([f.scale for f in SLOW_SCHEMA])
FAST_SCALES = np.array([f.scale for f in FAST_SCHEMA])
MEMORY_SCALES = np.array([f.scale for f in MEMORY_ROW_SCHEMA])


def registry():
    return {k:[asdict(f) for f in rows] for k,rows in
            [('g',G_SCHEMA),('x',X_SCHEMA),('memory',MEMORY_SCHEMA)]}

SCHEMA_HASH = hashlib.sha256(json.dumps(registry(),sort_keys=True).encode()).hexdigest()


def concatenate_privileged(physics_p, memory):
    """p_total=[physics_p,feature_memory]; no guessed physics dimension."""
    physics_p, memory = np.asarray(physics_p), np.asarray(memory)
    if physics_p.ndim != 1 or memory.shape != (MEMORY_DIM,):
        raise ValueError('Expected 1D physics p and complete feature memory')
    if not np.isfinite(physics_p).all() or not np.isfinite(memory).all():
        raise ValueError('Nonfinite privileged input')
    return np.concatenate((physics_p,memory)).astype(np.float32)


@dataclass(frozen=True)
class CoordinateMap:
    """Output-side telemetry adapter only; never reapplied to env boundaries.

    Rotor units require an upstream, explicit transmission model.
    """
    axis_sign: int = 1
    canonical_angle_at_encoder_zero_rad: float = 0.
    calibration_valid: bool = True
    source: str = 'declared_output_side_calibration'
    version: str = 'canonical-output-1'

    def __post_init__(self):
        if self.axis_sign not in (-1,1) or not math.isfinite(self.canonical_angle_at_encoder_zero_rad):
            raise ValueError('Invalid coordinate map')

    def _check(self):
        if not self.calibration_valid:
            raise ValueError('Trusted calibration required for canonical geometry')

    def canonical(self,q,dq,tau):
        self._check()
        s = self.axis_sign
        return (s*np.asarray(q)+self.canonical_angle_at_encoder_zero_rad,
                s*np.asarray(dq),s*np.asarray(tau))

    def limits(self, raw_limits):
        self._check()
        return np.sort(self.axis_sign*np.asarray(raw_limits)+self.canonical_angle_at_encoder_zero_rad)

    def torque_limits(self, raw_limits):
        self._check()
        return np.sort(self.axis_sign*np.asarray(raw_limits))

    def request(self,u_c,request_scale,device_scale=None):
        self._check()
        device_scale = request_scale if device_scale is None else device_scale
        if request_scale <= 0 or device_scale <= 0:
            raise ValueError('Positive request scales required')
        return self.axis_sign*(request_scale/device_scale)*np.asarray(u_c)
