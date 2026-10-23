# Ruling — C-P1-002 (Timely body-response role)

1. **Claim ID:** C-P1-002
2. **Adjudicator family:** Opus (Claude Opus; claim adjudicator for Astra-authored claims per `roster.md`)
3. **Author family:** Astra
4. **Ruling:** **tighten-premises-then-Candidate-stay**
5. **Grade:** Grade 2 (conditional structural candidate) **confirmed provisionally**. State: **Candidate**. Not lockable at present. No veto authority.

## 6. Gates check (B.3 / B.9)

| Gate | Status |
|---|---|
| Premises complete (B.3.1) | **Partial.** The form is now explicit: fixed plant, envelope, disturbance set, resources, total-force accounting incl. passive and embedded forces, and feasibility. Two defects remain. (a) **No information structure.** "Initially hidden" never says which channel reveals the disturbance, or when. C-P1-001 premise 4 has no analogue here. (b) **Deadline is mis-specified.** Disjointness of safe sets on [0,T] only implies the histories differ *somewhere* in [0,T]. "Early enough" needs the latest common-prefix time τ* = sup{τ : ∃ safe h₊ ∈ S₊, h₋ ∈ S₋ with h₊ = h₋ a.e. on [0,τ)}. In C-P1-001, τ* = L*. No target-plant parameterization exists yet (acknowledged). |
| Conclusion shape (B.3.2) | **Pass (conditional functional completeness).** Note that given premise 3 the conclusion is a logical consequence. The empirical content of the claim is carried *entirely* by premise 3 for a given plant. |
| Implementation independence (B.3.3) | **Pass** in form: total corrective force is counted irrespective of mechanism. |
| Falsifier operational (B.3.4 / B.9.3) | **Pass in definition, not yet instantiated.** A force/state absence test with predeclared resolution and response-removal probes is specified. Caveat: success with role absent is impossible by construction once premise 3 holds. The only live falsifier is therefore a **safe common force history**, i.e. failure of premise 3. The counterexample search must target that. State-dependent passive forces differ between worlds trivially; the absence test must use the *required* separation magnitude, not just any difference. |
| Citation-ablation (B.8.7) | **Pass.** Removing evolutionary/anatomical motivation leaves the conditional argument intact. |
| Grade-2 lock gates (B.9.2) | **Not met.** No target-plant premise match. No logged serious failed counterexample search. No signature. Cross-family agreement is not grade evidence (B.9.7). |

## 7. Counterexample spike before further action?

**Not before Candidate-stay. Yes, before any recommended-for-lock or any use as a gate.** Prerequisite: one fixed, feasible target mode with a declared envelope and disturbance pair. Then a sealed `PLAN.md` (§12.2) must search for a **safe common total-force history** (an attack on premise 3) and compare passive-only, embedded-feedback and active realizations, with preregistered force-resolution limits. The runner files data and does not change state (B.9.8).

## 8. Justification

- The author's amendment does what P1 mandated: it removes "or an equivalent physical mechanism" in favour of measured total corrective force. I accept it as **scope-narrowing event 1**.
- The disjoint-safe-history argument is valid and implementation-independent, but it is nearly definitional. The role adds no content beyond premise 3 plus a realization measurement. Therefore Grade 2 is retained only as a **conditional template** that needs a per-plant premise match.
- The two required tightenings, (a) information structure and (b) the τ* deadline, are precisions without which "timely" is not well defined. They are not rescues from a counterexample.
- Because (a) excludes pre-onset predictive information, it restricts admissible systems. When the author adopts it, log it conservatively as **narrowing event 2**. A third event triggers mandatory retirement review (B.9.6).
- If no target mode can be parameterized so that premise 3 is independently established, the next ruling should be **downgrade-grade** rather than retaining necessity language.
- C-P1-001 supplies one scalar instance of premise 3 (τ* = L*). It does not establish premise 3 for any humanoid mode.
- D-P1-001 remains Provisional (an S0a acceptance gate, not a necessity order). A spike PASS ≠ necessity.

## 9. Outstanding items for human lead

1. Author revision (via the orchestrator, not the adjudicator) adding (a) an explicit information/indistinguishability premise and (b) the τ* common-prefix deadline definition. Log narrowing events 1 and 2 in `upgrade-log.md`.
2. Name an envelope owner and an approval/version path. Choose one support mode to parameterize first. The humanoid-plausible mode near a ≈ 3.3 s⁻¹ is the natural candidate.
3. Approve a sealed counterexample-search PLAN targeting safe common force histories, including passive-only and existing embedded-control realizations.
4. Unresolved: whether envelope definition depends on contact/support distinguishability (circularity flag from P1). This blocks hardware applicability and is not a reason to gate S1/S2 research.
