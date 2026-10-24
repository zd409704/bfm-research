# v3-core read-only cross-audit

Review time: 2026-10-10 08:34–08:44 UTC. The object is code under concurrent development, not a frozen release version. No code, configuration, test or physical files were changed in this round, only this report was written; no GPU was used, dependencies were installed, training, sub-agents were created, or outgoing messages were not used. CPU tests are all run through stdin, `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`; only the in-process environment status is modified, and there is no disk replay/weight product.

The first round of the pre-order core has been accepted by the main window; this file does not exist at the beginning, and the previous queue tasks that have not been placed are not repeated. Read the current coordination API, three design documents, physics/pipeline handoff and development acceptance records. The overview of earlier issues in the record is for deduplication only and the following evidence is an independent check.

## Review version and evidence scope

The hashes before and after the last set of physical renditions are the same (around 08:41). The file paths are all in `unit_bfm/v3/`:

| File | SHA256 |
|---|---|
| physics.py | `387d12546a6c25175fda4624566ae5746752c92d484478dbd018a1a9183bd588` |
| privileged.py | `e33a207bd9afebeba7abd0668019ce53ebe948296876b4f22c6448ee8c68af57` |
| mechanics.py | `94120a2c7184419267a909bde08f64d7e59082d56ddb74f945c6008f12abab79` |
| randomization.py | `271080e297c9bf1a6c27665bf3f1540d41146df19488a71093903020ff826880` |
| train.py | `859c49b9f6553fba1aef1372e7f9caa67b0ed0273ce70cf527052fb638480d0b` |
| replay.py | `af92b3d4ab364bf82d806b9c07c9cbcda06c08aec464ecc27c19bd0e2c9bea2e` |
| coverage.py (auxiliary) | `0214e7df1caeabe1e5059f0feda2080292b50e266a883e0eaa89a8f4eaa2c23b` |
| collect.py (secondary) | `1a90b3c4b0b59df5c6a3cabb68c9b20dec6e38f1ffa39bf5e827b66e483ffe09` |

Physics p has been expanded from 3176 to 4534 during review; the old dimensions will not be used for conclusions. The following P1 refers to repairs that should be made before formal collection/training, and P2 refers to interface integrity, coverage, or continued operation risks. There is no announcement that GPU/full physics balancing/full training passed.

Immediate issues

### P1-1: E1/E4 reset does not provide actual support stiffness/damping to F, the complete y is the same but has different successors

Position: `if self._solve` support block of `physics.UnitEnv._privileged`; `privileged._schema` support mask.

The support already exists, the first step must take effect, but when reset `_solve=None`, the support block is set to zero and present = 0. Added process.support with motion/frequency/preload and still no k/damping. The other parameters of the two sets of E1 are the same, change `support_k`, and the x, p, and memory of the reset are exactly the same; the same u = .1, the next dq difference * * 0.011423285907458502 rad/s * *. This is not a counterexample of arbitrary abstract compression, but a practical counterexample of two production environments. The boundary feature_memory cannot make up for missing real parameters.

Specific modification: Separate the support entity existence bit, actual parameters/connection side, current reference generator status and force solution valid bit. Parameters/entities present are exported at reset; only the previous interval force has solve_valid=0. Similarly, check the reset object servo/loader current parameters. Don't code "Supreme Beat Power" as "Unsupported" before solving it. To rerun the same pair, reset p is required to have different actual effective parameters.

# # P1-2: F lacks the distance of the ground relative to M, and the geometry constant cannot replace the current boundary geometry

Position: `mechanics.build_xml` floor; `physics._privileged` body/state/geometry; `privileged._schema` No floor→M current transformation.

In E2, all the moving bodies and anchor points are translated along the world z by .2 m, maintaining the same relative configuration/speed, and the current p difference is only * * 2.78 e − 17 * *. Give the near and far ground states the same downward velocity, action 0: the next contact number is * * 1 vs 0 * *, and the M origin vertical velocity * * − 0.06267789095661687 vs − 1.098100000000001 m/s * *. The geometry.floor in the code is a fixed local parameter of the world body; the network did not receive the transformation of the world body relative to M, so the distance information cannot be obtained. The gravity projection does not contain translation. The current contact only exports the solved contact that has occurred, and cannot predict the distance when it has not yet been contacted.

Experiment with in-process legal qpos/qvel shifts to construct contactless boundaries, not the current default reset distribution; prove that the input contract does not contain this physical state, and do not claim that the default training has accessed this pair of states.

Specific modification method: export the current M system geometry for each external static object/plane; the ground must have at least the M system unit normal, signed plane offset/closest distance and existence position. The dynamic object provides a relative reference to the active servo and the current process status. Absolute world coordinates must not be leaked directly to the Actor; these fields are F only.

# # P1-3: Numeric invalidation, physical termination and solving valid bits are still obfuscated

Location: `physics._boundary`, `_privileged clock.solve_valid`, `_snapshot_solve`.

The latest version has added MuJoCo warning and penetration check, which is progress; but `terminated=not valid` still marks the value failure as a physical terminal. Inject `mjWARN_BADQACC` and output `(valid,terminated,clock.solve_valid)=(False,True,1)`; clear warning, set the saved solution `qacc` to NaN and output **(True,False,1)**. This is a fault injection verification check path that does not claim that regular traces naturally generate NaNs. solve_valid currently only indicates that `_solve` exists and does not prove that the solution is valid; qacc/constraint is non-finite and solver convergence quality is not checked.

Specific modifications: qpos/qvel/qac/qfrc_constrain, export vernch, warning, capacity and containment diagnostics to aggregate the effectiveness of the entire 10-step range; Any substep failure immediately stops and isolates. `terminated` only terminates a physical mission; The value should be invalid by a separate error/invalid cut-off semantic, and the collector retains the diagnosis but does not give it normal Bellman rows. Distinguishing between snapshot_present and solve_valid; The invalidity of the solution should be clarified accordingly, and no precise truth could be declared.

##P2-4: Add a new layer reset that is currently not connected to the official train factory. Partial random dimensions still tied to structure

Locations: `randomization.make_scene`, `SceneConfig.reset_mode`, `physics.reset`, `train._scene`.

The concurrent version has implemented `reset_mode='stratified'`, but is still configured by default, and the `train._scene`/full configuration is not enabled. The fixed structure of 12 consecutive factory-configured `(initial_q,initial_fraction,initial_dq)` still only has **(0,None,0)**; the actual training cannot claim that the reset ξ/dq mixing is completed because of the optional API.

Currently tilt=`geometry_id%8`, encoder_sign=`geometry_id%2`, load_side=`geometry_id%2`, load_frame=`limit_id%2` are still bound; changing episode_seed does not change these items. The same geometry/limit does not cover positive and negative encoders, installation sectors and loading on both sides. load_start=.2/load_end=1.7 Also fixed, regular multi-segment load/resume tags do not change the true force clock. The newly added support/adjacency/object parameter randomization has been truly changed and no longer reports "all are still constants".

Specific repair method: The pipeline clearly selects and records the reset mixture, and makes up the outstanding amount after physical threshold screening;  independently or explicitly cross-allocates the installation/calibration/loading side and process with  `(run_seed, structure, scenario, episode, purpose)` , and checks the joint coverage by structure. The excitation cannot be replaced by a relaxed coverage  threshold. The initial snapshot mixture still needs to be implemented/declared missing separately.

### P2-5: Replay.validate trusts the external valid array and may transfer explicit invalid raw into the gradient again

Location: `replay.Episode.validate`; `Replay._build` uses `e.valid`.

For a real short episode, `raw[3]['valid']=False`, `valid=np.ones(T,bool)`, and `validate()` are still successful; the adjacency transfer valid[2]/valid[3] are both True. This entry is also used for disk recovery, and shape verification is not equal to semantic verification. The current collector's automatically deduced normal path does not have this error and does not claim that it has generated this bad array.

Specific fixes: Each validate regenerates the allow mask from two original boundaries, interval_valid, and the necessary physical diagnostics; the caller passes the mask must be boolean, must not be wider than the allow mask, and can allow more strict isolation. Missing required valid should not default to true; check u and next.u_previous, discount and terminate/truncate the contract. Add this Fault Injection Rejection Test.

##P2-6:strict Replay still retreats from missing configuration, formal=true and fallback=true can appear at the same time

Position: strict branch of `Replay.distribution`.

Set `scene_weights={'E0':1}`, expected_configs={'E0':['present','missing']}; each of the two sources provides a present episode. `distribution()` returns `formal=True, fallback=True`, empty_groups contains two missing items, and no error is thrown. strict only checks if source/scene exists and does not check expected configuration.

Specific amendments: Freeze strict semantics. Formal distribution should reject missing required groups, or explicitly set up another distribution version that allows missing groups and report weight changes; you cannot nominally use full configuration distribution but actually only average the existing configuration. The existing train coverage gate may block some scenes in advance and cannot replace Replay's own strict contract.

### P2-7: Continuous training still involves the risk of large database reconstruction and P0 recovery granularity (static analysis, long tasks not run)

Location: `Replay.add/_build`, `train.run` P0 loop and coverage gate.

Each new episode makes the entire `_index=None`; next time sample/matching_goal_provider rebuilds multiple family and goal pools of the entire active library, and `_build` reads `raw[-1]` of each episode. Although raw has been cached in two episodes, scanning all episodes will still decompress the records JSON in sequence. When P0 transfers millions, this is the O (library size) overhead repeated in each round; the full throughput benchmark has not been done in this round, so exaggerated time figures cannot be given. There is no periodic checkpoint in the P0 cycle, and checkpoint('p0') is not performed until the end of the complete P0; exceptions can be saved at the boundary, but when the process/host is killed, the entire P0 collection progress has no recent recovery point.

Specific modification method: maintain incremental index according to source/scene/config; use goal/last boundary valid bit to persist in small index, and do not read the entire raw JSON for index building. P0 saves a complete episode boundary checkpoint per fixed number of physical steps; adds new capacity/IO budget and 100,000-level CPU storage benchmark. When the official coverage is insufficient, the current cycle will continue to consume the budget and clear credits. It is necessary to have durable underpayment collection and clear blocked reasons. You cannot just expand the budget and expect it to pass automatically.

# Retarded, changed or undiscovered (not listed as currently pending)

- * * Adjacency frequency missing fixed * *: 08:35 Legacy E3 is different from x/p next dq; re-run reset p-poor = .1899203478844882 after adding process.neighbour, this counterexample has been eliminated. It is no longer possible to take old evidence to report the frequency of shortage.
- **Fixed P/D static p mixed with the old counterexample has expired**: the old 3176 dimension is the same as x/p, the next dq=.1878154199 vs. .3322810032; p can be distinguished after adding geometry/joint/extra body. The tree symbol itself is correct in the independent endpoint geometry/velocity sample, no duplicate negative signs were found.
- **Support angle coordinates have been revised**: The target_angle of the old version of the M system is actually world .6; the latest minus the same solve M angle, the difference between reproduction and analysis is 0.
- **Replay resident raw memory problem has been alleviated**: The first version of short ep measured raw+known to be about 108100 bytes/boundary, and the simple expansion of P0 was about 290 GiB; the latest version of DiskRecords+LRU2 no longer takes this extrapolation as the current resident memory conclusion. There is still a risk of P2-7 scanning IO.
- * * Replay archive byte check has been added * *: the old hash only contains metadata/id/length/structure, the change u/p is still the same; the latest state adds archive_integrity and recovers the hash file, this old counterexample no longer constitutes the current defect. Due to the prohibition of new files, no additional tampering recovery tests have been performed in this round, and the label "code has been repaired, disk re-inspection is waiting for the main window".
- * * Source Fixed Side Binding fixed * *: Old global episode % 2 with 50/50 scheduler produces rule = P, policy = D; latest train uses independent assignment stream, old evidence is no longer a current issue.
- * * full Evidence switch false Still Start Long Acquisition Fixed * *: The latest run rejects unaccepted pre-evidence before building the catalog/acquisition. Coverage is not ready No longer use continue to skip cycle checkpoint.
- **coverage diagnostics field disconnection has been fixed**: the new fallback is extracted according to the registered field, the real short episode missing_diagnostics=[], and the old missing field problem is no longer reported.
- **No counterexample found in this round for actual force timing/reference point**: forward→rnePostConstraint→Snapshot→Euler; boundary t=.010, solve_time=.009 conforms to the semantics of the last completed substep. Contact frame transposition, geom1 forward, cfrc_int moves from root subtree COM to M origin formula is correct. The force only represents the last 1ms solution and does not pretend to be the 10ms integral mean; if continuous contact coverage is counted according to the 10ms endpoint, it cannot claim to have proven continuous force within the interval.
- **Actor knowsn isolation did not detect leaks from the current round**: same q/declaration, mass_error and drive_error=true, real Density/capacity multipliers of 8.81.1.2, konown Rigid gap of about 2e-15, drive-0; While COM/Iyy is read by simulation, it can be rebuilt in known quantities under the current rigid known geometry, planeq and unified density model, and should not be misreported for the mere reading of xipos. The addition of additional weights still requires the maintenance of a clear semantic “declaration geometry known”.
- **Transient syntax error not retained as release defect**: 08:36 read of extra closing bracket in randomization write, subsequently fixed. No changes were made to the documents and no duplicate reports were made.

## Reproducible CPU script

Execute the following two stdin scripts in the workspace; no files are created. First check the hash in the above table. If the version changes and re-record the value, the old conclusion cannot be applied mechanically.

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import numpy as np, mujoco
from dataclasses import replace
from unit_bfm.v3.physics import UnitEnv, make_scene
from unit_bfm.v3.features import FeatureHistory
from unit_bfm.v3.privileged import INDEX, SCALES
base=make_scene(seed=81, initial_q=0., initial_fraction=None,
                initial_dq=0., reset_mode='configured')
# P1-1: support entity parameters are absent at reset.
c=replace(base,scene='E1')
es=[UnitEnv(c),UnitEnv(replace(c,support_k=(180.,450.,4.)))]
bs=[e.reset() for e in es]; fs=[]
for e,b in zip(es,bs):
 h=FeatureHistory(); h.reset(b,e.known); fs.append(h.features())
print('support p/x/memory max diff',np.max(abs(bs[0]['p']-bs[1]['p'])),
      np.max(abs(fs[0]['x']-fs[1]['x'])),
      np.max(abs(fs[0]['memory']-fs[1]['memory'])))
out=[e.step(.1) for e in es]
print('support next dq diff',out[0]['dq']-out[1]['dq'])
for e in es:e.close()
# P1-2: translate the whole movable assembly without changing relative state.
es=[UnitEnv(replace(base,scene='E2',load_force=0.)) for _ in range(2)]
bs=[]
for e,extra in zip(es,[0.,.2]):
 m,d=e.model,e.data
 bottom=min(d.geom_xpos[i,2]-m.geom_rbound[i]
            for i in range(m.ngeom) if m.geom_bodyid[i]!=0)
 shift=.002-bottom+extra
 for name in ('root_z','object_z'):
  j=m.joint(name).id
  d.qpos[m.jnt_qposadr[j]]+=shift
  d.qvel[m.jnt_dofadr[j]]=-1.
 for v in e._anchors.values():v[2]+=shift
 e._object_base[2]+=shift
 mujoco.mj_forward(m,d); bs.append(e._boundary(False))
print('ground pmax',np.max(abs(bs[0]['p']-bs[1]['p'])))
for e in es:
 b=e.step(0.)
 print('ground contacts/vz',b['diagnostics']['contact_count'],
       b['p'][INDEX['common.linear_z']]*SCALES[INDEX['common.linear_z']])
 e.close()
# P1-3 fault injection checks validity semantics, not a natural instability claim.
e=UnitEnv(replace(base,scene='E1'));e.step(0.)
e.data.warning[mujoco.mjtWarning.mjWARN_BADQACC].number=1
b=e._boundary(True)
print('warning',b['valid'],b['terminated'],b['p'][INDEX['clock.solve_valid']])
e.data.warning[mujoco.mjtWarning.mjWARN_BADQACC].number=0
e._solve['qacc'][:]=np.nan;b=e._boundary(True)
print('qaccnan',b['valid'],b['terminated'],b['p'][INDEX['clock.solve_valid']])
e.close()
PY
```

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import copy,numpy as np
from unit_bfm.v3.physics import UnitEnv,make_scene
from unit_bfm.v3.collect import collect_episode
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.train import load_config,_scene
c=load_config('unit_bfm/v3/configs/full.json')
a=c['collection']['structures'][0]
cs=[_scene(c,a,'E0',i) for i in range(12)]
print('factory reset values',{(v.reset_mode,v.initial_q,v.initial_fraction,v.initial_dq) for v in cs})
print('bound dimensions',{k:len({str(getattr(v,k)) for v in cs})
      for k in ['tilt','encoder_sign','load_side','load_frame','load_start','load_end']})
e=UnitEnv(make_scene(seed=81,duration=.1))
ep=collect_episode(e,'audit',max_steps=10);e.close()
bad=copy.deepcopy(ep);bad.raw[3]['valid']=False
bad.valid=np.ones(len(bad),bool);bad.validate()
print('invalid raw but accepted',bad.raw[3]['valid'],bad.valid[2:4])
# Root already exists; never call add/save, only in-memory episodes.
r=Replay('unit_bfm/v3/docs',scene_weights={'E0':1.},
         expected_configs={'E0':['present','missing']},strict=True)
ep.config_id='present';other=copy.deepcopy(ep);other.source='policy'
r.episodes=[ep,other]
d=r.distribution();print('strict distribution',d['formal'],d['fallback'],d['empty_groups'])
PY
```

These scripts are observational evidence, and a successful exit does not mean that the discovered problem has passed. The fix should be to change the above output to distinguishable p, effective isolation or explicit rejection, and then rerun independent integration from the main window. External procedures, ground, reset and fault injection tests do not require lengthy training.


# Final rerun record

2026-10-10 08:44:23 UTC: The above two code blocks are extracted directly from this report and executed in a separate dictionary, exit code 0. All main conclusions get the same values again: support p/x/memory difference=0, next dq difference=.011423285907458502; ground p difference=2.7755575615628914e-17, contact 1/0, vertical speed −.06267789095661687/−1.098100000000001; warning=(False,True,1), qaccnan=(True,False,1); train factory reset is only configured/0/None/0; invalid raw is still allowed by explicit valid; strict returns formal=True/fallback=True and two missing configurations.

The SHA256 of the six designated review modules and collect this time is the same as the above table. The auxiliary coverage becomes `2d07fcfddf08e138c34d68c73bb926257166d3399e8fb7be92c4d9d30b9198c2` during concurrency. The two final recurrence scripts do not rely on coverage judgment and do not mistake this change as physics/Replay has been repaired. For subsequent version modifications, please refer to the reproduction output and the latest hash. This report is the result of an independent audit and is not a statement that the modification request has been executed or that formal project acceptance has been passed.
