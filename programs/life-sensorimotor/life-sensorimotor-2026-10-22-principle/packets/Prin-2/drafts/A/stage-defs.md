# Author-A working stage definitions (Prin-2)

The permitted sources name S0a ("bounded-response viability") and S0b ("remaining reflex/impedance content") and refer to S2a as a "contact observability floor". They do not define S1 or S2. The definitions below are **Author-A working definitions (W-defs)**. Every edge claim in this draft depends on them. If the Orchestrator or human lead ratifies different stage definitions, each affected claim must be re-scoped, and that re-scoping is logged as a B.9.6 event.

| Stage | W-def (generic home humanoid / target plant) |
|---|---|
| **S0a** | Bounded-response viability: the body envelope is robustly maintained under a declared set of initially hidden disturbances, within a declared response deadline (C-P1-001 fixture form; C-P1-002 role form). |
| **S0b** | Remaining reflex/impedance content: fast-tier rendering of impedance/compliance and reflexive responses beyond viability, e.g., a passive virtual impedance at a joint (C-P1-010 setting). |
| **S1** | Policy-tier goal-directed whole-body motor competence (posture, locomotion, reach) commanded at the policy period `T_R2` (≈ 20 ms placeholder), including support-contact handling but **no reasoning about non-support contacts**. |
| **S2a** | Contact observability floor: the body-loop export `X` carries at least a declared amount of information about a declared non-support contact variable `Z` (onset/wrench/link, window, resolution; C-P1-011 premise 1) for a declared contact class (C-P1-012 premise 3). |
| **S2** | Contact-aware interaction: detecting, localizing and responding to non-support contacts with unknown passive environments (objects, humans) to a declared task specification. |

## Two readings of every edge (B.8: "must precede, **or** be available to")

- **Reading P (precede / acquisition order):** stage *k* must be *acquired or engineered first*, before work on *k+1*. This is a statement about evolutionary, developmental or engineering order (B.8.6).
- **Reading A (availability / runtime):** any system that has competence *k+1* under stated premises must, at runtime, have available a signal, bound or property that stage *k* names. It says nothing about which is built first, or whether *k* and *k+1* are realized by the same mechanism.

Author-A position: Grade-1/Grade-2 arguments of the B.8.2 kinds (information, stability, resource, obligatory role) can at most establish **Reading A**. No permitted source contains an argument for Reading P that survives citation-ablation. A planned order (D-P1-001) is not evidence (B.8.3). Therefore **Reading P is Grade 3 quarantined for every edge in this packet**. Each claim record states its Reading A grade separately and names the quarantined Reading P explicitly, so that no one can cite an upgraded Reading A as if it were an order.
