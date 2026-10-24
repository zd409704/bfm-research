# B05 Order-Swapped Adjudication (Presentation Order 2: P and Q reversed)

Adjudicator: Sonnet 5.5, order-swapped pass. Methodology v1.0 §4 Step 4 and Appendix B.9.
Inputs read: Charter, `brief.md`, `order2_P.md`, `order2_Q.md`, `review-A-on-B.md` (the critique of P), `review-B-on-A.md` (the critique of Q), and `spikes/B05-SPIKE/VERDICT.json`.
Not read: `adjudication-agy-order1.md`, `baseline/*`, `synthesis/*`, and the Appendix B text itself.
Identity note: I judge P and Q only by their content. The scores below follow the `brief.md` §4 rubric (35/25/20/20).
The Charter §4 rubric (25 each) is used only to check the gates.
The `VERDICT.json` file reports PASS in 0.009 s. That timing fits logic-only fixtures. It is not evidence of MuJoCo stepping.

## 1. Eligibility Gate Check

| Gate | P (Order 2) | Q (Order 2) |
|---|---|---|
| §2.1 No BC or tracking fallback | PASS. RMSE is rejected, and tracking PPO appears only as a comparator. | PASS. RMSE is demoted to a novelty diagnostic. The actor objective is unspecified, which is a gap but not a violation. |
| §2.2 Behavior-z vs z_update separation | PASS. The 50/50 relabel is specified, z_update never overwrites behavior_z, and Q trains on z_actual. | PARTIAL. behavior_z and z_actual are preserved, but there is no `sample_mixed_z` algorithm. FB uses a bare z_update symbol. |
| §2.3 B input is single-frame 229-d motion only | PASS. | PASS, but only by a dimension statement. Review B's concern about substitution is noted. |
| §2.4 Credible penetration committed; invalid rejected | Mostly PASS. The terminal row has Φ_next=0 and m_next is retained. It adds heuristic invalid triggers (`J>0.5 m`, `V>100 rad/s`, `ncon≥nconmax`) beyond the charter's "verified divergence" and "overflow with lost contacts". | Mostly PASS, with the same J and V heuristics and the same `ncon≥nconmax` rule. It also uses MuJoCo warning counters (`BADQACC`, `CONTACTFULL`) as verified witnesses, which is closer to the charter. |
| §2.5 No unproven claims | PASS. | PASS. |
| Brief §2 (0.03 m kept, no denominator shrink, keep checking after penetration, no zero-fill) | PASS. | PASS. A void panel is re-run on the same seeds. |
| Brief §2 "no forgetting >10 pp" | PASS. Any single drop >10 pp holds the unlock. | FAIL-risk. Forgetting is "confirmed" only after two consecutive drops. A pass, then a frontier pass with a first-panel drop, can still unlock. |

Gate verdict: P is eligible with conditions (the Charter §2.4 heuristics must be demoted to `suspect`). Q is eligible only with conditions, and has two defects: the missing UFO algorithm and the delayed hold rule.
The Charter §2.4 heuristic problem is shared by both candidates, so it does not separate them.

## 2. Scores (brief.md rubric, 100 points)

### Candidate P (Order 2)

| Row | Max | Score | Justification |
|---|---:|---:|---|
| Substep Priority & Replay Isolation | 35 | 28 | The latch-max ordering, four mandatory integrations before invalid, the final audit, and the induction proof are correct. The deferred-commit transaction touches no replay, BN, Gram tracker, counter, or quota debit. Quarantine is separate, and attempted physics is ledgered. The failure row is complete (Φ=0, measured m_next, c=0). Deductions: the heuristic invalid triggers (Review O1); the vectorized-batch commit unit is unspecified, so the fate of the other 4095 envs is undefined (O2); the timestamp tolerance is unspecified (O3). |
| UFO Relabel & BN Order Fidelity | 25 | 20 | It specifies BN updated once on `(o_t,m_t)`, once on `(o_{t+1},m_{t+1})`, then frozen. z_update is a 50/50 mix of projected Gaussian and online `B(m_next[perm])` on S^255(16). Expert encoding is eval/no_grad and never updates BN. The behavior_z and z_actual separation is explicit. Deductions: no stop-gradient boundary on the B-encoded latent, and the split type (exact half or Bernoulli) is unstated (O6). There is no CandidateProvider assertion. |
| Curriculum & Quota Completeness | 20 | 16 | It has credits C_h and reservations R_h with 0≤R_h≤C_h. It replenishes atomically when ΣC=0 and wakes paused workers, which rules out an all-paused deadlock. Group allocation is conserved exactly. The 2/5/7 vectors match the spike. Migration happens only on natural resets. The two-panel Wilson gate and the >0.10 hold are explicit, and 0.10 exactly is not a trigger. Deductions: references re-based at each unlock allow cumulative drift (O8). The Stage 3 table could be misread as a training vector (O9). |
| Verification Suite Executability | 20 | 16 | It covers all three R2.1 §7 targets: credible failure commit; corruption dominance including NaN at substep 3, overflow at substep 4, and equality boundaries; and panel continuation with denominator 100. It adds 78/79 and 10/11-point boundary tests, a bounded real-backend run (seeds 101–104, ≤600 controls), six-optimizer gradients, and resume parity with a 10⁻⁶ tolerance. Deductions: no engineered real collision witness; no false-halt negative control; resume over 32 controls will not cross a macro, epoch, or evaluation boundary; the optimizers are not enumerated. |
| **Total** | 100 | **80** | |

### Candidate Q (Order 2)

| Row | Max | Score | Justification |
|---|---:|---:|---|
| Substep Priority & Replay Isolation | 35 | 29 | It gives a clean closed form for ℓ* and a proof by induction. It adds warning-counter witnesses (`BADQACC`, `CONTACTFULL`). It specifies all-or-nothing rejection of the 4096-env batch. The bitwise-unchanged list covers replay, normalizers, the Gram tracker, S, and the ledgers. The FB and macro failure targets are given. It has an exhaustive 2048-pattern logic check. Deductions: the J and V heuristics (Review B); penetration at the final check is not included in the final rule; BN buffers, RNG, and pending macros are not under prepare/commit ownership; discarding valid siblings is not justified. |
| UFO Relabel & BN Order Fidelity | 25 | 12 | Only the normalizer update order is stated: once on `(o_t,m_t)` and once on `(o_{t+1}^{pre},m_{t+1}^{pre})`. There is no 50/50 sphere/online-B mixture, no frozen-BN relabel, no radius √d_z, and no expert no-BN rule. There is no stop-gradient contract and no CandidateProvider or production-path wiring. The "normalizer count by 1" in Test 1 contradicts the two updates in §1.3. This is the weakest row. |
| Curriculum & Quota Completeness | 20 | 12 | It has integer Split conservation, a seven-stage table that includes the k=3,4,6 vectors, and a deficit ledger with ΣD≡0. The Wilson gate is correct. Deductions: the ledger conserves only the total, so simultaneous resets can pick the same argmax and starvation is not bounded; there are no reservations or debits; the S counter conflates rows and vector steps; the hold rule admits an unlock despite regression; resume hash omits per-env heights and outstanding state. Void-panel handling (same-seed re-run) is good. |
| Verification Suite Executability | 20 | 10 | Tests 1 and 2 are detailed. Test 2 has three corruption fixtures and the exhaustive pattern check. Test 3 has quotas, a 10⁴-epoch ledger run, and panel sequences. Deductions: the panel-continuation denominator test is missing. Resume parity is hash equality only, with no actual six-optimizer update or resumed-versus-uninterrupted comparison. The capsule fallback cannot certify the 229-d production runner. Fixtures are not exactly reproducible. There is no train.py→runner.run→Trainer exercise. |
| **Total** | 100 | **63** | |

Score margin: P leads by 17 points. Q's only row lead is Substep Priority, at +1.

## 3. Principle Claim Adjudication (Appendix B.9)

I did not have the Appendix B text. Grades are judged against the necessity-grade definitions as the candidates state them, and are therefore provisional.

| Claim | Candidate | Ruling | Reason |
|---|---|---|---|
| C-B05-CAND-01 (P): deferred commit | P | ACCEPT as Grade 1 conditional, reworded | The premises are stated and there is an exact-rollback carve-out. It holds by construction, so it is a lemma, not an empirical result. The witness (a commit at j=2) is vacuous, because `o_{t+1}` does not exist before j=4. Restate it with the commit-after-integration, before-final-audit trace. Name the irreversible mutations (BN momentum, ring overwrite). The hash test is a conformance test. |
| C-B05-CAND-02 (P): preserve failure information | P | ACCEPT as Grade 1 conditional | The two-plant observational-equivalence argument is a valid identification counterexample. The premises (replay-only estimator, no external failure model) are explicit. The claim does not say every alternative is impossible. The charter already mandates retention, so the claim adds little new separation. |
| C-B05-CAND-03 (P): boundary coverage | P | ACCEPT as Grade 2 candidate only | It is scoped to the experimental family and its falsifier is the censoring arm passing the gates. It remains unproven until the multi-seed GPU run. |
| C-B05-CAND-01 (Q): commit credible failures | Q | DOWNGRADE to Grade 2, or restrict to a fixed-policy finite MDP | Review B's point is sound. P1–P3 do not exclude function approximation, a changing planner, a recursive fixed point, or an independent failure estimator. The falsifiers are not negations of the analytic claim: a CI containing 0 may reflect low power, and equal penetration rates do not contradict critic bias. The bias identity itself is correct. |
| C-B05-CAND-02 (Q): pre-statistic rejection | Q | ACCEPT in narrowed form (Grade 1) | The EMA with a single non-finite input argument holds under IEEE-754. The conclusion overreaches. Only rejection before any statistic is necessary, not atomic rejection of the whole batch. Per-env rejection satisfies the premises. The charter mandates this behavior already. |

## 4. Disposition

**Recommend: P**

**Alternate: Q.** Use Q's classifier and quarantine text as the reference if P's state machine is challenged. Q is not suitable as the primary because its UFO/BN, verification, and curriculum rows are materially weaker.

**Mandatory Merge items**
1. From Q into P: add the MuJoCo warning counters (`BADQACC`, `CONTACTFULL`) as the verified-divergence and lost-contact witnesses. Demote the J, V, and `ncon≥nconmax` triggers to a `suspect` state that is verified before it is classified as invalid.
2. From Q into P: state the batch commit unit. The default is whole-batch rejection with resume from the last committed checkpoint. Add explicit prepare/commit ownership for BN buffers, RNG, and pending macro accumulators.
3. From Q into P: add the explicit final-state penetration term `P_F` and the exhaustive predicate-pattern check (2048 patterns) against the closed form.
4. From Q into P: add the A3 rationale for why RMSE is neither necessary nor sufficient, and keep RMSE as a novelty diagnostic only.
5. Fix in P: add a stop-gradient contract for the B-encoded z_update. Specify the exact or Bernoulli split, in-batch `perm`, and eval-mode BN after the two updates. Add an executable UFO/BN fixture (BN changes exactly twice in order, expert encoding leaves BN bit-identical, ‖z‖=16, zero B gradient through z).
6. Fix in P: keep a run-wide low-height reference or require the Wilson gate on low heights at every panel (Review O8). Use an evaluation-only table for 0.80 m.
7. Fix in P: add a deterministic real-backend collision fixture, a negative-control panel of valid hard falls (zero invalids), resume points before a macro boundary, an epoch replenishment, and an `S=100000j` evaluation split, and a named list of the six optimizers.
8. Claims: apply the rulings in §3. Do not carry Q's CAND-01 forward as Grade 1.

## 5. Confounds

- **Order and position effects.** This is the order-swapped pass, with the same content under swapped labels. The mapping used here is P = Primary Author B's file and Q = Primary Author A's file. A first-order disagreement would indicate position bias. I did not read it.
- **Review asymmetry.** The critique of Q tags more items `[CRITICAL]` and uses the Charter §4 rubric framing. The critique of P is more calibrated and cites line numbers. Severity labels are not comparable across the two reviews, so I scored from the candidate text and used the reviews only to find defects I then confirmed myself.
- **Length and density.** P is more complete on spike and curriculum detail. Q is more complete on algebra and alternatives. The rubric rewards the former, so P's lead partly reflects rubric alignment, not overall quality.
- **Scope creep.** Both include an acceleration ledger outside B05's three deliverables (Review O11). I did not score it.
- **Evidence limits.** The spike is logic-only (0.009 s) and confirms only the quotas 2/5/7 and Wilson 78/79, which both candidates match. Neither review read the baselines, so baseline/05 and B01 alignment is UNVERIFIED for both. I did not read Appendix B, so the claim grades are provisional.
- **Shared defect.** Both share the heuristic J and V triggers. The Charter §2.4 conformance of both is therefore conditional, and the merge items above are needed regardless of the recommendation.
