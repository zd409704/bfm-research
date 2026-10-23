# Decision — Packet Prin-2 (Ladder-edge necessity)

**Packet:** Prin-2  
**Box-local close:** 2026-10-22 ~16:17 EDT  
**Adjudication:** Sonnet order-swap P/Q (pass1 P=A/Q=B totals 39/40; pass2 P=B/Q=A totals 40/39). Consistent after swap.

## Packet outcome

| Role | Proposal | Disposition |
|------|----------|-------------|
| **Recommend** | **B** (even edges E02–E14) | All seven edges **Grade 3 quarantined / Candidate**. No Eng-1 necessity gate. Upgrade attempts (E04/E06/E10) remain non-authoritative until B.9 complete. |
| **Alternate** | **A** (odd edges E01–E19) | Richer design inputs (E03/E07 timing bound; E17 DPI/KL specification form). Headline recommended-for-lock on E17 and G1 labels on E13/E15 **not sustained** as packet locks. |
| **Reject** | Any text promoting a Grade-3 edge to gate/veto now | — |

## Claim rulings (authoritative for state)

See `adjudication/summary-astra-odd-edges.md` and `summary-opus-even-edges.md`.

**Quarantine-Grade3:** E01, E02, E04, E05, E06, E08, E09, E10, E11, E12, E14, E19 (and acquisition-order readings of all edges).

**Candidate-stay / tighten (no Eng-1 gate):** E03, E07, E13, E15, E17 — remain Candidate; E17 not recommended-for-lock by claim adjudicator (tighten-premises); independent B.9.2 checks outstanding.

**Eng-1 gates from ladder edges: NONE.**

## Inherited

D-P1-001 remains Provisional S0a acceptance-gate (not necessity order). No Grade-1 Locked.

## Mandatory amendments before any edge lock

1. Independent B.9.2 proof checks + human signature for any Grade-1 nomination (E03/E07/E17 cores; E10 TV kernel if split out).
2. Register sealed counterexample PLANs before treating Grade-2 role upgrades as Incomplete-gates.
3. Fix E17 zero-FPR assertion / rare-event KL caveat; fix E13/E15 falsifier scope.
4. Eng-1 must list bypassed Grade-3 edges (B.8.5): at least E05/E06, E08/E09, E14; and E10/E11 if S1 without prior S2a.

## Next packet

**Eng-1** — Competing proposals for next mainline engineering packet after P1 (likely S2a contact observability floor per P1 Alternate), gated only by surviving Principle claims (none as locks); interface contracts + spike if recommended.
