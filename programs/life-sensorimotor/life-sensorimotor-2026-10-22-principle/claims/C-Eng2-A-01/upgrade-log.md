# C-Eng2-A-01 — Upgrade log

## 2026-10-22 — Cross-family claim adjudication

- **Baseline:** narrow formal Grade-1 Candidate; author proof supplied; no prior upgrade log or sidecar evidence present. Initial recorded B.9.6 counter: 0.
- **Action:** tighten-premises; Candidate retained, with no lock recommendation, grade change, or veto. See `adjudication/ruling.md` for the proof review and outstanding B.9.2 requirements.
- **Finding:** the exact side-information bound survives. The statistical union-bound proof requires a fixed evaluated test; fixing only its threshold family leaves selection validity unproved. This is a document-level proof audit, not an empirical counterexample or spike.
- **Narrowing event 1:** restrict statistical form (b) to a test fixed independently of evaluation, with fixed sample sizes and independent per-window randomization where used. Independent calibration is allowed. Evaluation-based search needs separate selection-valid justification. Counter **0 → 1**; the exact form is unchanged. This conservative restriction is counted even though the original falsifier already excluded evaluation-fitted thresholds.
- **Clarifications, not additional narrowing events:** enforce the existing true-joint-model requirement for the full genie; correct atom handling and finite-sample NULL/harness interpretations; distinguish per-cell false-certificate control from conditional or simultaneous coverage.
- **Outstanding:** reconcile the deferred PLAN's threshold-selection wording and conditional likelihood with the ruling before sealing. Any later lock path requires B.9.2-acceptable verification and the human lead's signature. No other claim's narrowing counter or state is assigned here.
- **Execution:** none. No simulation, spike, empirical counterexample search, or run artifact was produced. Existing execution gates remain in force.

**B.9.6 counter after this entry: 1.** Mandatory retirement review begins at event 3. No 3→2→1 promotion occurred.
