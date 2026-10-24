"""Frozen-policy command switching; paired exogenous seeds, never reset history."""
import argparse
import gc
import json
from pathlib import Path

import numpy as np
import torch
import warp as wp

from .diagnose_motion import static_goals
from .environment import UnitEnv
from .learner import Learner
from .mechanics import Structure, library
from .networks import physical_result
from .tasks import project


@torch.no_grad()
def run(learner, out, nominal_query='goal', nominal_only=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    periods = [0, 4, 8, 50, 100]  # 0 is the paired fixed-first-command condition.
    pairs = 16
    ids = np.tile(np.arange(pairs), len(periods))
    generator = torch.Generator(device=learner.device).manual_seed(96001)
    directions = project(torch.randn(pairs, 2, 16, device=learner.device, generator=generator))
    structures = [Structure(0, 100)] + [s for s in library(61001, 8, False) if s.index == 0]
    if nominal_only:
        structures = structures[:1]
    records = []
    for si, structure in enumerate(structures):
        commands = directions
        if si == 0:
            if nominal_query == 'goal':
                goals = torch.as_tensor(static_goals(structure, [-.6, .6]), device=learner.device)
                pair = project(learner.net.b(physical_result(goals)))
            else:
                pair = learner.encode(np.array([[0, -.6, 0, 0, 0], [0, .6, 0, 0, 0]], np.float32))
            commands = pair[None].repeat(pairs, 1, 1)
            commands[1::2] = commands[1::2].flip(1)
        env = UnitEnv(structure, len(ids), seed=86001)
        x = env.reset(ids, level=0 if si == 0 else 1, snapshots=False)
        # Repeated episode IDs deliberately give every schedule the same initial
        # state, physical parameters and exogenous force plan before divergence.
        initial = env.tensors['obs'].cpu().numpy().copy()
        if not np.array_equal(initial.reshape(len(periods), pairs, 24),
                              np.broadcast_to(initial[:pairs], (len(periods), pairs, 24))):
            raise AssertionError('Switching schedules must start from matched states')
        ys, qps, works, phases = [], [], [], []
        for step in range(500):
            phase = np.repeat([0 if p == 0 else (step // p) % 2 for p in periods], pairs)
            z = commands[torch.as_tensor(ids, device=learner.device),
                         torch.as_tensor(phase, device=learner.device)]
            x, y = env.step(learner.net.actor(x, z))
            if not torch.isfinite(y).all():
                raise FloatingPointError(f'Nonfinite switching rollout: {structure.key}')
            ys.append(y.cpu())
            qps.append(env.sim.data.qpos.cpu().clone())
            works.append(env.tensors['work'].cpu().clone())
            phases.append(phase)
        y = torch.stack(ys, 1).numpy()
        work = torch.stack(works, 1).numpy()
        phase = np.stack(phases, 1)
        fixed_q = y[:pairs, :, 0] * 1.2
        for group, period in enumerate(periods):
            start = group * pairs
            for k in range(pairs):
                i = start + k
                q, v, u = y[i, :, 0] * 1.2, y[i, :, 1] * 6, y[i, :, 13]
                changes = np.flatnonzero(np.diff(phase[i]) != 0) + 1
                delta = np.abs(u[changes] - u[changes - 1])
                record = dict(model=structure.key, nominal_goal=si == 0,
                    period_steps=period, initial=k, q_min=float(q.min()), q_max=float(q.max()),
                    mean_q_range=float(np.ptp(q)), dq_rms=float(np.sqrt(np.mean(v*v))),
                    dq_max=float(np.abs(v).max()), saturation=float(np.mean(np.abs(u) > .98)),
                    limit_overrun_max_rad=float(max(0., np.abs(q).max() - 1.2)),
                    positive_work_J=float(work[i, :, 0].sum()),
                    negative_work_J=float(work[i, :, 1].sum()),
                    switch_count=len(changes),
                    switch_mean_abs_du=float(delta.mean()) if len(delta) else None,
                    switch_max_abs_du=float(delta.max()) if len(delta) else None,
                    paired_fixed_q_rms_difference=float(np.sqrt(np.mean((q-fixed_q[k])**2))))
                if si == 0:
                    target = np.where((phase[i] + k % 2) % 2 == 0, -.6, .6)
                    record['tracking_rmse_rad'] = float(np.sqrt(np.mean((q-target)**2)))
                    # This is a descriptive result, not a 40 ms reachability gate.
                records.append(record)
        np.savez_compressed(out / f'{structure.key}.npz', y=y,
            qpos=torch.stack(qps, 1).numpy(), work=work, initial=initial, phase=phase,
            command_pairs=commands.cpu().numpy(), episode_ids=ids,
            period_steps=np.repeat(periods, pairs),
            q_target=np.where((phase + ids[:, None] % 2) % 2 == 0, -.6, .6)
                if si == 0 else np.full(phase.shape, np.nan))
        (out / f'{structure.key}.xml').write_text(structure.xml())
        del env
        gc.collect()
    result = dict(controller='frozen_FB_actor', seed=86001, nominal_query=nominal_query,
        interpretation='Short calls test command continuity, not instantaneous target arrival.',
        records=records)
    (out / 'metrics.json').write_text(json.dumps(result, indent=2))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--nominal-query', choices=['goal','reward'], default='goal')
    p.add_argument('--nominal-only', action='store_true')
    args = p.parse_args()
    torch.set_num_threads(1)
    wp.config.quiet = True
    state = torch.load(args.checkpoint, weights_only=False, map_location='cuda:0')
    learner = Learner(state['learner']['reference'])
    learner.load_state_dict(state['learner'])
    result = run(learner, args.out, args.nominal_query, args.nominal_only)
    print(json.dumps(dict(out=args.out, trajectories=len(result['records']))), flush=True)


if __name__ == '__main__':
    main()
