# Ruling: C-P1-011

- Claim ID: C-P1-011
- Adjudicator family: Astra
- Author family: Opus
- Ruling: tighten-premises-then-Candidate-stay
- Grade: Grade 1 confirmed for the conditional data-processing invariant only; no grade attaches to an export choice or research-order inference.
- State: Candidate. No lock or veto authority; no Locked Grade-1 without independent verification and human lead signature.

## Gates check (B.9)

| Gate | Finding |
|---|---|
| Premises complete? | Partial. The export-only Markov condition is explicit. The side-information form must explicitly require Z → (X, W) → Y, with all retained information, time windows and causal feedback accounted for. An application still needs a specified Z and architecture audit. |
| Falsifier operational? | Partial. Finding an omitted contact-informative input is an actionable premise challenge, but the target input inventory and audit criteria are not supplied. B.9.4(a) must remain available for an artifact exposing an error in the recorded formulation or premise mapping. |
| Citation-ablation pass? | Yes for B.8.7: no biological citation supports the invariant. This is not a substitute for independent B.9.2 verification. |
| Confound disclosed? | Yes: commands, memory and other side channels, redundant derived fields, ordering stretch and limited programmatic force are disclosed. This cross-family review did not inspect the cited theorem source or a target architecture. |

## Registered counterexample spike

None registered; no counterexample spike is required before further action. Required next work is premise repair and a side-channel document audit, followed by independent theorem verification. A numerical PASS would not prove necessity.

## Justification

1. The export-only inequality follows from the stated Markov condition and is implementation independent within that condition.
2. Adding W requires conditional independence of Y and Z given the joint input (X, W); merely naming side information does not establish it.
3. Replace “a channel independent of X” with “additional information about Z conditional on X”: a useful side channel may be correlated with X.
4. Processing cannot increase information relative to its complete input; with W present, do not compare joint-channel information to X alone.
5. Accept the proposed definition, side-channel and ordering repairs as B.9.6 event #1: they restrict the inherited application, even though they clarify a theorem.
6. Independent source verification and the human signature are outstanding; the record is not ready for an unconditional lock recommendation.
7. D-P1-001 remains an acceptance-gate decision, not a necessity ordering; DPI supplies neither a mandatory export schema nor a ladder edge.

## Outstanding items for human lead

- Require the explicit joint Markov condition and corrected side-channel wording before reconsideration.
- Arrange an independent item-by-item theorem match; specify Z, resolution, time window and the complete input inventory for each target application.
- Have the record maintainer log accepted premise-repair event #1; log later distinct restrictions separately under B.9.6. No claim or log is edited here.
- Retain Candidate status pending verification and any eventual human-signed lock.
