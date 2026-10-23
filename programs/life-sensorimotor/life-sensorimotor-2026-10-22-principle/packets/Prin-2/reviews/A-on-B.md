# Prin-2 — Blind Review A (Claude Opus) on Proposal B

Read boundary: `proposals/B.md`, `drafts/B/edge-index.md`, `claims/C-Prin2-E02,E04,E06,E08,E10,E12,E14/claim.md`, `brief.md`, `source/method-Appendix-B.md`. To check for overlap I also looked at the header of inherited `C-P1-011/claim.md` and grepped `C-P1-002` and `Prin-1-decision.md` for grade and state lines. I did not open Proposal A, drafts/A or any odd-numbered C-Prin2 claim. I changed no claim files.

## 1. Summary

- B registers seven directed edges, each with its own claim record (E02, E04, E06, E08, E10, E12, E14). All seven are submitted as **Grade 3 / Candidate / quarantined**, with no recommended-for-lock nomination and **no Eng-1 gate**.
- B's main conceptual contribution is to separate **runtime availability** from **acquisition precedence**, and both from "a shared property that one controller can supply". This is the right lens for B.8 and is applied consistently.
- The E10 information kernel (TV(P0,P1) ≥ 1−2ε through the data-processing inequality) is algebraically correct. It passes citation ablation and is honestly kept separate from the edge's grade.
- The E04/E06 timely-response premise is **internally inconsistent as written** (§5, O1). It needs reformulating before any Grade-2 review.
- The claim records are heavily templated. The falsifier, ablation and governance paragraphs are near-identical across edges, which weakens per-edge falsifiability.
- B registers no PLAN.md and no counterexample search, so all falsifiers are prospective only.
- Overall verdict: B is sound on gating and on Principle integrity. Its upgrade attempts are useful but need repair (E04/E06) and de-duplication (E10 vs C-P1-011).

## 2. Constraint fit / Principle integrity / Falsifiability notes

**Constraint fit.**
- No named robot or company appears.
- No Grade-3 claim is treated as law.
- No Grade-1 lock is claimed.
- D-P1-001 is preserved as a Provisional acceptance gate rather than a necessity order (brief constraint 8).
- The read boundary is declared. Author ≠ adjudicator bindings are recorded (Astra author, Opus adjudicator).
- The B.9.6 narrowing ledger is started for E04, E06 and E10. This is good hygiene.

**Principle integrity.**
- Grades are stated, and necessity is kept separate from sufficiency ("PASS validates harness, not necessity").
- B never cites the planning order as evidence (B.8.3).
- No transitive or reverse-edge upgrade is taken for free.
- Ablation is applied with the correct reading: survival is necessary but not sufficient for an upgrade.
- B also refuses to define the source stage after the fact as "whatever the successful destination used". This guards against the degenerate-relabelling failure that B.9.6 targets, which is a strong point.
- Weakness: the unsplit stage contracts (S1/Q1, S0b) are flagged as missing but never even sketched. Every edge therefore fails on the same "no canonical Q1" premise. That is honest, but it means the packet produces little per-edge discrimination.

**Falsifiability.**
- Every record names a falsifier shape: a formal counterexample for the E10 kernel, and bypass witnesses for each edge.
- However, none is registered as a §12.2 PLAN.
- The common closing paragraph ("A successful same-premise destination competence … Simulation success proves tested sufficiency only") is repeated verbatim in all seven records, so per-edge falsifiers are thinner than they look.
- The E10 kernel has a cheap, failable-within-days check: an exact finite fixture that enumerates P0/P1 and the action kernel. B mentions this but does not plan it.

## 3. Per-edge positions

| Edge | B's action | My position |
|---|---|---|
| E02 S0a→S0b | Quarantine; no acquisition order | **Agree.** Viability as an acceptance conjunction is not an input dependency, and S0b can itself realize S0a. The argument is clean. |
| E04 S0a→S1 | Quarantine; keep conditional Grade-2 attempt | **Agree with quarantine; dispute the attempt as currently formulated** (O1). Premises 3 and 4 are jointly unsatisfiable. Once repaired, the attempt is really a **latency lower bound** (Grade-1 shape) more than a Grade-2 role. Even then it maps to the role "timely response" and not to the stage "S0a" — B correctly notes this mapping gap. |
| E06 S0a→S2a | Quarantine; Grade-2 for safe online probing only | **Agree with quarantine.** The offline-estimation and passive-observation bypasses are decisive against the broad edge. The narrow variant inherits O1 from E04. I also question whether it belongs on this edge at all: its necessity comes from the probe's envelope, i.e. from an S2a-*execution* task, not from S2a observability. I would retire the narrow variant from E06 and refile it as a property of "active probing tasks", rather than spend a narrowing event on it. |
| E08 S1→S2a | Quarantine; reject universal active-action prerequisite | **Agree.** Supplier exclusivity fails: a fixed probe or direct sensor suffices. The separate active-information lower bound is correctly left unregistered on this edge. |
| E10 S2a→S1 | Quarantine; prioritize Grade-1 kernel | **Agree with quarantine and with prioritizing it.** I checked the math: μ1(A0) ≤ ε ⇒ TV(μ0,μ1) ≥ 1−2ε; the data-processing inequality for TV under a common Markov kernel holds; and the equal-prior optimal-error corollary ≤ ε follows from err* = (1−TV)/2. However, see O2: the kernel is essentially a two-hypothesis (Le Cam) instance of the same DPI that inherited **C-P1-011** already carries as a Grade-1 Candidate. E10 should cite C-P1-011 and either specialize it or merge into it, not set up a parallel Grade-1 track. The edge bridge (S2a as a contract ≠ "information present in H") remains open, as B says. |
| E12 S0b→S1 | Quarantine; don't mandate reflex/impedance package | **Agree.** No concrete role is identified, and "all helpful feedback = S0b" would be a relabelling. |
| E14 S0b→S2a | Quarantine; don't require impedance/reflexes for observation | **Agree.** The distinguishing channel need not be S0b (direct sensor, calibrated actuator model). |

No upgrade attempt in B succeeds, and none is presented as succeeding. I dispute only the *formulation* of the E04/E06 attempt and the *novelty/placement* of E10, not B's dispositions.

## 4. Eng-1 gating implications

- **Should any edge gate Eng-1? No.** All seven are Grade-3 Candidates, and B.4 and B.9.5 forbid Candidate vetoes. I agree with B's "none gates now".
- B correctly requires that an S2a-first Eng-1 proposal list the edges it bypasses (E06, E08, E14, plus E10 if S1 is developed without S2a) together with their grades (B.8.5). Endorse this.
- B also lists interface requirements as ordinary proposal completeness rather than vetoes: Z, window, ε, deadline t_d, full joint-channel inventory, online vs offline, and envelope ownership. Endorse this too. It is the right non-gating route by which the E10/C-P1-011 kernel can shape Eng-1 lawfully.
- Recommendation to the adjudicator: if the E10/C-P1-011 kernel is independently verified and signed later, it would constrain **runtime information availability** at the decision interface. It would never constrain packet chronology, so it still would not block S2a-first engineering.

## 5. Concrete objections

**O1 (E04, E06): the timely-response premise is self-contradictory.** E04 premise 3 asks for two worlds "indistinguishable to all force-changing channels through a declared deadline τ\*, with no common safe corrective-force prefix through that deadline". Premise 4 requires the task to be feasible.
- If every channel that can change force is identical in both worlds up to τ\*, then any realization emits the same force prefix in both worlds up to τ\*.
- If no common safe prefix exists, every realization fails in at least one world, so the task is infeasible and premise 4 is violated.
- The useful kernel needs the worlds to be indistinguishable only up to some t0 < τ\*, with a distinguishing channel available in [t0, τ\*]. The conclusion is then a **response-latency bound**: world-dependent force must be produced within τ\*−t0 of the information arriving.
- **Fix:** restate with t0 and the information-arrival time, and reclassify the target as a Grade-1 latency bound (premise-conditional) plus a Grade-2 timely-response *role*. Neither maps to the S0a stage without a separate contract.

**O2 (E10): duplicate Grade-1 track.**
- The TV kernel is a binary-hypothesis instance of the DPI ceiling in inherited C-P1-011.
- Running it as a second, independently verified Grade-1 candidate duplicates verification work and risks two diverging statements of the same invariant.
- **Fix:** cite C-P1-011, and state E10's kernel as a corollary: accuracy ε at deadline t_d implies a lower bound on TV for the joint history. Request a single verification for both.

**O3: templated records reduce per-edge falsifiability.**
- These sections are nearly identical across all seven claim.md files: "Scope and order semantics", the second paragraph of "Operational test", "Citation ablation" and "Verification and governance".
- As a result, each record's specific falsifier is often one or two sentences.
- **Fix:** keep the boilerplate in one shared governance note, and expand each edge's falsifier to name concrete variables, a concrete pass/fail threshold, and what artifact counts as a bypass witness.

**O4: no registered counterexample PLAN.**
- B.9.8 and the brief prefer completed Principle work.
- E10's exact finite-fixture check and E02's "simultaneous realization" search are both cheap. Neither is sealed as a PLAN.
- Falsifiability is therefore stated but not exercised.

**O5: the missing stage contracts are blocking, but B offers no draft.**
- Every edge stops at "canonical Q1 / S0b contract undefined". B gives no candidate contract that an adjudicator could accept or reject.
- This ensures uniform Grade 3 but defers the actual Prin-2 question.
- **Fix:** propose at least a minimal S2a contract (Z, window, ε, t_d, channel inventory) as a planning-level definition that the human lead can adopt under B.8.3.

**O6 (minor): E06's narrow variant may be misplaced.**
- Its necessity comes from the safety of active probing, not from S2a observability.
- Filing it under S0a→S2a uses a narrowing event on an edge it does not really concern.

## 6. Scores (1–5)

| Dimension | Score | Note |
|---|---|---|
| Constraint fit | 5 | All hard constraints and non-goals respected; D-P1-001 preserved; no locks, no named platforms. |
| Principle integrity / Necessity | 4 | Exemplary grade discipline and availability/acquisition split. Docked for O1 (an inconsistent premise in a nominated upgrade route) and O2 (duplicate Grade-1 track). |
| Falsifiability | 3 | Falsifier shapes are named but templated (O3), and no PLAN is registered (O4). E10 has a cheap fixture check that is not planned. |
| Evidence demand | 5 | Analytic only; no compute or hardware asked for. Proposed tests are low-cost. |
| Failure modes | 4 | Bypass paths named per edge (offline estimation, direct sensors, passive mechanics, joint controllers). The relabelling failure is explicitly guarded. |
| Integrability | 3 | Body loop / contact export / decision interface are referenced generically, but S0b and Q1 contracts are left undefined (O5), so ownership boundaries are unresolved. |
| Latency / criticality | 3 | Recognizes that the E04/E06 content is a runtime timing matter, but does not state it as a latency bound, and O1 blocks the tiering argument as written. |
| Complexity cost | 4 | Seven separate records are required by B.8.1. The repeated boilerplate is overhead but cheap; no extra machinery. |
| Reversibility | 5 | Nothing locked and nothing gated, so it is trivially abandonable. |
| Stackability | 4 | Leaves Eng-1 open with bypass-listing and interface-completeness duties. That enables S2a-first work without premature S1/S0b, though it gives Eng-1 little positive structure. |

Gate note (B.9.5): no Proposal-B edge passes a lock gate, and none is claimed to. Ranking proceeds with zero Principle gates from B.
