from pathlib import Path
import shutil

root=Path('/srv/claude/research/life-sensorimotor-2026-10-22-principle')
draft=root/'packets/Prin-2/drafts/B'
ids=(draft/'allocation.txt').read_text().splitlines()

edges=[
 dict(edge='S0a → S0b', action='quarantine-Grade3; do not impose acquisition order', target='Grade 2 availability argument considered; unsupported as a stage edge',
 premises='''1. S0a means bounded-response viability; S0b means the remaining reflex/impedance content, as delimited in C-P1-001/002. Neither definition supplies an acquisition chronology.
2. A proposed S0b competence must specify a plant, operating mode, envelope, disturbances, actuator authority and input/output contract. These are not fixed for the target plant in the sealed material.
3. The edge hypothesis is that S0a must precede, or be available to, an implementation of that S0b competence. It is not an accepted premise.
4. Existing mechanics, embedded feedback and a concurrently developed controller are admissible unless an independently justified resource restriction excludes them.''',
 argument='''The strongest proposed argument is that a reflex/impedance experiment must preserve a viable body envelope. That can be a legitimate acceptance requirement. It does not show that a separately acquired S0a capability is an input to S0b. An S0b controller can itself establish bounded response; composing that controller and the plant can produce S0a as an outcome.

C-P1-010 constrains a narrow implementation class and a specified passivity objective; it neither establishes target-plant viability nor orders two research stages. C-P1-001 is similarly a conditional scalar constraint. Promoting their conclusions to this edge loses their premises and reverses a possible realization relation. No Grade-2 edge upgrade is supported.''',
 boundary='''Candidate bypass construction, not an executed result: design a joint impedance controller and demonstrate its envelope and impedance specification in the same analysis. There is no earlier completed S0a packet. This defeats a chronological inference if realized, but still provides bounded response at use time. A passive stabilizing plant also tests whether a distinct S0a acquisition is needed. Neither construction refutes a correctly scoped latency theorem.''',
 test='''First fix the S0b behavioral contract independently of S0a labels. Search for a simultaneous realization that satisfies that contract and its required envelope without an earlier S0a artifact. Measure total applied-force response and envelope traces. To test runtime availability separately, establish which independently measurable S0a property is actually consumed by S0b; ordinary safe execution alone cannot identify this dependency.''',
 missing='A specified S0b competence, target premise match and an independently measurable dependency rather than an acceptance conjunction.',
 narrow='0; no replacement scope proposed.'),
 dict(edge='S0a → S1', action='quarantine-Grade3; retain conditional Grade-2 upgrade attempt for review', target='Grade 2 for runtime availability in a fixed robust S1 task; not acquisition order',
 premises='''1. S1 denotes a task predicate Q1, not an imported stage definition: the permitted sources do not specify its canonical competence contract.
2. For the proposed narrow variant only, Q1 requires a specified target plant to maintain an envelope throughout action under a fixed disturbance and resource set. Whether Q1 actually contains this requirement is unresolved.
3. There must be two admissible worlds indistinguishable to all force-changing channels through a declared deadline τ*, with no common safe corrective-force prefix through that deadline. Verify this from the fixed dynamics; disjoint complete histories alone do not establish a deadline for divergence.
4. All passive, embedded, predictive and distributed mechanisms count. The task must be feasible for some allowed realization; an impossible task cannot establish a useful stage dependency.''',
 argument='''Conditional argument: if the narrow premises hold, a successful realization must obtain enough world-dependent response before τ* to avoid a common unsafe prefix. This applies to learned and classical implementations alike. It motivates the timely-response role discussed in C-P1-002; C-P1-001 supplies only a scalar fixture, not target premises.

Two bridges remain missing. First, neither Q1 nor the target incompatible-prefix condition is established. Second, the necessary response may be realized inside S1, by passive mechanics, or by existing embedded feedback. Calling every such response “S0a” may classify a shared property but proves no separate stage prerequisite. Thus a Grade-2 role argument is plausible, while the registered stage edge remains Grade 3. No iteration of D-P1-001 converts this into a lock.''',
 boundary='''A task on a passively stable or mechanically supported target plant can remove the incompatible-prefix premise. A single controller can establish Q1 and bounded response together. These are explicit candidate failures of transfer or chronology, not verified counterexamples to the conditional role argument. A safe common force prefix in the originally fixed task would defeat the proposed necessity application directly.''',
 test='''Specify Q1, τ*, envelope tolerances, measurement error and force-history resolution before testing. Include active and passive corrective forces in paired-world traces. A valid absence test is failure of total corrective-force histories to diverge by the independently derived necessary deadline; missing force instrumentation means unestablished realization. Search for robust Q1 success with a safe common prefix using passive-only, existing embedded and joint-controller candidates. Replay interventions must preserve the declared plant and channel premises.''',
 missing='Canonical Q1; fixed target mode; independent incompatible-prefix derivation; role-to-S0a mapping; registered serious failed counterexample search and signature.',
 narrow='1 proposed narrowing: from unrestricted S1 to robust envelope-constrained Q1 with verified incompatible prefixes. Not adjudicated; not a grade change.'),
 dict(edge='S0a → S2a', action='quarantine-Grade3; permit observability work without an S0a-order lock', target='Grade 2 for safe online probing only; unsupported for a general contact floor',
 premises='''1. S2a is the proposed contact observability floor: a declared contact variable Z, observation window, error tolerance and decision deadline. Full S2 is not defined or graded by this split.
2. The broad edge says this floor requires prior or available S0a bounded-response viability. No offline/online or active/passive restriction is implicit.
3. A narrow variant would restrict S2a to active online probes on a target plant, with a mandatory body envelope and an independently established incompatible-force-prefix deadline.
4. Contact observations may come from any permitted joint channel: direct sensing, motion history, commands, memory or a body export. Acquisition and safe physical execution are different tasks.''',
 argument='''Contact information can be estimated from recorded trajectories or direct sensing while no new body-response capability is being learned. Information acquisition need not use an unstable active probe. The broad edge therefore lacks a universal dependency.

For a fixed class of active probes, the conditional timely-response argument from C-P1-002 could apply while the probe runs. Its necessity would derive from the probe's envelope and dynamics, not from contact estimation itself. It requires a common-prefix deadline and accounting for passive forces, and still allows concurrent realization. C-P1-011 bounds a joint information channel; it does not supply a viability prerequisite or research chronology. This attempted Grade-2 upgrade is incomplete and the edge remains Grade 3.''',
 boundary='''Candidate bypasses: an offline contact estimator using previously acquired traces; a direct contact sensor on a supported target-plant segment; passive observation during an already viable routine. These may lie outside an eventual active-probing scope, which must be logged rather than silently substituted for the broad edge. None is claimed to have been built here.''',
 test='''Separate an observation-only arm from an active-probe arm with the same Z/error/deadline task. For active probes, measure the total timely-response role using paired worlds, all corrective forces and an independently computed prefix deadline. Search for a safe observation strategy without new S0a work, then for in-premise active probing without the named response role. A detector's accuracy alone does not establish the response dependency.''',
 missing='S2a task contract; evidence that active probing is obligatory for that contract; target viability premises; independently identifiable response role and failed counterexample search.',
 narrow='1 proposed narrowing: general S2a to online active probes with a specified robust envelope. Not adjudicated; no broad-edge upgrade.'),
 dict(edge='S1 → S2a', action='quarantine-Grade3; reject a universal active-action prerequisite', target='Grade 1 information-gain route considered; supplier exclusivity fails',
 premises='''1. Q1 is the unresolved S1 competence predicate. S2a is a specified contact observability floor, with Z, window, error and deadline supplied before testing.
2. The broad hypothesis says satisfying S2a requires S1 to precede or be available. It does not restrict observations to active experiments.
3. A proposed narrow upgrade would need a family in which passive histories cannot separate required Z values but an allowed action can. This property is not established for the target plant.
4. All available sensors, prior observations, command histories and probing mechanisms must be included; “only S1 can probe” cannot be assumed from a stage label.''',
 argument='''Active sensing can be necessary when all passive observation laws coincide and informative interventions exist. That establishes an information-gathering action role for that task, not the complete S1 stage. A simple preprogrammed probe, a local feedback mechanism or direct sensing may supply the missing information without Q1.

There is no sealed proof that S2a always requires active probing, nor a Q1 contract showing that only S1 can supply any required intervention. C-P1-011 does not fill either gap. A Grade-1 information-flow upgrade of the stage edge therefore fails, even though an independently scoped active-information lower bound could be valid. The edge stays quarantined.''',
 boundary='''Directly observe a contact bit at the declared deadline while the target plant is held fixed, or infer Z from existing traces. These are constructive bypass sketches of an action-first inference, conditional on sensor accuracy; no new experimental evidence is asserted. If a probe is required, a fixed diagnostic movement tests whether full Q1 is unnecessary.''',
 test='''Declare Z and absolute competence thresholds. Compare passive observations, a fixed probe and a Q1-driven probe under the same sensing and actuator budget. Establish any passive indistinguishability analytically rather than from an estimator failure. A passive or fixed-probe realization meeting the task without Q1 is a bypass witness; failure of those chosen estimators is not proof of S1 necessity.''',
 missing='A task requiring active information gain, a formal information bound, and a noncircular proof tying the requisite intervention specifically to Q1.',
 narrow='0 adopted; active-only restrictions are a diagnostic upgrade route, not an accepted replacement statement.'),
 dict(edge='S2a → S1', action='quarantine-Grade3; prioritize the contact-information upgrade attempt', target='Grade 1 information lower bound survives ablation; stage-edge bridge remains open',
 premises='''1. Q1 is unspecified in the sealed material. The proposed narrow variant concerns only contact-conditioned S1 action decisions with a fixed decision time t_d.
2. Two admissible contact worlds z=0 and z=1 have disjoint acceptable action sets A0 and A1 at t_d. Success in each world is at least 1−ε, with 0 ≤ ε < 1/2. Actions are specified at the plant-relevant interface, not merely as upper-layer commands.
3. H contains every observation and internal history capable of influencing that action by t_d: all sensors, commands, priors, memory, embedded feedback and permitted probes. A single controller maps H to actions using the same conditional randomization law in both worlds. Omitted world-dependent mechanics or actuation invalidates this reduction.
4. Let P0 and P1 be the laws of H in those worlds. S2a as an information role could mean access to contact-discriminating history at the required accuracy and deadline. Whether the program's S2a requires an explicit contact estimate, export or localization is unresolved; those stronger contracts are not assumed equivalent.''',
 argument='''Author-derived information kernel: write μ0 and μ1 for the action laws. Since μ0(A0) ≥ 1−ε and A0 is disjoint from A1, μ1(A0) ≤ ε. Therefore TV(μ0, μ1) ≥ 1−2ε. A common stochastic action map cannot increase total variation: for each action event B, its conditional probability g_B(h) lies in [0,1], so |∫g_B dP0−∫g_B dP1| ≤ TV(P0,P1). Taking the supremum over B gives

    TV(P0, P1) ≥ TV(μ0, μ1) ≥ 1 − 2ε.

Here TV(P,Q)=sup_B |P(B)−Q(B)|. In particular identical complete histories cannot support robustly different required actions. This is an implementation-independent Grade-1 candidate kernel under premises 2–3; it uses no biological evidence and no benchmark win. This author derivation is not independent verification.

The kernel is NOT the registered edge's grade. It requires enough joint information, not a contact-estimation module, separately trained stage, designated body export or prior S2a packet. A direct policy can branch on a sensor without estimating Z explicitly. Q1 may also contain contact-insensitive tasks, and some contact tasks admit a common safe action. Until the operational S1/S2a contracts match the kernel without redefining S2a as “whatever successful action uses,” the broad edge stays Grade 3. If matched, only a runtime availability edge is a possible Grade-1 upgrade; acquisition chronology still does not follow.''',
 boundary='''Candidate bypasses of stronger wording: a direct sensor-to-action policy without an explicit contact estimate; a common conservative action acceptable in both worlds; a contact-free Q1 task. The latter two violate the disjoint-action premise and block generalization, not the narrow bound. Commands, previous probes or embedded feedback omitted from H are premise failures, not exceptions to the inequality.''',
 test='''For the kernel, a formal counterexample would specify P0/P1 and a common action kernel with TV(P0,P1)<1−2ε yet both success bounds hold; an algebraic error also defeats it. For stage transfer, specify Q1, A0/A1, ε, t_d and S2a's independently testable contract, then audit all channels in H. Seek Q1 success without that contract, including direct policies and common-action strategies. Evaluate an equal-prior world classifier on the complete decision history as a diagnostic: the bound implies optimal binary error ≤ ε. A trained classifier's failure does not upper-bound the optimal classifier and cannot prove absent information. Exact finite fixtures can enumerate laws and optimal error; general traces cannot certify the bound from accuracy alone.''',
 missing='Fixed Q1 and S2a stage contracts; task-specific disjoint action sets; complete channel audit; independent proof verification and human signature. No recommended-for-lock nomination is made for this edge.',
 narrow='1 proposed narrowing: unrestricted S1 to two-world contact-conditioned decisions with disjoint acceptable actions and explicit ε/deadline. Not adjudicated; formal kernel is not a second upgraded edge.'),
 dict(edge='S0b → S1', action='quarantine-Grade3; do not mandate a reflex/impedance package', target='Grade 2 role route considered; implementation-specific content is not obligatory',
 premises='''1. S0b is the remaining reflex/impedance content after the S0a split; no complete mandatory role list is supplied. S1 is an unresolved task predicate Q1.
2. To upgrade, identify a specific function from S0b obligatory for a fixed Q1 competence across allowed implementation classes, and measure it independently of overall success.
3. No particular reflex wiring, impedance controller, update frequency or anatomical arrangement is part of Q1 merely because a planning ladder names it.
4. Physical compliance, direct feedback policies and known-environment solutions are admissible unless the task independently excludes them.''',
 argument='''A Q1 task may require force regulation or timely correction, but neither requirement selects the full S0b package. For the narrow virtual-impedance class, C-P1-010 may constrain sampled rendering; it does not establish that Q1 requires virtual impedance or passivity against every passive environment. C-P1-002 concerns a total response role that can have several realizations.

A valid Grade-2 upgrade would need a concrete role, an across-class obligation argument and an absence test. The supplied S0b/Q1 contracts do not identify that role. Assigning all helpful feedback to S0b would make the edge a relabeling of competence. Grade 3 quarantine remains.''',
 boundary='''Candidate bypasses include a direct action policy with no explicit impedance representation, or physical compliance plus a task controller. A narrow open-loop task in a known environment can test whether any claimed reflex is obligatory. These sketches do not claim robust competence under an unstated disturbance class.''',
 test='''Fix Q1 and a particular S0b role before comparison. Record an observable realization variable and a predeclared absence criterion. Search across direct-policy, physical-compliance and explicit-impedance realizations at the same task/resource envelope. A controller beating another is irrelevant to necessity; a matching-task realization without the operational role is the relevant witness.''',
 missing='An independently defined S0b role, Q1 contract, across-class necessity argument, operational absence criterion and failed registered counterexample search.',
 narrow='0; no accepted narrowing.'),
 dict(edge='S0b → S2a', action='quarantine-Grade3; do not require impedance or reflexes for observation', target='Grade 1 identifiability and Grade 2 probing routes considered; neither selects S0b',
 premises='''1. S2a specifies Z, error, observation window and deadline; S0b denotes remaining reflex/impedance content, not all sensor processing.
2. The edge hypothesis requires that content for contact observability. Passive sensing, direct contact channels and existing recorded observations remain admissible.
3. A proprioceptive estimator may face actuator/contact confounding, but a particular estimator is not the full S2a competence class.
4. For any restricted active-probing task, the probe's dynamics and signal requirements must be established independently of a selected S0b implementation.''',
 argument='''C-P1-012 is an inherited Grade-2 Candidate with rate/source confounds and unresolved target premises; it supplies no necessity for a reflex/impedance stage. Even a sound identifiability argument would require a distinguishing channel, which may be a direct sensor, calibrated actuator model or informative intervention. It would not uniquely select S0b.

If active probing needs controlled forces, the relevant role must be stated and tested across all permitted mechanisms. No such obligatory S0b role has been demonstrated. C-P1-011's joint-channel ceiling likewise concerns accessible information rather than reflex content. The edge remains Grade 3 after these attempted upgrade routes.''',
 boundary='''A direct contact channel can supply Z while the target segment remains fixed. Recorded force/state data can support an offline detector without a newly acquired S0b stage. A fixed probe with independent sensing is another possible bypass. These are analytic construction sketches only; no detector or target-plant experiment was executed.''',
 test='''Specify the contact contract and compare direct sensing, calibrated proprioception and controlled probing with matched resources. For an alleged obligatory S0b role, identify its observable output and how an intervention removes it while preserving the task premises. Success without that role is a bypass witness. Do not infer necessity from a single observer's failure or a higher-rate export's performance advantage.''',
 missing='A contact task whose observability requires an independently specified S0b role; exclusion of alternative channels by real resource premises; operational test and failed registered counterexample search.',
 narrow='0; no replacement scope proposed.')
]

common_scope='''This record covers only the named directed edge; it assigns no grade to a whole ladder or to the reverse edge. Evolutionary order, developmental order and engineering order are distinct. No empirical chronology for any of them is established here. A runtime availability dependency, if eventually verified, does not establish which research or training packet must finish first. D-P1-001 remains **Provisional S0a acceptance-gate only**, not a necessity order. No inherited Candidate is treated as a lock.'''

for cid,e in zip(ids,edges):
    p=draft/'claims'/cid
    p.mkdir(parents=True,exist_ok=True)
    claim=f'''# {cid} — {e['edge']}

- **Packet / author:** Prin-2 / Author B (Astra family).
- **Claim adjudicator:** Opus family, distinct from the author, per roster; no adjudication performed here.
- **Initial and submitted edge grade:** **Grade 3**. All edges start here under B.8.2; no author promotion is asserted.
- **State:** **Candidate**. **Usage:** quarantined; no necessity gate, theorem-style use or veto.
- **Recommended action:** {e['action']}.
- **Upgrade target considered:** {e['target']}.

## Edge statement and conclusion shape

Hypothesis under examination: the source stage must precede, or be available to, the destination stage. Acquisition precedence and runtime availability are evaluated separately below. No universal necessity conclusion is established. The broad Grade-3 edge does not yet meet a B.3 impossibility/lower-bound/functional-completeness/invariant conclusion; a conditional kernel is not permission to upgrade the broad edge.

## Explicit premises and unresolved contracts

{e['premises']}

## Upgrade argument and disposition

{e['argument']}

## Scope and order semantics

{common_scope}

{e['boundary']}

## Operational test / falsifier and search target

{e['test']}

A successful same-premise destination competence without the independently specified source capability challenges an availability upgrade. A concurrent or reverse development sequence challenges only acquisition precedence unless source absence at runtime is established. Premise failures withdraw the application; they do not refute an accurately scoped conditional theorem. Simulation success proves tested sufficiency only, never universal necessity or hardware transfer.

## Citation ablation

Delete every evolutionary, developmental and anatomical citation or motivation. None is used as a premise in the argument above. The conditional reasoning and the identified missing bridges remain unchanged. **Ablation survives for the analytic attempt, but does not establish the stage edge.** The historical-order fallback loses all necessity force and remains Grade 3. The edge stays quarantined because the upgrade is incomplete, even though the analytic kernel does not depend on biological citations.

## Verification and governance

Outstanding: {e['missing']}

No edge is recommended-for-lock. Grade-1 locking would require an allowed independent proof check and human-lead signature. Grade-2 locking would require the across-class argument, operational realization test, a logged serious failed counterexample search and human-lead signature. All are governed by the distinct claim adjudicator. Candidate claims may guide exploration but cannot veto Eng-1. Agreement among researchers is not grade evidence.

**B.9.6 scope-narrowing ledger:** {e['narrow']} Future premise additions and scope repairs must be appended; at the third event require retirement review. The broad quarantined edge has not been silently replaced by its narrow attempt.

**Counterexample search registered/executed here:** no / no. Tests above are prospective specifications, not sealed PLANs or experimental results. No failed-search evidence is claimed.

## Permitted provenance

Run-root `brief.md`, `roster.md`; sealed `packets/Prin-2/source/method-Appendix-B.md`, `Prin-1-decision.md`, `program-ledger-sealed.md`, `summary-astra-on-A.md`, `summary-opus-on-B.md`; inherited `claims/C-P1-001/claim.md` through `003`, and `010` through `012`. References are by inherited ID; linked external or unsealed artifacts were not inspected. The sealed Prin-1 decision governs inherited dispositions where a claim author's earlier recommendation differs.
'''
    log=f'''# {cid} — upgrade log

State throughout: **Candidate**. Edge grade throughout: **Grade 3, quarantined**.

| Event | Attempt / evidence | Outcome |
|---|---|---|
| 0 — registration | One directed edge, {e['edge']}; default B.8.2 grade | Grade 3; no order inferred from packet sequence |
| 1 — analytic assessment | {e['target']} | Author argument in claim.md; no independent check, benchmark promotion or state transition |
| 2 — source exclusivity / stage mapping | Check whether the required property is specifically supplied by the source stage | Missing: {e['missing']} |
| 3 — B.8.7 ablation | Remove evolution/development/anatomy citations | Conditional analysis survives; stage mapping remains unresolved; broad edge does not upgrade |
| 4 — governance disposition | {e['action']} | Candidate-stay; no Eng-1 veto, no recommended-for-lock nomination |

## Counterexample-search status

Only analytic bypass sketches are listed in claim.md and violations.md. No candidate was built, no experiment executed, no serious failed-search result asserted. A future experiment must first seal a PLAN with plant/task/resource premises, operational source-absence criteria, numerical or measurement error, and an explicit counterexample rule. The runner files data; the distinct adjudicator decides grade/state. The prospective test in claim.md is not a completed B.9.2 search.

## Scope-narrowing counter

{e['narrow']}

Count future distinct restrictions separately; the third triggers mandatory review for retirement. A narrowed information or response lemma cannot confer its grade on a broader stage chronology. No inherited claim or its narrowing counter was edited.
'''
    violations=f'''# {cid} — violations and failed-transfer register

## Known executed counterexamples

None supplied or generated here. Absence of a completed counterexample is not support for necessity.

## Concrete bypass candidates and boundary cases

{e['boundary']}

## Attempted transfer that is not warranted

{e['argument']}

## What would count as a violation

{e['test']}

Record exact task, plant, resources, source-stage operational definition, source absence, destination success and error bounds. Distinguish acquisition-order witnesses from availability witnesses. A purported absence that only deletes one named module does not exclude implicit or passive realization. Conversely, do not absorb every successful mechanism into the source stage after observing success; any such redefinition is a logged scope/premise change.

## Misuse prohibitions and disposition

- Do not turn D-P1-001 into a necessity edge lock.
- Do not transfer a fixture bound, joint-channel theorem or implementation-class result to an unaudited target plant.
- Do not use Grade 3 in Eng-1 gates, vetoes or theorem-style requirements.
- Do not use spike PASS, citation survival or researcher agreement as a grade promotion.
- Candidate-stay and quarantine remain in force; no independent reviewer or human signature is asserted.

**B.9.6 count:** {e['narrow']}
'''
    (p/'claim.md').write_text(claim)
    (p/'upgrade-log.md').write_text(log)
    (p/'violations.md').write_text(violations)

rows='\n'.join(f"| [{cid}](../../../claims/{cid}/claim.md) | {e['edge']} | 3, Candidate, quarantined | {e['target']} | {e['action']} |" for cid,e in zip(ids,edges))
proposal=f'''# Prin-2 — Author B proposal: constrain task interfaces before ordering stages

**Thesis:** no proposed stage edge currently has the premises needed to gate Eng-1 as necessity. Register seven directed edges separately, leave all seven **Grade 3 / Candidate / quarantined**, and prioritize the narrow contact-information argument for {ids[4]} and the runtime response arguments for {ids[1]} and {ids[2]}. Their analytic content survives citation ablation; their transfer to stage edges is not yet established. No edge is nominated recommended-for-lock.

The useful distinction is between a property that must be available when a task executes and a stage that must be acquired first. A joint controller can supply several properties at once. A contact decision can consume raw information without a separate contact estimator. Those observations prevent a sound response or information constraint from silently becoming a research chronology.

## Stage contracts and evidence boundary

| Label | Contract used here | Limitation |
|---|---|---|
| S0a | Bounded-response viability, per C-P1-001/002 | A specified plant, mode, envelope and resources are required; no universal frequency or controller follows |
| S0b | Remaining reflex/impedance content after S0a split | No complete mandatory role inventory is present in the permitted sources |
| S1 | An independently specified competence predicate Q1 | The sealed materials do not define canonical S1 content; no locomotion, manipulation or other definition is imported |
| S2a | Proposed split: contact observability floor for variable Z, window, accuracy and deadline | Access to task-relevant information, explicit estimation, localization and a particular export are different contracts |
| S2 | Unsplit broader stage | Not defined by the sealed material; conclusions about S2a do not automatically upgrade or exhaust S2 |

These are explicit working contracts, not amendments to the planning ladder. Missing canonical Q1 is material: a contact-sensitive subset can need information that a contact-free subset does not. The safe conclusion is to retain the edge's starting grade until the subset and stage mapping are independently accepted.

Read boundary: only brief.md, roster.md, the sealed Prin-2 source files, and inherited C-P1 claim.md files were used. No other author's draft or proposal, external literature or unsealed supporting artifact was inspected. Inherited dispositions are taken by ID from the sealed Prin-1 decision; earlier author recommendations inside inherited claims do not supersede that decision.

## Edge claims

| ID | Directed edge | Submitted grade/state | Upgrade attempt | Recommended action |
|---|---|---|---|---|
{rows}

Each row has its own claim.md, upgrade-log.md and violations.md. No reverse edge or transitive edge receives a free upgrade. In particular, simultaneous plausibility of S1 → S2a and S2a → S1 in different task subsets is not a universal cycle or a reason to lock a whole ladder.

## Strongest attempts and why they stop short

**{ids[4]}: S2a → S1.** Fix two contact worlds whose acceptable actions at a deadline are disjoint, and require success at least 1−ε in each. Let H include every observation and history capable of affecting the plant-relevant action. A common action map implies

    TV(P(H|z=0), P(H|z=1)) ≥ 1 − 2ε.

The claim record gives the direct derivation. Indistinguishable histories cannot support different required actions with ε < 1/2. This is a Grade-1 candidate information kernel, independent of model family, historical stories and performance comparisons. It has not received an allowed independent proof check. More fundamentally, it establishes joint information availability, not a separately acquired S2a estimator or designated body export. Stage-contract matching and a complete side-channel audit are missing. **The registered edge stays Grade 3.** A future accepted mapping could support a narrow runtime edge, never acquisition order merely from this proof.

**{ids[1]}: S0a → S1, and {ids[2]}: S0a → S2a.** A fixed robust task may require differing corrective-force histories before a deadline. The proposed Grade-2 role needs incompatible *prefixes*, not just disjoint complete histories, plus an information-structure audit covering passive and embedded mechanisms. C-P1-002 is inherited as Candidate with unresolved premises; C-P1-001 is only its separately scoped fixture reference. For S2a, active online probing must itself be required before that response argument can apply. Offline estimation and passive observation expose the unrestricted edge's gap. Neither attempt proves a prior S0a packet is necessary.

**The remaining four edges.** S0a → S0b confuses a safe-execution acceptance conjunction with a separately acquired prerequisite; S0b may itself realize viability. S1 → S2a lacks proof that active probing is necessary and that only full Q1 can supply it. S0b → S1 and S0b → S2a lack an obligatory, independently testable role that uniquely matches the S0b contract. C-P1-010/011/012 do not repair those gaps. The claim records specify plausible bypasses and prospective tests without representing them as executed experiments.

## Citation ablation and order discipline

Removing evolution, development and anatomy leaves the analytic inequalities, conditional response reasoning and missing-stage diagnoses unchanged. This passes ablation for those arguments; it is necessary discipline, not a sufficient upgrade test. A residual assertion that the stages must follow one another because life did so collapses and stays quarantined, consistent with C-P1-003. Evolutionary, developmental and engineering orders remain distinct; evidence about one transfers to another at Grade 3 at most. No particular historical chronology is verified here.

All seven submitted edges remain Grade 3 and thus quarantined, including the three with promising kernels. They may organize exploration as hypotheses. They cannot appear in theorem-style conclusions, necessity gates or vetoes. A planning choice can still be adopted as an explicit run constraint without acquiring evidential force.

## Gates before ranking; exact Eng-1 consequence

**Edges that can GATE Eng-1 now: none.** Every new edge is Candidate and Grade 3; the sealed Prin-1 decision also supplies no Locked inherited claim. A high rubric score, ablation survival or successful spike cannot fill the B.9 gates.

Before ranking Eng-1 proposals, check actual Locked claims and their scope; the supplied snapshot has none. Preserve **D-P1-001: Provisional S0a acceptance-gate, not necessity order**. Its existing engineering acceptance obligations remain distinct from edge vetoes. Then rank admissible engineering candidates. S2a can be proposed as next work; no completed S1 or S0b stage is required by these records, and no new necessity lock requires finishing S0a research first.

**Edges that could gate later:** a narrowly mapped {ids[4]} could constrain online contact-conditioned decisions if its proof, contracts and channel premises are verified and a Grade-1 lock receives the human signature. A narrowed {ids[1]} or {ids[2]} could require a timely-response role for a specified online task after the full Grade-2 route, serious failed counterexample search and human signature. Such locks would constrain availability during execution, not prohibit concurrent or offline research. No such future condition is treated as satisfied here.

For a prospective S2a-focused Eng-1 proposal, explicitly list the potentially bypassed incoming edges {ids[2]}, {ids[3]}, {ids[6]} and their Grade-3 status when proceeding without their source stages. If it also develops S1 without a prior S2a stage, list {ids[4]}; distinguish chronological bypass from absence of runtime information. Do not infer a transitive veto through S0b.

For engineering review, require concrete task and interface descriptions as ordinary proposal completeness: Z, window, error/latency requirements, full joint-channel inventory, online versus offline operation, target mode and envelope ownership. These are recommendations for testable work, not hidden Principle vetoes. A PLAN should distinguish observation sufficiency from an actual counterexample search. PASS validates its harness and tested realization, not hardware transfer or necessity.

## Adjudication requests and scope governance

Request Candidate-stay with quarantine for all seven records; ask the distinct adjudicator to assess the proposed narrow variants without transferring their grades to the broad edges. No independent verification, serious failed counterexample search or human signature is supplied. Grade-1 and Grade-2 locks both require their respective B.9.2 route and human signature. No author may sign its own transition.

The logs count one proposed narrowing each for {ids[1]}, {ids[2]} and {ids[4]}; none is an accepted replacement or a grade change. Other edges have zero accepted/proposed replacement events as recorded. Future distinct repairs must be counted, with mandatory retirement review at the third. Do not quietly define the source stage as whatever a successful destination happened to use.

The bounded next step is stage-contract adjudication and task-specific counterexample PLANs. Honest unresolved edges leave Eng-1 room to test interfaces without pretending that a planning ladder is already a law.
'''
(draft/'proposal.md').write_text(proposal)
index='''# Prin-2 Author B — edge index

All IDs were allocated by exclusive directory creation; existing even-numbered directories were skipped. No odd-numbered claim or other-author path was changed.

All seven records are **Grade 3 / Candidate / quarantined**. No recommended-for-lock nomination; no current Eng-1 necessity gate.

| ID | Edge | Grade | Recommended action |
|---|---|---|---|
'''+ '\n'.join(f"| [{cid}](../../../../claims/{cid}/claim.md) | {e['edge']} | 3 | {e['action']} |" for cid,e in zip(ids,edges))+f'''

Priority upgrade attempts: {ids[4]} (conditional Grade-1 information kernel; stage mapping unresolved), {ids[1]} and {ids[2]} (conditional Grade-2 timely-response roles; premises and stage mapping unresolved). These target grades do not change the submitted edge grades.

Final proposal: [proposals/B.md](../../proposals/B.md). Each claim directory contains claim.md, upgrade-log.md and violations.md; draft copies are in this directory's claims/ subtree. D-P1-001 remains Provisional S0a acceptance-gate only. No experiment was run.
'''
(draft/'edge-index.md').write_text(index)
# Drafts are complete before final copies are published to the authorized paths.
for cid in ids:
    dest=root/'claims'/cid
    if any(dest.iterdir()):
        raise RuntimeError('Allocated destination is no longer empty: '+str(dest))
    for name in ('claim.md','upgrade-log.md','violations.md'):
        shutil.copyfile(draft/'claims'/cid/name,dest/name)
(root/'packets/Prin-2/proposals').mkdir(parents=True,exist_ok=True)
shutil.copyfile(draft/'proposal.md',root/'packets/Prin-2/proposals/B.md')
print('Wrote proposal, edge index and '+str(len(ids))+' claim triplets after drafting.')
