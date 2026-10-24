"""Measure observation-ready to returned-action latency, not simulator throughput."""
import argparse,json,time
from pathlib import Path
import numpy as np
import torch
from .interface import FrozenUnit


def main():
    p=argparse.ArgumentParser(); p.add_argument('--bundle',required=True); p.add_argument('--out',required=True)
    p.add_argument('--device',default='cpu'); p.add_argument('--samples',type=int,default=1000)
    a=p.parse_args(); torch.set_num_threads(1)
    records=[]
    for count in (1,2):
        unit=FrozenUnit(a.bundle,nworld=count,device=a.device)
        o=torch.zeros(count,24); o[:,[3,8]]=1; o[:,16:18]=.5
        m=torch.zeros(count,28); m[:,14:]=1
        z=torch.zeros(count,16); z[:,0]=4
        unit.reset(o,m)
        elapsed=[]
        for step in range(a.samples+30):
            start=time.perf_counter_ns()
            unit.observe(o)
            feedback=unit.feedback().cpu().numpy()
            action=unit.act(z).cpu().numpy()
            elapsed.append((time.perf_counter_ns()-start)/1e6)
        times=np.asarray(elapsed[30:])
        records.append(dict(units=count,device=a.device,median_ms=float(np.median(times)),
            p95_ms=float(np.quantile(times,.95)),p99_ms=float(np.quantile(times,.99)),
            observed_max_ms=float(times.max()),deadline_misses_10ms=int((times>10).sum()),samples=a.samples))
    result=dict(boundary='normalized observation ready -> history, B/context, host feedback, Actor, host action',
                excludes=['sensor communication','motor communication','upper policy','simulation'],records=records)
    Path(a.out).write_text(json.dumps(result,indent=2)); print(json.dumps(result))

if __name__=='__main__': main()
