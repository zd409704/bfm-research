# Eng-1 — Blind Review A (Opus) on Proposal B

Reviewer: Blind Reviewer A (Claude Opus). Inputs read: `packets/Eng-1/proposals/B.md`, `drafts/B/summary.md`, `drafts/B/PLAN.md` (+ `PLAN.sha256`), `brief.md` (rubric), `packets/Eng-1/source/*`. Proposal A, `drafts/A` and any `C-Eng1-A-*` were **not** read. This is a reviewer lean, not a packet adjudication. I make no claim-state changes.

Seal check: `sha256sum drafts/B/PLAN.md` = `9b808ea0…4a2a49`, which matches `PLAN.sha256`. The PLAN is intact as sealed.

Reviewer computation disclosure: I ran a non-rigorous float64 zonotope propagation and one clipped replay of the frozen fixture (scratch scripts in `$TMPDIR` only; nothing filed under the run root). These numbers are reviewer estimates, not spike results. They do not substitute for the PLAN's verified-arithmetic run.

## Summary

B recommends one scope: richer-plant **S0a finite-horizon envelope certification**. It uses a two-state, two-mode discrete surrogate with observation delay j∈{2,5,10,20}, a first-order actuator, effort caps, a reset at k=100, and correlation-preserving affine reachability. Arithmetic is exact or outward-rounded, and producer and checker are separate. Outputs are a checked certificate, a verified witness, or an explicit UNRESOLVED. The interfaces have generic owners (envelope owner, body loop, certificate producer/checker, scene publisher, decision core) and a refusal semantics that does not claim safe stopping. Three new IDs (C-Eng1-B-01..03) are engineering sufficiency/contract hypotheses with grade N/A. Principle hygiene is very strong. The weakness is scientific: as frozen, the spike's engineering outcome is close to determined in advance, and its witness logic cannot see the saturation/authority failures that motivate the packet.

## Gate notes (applied before ranking, B.9.5)

**Principle integrity: PASS.**
- No Locked claim exists and none is asserted. D-P1-001 is correctly kept as a Provisional S0a acceptance gate, not a necessity order. X-P1-001..004 are inherited by ID.
- Inherited grades match the sealed rulings. C-P1-001 is G1 narrow, recommended-for-lock conditional. C-P1-002 is G2, tighten. C-P1-003 is G3, quarantined. C-P1-010/011 are G1 narrow, tighten. **C-P1-012 is correctly reported as downgraded to G2** and is not used as export necessity, as Prin-1 amendment 4 requires. E03/E07/E13/E15/E17 carry conditional or provisional G1 kernels, with G3 acquisition readings, as Candidates.
- The necessity/sufficiency split is explicit. A certificate is finite-model sufficiency for one controller and contract; a violation defeats only that implementation/contract pair; non-certification is not impossibility. Citation ablation is stated, and no biology is load-bearing.
- No Grade-3 reading is used as a gate, veto or ordering argument.

**Bypassed Grade-3 edges (B.8.5): PASS, complete.** Prin-2 amendment 4 requires at least E05/E06, E08/E09 and E14, plus E10/E11 if S1 is pursued without S2a. All of these are listed. The inventory also covers E01/E02, E03/E04, E07, E12/E13, E15, E17 and E19. That is all 17 edges (odd E01–E19, even E02–E14). B states that the S0a-only spike traverses no forward edge. Under B.8.5 that is accurate: B adds no stage, so nothing is skipped. B's distinction between "waived as prerequisite for independent S2a" and "experimentally bypassed" is correct and helpful.

**Hidden-S2a check: PASS.** The controller is mode-blind with a fixed K and receives no mode, reset or disturbance truth. The schedule is an evaluator premise. Mutation 5 audits for truth leakage.

No gate blocks ranking.

## Concrete objections

1. **The fixture is far inside its envelope, so the engineering outcome is effectively predetermined (Falsifiability, Complexity).** My float estimate of the unclipped affine support over all 16 cells gives worst |x| between ≈0.0032 (j=2, all-0) and ≈0.0050 (j=20, 1→0), against an envelope of 0.02. Worst pre-clip |v| is between ≈0.08 and ≈0.14, against a cap of 2. So the state margin is about 4× and the command margin about 14× in every cell. Saturation is never active, and moving the delay from 2 to 20 ms changes the bound by under 1.5×. Under the frozen rules, every cell should come back VERIFIED_MODEL_CERTIFICATE, and C-Eng1-B-01 "SUPPORTED" is near-certain. The spike can still fail as a *harness*, but it cannot tell us whether "the scalar acceptance concept remains useful when assumptions interact." It never approaches the boundary where delay, coupling, reset and authority interact. **Amendment:** extend the delay sweep until certification is lost, or calibrate j and K so that cells straddle the boundary. Also preregister the expected boundary, for example the scalar L* from C-P1-001 mapped to this fixture, so that a scalar-to-coupled prediction can actually fail. B explicitly declines to compare against C-P1-001's L*. That keeps it honest, but it leaves the packet's own question untested.

2. **The witness search cannot find saturation-driven violations, which are the authority failures C-P1-002 motivates (Failure modes, Falsifiability).** The PLAN only constructs a witness "when unsaturated support exceeds the state envelope," using generator signs taken from the *linear* system. If pre-clip commands exceed the cap, the result is UNRESOLVED_SATURATION. In authority-stress control 6 (all-0, j=2, cap 0.01), the unclipped support stays at ≈0.003, so no witness search is ever triggered. Yet a trivial in-set clipped violation exists. In my float replay, x[0]=(+0.002,+0.002), d≡(+0.05,+0.05) and n≡+1e-4 give |x₂|≈0.02006 > 0.02 at k=138. The PLAN would report UNRESOLVED_SATURATION where a verifiable WITNESS_VIOLATION is available, so the main authority failure would be reported as numerics. **Amendment:** add a saturation-aware witness generator. Candidates are constant-extreme or bang-bang disturbance/noise/initial-vertex replays in the clipped recurrence, or a simple clipped-system enclosure. Keep "only verified replays count."

3. **The finite horizon is not tied to how a decision core would use the certificate (Latency, Integrability, Stackability).** Certificates cover 0.2 s, and concatenation "requires a checked handoff-state inclusion," but no spike test exercises that. A decision core consuming a certificate that expires after 0.2 s needs either rolling recertification or terminal-set ⊂ initial-set invariance. The spike checks neither, so the decision-core interface is specified but untested. **Amendment:** add one cheap test. Check whether the terminal augmented-state enclosure, including actuator and history memory, lies inside the declared initial set. On my estimates the terminal |x| bound (~0.003) exceeds the initial box (0.002), so this test should *fail* informatively. That is exactly the kind of result the packet should surface.

4. **Engineering IDs reuse the `C-` claim namespace without claim records (Principle integrity, governance hygiene).** The brief's layout puts `C-*` items under `claims/C-*/claim.md`. B names its hypotheses C-Eng1-B-01..03 but says "no new … claim directories are needed." That invites ledger confusion between necessity-track Candidates and engineering hypotheses. **Amendment:** either use a distinct prefix (for example `H-Eng1-B-*`) or file minimal records marked "engineering sufficiency, no grade."

5. **C-Eng1-B-02 and C-Eng1-B-03 are weakly informative (Falsifiability).** Mutations 3, 4 and 7 mostly test hash and scope equality. A correctly built checker passes them by construction. C-Eng1-B-03 fails only if logging is missing. These are good harness hygiene, but calling them hypotheses overstates what they test. Consider merging them into the harness PASS criteria.

6. **Spike artifact location deviates from the brief (Constraint fit, minor).** The brief says spikes are "Filed under `spikes/<packet-id>/` with sealed PLAN.md before run." The PLAN puts the implementation and verdict under `packets/Eng-1/drafts/B/spike/`. This is easy to fix at run time (copy or link the sealed PLAN to `packets/Eng-1/spikes/`), but it should be recorded as an amendment rather than done silently.

7. **The scope departs from the inherited "Alternate A→S2a next," and the post-SUPPORTED handoff is unspecified (Stackability).** D-P1-001 and Prin-2 both point to S2a as the likely next mainline. B's choice is admissible: planning order is not evidence, and B gives a rationale. But B says what an *unsupported* result implies (favor S2a or amend) and not what a *supported* result unlocks next. Given objection 1, "supported" is the likely outcome, so the packet risks spending a cycle deepening S0a without a defined next step. **Amendment:** state the post-SUPPORTED next packet, for example "S2a proceeds and consumes the certificate interface as its acceptance object."

8. **Minor PLAN clarifications.**
   - For transition schedules, state m[100] explicitly. The current wording ("0→1 at k=100", with the reset applied "before the k=100 command and state step") implies m[k]=1 for k≥100 but does not say so.
   - Clarify that n[k] indexes the step at which the observation is *used*. With 4N noise generators this matters for generator bookkeeping.
   - Budget looks feasible. I estimate about 800 generators in an augmented dimension of about 44, with sparse shift-register history, so even exact rationals with large denominators should fit 16 cells in 15 CPU-minutes. The runner should still log arithmetic time per cell.

## Strengths worth keeping

- Gate discipline is among the best possible. Grades are exact, C-P1-012's downgrade is honored, the edge inventory is complete, and harness PASS is consistently separated from engineering outcome and from hardware transfer.
- The three-valued outcome (certificate / verified witness / unresolved), with "unresolved is not unsafe" and "loose bounds are not impossibility," is the correct epistemics.
- Command vs applied effort, observation age vs total latency, and evaluator truth vs feedback inputs are kept separate and auditable.
- Analytic controls are correct. The positive-control closed form 0.9^k·0.002 + 0.001(1−0.9^k) is right, and the negative control first exceeds 0.02 at k=21 (0.021).
- Very low evidence demand and very high reversibility.

## Rubric scores (1–5)

| Dimension | Score | Basis |
|---|---|---|
| Constraint fit | 4 | All hard constraints and non-goals respected; spike path deviates from `spikes/<packet-id>/` (obj. 6). |
| Principle integrity | 5 | Grades, states, the necessity/sufficiency split, ablation and the bypass inventory are all correct and complete. The ID-namespace issue (obj. 4) is hygiene, not integrity. |
| Falsifiability | 2 | The harness can fail, but the engineering outcome is near-certain on this fixture (obj. 1). Saturation violations can't be witnessed (obj. 2). B-02/B-03 are close to tautological (obj. 5). |
| Evidence demand | 5 | CPU-only, 15 min / 1 GiB, no hardware or data. |
| Failure modes | 4 | Dominant risks are named with handling; the saturation-witness gap undercuts the authority row (obj. 2). |
| Integrability | 4 | Clear generic ownership and read-only publication. Horizon/expiry use by the decision core is untested (obj. 3). |
| Latency / criticality | 3 | Fast-tier feedback is fixed and certification is offline, which is correct. But a 0.2 s certificate with no recertification or invariance story leaves the runtime tier role unclear. |
| Complexity cost | 3 | Exact arithmetic, a producer/checker split and a mutation suite are justified in principle, but they buy little on a fixture with 4×–14× margins. |
| Reversibility | 5 | Synthetic, self-contained, cheap to abandon; S2a remains independent. |
| Stackability | 3 | The versioned certificate/refusal interface is reusable, but no next step is defined after a SUPPORTED result, and the scope stays at S0a rather than advancing toward S2a (obj. 7). |

Total: 38/50 (unweighted; for reference only — gates govern, not totals).

## Lean

**Alternate**, conditional on amendments 1–3. Recommend becomes reasonable if the fixture is moved to the certification boundary, a saturation-aware witness search is added, and an invariance/handoff check is included. B passes every Principle gate cleanly and is cheap and reversible, so it does not merit Reject. As frozen, though, the spike mainly validates certificate bookkeeping on a problem whose answer a float calculation already shows. It would add little scientific information relative to advancing the inherited S2a alternative. If the adjudicator selects B as Recommend without amendments, it should record in advance that the expected outcome is "all 16 cells certified; authority stress UNRESOLVED_SATURATION," and treat that outcome as low-information.
