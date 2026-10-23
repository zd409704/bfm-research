# Eng-2 B — deferred PLAN v1: exact-reference channel discriminator

**Status: sealable draft; DEFERRED. No execution, results, or authorization asserted.** Scope is a synthetic proprioceptive channel for a home humanoid / target plant. Proposal stance is contract-first → bounded amended-A, a proposed override of D-Eng-1-001 Alternate-B routing under D-Prin-3-001.

## 1. Entry manifest and seal

Required fields before execution:

- Human-lead approval reference for the complete `(q_c,r_c)` table and deadline, or explicit exploratory placeholder policy: **PENDING**.
- Human-lead declaration of target effort measurement point, including nuisance locations: **PENDING**. Record match/mismatch to this motor-side fixture; do not silently relocate noise/friction to fit the declaration.
- Human-lead choice of amended-A branch / override: **PENDING**.
- Contract, implementation, generator and PLAN SHA-256; code-review/checker identity; dependency versions: **PENDING**.

Only the approval/identity/hash fields may be filled without changing the experimental design. If the ratified task requires different numbers or a different measurement point, amend the design explicitly, review and reseal before running. Missing approval means DEFERRED, not experimental FAIL. No approval is inferred from elapsed time or this proposal.

Runner writes only to an orchestrator-assigned authorized spike directory after selection; this author creates no such directory or runnable experiment. Record all seeds, hashes, elapsed time and deviations. No rerun after inspecting evaluation outcomes. A failed harness may receive a documented bug-fix amendment; its prior output remains INVALID. Changing a scientific assumption starts a new plan version.

## 2. Question and limitations

At a fixed false-positive probability per independent 60 ms window, is a poor frozen detector improvable within the very same channel, or is the requested operating point beyond that channel under this exact model? The reference must be capable of returning a channel shortfall; a stronger detector alone is not an upper reference.

This is a deliberately analytically tractable surrogate. It does **not** reproduce Eng-1 dynamics, detector, class distribution or A02. It tests diagnostic machinery and yields conditional channel comparisons. It cannot retrospectively attribute Eng-1 FAIL. The common class names below preserve the duration/magnitude grid but do not make experiments equivalent.

## 3. Fixed channel model

Normalized single-joint inertia is 1. Time step `h=0.005 s`, horizon `T=0.060 s`, `N=12`. Commanded effort is zero and public. Each trial is independently reset. Positive classes are the full Cartesian product `d ∈ {10,20,50} ms`, `M ∈ {2,5,10}` in normalized generalized-effort units; negative trials have no contact. Contact is `c_i=M` for intervals with `i*h<d` and zero thereafter, `i=0..11`. The probe onset is known at window start under both hypotheses. Duration/magnitude are protocol settings, not hidden labels; the null trial receives the same settings.

Dynamics and observations:

```
v_0 = 0
v_(i+1) = v_i + h*(a_i + f_i + c_i)
v_obs_i = v_i + epsilon_i, i=0..12
y_i = (v_obs_(i+1) - v_obs_i)/h
m_i = a_i + eta_i
```

`a_i` is motor effort error, iid Gaussian with SD 3. `f` is stationary zero-mean Gaussian downstream friction/nuisance with covariance `F_ij = 9*(0.8^abs(i-j))`. `epsilon_i` are iid Gaussian with SD 0.002 in velocity units. `eta_i` are iid Gaussian with SD 1. All four families are mutually independent; distributions do not depend on the contact label. Measured effort `m` is upstream of `f`. This is a phenomenological Gaussian nuisance model, not a mechanistic claim about friction. Its unbounded tails preclude deterministic safety guarantees.

Define first-difference matrix `D` of shape 12×13 (−1,+1 in neighboring columns). Then `S_y=9I+F+(0.002/h)^2 DDᵀ`, `S_m=10I`, `Cov(y,m)=9I`. Means are `E[y|Z=1]=c`, `E[m|Z]=0`; null means are zero.

Four export channels:

- R1/CMD: `X=y`; command history is public zero.
- R1/REAL: `X=(y,m)`.
- R2/CMD: `X=B y`.
- R2/REAL: `X=(B y,B m)`.

`B` is 3×12, nonoverlapping blocks of four with coefficient 1/4. R2 interval is 20 ms, and both rates end at 60 ms. This is a specified interval-average export, **not** an assertion that a 50 Hz point-sampling implementation has this channel. Construct each channel mean and covariance by the same explicit linear map. Rates and effort sources remain separate factors. No upstream-friction variant or dedicated contact sensor is included.

## 4. Exact channel reference and frozen detector

For each of 36 cells, let `mu` be the positive mean and `S` the shared covariance. Both simple hypotheses and their metadata are declared. Compute `kappa²=muᵀ solve(S,mu)`. The likelihood-ratio statistic is monotone in `muᵀ solve(S,X)`. At false-positive budget `r`, the optimal TPR is

`U(r) = Phi(kappa - Phi_inverse(1-r))`.

It is both an attainable reference and a ceiling **only for this exact Gaussian model/channel and its simple-hypothesis protocol**. The reference is not given realized nuisance, contact truth or an extra measurement. For `mu=0`, define `U=r` with an independent randomized decision. Implement `Phi` with standard-library `erfc` and inverse by bounded bisection; NumPy linear solves suffice. No external literature or library downloads are required to implement this sealed calculation; independent algebra review is required before trusting it.

Independent checker: Cholesky-whiten `mu`, calculate its Euclidean norm and reconstruct the one-dimensional Gaussian ROC; compare `kappa` and `U` to the solve path within `1e-10` absolute/relative tolerance (absolute tolerance applies near zero). Verify `S` symmetry/positive definiteness and solve residual ≤ `1e-10` relative. Borderline or failed numerics yield UNRESOLVED, never a channel shortfall.

Frozen practical comparator: uniform boxcar score `s=wᵀX`, where `w` averages all y samples for CMD, and averages y minus m for REAL, at the given rate. Its weights are fixed before all data, identical across durations and magnitudes. This deliberately simple detector is **not Eng-1's detector**. It is a transparent benchmark for whether the reference separates an inefficient statistic from a channel limit. Compute its analytic variance for checks but calibrate its threshold on a disjoint null split. No gain search, per-class detector selection or second detector is allowed.

## 5. Operating points, independence and resources

Exploratory policy offered for explicit approval: every class requests `q=0.90`, `r_w=0.0006`, deadline 60 ms. There is one binary decision per reset window, so `r_w/T=0.01` expected false events/s applies only to disjoint windows running continuously under this reset protocol. It is not interchangeable with a continuous detector's false-event rate or latency convention. Secondary descriptive table at `r_w=0.001` is fixed in advance to aid reading the inherited result; it never replaces the primary threshold or repairs A02. No continuous-onset p95 latency claim is made.

Splits use independent random-generator streams, PCG64 seeds 220201 (calibration), 220202 (null evaluation), 220203 (positive evaluation), 220204 (controls), 220205 (non-interference). Draw 100,000 calibration-null windows per channel, 100,000 evaluation-null windows per channel and 10,000 positive windows per class/channel. Sharing a base trajectory across channels is permissible for paired comparison; no window is reused across splits or counted as multiple independent observations within one cell. Preserve labels only in the evaluator. Each window draws fresh `a,f,epsilon,eta` and resets state. No pooled successive windows from a long episode.

Comparator threshold: sorted calibration score with order index `ceil((1-r_w/2)*n_cal)` using one-based indexing; strict `>` declares contact. The conservative calibration target allows sampling slack; evaluation determines whether the actual r budget is met. Reference threshold uses the analytic normal quantile for the stated budget. Generate in batches ≤2,000; CPU-only, standard library/NumPy, total ≤15 minutes and peak RSS ≤1 GiB. If incomplete, emit INCOMPLETE; do not truncate the grid or reduce the sample count and still claim a formal result.

Report exact Clopper–Pearson upper/lower bounds for evaluation TPR/FPR. Implement stable binomial-tail inversion using log-gamma/log-sum-exp and bisection; test boundary counts separately. For 36 primary cells ×2 detectors ×2 metrics ×2 tails, allocate `alpha_tail=0.05/288` (conservative even where a null sample is shared). This bounds all primary reported intervals jointly by a union bound without assuming cell independence. Secondary operating points are analytic descriptive outputs only. Do not bootstrap pooled windows or use zero observed errors as zero FPR.

## 6. Harness gates and controls

All gates must pass for `harness_pass=true`:

1. Algebra/numerics: reference paths agree; covariance checks pass. Analytic boxcar ROC never exceeds the optimal ROC by >`1e-10`. R2's transformed-channel reference does not exceed R1's, and adding m does not lower the reference, within tolerance. These are implementation consistency checks, not empirical proof of a theorem.
2. Controls: exact null `mu=0` gives `U=r`; exact high-signal unit-variance control with `kappa=10` gives `U>0.999`. CP routines satisfy direct binomial-tail equations within `1e-8` and boundary-count formulas within `1e-10`. Primary reference's analytic probabilities must lie inside the simultaneous evaluation intervals. A miss invalidates this run; no seed reroll (a predeclared finite false-alarm probability remains).
3. Provenance/independence: manifest enumerates all detector inputs; no truth fields; every evaluation window has a unique split/seed/index; per-window state resets verified. Mutation of class/version/rate/effort point makes the report consumer return UNKNOWN/OUT_OF_SCOPE. Deliberate hidden-label access must be rejected by the interface test.
4. Non-interference: identical seeded fixture replay with publication on/off yields exactly equal commands and plant trajectories. Only report traces differ.
5. Completeness: all 36 primary cells, uncertainty bounds, analytic reference, seeds, hashes and elapsed/resource status present. No unexplained deviation or out-of-scope UP evidence.

A harness failure gives INVALID, independent of detector performance. A numerically unresolved reference prevents a trusted diagnostic verdict for that cell; do not convert it to a shortfall.

## 7. Scientific statuses and stopping

For a valid cell, at primary r:

- `MODEL_CHANNEL_SHORTFALL` if validated analytic `U < q-1e-8`. This is a conditional result about this model/channel, not the target and not a C-P1-012 downgrade.
- `SUPPORTED` if comparator `TPR_L≥q` and `FPR_U≤r`. Report achieved sufficiency, with this fixture, detector and calibration qualifier.
- `REF_DETECTOR_GAP` if `U≥q+1e-8`, comparator `FPR_U≤r`, and comparator `TPR_U<q`. The attainable exact reference supplies the witness; its sampled check must have passed the harness.
- `UNRESOLVED` otherwise, including overlapping confidence bounds, FPR calibration failure, or a numerical threshold margin. Never interpret calibration failure as information absence.

Report reference and comparator results separately even when a cell has a shortfall. All-class task support requires every ratified required cell to be SUPPORTED; no class-selected average passes it. C-Eng2-B-02 is supported only if at least one REF_DETECTOR_GAP exists. A full grid without such a gap is NOT_SUPPORTED for that hypothesis, even if channel shortfalls are informative.

Stop after this one complete attempt. If a gap exists, propose a separately scoped detector improvement; no automatic second run. If the ceiling fails, propose contract/model/channel review; do not loosen q, delete classes or move friction. If unresolved, report it. Choosing an envelope branch afterward remains a human planning choice with its own independent question, not a theorem following from FAIL.

## 8. Artifact schema and interpretation

Future runner produces `manifest.json`, `results.json`, `VERDICT.json`, `run.log`, `deviations.md` and a concise report, all attached to the original seal. Minimum verdict fields:

```
plan_sha256, code_sha256, contract_sha256, approval_refs, branch,
execution_status: COMPLETE | INCOMPLETE | INVALID,
harness_pass: boolean,
engineering_support: SUPPORTED | NOT_SUPPORTED | UNRESOLVED,
per_cell: {class, channel, q, r_window, deadline_ms, U_model,
           reference_counts, detector_counts, simultaneous_bounds, status},
claim_grade_changes: "none",
scope: "Gaussian surrogate; known-onset reset-window protocol; harness only",
bypassed_edges: [E05,E06,E08,E09,E14],
listed_not_bypassed: [E10,E11], not_invoked: [E17-acquisition]
```

`engineering_support` refers to C-Eng2-B-02, not all-class task acceptance, which must have its own explicit boolean and required-class list. If any missing/unresolved cell prevents the registered conclusion, use UNRESOLVED. PASS means harness only; no hardware transfer, retroactive A02 pass or claim state change. No amendments to C-P1-012 are self-adjudicated; send proposals/data to its assigned claim adjudicator, including the unresolved B.9.6 accounting.

## 9. Concrete amended-B alternative contract (separate branch)

This contract makes the alternative reviewable; it is **not** a second authorized experiment in this PLAN. Independent question: can one fixed controller certify both fixed-mode and transition envelopes under one delayed coupled plant specification?

Proposed synthetic parameters, requiring explicit owner adoption: 1 ms discrete step, 200 steps, state `x∈R²`; modes `A0=[[1.002,.001],[.001,1.001]]`, `A1=[[1.001,.002],[-.001,1.002]]`; `b=[.001,0]ᵀ`; bounded disturbance `|w_j|≤0.00001` each step. Update `x_(k+1)=A_mode x_k+b a_k+w_k`; actuator `a_(k+1)=0.8a_k+0.2 clip(-[8,4] y_k,-1,1)`. Delayed observation `y_k=x_(k-l)+n_k`, `|n_j|≤0.0001`, delays `l∈{0,2,5,10}` steps. Initial x box `|x_j|≤0.001`, a=0; negative-time history equals the same uncertain x0, preserving correlation. Envelope `|x_j|≤0.01`, `|a|≤1`, including reset states.

Schedules: constant mode0, constant mode1, mode0→mode1 at 100 ms, mode1→mode0 at 100 ms. At transition apply `x←diag(1,0.9)x` before the next update, retain actuator and entire observation history. Schedule is an evaluator premise, not an inferred contact label; feedback uses only y. The certificate scope includes the exact schedule and reset, not arbitrary switching. The owner controls all versions and bounds; the body-loop owner controls the fixed controller; checker owns certificate validity; scene publisher is read-only; decision core treats missing/stale/out-of-scope certificates as UNKNOWN. This refusal does not certify physical stopping.

A sound augmented-state reachability checker yields CERTIFIED if all bounds and command unsaturation are proved for the whole horizon; a verified in-set replay violating the envelope yields VIOLATION; otherwise UNRESOLVED. Correlations across history and actuator state must be preserved; positive sampling is never a proof. Saturation not proven inactive is unresolved unless explicitly covered by a sound piecewise checker. Engineering support requires a CERTIFIED fixed-mode/transition pair at the same delay. Harness PASS additionally requires analytically checkable positive/negative controls, certificate mutation rejection, and publication non-interference.

Before selecting this alternative for execution, complete and seal a branch-specific PLAN specifying checker arithmetic/outward rounding, control fixtures, witness-search budget and result schema. These omissions are explicit: the alternative is a specified contract, not an executable solver PLAN. The same human `(q,r)`/placeholder and effort-point gate still applies by D-Prin-3-001, even though q/r is not an envelope theorem premise. No Candidate-as-veto or automatic promotion from amended-A failure.
