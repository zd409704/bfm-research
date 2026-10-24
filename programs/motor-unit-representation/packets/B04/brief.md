# Brief B04: Composing Frozen Local Motor-Unit Representations (`B/actor`) into Multi-Joint Limb Controllers Under Coupled Loads

**Packet ID**: `B04`
**Status**: `IN_PROGRESS`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`
**Tie Margin**: `5.0` points out of `100.0`
**Baseline References**: `baseline/01-motor-unit-proprioception-and-representation-design.md` (§4), `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md` (Audit Issue #9)

---

## 1. Problem Statement

The foundational motivation of the `motor-unit-representation` program is that a converged, frozen single-actuator module $(B_\omega, \pi_\theta)$ (`281,617` parameters) can be instantiated at every joint $j \in \{1, \dots, N_J\}$ of a multi-joint robot (such as a 2-DoF planar leg or a multi-DoF bipedal limb), allowing an upper-level coordinator $\Pi_{\mathrm{upper}}$ to output local latent commands $z_{16}^{(1)}, \dots, z_{16}^{(N_J)}$ rather than raw joint torques.

However, Audit Issue #9 (`baseline/03`) notes that a critical physical discrepancy arises when transitioning from a single-actuator testbed (where housing link $P$ is inertially fixed or undergoes only quasi-static gravity rotation) to a serial multi-joint kinematic chain:
- In a serial chain (e.g., hip joint $j=1$ and knee joint $j=2$), the knee's housing link $P_2$ is the hip's driven link $D_1$, which undergoes large linear accelerations $a_{P_2}$, angular velocities $\omega_{P_2}$, and angular accelerations $\dot{\omega}_{P_2}$.
- Consequently, joint $j=2$ experiences **inter-joint inertial coupling, Coriolis/centrifugal torques, and multi-joint ground reaction forces** through its distal link $D_2$.

**Core Question**: Under what conditions do the E2 (contact), E3 (sustained external load), and E4 (impulse recovery) regimes of the single-actuator training distribution cover the inter-joint coupling torques of a serial multi-joint limb, and what minimal 2-DoF serial-limb benchmark falsifies or validates the composition hypothesis?

---

## 2. Hard Constraints & Non-Goals

- Must keep each local unit's deployed $(B_\omega, \pi_\theta)$ weights **frozen** during downstream multi-joint control to test true modular reuse.
- Must compare against a fair baseline: an upper-level controller outputting raw torques $u \in [-1, 1]^{N_J}$ with access to the exact same joint proprioception.

---

## 3. Deliverables Required from Primary Authors

1. **Multi-Body Coupling Dynamics Reduction**: Write the exact Euler-Lagrange equations of a 2-DoF serial limb (hip $j=1$, knee $j=2$ with foot contact) and express the coupling torques $(\tau_{\mathrm{inertial}}^{(j)}, \tau_{\mathrm{Coriolis}}^{(j)}, \tau_{\mathrm{grav}}^{(j)}, \tau_{\mathrm{contact}}^{(j)})$ acting on joint $j$ in the local unit equation of motion (`baseline/01` §3.1). Determine when those coupling torques fall inside vs outside the single-unit E0–E4 training envelope.
2. **Upper-Layer Calling Architecture Comparison**: Compare the three upper-layer calling modes from `baseline/01` §4 on the 2-DoF limb:
   - Mode A: Direct latent policy $\Pi_{\mathrm{upper}}(O_{\mathrm{limb}}) \to (z_{16}^{(1)}, z_{16}^{(2)})$.
   - Mode B: Target local outcome decoding $\Pi_{\mathrm{upper}}(O_{\mathrm{limb}}) \to (g_{13}^{\mathrm{des},(1)}, g_{13}^{\mathrm{des},(2)}) \xrightarrow{B_\omega} (z_{16}^{(1)}, z_{16}^{(2)})$.
   - Baseline C: Direct raw torque policy $\Pi_{\mathrm{raw}}(O_{\mathrm{limb}}) \to (u^{(1)}, u^{(2)})$.
3. **Standardized 2-DoF Transfer Benchmark Specification (Closing Audit Issue #9)**: Specify the exact 2-DoF serial limb tasks (free-space tracking, payload squat/hold, and ground-impact hopping/landing), sample-efficiency metrics, and zero-shot morphology-transfer tests (changing link length $L_2$ or actuator capacity $C_0$).

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Exactness of Serial-Chain Coupling Reduction | 30% | Quantifies inertial/Coriolis coupling relative to E3/E4 torque amplitudes. |
| Fairness of Modular vs Raw-Torque Ablation | 25% | Controls for observation history, control rate (50 Hz), and update budget. |
| Morphology-Transfer Falsifiability | 25% | Tests zero-shot or few-shot adaptation when $L_D$ or $C_0$ is swapped. |
| Benchmark Reproducibility | 20% | Provides a complete, self-contained specification closing Audit Issue #9. |
