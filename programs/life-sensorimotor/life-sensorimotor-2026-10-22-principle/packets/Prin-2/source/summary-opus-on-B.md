# Summary — Opus claim adjudication on Astra-authored (Proposal B) claims, Packet Prin-1

Adjudicator family: Opus. Author family: Astra (cross-family, per `roster.md` / B.9.1).
All three claims remain in state **Candidate**. No Locked Grade-1 is asserted.

| Claim | Title | Grade (confirmed) | Ruling | Key gate status | Spike required before further action? |
|---|---|---|---|---|---|
| C-P1-001 | Scalar response-latency bound | 1 (narrow, scalar fixture) | **recommended-for-lock** (conditional) | B.3 all pass. Citation-ablation pass. L* = ln(1.1)/10 = 9.531 ms re-derived by adjudicator. **B.9.2 allowed-route independent check missing.** No signature. | No (analytic; optional harness check only) |
| C-P1-002 | Timely body-response role | 2 (conditional template) | **tighten-premises-then-Candidate-stay** | Form explicit. Missing information-structure premise and τ* common-prefix deadline. No target-plant premise match. No failed counterexample search. | Not for Candidate-stay. **Yes** before any lock/gate use: search for safe common force history in a fixed target mode |
| C-P1-003 | Evolutionary S0-first path contingency | 3 | **quarantine-Grade3** | Citation-ablation fails → Grade 3. No B.3 shape (intentional). Ineligible for lock. | No |

Cross-cutting:
- Gates were applied before any ranking (B.9.5).
- D-P1-001 remains **Provisional**: an S0a acceptance-gate recommendation, not a necessity order. None of these rulings changes that.
- A spike PASS is harness/sufficiency evidence only. It does not establish necessity or hardware transfer (B.8.4).
- Adjudicator agreement with the author is not grade evidence (B.9.7). C-P1-001 still needs a formal-checker or qualified-human proof check plus the human lead's signature before any lock.
- Scope-narrowing counters: C-P1-001 = 0. C-P1-002 = 1 accepted, 2 if the required information premise is adopted. C-P1-003 = 0.

Rulings: `ruling-C-P1-001.md`, `ruling-C-P1-002.md`, `ruling-C-P1-003.md` (this directory).
