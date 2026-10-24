"""Catalog trusted local artifacts and decode saved physical trajectories."""
from functools import lru_cache
from pathlib import Path
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / 'unit_bfm' / 'artifacts'
VERSION = 'SIM_PRIVILEGED_FF_MR_RF_V2'
TASKS = ['Hold', 'Speed', 'Brake', 'Adaptive.']
PLANS = [
    dict(id='nominal', name='Nominal maintenance . Three types of query comparison', count=96,
         description='8 targets x 4 initial x complete target / incentive points / randomz; error is maintained at last 1 second.'),
    dict(id='cross', name='• Cross-conditional query · Pairing reference', count=2048,
         description='8 Structure × 32 mission x 4 initial state, 1024 pieces per controller; run FB in turn and resolve reference.'),
    dict(id='switch_goal', name='Original Switch Panel . Point Targets and Randomz', count=400,
         description='5 Structures x 5 call cycles x 16 initial states; nominal R0 point target, remaining random z pairs.'),
    dict(id='switch_reward', name='Incentive Query Switch . Nom R0', count=80,
         description='<unk>0.6 Rad Incentive Query, Fixed / 40 / 80 / 500 / 1000 ms; Additional diagnostics from the original study.'),
    dict(id='atlas', name='Random z . Behavioural mapping', count=4096,
         description='8 Structures 256 z x 2 at first; no tracking targets have been specified, and movement and exposure coverage is observed.'),
]


def read_json(path, fallback=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return fallback


def confined(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path is not in the allowed data directory')
    return path


def checkpoints():
    result = []
    for run in ARTIFACTS.iterdir():
        manifest = read_json(run / 'manifest.json', {})
        if manifest.get('version') != VERSION:
            continue
        for p in sorted(run.glob('model_*.pt')):
            try:
                w = int(p.stem.split('_')[-1])
            except ValueError:
                continue
            result.append(dict(id=p.relative_to(ARTIFACTS).as_posix(), run=run.name, W=w,
                               label=f'{run.name} · W={w:,}'))
        p = run / 'checkpoint.pt'
        if p.exists() and not list(run.glob('model_*.pt')):
            w = read_json(run / 'status.json', {}).get('W', 0)
            result.append(dict(id=p.relative_to(ARTIFACTS).as_posix(), run=run.name, W=w,
                               label=f'{run.name} · W={w:,}'))
    return sorted(result, key=lambda r: (r['run'] != 'rf_v2_full', -r['W']))


def evaluations():
    result = []
    historical = [
        ('motion_panel', 'Keep the name on three queries.', 'nominal', None),
        ('final_eval', 'Cross-Conditions Query . FB', 'cross', 'final_eval_analytic'),
        ('final_eval_analytic', 'Cross-Conditions Query Query Query Query Query Query Query', 'analytic', None),
        ('switching', 'Original Switch Panel . Point Target / Randomz', 'switch_goal', None),
        ('switching_reward', 'Incentives for query switching . Supplementary diagnostics', 'switch_reward', None),
        ('final_eval/random_z', 'Random z spectra', 'atlas', None),
    ]
    for run_name in ('rf_v2_full', 'rf_v2_r0'):
        for rel, title, kind, compare in historical:
            p = ARTIFACTS / run_name / rel
            if list(p.glob('*.npz')):
                result.append(dict(id=p.relative_to(ARTIFACTS).as_posix(),
                    label=f'History .{run_name} · {title}', kind=kind,
                    checkpoint=f'{run_name}/ Final freezing of weight',
                    compare=f'{run_name}/{compare}' if compare and (ARTIFACTS / run_name / compare).exists() else None))
    jobs_root = ARTIFACTS / 'web_evaluations'
    if jobs_root.exists():
        for job_dir in sorted(jobs_root.iterdir(), reverse=True):
            job = read_json(job_dir / 'job.json', {})
            if job.get('status') != 'completed':
                continue
            for item in job.get('results', []):
                result.insert(0, dict(id=f'web_evaluations/{job_dir.name}/{item["folder"]}',
                    label=f'{job_dir.name} · {item["label"]}', kind=item['kind'],
                    checkpoint=job['checkpoint'], checkpoint_sha256=job.get('checkpoint_sha256'),
                    compare=f'web_evaluations/{job_dir.name}/{item["compare"]}' if item.get('compare') else None))
    return result


def evaluation(identifier):
    catalog = evaluations()
    match = next((r for r in catalog if r['id'] == identifier), None)
    if match is None:
        # A paired branch can be intentionally absent from the visible selector.
        parent = next((r for r in catalog if r.get('compare') == identifier), None)
        if parent:
            match = dict(parent, id=identifier, label='Pair branch...'+parent['label'], compare=None)
    if match is None:
        raise ValueError('Full assessment not found')
    return match, confined(ARTIFACTS, identifier)


@lru_cache(maxsize=2)
def _arrays(path, modified):
    with np.load(path, allow_pickle=False) as archive:
        return {k: archive[k] for k in archive.files}


def arrays(path):
    return _arrays(str(path), path.stat().st_mtime_ns)


def dataset(identifier, filename):
    meta, root = evaluation(identifier)
    if Path(filename).name != filename or not filename.endswith('.npz'):
        raise ValueError('Invalid track filename')
    path = confined(root, filename)
    if not path.is_file():
        raise ValueError('Track file does not exist')
    return meta, path, arrays(path)


def case_metadata(data, index, filename):
    row = dict(index=index, task='Random z', period=None, initial=None)
    if 'alpha' in data:
        alpha = data['alpha'][index]
        task = int(alpha[0])
        row.update(task=TASKS[task], initial=index % 4, alpha=alpha.tolist())
        if task == 0:
            detail = f'q*={alpha[1]:+.2f} rad'
        elif task == 1:
            detail = f'v*={alpha[1]:+.2f} rad/s'
        elif task == 2:
            detail = f'Weight a ={alpha[2]:.2f}'
        else:
            detail = f'K={alpha[2]:.2f}, D={alpha[3]:.2f}'
    elif 'period_steps' in data:
        period = int(data['period_steps'][index]) * 10
        row.update(task='Switch', period=period, initial=int(data['episode_ids'][index]))
        detail = 'Fixed First Command' if period == 0 else f'Every{period}ms Switch'
    elif 'targets' in data and filename != 'random_z.npz':
        row.update(task='Hold', initial=index % 4)
        detail = f'q*={data["targets"][index]:+.2f} rad'
    else:
        detail = f'z #{index // 2}/ Initial state{index % 2}' if 'targets' not in data else 'No target random direction'
    row['label'] = f'#{index:03d} · {row["task"]} · {detail}'
    if row['initial'] is not None:
        row['label'] += f'• Initial state{row["initial"]}'
    return row


def joint_limits(data,index=0):
    return tuple(float(v) for v in data['joint_limits'][index]) if 'joint_limits' in data else (-1.2,1.2)


def targets_for(data, index, filename):
    y = data['y'][index]
    n = len(y)
    q, v = y[:, 0] * 1.2, y[:, 1] * 6
    lower,upper=joint_limits(data,index)
    targets = {}
    if 'q_target' in data and np.isfinite(data['q_target'][index]).any():
        targets['q'] = data['q_target'][index]
    elif 'targets' in data and filename != 'random_z.npz':
        targets['q'] = np.full(n, data['targets'][index])
    elif 'alpha' in data:
        kind, ref, k, d, bias = data['alpha'][index]
        if kind == 0:
            targets['q'] = np.full(n, ref)
        elif kind == 1:
            distance = upper - q if ref >= 0 else q - lower
            ramp = np.clip(distance / .15, 0, 1)
            targets['dq'] = ref * ramp * ramp * (3 - 2 * ramp)
        elif kind == 2:
            targets['dq'] = np.zeros(n)
        else:
            targets['tau'] = bias + k * (ref - q) - d * v
    return targets


def physical_stats(data, index, filename):
    y = data['y'][index]
    q, v, tau, u = y[:, 0] * 1.2, y[:, 1] * 6, y[:, 12] * 6, y[:, 13]
    lower,upper=joint_limits(data,index)
    limit_label='Distance from current limit < 0.1 Rad' if 'joint_limits' in data else 'Near limit. <unk>1<unk>'
    metrics = [dict(label='Command Saturation', value=float(np.mean(np.abs(u) > .98) * 100), unit='%'),
        dict(label=limit_label, value=float(np.mean(np.minimum(q-lower,upper-q) < .1) * 100), unit='%'),
        dict(label='The scope of joints.', value=float(np.ptp(q)), unit='rad'),
        dict(label='Last second speed RMS.', value=float(np.sqrt(np.mean(v[-100:] ** 2))), unit='rad/s')]
    target = targets_for(data, index, filename)
    error = None
    if 'q_target' in data and 'q' in target:
        error = dict(label='Follow RMSE all the way.', value=float(np.sqrt(np.mean((q-target['q'])**2))), unit='rad')
    elif 'alpha' in data:
        kind, ref, k, d, bias = data['alpha'][index]
        if kind == 0:
            error = dict(label='RMSE, hold at last one second.', value=float(np.sqrt(np.mean((q[-100:]-ref)**2))), unit='rad')
        elif kind == 1:
            mask = (upper-q if ref >= 0 else q-lower) > .15
            error = dict(label='Viable inter-zone speed RMSE', value=float(np.sqrt(np.mean((v[mask]-ref)**2))) if mask.any() else None, unit='rad/s')
        elif kind == 3:
            error = dict(label='RMSE', value=float(np.sqrt(np.mean((tau-target['tau'])**2))), unit='N·m')
    elif 'q' in target:
        error = dict(label='RMSE, hold at last one second.', value=float(np.sqrt(np.mean((q[-100:]-target['q'][-100:])**2))), unit='rad')
    if error:
        metrics.insert(0, error)
    if 'work' in data:
        metrics.extend([dict(label='Power.',value=float(data['work'][index,:,0].sum()),unit='J'),
            dict(label='Power failure.',value=float(data['work'][index,:,1].sum()),unit='J')])
    return metrics


def poses(xml, qpos):
    import mujoco
    model = mujoco.MjModel.from_xml_path(str(xml))
    state = mujoco.MjData(model)
    links = []
    for name, color in [('A', '#94a3b8'), ('P', '#3985df'), ('D', '#ea8e38'), ('T', '#50ac8d')]:
        body = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
        geom = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name + '_box')
        if body >= 0 and geom >= 0:
            links.append(dict(name=name, color=color, body=body, length=float(model.geom_size[geom, 2] * 2)))
    frames = []
    for q in qpos:
        state.qpos[:] = q
        mujoco.mj_forward(model, state)
        frame = []
        for link in links:
            b = link['body']
            start = state.xpos[b]
            end = start + state.xmat[b].reshape(3,3) @ np.array([0, 0, -link['length']])
            frame.append([float(start[0]), float(start[2]), float(end[0]), float(end[2])])
        frames.append(frame)
    return dict(links=links, frames=frames,
                ground=mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'floor') >= 0)


def desired_qpos(xml, qpos, target):
    """A relative motor-angle reference; never change root or neighbour states."""
    import mujoco
    model = mujoco.MjModel.from_xml_path(str(xml))
    motor = model.joint('motor').id
    result = np.array(qpos, copy=True)
    result[:, model.jnt_qposadr[motor]] = target
    return result


def static_goal_torque(xml, target):
    """Reproduce diagnose_motion.static_goals' canonical zero-motion bias."""
    import mujoco
    model = mujoco.MjModel.from_xml_path(str(xml))
    state = mujoco.MjData(model)
    motor = model.joint('motor').id
    values = {}
    for q in np.unique(target):
        state.qpos[:] = 0
        state.qvel[:] = 0
        state.qpos[model.jnt_qposadr[motor]] = q
        mujoco.mj_forward(model, state)
        values[float(q)] = float(state.qfrc_bias[model.jnt_dofadr[motor]])
    return np.array([values[float(q)] for q in target])


def goal_for(path, data, index, targets, evaluation_kind=None):
    """Describe the recorded query, not an invented inverse decoding of z."""
    query = 'random'
    if targets:
        if path.stem == 'goal_result':
            query = 'point'
        elif 'q_target' in data:
            mode = read_json(path.parent / 'metrics.json', {}).get('nominal_query')
            query = {'goal':'point', 'reward':'reward'}.get(mode,
                {'switch_goal':'point', 'switch_reward':'reward'}.get(evaluation_kind, 'unknown'))
        elif 'alpha' in data or path.stem == 'reward_query':
            query = 'reward'
        else:
            query = 'unknown'
    sources = dict(point='Complete target .z = project (B(g*))',
        reward='Incentive points . z <unk> E[r(g) B(g)]', random='Random ball orientation. No predefined physical targets.',
        unknown='Physical targets maintained . Query source not recorded')
    goal = dict(query=query, source=sources[query], kind='random', channels=[],
        title='Random z behavioral observation', expression='No q* velocity or forcecrack target specified',
        description='It is only possible to observe what behaviour this z produces; it cannot be used as a successful tracking of a hidden target.',
        criterion='View the motion cover, saturation, limit and initial state sensitivity; there is no target tracking test here.',
        scope='The current model allows only x-z flat motion.',
        semantics='Below is the source of the search for target z; 16 potential coordinates are not fixed physical axes.')
    if 'phase' in data:
        goal['phase'] = data['phase'][index]
    if not targets:
        return goal
    n = len(data['y'][index])
    def channel(key, label, unit):
        goal['channels'].append(dict(key=key, label=label, unit=unit))
    if 'q' in targets:
        switching = 'q_target' in data
        goal.update(kind='hold', title='Joint angle switch' if switching else 'Keep the joint angle.',
            expression='q q*; dq 0',
            description='The gold dotted pole is the geometric reference for the current relative angle q*. Maintaining the query is also more static; switching will create the necessary transition movement.',
            criterion='q-tracking RMSE, containing the transient transient; does not require the transient arrival.' if switching
                else 'The last one-second q maintains RMSE; also sees residual velocity, saturation and limit.',
            scope='The reference rod position only changes the relative angle of the motor, and the roots and other joints follow the current actual state; it is not a whole-of-the-world attitude directive.')
        channel('q', 'joint angle', 'rad')
        if query in ('point','reward'):
            targets['dq'] = np.zeros(n)
            channel('dq', 'still reference speed', 'rad/s')
        if query == 'point':
            targets['tau'] = static_goal_torque(path.with_suffix('.xml'), targets['q'])
            channel('tau', 'Geostationary Gravity Compensatory Rectangular', 'N·m')
            goal['expression'] = 'Full g*:q=q*, P/D static attitude and zero velocity, instead = gravity compensation, exposure/environmental stress = 0'
            goal['description'] += 'B(g*) The two-pronged attitude, zero angle/line velocity, gravity compensation rectangular, and zero contact/environmental stress are also actually coded for the XML stationary configuration.'
        elif query == 'reward':
            goal['expression'] = 'r(g) = −((q−q*)/0.5)² − 0.1(dq/3)²'
    elif 'dq' in targets:
        kind, ref, a, b, _ = data['alpha'][index]
        brake = kind == 2
        goal.update(kind='brake' if brake else 'velocity', title='Brake / Deplete Prefer' if brake else 'Joint speed control',
            expression=f'r(g) = −{a:g}(dq/3)² − {b:g} max(τ·dq,0)/36' if brake
                else f'dq* = {ref:+g}xSmoothstep (Range range along target / 0.15)',
            description='The speed is close to zero, and the power is reduced; no stop angle is specified. Stopping on the limit cannot be judged successful by low speed alone.' if brake
                else 'The golden arc arrow indicates the direction of the target; the arc length is only indicative of the direction, and the target value is in the card. The speed within the distance limit is 0.15 rad and the final position is not specified.',
            criterion='RMS, RMS, RMS, RMS, RMS; original panel does not have a complete brake success threshold.' if brake
                else 'The original indicator calculates RMSE relative nominal speed only in samples at > 0.15 rad in the direction of the target.',
            scope='The target is the relative angle speed; it is not the rate of movement of root or condensed heart.')
        channel('dq', 'Brake speed' if brake else 'Target speed when border drops.', 'rad/s')
        if not brake:
            goal['nominal_speed'] = float(ref)
    elif 'tau' in targets:
        _, ref, k, d, bias = data['alpha'][index]
        goal.update(kind='compliance', title='Local force rectangular relationship / responsive',
            expression=f'τ* = {bias:+g} + {k:g} × ({ref:+g} − q) − {d:g} × dq  N·m',
            description='Gold arc arrows represent the current orientation of the target \' s electrical power rectangular;* they vary with actual q, dq. q references are spring balance parameters, not the position that must be reached.',
            criterion='RMSE for the entire course of the actual electrical power rectangular and *(q,dq); not a successful test of contact or body balance.',
            scope='Targets are directed at electric power rectangles; environmental and power rectangles are additional observations.')
        channel('tau', 'Target power grid.', 'N·m')
    if 'joint_limits' in data:
        lower,upper=joint_limits(data,index)
        goal['scope'] += f'Current physical joint limit [s]{lower:.3f}, {upper:.3f}]] Rad; training fixed to [-1.2, 1.2] Rad.'
        if goal['kind']=='hold' and np.any((targets['q']<lower)|(targets['q']>upper)):
            goal['description'] += 'The current angle target exceeds the physical limit and is subject to a restricted call test, and geometric references are not considered to be achievable.'
        if goal['kind']=='velocity':
            goal['scope'] += 'The current limit is used for querying and displaying the speed reduction boundary, and the reference sample is still derived from the training data of the old weight.'
    return goal


def decode(path, data, index, evaluation_kind=None):
    y = data['y'][index]
    names = {'q':(0,1.2), 'dq':(1,6), 'tau':(12,6), 'u':(13,1),
             'p_fx':(18,20), 'p_fz':(19,20), 'd_fx':(21,20), 'd_fz':(22,20),
             'p_contact':(14,1), 'd_contact':(15,1), 'p_my':(20,6), 'd_my':(23,6)}
    targets = targets_for(data,index,path.name)
    goal = goal_for(path,data,index,targets,evaluation_kind)
    if evaluation_kind == 'analytic':
        goal['semantics'] += 'This track is executed by the Law of Resolution Control, and the z is saved as a corresponding query code and is not used to generate actions.'
    result = dict(time=(np.arange(len(y))+1)*.01,
        joint_limits=joint_limits(data,index),
        series={k:y[:,c]*s for k,(c,s) in names.items()},
        targets=targets, goal=goal, metrics=physical_stats(data,index,path.name),
        pose=poses(path.with_suffix('.xml'), data['qpos'][index]))
    if 'q' in targets:
        result['goal_pose'] = poses(path.with_suffix('.xml'),
            desired_qpos(path.with_suffix('.xml'),data['qpos'][index],targets['q']))
    if 'z' in data:
        result['z'] = [data['z'][index]]
    elif 'command_pairs' in data:
        pair = data['command_pairs'][int(data['episode_ids'][index])]
        result['z'] = pair[data['phase'][index]]
    else:
        result['z'] = []
    return result


def trajectory(identifier, filename, index):
    meta, path, data = dataset(identifier, filename)
    if index < 0 or index >= len(data['y']):
        raise ValueError('Case number crossed the border')
    result = decode(path, data, index, meta['kind'])
    result.update(case=case_metadata(data,index,filename), evaluation=meta, file=filename)
    if meta['kind']=='live':
        from .live import applied_events, COMPARISON_LABEL
        result['comparison_label']=COMPARISON_LABEL
        result['events']=read_json(path.parent/'events.json',[])
        result['perturbations']=[applied_events(result['events'],float(t)) for t in result['time']]
        result['session']=read_json(path.parent.parent/'session.json',{})
    if meta.get('compare'):
        _, other_path, other = dataset(meta['compare'],filename)
        if 'alpha' in data and np.array_equal(data['alpha'][index], other['alpha'][index]):
            result['comparison'] = decode(other_path,other,index,'live' if meta['kind']=='live' else 'analytic')
    return result


def clean(value):
    if isinstance(value,np.ndarray):
        return clean(value.tolist())
    if isinstance(value,np.generic):
        return clean(value.item())
    if isinstance(value,dict):
        return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [clean(v) for v in value]
    if isinstance(value,float) and not math.isfinite(value):
        return None
    return value


def summary_rows(root):
    rows = []
    metrics = read_json(root/'metrics.json', {})
    if 'summary' in metrics:
        for i,key in enumerate(('hold','velocity','brake','compliance')):
            r = metrics['summary'][key]
            rows.append(dict(name=TASKS[i], value=r['mean_physical_error'], unit=['rad','rad/s','rad/s','N·m'][i],
                             note=['Last 1 second angle RMSE','Viable inter-zone speed RMSE','RMS, last second speed.','RMSE Total ForceRange'][i]))
    else:
        nominal = read_json(root/'summary.json', {})
        for key,label in [('goal_result','Full target B (g*)'),('reward_query','Incentive score query'),('random_z','Random z')]:
            if key in nominal:
                r = nominal[key]
                rows.append(dict(name=label,value=r['mean_hold_rmse'],unit='rad',note='Last 1 second angle RMSE' if key!='random_z' else 'Reference error to specified target; no target command for randomz'))
    if not rows and metrics.get('records'):
        for period in (0,4,8,50,100):
            subset=[r for r in metrics['records'] if r.get('period_steps')==period and 'tracking_rmse_rad' in r]
            if subset:
                rows.append(dict(name='Fixed First Command' if period==0 else f'{period*10} ms',
                    value=float(np.mean([r['tracking_rmse_rad'] for r in subset])),unit='rad',note='RZSE is tracked throughout R0.'))
    return rows


def detail(identifier):
    meta, root = evaluation(identifier)
    files = []
    for path in sorted(root.glob('*.npz')):
        data = arrays(path)
        files.append(dict(name=path.name,count=len(data['y'])))
    return dict(**meta, files=files, summary=summary_rows(root))
