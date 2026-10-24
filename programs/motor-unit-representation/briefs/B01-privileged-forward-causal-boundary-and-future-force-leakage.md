# Brief B01: Privileged Forward Input Causality, Exogenous vs Endogenous Future Load Boundaries, and 22-Group Schema Audit

**Packet ID**: `B01`
**Status**: `READY_NOT_STARTED`
**Baseline References**: `baseline/01-motor-unit-proprioception-and-representation-design.md`, `baseline/02-v3-asymmetric-network-and-training-specification.md`, `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md` (Audit Issue #4)

---

## 1. Problem Statement

In `LOCAL_RESPONSE_ASYM_FB_V3`, the dual forward networks $F_{\eta_1, \eta_2}(x_{137,t}, p_{5065,t}, a_t, z_{16})$ read a 5,065-dimensional privileged physical context tensor $p_{5065,t}$ partitioned across 22 schema boundaries (`4,822` physical/solver fields + `243` historical privileged memory fields). Audit Issue #4 (`baseline/03`) reveals that Groups 18–21 pack future external disturbance values alongside current physical states without separating:
1. **Exogenous Open-Loop Disturbance Schedule Parameters** (e.g., pre-sampled constant torque bias, ramp rate, or scheduled release countdown timer of the environment's Markov state at time $t$), which are causally determined at time $t$ independent of $a_t$, versus
2. **Endogenous State-Dependent Future Reaction Forces** (e.g., contact normal forces, end-stop spring forces, or velocity-dependent friction at $t+1..t+K$), which depend on the action $a_t$ and future actions $a_{t+1..t+K-1}$.

**Core Question**: Which exact slices of the 22 schema groups in $p_{5065,t}$ are valid causal Markov state variables of the environment at time $t$, which slices leak endogenous future outcomes of $a_t$, and how should $p_{5065,t}$ be sanitized so that $F_{\eta_1, \eta_2}$ remains strictly causal while preserving full regime disambiguation across E0–E4?

---

## 2. Hard Constraints & Non-Goals

- Must keep the deployed modules $B_\omega(g_{13})$ and $\pi_\theta(x_{137}, z_{16})$ (`281,617` parameters total) 100% free of privileged inputs.
- Must account for every one of the 22 schema boundaries (`4,822 + 243 = 5,065` dims) and specify whether each group is retained as-is, replaced by causal generator state at time $t$, or masked.

---

## 3. Deliverables Required from Primary Authors

1. **Formal Causality Partition of $p_{5065}$**: Define the mathematical distinction between exogenous environment Markov state $\xi_t$ (where $P(\xi_{t+1} \mid \xi_t)$ is independent of $a_t$) and endogenous physical reaction $y_{t+1}(s_t, a_t, \xi_t)$, and classify all 22 groups of $p_{5065}$.
2. **Bellman Bias Proof**: Prove how leaking endogenous post-action forces at $t+1$ into $F(x_t, p_t, a_t, z)$ distorts the policy gradient $\nabla_a F(x_t, p_t, a_t, z)^\top z$ (specifically, allowing $F$ to read the consequence of $a_t$ from $p_t$ rather than from its action input $a_t$, which zeroes or corrupts $\partial F / \partial a_t$).
3. **Minimal Empirical Spike Protocol**: Define a Jacobian sensitivity test measuring $\|\partial F / \partial a_t\|_2$ vs $\|\partial F / \partial p_{\mathrm{future}}\|_2$ before and after causal sanitization of Groups 18–21.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Action-Jacobian Degeneracy Proof | 35% | Rigorously proves how future endogenous force leakage bypasses the action input $a_t$ in $F$. |
| Completeness of 22-Group Audit | 25% | Explicitly specifies the causal replacement for every acausal slice in $p_{5065}$. |
| Preservation of E0–E4 Disambiguation | 20% | Retains full Markov observability of load/contact regimes at time $t$. |
| Spike Falsifiability | 20% | Pre-registers quantitative action-gradient norm and Bellman residual checks. |
