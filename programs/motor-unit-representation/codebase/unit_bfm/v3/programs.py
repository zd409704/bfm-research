"""Behaviour programs generate real canonical torque requests, never training rewards."""
from __future__ import annotations
import copy
import numpy as np

class TimeDeficitScheduler:
    """Account elapsed control steps, rather than equal numbers of unequal calls."""
    def __init__(self,weights):
        if not weights or any(v<=0 for v in weights.values()) or not np.isclose(sum(weights.values()),1):
            raise ValueError('positive normalized time weights required')
        self.weights=dict(weights); self.steps={k:0 for k in weights}
    def choose(self):
        total=sum(self.steps.values())
        return max(self.weights,key=lambda k:self.weights[k]*(total+1)-self.steps[k])
    def record(self,key,steps): self.steps[key]+=int(steps)
    def state_dict(self): return {'weights':self.weights,'steps':self.steps}
    def load_state_dict(self,s):
        if self.weights!=s['weights']: raise ValueError('scheduler specification changed')
        self.steps=dict(s['steps'])

class CallScheduler:
    def __init__(self,seed=0,dt=.01):
        self.rng=np.random.default_rng(seed); self.dt=dt
        self.time=TimeDeficitScheduler({'short':.2,'long':.8})
        self.remaining=0; self.kind=None
    def begin(self):
        self.kind=self.time.choose()
        duration=float(self.rng.choice([.04,.08])) if self.kind=='short' else float(self.rng.uniform(.5,2.0))
        self.remaining=max(1,int(round(duration/self.dt)))
        return self.remaining
    def step(self):
        if self.remaining<=0: raise RuntimeError('call not started')
        self.time.record(self.kind,1); self.remaining-=1
    def state_dict(self): return {'time':self.time.state_dict(),'rng':self.rng.bit_generator.state,'remaining':self.remaining,'kind':self.kind,'dt':self.dt}
    def load_state_dict(self,s):
        self.time.load_state_dict(s['time']); self.rng.bit_generator.state=s['rng']; self.remaining=s['remaining']; self.kind=s['kind']; self.dt=s['dt']

class RuleProgram:
    """Inertia-scaled PD/I, time-budgeted impulses, motion and load/release holds.

    External load/object trajectories belong to physics; program labels never assert
    that a load was present or released. Those claims require measured diagnostics.
    """
    VERSION='rule-inertia-pid-1'
    def __init__(self,known,seed=0,dt=.01,feedforward=None,fixed_side="P",load_schedule=None):
        self.known=copy.deepcopy(known); self.rng=np.random.default_rng(seed); self.dt=dt
        self.schedule=TimeDeficitScheduler({'transient':.2,'motion':.3,'load_release':.5})
        self.remaining=0; self.elapsed=0; self.integral=0.; self.feedforward=feedforward
        self.fixed_side=fixed_side;self.load_schedule=load_schedule
        rigid=np.asarray(known['rigid']); rigid=rigid if fixed_side=='P' else np.r_[rigid[4:],rigid[:4]]; drive=np.asarray(known['drive'])
        inertia=max(.005,float(rigid[7]+rigid[4]*(rigid[5]**2+rigid[6]**2)+drive[7]))
        self.kp=inertia*36; self.kd=inertia*12; self.ki=.5*self.kp
        self.q_ref=0.; self.mode=None; self.category=None; self.duration=0
        self.last={}; self.count=0
    def _begin(self,b):
        self.category=self.schedule.choose(); self.elapsed=0; self.integral=0
        lo,hi=np.asarray(self.known['limits']); width=hi-lo
        self.q_ref=float(lo+(.05+.9*((self.count%10)+.5)/10)*width)
        if hasattr(self,'target_xi'):self.q_ref=float(lo+np.clip(self.target_xi,.02,.98)*width)
        self.count+=1
        if self.category=='transient':
            self.duration=int(self.rng.choice([4,8])); self.mode='torque'
            self.tau_ref=float(self.rng.choice([-1,1]))*float(self.known['drive'][0])
        elif self.category=='motion':
            self.duration=int(self.rng.integers(50,201)); self.mode=str(self.rng.choice(['sweep','velocity','compliance']))
            self.velocity=float(self.rng.choice([-4,-2,-1,-.5,.5,1,2,4]))
            self.q_start=float(b['q']); self.amplitude=.4*width
            self.frequency=float(self.rng.uniform(.2,.8))
        else:
            self.duration=200; self.mode='hold'; self.q_start=float(b['q'])
        self.remaining=self.duration
    def action(self,b,known=None):
        if known is not None: self.known=copy.deepcopy(known)
        if self.remaining<=0: self._begin(b)
        q=float(b['q']); dq=float(b['dq']); S=float(self.known['drive'][0]); lo,hi=self.known['limits']
        phase='main'
        if self.load_schedule is not None:
            now=float(b['time']);start=self.load_schedule.load_start;end=self.load_schedule.load_end
            if getattr(self.load_schedule,'load_mode','single')=='repeated':
                cycle=max(0,int(np.floor((now-start)/self.load_schedule.load_period)))
                if cycle<self.load_schedule.load_repeats:now-=cycle*self.load_schedule.load_period
            phase='approach' if now<start else ('main' if now<end else ('unload' if now<end+self.dt else 'recovery'))
        elif self.category=='load_release':
            phase='unverified_load_schedule'
        ff=float(self.feedforward(b)) if self.feedforward is not None else 0.
        if self.mode=='torque': tau=self.tau_ref
        else:
            if self.mode=='sweep':
                center=(lo+hi)/2
                self.q_ref=float(center+self.amplitude*np.sin(2*np.pi*self.frequency*self.elapsed*self.dt))
            error=self.q_ref-q
            if self.mode=='velocity':
                # Braking envelope from declared available torque and tuning inertia.
                acceleration=max(.1,abs(float(self.known['drive'][2]))/(self.kp/36))
                stop=np.sqrt(max(0,2*acceleration*((hi-q) if self.velocity>0 else (q-lo)))*.7)
                v_ref=np.sign(self.velocity)*min(abs(self.velocity),stop)
                tau=ff+self.kd*(v_ref-dq)
            elif self.mode=='compliance': tau=ff+.3*self.kp*error-.5*self.kd*dq
            else:
                trial=self.integral+error*self.dt
                tau_trial=ff+self.kp*error-self.kd*dq+self.ki*trial
                lower,upper=float(self.known['drive'][1]),float(self.known['drive'][2])
                if not ((tau_trial>upper and error>0) or (tau_trial<lower and error<0)): self.integral=trial
                tau=ff+self.kp*error-self.kd*dq+self.ki*self.integral
        u=float(np.clip(tau/S,-1,1))
        self.last={'program':self.mode,'category':self.category,'phase':phase,'q_ref':self.q_ref,
                   'tau_ref':float(tau),'S':S,'u_c':u,'feedforward':ff,
                   'gain_source':'declared_output_inertia','kp':self.kp,'kd':self.kd,'ki':self.ki,
                   'privileged_feedforward':self.feedforward is not None,'reference_time':float(b['time']),
                   'response_time':float(b['time'])+self.dt,'physical_load_phase':phase,'integral':self.integral}
        self.schedule.record(self.category,1); self.elapsed+=1; self.remaining-=1
        return u,phase,dict(self.last)

    def state_dict(self):
        return {'version':self.VERSION,'rng':self.rng.bit_generator.state,'time':self.schedule.state_dict(),
                'state':{k:copy.deepcopy(v) for k,v in self.__dict__.items() if k not in ('rng','schedule','feedforward')}}

    def load_state_dict(self,s):
        if s['version']!=self.VERSION: raise ValueError('program version')
        self.rng.bit_generator.state=s['rng']; self.schedule.load_state_dict(s['time'])
        self.__dict__.update(copy.deepcopy(s['state']))


def calibrate_rule(env,targets,duration_s=3.,seed=0):
    """Independent static feasibility and actual hold test, with honest failure classes.

    CPU oracle-only calibration; resets are explicit, controller never writes state.
    Returns evidence instead of toggling any formal coverage flag.
    """
    import mujoco
    from .collect import oracle_static_feedforward
    results=[]
    for episode,target in enumerate(targets):
        b=env.reset(episode_id=episode);known=env.known;lo,hi=known['limits']
        if not lo<=target<=hi:
            results.append({'target':target,'classification':'mechanically_infeasible','reason':'outside verified limits'});continue
        probe=mujoco.MjData(env.model);probe.qpos[:]=env.data.qpos;probe.qvel[:]=0
        probe.qpos[env.qadr]=env.tree_sign*target;mujoco.mj_forward(env.model,probe)
        required=float(env.tree_sign*probe.qfrc_bias[env.vadr]);declared=known['drive'][1:3]
        feasible=bool(declared[0]<=required<=declared[1])
        controller=RuleProgram(known,seed+episode,feedforward=oracle_static_feedforward(env),fixed_side=env.config.fixed_side,load_schedule=env.config)
        controller.category='load_release';controller.mode='hold';controller.q_ref=float(target)
        controller.duration=controller.remaining=int(round(duration_s/.01));controller.elapsed=0
        streak=best=0.;trace=[]
        for _ in range(controller.duration):
            u,phase,info=controller.action(b,env.known);b=env.step(u)
            trace.append({'time':b['time'],'q':b['q'],'dq':b['dq'],'tau':b['tau_endpoint'],'u':u,'valid':b['valid']})
            streak=streak+.01 if abs(b['q']-target)<=.05 and abs(b['dq'])<=.05 and b['valid'] else 0.;best=max(best,streak)
            if b['terminated'] or b['truncated']:break
        classification='passed' if best>=.2 else ('numerical_failure' if not all(r['valid'] for r in trace) else ('capacity_limited' if not feasible else 'rule_not_converged'))
        results.append({'target':float(target),'static_required_torque':required,'declared_capacity':list(declared),
                        'static_feasible':feasible,'classification':classification,'longest_hold_s':best,'trace':trace,
                        'scope':'static same other-joint coordinates; dynamic external constraints require separate calibration'})
    return {'version':'v3-rule-calibration-1','results':results,'all_passed':all(x['classification']=='passed' for x in results)}


def calibrate(config,output,quick=False):
    """Executable evidence generation, bound to exact config/code/schema hashes."""
    import json,time
    from pathlib import Path
    from dataclasses import replace
    from .physics import make_scene,UnitEnv
    from .train import safe_run_directory,schema_manifest
    from .replay import plain,fingerprint,file_hash,storage_report
    from .collect import collect_episode
    root=safe_run_directory(output);results=[];schemas=[];failures=[];noise=[];count=0
    begin=time.monotonic()
    # Independent zero-load fixed-side holds, actual light/heavy and both trees.
    for side in ('P','D'):
        for mass in (.2,1.5):
            cfg=make_scene(seed=config['seed'],scene='E0',fixed_side=side,masses=(mass,mass),ballast_ratios=(0.,0.),
                           capacity_nominal=9.,duration=3. if quick else 5.,load_force=0.,load_couple=0.,tilt=0.,initial_q=0.)
            env=UnitEnv(cfg)
            try:
                result=calibrate_rule(env,[0.,.3] if quick else [-1.4,-.3,0.,.3,1.4],duration_s=cfg.duration)
                results.append({'side':side,'mass':mass,**result});schemas.append(schema_manifest(env))
                env.reset();trace=[env.step(0.) for _ in range(10 if quick else 100)]
                noise.append({'side':side,'mass':mass,'dq_abs_max':max(abs(r['dq']) for r in trace),
                              'tau_abs_max':max(abs(r['tau_endpoint']) for r in trace),
                              'contact_noise_N':max(float(r['diagnostics'].get('contact_normal_force_N',float('nan'))) for r in trace)})
            except (ValueError,RuntimeError,FloatingPointError) as exc:failures.append({'side':side,'mass':mass,'error':repr(exc)})
            finally:env.close()
    # Real broad-scene records, including failed physics, for size and SI contract checks.
    checks=[]
    required=('contact_normal_force_N','adjacent_max_abs_dq','fixture_P_force_N','fixture_D_force_N','applied_load_norm_N','solver_valid')
    for scene in config['collection']['scene_weights']:
        try:
            env=UnitEnv(make_scene(seed=config['seed'],scene=scene,duration=.2 if quick else 1.))
            try:
                ep=collect_episode(env,f'calibration_{scene}',max_steps=20 if quick else 100)
                ep.save(root/'archive');count+=len(ep)
                checks.append({'scene':scene,'valid':bool(ep.valid.all()),'reconstruct':all(np.allclose(v,getattr(ep,k),atol=1e-5) for k,v in ep.reconstruct().items()),
                               'missing_diagnostics':[k for k in required if any(k not in r['diagnostics'] for r in ep.raw[1:])]})
            finally:env.close()
        except (ValueError,RuntimeError,FloatingPointError) as exc:failures.append({'scene':scene,'error':repr(exc)})
    code={p.name:file_hash(p) for p in Path(__file__).parent.glob('*.py')}
    report={'version':'v3-preflight-2','config_hash':fingerprint(config),'code_hashes':code,'schema_hash':fingerprint(schemas[0]) if schemas else None,
            'rule_calibration':results,'noise':noise,'physics_checks':checks,'failures':failures,'quick':quick,'elapsed_s':time.monotonic()-begin,
            'conditional_manifest_hash':fingerprint(config['coverage']['groups']),
            'storage':storage_report(root/'archive',count,count) if count else None}
    report['implementation_ready']=bool(checks and all(c['valid'] and c['reconstruct'] and not c['missing_diagnostics'] for c in checks) and not failures)
    report['rules_calibrated']=bool(results and all(r['all_passed'] for r in results))
    report['noise_calibrated']=bool(noise and all(np.isfinite(r['contact_noise_N']) and 5*r['contact_noise_N']<config['coverage']['thresholds']['contact_force_floor_N'] for r in noise))
    report['formal_ready']=bool(not quick and report['implementation_ready'] and report['rules_calibrated'] and report['noise_calibrated'])
    (root/'preflight.json').write_text(json.dumps(plain(report),indent=2,allow_nan=False));return report


def main(argv=None):
    import argparse,json
    from pathlib import Path
    from .train import load_config
    p=argparse.ArgumentParser(description='V3 real CPU rule/physics/noise/storage calibration')
    p.add_argument('--config',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--quick',action='store_true')
    a=p.parse_args(argv);report=calibrate(load_config(a.config),a.output,a.quick)
    print(json.dumps({k:report[k] for k in ('implementation_ready','rules_calibrated','noise_calibrated','formal_ready','elapsed_s')}))
if __name__=='__main__':main()
