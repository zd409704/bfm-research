# Proposal B (Packet B05): Falsifiable Verification Protocols for Beyond-Imitation Competence and Training Acceleration

Author: Primary Author B. Scope: transactional physics validation, conserved curriculum quotas, and preregistered evidence gates.
Frozen authorities: PROGRAM_CHARTER.md; synthesis/B01-synthesis.md; packets/B05/brief.md; baseline/02, baseline/03, baseline/05.
The permitted B05-SPIKE/VERDICT.json is prior contract evidence, not evidence of trained competence or end-to-end MuJoCo execution.
All protocols below are prospective; this proposal neither executes training nor claims acceleration.

## 1. Exact Substep Terminal-Boundary State Machine and Data Quarantine Specification

Let a control transition hold the applied 29-dimensional action through four MuJoCo substeps, each $\delta=0.005$ s.
The intended control duration is $4\delta=0.02$ s; $x_0$ is the committed pre-step state and $x_4$ the genuine pre-reset final state.
Use $s_j\in\{\mathrm{running},\mathrm{success},\mathrm{timeout},\mathrm{severe\_penetration},\mathrm{invalid}\}$, initialized to running.
These are provisional states until validation finishes; success or failure detection never authorizes an early replay write.
For this boundary machine order states by $\mathrm{running}<\mathrm{timeout}<\mathrm{success}<\mathrm{severe\_penetration}<\mathrm{invalid}$.
Other baseline task failures retain their own reason codes and absorbing masks; they are not relabeled as penetration.
At each $j\in\{1,2,3,4\}$ capture immutable state, contacts, body positions, simulation time, and solver diagnostics.
Define the following predicates on the snapshot and the previous substep, before constructing learning observations:
$$
d_j=\max_{\ell<ncon_j}\max(0,-\mathrm{contact.dist}_{j,\ell}),\qquad
J_j=\max_b\|p_{b,j}-p_{b,j-1}\|_2,\qquad V_j=\max_{i\in\mathrm{29\ joints}}|\dot q_{i,j}|.
$$
For no contacts set $d_j=0$; exclude reset displacement from $J_j$, and do not apply the angular-speed threshold to root translation.
Let $f_j$ require finite $(qpos,qvel,qacc,cfrc_{\rm ext})$, contact distances/forces, and all fields used in observations or rewards.
Let $g_j$ require correct dimensions, geometry indices, timestamps $t_j=t_0+j\delta$, and a valid pre-reset snapshot.
Let $v_j$ denote verified divergence or a simulator fault; finite output alone does not negate a recorded solver fault.
$$
I_j=\neg f_j\lor\neg g_j\lor v_j\lor(J_j>0.50\,{\rm m})\lor(V_j>100\,{\rm rad/s})\lor(ncon_j\ge nconmax).
$$
Here nconmax is a declared finite collector/backend contact capacity; saturation is conservatively invalid even before dropped-contact evidence.
The adapter must expose this capacity and overflow status explicitly; it must not assume an undocumented MuJoCo attribute exists.
Let $P_j=(d_j>0.03\,{\rm m})$; equality at 0.03 m, 0.50 m, or 100 rad/s does not trigger the corresponding strict inequality.
Let $U_j$ be the complete ordered traversal-success event and $T_j$ the 12.0 s timeout event.
Compute $e_j$ by the first matching row below, then $s_j=\max(s_{j-1},e_j)$ in the stated order.

| First matching predicate | $e_j$ | Immediate action |
|---|---|---|
| $I_j$ | invalid | Latch invalid; reject transaction; halt run/panel; no further integration required. |
| $\neg I_j\land P_j$ | severe_penetration | Latch physical failure; continue all remaining substep checks. |
| $\neg I_j\land\neg P_j\land U_j$ | success | Latch provisional success; continue checking. |
| $\neg I_j\land\neg P_j\land\neg U_j\land T_j$ | timeout | Latch provisional truncation; continue checking. |
| Otherwise | running | Continue checking. |

After substep 4, run a final audit of state/contact tensors, observation schema, reward finiteness, and elapsed time.
Set $s_{\rm final}=\max(s_4,e_{\rm final})$; no fifth integration step occurs.
Success requires rear whole-body/foot clearance, released box contact, legal corridor, bipedal support, low slip, and upright stability for 0.75 s.
Track that dwell in physics time: 150 qualifying substeps, not 37 rounded control ticks; audit contact/support predicates at every substep.
Success latches only on completion of the entire event chain; timeout cannot overwrite it, while penetration and invalid can.
Hand-on-box support is allowed; bypass, hanging, box-top stopping, and the baseline sustained crawling condition cannot count as success.
The priority proof is induction: after each audit, $s_j$ is the maximum of all latched events seen so far.
Thus any later invalid event replaces earlier penetration or success; later finite states cannot restore validity.
Before invalid, all four integrations are mandatory even after penetration; after invalid, immediate halt is mandatory.

| Final classification | valid_sample | terminated | truncated | Continuation $c$ | Commit |
|---|---|---|---|---|---|
| running | True | False | False | 1 | Real control row |
| success | True | True | False | 0 | Real terminal row |
| timeout | True | False | True | 1 | Real final row, bootstrap before reset |
| severe_penetration | True | True | False | 0 | Real failure row and closed task macro |
| invalid | False | Not a learning label | Not a learning label | Undefined | Nothing from rejected transaction |

A transition transaction contains raw $m_t,m_{t+1}\in\mathbb R^{229}$, $o_t,o_{t+1}$, applied action, immutable behavior_z, and diagnostics.
Before final acceptance, it touches neither replay, BN/normalizer moments, Gram tracking, committed counters, nor quota-credit debits.
On credible penetration, atomically append the FB row and close the current task macro after its actual $k\in[1,10]$ accepted controls.
The task record stores $(H_t,z_{\rm actual},R_k,H_{t+k},k,c=0)$ with $R_k=\sum_{i=0}^{k-1}\gamma_{\rm task}^i r_{t+i}$.
Use $y_Q=R_k+\gamma_{\rm task}^k c\min_iQ_{\bar\phi_i}(H_{t+k},c^{\rm geom}_{t+k},P_{\bar\psi}(H_{t+k}))$.
Set failure $\Phi_{\rm next}=0$ and first-success reward to zero; retain the measured $m_{\rm next}$ rather than replacing it by an absorbing zero vector.
For FB, retain the immediate successor-density/feature contribution but set its future-bootstrap mask to zero.
A failure outcome need not have a negative FB feature vector: its negative physical evidence is termination plus task reward and observed boundary geometry.
Deleting it changes the learned transition distribution and removes evidence that the executed action terminates future occupancy.
Publish both buffers through one commit identifier; a restart must complete or roll back a partial transaction, never duplicate it.
An invalid event discards the uncommitted control and unfinished macro transaction; earlier independently committed valid rows remain valid.
Store rejected snapshots only in a separate diagnostic quarantine, with seed, environment, height, first penetration, offending substep, and fault predicates.
No reset, synthetic final observation, quota debit, or committed-control increment may conceal the invalid event; halt the entire affected training run/panel.
Attempted physics work still enters the compute ledger even though the learning counter does not advance.

Eligible committed replay batches update BN once on $(o_t,m_t)$ and once on $(o_{t+1},m_{t+1})$, then freeze statistics.
Sample fresh z_update: 50% projected isotropic Gaussian and 50% current online $B(m_{\rm next}[\mathrm{perm}])$, both on $\mathcal S^{255}(16)$.
Expert encoding uses eval/no_grad and never updates BN; z_update never overwrites behavior_z or macro z_actual.
The target-coordinate Gram tracker consumes valid committed outcomes, including credible failure outcomes, exactly as B01 specifies.

## 2. Exact 4096-Environment Pool Quota Accounting and Multi-Seed Statistical Gates

Distinguish the 4096 physical environment IDs, 4096 committed control-row credits per quota epoch, and per-height evaluation trials.
No vectorized call counts as one environment transition: $S$ counts individual accepted training control rows.
The frozen training bank is $\{0.10,\ldots,0.70\}$ m; reserve 0.80 m for held-out evaluation.
Because the frozen files do not assign numbered stages, define Stage 0/1/2 as two-/five-/seven-height accounting snapshots.
Stage 1 is reached by successive single-height unlocks through 0.30 and 0.40 m; Stage 2 similarly passes through 0.60 m.
Stage 3 is an eight-height evaluation-only pool, never an authorization to train on the held-out 0.80 m height.
For $L\ge3$ active heights, use disjoint groups: lowest two, singleton frontier, and the remaining $L-3$ intermediates.
When intermediates exist, allocate integer group totals $Q_F=2048$, $Q_L=\lfloor0.20(4096)\rfloor=819$, and $Q_M=4096-Q_F-Q_L=1229$.
This assigns the fractional group remainder to intermediates; no rounding residue disappears.
For an ordered group of size $r$ and budget $b$, define
$$
A_i(b,r)=\lfloor b/r\rfloor+\mathbf1\{i>r-(b\bmod r)\},\qquad i=1,\ldots,r.
$$
Ties go to higher heights; store this convention in the configuration hash.
For $L=2$, use the explicit initial exception $(2048,2048)$; frontier/lowest groups must not overlap.
For $L=3$, donate the empty intermediate group's 1229 credits to the frontier: $(409,410,3277)$.
For every $r>0$, $\sum_iA_i(b,r)=r\lfloor b/r\rfloor+(b\bmod r)=b$ proves exact conservation.

| Stage | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0: initial training | 2048 | 2048 | 0 | 0 | 0 | 0 | 0 | 0 | 4096 |
| 1: frontier 0.50 | 409 | 410 | 614 | 615 | 2048 | 0 | 0 | 0 | 4096 |
| 2: frontier 0.70 | 409 | 410 | 307 | 307 | 307 | 308 | 2048 | 0 | 4096 |
| 3: held-out pool layout | 409 | 410 | 245 | 246 | 246 | 246 | 246 | 2048 | 4096 |

The Stage 3 layout reserves workers only; it does not weight success rates or replace the fixed 100-trial-per-height evaluation denominator.
Assign contiguous environment-ID intervals of the indicated lengths at pool construction; the last interval ends at ID 4095.
All environments retain their height throughout an episode; no unlock changes geometry under a robot.
At a stage change, queue target assignments and migrate IDs only on natural resets; every ID belongs to exactly one current height throughout.
During this explicitly logged migration, instantaneous per-height occupancy may differ from the target table, but total occupancy is always 4096.
Activate the new row-credit vector only after target occupancy is installed and the previous credit epoch completes; this separates layout from row accounting.
Reserve at least one worker at each old active height until old credits finish; newly assigned workers may wait without losing their environment IDs.
Replenish old-stage epochs while migration remains incomplete; all old heights retain workers, and new-frontier collection waits for activation.
Maintain nonnegative remaining credits $C_h$ and in-flight reservations $R_h$ with $0\le R_h\le C_h$.
Dispatch a row only when $C_h-R_h>0$; acceptance decrements both $C_h$ and $R_h$, rejection releases the reservation and halts.
An exhausted height pauses collection; other heights continue and may reset into another episode at the same height.
When $\sum_hC_h=0$ and no rows remain in flight, atomically replenish all credits and increment quota_epoch; paused workers must wake.
This prevents an all-paused deadlock and ensures exactly 4096 accepted rows per completed epoch, independent of episode lengths.
At each accepted $S=100000j$, suspend new dispatch for evaluation; split a vector batch at the threshold rather than silently overshooting.
Evaluation consumes no training quota, replay writes, BN updates, or training-source schedule increments.

For each frozen training seed and distinct tested height, evaluate $n=100$ independent ground-start episodes under 100% planner.
Use the conventional two-sided 95% Wilson lower endpoint ($z=1.95996398454$), not a one-sided 95% quantile:
$$
L(x,n)=\frac{\hat p+z^2/(2n)-z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n},\qquad \hat p=x/n.
$$
At $n=100$, $L(78,100)\simeq0.689296<0.70$ and $L(79,100)\simeq0.700200\ge0.70$.
Require $x\ge79$, zero invalid steps in the panel, and zero severe_penetration in every successful episode.
Credible penetration counts as a valid failed trial; never replace its seed, remove it, or shrink $n$.
Invalid halts the panel with a failed integrity gate; retain its planned denominator and label unexecuted trials unexecuted, not estimated successes.
Test the current frontier and each of 0.10 and 0.20 m; deduplicate the frontier if it is already a low height.
Unlock one height only after two consecutive, non-overlapping passing panels at the same frontier, then clear the passing streak.
Define low-height reference rates as the rates at the last accepted unlock (initially the first complete panel); freeze them until the next unlock.
Hold and reset the streak if either low-height rate drops by more than 0.10, or any current height gate fails.
Treat this observed-rate rule as a conservative operational hold, not a claim of statistical significance; exactly 0.10 is not a regression trigger.
Keep the present frontier and its quotas during a hold; no seed deletion, height demotion, or denominator repair is permitted.
Checkpoint frontier, pending layout, credits/reservations, epoch, streak, references, next evaluation S, RNGs, replay cursors, recurrent states, and all optimizers.
Resume only at a drained transaction barrier; verify hashes of code, XML/assets, source NPZ, schemas, quotas, seed manifests, and counters.

Preregister five training seeds $\{11,23,37,53,71\}$ and disjoint evaluation-seed manifests before launching any arm.
A competence claim requires every seed to pass the per-height gate; pooled 500-episode rates cannot rescue a failed seed.
Report each seed/height Wilson interval; these are marginal intervals, not simultaneous 95% coverage over the whole matrix.
Use separate confirmatory ID $\{0.10,\ldots,0.70\}$, interpolation $\{0.15,\ldots,0.65\}$, and OOD $\{0.05,0.75,0.80\}$ panels.
Include depths 0.25 and 0.45 m with all height-depth cells declared in advance; unseen reset seeds alone do not establish height generalization.
Require ordered physical success, not demonstration pose RMSE; log novel contact modes after auditing their absence in all 859 source frames.
Report planner/expert return crossover at matched states and source budgets; $Q$ predictions alone cannot certify crossover.
Retain pure task PPO, tracking PPO, AMP, and planner-only FB comparators with the same plant, reward endpoint, and resource caps.

Preregister three acceleration interventions on the common joint-FB baseline, with all eight binary factorial combinations:
$I_1$: optimized batching/compilation only; $I_2$: real replay four-step FB targets with behavior-command mismatch trace cutting;
$I_3$: eight-step differentiable world-model actor objective with the B01-consistent FB terminal tail.
$I_2$ cuts before the first unsupported continuation; fresh continuous z_update may reduce effective horizons to one, which must be reported.
For $I_3$, train dynamics only on valid real data, use no future reference hints, and route unreliable model rollouts to the standard one-step actor.
Use $r_z(\hat m)=\bar B(\hat m)^\top W_tz$, with B01's damped target Gram solve and routing gate; do not whiten prompts or z_update.
Freeze model, target-network, $W_t$, and $z$ parameters during actor differentiation while preserving state/action input gradients.
The short rollout and FB tail share the same latent, discount, feature coordinates, and termination mask; raw-dot-product splicing is a diagnostic ablation only.
Fix hardware, training seeds, update/data ratio, validation schedule, and hyperparameter-search allowance; preregister real-step and wall-time caps.
For every arm/seed/checkpoint record the four-dimensional ledger
$$
\mathcal C=(N_{\rm real},N_{\rm imagined},V_{\rm peak},T_{\rm GPU,total}).
$$
$N_{\rm real}$ counts attempted per-environment control transitions, with accepted/rejected/evaluation splits and an additional physics-substep counter.
$N_{\rm imagined}$ counts every predicted state-action transition, including dynamics training unrolls, detached targets, actor passes, and rejected rollouts.
$V_{\rm peak}$ is measured device-resident peak VRAM on the same hardware; report allocated/reserved peaks and the maximum over devices.
$T_{\rm GPU,total}$ includes compilation, model fitting, simulation, updates, evaluation, checkpointing, and idle CPU waits within the allocated GPU job.
For multiple GPUs report both elapsed job time and device-summed GPU-seconds; no acceleration factor may hide a change in device count.
Evaluate at equal real-step caps and, separately, equal GPU-time/VRAM caps; imagined steps are charged rather than equated with real steps.
Define time-to-gate at the second qualifying panel; non-attainment is right-censored at the fixed cap, never omitted.
If all five pairs attain the gate, set $d_s=\log(T_{{\rm base},s}/T_{{\rm arm},s})$ and report $\exp(\bar d\pm2.776\,s_d/\sqrt5)$, assuming approximately normal seed log-ratios.
Require the lower endpoint to exceed one; with any censored pair report bounded time-to-gate results and withhold this confirmatory speedup claim.
Also require competence non-regression in every seed; report sample efficiency separately from wall-clock acceleration and factorial interactions.
Tracking-task speedups cited in baseline/03 do not transfer numerically to autonomous traversal.

## 3. Serious Alternative Considered and Rejected

The serious alternative is to discard every $d>0.03$ m transition, arguing that uncertain contact geometry should not contaminate representation learning.
This improves apparent replay cleanliness and may reduce extreme targets, but conditions learning on the outcome of the executed action.
Let $D$ denote credible penetration and $p=P(D\mid s,a)\in(0,1)$; let failure reward be $-M$ and surviving one-step reward be $r$.
For a one-step example the true target is $Q(s,a)=(1-p)r-pM$; discarding $D$ estimates $Q_{\rm keep}(s,a)=r$.
Consequently $Q_{\rm keep}-Q=p(r+M)>0$ whenever $r+M>0$: boundary censoring creates optimistic bias even with infinite retained data.
Two plants with identical retained transitions but different $p$ are observationally identical to the censored learner and have different true values.
Thus silent deletion cannot universally recover the required Bellman operator; keeping valid failure evidence is necessary under the stated replay-only estimator.
This is the substantive alternative analysis required by method v1.0 §11.5; it does not claim every alternative estimator is impossible.
Explicitly modeling discarded-event probabilities and outcomes could repair identification, but would reintroduce the very failure evidence being discarded.
Soft penalties for NaN/overflow fail more directly: arithmetic corruption supplies no defined physical target, so a finite penalty cannot restore observability.
Pose-tracking RMSE is also insufficient: identical root-relative poses on opposite sides of a box can have different traversal outcomes.
These counterexamples reject the alternatives for this protocol; they do not establish that the proposed learner will succeed.

## 4. Candidate Necessity Claims (Appendix B)

**C-B05-B-01 — Grade 1, conditional logical necessity: deferred commit under substep corruption.**
Premises: a control row spans four substeps; later substeps can invalidate earlier finite states; replay/BN mutations are not perfectly reversible.
Conclusion shape: zero invalid-row contamination requires deferring irreversible publication until the final audit, or an exactly equivalent isolation transaction.
Proof witness: penetration at $j=2$, NaN at $j=3$ defeats any irrevocable commit at $j=2$.
Operational test: enumerate first-penetration and later-corruption positions, including final audit, and compare replay/BN/counter hashes before and after rejection.
Falsifier: a system satisfying the premises commits irreversibly before final audit yet guarantees zero contamination for every such trace.
An exact rollback system lies outside the irreversible-mutation premise and is an allowed equivalent mechanism, not contrary evidence.

**C-B05-B-02 — Grade 1, conditional identification necessity: preserve credible failure information.**
Premises: on-policy dynamics have $p(D\mid s,a)>0$; values are estimated solely from unweighted retained replay; no external failure model is supplied.
Conclusion shape: unbiased identification across all such dynamics requires retaining failure outcomes or equivalent sufficient failure statistics.
Operational test: the two-outcome MDP above, varying $p$ while holding the conditional surviving distribution fixed.
Falsifier: a replay-only estimator recovers both distinct true values from identical retained distributions under all stated premises.

**C-B05-B-03 — Grade 2, empirical necessity candidate: realistic boundary coverage for reliable obstacle learning.**
Premises: the frozen architecture, five seeds, fixed budgets, and all task/geometry contracts; only retention of credible failure rows changes.
Conclusion shape: failure retention is necessary within this experimental family for all-seed held-out competence at the preregistered budget.
Operational test: retention versus deliberate censoring as an isolated diagnostic arm, keeping failure counts and evaluation denominators intact.
Falsifier: the censoring arm passes every competence gate within budget; absence of such a result is evidence within this family, not a universal theorem.

## 5. Pre-Registered Empirical Spike Protocol

Pin the requested MuJoCo 3.17 backend identifier, package/build hash, model XML, controller, and adapter in the manifest before execution.
If that exact backend cannot be instantiated, mark the backend suite BLOCKED; a mocked oracle cannot substitute for real-backend evidence.
Separate deterministic adapter fault injection from bounded real simulation; both must exercise the production train.py -> runner.run -> Trainer path.
**Test 1 — credible penetration commit:** use a prevalidated finite collision fixture with $d=(0.01,0.031,0.02,0.01)$ m, no overflow or divergence.
Assert four integrations plus final audit, valid_sample=True, terminated=True, $c=0$, $\Phi_{\rm next}=0$, exactly one FB append and one closed task macro.
Assert measured terminal m_next, unchanged behavior_z, correct actual $k$, and continuation to the next panel seed with denominator 100.
**Test 2 — corruption dominance:** reuse that trace; inject NaN in qacc at substep 3, and separately ncon=nconmax at substep 4.
Both must return invalid with valid_sample=False, halt, zero appends/normalizer updates/credit debits, and unchanged committed counters.
Extend the matrix to Inf in each required tensor, jump 0.500001 m, joint speed 100.000001 rad/s, malformed final snapshots, and final-audit overflow.
Repeat with provisional success before the fault; test equality boundaries separately and prove quarantine cannot enter later replay sampling.
**Test 3 — quotas and gates:** assert the exact 2-, 5-, and 7-height vectors in §2, plus the 8-height evaluation layout and the empty-middle exception.
For each completed epoch assert sum=4096, no negative credit, no duplicate environment ID, atomic replenishment, and wake-up of exhausted workers.
Assert 78/100 fails and 79/100 passes; exercise pass/pass, pass/fail/pass, low-height 11-point regression, and a 10-point boundary case.
A penetration episode remains in the 100-trial denominator; an invalid episode halts the panel and blocks unlock without replacement.
Then run bounded real-backend CPU checks with seeds 101–104, at most 600 controls per seed, retaining every failure and integrity diagnostic.
Require at least one credible collision witness; if none occurs, mark real-collision coverage NOT ESTABLISHED rather than claiming Test 1 backend success.
Exercise all six optimizer states, finite nonzero gradients on intended paths, and forbidden-gradient/BN/source-label assertions.
Checkpoint at a drained boundary; compare resumed versus uninterrupted next 32 accepted controls, quota transitions, RNG draws, and update outputs.
Require exact discrete-state/hash equality and preregistered numeric tolerance $10^{-6}$ on a deterministic CPU build; report unsupported determinism explicitly.
Publish per-test assertions, traces, hashes, elapsed time, and coverage gaps; PASS requires every mandatory assertion, not merely process exit zero.
The existing verdict reports the expected 2/5/7 quotas and Wilson threshold, but omits evidence for several backend, overflow-isolation, and resume assertions.
Therefore it motivates this expanded suite; only full GPU multi-seed training and held-out panels can establish beyond-imitation competence or acceleration.
