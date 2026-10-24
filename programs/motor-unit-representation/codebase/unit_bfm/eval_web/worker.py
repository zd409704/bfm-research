"""Execute the existing frozen-policy evaluation methods in an isolated process."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from .data import ARTIFACTS, ROOT, VERSION, confined


def write(path, payload):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    temp.replace(path)


def run(job_path):
    import torch
    import warp as wp
    from ..learner import Learner
    from ..diagnose_motion import run as nominal
    from ..evaluate import evaluate, random_atlas
    from ..evaluate_switching import run as switching

    job_path = Path(job_path)
    job = json.loads(job_path.read_text())
    checkpoint = confined(ARTIFACTS, job['checkpoint'])
    digest = hashlib.sha256()
    with checkpoint.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    job['checkpoint_sha256'] = digest.hexdigest()
    job['source_sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (ROOT/'unit_bfm').glob('*.py')}
    job['source_sha256'].update({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in Path(__file__).parent.glob('*.py')})
    job['stage'] = 'Load Freezing weights'
    write(job_path, job)
    print('Organisation'+job['checkpoint'], flush=True)
    torch.set_num_threads(1)
    torch.manual_seed(20261001)
    wp.config.quiet = True
    state = torch.load(checkpoint, weights_only=False, map_location='cuda:0')
    if state.get('version') != VERSION or state['learner'].get('version') != VERSION:
        raise ValueError('Only support V2Learner Checkpoint')
    learner = Learner(state['learner']['reference'])
    learner.load_state_dict(state['learner'])
    learner.net.eval().requires_grad_(False)
    job['W'] = state['W']
    del state
    results = []

    def stage(folder, label, kind, fn, compare=None):
        job['stage'] = label
        write(job_path, job)
        print('_Other Organiser'+label, flush=True)
        with torch.no_grad():
            fn(job_path.parent/folder)
        results.append(dict(folder=folder,label=label,kind=kind,compare=compare))
        print('_Other Organiser'+label, flush=True)

    plan=job['plan']
    if plan=='nominal':
        stage('nominal','Keep the name on three queries.','nominal',lambda p:nominal(learner,p))
    elif plan=='cross':
        stage('fb','Cross-Conditions Query . FB','cross',lambda p:evaluate(learner,p,full=True,save_trajectories=True),compare='analytic')
        stage('analytic','Cross-Conditions Query Query Query Query Query Query Query','analytic',lambda p:evaluate(learner,p,full=True,analytic=True,save_trajectories=True))
    elif plan=='switch_goal':
        stage('switch_goal','Toggle Panel','switch_goal',lambda p:switching(learner,p))
    elif plan=='switch_reward':
        stage('switch_reward','Incentive Query Switch','switch_reward',lambda p:switching(learner,p,nominal_query='reward',nominal_only=True))
    elif plan=='atlas':
        stage('atlas','Random z spectra','atlas',lambda p:random_atlas(learner,p,nz=256))
    else:
        raise ValueError('Unknown assessment item')
    job.update(status='completed',stage='Evaluation complete.',results=results,finished_at=time.time())
    write(job_path,job)
    print('All completed; weights not updated.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--job',required=True)
    run(parser.parse_args().job)
