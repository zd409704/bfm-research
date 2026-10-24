"""Frozen Actor/B runtime. No privileged input or F module is needed to act."""
from __future__ import annotations
import copy
from pathlib import Path
import numpy as np
import torch
from . import VERSION
from .replay import fingerprint, plain

def export_actor_b(learner,destination,schema,query_manifest=None):
    path=Path(destination); path.mkdir(parents=True,exist_ok=False)
    actor=copy.deepcopy(learner.net.actor).cpu().eval().requires_grad_(False)
    b=copy.deepcopy(learner.net.b).cpu().eval().requires_grad_(False)
    # Trace only public x/z and g inputs; no training-only F/p in exported graph.
    torch.jit.trace(actor,(torch.zeros(1,137),torch.ones(1,16))).save(str(path/'actor.pt'))
    torch.jit.trace(b,torch.zeros(1,13)).save(str(path/'b.pt'))
    import json
    manifest={'version':VERSION,'export_version':'actor-b-only-1','schema':plain(schema),
              'schema_hash':fingerprint(schema),'g_dim':13,'x_dim':137,'z_dim':16,
              'query_manifest':plain(query_manifest),'privileged_inputs':False,'extra_F_privileged_vector_required':False,
              'telemetry_privilege':{'tau_endpoint':'exact simulator output-axis torque; privileged simulation telemetry',
                                     'hardware_validated':False},'deployment_claim':'no additional F p; exact torque telemetry still privileged'}
    (path/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return manifest

class Interface:
    def __init__(self,export_path,device='cpu'):
        import json
        path=Path(export_path); self.manifest=json.loads((path/'manifest.json').read_text())
        if self.manifest.get('version')!=VERSION or self.manifest.get('export_version')!='actor-b-only-1': raise ValueError('V3 export required')
        if self.manifest['schema_hash']!=fingerprint(self.manifest['schema']): raise ValueError('schema integrity')
        if self.manifest.get('privileged_inputs') is not False: raise ValueError('privileged deployment graph')
        self.actor=torch.jit.load(str(path/'actor.pt'),map_location=device).eval()
        self.b=torch.jit.load(str(path/'b.pt'),map_location=device).eval(); self.device=device; self.history=None
    def reset(self,known_model,telemetry,coordinate_map=None):
        from .features import FeatureHistory
        mapping=coordinate_map or known_model.get('coordinate_map')
        if not mapping or mapping.get('calibration_valid') is not True: raise ValueError('trusted canonical output calibration required')
        if mapping.get('telemetry_coordinates','canonical')!='canonical': raise ValueError('adapt raw output telemetry before Interface')
        self.coordinate_map=copy.deepcopy(mapping); self.known={k:copy.deepcopy(known_model[k]) for k in ('lengths','limits','rigid','rigid_valid','drive','drive_valid')}
        self.history=FeatureHistory(); self.history.reset(telemetry,self.known); self.telemetry=copy.deepcopy(telemetry)
        return self.feedback()
    def observe(self,telemetry,known_model=None):
        if self.history is None: raise RuntimeError('reset first')
        if known_model is not None: self.known={k:copy.deepcopy(known_model[k]) for k in ('lengths','limits','rigid','rigid_valid','drive','drive_valid')}
        self.history.append(telemetry,self.known); self.telemetry=copy.deepcopy(telemetry)
        return self.feedback()
    def feedback(self):
        if self.history is None: raise RuntimeError('reset first')
        f=self.history.features()
        with torch.no_grad(): b=self.b(torch.as_tensor(f['g'],dtype=torch.float32,device=self.device)[None]).cpu().numpy()[0]
        from .queries import SCALES
        physical=np.asarray(f['g'])*SCALES
        return {'physical':dict(zip(('L_P','L_D','q','dq','tau','q_min','q_max','tip_vx','tip_vz','ddq_hat','tip_ax','tip_az','acc_valid'),physical.tolist())),
                'B16':b,'acc_valid':bool(f['g'][12]>.5),'known_model':copy.deepcopy(self.known),
                'known_drive':np.asarray(self.known['drive']).copy(),'drive_valid':np.asarray(self.known['drive_valid']).copy(),
                'coordinate_map':copy.deepcopy(self.coordinate_map)}
    def act(self,z):
        if self.history is None: raise RuntimeError('reset first')
        z=np.asarray(z,dtype=np.float32)
        if z.shape!=(16,) or not np.isfinite(z).all(): raise ValueError('finite z16 required')
        with torch.no_grad():
            x=torch.as_tensor(self.history.features()['x'],dtype=torch.float32,device=self.device)[None]
            return float(self.actor(x,torch.as_tensor(z,device=self.device)[None]).reshape(-1)[0].cpu())


def main(argv=None):
    import argparse,json
    from pathlib import Path
    from .learner import Learner
    from .train import safe_run_directory
    p=argparse.ArgumentParser(description='Export frozen V3 Actor/B from complete checkpoint')
    p.add_argument('--checkpoint',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(argv);state=torch.load(a.checkpoint,map_location='cpu',weights_only=False)
    if state.get('version')!=VERSION:raise ValueError('V3 checkpoint required')
    learner=Learner(state['schema']['p_dim'],config=state['learner']['config']);learner.load_state_dict(state['learner'])
    parent=safe_run_directory(a.output)
    manifest=export_actor_b(learner,parent/'actor_b',state['schema'])
    print(json.dumps({'output':str(parent/'actor_b'),'telemetry_privilege':manifest['telemetry_privilege']}))
if __name__=='__main__':main()
