"""Read-only numerical summaries/plots; no learned weights or acceptance flags changed."""
import argparse
import json
from pathlib import Path

import numpy as np


NAMES = ['hold', 'velocity', 'brake', 'compliance']
UNITS = ['rad', 'rad/s', 'rad/s', 'Nm']


def mean(values):
    values = [v for v in values if v is not None]
    return float(np.mean(values)) if values else None


def task_groups(records):
    result = {}
    for group in ['all', 'monitor_reused', 'new_structure'] + [f'R{i}' for i in range(4)]:
        subset = [r for r in records if group == 'all'
                  or (group == 'monitor_reused' and r['model'].endswith('_000'))
                  or (group == 'new_structure' and r['model'].endswith('_001'))
                  or r['model'].startswith(group + '_')]
        result[group] = {}
        for task, name in enumerate(NAMES):
            rows = [r for r in subset if r['task'] == task]
            result[group][name] = dict(n=len(rows), unit=UNITS[task],
                mean_error=mean([r['physical_error'] for r in rows]),
                mean_reward=mean([r['reward'] for r in rows]),
                mean_saturation=mean([r['saturation'] for r in rows]))
    return result


def task_key(row):
    return row['model'], row['initial'], tuple(row['alpha'])


def run(root):
    root = Path(root)
    out = root / 'analysis'
    out.mkdir(exist_ok=True)
    trace = [json.loads(line) for line in (root / 'metrics.jsonl').read_text().splitlines()]
    report = dict(W=trace[-1]['W'], training_seed_count=1,
        role_W=trace[-1]['role_W'], visited_models=len({r['model'] for r in trace}),
        learning_last=trace[-1]['learning'],
        rank_threshold=1e-3, rank_min=min(r['effective_rank'] for r in trace),
        rank_final=trace[-1]['effective_rank'],
        finite_learning=all(np.isfinite(v) for r in trace for v in r['learning'].values()),
        notes=['Errors retain physical units; no post hoc acceptance threshold.',
               'Monitor index 0 structures were repeatedly evaluated; index 1 extends the panel.',
               'Random-z atlas varies both z and initial dynamics; spread alone is not controllability.'])
    for name in ('final_eval', 'final_eval_analytic'):
        path = root / name / 'metrics.json'
        if path.exists():
            report[name] = task_groups(json.loads(path.read_text())['records'])
    if all(name in report for name in ('final_eval', 'final_eval_analytic')):
        fb = json.loads((root / 'final_eval/metrics.json').read_text())['records']
        ref = {task_key(r):r for r in json.loads((root / 'final_eval_analytic/metrics.json').read_text())['records']}
        if set(map(task_key, fb)) != set(ref):
            raise AssertionError('Analytic and learned evaluation cases do not match')
        report['paired_FB_minus_analytic_error'] = {}
        for task, name in enumerate(NAMES):
            diff = [r['physical_error'] - ref[task_key(r)]['physical_error'] for r in fb
                    if r['task'] == task and r['physical_error'] is not None
                    and ref[task_key(r)]['physical_error'] is not None]
            report['paired_FB_minus_analytic_error'][name] = dict(n=len(diff),
                mean=float(np.mean(diff)), median=float(np.median(diff)), unit=UNITS[task])
    atlas = []
    for path in sorted((root / 'final_eval/random_z').glob('*.npz')):
        data = np.load(path)
        y = data['y']
        q = y[:, :, 0] * 1.2
        v = y[:, :, 1] * 6
        endpoint = q[:, -100:].mean(1)
        atlas.append(dict(model=path.stem, n=len(q),
            mean_range_rad=float(np.ptp(q, axis=1).mean()),
            terminal_q_std_rad=float(endpoint.std()),
            within_z_pair_terminal_difference_rad=float(np.abs(np.diff(endpoint.reshape(-1, 2), axis=1)).mean()),
            terminal_speed_rms=float(np.sqrt(np.mean(v[:, -100:]**2))),
            saturation_fraction=float(np.mean(np.abs(y[:, :, 13]) > .98)),
            near_limit_fraction=float(np.mean(np.abs(q) > 1.1)),
            limit_overrun_max_rad=float(max(0., np.abs(q).max() - 1.2)),
            contact_fraction=float(np.mean(y[:, :, 14:16].max(axis=-1) > 0))))
    if atlas:
        report['atlas'] = atlas
    switch_path = root / 'switching/metrics.json'
    if switch_path.exists():
        rows = json.loads(switch_path.read_text())['records']
        report['switching'] = []
        for model in sorted({r['model'] for r in rows}):
            for period in (0, 4, 8, 50, 100):
                group = [r for r in rows if r['model'] == model and r['period_steps'] == period]
                stats = dict(model=model, period_ms=period*10, n=len(group))
                for key in ('tracking_rmse_rad', 'switch_mean_abs_du', 'switch_max_abs_du',
                            'saturation', 'dq_rms', 'limit_overrun_max_rad', 'paired_fixed_q_rms_difference'):
                    stats[key] = mean([r.get(key) for r in group])
                report['switching'].append(stats)
    (out / 'summary.json').write_text(json.dumps(report, indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    w = np.array([r['W'] / 1e6 for r in trace])
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for name in ('f_grad', 'b_grad', 'actor_grad'):
        axes[0, 0].semilogy(w, [r['learning'][name] for r in trace], label=name)
    axes[0, 0].set_title('Gradient norms before any clipping (none used)')
    for name in ('fb_offdiag', 'fb_positive', 'orth'):
        axes[0, 1].plot(w, [r['learning'][name] for r in trace], label=name)
    axes[0, 1].set_title('Reference FB terms; values are not task performance')
    for index, name in ((0, 'min eigenvalue'), (-1, 'max eigenvalue')):
        axes[1, 0].plot(w, [r['covariance_eigenvalues'][index] for r in trace], label=name)
    axes[1, 0].set_title('B second moment spectrum')
    axes[1, 1].plot(w, [r['projection_nrmse'] for r in trace], label='diagnostic reward readout')
    axes[1, 1].set_title('Readout NRMSE (no gradient)')
    for ax in axes.flat:
        ax.set_xlabel('W / million (includes shared P0)')
        ax.grid(alpha=.25)
        ax.legend()
    fig.savefig(out / 'training.png', dpi=150)
    plt.close(fig)
    monitors = [(int(path.parent.name[1:]), json.loads(path.read_text())['summary'])
                for path in sorted((root / 'validation').glob('*/metrics.json'))]
    if monitors:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        for task, ax in enumerate(axes.flat):
            name = NAMES[task]
            ax.plot([r[0]/1e6 for r in monitors], [r[1][name]['mean_physical_error'] for r in monitors])
            ax.set_title(name + ' / ' + UNITS[task])
            ax.set_xlabel('W / million; repeated monitor panel')
            ax.grid(alpha=.25)
        fig.savefig(out / 'monitor_errors.png', dpi=150)
        plt.close(fig)
    print(json.dumps(dict(out=str(out), W=report['W'], finite=report['finite_learning'])))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    run(parser.parse_args().run)


if __name__ == '__main__':
    main()
