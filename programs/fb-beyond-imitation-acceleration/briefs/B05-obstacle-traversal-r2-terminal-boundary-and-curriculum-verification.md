# Brief B05: Autonomous 3D Obstacle Traversal R2.1 Terminal Boundary (`severe_penetration` vs `invalid`) and Multi-Height Curriculum Verification

**Packet ID**: `B05`
**Status**: `READY_NOT_STARTED`
**Baseline References**: `baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md`

---

## 1. Problem Statement

The R2.1 obstacle-traversal implementation plan (`baseline/05`) identifies two critical engineering and algorithmic requirements before full-scale GPU joint training can proceed:
1. **Terminal-Boundary Disambiguation (`severe_penetration` vs `invalid`)**: In earlier runs (`R2_FINAL`), runtime contact penetration depth $> 0.03\text{ m}$ was treated as an unrecoverable `InvalidPhysicsError`, halting evaluation panels at step 9 during exploratory falls/collisions without logging whether the event was a physically valid hard impact or numerical solver divergence. R2.1 mandates separating **credible task failure (`severe_penetration`)** from **data corruption (`invalid`)** across all 4 physics substeps (`4 x 0.005 s = 0.02 s`).
2. **Formal Runner Unification & Active Curriculum Unlock**: The production entry point (`train.py -> runner.run -> Trainer`) must wire the unfiltered `[T, 229]` `CandidateProvider`, the restored UFO `sample_mixed_z` update (`m_current`/`m_next` BN ordering), and the active multi-height curriculum controller (`PoolQuotaSchedule` credit replenishment + `95%` Wilson lower bound $\ge 0.70$ unlock across two consecutive `100%`-planner panels without $> 10$ percentage point low-height forgetting).

**Core Question**: How do we formally verify the state-machine invariants, substep priority rules, replay/normalizer isolation, and curriculum credit state transitions of the R2.1 specification so that neither silent numerical corruption nor false training halts can occur during long-horizon GPU runs?

---

## 2. Hard Constraints & Non-Goals

- Must not relax the $0.03\text{ m}$ penetration threshold, delete failure seeds, or shrink evaluation panel denominators.
- Must not stop checking remaining substeps when a substep exceeds $0.03\text{ m}$: if a subsequent substep or final state in the same $0.02\text{ s}$ control step exhibits `NaN`/`Inf`, contact buffer overflow, or solver divergence, `invalid` must strictly override `severe_penetration` and reject the entire uncommitted transition.
- Must not fabricate zero-filled terminal observations or advance committed step counters on `invalid` transitions.

---

## 3. Deliverables Required from Primary Authors

1. **Formal Substep State-Machine & Priority Proof**: Specify the exact transition table over substeps $j \in \{1, 2, 3, 4\}$ and post-step `final` check mapping `(penetration_depth, finite_mask, contact_count < nconmax, solver_status, schema_ok)` to `{continue, terminal(severe_penetration), reject(invalid)}`, proving that `invalid` strictly dominates `severe_penetration` and `severe_penetration` strictly dominates `success` and `timeout`.
2. **Curriculum Quota & Anti-Forgetting Controller Specification**: Formalize the exact state transitions of `PoolQuotaSchedule` across `quota_epoch_control_rows = 4096` and `eval_interval_control_steps = 100,000`, including integer rounding remainder accounting, hold-on-regression when low-height success drops by $> 10$ percentage points, and resume hash verification.
3. **Three-Part Verification & Smoke Suite**: Specify the exact deterministic test fixtures and bounded real-backend CPU closed-loop checks required by R2.1 §7 (credible failure commit test, injected post-penetration corruption rejection test, panel continuation denominator test, and 6-optimizer update + `--resume` parity check).

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Substep Priority & Replay Isolation Rigor | 35% | Zero possibility of corrupted data entering replay/BN or valid falls halting runs. |
| UFO Relabel & BN Order Fidelity | 25% | Exact match to `sample_mixed_z` and single-pass `(obs, m_current)` / `(next_obs, m_next)` BN updates. |
| Curriculum & Quota State Completeness | 20% | Prevents quota starvation (`paused` deadlock) and enforces two-panel Wilson gate. |
| Verification Suite Executability | 20% | Covers all three R2.1 §7 targeted tests plus `--resume` state equivalence. |
