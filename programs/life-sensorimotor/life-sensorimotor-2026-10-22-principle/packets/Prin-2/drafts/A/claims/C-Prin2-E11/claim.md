# C-Prin2-E11 — Edge S2a → S1 (reverse edge)

| Field | Value |
|---|---|
| **Edge** | S2a → S1 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **3** for the edge as named (both readings). A Grade-1 *lemma* is recorded that applies to S1's **own support-contact** observability, which is S1-internal content and not S2a. |
| **State** | Candidate, **quarantined** (edge as named) |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | quarantine-Grade3. Planning note to the Orchestrator on stage-definition scoping (below). |

Stage meanings: Author-A W-defs (`proposals/A.md` §1). S2a is defined over **non-support** contacts. S1 includes support-contact handling but no reasoning about non-support contacts.

## Upgrade argument attempted

**Action-dependence lemma** (the same mathematics as C-Prin2-E17, steps 1–3). Suppose a competence requires response actions whose admissible sets are disjoint between two values of a hidden contact variable `Z`, and the policy's input is `Y` with `Z → (X, W) → Y → A`. Then the channels must carry a class-conditional divergence of at least `d(q‖r)`. Here `q` and `r` are the required probabilities of correct and incorrect response.

- **Applied to non-support `Z` (S2a's variable).** By W-def, S1 competence does not require world-dependent responses to non-support contact *identity*. Unexpected bumps act on S1 only as envelope disturbances, which is C-Prin2-E03's domain (S0a), not information about `Z`. **The lemma's premise fails, so there is no edge.** If S1 is redefined to include responding to non-support contacts, it has absorbed S2 content, and the edge becomes definitional containment.
- **Applied to support-contact `Z_s`** (stance/swing, foothold contact). If S1 requires responses that differ by `Z_s`, the lemma gives a Grade-1 conditional floor on the information about `Z_s` that S1's input channels carry. **That floor is S1-internal, not S2a.** It does not upgrade the edge as named.
- **Grade-2 role.** No obligatory S1 role is realized only by the non-support observability floor. **Fails.**

## Citation-ablation (B.8.7)

The edge as named has no surviving argument → **Grade 3.** The support-contact lemma survives ablation, but it attaches to a different claim (see the planning note).

## Planning note (not a claim; for Orchestrator / human lead)

The stage definitions should state explicitly whether support-contact observability belongs to S1 or to S2a. P1 scoped contact detection to non-foot contacts (C-P1-012 scope). If a future definition merges support contact into S2a, this edge would be eligible for a conditional Grade-1 re-attempt via the lemma. That re-scoping would count as a B.9.6 event on this record.

## Falsifier / challenge mode

Reading A for the edge as named would be refuted by a system with S1 competence whose export carries no non-support contact information. Such a system is expected to exist, so the claim is expected to be falsified rather than upgraded.

## Counterexample-search spike registered?

**No.** If wanted, a cheap PLAN is an S1 policy evaluated with the non-support contact channel ablated, no non-support contacts in the S1 task set, and support-contact signals intact.
