# C-Prin2-E05 — Edge S0a → S2a (contact observability floor)

| Field | Value |
|---|---|
| **Edge** | S0a → S2a |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **3** (both readings). Upgrade attempted; failed. |
| **State** | Candidate, **quarantined** |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | quarantine-Grade3. Register the counterexample PLAN. Retire-nominate is premature because no in-premise counterexample has been run. |

Stage meanings: Author-A W-defs (`proposals/A.md` §1). S2a is an *information* property of the body-loop export `X` about a declared non-support contact variable `Z`.

## Premises

1. S2a competence means the exported signal provides `I(Z; X) ≥ h_req` for a declared non-support contact class. Equivalently, it means the detection divergence floor of C-Prin2-E17.
2. `Z` is defined per C-P1-011 premise 1, and the contact class per C-P1-012 premise 3.
3. No premise says that contact observation is evaluated only during envelope-threatening disturbances.

## Upgrade argument attempted and result

- **Grade-1 information.** Does `I(Z; X)` need a signal only S0a supplies? No. The information about `Z` in `X` depends on the sensing channel (realized effort, rate, friction placement; C-P1-012). It does not depend on whether a viability loop is closed. **Fails.**
- **Grade-1 stability.** Observer stability, such as a generalized-momentum observer, depends on observer gain × period (C-P1-012 H2). It does not depend on the body envelope. **Fails.**
- **Grade-1 resource.** S0a and S2a may share a fast tier and a high-rate effort channel. That is a shared resource, not an order. **Fails.**
- **Test-condition dependency (not an edge).** On a floating-base plant, contact observability is evaluated while the body stays in the operating region where the contact class is defined. If the body falls, the class is undefined. This makes S0a (or a support fixture, or a stable mode) a **test-condition enabler** for S2a evaluation on hardware. It is not a property S2a's information content requires. It does not upgrade the edge.
- **Grade-2 role.** No obligatory role for S2a is realized only by S0a. **Fails.**

## Citation-ablation (B.8.7)

Without the S0-first narrative (C-P1-003), and without D-P1-001, which B.8.3 forbids citing, nothing supports the edge. **Collapses → Grade 3.**

## Conclusion

No necessity edge. The record's best current estimate is that S2a and S0a are **parallel** with respect to necessity. They share engineering resources (a fast tier, effort sensing) and a hardware-test enabler.

## Falsifier / challenge mode

Reading A would be refuted by a system meeting S2a's divergence/information floor for a declared contact class with no S0a competence: a stable or supported mode, or an envelope-free evaluation. An upgrade would need an argument that `I(Z; X)` or detection divergence depends on a property only S0a supplies.

## Use restriction

May not gate or veto Eng-1. An Eng-1 proposal working on S2a before S0a completion **bypasses this edge (Grade 3)** and must list it as bypassed (B.8.5). No lock forbids the bypass.

## Counterexample-search spike registered?

**No (PLAN proposed).** One-line PLAN: on the C-P1-012 planar 2-link fixed-base arm (no envelope controller), measure the detection divergence or TPR at a fixed false-event rate for a declared contact class. A counterexample to Reading A is any cell meeting the declared floor. B.9.8 applies.
