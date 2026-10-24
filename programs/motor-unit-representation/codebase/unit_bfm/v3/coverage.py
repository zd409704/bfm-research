"""Conditional coverage. Missing evidence is a deficit, never an inferred pass."""
from __future__ import annotations
from collections import defaultdict, Counter
from pathlib import Path
import html
import json
import numpy as np
from .replay import plain, fingerprint

DEFAULT_THRESHOLDS={'xi_episodes':2,'xi_steps':20,'cross_xi_episodes':20,'process_episodes':2,
    'active_duration_s':.5,'hold_duration_s':.2,'hold_q_error':.05,'hold_dq':.05,
    'contact_force_floor_N':.2,'contact_weight_fraction':.02,'adjacent_dq':.05,
    'adjacent_stall_capacity_fraction':.1,'fixture_weight_fraction':.02,
    'fixture_capacity_fraction':.02,'e4_contact_motion_fraction':.2,'e4_bilateral_fraction':.25,
    'scene_fraction_tolerance':.05,'noise_multiplier':5,'motion_dq':.05}

def longest_duration(mask,dt):
    best=cur=0.
    for ok,d in zip(mask,dt):
        cur=cur+float(d) if ok else 0.; best=max(best,cur)
    return best

def _diagnostic_array(ep,name,default=np.nan):
    direct=[r.get('diagnostics',{}).get(name,default) for r in ep.raw[1:]]
    if np.isfinite(direct).all(): return np.asarray(direct,dtype=float)
    # No fallback over all geom contacts: only the physics SI diagnostics contract is authoritative.
    return np.asarray(direct,dtype=float)

def inspect_episode(ep,thresholds):
    t=thresholds; n=len(ep); valid=np.asarray(ep.valid,dtype=bool)
    dt=np.asarray([r['interval_dt'] for r in ep.raw[1:]])
    q=np.asarray([r['q'] for r in ep.raw[:-1]]); dq=np.asarray([r['dq'] for r in ep.raw[:-1]])
    tau=np.asarray([r['tau_endpoint'] for r in ep.raw[:-1]])
    xi=np.asarray(ep.bins['xi']); end_xi=np.asarray([r['q'] for r in ep.raw[1:]])
    limits=np.asarray([k['limits'] for k in ep.known[:-1]])
    end_xi=(end_xi-limits[:,0])/(limits[:,1]-limits[:,0])
    mass=float(np.asarray(ep.known[0]['rigid'])[[0,4]].sum()); capacity=max(abs(float(ep.known[0]['drive'][1])),abs(float(ep.known[0]['drive'][2])))
    force=_diagnostic_array(ep,'contact_normal_force_N'); adjacent=_diagnostic_array(ep,'adjacent_max_abs_dq')
    adjacent_tau=_diagnostic_array(ep,'adjacent_max_abs_tau_Nm')
    adjacent_capacity=_diagnostic_array(ep,'adjacent_declared_capacity_Nm')
    fixture_p=_diagnostic_array(ep,'fixture_P_force_N'); fixture_d=_diagnostic_array(ep,'fixture_D_force_N')
    torque_p=_diagnostic_array(ep,'fixture_P_torque_Nm'); torque_d=_diagnostic_array(ep,'fixture_D_torque_Nm')
    solver_values=_diagnostic_array(ep,'solver_valid'); solver=np.isfinite(solver_values)&(solver_values>.5)
    contact=force>max(t['contact_force_floor_N'],t['contact_weight_fraction']*mass*9.81)
    motion=adjacent>t['adjacent_dq']
    stall=np.asarray([any(axis['abs_dq']<=t['adjacent_dq'] and axis['abs_tau_Nm']>t['adjacent_stall_capacity_fraction']*axis['declared_capacity_Nm'] for axis in r['diagnostics'].get('adjacent_axes',[])) for r in ep.raw[1:]])
    p=(fixture_p>t['fixture_weight_fraction']*mass*9.81)|(np.abs(torque_p)>t['fixture_capacity_fraction']*capacity)
    d=(fixture_d>t['fixture_weight_fraction']*mass*9.81)|(np.abs(torque_d)>t['fixture_capacity_fraction']*capacity)
    active=valid&solver&contact&motion; bilateral=valid&solver&p&d
    load=_diagnostic_array(ep,'applied_load_norm_N')
    load_active=valid&solver&(load>max(t['contact_force_floor_N'],t['contact_weight_fraction']*mass*9.81))
    # A full load->unload->response run needs measured contiguous load and recovery.
    releases=0; loaded_duration=0.; recovering=0.; armed=False
    for ok,loaded,step in zip(valid&solver,load_active,dt):
        if not ok: loaded_duration=recovering=0.; armed=False; continue
        if loaded:
            loaded_duration+=step; recovering=0
            if loaded_duration>=t['active_duration_s']: armed=True
        else:
            if armed:
                recovering+=step
                if recovering>=t['active_duration_s']: releases+=1; armed=False
            loaded_duration=0
    refs=np.asarray([a.get('q_ref',np.nan) for a in (ep.behaviour() or [{}]*n)])
    q_response=np.asarray([r['q'] for r in ep.raw[1:]]);dq_response=np.asarray([r['dq'] for r in ep.raw[1:]])
    holding=valid&(np.abs(q_response-refs)<=t['hold_q_error'])&(np.abs(dq_response)<=t['hold_dq'])&load_active
    entry=(xi[1:]!=xi[:-1])&valid[1:]&valid[:-1]
    entries=Counter(map(int,xi[1:][entry])); exits=Counter(map(int,xi[:-1][entry]))
    processes={'positive_motion':bool(np.any(valid&(dq>t['motion_dq']))),
               'negative_motion':bool(np.any(valid&(dq<-t['motion_dq']))),
               'boundary_approach':bool(np.any(valid&(((xi==0)&(dq<-.05))|((xi==9)&(dq>.05))))),
               'boundary_departure':bool(np.any(valid&(((xi==0)&(dq>.05))|((xi==9)&(dq<-.05))))),
               'loaded_hold':longest_duration(holding,dt)>=t['hold_duration_s'],
               'load_release_recovery':releases>0,
               'contact_adjacent_active':longest_duration(active,dt)>=t['active_duration_s'],
               'bilateral_force':longest_duration(bilateral,dt)>=t['active_duration_s']}
    return {'response_alignment':'reference/action at t matched to response at t+1; current bins remain t',
            'action_saturated_steps':int(np.sum(np.abs(ep.u[:,0])>=.999)),
            'drive_saturated_steps':sum(bool(r.get('diagnostics',{}).get('saturated',False)) for r in ep.raw[1:]),
            'valid_steps':int(valid.sum()),'invalid_steps':int((~valid).sum()),
            'xi_steps':{str(i):int(np.sum(valid&(xi==i))) for i in range(10)},
            'entries':dict(entries),'exits':dict(exits),'processes':processes,'releases':releases,
            'active_steps':int(active.sum()),'bilateral_steps':int(bilateral.sum()),'stall_steps':int(np.sum(valid&solver&stall)),
            'max_active_s':longest_duration(active,dt),'max_bilateral_s':longest_duration(bilateral,dt),
            'acc_valid_steps':int(np.sum(valid&(ep.g[1:,12]>.5))),
            'missing_diagnostics':[k for k in ('contact_normal_force_N','adjacent_max_abs_dq','fixture_P_force_N','fixture_D_force_N','applied_load_norm_N','solver_valid') if not np.isfinite(_diagnostic_array(ep,k)).all()],
            'joint_histograms':{'xi_dq':np.histogram2d(xi[valid],dq[valid],bins=[np.arange(11)-.5,[-np.inf,-4,-2,-.5,.5,2,4,np.inf]])[0].astype(int).tolist(),
             'dq_tau':np.histogram2d(dq[valid],tau[valid],bins=[[-np.inf,-4,-2,-.5,.5,2,4,np.inf],[-np.inf,-6,-1.2,1.2,6,np.inf]])[0].astype(int).tolist(),
             'q_tau':np.histogram2d(q[valid],tau[valid],bins=[[-np.inf,-np.pi,-1.2,-.6,0,.6,1.2,np.pi,np.inf],[-np.inf,-6,-1.2,1.2,6,np.inf]])[0].astype(int).tolist(),
             'dq_ddq':np.histogram2d(dq[valid&(ep.g[:-1,12]>.5)],(ep.g[:-1,9]*200)[valid&(ep.g[:-1,12]>.5)],bins=[[-np.inf,-4,-2,-.5,.5,2,4,np.inf],[-np.inf,-200,-20,-2,2,20,200,np.inf]])[0].astype(int).tolist(),
             'length_D_dq':np.histogram2d((ep.g[:-1,1]*.4)[valid],dq[valid],bins=[[0,.15,.25,.35,.45,np.inf],[-np.inf,-4,-2,-.5,.5,2,4,np.inf]])[0].astype(int).tolist()}}

class Coverage:
    def __init__(self,spec):
        self.spec=plain(spec); self.thresholds={**DEFAULT_THRESHOLDS,**self.spec.get('thresholds',{})}
        self.spec_hash=fingerprint(self.spec); self.records=[];self.cross_counts=Counter();self.total_episodes=0
    def add(self,ep):
        s=inspect_episode(ep,self.thresholds)
        s.update({'episode_id':ep.episode_id,'source':ep.source,'scene':ep.scene,'config_id':ep.config_id,
                  'fixed_side':ep.metadata.get('fixed_side','UNKNOWN'),'cross_tags':ep.metadata.get('cross_tags',{}),
                  'failure_class':ep.metadata.get('failure_class','unclassified')})
        self.total_episodes+=1
        for i,cross in enumerate(self.spec.get('cross_requirements',[])):
            if all(s['cross_tags'].get(k)==v for k,v in cross['tags'].items()):self.cross_counts[i]+=1
        key=(s['source'],s['scene'],s['config_id'],s['fixed_side'])
        old=next((r for r in self.records if (r['source'],r['scene'],r['config_id'],r['fixed_side'])==key),None)
        if old is None:
            old={**s,'episode_count':0,'xi_episodes':{str(i):0 for i in range(10)},'processes':{k:0 for k in s['processes']},
                 'xi_steps':{str(i):0 for i in range(10)},'entries':{},'exits':{},'joint_histograms':{k:np.zeros_like(v).tolist() for k,v in s['joint_histograms'].items()}}
            for k in ('valid_steps','invalid_steps','active_steps','bilateral_steps','stall_steps','acc_valid_steps','releases','action_saturated_steps','drive_saturated_steps'):old[k]=0
            self.records.append(old)
        old['episode_count']+=1
        for b,v in s['xi_steps'].items():old['xi_steps'][b]+=v;old['xi_episodes'][b]+=int(v>0)
        for name,v in s['processes'].items():old['processes'][name]+=int(v)
        for name in ('entries','exits'):
            for b,v in s[name].items():old[name][str(b)]=old[name].get(str(b),0)+v
        for k in ('valid_steps','invalid_steps','active_steps','bilateral_steps','stall_steps','acc_valid_steps','releases','action_saturated_steps','drive_saturated_steps'):old[k]+=s[k]
        for k,v in s['joint_histograms'].items():old['joint_histograms'][k]=(np.asarray(old['joint_histograms'][k])+v).tolist()
        old['missing_diagnostics']=sorted(set(old['missing_diagnostics'])|set(s['missing_diagnostics']))
        return s
    def report(self,replay_audit=None,formal=False):
        deficits=[]; groups=[]; t=self.thresholds
        expected=self.spec.get('groups',[])
        if not expected: deficits.append({'kind':'missing_expected_group_manifest'})
        for group in expected:
            rows=[r for r in self.records if all(r.get(k)==v for k,v in group.items() if k in ('scene','config_id','fixed_side'))]
            counts={}; processes={};
            for b in group.get('feasible_xi',range(10)):
                hits=sum(r['xi_episodes'][str(b)] for r in rows)
                count=sum(r['xi_steps'][str(b)] for r in rows)
                counts[str(b)]={'steps':count,'episodes':hits}
                entering=sum(r['entries'].get(b,r['entries'].get(str(b),0)) for r in rows)
                leaving=sum(r['exits'].get(b,r['exits'].get(str(b),0)) for r in rows)
                if not entering or not leaving: deficits.append({'kind':'xi_enter_exit','group':group,'bin':b,'enter':entering,'exit':leaving})
                if count<t['xi_steps'] or hits<t['xi_episodes']:
                    deficits.append({'kind':'conditional_xi','group':group,'bin':b,'steps':count,'episodes':hits})
            required=group.get('required_processes',['positive_motion','negative_motion','boundary_approach','boundary_departure','loaded_hold','load_release_recovery'])
            for name in required:
                value=sum(r['processes'].get(name,0) for r in rows); processes[name]=value
                if value<t['process_episodes']: deficits.append({'kind':'process','group':group,'process':name,'episodes':value})
            if group.get('scene')=='E4':
                for metric,threshold in [('active_steps','e4_contact_motion_fraction'),('bilateral_steps','e4_bilateral_fraction')]:
                    ratio=sum(r[metric] for r in rows)/max(1,sum(r['valid_steps'] for r in rows))
                    if ratio<t[threshold]: deficits.append({'kind':metric,'group':group,'fraction':ratio,'required':t[threshold]})
            groups.append({'group':group,'xi':counts,'processes':processes})
        for i,cross in enumerate(self.spec.get('cross_requirements',[])):
            hits=self.cross_counts[i]
            if hits<cross.get('episodes',2): deficits.append({'kind':'cross_combination','requirement':cross,'episodes':hits})
        if not self.spec.get('cross_requirements'): deficits.append({'kind':'missing_cross_combination_manifest'})
        for scene in self.spec.get('scene_weights',{}):
            for b in range(10):
                hits=sum(r['xi_episodes'][str(b)] for r in self.records if r['scene']==scene)
                if hits<t['cross_xi_episodes']: deficits.append({'kind':'scene_xi','scene':scene,'bin':b,'episodes':hits})
        for required in ('physics_contract_verified','rules_calibrated','noise_calibrated','cross_manifest_frozen'):
            if self.spec.get('evidence',{}).get(required) is not True: deficits.append({'kind':'missing_evidence','name':required})
        for r in self.records:
            if r['missing_diagnostics']: deficits.append({'kind':'missing_diagnostics','episode':r['episode_id'],'fields':r['missing_diagnostics']})
        invalid=sum(r['invalid_steps'] for r in self.records)
        if invalid: deficits.append({'kind':'invalid_physics_transitions','steps':invalid})
        total=sum(r['valid_steps'] for r in self.records)
        scene_steps={s:sum(r['valid_steps'] for r in self.records if r['scene']==s) for s in self.spec.get('scene_weights',{})}
        for s,w in self.spec.get('scene_weights',{}).items():
            ratio=scene_steps[s]/max(total,1)
            if abs(ratio-w)>t['scene_fraction_tolerance']: deficits.append({'kind':'scene_time_fraction','scene':s,'actual':ratio,'target':w})
        return plain({'version':'v3-coverage-1','spec_hash':self.spec_hash,'formal_requested':formal,
                'diagnostic_complete':True,'coverage_ready':bool(formal and not deficits),
                'validated':False,'valid_steps':total,'invalid_steps':invalid,'scene_steps':scene_steps,
                'conditional_groups':groups,'deficits':deficits,'group_aggregates':self.records,'episode_count':self.total_episodes,'gradient_usage':replay_audit or {},
                'closed_chain_weld_covered':False})
    def write(self,path,replay_audit=None,formal=False):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); report=self.report(replay_audit,formal)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        path.with_suffix('.html').write_text('<!doctype html> <Meta charset="utf-8">title>V3 cover <h1>V3 <h1>'+html.escape(json.dumps(report,ensure_ascii=False,indent=2))+'</pre>',encoding='utf8')
        return report
    def state_dict(self): return {'spec_hash':self.spec_hash,'records':self.records,'cross_counts':dict(self.cross_counts),'total_episodes':self.total_episodes}
    def load_state_dict(self,s):
        if s['spec_hash']!=self.spec_hash: raise ValueError('coverage thresholds changed')
        self.records=s['records'];self.cross_counts=Counter(s['cross_counts']);self.total_episodes=s['total_episodes']
