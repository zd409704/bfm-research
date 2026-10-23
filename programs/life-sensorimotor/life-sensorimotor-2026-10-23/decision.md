# Decision — Packet P1 (life-sensorimotor-2026-10-23)

**Status:** **Provisional (sim harness PASS; target plant not claimed; amendments required before lock).**  
**Method:** v0 (commit 3cb8fd5, sha256 `9bc0d7807e81e221508bcbb998dbd0084347521ca661370b8f9da99ac7fec1bb`); pinned at `/srv/claude/research/methodology-upgrade-2026-10-23/pinned/orchestrating-ai-research-teams.v0-3cb8fd5.md`.  
**v1 mid-run adoptions (Class 0/1 only):** seal+cmp; method pin; epoch/UTC canonical time; Sonnet P/Q order-swap adjudication; Candidate-only necessity claims this run; confounds + dissent disclosure; mechanical spike PLAN rules. Class-2 dual cross-family adjudication **not** applied (no human sign-off).  
**Canonical time:** deadline epoch `1792706829`. Box-local labels America/Toronto (EDT) are display-only.  
**Sealed mapping:** `logs/pq-mapping.json` — **P = Proposal A (Opus), Q = Proposal B (Astra)**. Adjudicator prompts used only P/Q.

## Adjudication procedure

| Pass | Log | Order | Recommendation |
|------|-----|-------|----------------|
| pass1 | `adjudication/score-pass1.md` (+ `logs/adjudicate-pass1-attempt1.*`) | P then Q | **Recommend Q** (provisional + amendments) |
| pass2 | `adjudication/score-pass2.md` (+ `logs/adjudicate-pass2-attempt1.*`) | Q then P | **Recommend Q** (provisional + amendments) |

**Order-swap result:** stable (same pick). Not escalated as unstable tie.

**Adjudicator:** Claude Sonnet 5.5 medium (same family as Author A; also Experiment-runner slot). Confound disclosed below. Orchestrator (Opus) did **not** sole-score; this file only formats Sonnet tables and unblinds P/Q after both passes completed.

## Unblinded recommendation

**Recommend Proposal B** (“Lock the Body’s Response Envelope First” / S0a bounded-response viability contract), **provisional**, with mandatory amendments in §Amendments before any non-provisional lock.

**Alternate:** Proposal A (body-loop contract + S2a proprioceptive contact-observability floor), to be pursued as next packet (S2a) after S0a certification — carrying forward A’s C2 information-ceiling, realized-torque export, and `ident_flag` ideas after repairing C7 confound.

## Rubric scores (from Sonnet; unblinded)

### Pass1 totals: A(P)=30/50, B(Q)=34/50

| Dimension | A (P) | B (Q) |
|---|:-:|:-:|
| Constraint fit | 3 | 4 |
| Falsifiability | 3 | 2 |
| Evidence demand | 2 | 4 |
| Failure modes | 3 | 3 |
| Integrability | 3 | 3 |
| Latency / criticality | 3 | 3 |
| Complexity cost | 3 | 4 |
| Reversibility | 4 | 5 |
| Necessity discipline | 3 | 4 |
| Stackability | 3 | 2 |

### Pass2 totals: A(P)=29/50, B(Q)=37/50

| Dimension | A (P) | B (Q) |
|---|:-:|:-:|
| Constraint fit | 3 | 4 |
| Falsifiability | 3 | 3 |
| Evidence demand | 2 | 4 |
| Failure modes | 3 | 3 |
| Integrability | 3 | 4 |
| Latency / criticality | 3 | 3 |
| Complexity cost | 3 | 4 |
| Reversibility | 4 | 5 |
| Necessity discipline | 2 | 4 |
| Stackability | 3 | 3 |

Scores are not averaged into a new ranking; both passes independently recommend B.

## Rationale (composed from Sonnet)

B wins on constraint fit, evidence demand, complexity, reversibility, and necessity discipline. It states a narrow Grade-1 response-deadline claim (B-N1) with honest scope and does not let the spike promote necessity. A is richer and has the only program-informative falsifier (PF-2), but its ordering leans on confounded C7, an infeasible SA-1 runtime as written, and passivity stretch beyond cited assumptions. B’s weakness is a near-vacuous scalar spike; amendments below are mandatory before lock.

## Strongest unresolved objection (from reviews + Sonnet)

B’s S0a gate may carry no research information for a legged target plant: envelope (D, b, latency budget) undefined for the real plant; may already be satisfied by kHz joint PD; or may require per-support-mode certification that imports S2 distinguishability (circular) / blocks S1 via no-enlargement. Quoted from adjudication pass1/pass2 dissent sections.

## Amendments required before non-provisional lock

1. Record **S0a-first as an acceptance gate**, not a necessity ordering of research.
2. Explicit **ladder amendment**: S0 split into S0a (bounded-response viability) / S0b (remaining reflex/impedance content).
3. **Discriminating spike**: effective-latency sweep across L* (~2–20 ms), off-grid onsets, noise + actuator lag; remove vacuous oracle/on-grid-only checks; include humanoid-plausible mode (LIP a≈3.3 s⁻¹) + one joint-level mode; mark 250 Hz/1 kHz as placeholders until mode-specific L* exists.
4. Name **envelope owner** + approval/version path; declare whether S0a is scoped per support mode.
5. Tighten or downgrade B-N2 (“equivalent physical mechanism”).
6. Carry A’s best content to a **separate S2a packet** (not discarded).

## Spike status

PLAN sealed before runner (`logs/seal.txt`). Runner: Sonnet fresh call (`logs/spike-runner-attempt1.*`), code only under `spikes/`.

**Attempt 1:** `verdict=FAIL` (τ interpreted as pure delay stacked on lag+ZOH → total latency > labeled τ; τ=5 ms peak > b). Logged in `spikes/runs.log`.

**Attempt 2:** harness interpretation fix (τ = total effective latency); metrics/thresholds/seeds unchanged — see `spikes/deviations.md`.

Verbatim JSON (attempt 2 / METRICS.md):
```json
{"metric": "discriminating_latency_sweep", "threshold": "tau<=5ms peak<=0.01 AND tau>=15ms peak>0.01", "fixture_A_peaks": {"2": {"0": 0.005517037668933026, "1": 0.005523117807014134, "2": 0.005546855115887719}, "5": {"0": 0.0075200071960854955, "1": 0.0075353043790616055, "2": 0.007550524893934129}, "8": {"0": 0.010795542423835859, "1": 0.01080983207273388, "2": 0.010817335814347944}, "9.5": {"0": 0.022093849997547002, "1": 0.022081250416703998, "2": 0.022173481426451737}, "10": {"0": 0.025055232944359594, "1": 0.025023758839973223, "2": 0.025031578880800667}, "12": {"0": 0.038590125319057755, "1": 0.038507957746963785, "2": 0.0384543796170672}, "15": {"0": 0.0574001905881876, "1": 0.05741194385130749, "2": 0.05742254070411094}, "20": {"0": 0.08282377777659555, "1": 0.08278861991193864, "2": 0.0828264334321471}}, "open_loop_peaks_min": 1.071517289228084, "L_star_ms": 9.531, "L_star_lip_ms": 9.838, "a_lip": 3.302, "lip_formula": "L*=ln(1+a*b/D)/a, b=0.01, D=1", "flag": "NONE", "verdict": "PASS"}
```

**Interpretation:** PASS validates only the amended scalar discrimination harness. Does **not** transfer to the target plant. Fixture B observation: `L_star_lip_ms=9.838` (no `POLICY_50HZ_MAY_SUFFICE`). Peak crosses b near τ=8 ms (< analytic L*=9.53 ms) — discriminating but not tight to L*.

**Decision status after spike:** **Provisional (sim harness PASS; hardware transfer not claimed; amendments 1–6 still required before non-provisional lock).**

## Necessity claims this run

All claims from A and B remain **Candidate**. No Grade-1 lock signed by human lead in this wall clock. See `ledger-entries.md` / `principles/`.

## Confounds (mandatory disclosure)

1. **Author resource asymmetry (ISSUE-006):** Opus medium + Write tools vs Astra high + read-only stdout.
2. **Adjudicator family (ISSUE-005):** Sonnet same family as Author A; also Experiment-runner slot. Mitigated by P/Q blinding + order-swap (stable) + mechanical spike verdict.
3. **Draft isolation residual (ISSUE-001/1.3):** A.md complete before B appeared; A process briefly alive after B deposit — unaudited whether A tools could have read B in that window (low risk, disclosed).
4. **Review publish-after-all missed (ISSUE-007):** A-on-B written to `reviews/` while B-on-A still running.
5. **Log overwrite (ISSUE-003):** first Opus failure stderr overwritten by relaunch.
6. **Method pin:** later steps pointed at v0 pinned copy; repo path may hold v1.

## Version

- `decision.md` v0.2 — Recommend B + amendments + spike attempt2 PASS quoted — see progress.md
- Change requests only after this version; silent drift forbidden.

## Human lead open questions

- Prefer A if weighting program-relevant falsifiability above cost? (Sonnet notes this is reasonable.)
- Sign any Grade-1 lock this run? (Recommended: no; keep Candidate.)
- Approve Class-2 dual cross-family adjudication for next packet?
