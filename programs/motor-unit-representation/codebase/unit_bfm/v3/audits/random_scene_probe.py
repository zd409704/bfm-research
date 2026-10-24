"""Coordinator probe, prints real randomized assembly/rollout failures as JSON."""
import json,time
from dataclasses import replace
from unit_bfm.v3.physics import UnitEnv,make_scene

def probe():
    started=time.monotonic();fail=[];success=0
    for seed in range(10):
        for scene in ('E0','E1','E2','E3','E4'):
            for side in ('P','D'):
                env=None
                try:
                    c=make_scene(seed=100+seed,geometry_id=seed,limit_id=seed%4,scene=scene,fixed_side=side)
                    env=UnitEnv(c)
                    for t in range(30):
                        b=env.step(.25 if t<15 else -.25)
                        if not b['valid']:raise ValueError('invalid '+str(b['diagnostics']))
                    success+=1
                except Exception as e:fail.append(dict(seed=seed,scene=scene,side=side,error=str(e)))
                finally:
                    if env:env.close()
    return dict(success=success,failed=len(fail),failures=fail,seconds=time.monotonic()-started)
if __name__=='__main__':print(json.dumps(probe(),indent=2))
