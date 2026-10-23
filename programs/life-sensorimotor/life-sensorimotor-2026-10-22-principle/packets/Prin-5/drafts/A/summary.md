# Prin-5 — Author A summary

**Full proposal:** `packets/Prin-5/proposals/A.md`
**Status:** Planning only. C-P1-011 stays **Candidate** (Grade 1, narrow). No grade or state change. No Locked Grade-1. No Eng-2 gate changes (D-Prin-3-001 unchanged). Not a necessity order.

## Thesis
C-P1-011's premise 2 is a conditional-independence claim about a closed-loop, time-evolving system. It is audited by a **d-separation path certificate on a time-unrolled channel graph** (nodes: scene `S`, contact `Z`, body-internal `B`, realized export `X`, upper outputs `C_up`, sensors/memory/infrastructure `W_s/W_m/W_i`, label process `L`, upper state `Y`), not by a sensor list.

The audit output is an attribution report, `I(Z;X,W) = I(Z;W) + I(Z;X|W)`. The export's real contribution is `I(Z;X|W)`, which can be smaller *or larger* than `I(Z;X)`.

## Inventory: seven path classes
- **E** efference / own outputs (commands, gains, contact schedule, active probing)
- **T** temporal and metadata inside `X` (arrival jitter, event-triggered rate, drops, fault/saturation/safety flags, schema version)
- **S** independent sensing, plus duplicated proprioceptive streams that silently enlarge `X`
- **M** memory, priors, common cause (maps, cross-episode memory, train/eval overlap in learned parameters, privileged-teacher wiring)
- **I** infrastructure and harness (simulator or debug ground truth, shared memory and logs, shared RNG and clocks, power and thermal telemetry)
- **L** label-definition coupling (`Z` defined from a signal that is also in `X` or `W`; label source mismatch; post-hoc windows)
- **D** distribution mismatch and adaptive evaluation

## Tighten-premises (TP-1..TP-7; adjudicator to rule)
1. Label provenance is part of the definition of `Z`.
2. Path certificate required for any application.
3. `X` is the realized stream, metadata included.
4. `W` must include past upper outputs (closes feedback), memory, and parameters when train and eval are not independent.
5. DPI processing covers only Z-independent processing. Event-triggered sampling is part of `X`.
6. **H4 amendment:** a derived field adds no information only if it is derived from published fields.
7. Usage rule: report `I(Z;W)` vs `I(Z;X|W)`; never cite `I(Z;X)` alone when `W ≠ ∅`.

B.9.6: these are hypothesis clarifications, not survival narrowings. The proposal asks the adjudicator to count them as one bundled event (or zero), and discloses that counting each one separately would trigger retirement review.

## Audit checklist
14 yes/no items with artifact pointers. Inputs are enumerated from **deployment config**, not design intent, and the certificate needs a non-designer sign-off. Any "unknown" means unaudited, and the claim may not be cited for that stack. Findings are filed as B.9.4(b) premise failures, not as counterexamples.

## Optional sub-item (not a gate)
**Leak-alarm lemma (author sketch).** Suppose the C-Eng2-A-01 ceiling is computed with `W=∅` (export only), and a held-out detector on `Y` beats it by C-Eng1-A-01-style bounds. Then the Markov chain fails with probability ≥ 1−2α. This is a trigger only. It localizes nothing, and it carries no certificate of absence. It needs its own claim record and a cross-family adjudication.

## Falsifier for this proposal
A non-author reviewer constructs a contact-informative path to `Y` that fits none of E/T/S/M/I/L/D. That would show the taxonomy is incomplete. It would not count against C-P1-011.
