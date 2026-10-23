# C-P1-002 — Timely body-response role

- **Origin:** B-N2; inherited C-P1-002.
- **Author family:** Astra (P1 Proposal B)
- **Grade:** 2, structural candidate with tightened premises.
- **Current state:** Candidate; no veto or lock authority.
- **Recommended adjudicator action:** tighten-premises.

## Premises

1. Fix a target-plant model, initial-state set, body envelope, disturbance set, actuator authority and observation/actuation channels. Declare whether certification is per support mode; do not pool modes without justification. None of these hardware-specific quantities is established by the scalar fixture alone.
2. The competence sought is robust maintenance of that envelope under all declared disturbances over the declared horizon. The envelope is feasible for some allowed response mechanism; faster response alone cannot repair inadequate authority.
3. There is an admissible pair of initially hidden disturbances and a finite deadline T such that the sets of safe **total corrective generalized-force histories** on [0,T], computed for the fixed plant and resources, are disjoint between the two worlds. This incompatibility must be established from dynamics/reachability or another independent argument, not inferred from one controller's failure.
4. Total corrective force includes all active actuator feedback and all state-dependent mechanical restoring/dissipative forces that can affect the envelope. The exogenous disturbance itself is excluded. Hidden embedded feedback and passive forces must be accounted for. If fixed passive mechanics permit a common safe force history, premise 3 fails and no active correction requirement follows.
5. Every permitted source of timely force variation is included in the assessment. Body-local means available at the body's relevant response deadline; it does not require a dedicated module, physical processor location, separate process, or a particular controller family. Where upper-layer interruption is part of the declared disturbance/resource envelope, availability must also be tested during that interruption; no new universal stall premise is imported.

## Conclusion shape and tightened role

**Conditional functional completeness:** any implementation satisfying these premises and the robust envelope must realize world-dependent corrective force histories early enough to avoid the incompatible-history deadline. Otherwise it supplies a common history, which cannot belong to both disjoint safe-history sets. This argument motivates the role across implementation classes; the general target-plant premise and realization evidence remain unverified.

Replace “or an equivalent physical mechanism” with this measurable definition: a mechanical realization counts only when measured state-dependent restoring/dissipative forces supply the requisite differing histories within the same declared envelope and deadline. Active actuator feedback, embedded control, distributed feedback and passive mechanics are possible realizations, not mandatory architectures. A larger tolerance, reduced disturbance class or changed dynamics is an explicit premise/version change, not an untested equivalent mechanism. Successful behavior alone does not identify a hidden role.

## Scope

Generic home humanoid / target plant, restricted to an explicitly specified feasible envelope and verified incompatible disturbance pair. This is a conditional target-plant role candidate, not hardware certification. C-P1-001 supplies one scalar-fixture example of incompatible common inputs, not the missing target-plant premise match. No unique reflex, impedance, control frequency or anatomical module is necessary by this record.

## Operational realization and absence test

Before testing, specify the paired disturbances, matched initial conditions, horizon T, required force-history separation, sensor/force measurement error and temporal resolution from the chosen plant. Record disturbance, body state and total corrective force, including passive contributions, with a common clock. A claimed realization must produce measured world-dependent force histories within the deadline and meet the envelope on the registered probes; comparison tolerances must resolve the required separation. Use replay or channel interventions to remove the proposed differentiating response, preserving the declared plant and recording any intervention-induced premise change. Test passive-only and existing embedded-control realizations as seriously as a new controller.

The named role is absent in a valid probe if total corrective histories remain indistinguishable within the predeclared resolution throughout the necessary response window, or differentiation arrives too late. Missing force instrumentation makes realization unestablished, not proven absent. Finite successful probes validate only tested realization; they do not establish universal necessity. Envelope success while the role is demonstrably absent under matched premises is the counterexample target.

## Falsifier / challenge mode

Construct a system satisfying the same plant/envelope/resource premises and the independently established incompatible-history condition, yet meeting the robust task without timely differentiating corrective forces. Supply force/state traces and measurement bounds, or expose an error in the incompatible-history argument. A passive stabilizer that succeeds must be assessed as either a measured force-response realization or a failure of the fixed-plant/incompatibility premise, not dismissed by definition. If safe common histories exist, withdraw the target application of this claim. If the role cannot be operationally distinguished from mere success, downgrade rather than retain unfalsifiable necessity language.

## P1 decision hygiene

This tightening directly addresses the mandatory B-N2 tighten-or-downgrade amendment. It remains pending adjudicator acceptance. D-P1-001 is **Provisional**, an S0a acceptance-gate recommendation only; S0a is bounded-response viability and S0b retains remaining reflex/impedance content. No necessity order of research or training follows.

The mandatory discriminating total-delay sweep across approximately 2–20 ms must include off-grid disturbance onsets, noise, actuator lag, a humanoid-plausible mode near a=3.3 s^-1 and a joint-level mode. The sealed decision's reported PASS supports the scalar harness only; no completed hardware or role-absence experiment is asserted. 250 Hz / 1 kHz remain placeholders pending mode-specific deadlines. An envelope owner, approval/version path and support-mode scope remain required before implementation acceptance. Existing passive or embedded mechanisms may already discharge the role. Potential support-mode dependence on contact distinguishability remains unresolved, not a reason to prohibit other research.

Citation-ablation: removing evolutionary/anatomical motivation leaves the conditional incompatible-history argument unchanged. Evolution supplies no target-plant premise or grade upgrade.

## Governance and counterexample search

The roster assigns an Opus-family adjudicator distinct from the Astra author. Grade-2 locking requires an implementation-independent argument, an operational test, a logged serious failed counterexample search and human-lead signature. The supplied record does not satisfy all these gates, and researcher agreement changes no grade.

**Counterexample-search spike registered? No.** Future PLAN: for one fixed feasible target mode, compare passive-only, embedded-feedback and active-controller realizations; seek verified envelope success with no timely force-history differentiation, preregistering premise checks, force-resolution limits and counterexample criteria before execution.

## Sealed provenance

`packets/Prin-1/source/P1-proposal-B.md` (B-N2); `P1-decision.md`; `inherited-ledger-P1.md`; `method-Appendix-B.md` (B.2–B.9); run-root `brief.md` and `roster.md`. Short source filenames denote the same sealed source directory. No referenced external evidence was inspected.
