# C-Prin2-E01 — Edge S0a → S0b

| Field | Value |
|---|---|
| **Edge** | S0a → S0b ("bounded-response viability must precede / be available to remaining reflex/impedance content") |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family; not this author) |
| **Grade** | **3** (both readings). Upgrade attempted; failed. |
| **State** | Candidate, **quarantined** (inspiration / planning only; no claim, gate or veto use) |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | quarantine-Grade3 |

Stage meanings: Author-A W-defs (`drafts/A/stage-defs.md`, copied in `proposals/A.md` §1).

## Premises

1. Generic home humanoid / target plant; S0a and S0b as W-defs.
2. S0b competence is measured joint-locally: e.g., passive rendering of a virtual impedance `(K, B)` against unknown passive environments (C-P1-010 Part A setting), or a reflex response within a declared latency.
3. No premise states that S0b competence is exercised only while the whole-body envelope is threatened.

## Conclusion shape (proposed, not established)

Reading A: "Any system with S0b competence must have S0a bounded-response viability available." Reading P: "S0a must be acquired before S0b."

## Upgrade argument attempted and result

- **Grade-1 information:** S0b competence (passive impedance, reflex latency) needs joint-local position/velocity/effort and a fast loop. It needs no signal that only the S0a envelope supplies. **Fails.**
- **Grade-1 stability:** C-P1-010 Part A's passivity condition `b > K·T/2 + |B|` contains no whole-body envelope term. A joint can render passive impedance on a fixed or supported base with no S0a envelope. **Fails.**
- **Grade-1 resource:** S0a (latency ≤ L*, C-P1-001) and S0b (period T with `K < 2(b−|B|)/T`, C-P1-010) both consume a *fast tier*. That is a **shared resource**, not an order. If anything, the relation runs the other way: S0b content (fast impedance/reflex) is one possible *realization* of S0a. Passive mechanics are another (C-P1-002 premise 4). **Fails as an edge.**
- **Grade-2 obligatory role:** No functional role obligatory for S0b is realized only by S0a. **Fails.**

## Citation-ablation (B.8.7)

The only support for S0a-before-S0b in the record is the evolutionary S0-first narrative (C-P1-003, Grade 3) and the planning choice D-P1-001. Deleting the evolutionary citation leaves no argument. D-P1-001 is a Provisional acceptance gate, and B.8.3 forbids citing it. **The argument collapses → Grade 3.**

## Scope

Planning ladder only. This record asserts no order, independence, or reverse edge. A reverse "S0b realizes S0a" statement would be a **realization relation**, not a necessity edge, and is not claimed.

## Falsifier / challenge mode

An upgrade would need to exhibit a signal, bound or property that S0b requires and that only S0a supplies, under stated premises. A system with verified S0b competence (passive impedance at declared `K`, `T`) and no S0a envelope competence would directly show that Reading A is false. Such a system is easy in principle: a fixed-base joint. See violations.md.

## Use restriction

May not be used as a gate, veto or theorem in any packet. D-P1-001 is not affected. It remains a Provisional acceptance-gate recommendation, **not** a necessity order.

## Counterexample-search spike registered?

**No.** Reading A is already expected to be false under premise 2, so a PLAN would only confirm the quarantine. One-line PLAN for the record, if wanted: a 1-DoF fixed-base ZOH impedance with no envelope controller, checked for passivity at `K < 2(b−|B|)/T`. A pass would count as the counterexample to Reading A.
