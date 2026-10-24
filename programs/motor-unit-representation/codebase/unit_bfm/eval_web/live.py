"""CPU MuJoCo live perturbation test of the frozen V2 policy, never training.

Three initially identical copies: feedback, perturbed command replay, and an
unperturbed policy that supplies the replay commands. Only the first two receive
manual external pulses. Existing CPUUnit owns the millisecond actuator physics.
"""
import hashlib
import json
import math
from pathlib import Path
import threading
import time
import uuid
import numpy as np
from . import data as view
from .worker import write
from . import parameters

TASK_IDS = dict(hold=0, velocity=1, brake=2, compliance=3)
COMPARISON_LABEL = '. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . no . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .'


def number(payload, name, default, lower, upper):
    try:
        value = float(payload.get(name, default))
    except (TypeError, ValueError):
        raise ValueError(f'{name}Must be a value.')
    if not math.isfinite(value) or not lower <= value <= upper:
        raise ValueError(f'{name}It must be.{lower}Present.{upper}Between')
    return value


def config(payload):
    role = number(payload, 'role', 0, 0, 3)
    if role != int(role):
        raise ValueError('Connecting roles must be integer')
    task = payload.get('task', 'hold')
    if task not in TASK_IDS:
        raise ValueError('Unknown real-time task')
    physics = parameters.validate(payload.get('physics', {}))
    target = 0. if task=='brake' else number(payload, 'target', .3,
        -4 if task == 'velocity' else -math.pi, 4 if task == 'velocity' else math.pi)
    initial_q = number(payload, 'initial_q', 0., -math.pi, math.pi)
    if not physics['lower'] <= initial_q <= physics['upper']:
        raise ValueError('Initialq must be within the current physical joint limit; targetq can be used outside the limit for restricted call tests')
    seed = number(payload, 'seed', 20261001, 0, 2**32-1)
    if seed != int(seed):raise ValueError('Random torrents must be integer')
    auto_pulses = payload.get('auto_pulses', False)
    if not isinstance(auto_pulses,bool):raise ValueError('Autodisturbing must be a boolean value')
    k = number(payload, 'stiffness', 1., .3, 12.)
    d = number(payload, 'damping', .15, .02, .5)
    bias = number(payload, 'bias', 0., -1., 1.)
    alpha = [TASK_IDS[task], target, k, d, bias]
    if task in ('hold', 'velocity'):
        alpha[2:] = [0, 0, 0]
    if task == 'brake':
        alpha = [2, 0, 1, .1, 0]
    return dict(role=int(role), task=task, alpha=alpha, physics=physics,
        seed=int(seed), auto_pulses=auto_pulses, initial_q=initial_q,
        initial_dq=number(payload, 'initial_dq', 0., -4, 4),
        duration=number(payload, 'duration', 30., 5, 60))


def pulse_config(payload):
    side = payload.get('side', 'D')
    if side not in ('P', 'D'):
        raise ValueError('The side of the force must be P or D.')
    return dict(side=side, fx=number(payload, 'fx', 4., -15, 15),
        fz=number(payload, 'fz', 0., -15, 15), my=number(payload, 'my', 0., -3, 3),
        fraction=number(payload, 'fraction', .8, .2, 1.),
        duration=number(payload, 'duration', .25, .1, 1.5))


def pulse_mean(event, end_time):
    """Same 1ms sample times and 50ms cosine edge as CPUUnit.step."""
    phase = end_time - .01 + np.arange(10) * .001 - event['start']
    edge = np.clip(np.minimum(phase / .05, (event['duration'] - phase) / .05), 0, 1)
    envelope = (.5 - .5 * np.cos(np.pi * edge)) * ((phase >= 0) & (phase < event['duration']))
    return float(envelope.mean())


def applied_events(events, end_time):
    return [dict(id=e['id'], side=e['side'], fraction=e['fraction'],
        fx=e['fx'] * a, fz=e['fz'] * a, my=e['my'] * a)
        for e in events if (a := pulse_mean(e, end_time)) > 1e-12]


def encode_query(learner, alpha, limits):
    # Same frozen reward-integral query; custom velocity limits change only the
    # existing boundary ramp. The stored reference still comes from old training.
    if alpha[0,0] != 1 or np.allclose(limits,[-1.2,1.2],rtol=0,atol=1e-9):
        return learner.encode(alpha)
    from ..networks import physical_result
    from ..tasks import project
    y=learner.reference[learner.cache_ids]
    q,v=y[:,0]*1.2,y[:,1]*6
    ref=float(alpha[0,1])
    distance=limits[1]-q if ref>=0 else q-limits[0]
    ramp=(distance/.15).clamp(0,1)
    desired=ref*ramp.square()*(3-2*ramp)
    reward=-((v-desired)/3).square()
    b=learner.net.b(physical_result(y))
    return project((reward[:,None]*b).mean(0,keepdim=True))


class Experiment:
    def __init__(self, learner, options, folder, checkpoint):
        import torch
        import mujoco
        from ..cpu import CPUUnit
        from ..history import History
        from ..mechanics import Structure
        self.torch, self.mujoco = torch, mujoco
        self.options, self.learner, self.folder = options, learner, folder
        self.lock = threading.RLock()
        self.condition = threading.Condition(self.lock)
        self.status, self.error = 'paused', None
        self.events, self.records = [], []
        p = options['physics']
        self.limits = [p['lower'], p['upper']]
        self.structure = Structure(options['role'], 100, **{k:p[k] for k in ('lp','ld','mp','md','bp','bd','fp','fd','tilt')})
        self.xml = parameters.model_xml(self.structure,p,actual=True)
        self.nominal_xml = parameters.model_xml(self.structure,p)
        self.alpha = np.array([options['alpha']], np.float32)
        with torch.no_grad():
            self.z = encode_query(learner, self.alpha, self.limits).detach()
        self.units = []
        for _ in range(3):
            m = mujoco.MjModel.from_xml_string(self.xml)
            d = mujoco.MjData(m)
            j = int(m.joint('motor').dofadr[0])
            d.qpos[int(m.joint('motor').qposadr[0])] = options['initial_q']
            d.qvel[j] = options['initial_dq']
            if options['role'] in (1,2):
                d.qpos[:3] = [p['root_x'] if options['role']==1 else 0, p['root_z'] if options['role']==1 else 0, p['root_pitch']]
                d.qvel[:3] = [p['root_vx'],p['root_vz'],p['root_omega']]
            if options['role']==3:
                for side,name in [('p','q1'),('d','q3')]:
                    d.qpos[int(m.joint(name).qposadr[0])] = p['q_'+side]
                    d.qvel[int(m.joint(name).dofadr[0])] = p['dq_'+side]
            mujoco.mj_forward(m, d)
            if options['role'] == 2:
                bottom = min(d.geom_xpos[m.geom(n).id, 2] -
                    np.abs(d.geom_xmat[m.geom(n).id].reshape(3, 3)[2]) @ m.geom_size[m.geom(n).id]
                    for n in ('P_box', 'D_box'))
                d.qpos[1] += p['clearance'] - bottom
                mujoco.mj_forward(m, d)
            mass = m.body_mass[1:].sum()
            inertia = m.body_inertia[1:, 1].sum() + mass * (self.structure.lp + self.structure.ld)**2 / 3
            stiffness = np.array([p['kx'],p['kz'],p['kt']])
            damping = 2 * np.array([p['zeta_x'],p['zeta_z'],p['zeta_t']]) * np.sqrt(stiffness * [mass, mass, inertia])
            state = dict(u=0., tau=0., cap=p['cap'], tm=p['tm'], delay=int(p['delay']), clock=0,
                ring=np.zeros(11), support=np.r_[stiffness, damping, mass * p['gravity']],
                pulses=np.empty((0, 7)), peripheral=np.array([[p['amp_'+side],2*np.pi*p['hz_'+side],p['phase_'+side]] for side in ('p','d')]))
            self.units.append(CPUUnit(m, d, self.structure, state))
        nominal = self.structure.nominal(mujoco.MjModel.from_xml_string(self.nominal_xml))
        nominal[10:12] = np.array(self.limits)/1.2  # Preserve frozen training scales.
        self.m = torch.as_tensor(nominal).repeat(2, 1)
        if options['auto_pulses']:
            rng=np.random.default_rng(options['seed'])
            start=float(rng.uniform(.5,2))
            while start < options['duration']:
                duration=float(rng.uniform(.1,.5)); angle=float(rng.uniform(0,2*np.pi))
                magnitude=float(rng.uniform(0,.5*mass*9.81))
                self.events.append(dict(id=len(self.events)+1,source='seeded',start=start,duration=duration,
                    side=str(rng.choice(['P','D'])),fx=magnitude*np.cos(angle),fz=magnitude*np.sin(angle),
                    my=float(rng.uniform(-1.8,1.8)),fraction=float(rng.uniform(.2,.8))))
                start+=duration+float(rng.uniform(.5,2))
            pulses=np.array([[e['start'],e['duration'],e['fx'],e['fz'],e['my'],e['fraction'],int(e['side']=='D')] for e in self.events]).reshape(-1,7)
            for u in self.units[:2]:u.s['pulses']=pulses.copy()
        self.history = History(2, 'cpu')  # Feedback + unperturbed reference; replay ignores observations.
        self.history.reset(torch.as_tensor(np.stack([self.initial_observation(u) for u in self.units[::2]])))
        self.links = []
        model = self.units[0].model
        for name, color in [('A', '#94a3b8'), ('P', '#3985df'), ('D', '#ea8e38'), ('T', '#50ac8d')]:
            try:
                self.links.append(dict(name=name, color=color, body=model.body(name).id,
                    length=float(model.geom(name+'_box').size[2] * 2)))
            except KeyError:
                pass
        self.target_state = mujoco.MjData(model)
        self.meta = dict(id=folder.name, checkpoint=checkpoint, config=options,
            profile='SIM_PRIVILEGED', engine='CPU MuJoCo + existing CPUUnit',
            outside_training=parameters.outside_training(p,options['role']),
            target_outside_limits=options['task']=='hold' and not p['lower']<=options['alpha'][1]<=p['upper'],
            nominal_input=nominal.tolist(),
            source_sha256={str(p.relative_to(view.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [Path(__file__), view.ROOT/'unit_bfm/cpu.py', view.ROOT/'unit_bfm/history.py',
                          view.ROOT/'unit_bfm/networks.py', view.ROOT/'unit_bfm/mechanics.py',
                          view.ROOT/'unit_bfm/learner.py', view.ROOT/'unit_bfm/tasks.py', Path(view.__file__),Path(parameters.__file__)]},
            checkpoint_sha256=hashlib.sha256(view.confined(view.ARTIFACTS, checkpoint).read_bytes()).hexdigest(),
            label='- Manual disturbance. - Closed rings and motion playback.', comparison_label=COMPARISON_LABEL,
            description='Three of the same self-defined dynamics and initials. Closed rings and motion replays are also subject to the same worldwide impulse; the third undisturbed branch generates a replay command.',
            note='Use a simulation privileges feedback. Action playback is not a PD, parser, or qpos-RL; disturbance response does not guarantee recovery success.')
        folder.mkdir(parents=True, exist_ok=False)
        (folder/'model.xml').write_text(self.xml)
        (folder/'nominal.xml').write_text(self.nominal_xml)
        write(folder/'session.json', self.meta)
        fake = dict(y=np.zeros((1,1,25), np.float32), alpha=self.alpha,joint_limits=np.array([self.limits]))
        targets = view.targets_for(fake, 0, 'live.npz')
        self.goal = view.goal_for(folder/'live.npz', fake, 0, targets)
        self.goal['criterion'] = 'Check the q/dq/and/u of the three branches before and after the disturbance; maintain the original physical error definition and deviate from the relatively undisturbed branch after the disturbance.'
        self.thread = None

    def initial_observation(self, unit):
        m, d = unit.model, unit.data
        o = np.zeros(24, np.float32)
        q = float(d.qpos[int(m.joint('motor').qposadr[0])])
        o[:2] = q/1.2, d.qvel[unit.motor]/6
        for side, b in enumerate((unit.p, unit.d)):
            rot = d.xmat[b].reshape(3,3)
            cv = d.cvel[b]
            v = cv[3:] + np.cross(cv[:3], d.xipos[b]-d.subtree_com[m.body_rootid[b]])
            o[2+side*5:7+side*5] = [rot[0,2], rot[0,0], v[0]/2, v[2]/2, cv[1]/6]
        o[16:18] = (q-self.limits[0])/2.4, (self.limits[1]-q)/2.4
        return o

    def pose(self, state):
        frame = []
        for link in self.links:
            b = link['body']
            start = state.xpos[b]
            end = start + state.xmat[b].reshape(3,3) @ [0, 0, -link['length']]
            frame.append([float(start[0]), float(start[2]), float(end[0]), float(end[2])])
        return frame

    def advance(self):
        """One atomic 10ms interval, callable directly in deterministic tests."""
        with self.lock, self.torch.no_grad():
            x = self.history.input(self.m)
            commands = self.learner.net.actor(x, self.z.expand(2,-1))[:,0].numpy()
            ys = [u.step(commands[0] if i == 0 else commands[1]) for i,u in enumerate(self.units)]
            for y in ys:
                q=float(y[0])*1.2
                y[16:18]=(q-self.limits[0])/2.4,(self.limits[1]-q)/2.4
            if not np.isfinite(ys).all():
                raise FloatingPointError('Real-time simulation produces invalid status')
            self.history.append(self.torch.as_tensor(np.stack([ys[0][:24], ys[2][:24]])))
            end_time = len(self.records)*.01 + .01
            row = dict(time=end_time, y=np.stack(ys), qpos=np.stack([u.data.qpos.copy() for u in self.units]),
                work=np.stack([u.work.copy() for u in self.units]),
                poses=[self.pose(u.data) for u in self.units],
                perturbations=applied_events(self.events, end_time))
            if self.options['task'] == 'hold':
                self.target_state.qpos[:] = self.units[0].data.qpos
                j = int(self.units[0].model.joint('motor').qposadr[0])
                self.target_state.qpos[j] = self.alpha[0,1]
                self.mujoco.mj_forward(self.units[0].model, self.target_state)
                row['goal_pose'] = self.pose(self.target_state)
            self.records.append(row)
            return row

    def inject(self, payload):
        pulse = pulse_config(payload)
        with self.lock:
            if self.status not in ('paused', 'running'):
                raise ValueError('Please start a real-time experiment.')
            if len(self.events) >= 100:
                raise ValueError('We\'ve recorded 100 disturbances this time. Please start new experiments.')
            pulse.update(id=len(self.events)+1, source='manual', start=len(self.records)*.01,
                queued_at=time.time())
            raw = [pulse['start'], pulse['duration'], pulse['fx'], pulse['fz'], pulse['my'],
                   pulse['fraction'], int(pulse['side']=='D')]
            for u in self.units[:2]:
                u.s['pulses'] = np.vstack([u.s['pulses'], raw])
            self.events.append(pulse)
            return pulse

    def launch(self):
        with self.condition:
            self.status = 'running'
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def run(self):
        try:
            while True:
                with self.condition:
                    while self.status == 'paused':
                        self.condition.wait()
                    if self.status != 'running':
                        break
                began = time.monotonic()
                # Lock again: a pause may have arrived since the above check.
                with self.lock:
                    if self.status != 'running':
                        continue
                    self.advance()
                    if len(self.records) >= round(self.options['duration']*100):
                        self.status = 'completed'
                time.sleep(max(0, .01-(time.monotonic()-began)))
        except Exception as exc:
            with self.lock:
                self.status, self.error = 'failed', str(exc)
        finally:
            self.save()

    def control(self, action):
        with self.condition:
            if self.status not in ('running','paused'):
                raise ValueError('The experiment is over.')
            if action == 'pause':
                self.status = 'paused'
            elif action == 'resume':
                self.status = 'running'
            elif action == 'stop':
                self.status = 'stopped'
            elif action == 'step':
                if self.status != 'paused':
                    raise ValueError('Please pause and take one step.')
                self.advance()
                if len(self.records) >= round(self.options['duration']*100):
                    self.status = 'completed'
            else:
                raise ValueError('Unknown experimental operation')
            self.condition.notify_all()

    def state(self, since=0):
        with self.lock:
            if not 0 <= since <= len(self.records):
                raise ValueError('Real-time frame numbers crossed.')
            rows = self.records[since:]
            result = dict(meta=dict(self.meta), status=self.status, error=self.error,
                offset=since, count=len(self.records), events=list(self.events),
                goal=self.goal, z=self.z[0].tolist(), links=self.links,
                ground=self.options['role']==2,
                frames=[dict(time=r['time'], y=r['y'].tolist(), poses=r['poses'],
                    goal_pose=r.get('goal_pose'), perturbations=r['perturbations']) for r in rows])
            if self.records:
                y = np.stack([r['y'] for r in self.records])
                result['feedback_vs_reference_q_rms'] = float(np.sqrt(np.mean(((y[:,0,0]-y[:,2,0])*1.2)**2)))
                result['replay_vs_reference_q_rms'] = float(np.sqrt(np.mean(((y[:,1,0]-y[:,2,0])*1.2)**2)))
            return result

    def save(self):
        with self.lock:
            self.meta.update(status=self.status, error=self.error, events=self.events, frames=len(self.records))
            write(self.folder/'session.json', self.meta)
            if not self.records:
                return
            y = np.stack([r['y'] for r in self.records])
            qp = np.stack([r['qpos'] for r in self.records])
            work = np.stack([r['work'] for r in self.records])
            for branch, name in enumerate(('feedback','replay','reference')):
                p = self.folder/name
                p.mkdir(exist_ok=True)
                filename = self.structure.key
                np.savez_compressed(p/(filename+'.npz'), y=y[:,branch][None], qpos=qp[:,branch][None],
                    work=work[:,branch][None], alpha=self.alpha, z=self.z.numpy(), joint_limits=np.array([self.limits]))
                (p/(filename+'.xml')).write_text(self.xml)
                write(p/'events.json', self.events if branch < 2 else [])
                write(p/'metrics.json', dict(controller=name, records=[]))
            write(self.folder/'job.json', dict(id=self.folder.name, checkpoint=self.meta['checkpoint'],
                checkpoint_sha256=self.meta['checkpoint_sha256'], plan='live',
                status='failed' if self.status=='failed' else 'completed',
                results=[dict(folder='feedback',label='- Manual disturbance. - Closed rings and motion playback.',kind='live',compare='replay')]))


class Manager:
    def __init__(self):
        self.lock = threading.RLock()
        self.experiment = None
        self.learner = None
        self.cache_key = None

    def start(self, payload):
        options = config(payload)
        checkpoint = payload.get('checkpoint')
        if checkpoint not in {r['id'] for r in view.checkpoints()}:
            raise ValueError('Please select the V2 weight of the list')
        with self.lock:
            if self.experiment and self.experiment.status in ('running','paused'):
                raise ValueError('Please stop the current real-time experiment.')
            import torch
            from ..learner import Learner
            torch.set_num_threads(1)
            path = view.confined(view.ARTIFACTS, checkpoint)
            key = (checkpoint, path.stat().st_mtime_ns)
            if self.cache_key != key:
                state = torch.load(path, weights_only=False, map_location='cpu')
                if state.get('version') != view.VERSION:
                    raise ValueError('Only V2 weights supported')
                self.learner = Learner(state['learner']['reference'], device='cpu')
                self.learner.load_state_dict(state['learner'])
                self.learner.net.eval().requires_grad_(False)
                self.cache_key = key
            folder = view.ARTIFACTS/'web_evaluations'/(time.strftime('%Y%m%d_%H%M%S')+'_live_'+uuid.uuid4().hex[:6])
            self.experiment = Experiment(self.learner, options, folder, checkpoint)
            self.experiment.launch()
            return self.experiment.state()

    def current(self, identifier=None):
        if self.experiment is None:
            raise ValueError('No real-time experiments.')
        if identifier is not None and identifier != self.experiment.meta['id']:
            raise ValueError('Real-time experiments have been replaced. Read again.')
        return self.experiment

    def state(self, since=0, identifier=None):
        with self.lock:
            if self.experiment is None:
                return None
            return self.current(identifier).state(since)
