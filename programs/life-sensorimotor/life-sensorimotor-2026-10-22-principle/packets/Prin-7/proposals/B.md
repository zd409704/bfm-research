# Prin-7 — Proposal B: bounded ambiguity with a separation refuter

**LABEL=B. PLAN only; no search, proof check, simulation, or spike executed.**

**Disposition requested:** select a prospective identifiability work plan. C-P1-012 remains **Grade 2, Candidate**. Its Grade-1 form remains an open upgrade target. No claim amendment, lock recommendation, retirement nomination, or Eng-2 gate change is requested.

## 1. Decision and distinct approach

Attempt a narrow, quantitative impossibility result for **contact-event detection**, using two bounded sets of admissible observation histories. Ask whether a no-contact history and a contact history can coincide. Give the refuter equal standing: an exact certificate that these sets are disjoint, together with a detector that separates them.

The distinguishing choice is to bound actuator nuisance *before* looking for ambiguity. Do not assume that nuisance can absorb any contact signal, infer nonidentifiability from shared frequency content, or declare a particular effort sensor necessary. A bounded nuisance model can support either ambiguity or separation. Report both regimes without selecting only the favorable regime.

This targets Factor E at one fixed observation rate. Factor R, localization, hardware competence, the Grade-2 role, and research ordering are separate conclusions. An inability to identify the full contact force does not by itself establish an inability to detect an event; the proposed pair must have different **event labels**.

## 2. Admissible model class to freeze before future work

Use the following deliberately small exact mechanical family as a formal test case, not as an asserted approximation theorem for the target plant:

`M q̈(t) = u(t) + n_up(t) + n_down(t) + g(t)`.

| Item | Prospective declaration |
|---|---|
| Plant | Two joint coordinates, `M = diag(1,2)` in consistent units; known gravity compensation, no other unmodeled dynamics; fixed known initial position and velocity. No stance/foot contact. |
| Time | A 200 ms trial; elementary intervals of 5 ms. Inputs are constant on each elementary interval, with exact continuous integration between boundaries. No numerical integrator error is part of the model. |
| Command | A fixed, known zero command for the primary theorem attempt. Full command history is available. This is a passive finite-horizon result, not a theorem over actively probing controllers. |
| Contact | Null: `g=0`. Alternative: onset at 100 ms; duration in `{10,20,50,100}` ms; `g=a s e_j` during the event, zero otherwise, where `a∈[1,2]`, `s∈{-1,+1}`, and `j∈{1,2}`. These are declared generalized non-foot contact torques. Force-to-torque mapping and fixed contact location are idealized by each direction `s e_j`. |
| Nuisance | For each channel separately, `|n_i[k]|≤b` and `|n_i[k+1]-n_i[k]|≤1`, componentwise, including the transition from a fixed zero pretrial nuisance. Parameters and initial conditions are identical in the two worlds; the unknown nuisance trajectory may differ. |
| Primary nuisance budget | Total nuisance bound `b=1`, allocated to one channel as specified below. This primary cell is selected now, independently of any result. |
| Boundary cells | Repeat the same prospective audit for `b∈{0,1/4,1/2,2}`. These are separate model classes, not permission to revise the primary cell after failure. |
| Baseline observation | Exact samples `(q,q̇,u)` every 5 ms, including the initial sample and all samples through the decision deadline. No current, torque, tactile, force, vision, hidden state, contact labels, simulator metadata, or unregistered training trace is accessible. |
| Prior history | Fixed identical reset history, available to the detector. No unknown persistent parameter is learned from undeclared earlier trials. |

Within every budget, retain two placement variants: **U**, `n_up=n`, `n_down=0`; and **D**, `n_up=0`, `n_down=n`. A hypothetical motor-side effort measurement is `a_motor=u+n_up`. It contains the nuisance in U and excludes it in D. A hypothetical net non-contact joint-effort measurement would be `a_joint=u+n_up+n_down`. The latter is a mathematical channel definition; no physical device is assumed to implement it. Any proposed actual measurement must pass a separate placement and provenance audit.

The nuisance family describes bounded additive disturbances, not automatically Coulomb friction, saturation, or transmission losses. If one of those mechanisms is invoked, its constitutive law and placement must be matched explicitly; a free disturbance sequence cannot masquerade as a friction model. Failure of this match limits target relevance even if the formal result is correct.

These contact classes belong only to this proposed formal fixture. They do not replace or filter the inherited factorial classes, remove d50_M10, or change any filed thresholds.

## 3. Observation sets, quantifiers, and intended conclusion

For each fixed budget and placement, future work will derive the exact finite-dimensional observation map by integrating the declared dynamics. After subtracting the common command response, write it as

`y = L(n + g)`.

`L` includes **both** position and velocity samples, the entire allowed history, and the 200 ms deadline. Nuisance trajectories form a bounded rational polytope `N_b`. Each duration/direction contact cell forms a rational polytope `G_j`; the contact alternative is their finite union, not its convex hull.

Define `Y0 = {Ln : n∈N_b}` and `Y1,j = {L(n+g) : n∈N_b, g∈G_j}`. The primary conjecture to investigate is that, for the preselected `b=1` class, there is an admissible event/no-event collision in each declared contact cell. Each cell receives its own verdict; one collision already obstructs a uniform all-class detector, but does not establish ambiguity for every cell.

The prospective proof obligation is to construct and independently check `n0,n1,g` with `g∈G_j`, all bounds satisfied, and

`L(n0) = L(n1+g)`.

This is a certificate specification, not a pair constructed or checked in this packet. Equality only at the final position, equality only in expectation, or contact/contact ambiguity is insufficient.

For a certified pair, the proposed conclusion is: **every detector using the permitted transcript, including randomized detectors, has the same alarm probability in those two worlds by the deadline**. The detector's random seed must be independent of the hidden world. This is a worst-case uniform-detection obstruction. It says nothing about average performance under an unspecified distribution of nuisance or contacts.

For an explicit model-level task, prescribe one alarm at most per independently reset 200 ms trial, false-event rate at most `0.01/s`, event TPR at least `0.95`, and p95 latency at most 100 ms from the known candidate onset. The null trial has the same announced candidate onset. A false-alarm probability at most `0.002` per trial enforces that rate under this trial accounting. Misses receive infinite latency; early alarms before onset do not count as detections and count as false events. The full deadline transcript is permitted even to a noncausal decision rule, giving the impossibility attempt the strongest observation available by that deadline. A detected collision would obstruct the stated contract because identical histories cannot support the required different alarm probabilities.

These numbers define a formal trial task, not human-ratified target `(q,r)`, and do not authorize an Eng-2 run. No inference about target p95 latency, real-time computational resources, or hardware transfer follows.

## 4. Refuter and prospective search protocol

After a separate execution authorization and sealing step, the runner would perform this finite, certificate-oriented investigation:

1. Freeze the model, channel manifest, all contact cells, exact units, and theorem wording. Record a content digest. Independently reconstruct `L` before testing it.
2. For each preregistered budget, placement, and contact cell, solve the linear feasibility problem for an event/no-event collision. Record every cell, including failures and boundary cases. No detector tuning, learning, or hardware is needed.
3. A feasible result requires exact rational witness validation against every bound, sample, initial condition, and event label. Floating-point residuals alone are inconclusive.
4. An infeasible result requires an independently checked exact dual certificate. Construct the corresponding separating functional and validate its strict gap on the two compact observation polytopes. A numerical solver's status alone is inconclusive.
5. For the full finite union, construct a detector that declares contact when any cell's certified separating test fires. Validate every null and contact cell. Do not replace the union by a convex hull: hull overlap can manufacture ambiguity absent from the declared family.
6. File the full certificate bundle and a premise-by-premise audit. Stop at that model-level result. No adaptive expansion of budgets, deletion of durations, or substitution of favorable sensing is allowed within the sealed attempt.

**Refuter of a cell-level impossibility:** a strict separation certificate for that cell and a detector based solely on the allowed transcript. It invalidates the proposed universal impossibility for that cell; another cell's collision must not erase it.

**Refuter of the all-class detection obstruction:** verified separation of the null set from every alternative cell, yielding a uniform detector for the entire declared class and task. In the exact model its false-event probability would be zero, TPR one, and decision latency 100 ms. This is a planned certificate implication, not a reported outcome. It establishes an existence result without implying an efficient online implementation.

**Premise refuter:** a demonstrated violation of the declared access boundary, disturbance law, measurement placement, or target applicability. Such evidence routes separately from detector competence. A physically constrained actuator model that cannot realize the proposed pair defeats that model's premise match; it is not permission to silently broaden the actuator family.

**Proof-error refuter:** an admissible same-history pair whose event probabilities differ under a compliant detector, or a checked counter-model to a claimed implication. Audit hidden information and randomization coupling first; retain a genuine mathematical error as adverse evidence.

Prospective effort cap: one local working day for exact map/certificate construction and one independent review session. At the cap, missing or unverified certificates are **unresolved**, never a failed counterexample search or proof. This packet supplies no code and launches none of these operations.

## 5. What the result would and would not support

A certified collision supports only a narrow information obstruction under the stated model and access boundary. To break that pair, some admitted observation or prior constraint must distinguish the two worlds. It does **not** single out measured effort: a valid actuator law, different permissible history, an independent contact channel, or another informative measurement could do so.

The placement variants make the sensor claim testable rather than definitional. Future channel augmentation could check whether adding `a_motor` removes the collision in U and leaves it in D. Any such extension needs its own frozen observation map and certificates. Distinguishing one pair is not sufficiency for all contacts. Exporting an observer residual may realize the Grade-2 role, but cannot erase a competent Factor-E witness under the inherited falsifier.

No numerical rate floor is attempted here. A later comparison of 5 ms and 20 ms sampling would require its own complete transcript maps, duration/phase class, and task contract. Merely exhibiting a short event between samples, or a collision at one rate, establishes neither a 200 Hz necessity nor superiority of one detector family.

The approach avoids the Grade-2 vacuity problem by testing distinguishability of explicitly listed histories. It does not define every useful body-state export as an effort-information role, nor claim to complete that role's operational audit.

## 6. Governance and handoff

Inherit D-Prin-4-001 priority 4, D-Prin-6-001, and the corrected formal-evidence routing in `source/C-P1-012-prin6-ruling.md`. Use the following routes; they are not tiers:

| Prospective output | Route and limit |
|---|---|
| Checked ambiguity certificate plus proposed theorem | Annotation and independent B.9.2 verification dossier; any grade reassessment needs a separate packet. Reviewer agreement alone is insufficient. |
| Formal counter-model or competent model-level detector | Claim review with premise/artifact audit. Missing target `(q,r)` does not cap model-level review. |
| Target-premise failure | Claim review based on provenance, measurement, and applicability; no competent detector prerequisite. |
| Incomplete certificate or exhausted budget | Annotation of unresolved work; no favorable evidence claim. |
| Proposed restricted reformulation of C-P1-012 | Separate amendment review; no silent replacement of its scope or falsifier. |

The primary author cannot adjudicate this B-authored extension. Bind an independent reviewer and disclose family relationships to both the inherited claim and the new text. Any future Grade-1 lock requires an accepted B.9.2 check and human signature on the exact statement; no such check or signature is supplied here.

Accepted B.9.6 narrowing count remains **1**. This proposed submodel is not an accepted change to C-P1-012. If it is later substituted for the broader claim, the adjudicator must rule on each scope restriction and added survival premise individually. Dropping a falsified factor and excluding its plant model are separate events; reaching three requires retirement review. A zero count requires a written reason.

The registered Factor-E/Factor-R competent-match routes remain operative, including the original full-class rule, absolute task competence, comparison uncertainty requirements, and the common-scope audit for combining witnesses from different runs. Formal nonidentifiability cannot retrospectively rescore the factorial or substitution result. A concrete in-premise witness may reach claim review even if this plan's checklist is incomplete.

No retirement is justified by the supplied materials. C-P1-012 stays **Grade 2, Candidate**; no export field, numeric rate, or ladder order becomes mandatory. D-Prin-3-001 and D-Eng-2-001 remain unchanged, including their human declarations and branch gate. Proposed future artifacts are a frozen model manifest, exact observation map, per-cell certificates, a compliant refuter detector if available, and an independent verification report—not a claim-state edit by the runner.
