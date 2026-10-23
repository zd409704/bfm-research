# Prin-5 — Blind review B on proposal A

Reviewer: Blind Reviewer B (Codex Astra). Read only proposal A, this packet's source/packet-brief.md and source/method-Appendix-B.md, and the run brief.md rubric. Proposal B was not read. This review changes no claim, grade, state, or Eng-2 gate.

**Disposition: revise before adoption of the certificate and premise amendments; retain the inventory as a useful planning deliverable.** A supplies substantial coverage beyond a sensor list, but its central certificate is weaker than the conditional-independence statement it claims to establish. The optional statistical lemma should remain deferred. This is an assessment of A alone, not a comparative ranking.

## Gates before scoring

| Gate | Finding |
|---|---|
| Claim authority and locking, B.9.1–2 | Pass for a proposal. C-P1-011 explicitly remains Candidate, narrow Grade 1; amendments go to the claim adjudicator. No human signature or completed verification is asserted. The proposed certificate is not itself verified Grade-1 evidence. |
| Necessity discipline, B.3–5 | Pass on grade separation; substantive proof objection below. No benchmark result promotes a claim. Candidate status cannot authorize a mainline veto. |
| Grade-3 quarantine and planning order, B.8 | Pass. No biological narrative supplies necessity; priority 2 is explicitly planning only. |
| Packet scope and Eng-2 non-interference | Pass as a planning submission, with adoption language requiring correction. The opening and §6 preserve D-Prin-3-001 as the sole Eng-2 gate. Mandatory wording in §§4–5 must be scoped to support for a particular theorem application, not permission to run Eng-2. |
| Scope-narrowing accounting, B.9.6 | Pending adjudicator ruling, not an author exemption. The request for zero or one event is disclosed, but is not established merely by calling amendments clarifications. |
| Experiments and new claims | No spike is required for this inventory. The optional lemma has no separate claim record here and is explicitly withheld from use; that is acceptable only while it remains deferred. Any later counterexample search needs its own plan under B.9.8. |

No present claim-state violation warrants rejecting the inventory. The mathematical and governance reservations block adopting the proposal wholesale as an authoritative certificate or usage policy; rubric scores do not cure them.

## Principle integrity: principal objections

**1. Directed-path coverage is not a d-separation certificate (§2, TP-2).** Listing directed paths from four selected source nodes to Y does not check every potentially active trail between Z and Y conditional on (X,W). In particular, it does not by itself establish causal sufficiency, handle unrepresented common causes, or check collider activation by conditioning on X or W. The displayed representation with residual U independent of Z given (X,W) is a sufficient assumption, but is asserted after the checklist rather than derived from it.

A small algebraic diagnostic illustrates the missing step: let Z and U be independent fair bits, X = Z XOR U, and Y = (X,U). The directed path from Z to Y crosses X, yet I(Z;X) = 0 and I(Z;Y) = 1 bit. Conditioning on X couples Z and U. A properly applied infrastructure inventory should place the shared U in W, repairing this example; the point is that directed-path coverage alone does not prove that this has happened. Require either actual d-separation on an explicitly complete time-indexed causal model, or an explicit conditional kernel/factorization argument. A document audit can support the premises while still leaving unknown edges unresolved.

**2. Putting commands in W does not automatically close every feedback issue (§2, TP-4).** Specify whether Y means the whole transcript or the state at one time, the temporal extent of X and W, initial controller state, and which randomness affects future contact. The needed statement is Z conditionally independent of Y given (X,W); including command history is an inventory decision, not a proof of that statement. Moreover, commands can carry information already acquired through earlier X. Thus I(Z;W) need not represent information obtained independently of the export, and I(Z;X|W) is an observational incremental-information quantity, not automatically a causal measure of what the export contributes. The chain-rule identity is sound, but the attribution interpretation needs this qualification. An enormous W can also make a valid bound practically vacuous.

**3. Several categorical statements need narrower wording.** M3's training/evaluation overlap is a reason to audit dependence, not proof that I(Z;theta) > 0 or that the fixed-distribution premise fails. State whether parameters vary in the probability model; a fixed deployed parameter vector is constant in that model. L1's label coupling limits interpretation but does not by itself show that the label says nothing about physical contact. I1's blanket claim that any ground-truth access invalidates evaluation should be restricted to an evaluation that excludes that access; an explicitly declared privileged-information baseline has different premises. These are proposed audit policies, not consequences of DPI alone.

**4. The optional leak alarm overstates its conclusion (§6).** Conditional on a correct export ceiling, a valid comparison detector, and simultaneous coverage for all required bounds, an exceedance can reject the export-only Markov hypothesis with a controlled false-alarm rate. It does not give a frequentist probability that the hypothesis is false after observation. Nor does it uniquely establish a side channel: an invalid genie model, selection leakage, distribution mismatch, or failed interval coverage can also explain the discrepancy. The proposed 2-alpha accounting needs a joint coverage specification for the detector's TPR and FPR bounds, in addition to the ceiling event. Defer this sub-item rather than making the minimum inventory depend on resolving it.

**5. B.9.6 requires an event history, not a preferred count (§4).** Determine for each proposed change whether it merely explicates an existing premise, narrows scope, or adds a premise to survive a counterexample. Log the qualifying events and leave grouping to the adjudicator. Absence of a counterexample does not automatically exempt a scope narrowing. The prose also says six amendments while the table contains seven; correct the accounting description without changing claims in this review.

## Inventory completeness versus laundry-list risk

The strongest parts are the realized-stream definition of X, duplicated raw-signal routes, efference, persisted state, shared infrastructure, label provenance, and the distinction between fields derived from published inputs and fields derived from richer internal signals. Together these are substantially more useful than a list of additional sensors. Deployment-configuration enumeration and artifact pointers are good safeguards against reviewing design intent alone.

Nevertheless, the seven categories mix transport paths, information sources, and evaluation-validity conditions. Their breadth makes the §9 falsifier weak: almost any missed channel can be fitted retrospectively into infrastructure or memory. Category membership is not completeness evidence. The operational failure criterion should be an upper-accessible input or retained state that is absent from the audited boundary record, or a claimed conditional independence contradicted by an explicit model satisfying the audit's recorded assumptions.

For a bounded minimum deliverable, use one compact register per declared application: receiver/input or retained state; provenance and temporal extent; assignment to X, W, blocked, or unknown; evidence pointer; owner; and consequence of uncertainty. Reconcile that register against actual subscriptions, handles, configuration, and initialization paths. Explicitly check initial state, parameter/configuration loading, and any external command or service inputs; these can fit existing classes without adding more categories. Record inaccessible or unknown evidence honestly. Do not imply that all paths have been certified from a taxonomy alone.

TP-6 is especially valuable and inexpensive. TP-7 is useful as an interpretation warning, but a qualitative ranking must be labeled qualitative: it does not numerically bound either information term. No information estimator or independent sign-off should become a prerequisite for completing this packet's planning inventory.

## Eng-2 non-interference

Preserve D-Prin-3-001 unchanged. Rewrite the proposed “any unknown” consequence as “this particular theorem application remains unsupported,” with no effect on authorization for the Eng-2 spike. Keep separate the result of the engineering harness and whether C-P1-011 supports an interpretation of that result. Require no Prin-5 certificate, attribution calculation, amended claim, independent auditor signature, or optional leak-alarm run before Eng-2 proceeds under its existing gate. The claim adjudicator may later adopt application-specific evidentiary requirements; this review does not enact them.

## Fixed rubric scores

Scores are 1–5, with 5 favorable, including low evidence demand and low justified complexity cost.

| Dimension | Score | Reason |
|---|---:|---|
| Constraint fit | 4 | Delivers the requested planning inventory and preserves claim state; mandatory audit language risks expanding the minimum task. |
| Principle integrity | 3 | Strong grade/governance declarations, but directed-path coverage does not establish the claimed conditional independence; feedback attribution and leak-alarm language overreach. |
| Falsifiability | 3 | Concrete audit questions can fail quickly; the broad-category completeness test is weak and should target omissions in the actual boundary record. |
| Evidence demand | 4 | Mostly document/configuration review with no compute requirement; exhaustive path certification and information attribution could exceed that modest demand. |
| Failure modes | 4 | Excellent coverage of metadata, memory, labels, and hidden access; certificate false assurance and endogenous W need explicit mitigation. |
| Integrability | 4 | Ownership across body loop, scene publication, decision core, and harness is clear; a compact application register would make handoffs more concrete. |
| Latency / criticality | 4 | Correctly places the work in an offline audit; timing channels are recognized without introducing fast-loop processing. |
| Complexity cost | 2 | Seven amendment proposals, exhaustive graph language, independent sign-off, attribution, and a statistical lemma overshoot the priority-2 minimum. Keep the register and defer the rest. |
| Reversibility | 5 | Planning artifacts are cheap to revise or abandon; no implementation or claim transition is performed. |
| Stackability | 4 | Boundary/provenance records support later applications; benefit depends on preventing the audit from becoming a new Eng-2 dependency. |

**Total: 37/50.** Retain the concrete inventory and provenance work; revise the certificate and interpretation claims, bound the minimum deliverable, and defer the optional lemma. Claim adjudication remains separate.
