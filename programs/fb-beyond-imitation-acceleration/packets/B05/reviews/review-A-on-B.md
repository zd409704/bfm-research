# Blind Review A on Proposal B (Packet B05)

Reviewer: Blind Reviewer A. Inputs read: `PROGRAM_CHARTER.md`, `packets/B05/brief.md`, `packets/B05/proposals/B.md`, `packets/B05/spikes/B05-SPIKE/VERDICT.json`.
I did not read `baseline/*`, `synthesis/*`, or any other review/draft. Where B cites those sources, alignment is marked UNVERIFIED rather than assumed.
Severity scale: `[CRITICAL]` blocks spike lock; `[MAJOR]` must be fixed before lock; `[MINOR]` is a clarification.

Overall: B is a strong, mostly charter-faithful proposal. The latch-max priority machine, the transactional commit, the quota conservation proof and the Wilson arithmetic are all correct. It also avoids overclaiming.
The main defects are: (i) the `invalid` predicate is broader than the charter's definition, which can halt runs on valid falls; (ii) the commit semantics for vectorized batches are unspecified; (iii) the UFO/BN fidelity row has no stop-gradient or test fixture; (iv) the necessity claim C-B05-B-01 is close to tautological.

## 1. Gate & Hard-Constraint Audit

| Constraint (source) | Status | Evidence / defect |
|---|---|---|
| No BC / tracking-penalty fallback (Charter §2.1) | PASS | No action-MSE or pose-tracking reward. Tracking PPO appears only as an external comparator (l.149), and pose RMSE is explicitly rejected (l.147, l.188). |
| Behavior-z vs z_update separation (Charter §2.2) | PASS | l.77–78: z_update never overwrites behavior_z / z_actual; Q trains on z_actual (l.64–65). |
| Single-frame 229-d motion-only B input (Charter §2.3) | PASS | l.61, l.77: raw `m ∈ R^229`. No obstacle height, phase or index reaches B. |
| Credible penetration committed as terminal, Φ_next=0 (Charter §2.4) | PASS | Table l.53–59, l.63–67. |
| Invalid limited to NaN/Inf, overflow *with lost contacts*, corrupt schema/timing, *verified* divergence (Charter §2.4) | **PARTIAL VIOLATION** | l.27–29 adds `ncon ≥ nconmax` "even before dropped-contact evidence", `J_j > 0.50 m` and `V_j > 100 rad/s`. These are heuristic triggers, not verified divergence. See O1. |
| 0.03 m threshold not relaxed; no seed deletion or denominator shrink (Brief §2) | PASS | Strict `>` at l.31; l.130–132 retain denominators and label unexecuted trials. |
| Keep checking substeps after penetration; invalid overrides (Brief §2) | PASS | l.38, l.50–51. |
| No zero-filled terminal obs; no counter advance on invalid (Brief §2) | PASS | l.66, l.73. |
| No unproven competence/speedup claims (Charter §2.5) | PASS | l.5–6, l.189, l.236. The VERDICT.json (0.009 s elapsed, contract-only) is characterized correctly at l.235. |
| Baseline/05 and B01 alignment (Charter rubric row 2) | UNVERIFIED | B cites B01 for the Gram solve and terminal handling (l.79, l.156). This reviewer cannot confirm the citation. |

Gate verdict: **conditional pass**. The only hard-constraint issue is O1. It is fixable by demoting the heuristic triggers to "suspect" status pending verification.

## 2. Rubric-Keyed Technical Objections

### Row 1 — Substep Priority & Replay Isolation Rigor (35%)
- **O1 [MAJOR] The invalid set exceeds the charter and can halt runs on valid falls.** The rubric requires "zero possibility of … valid falls halting runs".
  - The charter defines overflow as invalid only *with lost contacts*. B's `ncon_j ≥ nconmax` therefore halts on a legitimate pile-up that exactly fills capacity.
  - `V_j > 100 rad/s` is an uncalibrated constant. Small-inertia distal joints (ankle roll, wrist) can transiently exceed it under hard box impacts without any solver fault.
  - Fix: route these predicates to a `suspect` state that triggers a verification re-simulation (e.g., replay from `x_{j-1}` at δ/4, or a solver-residual/warning-counter check). Classify as invalid only if verification fails. Otherwise these are not "verified divergence".
  - For MuJoCo, the backend contact-full warning counter is the natural lost-contact witness, not the `ncon` count.
- **O2 [MAJOR] Vectorized-batch atomicity is unspecified.** B halts "the entire affected training run" on invalid (l.73) but never says what happens to the other 4095 environments' rows from the *same* vector step.
  - Those rows are valid. If they are committed, the halt checkpoint is mid-step. If they are dropped, quota reservations and macro states for 4095 envs must also roll back.
  - Fix: state the commit unit (per-env transaction vs whole vector step) and the restart semantics after inspection. Also say whether a resumed run replays the step or skips it.
- **O3 [MINOR] Timestamp predicate `t_j = t_0 + jδ`** (l.24) needs an explicit float tolerance or an integer-tick representation. Otherwise exact float comparison can produce spurious `¬g_j` invalids, which is another false-halt path.
- **O4 [MINOR] Terminal-state choice.** When penetration occurs at j=2, B stores `x_4` (two substeps later) as `m_next`. This is defensible as the "genuine pre-reset final state", but the FB/Gram consumers should be told explicitly that the terminal frame is post-penetration plus residual integration.
- **O5 [MINOR] Overloaded "first-success reward to zero" clause** (l.66). It is ambiguous whether this applies only on failure rows or also caps a success row's reward. Split it into a separate sentence.

### Row 2 — UFO Relabel & BN Order Fidelity (25%)
- **O6 [MAJOR] No stop-gradient boundary for the B-encoded half of z_update** (l.77). The charter rubric requires explicit stop-gradient boundaries.
  - It is unstated whether `B(m_next[perm])` is detached before entering F/actor losses. If it is not detached, the FB loss back-propagates into B through the latent as well as through the target features.
  - Also unspecified: whether the 50/50 split is an exact half-batch or a per-sample Bernoulli draw; whether `perm` is a within-batch permutation; and whether encoding runs in eval-mode BN after the two updates (l.76 says "freeze", l.78 only covers expert encoding).
  - "Exact match to `sample_mixed_z`" cannot be judged without these four facts.
- **O7 [MINOR] BN-update pairing.** "Once on `(o_t, m_t)` and once on `(o_{t+1}, m_{t+1})`" should state that each pair is a single forward pass updating both the F-side observation BN and the B-side motion BN. It should also state that the two passes are sequential in that order, so momentum ordering is deterministic.

### Row 3 — Curriculum & Quota State Completeness (20%)
- Arithmetic verified: `819 = 409+410`, `1229 = 614+615 = 3·307+308 = 245+4·246`, `L=3 → (409,410,3277)`. Each row sums to 4096 and matches VERDICT.json.
- `L(78,100)=0.689296`, `L(79,100)=0.700200` with two-sided z=1.95996 are correct.
- The credit/reservation invariant with all-zero replenishment (l.116–120) prevents the paused-deadlock case as long as every height with `C_h > 0` has at least one assigned worker. That condition is guaranteed by "activate credits only after occupancy installed" (l.113).
- **O8 [MAJOR] Cumulative-forgetting loophole.** Low-height references are re-based at each unlock (l.135). Successive stages can therefore each lose 9.9 pp without triggering a hold (e.g., 0.98 → 0.89 → 0.80 …).
  - Whether the per-panel `x ≥ 79` gate also applies to 0.10/0.20 m is ambiguous at l.136 ("any current height gate fails"). If it does, the floor is 0.79; if not, there is no floor.
  - Fix: keep a run-wide max reference, or state that low heights must pass the Wilson gate on every panel.
- **O9 [MINOR] The Stage 3 "pool layout" assigns 2048 workers to the held-out 0.80 m height** using the *training* allocator (l.106). This invites accidental training at 0.80 m. Use a separate evaluation-only allocator or table so no training credit vector can ever contain 0.80.
- **O10 [MINOR] Mid-epoch evaluation.** 100,000 is not a multiple of 4096, so every evaluation suspends mid-epoch. B checkpoints credits (l.139) but should state that the stage change and credit activation wait for epoch completion *after* evaluation, which l.113 implies.

### Row 4 — Verification Suite Executability (20%)
- Covered in §4 below. In brief: the three R2.1 §7 tests are present, but resume parity is too short and the UFO/BN row has no fixture.

### Scope
- **O11 [MINOR]** §2 lines 151–174 (acceleration factorial I1–I3, GPU ledger) are outside B05's three deliverables. They are well constructed, but they dilute the packet and should be deferred to the acceleration packet.

## 3. Audit of Rejected Alternative & Necessity Claim

**Rejected alternative (discard all `d > 0.03 m` rows).** The one-step bias derivation is correct: `Q_keep − Q = p(r+M) > 0`. The observational-equivalence argument (two plants, identical retained data) is a valid identification counterexample.
However, the alternative is **weakly non-trivial**. Charter §2.4 already forbids it, so rejecting it does not separate B from any admissible competitor.
Admissible design choices the analysis does not address:
- (a) halt-on-penetration, i.e. the `R2_FINAL` status quo the brief is replacing;
- (b) eager per-substep commit with an undo journal vs deferred commit;
- (c) penetration as a non-terminal penalty with continued integration.

Option (b) is partially covered by C-B05-B-01. (a) and (c) are not discussed.

**C-B05-B-01 (deferred commit), Appendix-B fit:**
- *Premises* are stated, which is good. But "later substeps can invalidate earlier finite states" is a **stipulation of the brief**, not a physical fact: a NaN at j=3 does not make `x_2` corrupt. The necessity is therefore derived from a policy rule, and the claim should say "given the brief's whole-transition rejection rule".
- *Witness is vacuous.* No reasonable design commits a control row at j=2, because `o_{t+1}` does not exist until j=4. The non-trivial failure is a commit after integration but *before the final audit* (schema or reward-finiteness failure detected post-j=4). The witness should be that trace.
- *Irreversibility premise.* Replay append is reversible by cursor rollback *unless* the ring buffer has overwritten its oldest row. BN momentum updates are lossy. Naming these concrete irreversible mutations would make the premise checkable.
- *Falsifiability.* The falsifier ("irreversible commit before audit yet zero contamination for every trace") contradicts the premises, and the rollback carve-out (l.199) closes the remaining gap. The claim is true by construction, which is acceptable for Grade 1 logical necessity but gives no empirical content.
  - The operational test (hash comparison) tests the *implementation*, not the claim. Relabel it as a conformance test and keep the claim as a lemma.
- C-B05-B-02 is the standard survivorship-bias identification result and is sound. C-B05-B-03 is properly scoped as within-family empirical evidence.

## 4. Spike Protocol Critique

1. **[MAJOR] Real collision witness is not engineered.** Seeds 101–104 with ≤600 controls each under an untrained policy may never produce `d > 0.03 m`, and B only downgrades this to NOT ESTABLISHED (l.230).
   - Add a deterministic real-backend fixture: drop the robot onto the box edge at a preregistered velocity, or command a pre-specified high-gain action into the box. Measure the real penetration profile so Test 1 has backend evidence and not just the adapter-injected `d = (0.01, 0.031, 0.02, 0.01)` trace.
2. **[MAJOR] No false-halt control.** Every invalid test checks *detection*; none checks that *valid* violent falls do *not* trigger `I_j`.
   - Add a negative-control panel of scripted hard falls and impacts. Report the distribution of `V_j`, `J_j`, `ncon_j/nconmax` and the solver residual, and require zero invalids. This calibrates the O1 thresholds against the rubric's "valid falls halting runs" criterion.
3. **[MAJOR] Missing dominance cases from Deliverable 1.**
   - The matrix tests invalid over penetration/success, but not *severe_penetration over success* (success latched at j=1, penetration at j=3) or penetration and timeout in the same control step.
   - It also lacks a fault at j=1 with no prior penetration, and penetration first occurring at j=4 followed by a final-audit-only fault.
   - Enumerate the full `(first-penetration ∈ {1..4, none}) × (fault ∈ {1..4, final, none}) × (provisional success/timeout)` grid, as the C-B05-B-01 operational test itself promises.
4. **[MAJOR] UFO/BN fidelity has no fixture.** "Forbidden-gradient/BN/source-label assertions" (l.231) is not a test. Required assertions:
   - BN running stats change exactly twice per update, in order `(o_t, m_t)` then `(o_{t+1}, m_{t+1})`;
   - expert encoding leaves BN bit-identical;
   - `‖z_update‖ = 16 ± ε` and the mixture count matches the spec;
   - B receives zero gradient through the z path (O6);
   - stored `behavior_z` hashes are unchanged after updates.
5. **[MAJOR] Resume parity is too shallow.** 32 controls from a drained barrier will likely not cross a macro boundary (`k < K` with live RNN state), a quota-epoch replenishment, an `S = 100000j` evaluation split, or a migration in progress. Each of these is a stateful transition the brief asks to be hash-verified. Add resume points immediately before each one.
6. **[MINOR] Test 2 isolation scope.** Assertions list replay, normalizers, credits and counters, but omit the Gram tracker, task-macro buffer, reservation release (`R_h` back to its prior value) and RNG stream position. Include all of them in the pre/post hash.
7. **[MINOR] Quota fixtures.** Assert `L = 4` and `L = 6` vectors (the single-height unlock path at l.87 passes through them), O2 batch-atomicity, and a stage change triggered mid-episode with lazy migration.
8. **[MINOR] Six optimizers are not enumerated.** Name them (e.g., F, B, actor, Q, planner, plus the sixth) so "all six states" is checkable.
9. **Threshold note.** `J_j > 0.50 m` per 5 ms (100 m/s) is so loose it effectively never fires except on blow-ups. It is harmless but weak as a divergence detector. Pair it with the solver-residual check from O1 rather than relying on it.

Recommendation: **Revise and resubmit, minor-to-moderate.** Fix O1, O2, O6, O8 and spike items 1–5 before the spike is locked. The core state machine and quota accounting are sound and can be reused as-is.
