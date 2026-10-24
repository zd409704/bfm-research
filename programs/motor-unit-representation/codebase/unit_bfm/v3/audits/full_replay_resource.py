import json,hashlib,time,resource,gc,threading
from pathlib import Path
import numpy as np
import torch
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.privileged import P_DIM
from unit_bfm.v3.schema import MEMORY_DIM
from unit_bfm.v3.tests.test_pipeline_contract import synthetic
ROOT=Path('unit_bfm/v3/runs/coordinator_full_replay_01');ROOT.mkdir(exist_ok=False);torch.set_num_threads(1)
def rss():
 for l in Path('/proc/self/status').read_text().splitlines():
  if l.startswith('VmRSS:'):return int(l.split()[1])*1024
report={'p_dim':P_DIM+MEMORY_DIM,'capacity':98304,'rule_capacity':32768,'policy_capacity':65536,'hash_before':hashlib.sha256(Path('unit_bfm/v3/replay.py').read_bytes()).hexdigest(),'baseline_rss':rss(),'stages':{}}
r=Replay(rule_capacity=32768,policy_capacity=65536,p_dim=P_DIM+MEMORY_DIM,scene_weights={'E0':1.})
e=synthetic('fixture',128);e.p=np.tile(np.arange(P_DIM+MEMORY_DIM,dtype=np.float32),(129,1))
def add(count,source,p0=False):
 e.source=source
 for i in range(count//128):e.episode_id=f'{source}_{p0}_{i}';r.add(e,p0=p0)
def save(label):
 data={'before_rss':rss(),'active':len(r),'tensor_capacity_bytes':sum(v.nbytes for v in r.arrays.values())};peaks=[data['before_rss']];stop=threading.Event()
 def watch():
  while not stop.wait(.002):peaks.append(rss())
 th=threading.Thread(target=watch);th.start();t=time.perf_counter();s=r.state_dict();data['state_rss']=rss();data['compact_bytes']=sum(v.numel()*v.element_size() for v in s['arrays'].values());data['full_zero_copy']=all(v.data_ptr()==r.arrays[k].ctypes.data for k,v in s['arrays'].items())
 path=ROOT/('memory_01_'+label+'.pt');torch.save(s,path);data['save_seconds']=time.perf_counter()-t;data['file_bytes']=path.stat().st_size;peaks.append(rss());stop.set();th.join();data['sampled_peak_rss']=max(peaks);data['process_peak_rss']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024;del s;gc.collect();data['after_rss']=rss();report['stages'][label]=data
add(8192,'rule',True);add(16384,'policy');save('quarter')
add(16384,'rule',True);add(16384,'rule');add(65536,'policy');assert len(r)==r.capacity;save('full')
del r,e;gc.collect();data={'before_rss':rss()};t=time.perf_counter();s=torch.load(ROOT/'memory_01_full.pt',weights_only=False);data['loaded_rss']=rss();rr=Replay(rule_capacity=1,policy_capacity=1);rr.load_state_dict(s);data.update(after_restore_rss=rss(),seconds=time.perf_counter()-t,active=len(rr),arrays_consumed=not s['arrays']);report['load_full']=data
report['hash_after']=hashlib.sha256(Path('unit_bfm/v3/replay.py').read_bytes()).hexdigest();(ROOT/'checkpoint_memory_01.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
