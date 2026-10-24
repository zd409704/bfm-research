"""Independent, reproducible SI scene sampling; no global RNG state."""
from dataclasses import dataclass, asdict, replace
import hashlib
import numpy as np


def stream(seed, geometry_id=0, limit_id=0, episode_id=0, purpose='physics'):
    key=f'{seed}:{geometry_id}:{limit_id}:{episode_id}:{purpose}'.encode()
    return np.random.default_rng(int.from_bytes(hashlib.sha256(key).digest()[:8], 'little'))


@dataclass(frozen=True)
class SceneConfig:
    seed: int = 0
    geometry_seed: int = 0
    episode_id: int = 0
    variant_id: int = 0
    scene: str = 'E0'
    fixed_side: str = 'P'
    geometry_id: int = 0
    limit_id: int = 0
    capacity_nominal: float = 6.
    lengths: tuple = (.3, .3)
    masses: tuple = (.6, .6)
    ballast_ratios: tuple = (0., 0.)
    ballast_fractions: tuple = (.5, .5)
    density_multiplier: float = 1.
    mass_error: bool = False
    drive_error: bool = False
    capacity_multiplier: float = 1.
    response_s: float = .01
    delay_ms: int = 5
    damping: float = .03
    friction: float = .02
    armature: float = .003
    tilt: float = 0.
    encoder_sign: int = 1
    beta_encoder: float = 0.
    initial_q: float = 0.
    initial_dq: float = 0.
    initial_fraction: float | None = None
    reset_mode: str = 'configured'
    root_velocity: tuple = (0.,0.,0.)
    duration: float = 10.
    load_force: float = 2.
    load_couple: float = 0.
    load_fraction: float = .8
    load_angle: float = 0.
    load_frame: str = 'world'
    load_side: str = 'D'
    load_start: float = .2
    load_end: float = 1.7
    load_mode: str = "single"
    load_period: float = 3.
    load_repeats: int = 1
    load_point_bin: int = 0
    load_direction_bin: int = 0
    support_k: tuple = (80., 250., 1.)
    support_damping_ratio: float = .7
    support_preload: float = .5
    support_motion: float = .02
    support_frequency: float = .5
    support_angle_motion: float = .1
    support_horizontal_preload: float = 0.
    support_torque_preload: float = 0.
    fixture_mode: str = "auto"
    neighbour_sides: str = "both"
    neighbour_lengths: tuple = (.25, .25)
    neighbour_masses: tuple = (.4, .4)
    neighbour_amplitude: float = .3
    neighbour_frequency: float = .7
    neighbour_phase: float = 0.
    neighbour_kp: float = 8.
    neighbour_kd: float = .5
    neighbour_capacity: float = 3.6
    object_mass: float = .5
    object_radius: float = .04
    object_speed: float = 0.
    contact_friction: float = .7
    weld: bool = False

    def __post_init__(self):
        if self.scene not in ('E0','E1','E2','E3','E4') or self.fixed_side not in ('P','D'):raise ValueError('invalid scene/side')
        if self.weld:raise ValueError('weld disabled pending calibration')
        if self.capacity_nominal not in (3.,6.,9.) or not .8<=self.capacity_multiplier<=1.2:raise ValueError('invalid capacity family')
        if not isinstance(self.delay_ms,int) or not 0<=self.delay_ms<=10:raise ValueError('delay must be integer 0..10 ms')
        if self.reset_mode not in ('configured','stratified','xi','velocity'):raise ValueError('unsupported reset mode')
        if self.load_period<=0 or self.load_repeats<1 or self.load_end<=self.load_start:raise ValueError('invalid loader timing')
        if self.load_mode=='repeated' and self.load_period<self.load_end-self.load_start+.3:raise ValueError('repeat period must include continuous withdrawal')
        if self.support_frequency<=0 or self.object_radius<=0 or self.object_mass<=0:raise ValueError('invalid external process')
        if min(self.lengths)<=.05 or min(self.masses)<=0 or self.response_s<=0:raise ValueError('nonphysical geometry/drive')
        if not 0<=min(self.ballast_ratios)<=max(self.ballast_ratios)<=.2:raise ValueError('ballast ratio outside 0..0.2')

    def to_dict(self):
        return asdict(self)


def make_scene(seed=0, scene='E0', fixed_side='P', geometry_id=0,
               limit_id=0, capacity_nominal=6., geometry_seed=0, episode_id=0,
               variant_id=None, **overrides):
    """Stable structural catalog, independent episode conditions and explicit strata.

    Passing variant_id makes per-configuration balance schedulable. Random seed
    alone is never used for geometry. No future random draws occur during step.
    """
    g=stream(geometry_seed,geometry_id,purpose='geometry-v2')
    def rng(purpose):return stream(seed,geometry_id,limit_id,episode_id,purpose)
    r,load,support,neighbour,installation,calibration=[rng(p) for p in
        ('dynamics','loader','support','neighbour','installation','calibration')]
    v=int(rng('variant').integers(0,2**20)) if variant_id is None else int(variant_id)
    bins=(geometry_id//12%3,geometry_id//4%3)
    lengths=tuple(float(g.uniform(.15+.1*b,.25+.1*b)) for b in bins)
    masses=tuple(np.exp(r.uniform(np.log(.15),np.log(2),2)))
    density=float(r.uniform(.8,1.2));mass_error=bool(r.random()<.2)
    def balanced(purpose,n):
        # Independent permutations per purpose and block: exact marginals in a
        # scheduled block without tying sign, fixture, side or installation.
        block=v//n;order=stream(seed if variant_id is None else geometry_seed,geometry_id,limit_id,block,'strata:'+purpose).permutation(n)
        return int(order[v%n])
    point_bin=balanced('load_point',5);direction_bin=balanced('load_direction',8)
    start=float(load.uniform(.05,.5));kind=('sustained','pulse','repeated')[balanced('load_kind',3)]
    duration=float(load.uniform(.1,.5) if kind=='pulse' else load.uniform(1,3))
    end=start+duration;period=duration+float(load.uniform(.5,1.5))
    fixture=('both','none','P','D')[balanced('fixture',4)] if scene=='E4' else (fixed_side if scene=='E1' else 'none')
    sides=('P','D','both')[balanced('neighbour_sides',3)] if scene in ('E3','E4') else 'none'
    c=SceneConfig(seed=seed,geometry_seed=geometry_seed,episode_id=episode_id,variant_id=v,
        scene=scene,fixed_side=fixed_side,geometry_id=geometry_id,limit_id=limit_id,
        capacity_nominal=capacity_nominal,lengths=lengths,masses=masses,
        ballast_ratios=tuple(r.uniform(0,.2,2)),ballast_fractions=tuple(r.uniform(.2,.8,2)),
        mass_error=mass_error,drive_error=bool(r.random()<.2),density_multiplier=density,
        capacity_multiplier=float(r.uniform(.8,1.2)),response_s=float(r.uniform(.005,.020)),
        delay_ms=int(r.integers(11)),damping=float(r.uniform(.01,.08)),friction=float(r.uniform(0,.08)),
        armature=float(np.exp(r.uniform(np.log(.001),np.log(.006)))),
        tilt=float(balanced('installation',8)*np.pi/4+installation.uniform(-np.pi/8,np.pi/8)),
        encoder_sign=(-1,1)[balanced('encoder_sign',2)],beta_encoder=float(-np.pi+(balanced('encoder_beta',8)+calibration.random())*np.pi/4),
        load_point_bin=point_bin,load_direction_bin=direction_bin,
        load_fraction=float(.05+.18*(point_bin+load.random())),
        load_force=float(load.uniform(0,.5*sum(masses)*(density if mass_error else 1.)*9.81)),
        load_couple=float(load.uniform(-1.8,1.8)),load_angle=float(-np.pi+(direction_bin+load.random())*np.pi/4),
        load_side=('P','D')[balanced('load_side',2)],load_frame=('world','body')[balanced('load_frame',2)],
        load_start=start,load_end=end,load_mode=kind,load_period=period,load_repeats=3 if kind=='repeated' else 1,
        support_k=(float(support.uniform(20,200)),float(support.uniform(100,500)),float(support.uniform(.1,5))),
        support_damping_ratio=float(support.uniform(.3,1)),support_preload=float(support.choice([0,.5,1,1.5])),
        support_horizontal_preload=float(support.uniform(-.25,.25)),support_torque_preload=float(support.uniform(-1.8,1.8)),
        support_motion=float(support.uniform(.01,.05)),support_frequency=float(support.uniform(.2,1)),
        support_angle_motion=float(support.uniform(.05,.3)),fixture_mode=fixture,neighbour_sides=sides,
        neighbour_lengths=tuple(neighbour.uniform(.15,.45,2)),neighbour_masses=tuple(np.exp(neighbour.uniform(np.log(.15),np.log(2),2))),
        neighbour_amplitude=float(neighbour.uniform(.1,.7)),neighbour_frequency=float(neighbour.uniform(.3,2)),
        neighbour_phase=float(neighbour.uniform(-np.pi,np.pi)),neighbour_kp=float(8*neighbour.uniform(.5,1.5)),
        neighbour_kd=float(.5*neighbour.uniform(.5,1.5)),neighbour_capacity=float(3.6*neighbour.uniform(.5,1.5)),
        object_mass=float(load.uniform(.1,2)),object_radius=float(load.uniform(.02,.1)),
        object_speed=float(load.uniform(-.5,.5)),contact_friction=float(load.uniform(.4,1)))
    if ('load_start' in overrides or 'load_end' in overrides) and 'load_period' not in overrides:
        active_duration=overrides.get('load_end',c.load_end)-overrides.get('load_start',c.load_start)
        overrides['load_period']=max(c.load_period,active_duration+.5)
    c=replace(c,**overrides)
    if c.scene not in ('E0','E1','E2','E3','E4') or c.fixed_side not in ('P','D'):raise ValueError('scene/side')
    if not 0<=c.limit_id<=3:raise ValueError('limit_id must be 0..3')
    if len(c.lengths)!=2 or min(c.lengths)<.15 or max(c.lengths)>.45:raise ValueError('length range .15..45 m')
    if c.encoder_sign not in (-1,1) or c.load_side not in ('P','D') or c.load_frame not in ('world','body'):raise ValueError('invalid frame')
    if c.neighbour_sides not in ('none','P','D','both') or c.fixture_mode not in ('auto','none','P','D','both'):raise ValueError('invalid topology')
    if c.initial_fraction is not None and not 0<=c.initial_fraction<=1:raise ValueError('initial_fraction in [0,1] required')
    return c
