# C-Prin2-E10 — S2a → S1

- **Packet / author:** Prin-2 / Author B (Astra family).
- **Claim adjudicator:** Opus family, distinct from the author, per roster; no adjudication performed here.
- **Initial and submitted edge grade:** **Grade 3**. All edges start here under B.8.2; no author promotion is asserted.
- **State:** **Candidate**. **Usage:** quarantined; no necessity gate, theorem-style use or veto.
- **Recommended action:** quarantine-Grade3; prioritize the contact-information upgrade attempt.
- **Upgrade target considered:** Grade 1 information lower bound survives ablation; stage-edge bridge remains open.

## Edge statement and conclusion shape

Hypothesis under examination: the source stage must precede, or be available to, the destination stage. Acquisition precedence and runtime availability are evaluated separately below. No universal necessity conclusion is established. The broad Grade-3 edge does not yet meet a B.3 impossibility/lower-bound/functional-completeness/invariant conclusion; a conditional kernel is not permission to upgrade the broad edge.

## Explicit premises and unresolved contracts

1. Q1 is unspecified in the sealed material. The proposed narrow variant concerns only contact-conditioned S1 action decisions with a fixed decision time t_d.
2. Two admissible contact worlds z=0 and z=1 have disjoint acceptable action sets A0 and A1 at t_d. Success in each world is at least 1−ε, with 0 ≤ ε < 1/2. Actions are specified at the plant-relevant interface, not merely as upper-layer commands.
3. H contains every observation and internal history capable of influencing that action by t_d: all sensors, commands, priors, memory, embedded feedback and permitted probes. A single controller maps H to actions using the same conditional randomization law in both worlds. Omitted world-dependent mechanics or actuation invalidates this reduction.
4. Let P0 and P1 be the laws of H in those worlds. S2a as an information role could mean access to contact-discriminating history at the required accuracy and deadline. Whether the program's S2a requires an explicit contact estimate, export or localization is unresolved; those stronger contracts are not assumed equivalent.

## Upgrade argument and disposition

Author-derived information kernel: write μ0 and μ1 for the action laws. Since μ0(A0) ≥ 1−ε and A0 is disjoint from A1, μ1(A0) ≤ ε. Therefore TV(μ0, μ1) ≥ 1−2ε. A common stochastic action map cannot increase total variation: for each action event B, its conditional probability g_B(h) lies in [0,1], so |∫g_B dP0−∫g_B dP1| ≤ TV(P0,P1). Taking the supremum over B gives

    TV(P0, P1) ≥ TV(μ0, μ1) ≥ 1 − 2ε.

Here TV(P,Q)=sup_B |P(B)−Q(B)|. In particular identical complete histories cannot support robustly different required actions. This is an implementation-independent Grade-1 candidate kernel under premises 2–3; it uses no biological evidence and no benchmark win. This author derivation is not independent verification.

The kernel is NOT the registered edge's grade. It requires enough joint information, not a contact-estimation module, separately trained stage, designated body export or prior S2a packet. A direct policy can branch on a sensor without estimating Z explicitly. Q1 may also contain contact-insensitive tasks, and some contact tasks admit a common safe action. Until the operational S1/S2a contracts match the kernel without redefining S2a as “whatever successful action uses,” the broad edge stays Grade 3. If matched, only a runtime availability edge is a possible Grade-1 upgrade; acquisition chronology still does not follow.

## Scope and order semantics

This record covers only the named directed edge; it assigns no grade to a whole ladder or to the reverse edge. Evolutionary order, developmental order and engineering order are distinct. No empirical chronology for any of them is established here. A runtime availability dependency, if eventually verified, does not establish which research or training packet must finish first. D-P1-001 remains **Provisional S0a acceptance-gate only**, not a necessity order. No inherited Candidate is treated as a lock.

Candidate bypasses of stronger wording: a direct sensor-to-action policy without an explicit contact estimate; a common conservative action acceptable in both worlds; a contact-free Q1 task. The latter two violate the disjoint-action premise and block generalization, not the narrow bound. Commands, previous probes or embedded feedback omitted from H are premise failures, not exceptions to the inequality.

## Operational test / falsifier and search target

For the kernel, a formal counterexample would specify P0/P1 and a common action kernel with TV(P0,P1)<1−2ε yet both success bounds hold; an algebraic error also defeats it. For stage transfer, specify Q1, A0/A1, ε, t_d and S2a's independently testable contract, then audit all channels in H. Seek Q1 success without that contract, including direct policies and common-action strategies. Evaluate an equal-prior world classifier on the complete decision history as a diagnostic: the bound implies optimal binary error ≤ ε. A trained classifier's failure does not upper-bound the optimal classifier and cannot prove absent information. Exact finite fixtures can enumerate laws and optimal error; general traces cannot certify the bound from accuracy alone.

A successful same-premise destination competence without the independently specified source capability challenges an availability upgrade. A concurrent or reverse development sequence challenges only acquisition precedence unless source absence at runtime is established. Premise failures withdraw the application; they do not refute an accurately scoped conditional theorem. Simulation success proves tested sufficiency only, never universal necessity or hardware transfer.

## Citation ablation

Delete every evolutionary, developmental and anatomical citation or motivation. None is used as a premise in the argument above. The conditional reasoning and the identified missing bridges remain unchanged. **Ablation survives for the analytic attempt, but does not establish the stage edge.** The historical-order fallback loses all necessity force and remains Grade 3. The edge stays quarantined because the upgrade is incomplete, even though the analytic kernel does not depend on biological citations.

## Verification and governance

Outstanding: Fixed Q1 and S2a stage contracts; task-specific disjoint action sets; complete channel audit; independent proof verification and human signature. No recommended-for-lock nomination is made for this edge.

No edge is recommended-for-lock. Grade-1 locking would require an allowed independent proof check and human-lead signature. Grade-2 locking would require the across-class argument, operational realization test, a logged serious failed counterexample search and human-lead signature. All are governed by the distinct claim adjudicator. Candidate claims may guide exploration but cannot veto Eng-1. Agreement among researchers is not grade evidence.

**B.9.6 scope-narrowing ledger:** 1 proposed narrowing: unrestricted S1 to two-world contact-conditioned decisions with disjoint acceptable actions and explicit ε/deadline. Not adjudicated; formal kernel is not a second upgraded edge. Future premise additions and scope repairs must be appended; at the third event require retirement review. The broad quarantined edge has not been silently replaced by its narrow attempt.

**Counterexample search registered/executed here:** no / no. Tests above are prospective specifications, not sealed PLANs or experimental results. No failed-search evidence is claimed.

## Permitted provenance

Run-root `brief.md`, `roster.md`; sealed `packets/Prin-2/source/method-Appendix-B.md`, `Prin-1-decision.md`, `program-ledger-sealed.md`, `summary-astra-on-A.md`, `summary-opus-on-B.md`; inherited `claims/C-P1-001/claim.md` through `003`, and `010` through `012`. References are by inherited ID; linked external or unsealed artifacts were not inspected. The sealed Prin-1 decision governs inherited dispositions where a claim author's earlier recommendation differs.
