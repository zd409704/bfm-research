# C-Prin2-E15 — Edge S0b → S2

| Field | Value |
|---|---|
| **Edge** | S0b → S2 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **Reading A-narrow: Grade 1 conditional, disjunctive, class-restricted** (from C-P1-010 Part B). **A-general: Grade 3. Reading P: Grade 3.** |
| **State** | Candidate |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | Candidate-stay (A-narrow). quarantine-Grade3 (A-general, P). |

Stage meanings: Author-A W-defs (`proposals/A.md` §1).

## Premises

1. C-P1-010 premises 1–8, for the contact-critical joint `j` used in S2 interaction.
2. **S2 specification demands a passivity guarantee** against unknown passive environments, including humans and household objects, at task stiffness `K_req,j`. This is more natural for S2 than for S1, because S2's environment is unknown by definition. It is still a specification choice, not a theorem.
3. The S2 tier, or the policy feeding it, renders the stiffness at period `T_S2 ≥ T_R2`.

## Conclusion shape — Reading A-narrow

If `K_req,j > 2(b_j − |B|)/T_S2`, then S2 competence requires one of three things:
- (i) faster rendering, which is S0b content;
- (ii) physical compliance;
- (iii) relaxing the passivity requirement.

The edge is S0b-or-physical-compliance, in the linear-ZOH-impedance class only.

## A-general / Reading P

These have the same status as C-Prin2-E13 → **Grade 3** (collapse on citation-ablation; no acquisition-order argument).

## Citation-ablation (B.8.7)

A-narrow **survives**. The others **collapse**.

## Scope / falsifier

Same as C-Prin2-E13, with `T_S2` in place of `T_R2` and the S2 contact joints. Retire for joint `j` if measured `2(b_j − |B|)/T_S2 ≥ K_req,j`.

## Relation to C-Prin2-E07

E07 concerns envelope viability under external contact (S0a). E15 concerns port passivity against unknown environments (S0b). They are independent premises, and either can hold without the other.

## Counterexample-search spike registered?

**No.** Same as C-Prin2-E13.
