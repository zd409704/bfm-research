"""Add an explicit contract to a separate candidate artifact without accepting it."""
import argparse
import hashlib
import json
from pathlib import Path

import torch

from . import VERSION
from .schema import contract


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    run = Path(args.run)
    source = run / 'candidate_unit.pt'
    destination = run / 'candidate_unit_with_schema.pt'
    if destination.exists():
        raise FileExistsError('Keep prior exports; choose a new run or inspect the existing artifact.')
    state = torch.load(source, weights_only=False, map_location='cpu')
    if state['version'] != VERSION:
        raise ValueError('Cannot attach a different schema version')
    state.update(schema=contract(), validated=False, candidate=True)
    state['postprocessing'] = dict(
        purpose='Explicit field order, units, privileged-input boundary; no parameter changes.',
        source_candidate_sha256=digest(source),
        source_checkpoint_sha256=digest(run / 'checkpoint.pt'),
        scripts_sha256={p.name:digest(p) for p in
                       (Path(__file__), Path(__file__).with_name('schema.py'))})
    torch.save(state, destination)
    result = dict(path=str(destination), sha256=digest(destination), W=state['W'],
                  validated=False, schema=state['schema'], postprocessing=state['postprocessing'])
    (run / 'export_manifest.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({k:result[k] for k in ('path','sha256','W','validated')}))


if __name__ == '__main__':
    main()
