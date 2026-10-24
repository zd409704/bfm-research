"""CPU/disk episode replay; the row sampler is also the definition of rho."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter, defaultdict, OrderedDict
import gzip
import hashlib
import json
from functools import lru_cache
import numpy as np
from . import VERSION

RHO_VERSION = 'v3-current-source-scene-config-key-bin-transition-2-strict-config'
SCENES = {'E0': .20, 'E1': .15, 'E2': .20, 'E3': .15, 'E4': .30}
FAMILIES = {'xi': .4, 'dq': .2, 'tau': .2, 'phase': .2}

def plain(value):
    if isinstance(value, np.ndarray): return value.tolist()
    if isinstance(value, np.generic): return value.item()
    if isinstance(value, Path): return str(value)
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    return value

def fingerprint(value):
    return hashlib.sha256(json.dumps(plain(value), sort_keys=True, allow_nan=False).encode()).hexdigest()

ARCHIVE_VERSION='v3-compressed-episode-2'
CHUNK_ROWS=128
CACHE_BYTES=128*1024**2
_CHUNK_CACHE=OrderedDict()
_CACHE_SIZE=0

def file_hash(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def _chunk(path):
    global _CACHE_SIZE
    path=str(path)
    if path in _CHUNK_CACHE:
        value=_CHUNK_CACHE.pop(path); _CHUNK_CACHE[path]=value; return value
    with np.load(path,allow_pickle=False) as z: value={k:z[k] for k in z.files}
    size=sum(v.nbytes for v in value.values())
    while _CHUNK_CACHE and _CACHE_SIZE+size>CACHE_BYTES:
        _,old=_CHUNK_CACHE.popitem(last=False);_CACHE_SIZE-=sum(v.nbytes for v in old.values())
    if size<=CACHE_BYTES: _CHUNK_CACHE[path]=value; _CACHE_SIZE+=size
    return value

class ChunkArray:
    def __init__(self,path,name,shape,dtype):
        self.path=Path(path);self.name=name;self.shape=tuple(shape);self.dtype=np.dtype(dtype);self.ndim=len(shape)
    def __len__(self):return self.shape[0]
    def __getitem__(self,key):
        first,rest=(key[0],key[1:]) if isinstance(key,tuple) else (key,())
        if isinstance(first,(int,np.integer)):
            i=int(first)%len(self);data=_chunk(self.path/f'chunk_{i//CHUNK_ROWS:06d}.npz')
            if self.name=='p': row=np.r_[data['physics_p'][i%CHUNK_ROWS],data['memory'][i%CHUNK_ROWS]].astype(np.float32)
            else:row=data[self.name][i%CHUNK_ROWS]
            return row[rest] if rest else row
        indices=np.arange(len(self))[first]
        out=np.asarray([self[int(i)] for i in np.atleast_1d(indices)])
        return out[(slice(None),)+rest] if rest else out
    def __array__(self,dtype=None):return np.asarray(self[:],dtype=dtype)

@lru_cache(maxsize=2)
def _records(path):
    with gzip.open(Path(path)/'records.json.gz','rt',encoding='utf8') as f:return json.load(f)

class DiskRecords:
    def __init__(self,path,key,length):self.path=Path(path);self.key=key;self.length=length
    def __len__(self):return self.length
    def __getitem__(self,index):
        if isinstance(index,slice):return [self[i] for i in range(*index.indices(self.length))]
        i=int(index)%self.length;data=_records(str(self.path))
        chunk=_chunk(self.path/f'chunk_{i//CHUNK_ROWS:06d}.npz');j=i%CHUNK_ROWS
        if self.key=='raw':
            r=dict(data['raw'][i]);r['p']=chunk['physics_p'][j].copy();return r
        result={k:np.asarray(v).copy() for k,v in data['known_constants'].items()}
        result.update({k[6:]:v[j].copy() for k,v in chunk.items() if k.startswith('known_')})
        return result
    def __iter__(self):return (self[i] for i in range(self.length))

@dataclass
class Episode:
    episode_id: str
    source: str
    scene: str
    config_id: str
    x: np.ndarray
    g: np.ndarray
    p: np.ndarray
    u: np.ndarray
    discount: np.ndarray
    phase: np.ndarray
    raw: list
    known: list
    metadata: dict = field(default_factory=dict)
    valid: np.ndarray | None = None
    bins: dict = field(default_factory=dict)
    path: Path | None = None

    def __len__(self): return len(self.u)

    @property
    def structure(self):
        if hasattr(self,'_structure'): return self._structure
        k = self.known[0]
        return fingerprint({'lengths': k['lengths'], 'limits': k['limits'],
                            'geometry_family': self.metadata.get('geometry_family', 'straight_planar')})

    def validate(self):
        n = len(self)
        if not n or self.source not in ('rule', 'policy') or self.scene not in SCENES:
            raise ValueError('invalid/empty episode or source/scene')
        for name, shape in [('x', (n+1, 137)), ('g', (n+1, 13)), ('u', (n, 1)), ('discount', (n, 1))]:
            a = np.asarray(getattr(self, name))
            if a.shape != shape or not np.isfinite(a).all(): raise ValueError(f'{name}: invalid shape/value')
        if self.p.ndim != 2 or len(self.p) != n+1 or not np.isfinite(self.p).all():
            raise ValueError('p must be finite, fixed dimension, T+1 boundaries')
        if len(self.raw) != n+1 or len(self.known) != n+1 or len(self.phase) != n:
            raise ValueError('full raw/known/phase sequence required')
        if not self.raw[-1].get('terminated', False) and not self.raw[-1].get('truncated', False):
            raise ValueError('only complete episodes accepted')
        if any('valid' not in r for r in self.raw): raise ValueError('explicit raw validity required')
        allowed=np.array([bool(a['valid'] and b['valid'] and b.get('interval_valid',False)) for a,b in zip(self.raw,self.raw[1:])])
        if self.valid is None: self.valid=allowed
        if np.asarray(self.valid).shape != (n,) or np.asarray(self.valid).dtype != np.bool_: raise ValueError('boolean valid [T] required')
        if np.any(self.valid & ~allowed): raise ValueError('valid mask admits invalid raw transition')
        for i,b in enumerate(self.raw[1:]):
            if not np.isclose(self.u[i,0],b['u_previous'],atol=1e-6): raise ValueError('stored action/next request mismatch')
        if np.any(np.abs(self.u) > 1.000001): raise ValueError('u is canonical request/S, bounded [-1,1]')
        for i, b in enumerate(self.raw[1:]):
            if b.get('terminated') and self.discount[i,0] != 0: raise ValueError('terminal bootstraps')
            if b.get('truncated') and not b.get('terminated') and self.discount[i,0] <= 0:
                raise ValueError('truncation must bootstrap')
        self.bins = self.make_bins()
        return self

    def make_bins(self):
        q = np.asarray([r['q'] for r in self.raw[:-1]])
        dq = np.asarray([r['dq'] for r in self.raw[:-1]])
        tau = np.asarray([r['tau_endpoint'] for r in self.raw[:-1]])
        limits = np.asarray([k['limits'] for k in self.known[:-1]])
        drive = np.asarray([k['drive'] for k in self.known[:-1]])
        capacity = np.where(tau < 0, np.abs(drive[:,1]), np.abs(drive[:,2]))
        if np.any(capacity <= 0): raise ValueError('positive declared directional capacity required')
        xi = (q-limits[:,0])/(limits[:,1]-limits[:,0])
        return {'xi': np.clip(np.floor(xi*10),0,9).astype(int),
                'dq': np.digitize(dq, [-4,-2,-.5,.5,2,4]),
                'tau': np.digitize(tau/capacity, [-.8,-.2,.2,.8]),
                'phase': np.asarray(self.phase, dtype=str)}

    def save(self, root):
        root=Path(root)
        if not self.episode_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in self.episode_id):raise ValueError('unsafe episode id')
        self.validate();dest=root/self.source/self.episode_id;dest.mkdir(parents=True,exist_ok=False)
        pdim=len(self.raw[0]['p']);raw=[{k:v for k,v in r.items() if k!='p'} for r in self.raw]
        arrays={'x':np.asarray(self.x,dtype=np.float32),'g':np.asarray(self.g,dtype=np.float32),
                'physics_p':np.asarray([r['p'] for r in self.raw],dtype=np.float64),
                'memory':np.asarray(self.p[:,pdim:],dtype=np.float32)}
        constants={}
        for k in self.known[0]:
            a=np.asarray([v[k] for v in self.known])
            if np.array_equal(a,np.broadcast_to(a[0],a.shape)):constants[k]=a[0]
            else:arrays['known_'+k]=a
        for start in range(0,len(self)+1,CHUNK_ROWS):
            np.savez_compressed(dest/f'chunk_{start//CHUNK_ROWS:06d}.npz',**{k:v[start:start+CHUNK_ROWS] for k,v in arrays.items()})
        # Small compact index is loaded once, never requires decoding p or raw.
        goal_ids=np.flatnonzero((np.asarray(self.g)[:,12]>.5)&np.asarray([r['valid'] for r in self.raw])).astype(np.int32)
        np.savez_compressed(dest/'index.npz',u=self.u,discount=self.discount,phase=self.phase,valid=self.valid,
                            goal_ids=goal_ids,**{'bin_'+k:v for k,v in self.bins.items()})
        payload={'raw':raw,'known_constants':constants,'behaviour':self.metadata.get('behaviour',[])}
        with gzip.open(dest/'records.json.gz','wt',encoding='utf8',compresslevel=6) as f:json.dump(plain(payload),f,allow_nan=False,separators=(',',':'))
        meta={k:v for k,v in self.metadata.items() if k!='behaviour'}
        header={'version':VERSION,'archive_version':ARCHIVE_VERSION,'episode_id':self.episode_id,'source':self.source,'scene':self.scene,
                'config_id':self.config_id,'metadata':meta,'n':len(self),'p_dim':self.p.shape[1],'physics_dim':pdim,
                'structure':self.structure,'last_boundary_valid':bool(self.raw[-1]['valid'])}
        (dest/'header.json').write_text(json.dumps(plain(header),separators=(',',':')))
        hashes={f.name:file_hash(f) for f in sorted(dest.iterdir())}
        (dest/'integrity.json').write_text(json.dumps(hashes,sort_keys=True));self.path=dest
        return dest

    @classmethod
    def load(cls,path):
        path=Path(path);d=json.loads((path/'header.json').read_text())
        if d.pop('version')!=VERSION or d.pop('archive_version')!=ARCHIVE_VERSION:raise ValueError('V3 compressed archive version required; no legacy reinterpretation')
        n=d.pop('n');pdim=d.pop('p_dim');d.pop('physics_dim');structure=d.pop('structure');last=d.pop('last_boundary_valid')
        with np.load(path/'index.npz',allow_pickle=False) as z:idx={k:z[k] for k in z.files}
        arrays={k:ChunkArray(path,k,(n+1,width),np.float32) for k,width in [('x',137),('g',13),('p',pdim)]}
        ep=cls(**d,**arrays,**{k:idx[k] for k in ('u','discount','phase','valid')},
               raw=DiskRecords(path,'raw',n+1),known=DiskRecords(path,'known',n+1),path=path)
        ep.bins={k:idx['bin_'+k] for k in FAMILIES};ep._goal_ids=idx['goal_ids'];ep._structure=structure;ep._last_boundary_valid=last
        return ep

    def behaviour(self):
        return self.metadata.get('behaviour',_records(str(self.path))['behaviour'] if self.path else [])

    def reconstruct(self):
        from .features import FeatureHistory
        h=FeatureHistory(); out=[]
        for i,(r,k) in enumerate(zip(self.raw,self.known)):
            if i==0: h.reset(r,k)
            else: h.append(r,k)
            f=h.features(); out.append((f['x'],f['g'],np.concatenate([np.asarray(r['p']),f['memory']])))
        return {name:np.asarray([a[j] for a in out]) for j,name in enumerate(('x','g','p'))}

class EmptyReplayGroup(RuntimeError): pass

class SlotTags:
    """Fixed numeric slot table; interned strings live only while slots reference them."""
    def __init__(self,capacity):
        self.values=np.zeros((capacity,8),dtype=np.int64);self.tables=[{} for _ in range(7)];self.reverse=[{} for _ in range(7)];self.refs=[Counter() for _ in range(7)];self.serial=[0]*7
        self.occupied=set()
    def __setitem__(self,slot,tag):
        group,keys,structure,goal,eid,t=tag;items=[tuple(group)]+[keys[f] for f in FAMILIES]+[structure,eid]
        for j,value in enumerate(items):
            if value not in self.tables[j]:
                self.serial[j]+=1;self.tables[j][value]=self.serial[j];self.reverse[j][self.serial[j]]=value
            code=self.tables[j][value];self.refs[j][code]+=1;self.values[slot,j]=code
        self.values[slot,7]=int(t)*2+int(goal);self.occupied.add(int(slot))
    def __getitem__(self,slot):
        row=self.values[slot];items=[self.reverse[j][int(row[j])] for j in range(7)]
        return (items[0],dict(zip(FAMILIES,items[1:5])),items[5],bool(row[7]%2),items[6],int(row[7]//2))
    def pop(self,slot):
        out=self[slot]
        for j,code in enumerate(self.values[slot,:7]):
            code=int(code);self.refs[j][code]-=1
            if self.refs[j][code]==0:
                value=self.reverse[j].pop(code);del self.tables[j][value];del self.refs[j][code]
        self.occupied.remove(int(slot));return out
    def items(self):return ((slot,self[slot]) for slot in sorted(self.occupied))

class CompactBucket:
    def __init__(self,positions):
        from array import array
        self.slots=array('I');self.positions=positions
    def add(self,slot):self.positions[slot]=len(self.slots);self.slots.append(slot)
    def remove(self,slot):
        at=int(self.positions[slot]);last=self.slots.pop()
        if at<len(self.slots):self.slots[at]=last;self.positions[last]=at
    def __len__(self):return len(self.slots)
    def draw(self,rng):return int(self.slots[int(rng.integers(len(self.slots)))])

class Replay:
    """Fixed-capacity RAM transitions. No disk access on add/sample/checkpoint restore.

    raw/known/behaviour are not retained. p current/next include feature memory.
    """
    def __init__(self,root=None,seed=0,scene_weights=None,expected_configs=None,
                 policy_capacity=65536,rule_capacity=32768,max_episode_steps=1000,
                 min_group_episodes=2,strict=False,rule_extra_per_group=32,p_dim=None,
                 memory_limit_bytes=4*1024**3,p0_fraction=.5):
        self.root=Path(root) if root is not None else None
        self.rng=np.random.default_rng(seed);self.scene_weights=dict(scene_weights or SCENES)
        self.expected_configs=expected_configs or {};self.strict=strict
        self.capacities={'rule':int(rule_capacity),'policy':int(policy_capacity)}
        if min(self.capacities.values())<1:raise ValueError('positive fixed replay capacities required')
        self.capacity=sum(self.capacities.values());self.memory_limit_bytes=memory_limit_bytes
        self.instance_id=__import__('uuid').uuid4().hex;self.p_dim=None;self.arrays={};self.active=np.zeros(self.capacity,dtype=bool);self.p0_mask=np.zeros(self.capacity,dtype=bool)
        self.next_slot={'rule':0,'policy':self.capacities['rule']};self.counts=Counter()
        self.tags=SlotTags(self.capacity);self.positions=np.zeros((5,self.capacity),dtype=np.int32);self.groups={};self.goals={};self.audit=Counter();self.revision=0;self._dist=None
        self.p0_fraction=float(p0_fraction)
        if not 0<self.p0_fraction<1:raise ValueError('P0 fraction must reserve both anchor and rolling rule slots')
        self.max_episode_steps=max_episode_steps;self.p0_capacity=int(self.capacities['rule']*self.p0_fraction);self.p0_cursor=0;self.rule_cursor=self.p0_capacity;self.p0_seen=Counter()
        self.p0_groups=[(s,c) for s in self.scene_weights for c in self.expected_configs.get(s,[])]
        self.p0_retention_mode=('stratified_reservoir' if self.p0_groups and len(self.p0_groups)<=self.p0_capacity else 'global_reservoir')
        self.p0_retention_reason=('configured_groups_fit' if self.p0_retention_mode=='stratified_reservoir' else ('capacity_below_expected_groups' if self.p0_groups else 'expected_configs_unspecified'))
        self.p0_global_seen=0
        if p_dim is not None:self._allocate(p_dim)
    def _allocate(self,pdim):
        # Conservative index overhead includes Python dict/int bookkeeping.
        estimate=self.capacity*(4*(2*137+2*pdim+13+2)+512)+2*512*4*(2*137+2*pdim+13+2)
        if estimate>self.memory_limit_bytes:raise MemoryError(f'Replay upper estimate {estimate} exceeds {self.memory_limit_bytes}; lower capacities explicitly')
        self.p_dim=int(pdim)
        dims={'x':137,'p':pdim,'u':1,'x_next':137,'p_next':pdim,'g_next':13,'discount':1}
        self.arrays={k:np.zeros((self.capacity,d),dtype=np.float32) for k,d in dims.items()}
        self.estimated_max_bytes=estimate
    def __len__(self):return int(self.active.sum())
    def _erase(self,slot):
        group,keys,structure,goal_valid,eid,t=self.tags.pop(slot)
        for family,b in keys.items():
            bucket=self.groups[group][family][b];bucket.remove(slot)
            if not len(bucket):del self.groups[group][family][b]
        if not self.groups[group]['xi']:del self.groups[group]
        if goal_valid:
            self.goals[structure].remove(slot)
            if not len(self.goals[structure]):del self.goals[structure]
        self.counts[group[0]]-=1;self.audit['evicted_'+group[0]]+=1
    def add(self,ep,p0=False):
        ep.validate()
        if self.p_dim is None:self._allocate(ep.p.shape[1])
        if ep.p.shape[1]!=self.p_dim:raise ValueError('p schema dimension changed')
        start=0 if ep.source=='rule' else self.capacities['rule'];cap=self.capacities[ep.source]
        group=(ep.source,ep.scene,ep.config_id);structure=ep.structure
        for t in range(len(ep)):
            if not ep.valid[t]:self.audit['invalid_isolated']+=1;continue
            if ep.source=='rule':
                if p0:
                    if self.p0_retention_mode=='stratified_reservoir':
                        if (ep.scene,ep.config_id) not in self.p0_groups:raise ValueError('P0 config outside declared expected groups')
                        group_number=self.p0_groups.index((ep.scene,ep.config_id))
                        base,remainder=divmod(self.p0_capacity,len(self.p0_groups))
                        size=base+int(group_number<remainder)
                        offset=group_number*base+min(group_number,remainder)
                        self.p0_seen[group]+=1;seen=self.p0_seen[group]
                    else:
                        offset=0;size=self.p0_capacity;self.p0_global_seen+=1;seen=self.p0_global_seen
                    pick=seen-1 if seen<=size else int(self.rng.integers(seen))
                    if pick>=size:
                        self.audit['p0_reservoir_not_retained']+=1;continue
                    slot=offset+pick
                else:
                    slot=self.rule_cursor
                    self.rule_cursor=self.p0_capacity+(self.rule_cursor-self.p0_capacity+1)%max(1,cap-self.p0_capacity)
            else:slot=self.next_slot[ep.source]
            if self.active[slot]:self._erase(slot)
            values={'x':ep.x[t],'p':ep.p[t],'u':ep.u[t],'x_next':ep.x[t+1],'p_next':ep.p[t+1],'g_next':ep.g[t+1],'discount':ep.discount[t]}
            for k,v in values.items():self.arrays[k][slot]=v
            keys={f:str(ep.bins[f][t]) for f in FAMILIES};valid_goal=bool(ep.g[t+1,12]>.5)
            self.tags[slot]=(group,keys,structure,valid_goal,ep.episode_id,t)
            families=self.groups.setdefault(group,{f:{} for f in FAMILIES})
            for f,b in keys.items():families[f].setdefault(b,CompactBucket(self.positions[list(FAMILIES).index(f)])).add(slot)
            if valid_goal:self.goals.setdefault(structure,CompactBucket(self.positions[4])).add(slot)
            self.active[slot]=True;self.p0_mask[slot]=p0;self.counts[ep.source]+=1
            self.next_slot[ep.source]=start+(slot-start+1)%cap
            self.audit['added_'+ep.source]+=1
            if p0:self.audit['p0_added']+=1
        self.revision+=1;self._dist=None
        return ep
    def distribution(self):
        if self._dist is not None:
            if self.strict and self._dist['empty_groups']:raise EmptyReplayGroup('cached distribution missing expected groups')
            return self._dist
        available={s:{} for s in ('rule','policy')};empty=[];empty_bins=[]
        for source in available:
            for scene in self.scene_weights:
                configs=sorted(k[2] for k in self.groups if k[:2]==(source,scene))
                if configs:available[source][scene]=configs
                else:empty.append([source,scene,'ALL'])
                for cid in self.expected_configs.get(scene,[]):
                    if cid not in configs:empty.append([source,scene,cid])
        if self.strict and empty:raise EmptyReplayGroup(f'expected source/scene/config missing: {empty}')
        sources=[s for s in available if available[s]]
        if not sources:raise EmptyReplayGroup('no valid transitions')
        for key,families in self.groups.items():
            for f,n in [('xi',10),('dq',7),('tau',5)]:
                missing=[i for i in range(n) if str(i) not in families[f]]
                if missing:empty_bins.append({'group':key,'family':f,'missing':missing})
        self._dist={'version':RHO_VERSION,'instance_id':self.instance_id,'revision':self.revision,'available':available,'sources':sources,
                    'empty_groups':empty,'empty_bins':empty_bins,'formal':bool(self.strict and not empty),
                    'full_expected_groups':not empty,'distribution_status':'complete' if not empty else 'partial',
                    'fallback':bool(empty),'source_weights':{s:1/len(sources) for s in sources},'scene_weights':self.scene_weights,'family_weights':FAMILIES,
                    'effective_scene_weights':{src:{sc:self.scene_weights[sc]/sum(self.scene_weights[v] for v in available[src]) for sc in available[src]} for src in sources}}
        return self._dist
    def _draw(self,n):
        d=self.distribution();slots=[];prob=[];paths=[]
        for _ in range(n):
            source=str(self.rng.choice(d['sources']));scenes=list(d['available'][source]);w=np.array([self.scene_weights[s] for s in scenes]);w/=w.sum()
            j=int(self.rng.choice(len(scenes),p=w));scene=scenes[j];configs=d['available'][source][scene];cid=str(self.rng.choice(configs))
            families=self.groups[(source,scene,cid)];f=str(self.rng.choice(list(FAMILIES),p=list(FAMILIES.values())));b=str(self.rng.choice(list(families[f])))
            slot=families[f][b].draw(self.rng);keys=self.tags[slot][1]
            probability=sum(weight/len(families[family])/len(families[family][keys[family]]) for family,weight in FAMILIES.items())/len(d['sources'])*w[j]/len(configs)
            slots.append(slot);prob.append(probability);paths.append((source,scene,cid,f,b))
        return np.asarray(slots),np.asarray(prob),paths,d
    def matching_goal(self,known,rng,geometry_family='straight_planar'):
        structure=fingerprint({'lengths':known['lengths'],'limits':known['limits'],'geometry_family':geometry_family})
        bucket=self.goals.get(structure)
        return None if bucket is None else self.arrays['g_next'][bucket.draw(rng)].copy()
    def sample(self,n,device='cpu'):
        import torch
        slots,prob,paths,d=self._draw(n);out={k:torch.as_tensor(v[slots].copy(),device=device) for k,v in self.arrays.items()}
        goals=np.zeros((n,13),np.float32);valid=np.zeros(n,bool);ids=[]
        for i,slot in enumerate(slots):
            group,keys,structure,_,eid,t=self.tags[int(slot)];bucket=self.goals.get(structure)
            if bucket is not None:goals[i]=self.arrays['g_next'][bucket.draw(self.rng)];valid[i]=True
            else:self.audit['goal_random_fallback']+=1
            self.audit['gradient_'+group[0]+'_'+group[1]]+=1;ids.append((eid,t))
        out.update(goal_g=torch.as_tensor(goals,device=device),goal_valid=torch.as_tensor(valid,device=device),
                   audit={'ids':ids,'probability':prob,'paths':paths,'rho':d})
        return out
    def reference(self,n):
        slots,prob,_,d=self._draw(n)
        return {'g':self.arrays['g_next'][slots].copy(),'probability':prob,'ids':[(self.tags[int(s)][4],self.tags[int(s)][5]) for s in slots],'rho':d}
    def memory_report(self):
        return {'capacity':self.capacity,'active':len(self),'source_active':dict(self.counts),'p0_retained':int(np.sum(self.active & self.p0_mask)),'p0_retention_mode':self.p0_retention_mode,'p0_retention_reason':self.p0_retention_reason,'tensor_bytes':sum(a.nbytes for a in self.arrays.values()),
                'estimated_max_bytes':getattr(self,'estimated_max_bytes',0),'limit_bytes':self.memory_limit_bytes,'raw_resident':0,'disk_sampling':False}
    def state_dict(self):
        """Caller pauses replay writes until synchronous checkpoint serialization ends.

        Full buffers share tensor storage; partial buffers gather only active rows.
        A torch slice over partial backing storage would serialize unused rows too.
        """
        slots=np.flatnonzero(self.active)
        arrays={k:__import__('torch').from_numpy(v if len(slots)==self.capacity else v[slots]) for k,v in self.arrays.items()}
        return {'version':VERSION,'storage_version':'bounded-ram-5-active-p0-remainder','instance_id':self.instance_id,'rho_version':RHO_VERSION,'p_dim':self.p_dim,
                'config':{'scene_weights':self.scene_weights,'expected_configs':self.expected_configs,'policy_capacity':self.capacities['policy'],'rule_capacity':self.capacities['rule'],
                          'strict':self.strict,'memory_limit_bytes':self.memory_limit_bytes,'p0_fraction':self.p0_fraction},'p0_global_seen':self.p0_global_seen,'p0_seen':dict(self.p0_seen),'slots':slots,'p0_mask':self.p0_mask,'p0_cursor':self.p0_cursor,'rule_cursor':self.rule_cursor,'arrays':arrays,
                'bucket_order':{g:{f:{b:list(v.slots) for b,v in bins.items()} for f,bins in fs.items()} for g,fs in self.groups.items()},
                'goal_order':{g:list(v.slots) for g,v in self.goals.items()},
                'tags':{int(k):v for k,v in self.tags.items()},'next_slot':self.next_slot.copy(),'rng':self.rng.bit_generator.state,'audit':dict(self.audit),'revision':self.revision}
    def load_state_dict(self,s):
        """Consume s['arrays'] one field at a time; no second preallocated full replay."""
        if s.get('version')!=VERSION or s.get('storage_version')!='bounded-ram-5-active-p0-remainder' or s.get('rho_version')!=RHO_VERSION:raise ValueError('incompatible RAM checkpoint')
        self.__init__(self.root,**s['config']);self.p_dim=s['p_dim']
        self.estimated_max_bytes=self.capacity*(4*(2*137+2*self.p_dim+13+2)+512)+2*512*4*(2*137+2*self.p_dim+13+2)
        if self.estimated_max_bytes>self.memory_limit_bytes:raise MemoryError('restored replay exceeds budget')
        slots=np.asarray(s['slots'],dtype=np.int64)
        if len(np.unique(slots))!=len(slots) or np.any(slots<0) or np.any(slots>=self.capacity):raise ValueError('invalid checkpoint active slots')
        full=len(slots)==self.capacity and np.array_equal(slots,np.arange(self.capacity))
        for key in list(s['arrays']):
            tensor=s['arrays'].pop(key)
            compact=tensor.numpy() if hasattr(tensor,'numpy') else tensor
            if compact.shape[0]!=len(slots):raise ValueError('checkpoint tensor row/slot mismatch')
            if full:self.arrays[key]=compact
            else:
                array=np.zeros((self.capacity,compact.shape[1]),dtype=np.float32)
                array[slots]=compact;self.arrays[key]=array
            del tensor,compact

        for slot,tag in s['tags'].items():
            slot=int(slot);group,keys,structure,goal,eid,t=tag;group=tuple(group);self.tags[slot]=(group,keys,structure,goal,eid,t)
            self.active[slot]=True;self.counts[group[0]]+=1
            families=self.groups.setdefault(group,{f:{} for f in FAMILIES})
            for f,b in keys.items():families[f].setdefault(b,CompactBucket(self.positions[list(FAMILIES).index(f)])).add(slot)
            if goal:self.goals.setdefault(structure,CompactBucket(self.positions[4])).add(slot)
        self.p0_global_seen=s['p0_global_seen'];self.p0_seen=Counter(s['p0_seen']);self.p0_mask=s['p0_mask'];self.p0_cursor=s['p0_cursor'];self.rule_cursor=s['rule_cursor'];self.instance_id=s['instance_id'];self.next_slot=dict(s['next_slot']);self.rng.bit_generator.state=s['rng'];self.audit=Counter(s['audit']);self.revision=s['revision']
        # Persist bucket order: swap/pop eviction changes it and exact RNG resume needs it.
        if 'bucket_order' in s:
            self.groups={group:{f:{} for f in FAMILIES} for group in s['bucket_order']}
            for group,families in s['bucket_order'].items():
                for f,bins in families.items():
                    for b,order in bins.items():
                        bucket=CompactBucket(self.positions[list(FAMILIES).index(f)])
                        for slot in order:bucket.add(slot)
                        self.groups[group][f][b]=bucket
        if 'goal_order' in s:
            for structure,order in s['goal_order'].items():
                bucket=CompactBucket(self.positions[4])
                for slot in order:bucket.add(slot)
                self.goals[structure]=bucket


def storage_report(root,transitions,total_W=20_000_000,reserve_bytes=5*1024**3):
    import shutil
    root=Path(root);files=[p for p in root.rglob('*') if p.is_file()]
    size=sum(p.stat().st_size for p in files);rate=size/max(1,transitions)
    free=shutil.disk_usage(root).free;estimate=int(rate*total_W*1.3)+reserve_bytes
    return {'archive_version':ARCHIVE_VERSION,'measured_bytes':size,'measured_transitions':transitions,
            'bytes_per_transition':rate,'projected_total_W':total_W,'projected_bytes_with_30pct_margin':estimate,
            'disk_free_bytes':free,'space_ready':estimate<=free,'cache_limit_bytes':CACHE_BYTES,
            'chunk_rows':CHUNK_ROWS,'physics_p_stored_once':True,'all_failures_preserved':True,
            'compression':'numpy zip deflate lossless; raw physics float64; features float32'}
