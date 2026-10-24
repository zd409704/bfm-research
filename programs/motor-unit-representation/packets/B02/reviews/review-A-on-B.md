# Blind Review A on Proposal B (Packet B02)

**Reviewer:** Blind Reviewer A. **Inputs read:** `PROGRAM_CHARTER.md`, `packets/B02/brief.md`, `packets/B02/proposals/B.md`. No other file in `reviews/` or `drafts/` was opened, and Proposal A was not read. Baseline documents were not available in this review context, so any claim in B that depends on `baseline/02` or `baseline/03` content (13-field `g` layout, network widths, legacy counter semantics) is marked *unverifiable here* rather than accepted or rejected.

**Overall assessment.** The proposal is careful and honest. It separates scheduled opportunity from physical success and from actor competence, it fails closed, and its arithmetic checks out (verified below). Its main weaknesses are not arithmetic. (i) The 720-cell guarantee counts rows but does not guarantee the *behaviourally relevant* diversity inside each cell: the replay is phase-locked across configurations and covers one load sign only. (ii) The rule-witness counters can be met by the easiest load tier under a feedforward controller that knows the release time. (iii) Memory compliance depends on an unverified assumption of 512 factorable slots, plus an unverified 350 MB model budget. (iv) The spike tests only whether the full bundle is *sufficient*. None of the ablations has a pre-registered prediction that could fail.

Verified arithmetic (all correct):
- Scene sequence counts are (4,3,4,3,6)/20.
- 144·20·80 = 230,400.
- Rule quotas (6,554/4,915/6,554/4,915/9,830) and policy quotas (13,107/9,831/13,107/9,830/19,661) follow the stated largest-remainder rule with the smaller-scene-ID tie-break. The per-cell ranges are correct.
- 10,419 floats × 4 B × 98,304 = 4,096,917,504 B. Factored: 9,395 × 393,216 + 294,912 = 3,694,559,232 B. Aggregate 4,052,559,232 B, headroom 47,440,768 B.
- atanh(0.95) = 1.831780823, and 1 − 0.92² = 0.1536.
- 19,200 groups × 240 = 4,608,000 transitions, and 19,200 × 25/24 = 20,000 updates.
- Static panel: 144·3·2·3·3 = 7,776.
- The cubic reference-velocity derivative is correct.

---

## 1. Gate & Hard-Constraint Audit

| # | Constraint (source) | Verdict | Notes |
|---|---|---|---|
| G1 | Method version hash `1ce8d1b3…` (brief header) | **PASS** | Matches. |
| G2 | Inherited ledger `X-BASE-001..005` (brief) | **CONDITIONAL** | B also declares `D-B01-001` "with its synthesis" as an inherited constraint (B.md:3), and relies on the "B01 slot manifest" / "B01-sanitized `p_t`" for its causal-integrity argument (B.md:57–59, 121, 150). `D-B01-001` is **not** in the brief's inherited snapshot. The orchestrator must confirm that it is admissible frozen context for B02. Otherwise the H1/Boundary-2 compliance argument rests on a decision outside this packet's ledger. |
| G3 | Charter Boundary 1: deployment purity | **PASS** | Actor uses only `x137, z*` with `z* = B(normalize(g_hold))` (B.md:169). Rule access to privileged state is training-only (B.md:59). Note that the auxiliary imitation term trains the actor toward a privileged-informed teacher (see §2, R1-c). This is not leakage, but it is an observability mismatch. |
| G4 | Charter Boundary 2: causal privileged inputs | **PASS** (conditional on G2) | Ordering is explicit: generator → latch `p_t` → action → integrate → pack `p_{t+1}` (B.md:57). Exogenous phase/countdown/scheduled release are explicitly separated from endogenous reactions, which the charter's "or explicitly separate…" clause permits. The contact estimate is the previous interval's (B.md:79). The Stage A fault injection of an action-dependent future reaction is a good executable check. |
| G5 | Charter Boundary 3: real physics across 144 × E0–E4 | **PASS** | Real rollouts; "label alone does not satisfy contact coverage"; nothing is synthesized; INFEASIBLE_CONFIG fails rather than dropping a configuration (B.md:27, 61, 185). |
| G6 | Charter Boundary 4: no convergence claim from the 101-update smoke run | **PASS** | Stated explicitly (B.md:5, 290). |
| G7 | Brief: 98,304-transition cap, split 32,768/65,536 | **PASS** | Fixed per-cell capacities; logical rows are never reduced (B.md:146, 150). |
| G8 | Brief: ≤ 4.10 GB tensor memory / rubric 4.694 GB peak RSS | **CONDITIONAL — likely BLOCKED without the factoring** | The dense layout alone is 4,096,917,504 B, which leaves 3.08 MB for *everything else*, so it is infeasible. Compliance therefore requires (a) exactly ≥512 provably immutable or constant-masked privileged slots, which B admits are unknown (B.md:154), and (b) all models, targets, gradients and optimizer state fitting in 350 MB, which is unverified (see R3-b). B correctly defines MEMORY_LAYOUT_BLOCKED, so this is honest, but the 20% rubric dimension is currently a promissory note. |
| G9 | Brief: all 144 groups (36 seeds × 4 strokes, C0 ∈ {3,6,9}) | **PASS** | Correctly avoids a spurious ×3 factor (B.md:11). |
| G10 | Brief Deliverable 1: E3 ≥25-step hold, E4 release + ≥20-step recovery, 20/15/20/15/30 % | **PASS** | E3 has 65 constant-load intervals and E4 has 30 loaded + 40 recovery intervals. Fractions are exact only at complete cycles, and B reports this honestly. Minor misstatement: B says "the brief permits either [release or impulse]" (B.md:53). The brief only mentions a "load-release transition". Remove the attribution. |
| G11 | Brief Deliverable 2: rule wiring across 720 cells, normalizer, tanh fix | **PASS (substantive objections in §2)** | |
| G12 | Brief Deliverable 3: exact `g_13^hold(q*)` and threshold < 0.35 rad/s across E0/E3/E4 | **PASS (layout unverifiable here)** | The 13-field count (2+1+1+3+3+3) is consistent. It cannot be checked against `baseline/02` from the frozen inputs given to this reviewer. |
| G13 | "No experiment results claimed" | **PASS** | Explicit (B.md:3, 248). |

**Gate verdict:** No hard-constraint violation found. Two items stay conditional: G2 (ledger scope of `D-B01-001`) and G8 (memory layout feasibility). Both must be resolved before the spike can be sealed.

---

## 2. Rubric-Keyed Technical Objections

### R1 — Resolution of Audit Issues #1, #2, #3, #5, #6, #8 (35%)

**R1-a [MAJOR] Training covers one load sign; the evaluation panel tests both (Issues #1/#5 interaction).**
Maximizing `|A| = |−G(q*) − σλS|` over σ ∈ {±1} always selects σ = sign(G(q*)), with ties only at G = 0 (B.md:29–35). The loaded equilibrium actuator torque is therefore always `τ_a = sign(G)·λS`. Every training E3/E4 episode, and every rule anchor witness, shows the actuator flipping sign relative to its unloaded gravity-holding torque `−G`. The static panel instead runs **both** signs (B.md:171). Half of the 5,184 loaded panel cases need `τ_a = −sign(G)·λS`, up to 0.92 S in the gravity-compensating direction. That regime never appears in training replay or in rule anchors.
- This is undeclared out-of-distribution evaluation: the panel either tests generalization without saying so, or the training schedule is wrong.
- Either way, `actor_hold_ok` requires every one of these cases to pass, so FULL is set up to fail for a reason unrelated to the mechanisms under test.
- *Fix:* alternate σ deterministically in training, e.g. `σ = (−1)^(c+j+⌊j/9⌋)`, with the same 0.15 S floor/0.95 S feasibility rule as the panel. Alternatively, declare the opposite-sign cases a held-out generalization panel with its own pre-registered criterion.

**R1-b [MAJOR] The rule's "recovery" is near-tautological, and its E4 witness does not exercise recovery.**
The rule feedforwards the *current scheduled* `τ_ext,t` with zero latency (B.md:72). At the E4 edge (interval 40) its bias switches in the same interval that the load is removed. In the ideal model the net disturbance is cancelled, so no transient remains to recover from, apart from actuator-path lag and model error.
- The `post_load_recovery_count = 144` gate (B.md:183) therefore certifies that a privileged-feedforward controller does not move. It does not certify that replay contains representative release transients. This is weaker than the legacy counter's evident intent.
- The success window starts only 5 intervals after release (`[45,65)`), which is consistent with there being essentially no transient.
- *Fix:* either (i) delay the rule's knowledge of `τ_ext` by the same number of intervals the actor needs to detect release from proprioception (e.g. bias from `τ_ext,t−d`, with `d` pre-registered), or (ii) keep the instant feedforward but add a source-qualified **policy** recovery counter as the readiness-relevant one.

**R1-c [MAJOR] The actor imitation anchor supervises actions the actor cannot infer at the release edge (Issue #8 fix).**
The `0.10·E_rule,hold[(h − h_r)²]` term (B.md:134–140) includes the certified E4 `[15,65)` blocks, which contain the release edge. At intervals 40–41 the rule's action changes on privileged knowledge of the schedule, while the actor's `x137` still reflects the loaded state. The term regresses `h(x, z*)` toward a target that is a discontinuous function of unobserved state. The result is averaged, anticipatory, or lagged behaviour around release: exactly the regime where the brief says saturation stalls recovery. Steady-state E3 targets are inferable only if `x137` contains action/torque history, which B does not state and which cannot be checked here.
- *Fix:* exclude the k intervals after any load edge from the imitation term, or use a teacher whose inputs are restricted to `x137`-observable quantities for this term only.

**R1-d [MINOR] Gain/inertia specification is ambiguous for an "inertia-scaled" controller (Issue #2).**
`J_nom` is "the manifest's nominal joint inertia" (B.md:69). It is not stated whether this is per-configuration `J_nom(c)`, whether it includes reflected rotor inertia, or how it relates to the `J(q)` in the plant equation (B.md:24). With a global nominal value, the 36 geometry seeds get different closed-loop bandwidths and the "inertia-scaled" property is lost. Specify `J_nom(c)` and its provenance in the configuration hash.

**R1-e [MINOR] The saturation penalty and the imitation target conflict where the rule saturates.**
`h_r = atanh(clip(u, ±0.98))` gives |h_r| = 2.298 > h0 = 1.832. Wherever the rule is at |u| ≥ 0.95 (near the E4 edge, λ = 0.92 plus PD/integral), the two added terms pull in opposite directions. Their coefficients (0.01 and 0.10) are fixed with no reference to the scale of `F^T z`, so the effective strength of either term relative to the main actor objective is unknown. Pre-register a logged ratio of gradient norms, or justify the scale.

**R1-f [MINOR] E1/E2 positions are not feasibility-checked.**
The `|G| ≤ 0.75 S` preflight covers anchors only (B.md:27). E1 resets near the stops and E2 operates at 0.35R–0.65R, and neither is checked. If gravity at a stop exceeds S for some configuration, E1 288/288 fails deterministically. That failure is only discovered after paying for training. Extend the preflight to every scheduled reset and command position, with INFEASIBLE_CONFIG semantics.

**R1-g [MINOR] Issue #6: the sealed transform is fitted on untrained-actor data.**
The balanced moment pass happens once, after the *untrained* actor fills the policy partition under an identity transform (B.md:113, 123). The policy half (weight 2/3) of the sealed statistics therefore describes a random-policy occupancy distribution. Fields that are near-constant there (variance floor 1e-6) can produce very large normalized values later. Logging out-of-reference rates is not a mitigation. Pre-register a threshold on out-of-reference rate that marks the run as integrity-degraded, or seal from the rule partition plus a short rule-perturbed policy phase.

**R1-h [MINOR] "Code-level" fixes are specified algorithmically only.**
The rubric asks for code-level fixes, but no module, function or config key is named. B explains that the frozen files contain no code. This is acceptable, but the implementation binding must map each mechanism (controller enum, per-cell buffer, sealed normalizer, logit loss) to concrete code before sealing.

### R2 — 720-Cell Cross-Coverage Guarantee (25%)

**R2-a [CRITICAL] The guarantee is nominal: the replay is phase-locked across configurations, so within-cell sub-case diversity collapses.**
B loops "over sequence position first, then configuration ID" (B.md:19), so all 144 configurations advance through the per-cell ordinal `j` in lockstep. In E3/E4 the anchor index (`j mod 3`) and the λ tier (`⌊j/3⌋ mod 3`) are functions of `j` alone. The resident cell capacities are tiny compared with an episode: rule E3 34–35 rows (25 protected + ~10 FIFO), rule E4 68–69 (50 + ~19), policy E3 68–69, policy E4 136–137 (≈ 1.7 episodes). In practice each cell holds the most recent one or two episodes.
- At any instant the **entire** E3 policy partition across all 144 configurations contains essentially one (anchor, λ) sub-case, and the same holds for E4. The resident load distribution cycles through tiers over training rather than being mixed.
- `F`, `B` and the actor are trained on a nonstationary, single-tier curriculum. The checkpoint-20,000 evaluation then tests all 3 anchors × 3 tiers × 2 signs.
- The 720/720 quota check (B.md:190–192) passes the whole time, so the gate certifies counts that hide this collapse. Brief §1 asks for coverage that *guarantees closure of readiness gates*; row counts per (config, scene) do not provide this when the behaviour-defining sub-case is synchronized globally.
- Also in P0 (one cycle), E3 sees only λ = 0.25 (j = 0..2) and E4 sees only λ ∈ {0.25, 0.60}. λ = 0.92 first appears in rule cycle 3. B acknowledges this (B.md:92) but does not analyse what it implies for the sealed normalizer, which is fitted without the heaviest tier.
- *Fix:* desynchronize sub-case phase across configurations, e.g. anchor `(j + c) mod 3` and tier `(⌊j/3⌋ + ⌊c/3⌋) mod 3`, plus the sign alternation from R1-a. Every resident snapshot then mixes all 18 sub-cases across configurations. Add a gate on a resident `(scene, anchor, λ, σ)` marginal (e.g. ≥ 1 resident E3 and E4 block per sub-case across configurations), alongside the 720-cell array.

**R2-b [MAJOR] The witness counters can be met using only the easiest tier.**
A protected rule block is replaced "only by a complete newer block that passes the physical success predicate" (B.md:105). The witness predicate needs only `|τ_ext| ≥ 0.15 S` (B.md:183). Once a λ = 0.25 success is resident, it can stay indefinitely while λ = 0.92 attempts fail. `sustained_load_hold_count = 144` and `post_load_recovery_count = 144` then pass with no heavy-load success anywhere in replay, which is the regime Issue #8 targets.
- *Fix:* key per-configuration success bits by tier and require ≥1 resident success at λ = 0.92 per configuration. Alternatively, report tier-qualified counts and gate on the top tier.

**R2-c [MAJOR] Initialization can deadlock.**
Normalizer sealing requires "both initial partitions … full" (B.md:113), and full means every protected block has completed. A crash, nonfinite state or safety termination before the window is a failed attempt, and the block stays "reserved and invalid" (B.md:61, 107). The policy initialization cycle uses an *untrained* actor under E3 loads up to |A| = |G| + 0.25 S. Stop slams or safety terminations are plausible. If any of the 288 E3/E4 policy cells fails to produce a complete window, the partition never fills, the transform is never sealed, and learning never starts.
- B does not define "safety termination", and it gives no retry rule or bound for the initialization cycle.
- *Fix:* pre-register a bounded retry rule for initialization, e.g. repeat failed (c, scene) episodes up to N times, then BLOCKED. Also define safety-termination criteria so that stop contact alone does not abort an episode.

**R2-d [MINOR] Inconsistent load-magnitude thresholds.**
The §1 certificate requires a release magnitude ≥ 0.25 S (B.md:61). The §3 panel floor and the rule witness predicate use 0.15 S (B.md:171, 183). Panel E4 cases with 0.15 S ≤ |A| < 0.25 S would fail the §1 certificate if it is applied to evaluation episodes. State which certificate applies to panel episodes.

**R2-e [MINOR] Protected E4 blocks dominate E4 sampling.**
Sampling is uniform over valid cell rows (B.md:109), and the protected block takes 50 of 68–69 rule E4 rows. About 73% of rule E4 samples therefore come from `[15,65)` of a single episode. This may be intended, but it should be declared as part of the reference measure, since the normalizer uses the same measure.

### R3 — Memory & Compute Compliance (20%)

**R3-a [MAJOR] Compliance depends on an unverified, apparently fitted assumption.**
The dense layout misses the all-tensor cap by construction (see G8). The design meets the cap only if exactly the assumed **512** slots are immutable or constant-masked (B.md:150–154). B gives no provenance for the number 512 and says the baseline does not reveal the slot widths. B reports the dependency honestly, but this rubric dimension cannot be scored as satisfied. The fallback is BLOCKED; there is no alternative compliant design.
- *Request:* supply a second compliant fallback that is lossless and needs no slot assumption, e.g. deduplicate `x_next`/`p_next` against the next row of the same episode within a cell, using episode/t metadata the design already stores. Dense p alone is about 2.0 GB per copy. Storing `p_next` only for terminal rows saves roughly 1.99 GB, far more than the 512-slot trick (~403 MB).

**R3-b [MAJOR] The 350 MB budget for all models and optimizer state is unbudgeted.**
`F` takes 137 + 5,065 + 1 + 16 = 5,219 inputs. For illustration, with a 1,024-wide first layer, two online F heads, two target copies, gradients and two Adam moments, the **first layers alone** cost about 10 × 5.34 M × 4 B ≈ 214 MB. A 2,048-wide layer would exceed 350 MB before B, the actor or the deeper layers are counted. Widths live in `baseline/02`, which this reviewer cannot see. B should compute the parameter and optimizer bytes from the frozen architecture instead of asserting a cap.

**R3-c [MINOR] RSS headroom and CPU wall-clock are not estimated.**
4.694 GB RSS − 4.10 GB tensors leaves ≈ 594 MB for the Python/torch runtime, the simulator for 144 configurations, allocator fragmentation and streaming writers. That may be fine, but no estimate is given. On compute, one learning arm/seed executes ≈ 5.07 M training transitions plus ≈ 2.5 M evaluation transitions (7,776 × 80 × 4 checkpoints, plus E1/E2 panels), about 30 M physics substeps, plus 20,000 updates × 15 microbatches. Within 24 h that needs ≈ 88 control steps/s sustained, alongside training. Twelve arm-seeds run sequentially take up to ~12 days. B pre-registers INCOMPLETE semantics for this, which is good, but it should give a throughput estimate so the reader knows whether INCOMPLETE is the *expected* outcome on CPU.

### R4 — Spike Falsifiability (20%)

These points are covered in detail in §4. In summary:
- **[MAJOR]** Only the full bundle's sufficiency is falsifiable. LEGACY-RULE, POLICY-NORM and NO-LOGIT carry no directional, thresholded predictions, so the mechanism claims for Issues #2, #6 and #8 cannot be falsified by this spike.
- **[MAJOR]** The deterministic, identical train/eval schedules (fixed release at interval 40, the same anchors and λ) leave the panel unable to detect timing memorization.
- **[MINOR]** Some gates are redundant or tautological, as described in §4.

---

## 3. Audit of Rejected Alternative & Necessity Claim (`C-B02-B-01`)

**3.1 The claim is correct but trivially narrow.**
The proof is valid. `[[k,0],[0,k]]` and `[[k/2,k/2],[k/2,k/2]]` share row and column marginals (k,k), and embedding them in a 144×5 matrix with identical remaining entries keeps the marginals equal. Any verifier that is a function of the marginals alone cannot be both sound and complete. Grade 1 / Candidate is the right status. The claim is a standard fact (marginals do not determine a contingency table) and could be independently verified quickly, so I see no obstacle to promoting it **as stated**.

**3.2 The claim does not support the rejection it appears beside.**
`C-B02-B-01` concludes that the *verifier* needs joint information. It says nothing about whether the *collector* must be deterministic, or whether the buffer must use fixed per-cell partitions. A deficit-weighted stochastic collector with a global reservoir can still maintain and expose the full 144×5 joint count array. Nothing in the alternative forces a marginal-only verifier. Read as an argument against the alternative, the claim attacks a straw man. B half-concedes this (B.md:213, 227), but the placement in §4/§5 still suggests more support than the claim provides. Recommend stating plainly: "C-B02-B-01 supports the joint-array gate (Issue #3) for any collector; it is not evidence for deterministic scheduling."

**3.3 The rejection arguments target a weaker version of the alternative.**
- *"`(1 − p_cell)^n > 0` under independent draws"* (B.md:213). A *deficit-weighted* collector is by definition not independent. It raises the sampling probability of under-filled cells, and with a hard per-cell minimum it gives deterministic coverage. The argument rejects i.i.d. sampling, not the alternative as named.
- *"Reservoir eviction can remove the only release boundary."* That is solved by window protection, which is orthogonal to stochastic versus deterministic collection. B concedes that a deficit scheduler with hard minima and protection "supplies the functional mechanisms adopted here".
- The surviving justification is engineering simplicity for a finite contract. That is legitimate, but it is a preference, not a necessity.

**3.4 B never weighs the costs of determinism.**
B does not count any advantage the alternative has over the adopted design:
1. **Phase-locked sub-case collapse** (R2-a). A stochastic or deficit-weighted collector naturally mixes anchors and tiers across configurations at every instant.
2. **Timing regularity.** Load onset (interval 10/15) and release (interval 40, exactly 30 intervals after full load) never vary. If `x137` history spans enough intervals, an actor can learn release *anticipation* keyed to time-since-onset. The deterministic panel rewards this and deployment does not provide it. Randomized release times within pre-registered bounds, with ≥25 hold and ≥20 recovery intervals still guaranteed, would keep the brief's guarantee and remove the regularity.
3. **Sign coverage** (R1-a) comes from the same deterministic choice rule.

A fair rejection must show that the adopted design beats a *deficit-weighted collector with hard per-cell minima, window protection and randomized in-bounds timing*. That hybrid is the strongest form of the alternative, and B does not evaluate it.

**3.5 The adaptive-normalizer rejection is reasonable.**
The coordinate-consistency cost of adaptive moments across nonlinear encoders, targets and optimizer state is real, and B correctly avoids calling the alternative wrong. The untrained-policy sealing problem (R1-g) means the sealed transform's advantage is smaller than presented.

**3.6 The operational test and falsifier work as a unit test only.**
"Feed the verifier the paired matrices with k = 100" is a correctness test for the implemented verifier, which is useful. It is not an empirical test of the claim, which is mathematical. The "eviction of a protected cell's last valid row" re-run is a good addition. The stated falsifier is acceptable.

**3.7 `C-B02-B-02` (not the audited claim; noted only).**
The bound `|dQ/dh| ≤ M sech²h ≤ 4M e^{−2|h|}` is correct. Its premises exclude other gradient paths, so it does not imply that the specific logit penalty is necessary. B states this correctly.

---

## 4. Spike Protocol Critique

**Strengths.**
- Success is decided at checkpoint 20,000, so the best intermediate checkpoint cannot be cherry-picked.
- One numerical attempt per arm/seed; infrastructure repair cannot erase a failure.
- Stage A has fault injections: missing cell with unchanged marginals, corrupted source tag, stale normalizer, acausal `p`, interrupted E4.
- Structural pass / control fail is reported separately from full pass.
- INCOMPLETE/BLOCKED semantics are explicit for CPU runs.
- All three seeds must pass.
- Output artifacts and the machine-computed `VERDICT.json` are named.

These features make the FULL-sufficiency hypothesis clearly falsifiable.

**S1 [MAJOR] The ablations have no pre-registered predictions.**
LEGACY-RULE, POLICY-NORM and NO-LOGIT "measure" effects but state no direction or threshold (B.md:258–262, 284). As a result:
- **POLICY-NORM's** "intended integrity gate fails" is true by construction (`normalizer_version_ok`) and is not an empirical result.
- **SHORT-LOAD** is a validator unit test labelled as an arm.
- If FULL fails, nothing in the protocol localizes which mechanism failed.

*Request:* pre-register at least one directional, thresholded, paired-seed prediction per ablation. Examples:
- NO-LOGIT: `Pr(|a| > 0.99)` on λ = 0.92 E3 late windows exceeds FULL by ≥ X in ≥ 2/3 seeds, *or* the logit term is declared unnecessary.
- LEGACY-RULE: rule-panel E3/E4 witness count < 144.
- POLICY-NORM: actor static-panel worst-case RMSE exceeds FULL's.

Then state in advance what each outcome implies for the corresponding Issue fix.

**S2 [MAJOR] Training and evaluation are too identical to detect memorization.**
The static panel uses the same anchors, the same λ tiers and the exact §1 timing used in training. Only the sign and the static E0/E3/E4 reference differ, and the sign is OOD by accident (R1-a). The protocol cannot tell real holding/recovery from memorized timing-keyed behaviour (§3.4 item 2). *Request:* add a pre-registered held-out panel, reported separately or gated, with release shifted by ±5 to 10 intervals, an intermediate λ (e.g. 0.75), and anchors off the training set (feasible grid points not selected for training).

**S3 [MAJOR] Several coverage conjuncts can pass trivially, so `coverage_ready = true` overstates readiness.**
Combining R1-b, R2-a and R2-b, `anchors_ok` can be met by λ = 0.25 rule witnesses under zero-latency feedforward, while the resident replay holds a single tier. The pre-registered predicate is exact, which is good, but it is weaker than its name. Tier-qualified and source-qualified counts should enter `coverage_ready`.

**S4 [MINOR] Redundant and duplicated statistics.**
Because every individual case must be strictly < 0.35 rad/s, the per-(config, scene), per-scene and full aggregates can never be the binding gate (if every case MSE < 0.1225, every equally weighted mean is too). E0 panel cases are 6× duplicates of 432 distinct deterministic conditions (B.md:171), which inflates E0 weight in the published aggregate. Report deduplicated E0 counts.

**S5 [MINOR] No anchor to the baseline failure.**
No arm reruns the V3-baseline configuration on the *new* static panel. The 5.89–13.88 rad/s figure was measured on the moving-target panel (Issue #5), so it is not comparable. A baseline-on-new-panel row would show how much of any improvement comes from fixing the panel rather than from the mechanisms.

**S6 [MINOR] Determinism criterion.**
`resume_diff_norm = 0.0` on CPU requires pinned BLAS/OpenMP thread counts and deterministic reduction order. Pre-register those settings in the manifest, or a failure will be logged as numerical when it is environmental.

**S7 [MINOR] Expected outcome on CPU.**
Given R3-c, the protocol should state whether a 24 h CPU run is *expected* to complete 20,000 updates plus 4 × 7,776-episode panels. If not, the registered outcome is predictably INCOMPLETE, and the spike's falsifying power on the actor gates is nil until accelerated hardware is available. Consider pre-registering a reduced evaluation cadence (e.g. full panel only at 20,000, a fixed sub-panel at 5,000/10,000) to protect the wall-clock budget without weakening the final gate.

**S8 [MINOR] The initialization retry rule is missing** (see R2-c). Without it, a single initialization failure in the untrained-actor cycle makes the whole arm BLOCKED or deadlocked. That is indistinguishable in the verdict from a real design failure unless reason codes separate them. Add a dedicated reason code.

---

*End of Blind Review A on Proposal B.*
