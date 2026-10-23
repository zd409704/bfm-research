# Prin-5 — Proposal A: Audit the graph, not the sensor list

**Packet:** Prin-5 (C-P1-011 side-channel / information-access inventory; D-Prin-4-001 priority 2, minimum deliverable)
**Author:** Competing Author A (Claude Opus). Planning artifact only.
**Claim state:** C-P1-011 stays **Candidate**, Grade 1 (narrow form). This proposal changes no grade or state. Claim adjudicators rule on everything below (B.9.1). No Locked Grade-1. No new Eng-2 preconditions: D-Prin-3-001 stays the only Eng-2 gate. Nothing here is a necessity order (B.8.3).

---

## 1. Thesis

C-P1-011's Markov premise (premise 2: `Z → X → Y`) is a **conditional-independence statement about a closed-loop system that evolves in time**. A list of "other sensors" cannot check it. What can check it is a **d-separation certificate on a time-unrolled channel graph** of the target stack. That certificate has to cover the *realized* message stream of `X` (timing and metadata included, not only the schema fields), the upper layer's own past outputs, shared infrastructure, and how the evaluation label `Z` is produced.

The audit then yields an **attribution report**, not a pass/fail flag:

`I(Z; X, W) = I(Z; W) + I(Z; X | W)`

The ceiling the program actually cares about ("what the export contributes") is `I(Z; X | W)`. It is **not** `I(Z; X)`. The two can differ in either direction: `W` can make `X` redundant, or it can make `X` *more* informative through synergy. So the export cannot be judged in isolation once `W ≠ ∅`. That is the practical content of H5 (near-vacuity): the theorem constrains the program only to the extent that the audit bounds `I(Z; W)`.

How this differs from a sensor inventory:
- (i) Channels are classified by **graph path type**, not by device. There are seven classes (§3).
- (ii) The **export `X` is defined as a realized stream**, so timing, presence/absence, ordering and fault or mode flags are inside `X` and cannot leak silently (§2, T-class).
- (iii) **Closed loop is handled explicitly**: the upper layer's past outputs go into `W`, so the chain is never asserted across a feedback edge (§2, E-class).
- (iv) **H4 gets an amendment**: "derived fields add no information" holds only if those fields are derived from *published* fields (§4, TP-6).
- (v) An **optional leak-alarm lemma** (§6) turns "the upper layer beats the export" into a statistically controlled audit trigger. It reuses C-Eng1-A-01 and C-Eng2-A-01 as sub-items. It is not a gate.

---

## 2. The audit object: time-unrolled channel graph

For a declared window `[t₀, t₁]` at a declared resolution, draw a directed graph with these nodes:

| Node | Meaning |
|---|---|
| `S` | Scene or world state (geometry, object poses, surface properties): the common cause of contact |
| `Z` | Declared contact variable (premise 1) |
| `B` | Body-loop internal state and raw signals (joint encoders, motor currents, internal estimators), **before** export |
| `X` | Body-loop export as **realized** at the upper-layer boundary: field values **plus** arrival times, sequence numbers, drops, ordering, mode, fault and saturation flags, and schema version |
| `C_up` | Upper-layer outputs: commands, targets, gains, mode requests, and efference copies of these |
| `W_s` | Independent upper-side sensors (vision, audio, skin, head inertial unit, separate force sensing) |
| `W_m` | Upper-layer memory and priors: maps, episodic memory, cross-episode state, learned parameters |
| `W_i` | Infrastructure: shared memory, logs, debug or introspection endpoints, shared clocks and RNG seeds, scheduler and load signals, power and thermal telemetry |
| `L` | The labelling process that produces the evaluated `Z` |
| `Y` | Everything the upper layer holds over the window |

**Certificate requirement (proposed TP-2):** the auditor lists every directed path from `{Z, S, B, L}` into `Y`. Each path must satisfy one of the following:
- **(a)** it passes through `X`;
- **(b)** it passes through a node that is placed in `W` (so it is accounted for in the joint channel);
- **(c)** it is shown blocked: no edge exists, with a reason given.

Paths that pass through `C_up` (feedback: `Y_{<t} → C_up → B → Z`) are always resolved by placing `C_up` in `W`. Once that is done, `Y_t = f(X_{≤t}, W_{≤t}, U_t)` with `U` independent of `Z` given `(X, W)`, and the joint-channel bound `I(Z; Y) ≤ I(Z; X, W)` applies with no further closed-loop machinery. (Directed-information refinements are not needed for the narrow claim. They are listed as an optional extension in §7.)

The certificate is a **document review** (architecture diagrams, interface definitions, deployment config, harness code paths). That matches the claim record ("a document review, not a spike").

---

## 3. Side-channel inventory (seven path classes)

Each row gives: the path, the premise it threatens, the audit question (which can fail within days by inspection), and the default disposition if the channel is present.

### E — Efference / self-generated (premise 3)
| # | Channel | Threat | Audit question | Default disposition |
|---|---|---|---|---|
| E1 | Commanded trajectory or target (planned foot or hand placement) | Contact timing and location are largely predictable from the command and the scene | Does the upper layer keep its own command history over the window? | `W` (mandatory) |
| E2 | Gain, impedance and mode requests | Contact wrench depends on commanded stiffness | Are gain or mode requests issued from above? | `W` |
| E3 | Expected-contact schedule (gait-phase clock, planner contact sequence) | Directly encodes the prior on `Z` | Does any upper module hold a contact schedule? | `W`; report `I(Z; E3)` separately |
| E4 | Outcome of earlier probing actions (actions chosen to elicit contact) | Active sensing: the action is chosen using `Y_{<t}` | Is the action policy contact-seeking? | `W` (covered by the closed-loop rule) |

### T — Temporal / metadata channels of `X` (premises 2 and 5)
| # | Channel | Threat | Audit question | Default disposition |
|---|---|---|---|---|
| T1 | Message arrival time or jitter | Contact-triggered work in the body loop (mode switch, estimator reset) shifts publication latency, so arrival time encodes `Z` | Is upper-side receipt time recorded or usable? Does body-loop compute vary with contact? | Inside `X` by definition (TP-3). Record it |
| T2 | Event-triggered publication (rate change, extra messages on contact) | **When** samples arrive encodes `Z`, even if the values are subsampled | Is any publication rate adaptive? | Inside `X`. Premise 5 holds only for Z-independent processing (TP-5) |
| T3 | Drops, sequence gaps, queue depth | Load spikes correlated with impact | Are drops or sequence numbers visible above? | Inside `X` |
| T4 | Mode, fault, saturation, torque-limit and safety-stop flags | A safety reflex fires on contact, so the flag is a contact detector | Which status fields cross the boundary? | Inside `X`; list them explicitly |
| T5 | Schema version or field presence | Fields appear only in certain modes | Is the schema static over the window? | Inside `X` |

### S — Independent sensing (claim scope "Does not cover")
| # | Channel | Audit question | Disposition |
|---|---|---|---|
| S1 | Vision, including indirect cues: motion blur or frame shake from impact, seeing one's own limb touch | Does the upper layer receive camera frames over the window? | `W_s` |
| S2 | Audio (impact sound, motor whine under load) | Is there a microphone path? | `W_s` |
| S3 | Head- or torso-mounted inertial unit read **directly** by the upper layer, not through the export | Which inertial streams bypass the body loop? | `W_s` |
| S4 | Tactile skin or separate force sensors on an upper-side bus | Bus topology | `W_s` |
| S5 | Proprioceptive streams duplicated to the upper layer outside the export (e.g. a raw joint-state topic that is also published) | Does any `B`-level stream reach `Y` other than through the export interface? | **This is not a new sensor. It makes `X` larger than the declared schema.** Redeclare `X`, or put the stream in `W` |

### M — Memory, priors, common cause (premises 2 and 4)
| # | Channel | Threat | Audit question | Disposition |
|---|---|---|---|---|
| M1 | Scene map, object poses | `S → Z` and `S → W_m`: a common cause, so `I(Z; W_m) > 0` | Does the upper layer hold geometry for the window? | `W_m` (legitimate; report it) |
| M2 | Cross-episode memory (same home, same furniture) | Episodes are not exchangeable, and prior contacts predict new ones | Is state persisted across episodes? | `W_m`. Also check premise 4 (TP-4) |
| M3 | Learned parameters `θ` | Contribute zero information about the current window **only if** the training data are independent of the evaluation episodes | Is there overlap between training and evaluation scenes, seeds or trajectories? | If there is overlap, `θ ∈ W` with `I(Z; θ) > 0`. Flag it as a TP-4 violation |
| M4 | Privileged-information training (teacher with ground-truth contact, distilled into a student) | Harmless at deployment if the student's inputs are `(X, W)`. A leak if any teacher pathway or ground-truth input is still wired at evaluation | Which inputs are live at evaluation? | Block, or `W` |

### I — Infrastructure / harness (premise 2)
| # | Channel | Threat | Audit question | Disposition |
|---|---|---|---|---|
| I1 | Simulator ground-truth or debug endpoints reachable by the upper layer | A direct `Z → Y` edge | Can the upper process read physics-engine state, contact lists or logs? | **Block** (any such path invalidates evaluation) |
| I2 | Shared memory, shared logging bus, introspection topics | `B → Y` bypassing the export | Process isolation and topic ACLs | Block, or redeclare `X` |
| I3 | Shared RNG seeds or common clocks | Noise `U` is not independent of `Z` | Is the seeding of body-loop and upper-layer randomness independent? | Separate the seeds, or include them in `W` |
| I4 | Scheduler, CPU load, power draw, battery voltage sag, thermal telemetry | Impact current shows up in power telemetry | Which health streams reach the upper layer? | `W_i` |

### L — Label-definition coupling (premise 1)
| # | Channel | Threat | Audit question | Disposition |
|---|---|---|---|---|
| L1 | `Z` is defined from a signal that is also in `X` or `W` (e.g. the onset label comes from the same force threshold the body loop uses to set a flag) | `Z` becomes a function of `X`, so the bound is tight by construction and says nothing about the physical contact | What is the label provenance (`L` node)? | Declare the label source. If `Z = h(X)`, report it as definitional and do not read the bound as physical |
| L2 | Label from simulator ground truth vs label from a hardware proxy | Different `Z` variables. A ceiling for one is not a ceiling for the other | Which `Z` was used where? | Treat them as separate claims instances |
| L3 | Window or alignment chosen after looking at `Y` | Violates the fixed probability model | Were the window and resolution fixed before evaluation? | Pre-register them |

### D — Distribution / model mismatch (premise 4)
| # | Channel | Threat | Audit question | Disposition |
|---|---|---|---|---|
| D1 | Evaluation distribution ≠ deployment distribution | The inequality holds per distribution. A ceiling measured in one does not transfer | Is the distribution over `(S, Z, X, W)` stated for each use? | Each application cites its distribution |
| D2 | Adaptive evaluation (thresholds or windows tuned on evaluation data) | Same problem as C-Eng2-A-01's selection restriction | Is evaluation data held out? | Hold it out |

---

## 4. Tighten-premises checklist (proposed amendments to C-P1-011)

These clarify the hypotheses of the standard DPI statement. None of them narrows the claim to survive a counterexample. **Request to the claim adjudicator:** rule these as **one bundled premise-clarification event** under B.9.6, or as zero events. If they were counted one by one, six would cross the default threshold of 3 and force a retirement review of a theorem that has had no counterexample. That would be the wrong signal. The adjudicator decides; this proposal only discloses the risk.

| ID | Amends | Proposed text (short) |
|---|---|---|
| **TP-1** | Premise 1 | `Z` is declared with quantity, window, resolution, **and label provenance `L`**. If `Z` is a function of `X` or `W`, the application is marked *definitional*. |
| **TP-2** | Premise 2 | Applying the claim to a target stack requires a **path certificate** on the time-unrolled channel graph (§2). Every path from `{Z, S, B, L}` to `Y` crosses `X`, or is placed in `W`, or is shown blocked. |
| **TP-3** | Premise 2 (definition of `X`) | `X` is the **realized** boundary stream: values, timestamps, ordering, drops, mode/fault/saturation flags, and schema version. Any stream from `B` that reaches `Y` outside the declared interface either enlarges `X` (redeclare it) or is placed in `W`. |
| **TP-4** | Premises 3 and 4 | `W` includes, at minimum, (i) upper-layer outputs and efference over the window **and earlier** (this closes the feedback path), (ii) persisted memory, and (iii) learned parameters whenever training and evaluation episodes are not independent. One probability model per application, with the distribution stated. |
| **TP-5** | Premise 5 | "Processing lowers information" covers processing whose **control is independent of `Z` given its input**. Event-triggered or adaptive subsampling is part of how `X` is defined: the pattern of samples is information inside `X`, not a removal. |
| **TP-6** | Hygiene H4 | `I(Z; I1 ∪ I2) = I(Z; I1)` holds **only if** I2 is a function of the *published* I1 stream. If I2 is computed from body-loop-internal signals (`B`) at a higher rate or with fields that are not published, then I2 can add information. Record I2's provenance. |
| **TP-7** | Programmatic use (H5) | Any statement of the form "the export limits upper-layer contact knowledge" must report the attribution `I(Z; W)` vs `I(Z; X | W)`, or bounds on them, or a qualitative ranking. It must not cite `I(Z; X)` alone when `W ≠ ∅`. |

TP-7 changes no grade. It is a usage rule for citing the claim. It is offered so that later packets cannot use C-P1-011 to argue for export-schema priorities while `W` is unaudited.

---

## 5. Audit checklist (operational; document review)

Applied per target stack and per declared `Z`. Each item is a yes/no answer with an artifact pointer. Any "unknown" leaves the application **unaudited**, and the claim may not be cited for that stack.

1. [ ] `Z` declared: quantity, window `[t₀, t₁]`, resolution, label source `L`. (TP-1; L1–L3)
2. [ ] `X` declared as a realized stream; list every field and metadata channel crossing the boundary. (TP-3; T1–T5, S5)
3. [ ] Upper-layer process inputs enumerated from deployment configuration (subscriptions, device handles, shared memory), not from design intent. (I2, S1–S4)
4. [ ] Simulator or debug ground-truth access from the upper process: **absent** (verified by process isolation or config). (I1, M4)
5. [ ] Upper-layer outputs and efference: listed and placed in `W`. (E1–E4)
6. [ ] Persisted memory and maps: listed and placed in `W`. (M1, M2)
7. [ ] Train/eval independence for learned parameters: confirmed, or `θ` flagged. (M3)
8. [ ] RNG and clock independence between body loop and upper layer: confirmed or recorded. (I3)
9. [ ] Health and power telemetry crossing to the upper layer: listed. (I4)
10. [ ] Body-loop publication: fixed-rate or event-triggered? Is latency contact-dependent? Recorded. (T1, T2; TP-5)
11. [ ] Derived export fields: provenance from published vs internal signals. (TP-6)
12. [ ] Distribution for this application stated. Windows and thresholds pre-registered. (D1, D2, L3)
13. [ ] Path certificate (§2) signed off by an auditor who is not the stack designer. Every path is labelled (a), (b) or (c).
14. [ ] Attribution note: qualitative or bounded `I(Z; W)` vs `I(Z; X | W)`. (TP-7)

Outputs: `audit/<stack-id>/<Z-id>/certificate.md` (template proposed; not created here). Discovered premise failures go to `claims/C-P1-011/violations.md` as **B.9.4(b) premise failures in the target setting**. They are not counterexamples to the theorem.

---

## 6. Optional sub-item: leak-alarm lemma (links C-Eng1-A-01 and C-Eng2-A-01; not a gate)

**Statement (author sketch; needs its own claim record and cross-family adjudication before any use):**

If `Z → X → Y` holds on the fixed model, then every (possibly randomized) detector on `Y` is a randomized detector on `X`, because the detector composes with the kernel `X → Y`. Hence, at any size `r`, its power is at most `β*_X(r)`.

So suppose two things hold on held-out data:
1. the C-Eng2-A-01 statistical ceiling, computed with `W = ∅` (export only), gives `TPR_U(t*) = c` at level `α`;
2. a fixed detector on `Y` achieves `TPR_L > c` with `FPR_U ≤ r`, using C-Eng1-A-01-style Clopper–Pearson bounds at level `α`.

Then, with probability ≥ `1 − 2α`, the Markov chain `Z → X → Y` fails on that model: a side channel exists.

**Use:** this is an audit trigger only. It **localizes nothing**: the path still has to be found through §5. It inherits C-Eng2-A-01's genie-model premises and selection restriction, and C-Eng1-A-01's held-out premise. Failing to fire certifies nothing; there is no certificate of absence. It is not an Eng-2 precondition and it adds no Eng-2 gate. It could be run inside an already-approved Eng-2 harness at no extra cost *if and when* D-Prin-3-001 clears. That is a sufficiency-side convenience and nothing more.

---

## 7. Explicitly out of scope / deferred

- Directed-information or causal-conditioning refinement (bounds over the full closed-loop horizon). The TP-4 rule of putting outputs in `W` makes this unnecessary for the narrow claim. It is optional future work and is not part of the lock path.
- Which fields the export *should* carry: C-P1-012 (Grade 2 Candidate). This proposal makes no field recommendations.
- Estimation quality and latency: out of scope for DPI (claim scope).
- Ordering: no claim that the audit must precede any stage. This is planning priority per D-Prin-4-001 only.

## 8. Gates self-check (before ranking)

| Gate | Status |
|---|---|
| No grade or state change by author | Yes. Candidate stays. Proposals routed to the claim adjudicator (Astra, cross-family) |
| No Locked Grade-1 | Yes |
| No Grade-3 used as law | Yes. No biological citations; the citation-ablation test is trivially passed (H6) |
| No new Eng-2 preconditions | Yes. §6 is explicitly not a gate |
| Planning order not used as necessity | Yes |
| No named products or companies | Yes |
| B.9.6 counter disclosed | Yes. Bundling requested; adjudicator rules |

## 9. Falsifiability of this proposal

The proposal itself is wrong if an auditor applying §5 to a concrete stack finds a contact-informative path to `Y` that fits none of the seven classes (E/T/S/M/I/L/D). That can be tested within days by having a second, non-author reviewer try to construct such a path. A found path is evidence that the taxonomy is incomplete. It does not count against C-P1-011.

## 10. Rubric-oriented notes (for adjudicators)

- **Evidence demand:** minimal. A document review; no compute.
- **Reversibility:** high. The checklist is an artifact template. TP-1..7 are wording amendments.
- **Integrability:** body loop owns `X` (including metadata). The scene-publication layer owns `W_s` and `W_m`. The decision core owns `C_up` and its efference. The harness owner owns the I-class and L-class channels.
- **Dominant failure mode:** the audit is done from design documents instead of deployment config, so the inventory misses real wiring. Mitigation: checklist item 3 requires config-derived enumeration, and item 13 requires an independent sign-off.
