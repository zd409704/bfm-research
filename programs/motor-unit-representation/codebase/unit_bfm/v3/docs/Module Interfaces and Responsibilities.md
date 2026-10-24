> The most recent monitoring restrictions are based on [the current round of development constraints and acceptance ](Current Development Constraints and Acceptance.md): the old "complete episode disk archive" of this document has been abolished; Replay defaults that the RAM is in line, and the old API needs to be compatible or explicitly moved.

# V3 Implementation Interface (2026-10-10)

The main window maintains this file. Only write unit_bfm/v3/ and this round of relay logs; modification of old unit_bfm/*.py, configs, tests, artifacts, biped, and eval_web is prohibited. There is no need to create a new worktree for the shared directory, and independent packages and output directories achieve version isolation.

# Boundaries that all modules must respect

Skeleton along V2: Actor/F double E branch, E=Linear256,LN,Tanh,Linear128,ReLU; head256 ReLU output. B=13→256 LN Tanh→256 ReLU→16 SphereNorm4. z16. No bonus/auxiliary loss/GRU added. g13/x137, F y=[x,p_physics,feature_memory]. Known parameters are entered into the Actor, and only F is unknown true value. Strictly 100Hz/1kHz, true integral, causal 5-point acceleration. The document is subject to unit_bfm/docs/V3 Network and Training Implementation Plan.md; if conflicts are found and reported, requirements cannot be reduced silently.

# Unified Python API (click here to implement it first, necessary changes are coordinated by the main window)

All environment raw records use numpy FP64/FP32 SI, control an episode, return immutable copies, and do not span resets. Public definition:

- `physics.py`: `SceneConfig` dataclass (jsonizable), `make_scene(seed=..., scene='E0', fixed_side='P', geometry_id=0, limit_id=0, capacity_nominal=6.0, **overrides)` returns configuration. `UnitEnv(config, seed=0)` CPU MuJoCo oracle.
- env ​​`.reset(episode_id=0) -> boundary dict`; `.step(u_c:float)-> boundary dict` (will not reset automatically); `.known` dict, `.physics_schema` field description list, `.p_dim`, `.metadata` dict, `.close()`.
- Baseary shall fill `time,q,dq,tau_endpoint,u_previous,tau_integral,u_integral,interval_dt,interval_valid` (previous inter-sector points); Reset = invalid; `p`, one-dimensional fixed physics privilege vector, `terminated,truncated` bool (10s normal cut nonterminal); `diagnostics` dict (independent overwhelm/solve valid/real active information). XPROTT4X bool indicates that physical transfer is available. No random plans for the future. q/tau/u regulates coordinates, qpos raw and tree map and metadata.
- env known: 0float [2], `limits`float[2], `rigid`float[8] (P then D, mass, COMx, COMz, Iyy); COM is currently expressed in M and can be updated at each border), `rigid_valid` float[8], `drive` float[8] (S,lower,upper, T_, Deray_s, damping, operation, armature), `drive_valid` float[8]. `known` parameters shall not contain actual hidden multipliers.
- `.physics_schema` is the same in all E0–4 templates and has field name/scale/source/units/time/reference; it is not allowed to fill in 0 to pretend to be an unimplemented true value, and there is a mask in the empty slot. Physics is responsible for registering precise fields and exporting, and memory is spliced ​​by core.
- `features.py`: `FeatureHistory()`; `.reset(boundary,known)`, `.append(boundary,known=None)`; `.features() -> dict {'g':np.ndarray(13), 'x':np.ndarray(137), 'memory':np.ndarray(MEMORY_DIM)}`. Internal 22 boundary rings, 10 slow at 50Hz + 8 fast at 100Hz, real integration; the original ring+phase of feature_memory is enough for recursion, and there is no world quantity to mix Actors.
- `networks.py`: `Networks(p_dim:int)` .actor/.f1/.f2/.b; F input y=137+p_dim, where p_dim contains physics+memory. `.counts()`.
- `learner.py`: `Learner(p_dim,device='cpu',seed=...,config=None)`; `.update(batch)->dict metrics`; batch tensor keys x, p, u, x_next, p_next, g_next, discount ([N ,1]), `goal_g` independently matches complete goal [N ,13], `goal_valid` [N]. The sample_z is random and half of the current B, it must be detach. Interfaces `.sample_z(n,goal_g=None,goal_valid=None)`, `.state_dict()`/`.load_state_dict(...)`; .net are public. Normalized g is given by features and no longer cuts old o24.
- `replay.py`: To manage complete episode data, it is recommended that `Episode` fields x[T+1,137],g[T+1,13],p[T+1,p_dim],u[T,1],discount[T,1], raw records/known, source(rule/policy), scene/config_id, phase[T]. The disk/CPU is reserved and the entire database is not moved to the GPU; the interface is stabilized by itself for train use.
- pipeline agent is responsible for the program, Replay, collect/train/evaluate/interface/coverage/config, core and physics provide the above API. The main window integrates README, dependency, run/acceptance documentation and cross-testing without snapping up with agents.

# Division of labor and resources

- v3-core: schema.py, features.py, networks.py, fb_loss.py, learner.py, tests/test_core*.py; only CPU, not GPU.
- v3-physics: physics.py, mechanics.py, randomization.py, privileged.py, warp_backend.py, kernels.py, tests/test_physics*.py; GPU is only used for physical verification of this agent, not for training.
- v3-pipeline: replay.py, programs.py, collect.py, train.py, coverage.py, queries.py, evaluate.py, interface.py, configs/*, tests/test_pipeline*.py; Only CPU short-term integration, relying on synthetic but not claiming physical acceptance.
- Main window: init/docs/README/manifest and tests/test_integration*.py; full-link GPU test waits for the physical agent to release the GPU.

An accurate handoff will be given after all responsibilities are fulfilled in the first round. The complete GPU training project cannot be declared passed just because CPU smoke has passed. Collaboration is required to write `unit_bfm/v3/docs/<agent>_handoff.md`, other exclusive paths cannot be written.

## Cross-module contract covering diagnostics (main window appended)

physics is responsible for generating the following SI fields from the real solution, the pipeline does not infer from the labels:
`contact_normal_force_N` (the sum of the relevant contact normal force amplitudes of the research unit to avoid impersonation of grounding of irrelevant objects), `adjacent_max_abs_dq`, `adjacent_max_abs_tau_Nm`, `adjacent_declared_capacity_Nm` (if the multi-adjacency capabilities are different, the stall determination needs to be measured axis by axis), ZXQPLACEHOLD ER4ZXQ/`fixture_D_force_N`, `fixture_P_torque_Nm`/`fixture_D_torque_Nm` (side name: mechanical identity), `applied_load_norm_N` (explicit external load of the research unit, excluding obstacle position control force; pure force coupling field), `solver_valid`.

The failover must be isolated and cannot be physically terminated under the guise of `terminated=true`. General operating capability and actual coverage are accepted separately. After the first round of core is passed, other modules are read-only audited without changing their code.
