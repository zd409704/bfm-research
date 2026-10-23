# C-P1-001 — Scalar response-latency bound

- **Origin:** B-N1; inherited C-P1-001, with the sealed stub expanded.
- **Author family:** Astra (P1 Proposal B)
- **Grade:** 1, narrow formal candidate.
- **Current state:** Candidate. No lock, veto authority, independent proof certification, or human signature is asserted.
- **Recommended adjudicator action (author, Prin-1; superseded as disposition):** Candidate-stay; obtain independent proof verification before considering recommended-for-lock.
- **Governing adjudicated disposition:** recommended-for-lock (conditional; Prin-1 ruling, reaffirmed Prin-4). State remains Candidate; conditions C1–C7 in `adjudication-prin4/ruling.md` are unmet.

## Premises

1. The research fixture obeys the scalar continuous-time equation \(\dot x=ax+u+d\), with \(a=10\,\mathrm{s}^{-1}>0\). Both worlds start at \(x(0)=0\).
2. The required envelope is \(|x(t)|\le b\), \(b=0.01\), throughout a horizon containing the indistinguishability interval. The guarantee must hold for both admissible worlds, not merely on average.
3. At time zero the unobserved disturbance takes one of the constant values \(+D\) and \(-D\), where \(D=1>0\), and persists through time \(L\).
4. The worlds are indistinguishable to every channel capable of changing applied control until \(L\): \(u_+(t)=u_-(t)\) almost everywhere on \([0,L)\). Earlier predictive information that distinguishes the disturbance is excluded. For randomized controllers couple the same random realization in both worlds; the claim concerns a robust guarantee, not an expected-cost or chance objective.
5. Applied inputs are locally integrable, with ordinary continuous state trajectories; there are no impulsive state resets. A finite change of control at \(L\) cannot erase an earlier envelope violation.
6. Proposal B also stipulates \(|u|\le3\). **This actuator bound is not used in the impossibility proof:** identical input cancels. It remains an implementation-fixture constraint and may impose additional feasibility restrictions; the latency inequality is not sufficient for invariance.

## Conclusion shape and author derivation

**Impossibility / response-latency upper limit (equivalently, a lower bound on response promptness).** Any controller guaranteeing this envelope under these premises must satisfy

\[
L\le L^*=\frac{\ln(1+ab/D)}a=0.00953101798\ldots\ \mathrm{s}.
\]

Set \(\Delta=x_+-x_-\). Then \(\dot\Delta=a\Delta+2D\), \(\Delta(0)=0\), hence
\[
\Delta(L)=\frac{2D}{a}(e^{aL}-1),\qquad
\max(|x_+(L)|,|x_-(L)|)\ge\Delta(L)/2.
\]
Both states in \([-b,b]\) require \(\Delta(L)\le2b\). At \(L=20\) ms at least one magnitude is at least \(0.0221402758\ldots>b\). This is an author derivation, not independent verification. Equality at the bound does not establish continued viability. No controller architecture or nominal update frequency follows uniquely.

## Scope

Scalar research fixture only. The intended application is a generic home humanoid / target plant, but no hardware dynamics, disturbance envelope, support mode, or total response deadline has been certified. Passive stabilization changing the dynamics, additional information, or different tolerances require a new premise match. The claim quantifies over classical, learned, predictive, and randomized controllers subject to identical applied-input histories.

## Falsifier / challenge mode

Supply an admissible common applied-input history that keeps both trajectories inside the envelope through an \(L>L^*\), with exact trajectories or controlled numerical error; alternatively identify an error in the separation proof. A hardware observation can challenge transfer by showing a premise fails, without refuting this fixture statement. Earlier world-dependent actuator action invalidates premise 4 rather than falsifying the bound. A successful run below \(L^*\) is sufficiency evidence only.

## P1 decision hygiene

D-P1-001 remains **Provisional**, an S0a acceptance-gate recommendation, never a necessity order for research. S0a denotes bounded-response viability; S0b denotes remaining reflex/impedance content. The mandatory discriminating effective-delay sweep spans approximately 2–20 ms across \(L^*\), uses off-grid onsets, noise and actuator lag, and includes a humanoid-plausible mode near \(a=3.3\,\mathrm{s}^{-1}\) plus a joint-level mode. Nominal 250 Hz / 1 kHz values remain placeholders. A measured total response delay is not automatically the common-input interval assumed in this proof; log that interval separately.

The sealed decision reports attempt 1 FAIL and attempt 2 PASS after correcting the meaning of total effective latency. Its peak crossing near 8 ms is below this necessary limit and does not refute it or show tightness. Those results were not rerun here. PASS does not promote necessity or establish target-plant transfer. The decision still leaves amendments pending, including envelope ownership/versioning and support-mode scope. B-N2 must be tightened or downgraded separately; this bound does not certify its broad role claim. Citation-ablation: no evolutionary premise is used, and deleting biological motivation leaves the derivation intact.

## Governance and counterexample search

The roster binds the Astra-authored claim to an Opus-family claim adjudicator, distinct from its author. Appendix B.9 requires an independent proof check through an allowed verification route and human-lead signature for a Grade-1 lock; neither is supplied by this author record or by model agreement.

**Counterexample-search spike registered? No.** The inherited decision reports a sealed discrimination-harness PLAN, not a newly registered counterexample search here. Future PLAN: search common-input histories for simultaneous envelope satisfaction above \(L^*\), preregister numerical error bounds and paired-world input checks, and deposit artifacts before any adjudicated transition.

## Sealed provenance

`packets/Prin-1/source/P1-proposal-B.md` (B-N1); `P1-claim-C-P1-001-stub.md`; `P1-decision.md`; `inherited-ledger-P1.md`; `method-Appendix-B.md` (B.3–B.9); run-root `brief.md` and `roster.md`. Short source filenames in this record refer to the same sealed source directory. Referenced external artifacts were not inspected.
