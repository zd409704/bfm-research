# C-P1-011 — Prin-5 claim adjudication (tighten-premises / checklist amendments)

Date: 2026-10-22. Role: claim adjudicator under B.9.1, **bound as ALTERNATE**. Adjudicator family: Claude Opus. Disposition: **Candidate stay, Grade 1 (narrow conditional DPI invariant only); tighten-premises accepted as listed below.** No recommended-for-lock and no retire-nominate. No Locked Grade-1 is asserted, no Eng-2 gate is added, and no spike is run or registered.

## Binding and role-separation disclosure

- **Alternate binding.** Under the roster, the claim adjudicator for Opus-authored claims is Codex gpt-6-astra. Prin-5 score-pass1 §5 follow-up 4 flagged that the Recommend proposal (B) was written by the same family (Astra) as that usual adjudicator, so ruling on B-derived amendment text would be a self-family review. I am bound as the alternate for this ruling only. The roster binding is otherwise unchanged.
- **Family relationships.** The claim author is Opus (P1 Proposal A, and the Prin-1 record compiled by Author A, Opus). I am also Opus, so **this ruling is same-family with respect to the claim author.** Opus authored neither Prin-5 proposal B nor the Prin-1 ruling. The **Recommend-B amendment text is cross-family to me** (Astra author, Opus adjudicator). The **Alternate-A merge text (TP-1..7, channel classes) is same-family to me** (Opus author, Opus adjudicator). I authored neither proposal. I treat A-derived text with extra scrutiny, and I record the same-family relationship with the claim author as a confound in place of the normal cross-family guarantee. This is acceptable here because nothing in this ruling raises the grade or the state. A human lead may re-bind and re-rule.
- This ruling is not B.9.2 verification. It does not substitute for the independent item-by-item theorem match or the human signature.

## Evidence read

`claims/C-P1-011/claim.md`, `upgrade-log.md`, `violations.md`; `packets/Prin-5/decision.md`; `packets/Prin-5/proposals/B.md` (Recommend); `packets/Prin-5/proposals/A.md` (Alternate merge source); `packets/Prin-5/adjudication/score-pass1.md` §4–§5; `packets/Prin-5/source/method-Appendix-B.md` B.9; `roster.md`. I also used `packets/Prin-1/adjudication/ruling-C-P1-011.md` and `summary-astra-on-A.md` for counter reconciliation. I did not inspect a target-stack architecture or a published theorem source.

**Paper checks I performed** (arithmetic only, not B.9.2 verification):
- B §3 XOR case: `I(Z;X)=0`, `I(Z;W)=0`, `I(Z;X,W)=1` bit. Correct.
- B §3 seed-feedback case: correct. `U=R=Z` violates "U independent of Z given X", so the seed must be in `W`.
- B's incremental form `I(Z;Y|W) ≤ I(Z;X|W)` under `Z→(X,W)→Y`. Correct by the chain rule.
- The sufficient condition for the export-only form is `Y=f(X,W,U)` with `(W,U) ⊥ Z | X` (score-pass1 §4.4). Correct.

## Amendment rulings

"Event" means an accepted B.9.6 event in this adjudication. Each item is counted individually. A's request to bundle the items, or to count them as zero, carries no weight (score-pass1 §5.2). The test I apply is B.9.6 as written: does the item narrow the claim's scope, or add a premise so the claim can survive a counterexample? Corrections that remove false or overstrong wording, and rules for how an application audit is conducted, are not narrowings of the theorem. Rejected and deferred text is not silently incorporated.

### Recommend B — §4 checklist (renumbered B-1..B-11 per score-pass1 §4.7)

| # | Amendment | Ruling | B.9.6 | Reason / operative boundary |
|---|---|---|---|---|
| B-1 | Define the target and two time boundaries: `Z`, resolution, target interval, recipient, information cutoff `t`, online/retrospective mode; history declared in `X_t` or `W_t` | **Accept** (into premise 1, statement) | No new event: implements Prin-1 event #1 (define `Z`; time windows) | This removes an implicit same-window restriction rather than adding one. The theorem is unchanged; only the declaration becomes precise. |
| B-2 | State both Markov premises: joint `Z→(X_t,W_t)→Y_t`; export-only `Z→X_t→Y_t`, which needs separate justification; naming `W_t` does not establish completeness | **Accept** (premise 2) | No new event: Prin-1 already required the explicit joint Markov condition (event #1) | Adopt the sufficient constructions: joint form `Y_t=f(X_t,W_t,U)`, `U ⊥ Z | (X_t,W_t)`; export-only form `(W_t,U) ⊥ Z | X_t` (score-pass1 §4.4). |
| B-3 | Replace "independent channel" with "additional accessible information"; replace the absolute-recovery wording in the conclusion with the MI bound | **Accept** (statement, conclusion, scope) | No event: a correction (Prin-1 justification 3). It widens what must be counted in `W`; it restricts nothing | Statistical independence from `X` is neither required nor typical. The XOR case shows jointly informative channels. |
| B-4 | Audit joint access, not individual correlation; marginal screening cannot justify exclusion | **Accept** (premise 3; application-audit rule) | No event | Supported by the XOR case. |
| B-5 | Account for feedback and internal random state: a seed that shapes contact is not independent noise | **Accept** (premises 2–3) | No new event: within event #1 ("causal feedback accounted for") | The clause "or narrow the application to an observation-only setting; log any narrowing" is accepted only as a *procedure*. Adopting any such narrowing in future is a separate B.9.6 event. None is adopted now. |
| B-6 | One probability law per assertion; replace "does not change between deployment and evaluation" with a re-audit on change | **Accept** (premise 4) | No event: corrects an overstrong premise | Both sides of a comparison use the same law. A distribution change triggers a new application audit, not a theorem failure. |
| B-7 | "Cannot increase", not "lowers"; account for adaptive parameters, timestamps, retained samples and auxiliary inputs before invoking P5/H4 | **Accept**, merged with A TP-5 (premise 5) | No event: a correction (equality is possible) | See TP-5 below. |
| B-8 | Preserve exclusions (estimator error, latency, sufficient export, mandatory signals, ladder edge, research order) | **Accept** | No event: restates existing scope | No change to H3. D-P1-001 and the P1 Alternate are not upgraded. |
| B-9 | Separate the structural argument from observations: traces expose bypasses but cannot prove absence; MI estimates and prediction success cannot certify conditional independence | **Accept** (falsifier / application evidence) | No event | Added to the falsifier section. |
| B-10 | Reconcile the record's "recommended-for-lock (conditional)" with the ledger's Candidate / tighten-premises | **Accept: reconciled here** | No event | See "State and reconciliation". |
| B-11 | Have an authorized, role-separated adjudicator do the B.9.6 accounting | **Accept: performed here** under alternate binding | — | See "Counter reconciliation". |

### Recommend B — certificate, inventory and outcomes (§1, §2, §5)

| Item | Ruling | B.9.6 | Note |
|---|---|---|---|
| Application record (target, recipient/cutoff, `X_t`, `W_t`, `Y_t`, model, evidence version) | **Accept as the application-audit object** | No event | This is not a theorem premise. It is the form in which premises 1–4 are declared for a stack. |
| B01–B08 access-class inventory with default disposition **unresolved** | **Accept as audit content** | No event | "Unchecked" or "unknown" never means "absent". |
| Three outcomes (export-only justified / joint-channel justified / unresolved) | **Accept** | No event | These describe evidence for one application. They are not claim lifecycle states and do not block Eng-2. |
| Anti-vacuity rule (no `W_t=Y_t`; inventory primitive inputs independently of `Y_t`) | **Accept** | No event | |
| Incremental bound `I(Z;Y_t|W_t) ≤ I(Z;X_t|W_t)` | **Note; not adopted into the claim statement** | — | Paper-checked here. Adding it to the claim would be a new consequence that needs its own B.9.2 check. |
| Mandatory amendment 1 (score-pass1 §4): frozen, versioned manifest; a later bypass is a B.9.4(b) premise failure; time-box for "unresolved" | **Accept manifest and B.9.4(b) routing; defer the time-box value** to the human lead | No event | I set no deadline number. |
| Mandatory amendment 2: falsifiable checklist failure criterion | **Accept** (falsifier section) | No event | |
| Mandatory amendment 3: triage B03/B04 first | **Accept as audit sequencing only** | No event | Not a necessity order (B.8.3). |
| Mandatory amendment 5: (a) upper layer sets export parameters, so `X` depends on earlier `Y`; (b) composite recipients | **Accept as inventory rows** (extend B03 and B02) | No event | For (a), the inputs to `Y_{<t}` must be inside the declared tuple. For (b), declare the recipient boundary, and treat upstream modules' inputs as access. |
| Mandatory amendment 8: "unknown ⇒ may not be cited" becomes "this application remains unsupported"; nothing in Prin-5 is required before Eng-2 | **Accept** | No event | |
| Mandatory amendment 9: C-Eng1-A-01 / C-Eng2-A-01 cross-reference placeholders | **Accept as cross-reference only** | No event | No ruling on those claims. No execution condition. |

### Alternate A — merged channel classes and TP-1..7

A's table lists **seven** items (TP-1..TP-7). Its prose says "six". I rule on all seven (score-pass1 §5.2).

| # | Amendment | Ruling | B.9.6 | Reason / operative boundary |
|---|---|---|---|---|
| TP-1 | Label provenance `L` in premise 1; the application is *definitional* if `Z=h(X_t)` or `Z=h(W_t)`; L2 (simulator vs proxy label = different `Z`); L3 (pre-register window/resolution) | **Accept** as a declaration item in premise 1 plus an application rule. It is not a theorem premise (§5 follow-up 6) | No event | DPI still holds when `Z=h(X)`; the bound is then tight by construction. The rule governs interpretation; it excludes nothing. |
| TP-2 | Path certificate on the time-unrolled graph: every directed path from `{Z,S,B,L}` into `Y` crosses `X`, is placed in `W`, or is shown blocked | **Accept the path enumeration as audit content inside B's certificate. Reject the "d-separation certificate" wording** | No event | Directed-path coverage is a useful search procedure. It is not by itself a proof of the conditional independence (shared exogenous noise, selection). The Markov premise must still be argued as in B-2. |
| TP-3 | `X` is the *realized* boundary stream: values, timestamps, ordering, drops, mode/fault/saturation flags, schema presence. A `B`-stream reaching `Y` outside the interface enlarges `X` or goes to `W` | **Accept** (premise 2 declaration; merged with B01 and S5) | No event | This enlarges the declared tuple rather than shrinking the scope. A payload-only ceiling needs a separate metadata argument (B01). |
| TP-4 | `W` minimum: (i) upper-layer outputs/efference over and before the window; (ii) persisted memory; (iii) learned parameters when train/eval are not independent; one model per application | **Accept (i), (ii) and the one-model rule. Accept (iii) with B05's qualification**: condition on genuinely fixed configuration and put run-varying state in `W_t`. **Reject the label "TP-4 violation"** for train/eval overlap | No new event: (i) and (ii) implement premise 3 / event #1 | Overlap is an accounting item (`θ` in `W_t` under the stated sampling model), not a violation (§5 follow-up 7, M3). |
| TP-5 | Processing bound covers processing whose control is independent of `Z` given its input; event-triggered or adaptive sampling patterns are information inside `X` | **Accept**, merged with B-7 | No event: a clarification (§5 follow-up 5) | The sampling pattern is part of the declared realized `X_t`. It is not a removal, and the bound is unchanged. |
| TP-6 | H4: `I(Z; I1∪I2)=I(Z;I1)` only if I2 is a function of the *published* I1 transcript and fixed configuration | **Accept** (H4 corrected) | No event: corrects an overstated hygiene note. The statement and scope are untouched, and the change was not prompted by a counterexample (§5 follow-up 5) | |
| TP-7 | Attribution usage rule: report `I(Z;W)` vs `I(Z;X|W)` | **Accept the negative rule only**: when `W_t` is non-empty, do not cite `I(Z;X_t)` as the upper layer's ceiling unless an export-only outcome is justified. **Defer the mandatory attribution report.** Any attribution that is given must be labelled "observational incremental information", not causal contribution, and a qualitative ranking must be labelled qualitative (score-pass1 §4.11) | No event: a usage rule | The decision rejected the attribution reading as written. |
| I1 (ground-truth/debug access blocked) | Policy statement | **Accept as an application-audit rule** | No event | A live `Z→Y` edge makes the application unsupported. It is not a theorem premise (§5 follow-up 7). |
| A §3 E/T/S/M/I/L/D rows | Channel classes | **Accept as merged inventory sub-rows** under B01–B08 | No event | |
| A §5 item 13 (independent sign-off) | Audit sign-off | **Accept for application audits only.** It is not an Eng-2 condition | No event | |
| A §6 leak-alarm lemma | Optional sub-item | **Defer.** **Reject** the "≥1−2α" posterior-style wording | No event | If revived, it needs its own claim record, a joint coverage specification for the TPR/FPR bounds, and wording as a controlled false-alarm test (score-pass1 §4.10). It is not a gate. |

## Counter reconciliation (B.9.6)

The upgrade log's "Accepted narrowings: **0** (1 proposed premise clarification, pending ruling)" is stale. The Prin-1 cross-family ruling (`packets/Prin-1/adjudication/ruling-C-P1-011.md`, justification 5; summary line 13) accepted the definition, side-channel and ordering repairs as **event #1**. That was never logged in the upgrade log, so I append the reconciliation rather than rewriting history.

- Prior accepted: **1** (Prin-1 event #1).
- New accepted in Prin-5: **0**. Every accepted item is a correction of overstrong or false wording, an implementation of event #1, or an application-audit or usage rule. None restricts the theorem's scope, and none was added to survive a counterexample. `violations.md` has no entries.
- **Cumulative: 1.** Retirement review triggers at the third accepted event, so it is not triggered.
- **Prospective items that would count if adopted later:** any narrowing to an observation-only setting (B-5); any exclusion of a recipient class or channel class from the theorem's scope; any premise added in response to an admitted B.9.4 challenge.

## State and reconciliation

- Ruling: **tighten-premises accepted → Candidate stay, Grade 1** (narrow conditional DPI invariant only).
- **Not recommended-for-lock.** The independent B.9.2 item-by-item match to the published DPI statement, for the *amended* statement and premises, is outstanding, and so is the human lead's signature. The tightened text is now in a form that can be checked. After that check, a cross-family adjudicator may reconsider recommended-for-lock.
- **Not retire-nominate.** There is no admitted counterexample or premise failure, and the counter is 1.
- **Record reconciliation (B-10).** The claim file's "recommended-for-lock (narrow form only), conditional on tighten-premises" was the author's recommendation. The adjudicated dispositions are Prin-1 "tighten-premises-then-Candidate-stay" and this ruling, "Candidate stay". The ledger entry "Candidate; tighten-premises" can now read "Candidate; premises tightened (Prin-5)". I do not edit the ledger; the orchestrator should.
- **Programmatic force (H5)** still depends on an application audit of a real target stack. No audit has been performed. Every target-specific disposition is **unresolved**.

## Bindings unchanged

D-Prin-3-001 remains the only Eng-2 gate. Unresolved inventory outcomes do not block Eng-2. No certificate, attribution, sign-off or lemma run is required before Eng-2. D-P1-001 and the P1 Alternate are not upgraded. C-P1-012, C-Eng1-A-01 and C-Eng2-A-01 are not ruled on.

## Record changes (staged as PENDING: claim files are sealed, mode 444)

`claim.md` and `upgrade-log.md` are read-only. I did not unseal them. Following the `C-P1-001/adjudication-prin4` precedent, the edits are staged in this folder for an authorized actor (the orchestrator) to apply and then re-seal:

- `pending-claim.md`: full replacement for `claim.md`. It contains minimal edits to the statement, premises 1–5, conclusion shape, one falsifier bullet, H4, the adjudicator and state rows, and the recommended-action reconciliation, all from accepted text only. `pending-claim.diff` is the unified diff.
- `pending-upgrade-log-append.md`: append-only rows 2–3, the counter correction, and the prerequisite status.
- `violations.md`: no change.

When the edits are applied, record that in `APPLIED.md` here.
