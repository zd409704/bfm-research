# Summary — Opus claim adjudication, Prin-2 even-numbered edges (Astra-authored)

Adjudicator: Claude Opus (cross-family vs author Codex gpt-6-astra, per roster.md). Inputs: claim.md / upgrade-log.md / violations.md for each ID, method-Appendix-B.md, brief.md, roster.md. No claim.md edited. Proposals A/B not read beyond the claim files.

| ID | Edge | Ruling | Grade | State | Ablation | B.9 | B.9.6 count | Eng-1 gate? | Note |
|---|---|---|---|---|---|---|---|---|---|
| C-Prin2-E02 | S0a → S0b | quarantine-Grade3 | 3 confirmed | Candidate | survives (no load-bearing kernel) | fails | 0 | no | Envelope is an acceptance conjunction; joint-controller bypass |
| C-Prin2-E04 | S0a → S1 | quarantine-Grade3 | 3 confirmed | Candidate | survives | fails | 1 proposed | no | Timely-response role kernel plausible as a *role*, not an edge |
| C-Prin2-E06 | S0a → S2a | quarantine-Grade3 | 3 confirmed | Candidate | survives | fails | 1 proposed | no | S2a work may proceed without an S0a-order lock |
| C-Prin2-E08 | S1 → S2a | quarantine-Grade3 | 3 confirmed | Candidate | survives | fails | 0 | no | Supplier exclusivity fails; retire-watch |
| C-Prin2-E10 | S2a → S1 | quarantine-Grade3 | 3 confirmed | Candidate | survives fully | fails (no B.9.2 check/signature; contracts unmatched) | 1 proposed | no | TV kernel algebra checked correct; register as separate claim |
| C-Prin2-E12 | S0b → S1 | quarantine-Grade3 | 3 confirmed | Candidate | survives (no load-bearing kernel) | fails | 0 | no | S0b is a package, not a role |
| C-Prin2-E14 | S0b → S2a | quarantine-Grade3 | 3 confirmed | Candidate | survives (no load-bearing kernel) | fails | 0 | no | Strongest retire candidate; direct-channel bypass |

## Cross-cutting findings

- **No grade changes. No recommended-for-lock. No Locked state.** No Grade-1 lock is claimed or implied. Grade-1 locks need a B.9.2 verifier and the human lead's signature (brief constraint 7).
- Every edge passes the citation-ablation half (no biological premise is load-bearing). Every edge fails the B.9 half: no registered or failed counterexample search, no independent proof check, no signature. So Grade-3 quarantine applies to all seven.
- **D-P1-001 is not a necessity order.** It stays a Provisional S0a acceptance gate. No even edge makes S0a, S0b or S1 a necessity prerequisite for S2a or S1. Eng-1 S2a work is not gated by any of these edges.
- Scope-narrowing counts (E04, E06, E10 = 1 each) are proposed narrowings recorded conservatively. None is adopted. No claim is near the B.9.6 retirement-review threshold of 3.
- Follow-up priority: (1) E10 kernel as a standalone Grade-1 Candidate claim, seeking a premise-matched published-result check; (2) E04 timely-response as a Grade-2 role claim; (3) registered bypass fixtures for E14/E08 (retire-watch).
- Disclosure: the E10 algebra check is by the LLM adjudicator. It does not count as a B.9.2 Grade-1 verification.
