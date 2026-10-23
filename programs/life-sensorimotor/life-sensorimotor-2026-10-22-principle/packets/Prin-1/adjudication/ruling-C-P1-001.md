# Ruling — C-P1-001 (Scalar response-latency bound)

1. **Claim ID:** C-P1-001
2. **Adjudicator family:** Opus (Claude Opus; claim adjudicator for Astra-authored claims per `roster.md`)
3. **Author family:** Astra
4. **Ruling:** **recommended-for-lock** (conditional; see items 6 and 9). State remains **Candidate**.
5. **Grade:** Grade 1 (narrow formal, scalar fixture) **confirmed**. State: **Candidate**. NOT Locked. No Locked Grade-1 is asserted or implied.

## 6. Gates check (B.3 / B.9)

| Gate | Status |
|---|---|
| Premises complete (B.3.1) | **Pass.** Plant (a=10 s⁻¹), envelope (b=0.01, robust over both worlds), disturbance pair (±D, D=1, constant through L), indistinguishability (u₊=u₋ a.e. on [0,L), randomized controllers coupled), regularity (locally integrable u, continuous x, no resets), and x(0)=0 are all stated. Unused actuator bound is correctly flagged as unused. |
| Conclusion shape (B.3.2) | **Pass.** Impossibility / upper bound on common-input interval L ≤ L*. |
| Implementation independence (B.3.3) | **Pass.** u cancels in Δ = x₊ − x₋ for every admissible common input, so the bound covers classical, learned, predictive and randomized controllers that obey premise 4. |
| Falsifier operational (B.3.4) | **Pass.** A common admissible input history keeping both trajectories in [−b,b] through some L > L*, or an error in the separation proof. Out-of-premise challenges (earlier world-dependent action, altered plant) are correctly routed to premise failure. |
| Citation-ablation (B.8.7) | **Pass.** No evolutionary/anatomical premise is used; the derivation survives deletion of all biological motivation. |
| Independent proof check for Grade-1 lock (B.9.2) | **NOT YET SATISFIED by an allowed route.** Adjudicator re-derivation (below) is cross-family model review. Per B.9.7 that is not grade evidence and is not one of the three acceptable routes (formal checker; published result matched item by item; qualified human review). |
| Human-lead signature (B.9.2) | **Absent.** |

**Adjudicator re-derivation (independent of author text, not a B.9.2 check):** with Δ = x₊ − x₋, Δ̇ = aΔ + (u₊ − u₋) + 2D = aΔ + 2D a.e. on [0,L), Δ(0)=0 ⇒ Δ(t) = (2D/a)(e^{at} − 1), strictly increasing and continuous. |x₊|,|x₋| ≤ b ⇒ Δ ≤ 2b ⇒ e^{aL} ≤ 1 + ab/D ⇒ L ≤ L* = ln(1 + ab/D)/a = ln(1.1)/10 = 0.009531017980… s. At L = 20 ms, Δ/2 = 0.1(e^{0.2} − 1) = 0.0221402758… > b. Because Δ is continuous and increasing, the violation for L > L* occurs strictly inside (L*, L], so the "envelope holds through the interval" premise suffices; the bound is non-strict (L = L* requires x₊ = b, x₋ = −b exactly). A numerical sanity check (Euler, h = 1 µs, three different common inputs including one saturating |u| ≤ 3 and one unbounded ramp) reproduced Δ(L) independent of u to ~1e-5 relative error. Agreement with the author moves no grade (B.9.7).

## 7. Counterexample spike before further action?

**No mandatory spike.** The bound is analytic; under the stated premises a counterexample search above L* is provably empty, and B.9.2 requires a logged failed search only for Grade 2. The author's registered-as-future PLAN may run optionally as a harness check, but its PASS would be sufficiency/harness evidence only and must not substitute for the B.9.2 proof check. The sealed P1 sweep results (attempt 1 FAIL, attempt 2 PASS, crossing near 8 ms) are neither counterexamples nor tightness evidence; this ruling does not rely on them.

## 8. Justification

- The separation argument is elementary, complete on its stated premises, and I re-derived L* and the 20 ms figure exactly.
- Every B.3 gate passes; citation-ablation passes; scope is honestly restricted to the scalar fixture.
- B.4 explicitly allows a narrow Grade-1 formal bound to lock early subject to B.9; the remaining blockers are procedural (allowed-route proof check + signature), not substantive.
- Hence recommended-for-lock is appropriate, but **conditional**: lock may occur only after a B.9.2-acceptable check is attached AND the human lead signs.
- Lock scope must be the fixture statement only. A lock would veto only routes whose premises match item by item (scalar a, b, D, common-input interval). It must not be cited as a home-humanoid hardware deadline, a control-frequency requirement, or evidence for C-P1-002's role or any S0→S1/S2 edge.
- D-P1-001 remains Provisional and an S0a acceptance-gate recommendation, not a necessity order. This bound does not convert it into one. A spike PASS does not establish necessity.
- Scope-narrowing counter: 0 (stub expansion only restates existing Proposal-B assumptions). I accept that count.

## 9. Outstanding items for human lead

1. Supply the B.9.2 independent check by an allowed route. A qualified human can review the five-line proof above in minutes, or a formal checker proof (e.g. a short ODE-comparison lemma) can be deposited. Then decide whether to sign the Grade-1 lock. Until both are done, the state is **Candidate**.
2. If signing, record the lock scope verbatim as "scalar fixture, premises 1–5", and record that the veto does not extend to target-plant hardware without a new premise match.
3. Open in D-P1-001: the measured total response delay ≠ the common-input interval L. Require the sweep to log L separately (as the claim states), so that no harness result is misread against L*.
4. Minor ledger hygiene: `inherited-ledger-P1.md` header says run date 2026-10-23 and cites `proposals/B.md`, while the claim cites `P1-proposal-B.md`. Confirm these refer to the same sealed artifact.
