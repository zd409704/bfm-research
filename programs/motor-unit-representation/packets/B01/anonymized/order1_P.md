# Candidate P (Packet B01): Privileged Forward Input Causality, Exogenous vs Endogenous Future Load Boundaries, and 22-Group Schema Audit

**Packet ID**: `B01`
**Author Slot**: Primary Author A
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`
**Frozen Context Read**: `PROGRAM_CHARTER.md`, `packets/B01/brief.md`, `baseline/01`, `baseline/02`, `baseline/03` (Audit Issue #4)
**Status of Every Claim Below**: `Candidate` (Appendix B.4). Nothing in this draft is empirical evidence; Section 5 is a pre-registration, not a result.

---

## 0. Summary of Position

1. **The defect is statistical, not graph-level.** Endogenous post-action fields in $p_{5065,t}$ are leaf tensors in replay; no gradient ever flows from $a_t$ into them. The bias arises because the critic *regresses conditionally on* those fields, so the population-optimal $F$ routes the effect of $a_t$ through $p_t$ instead of through its action port. Consequently, stop-gradient remedies are provably no-ops (Section 3.1).
2. **One state-revealing step is enough for total degeneracy.** If $(x_{137,t}, p^{c}_t, y_t)$ determines the post-action state $s_{t+1}$, the Bayes-optimal $F$ is constant in $a_t$ on its support, the deterministic policy gradient vanishes or is fixed purely by inductive bias, and the leaky Bellman operator collapses to the *behavior* Bellman operator, erasing $z$-dependence (Section 2.3).
3. **Partial leaks attenuate or sign-invert $\partial F/\partial a_t$.** A closed-form linear-Gaussian analysis gives retention $\chi = 1/(1+\mathrm{SNR}_{\mathrm{leak}})$ for outcome-measuring leaks and an explicit sign-inversion condition for stiff end-stop reactions (Section 2.4).
4. **Sanitization is width-preserving.** The proposed $p^{\mathrm{causal}}_{5065,t}$ keeps all `5,065` slots (so $F_{\eta_1}, F_{\eta_2}$ keep `2,805,008` parameters each and the deployed `281,617`-parameter $B_\omega + \pi_\theta$ is untouched). `3,929` dims are retained as-is, `816` are replaced by causal state or generator state at $t$, and `320` are masked.
5. **E0–E4 disambiguation is preserved exactly at the Bellman fixed point**, because the joint Markov state $(s_t^-, \xi_t, \theta)$ stays recoverable from $(x_{137,t}, p^{\mathrm{causal}}_t)$; the only variance lost is acausal hindsight variance, which no causal input can recover (Section 1.5, Claim `C-B01-P-02`).
6. **The masking-to-EMA-only alternative is rejected** because exogenous schedule phase (release countdown, remaining hold time, ramp onset) is part of $\xi_t$ but is not measurable with respect to the past, so an EMA-only critic is forced into aliasing on E3/E4 (Section 3.2).

---

## 1. Formal Causality Partition of $p_{5065}$ Across All 22 Schema Groups

### 1.1 Time-Indexing Convention

Control boundaries occur every $\Delta t_{\mathrm{ctrl}} = 20\text{ ms}$; each control interval $[t, t+1)$ contains four $5\text{ ms}$ physics substeps $t + \tfrac{1}{4}, t + \tfrac{2}{4}, t + \tfrac{3}{4}, t+1$. The action $a_t = u_{\mathrm{clip},t}$ is applied with zero-order hold over $[t, t+1)$. We write $t^-$ for the simulator state at boundary $t$ **before** $a_t$ is written to the actuator, and

$$
\mathcal{F}_t^- \;=\; \sigma\bigl(s_0,\ \xi_0,\ \theta,\ a_{0:t-1},\ \omega_{0:t}\bigr)
$$

for the information available at $t^-$, where $\theta$ is the static plant/morphology parameter vector (one of the 144 configurations), $\xi_t$ is the exogenous disturbance-generator state, and $\omega_{0:t}$ is all exogenous randomness realized up to $t$.

### 1.2 Definitions

**Definition 1 (Exogenous environment Markov state).** A process $(\xi_t)$ is *exogenous* if for all $t$,

$$
P\bigl(\xi_{t+1} \in \cdot \,\bigm|\, \xi_t,\ s_{0:t},\ a_{0:t}\bigr) \;=\; P_\xi\bigl(\xi_{t+1} \in \cdot \,\bigm|\, \xi_t\bigr),
$$

i.e. the generator never reads robot state or action. Equivalently, under any intervention $\mathrm{do}(a_t = a)$ vs $\mathrm{do}(a_t = a')$ with common random numbers, $\xi_{t+1}$ is bitwise identical.

**Definition 2 (Endogenous physical reaction).** A quantity $y_{t+k}$, $k \ge 1$, is *endogenous at lag $k$* if it is of the form

$$
y_{t+k} \;=\; h\bigl(s_{t+k},\ \xi_{t+k}\bigr), \qquad s_{t+1} = f(s_t, a_t, \xi_t, \omega_{t+1}),
$$

with $h$ non-constant in $s$ on the reachable set, so that its law under $\mathrm{do}(a_t = a)$ differs from its law under $\mathrm{do}(a_t = a')$ for some $a \ne a'$. Contact normal/tangential forces, end-stop spring-damper forces $k_s\,\delta + d_s\,\dot\delta$, velocity-dependent friction, and the joint-axis projection $\tau = \hat u^\top\bigl(r_D(q_{t+k}) \times F^W\bigr)$ of a world-frame wrench are all endogenous.

**Definition 3 (Admissibility at $t$).** A privileged field $f_t$ is *admissible* iff it is $\mathcal{F}_t^-$-measurable. Under this definition:
- the generator's open-loop envelope $\psi(\xi_t, k)$ (a deterministic function of $\xi_t$ evaluated at future offset $k$) **is** admissible;
- a realized future torque $\tau_{\mathrm{ext}, t+k} = h(s_{t+k}, \xi_{t+k})$ is **not** admissible if $h$ depends on $s$ (endogenous), and is also not admissible if $\xi$ evolves stochastically after $t$ (it then carries post-$t$ exogenous noise $\omega_{t+1:t+k}$, i.e. *exogenous clairvoyance*, treated in Section 3.3).

**Definition 4 (Three classes).**
- **R — retain-as-is**: the field, as specified, is already $\mathcal{F}_t^-$-measurable (subject to the timestamp assertion of Section 1.6).
- **G — replace by causal state or causal generator state at $t$**: the field carries regime/load information that is needed, but its current realization is post-action or post-$t$; it is replaced by an $\mathcal{F}_t^-$-measurable surrogate of identical width. Subtypes: **G-ξ** (function of $\xi_t$), **G-s** (pre-action snapshot $s_t^-$), **G-h** (causal history mirror).
- **M — mask**: the field has no admissible counterpart with regime value; it is set to the constant $0$ after normalization, and its normalizer statistics are frozen at $(\mu, \sigma) = (0, 1)$ so that Issue 6 normalizer drift cannot reintroduce sample information.

### 1.3 Two Hidden Endogeneity Traps in the Generator Itself

Groups 18–21 are nominally "external disturbance" fields, but three of the generator modes described in `baseline/02` §4.2 make even the *generator* endogenous:

1. **Sign mode "opposing or assisting motion"** (E3): $\tau_{\mathrm{ext}} = m(\xi_t)\cdot \operatorname{sign}(\pm\dot q_c)$ depends on $s$. The magnitude envelope $m(\xi_t)$ is exogenous; the realized signed torque is endogenous.
2. **World-frame wrench application**: if the load is a Cartesian force $F^W$ at the tip, the joint torque depends on $q_{t+k}$. $F^W(\xi_t, k)$ is exogenous; its joint-axis projection is endogenous.
3. **Event-triggered release**: if the E3→E4 release edge is triggered by a robot-state event (e.g. "release after the joint has held $|\dot q| < \varepsilon$ for 25 steps"), then the release countdown is endogenous. This is a live cross-packet risk: the natural fix for Issue 1 (B02) is a schedule synchronized to hold progress. If B02 adopts a state-triggered schedule, the admissible representation is the **trigger rule parameters plus the causal progress counter** (consecutive qualifying steps achieved up to $t^-$), never the future release time.

Finally, the scene label one-hot `E0..E4` is admissible only if it is the **allocation label sampled at reset**. Any step label derived retrospectively by the coverage evaluator (e.g. "this window qualified as post-load recovery") is a function of the future trajectory and must not enter $p_t$.

### 1.4 22-Group Classification Table

`baseline/02` §2.3 freezes only the block totals (`1,920 / 1,024 / 1,152 / 726 / 243`). The per-group widths below are a **nominal reconstruction** consistent with those totals; they must be reconciled against the V3 schema manifest in Spike Step 0 (Section 5.2). The classification is defined per *field semantics + timestamp*, and is enforced per field by the bitwise action-invariance audit, so it does not depend on the nominal widths being exact.

| Grp | Nominal content | Dims (nominal) | Causality risk | Class | Sanitized content in $p^{\mathrm{causal}}_t$ | E-regime role |
|---:|---|---:|---|:-:|---|---|
| 1 | Substep generalized positions (joint, rotor, backlash, obstacle bodies), 4 substeps | 320 | Post-action if logged for $[t, t+1]$ after `step(a_t)` | R | Substeps of $[t-1, t]$ ending at $t^-$ | All (state) |
| 2 | Substep generalized velocities | 320 | Same | R | Substeps of $[t-1, t]$ | All |
| 3 | Substep generalized accelerations | 320 | Same; final-substep accel at $t^-$ uses $u_{t-1}$ only | R | Substeps of $[t-1, t]$ | E1/E2 impacts |
| 4 | Substep actuator forces (post-saturation, post-gear) | 320 | Same; else causal (driven by $u_{t-1}$) | R | Substeps of $[t-1, t]$ | E3 saturation |
| 5 | Substep constraint forces (joint/stop/contact) | 320 | Same | R | Substeps of $[t-1, t]$ | E1/E2 |
| 6 | Solver residuals / iteration counts | 320 | Non-physical; residual of the solve that consumes $a_t$ is post-action; integrator-specific shortcut | **M** | $0$ | None (no physical regime information beyond G5/G16) |
| 7 | Link $D$ + payload mass, inertia tensor, COM | 160 | Static within episode | R | As-is | Morphology |
| 8 | Viscous damping $b$, Coulomb $\tau_c$, Stribeck table | 192 | Static | R | As-is | Morphology |
| 9 | Gear backlash, compliance | 160 | Static | R | As-is | Morphology |
| 10 | Capacity $C_0$, saturation $S = 1.25\,C_0$, thermal state | 160 | Thermal state must be value at $t^-$ (integrates past current; admissible) | R | As-is, thermal at $t^-$ | E3 saturation |
| 11 | Drive electrical/latency parameters | 160 | Static | R | As-is | Morphology |
| 12 | Stroke geometry, stop placement vs gravity, $L_D$ | 192 | Static | R | As-is | E1 |
| 13 | Signed distances, obstacle geometry/pose, contact material ($k_c$, $d_c$, restitution, $\mu$) | 256 | Configuration function at $t^-$; scheduled obstacle motion is exogenous | R | As-is at $t^-$; scheduled obstacle poses as generator parameters | E2 |
| 14 | Normal/tangential contact forces | 256 | Read from the solve of $[t, t+1]$ ⇒ post-action | **G-s** | Impulse-averaged contact force over last completed interval $[t-1, t]$ + force at final substep $t^-$ | E2 |
| 15 | Contact Jacobian projections | 192 | Function of $q$ at $t^-$ | R | As-is at $t^-$ | E2 |
| 16 | End-stop spring-damper penetration $\delta$, $\dot\delta$, stop force | 256 | Function of $(q, \dot q)$ at $t^-$ | R | As-is at $t^-$ | E1 |
| 17 | Active constraint masks | 192 | Active set computed by next solve is post-action | R | Active set at $t^-$ | E1/E2 |
| 18 | Generator parameters + regime: scene allocation one-hot (5), profile family one-hot (bias/ramp/sine/impulse/step-release), bias magnitude, ramp slope and onset/offset, sine $A/f/\phi$, impulse magnitude/duration/countdown, release timer, quiet-window timer, sign mode, application mode, $F^W$ direction/point | 64 | Exogenous iff Definition 1 holds; endogenous if release is state-triggered (Section 1.3) | R | As-is (pre-action timer values); state-triggered schedules → trigger parameters + causal progress counter | **E3/E4 primary** |
| 19 | Current external load over $[t-1, t]$: joint torque, 6-D world wrench, application point (4 substeps) | 102 | Causal if past interval | R | Substeps of $[t-1, t]$ | E3/E4 |
| 20 | **Future external torque/wrench window** $\tau_{\mathrm{ext}, t+1:t+K}$, $K = 10$ control steps × 4 substeps × 7 channels | 280 | Endogenous under sign mode, world-wrench projection, state-triggered release, or solver-clipped delivery; clairvoyant under stochastic $\xi$ | **G-ξ** | Open-loop envelope $\Psi_t[k] = \psi(\xi_t, k)$: magnitude envelope $m(\xi_t, k)$ + world wrench $F^W(\xi_t, k)$ for $k = 1..40$ substeps; conditional mean/hazard for stochastic arrivals | E3/E4 (schedule preview) |
| 21 | **Future reaction window** (end-stop, contact, friction reaction torques at $t+1..t+K$), 40 substeps × 7 | 280 | Endogenous by construction | **G-h** | Causal mirror window: realized reaction torques over $[t-K, t]$ (40 past substeps × 7) | E1/E2/E4 transients |
| 22 | Privileged feature memory: EMAs and multi-scale summaries of load, contact impulse, slip over preceding 320 ms | 243 | Admissible iff EMA is updated with data up to $t^-$ only (not inside `step(a_t)` before storage) | R | As-is with update-order assertion | E3/E4 (load history), E2 slip |

**Dimension accounting.**

| Class | Groups | Dims |
|---|---|---:|
| R (retain-as-is) | 1–5, 7–12, 13, 15, 16, 17, 18, 19, 22 | `1,600 + 1,024 + 896 + 64 + 102 + 243 = 3,929` |
| G (replace by causal state / generator state at $t$) | 14 (G-s), 20 (G-ξ), 21 (G-h) | `256 + 280 + 280 = 816` |
| M (mask) | 6 | `320` |
| **Total** | 22 groups | **`5,065`** (`4,822` physical/solver + `243` memory) |

Note that "R" for Groups 1–5, 13–17, 19 is **conditional on orientation**: if the current logger fills these from the $[t, t+1]$ interval (assembling $p_t$ after `env.step(a_t)`), the fields literally contain $s_{t+1}$ and are the most severe leak in the tensor, more severe than Groups 20–21. The remedy is a one-step index shift, not masking. Spike Step 0 decides this per field.

### 1.5 Sanitized Construction $p^{\mathrm{causal}}_{5065,t}$

Let $\Pi_j$ denote the slot projector for group $j$ in the frozen 5,065-slot layout, $\mathcal N$ the running normalizer, and $\mathcal{R} = \{1..5, 7..13, 15..19, 22\}$ the retained set. Define, slot by slot,

$$
\Pi_j\, p^{\mathrm{causal}}_{t} \;=\;
\begin{cases}
\mathcal N_j\bigl(\Pi_j\, p_{t^-}\bigr), & j \in \mathcal R,\\[3pt]
\mathcal N_{14}\Bigl(\tfrac{1}{\Delta t_{\mathrm{ctrl}}}\textstyle\int_{t-1}^{t} \lambda_c(\tau)\,d\tau,\ \lambda_c(t^-)\Bigr), & j = 14,\\[3pt]
\mathcal N_{20}\bigl(\Psi_t\bigr),\quad \Psi_t[k] = \bigl(m(\xi_t, k),\ F^W(\xi_t, k)\bigr)_{k=1}^{4K}, & j = 20,\\[3pt]
\mathcal N_{21}\bigl(\tau_{\mathrm{react},\,t-K:t}\bigr), & j = 21,\\[3pt]
0, & j = 6,
\end{cases}
$$

with three implementation invariants:

1. **Pre-action assembly.** $p^{\mathrm{causal}}_t$ is assembled in the environment's `observe()` call **before** `step(a_t)` and stored with the transition as-is; the next-state tensor $p^{\mathrm{causal}}_{t+1}$ used by target networks is assembled at $(t+1)^-$ by the same routine.
2. **Stateless preview.** $\Psi_t$ is produced by a pure function `generator.preview(xi_t, K)` that receives a copy of $\xi_t$ only and must raise if it reads robot state. This makes the G-ξ slot admissible by construction rather than by inspection.
3. **Bitwise action invariance.** For any snapshot and any $a_t \ne a'_t$ (and any perturbation of $a_{t+1:t+K-1}$), $p^{\mathrm{causal}}_t$ is bitwise identical. This is the operational definition of admissibility (Spike Step 0).

**Proposition 1 (Preservation of E0–E4 disambiguation at the Bellman fixed point).** Let $Z_t = (s_t^-, \xi_t, \theta)$ be the joint Markov state of the simulator, so $P(Z_{t+1} \mid Z_{0:t}, a_{0:t}) = P(Z_{t+1} \mid Z_t, a_t)$. If $(x_{137,t}, p^{\mathrm{causal}}_t)$ determines $Z_t$ up to components irrelevant to this kernel, then for every $z$ and every policy $\pi_z$ the successor measure $M^{\pi_z}(Z_t, a, \cdot)$ — and therefore the FB fixed point $F^{\star}(\cdot, a, z)$ — is a measurable function of $(x_{137,t}, p^{\mathrm{causal}}_t, a, z)$.

*Proof.* $M^{\pi_z}(Z_t, a, \cdot) = \sum_{k \ge 0} \gamma^k P^{\pi_z}(g_{t+k+1} \in \cdot \mid Z_t, a_t = a)$ depends on the past only through $Z_t$ by the Markov property, and $Z_t$ is a function of the sanitized input by hypothesis. $\square$

The sufficiency hypothesis is met by the table: $s_t^-$ is carried by Groups 1–2 (final substep), 13, 16, 17 and by $x_{137}$; $\theta$ by Groups 7–12 and the material fields of Group 13; $\xi_t$ by Group 18 (Group 20 is a deterministic, redundant but conveniently pre-evaluated function of $\xi_t$). The three aliasing cases of `baseline/01` §3.1 resolve as follows:

| Aliasing case (`baseline/01` §3.1) | Disambiguating variable | Admissible carrier |
|---|---|---|
| Rigid end-stop stall (E1) | $\delta, \dot\delta$, stop stiffness, $d_{\min}/d_{\max}$ | G16, G12, $x_{137}$ |
| Elastic/rigid obstacle contact (E2) | signed distance, $k_c, d_c$, restitution, contact force at $t^-$ | G13, G14 (G-s), G15, G17 |
| Sustained load (E3) | bias magnitude, ramp slope, remaining hold time, sign mode | G18, G19, G20 (G-ξ), G22 |
| Temporary pulse about to release (E4) | release countdown, quiet-window timer, pre-release load level | G18 timers, G20 envelope, G22 EMA |
| Free space (E0) | none beyond state/morphology | G1–G5, G7–G12 |

**Corollary (what sanitization loses).** Define the *acausal explained variance* of the leaky input $y_t$ as

$$
\mathrm{AEV} \;=\; \mathbb{E}\Bigl[\operatorname{Var}\bigl(\mathbb E[T_t \mid x_t, p^{c}_t, y_t, a_t] \bigm| x_t, p^{c}_t, a_t\bigr)\Bigr] \;\ge\; 0,
$$

where $T_t$ is the Bellman target (Section 2.1). Sanitization increases the irreducible TD residual by exactly $\mathrm{AEV}$, and by Proposition 1 none of it is Bellman-relevant. This bears directly on H1: the "$>95\%$ of TD-target explained variance" criterion is attainable only if $\mathrm{AEV}$ is below $5\%$ of target variance. If the spike measures a larger drop, that measures the size of the leak, not a loss of disambiguation; H1 should then be read against the factual EV of a causal critic plus the probe gates of Section 5.5, not against the leaky critic's inflated EV. This is a reading note for adjudication, not an amendment of H1.

### 1.6 Timestamp Assertions to Wire into the Collector

| Assertion | Applies to | Failure meaning |
|---|---|---|
| `p_t` assembled before `step(a_t)` | all groups | Groups 1–5, 13–17, 19, 22 contain $s_{t+1}$ |
| Generator timers read before decrement for step $t$ | G18 | Off-by-one leak of whether release happens in $[t, t+1)$ |
| `preview()` has no robot-state argument | G20 | Endogenous envelope |
| EMA update ordered after storage of `p_t` | G22 | Memory includes $[t, t+1]$ impulse |
| Scene one-hot = reset allocation label | G18 | Evaluator-derived future labels |

---

## 2. Bellman Bias and Action-Jacobian Degeneracy Proof

### 2.1 Setup

Write $u = (x, p, a, z)$ and partition the privileged input as $p_t = (p^{c}_t, y_t)$, with $p^{c}_t$ admissible and $y_t$ the endogenous future window (Groups 20–21 as logged, or Groups 1–5 if post-action). Endogeneity is expressed as a reparameterization

$$
y_t = Y(Z_t, a_t, \omega), \qquad \omega \perp a_t \mid Z_t,
$$

where $\omega$ collects post-$t$ exogenous noise and the behavior policy's own randomness $\varepsilon_{t+1:t+K-1}$ (future behavior actions are $a_{t+k} = \mu(x_{t+k}, \varepsilon_{t+k})$, so $Y$ is a composite deterministic map of $(Z_t, a_t, \omega)$).

For the FB measure loss with $\Sigma_B = \mathbb E_\rho[B B^\top] \approx I_{16}$ (`baseline/02` §5.2), expanding the loss pointwise shows its population minimizer is the conditional expectation

$$
F^{\star}(u) = \mathbb E\bigl[T_t \bigm| u_t = u\bigr], \qquad T_t = B_\omega(g_{13,t+1}) + \gamma\, \bar F\bigl(x_{t+1}, p_{t+1}, \pi_\theta(x_{t+1}, z), z\bigr),
$$

with $\bar F$ the target network. (For $\Sigma_B \ne I$ the same holds with $\Sigma_B^{-1}$ premultiplied; nothing below depends on it.) Every result below applies to any loss whose population minimizer is a conditional expectation, and to any function class rich enough to approach it.

The actor update (`baseline/03` Issue 8) is the deterministic policy gradient

$$
\nabla_\theta J = \mathbb E_{\mathcal D}\Bigl[\bigl(\nabla_\theta \pi_\theta(x_t, z)\bigr)^\top\, \bigl(\partial_a F(x_t, p_t, a, z)\big|_{a = \pi_\theta(x_t,z)}\bigr)^\top z\Bigr],
$$

evaluated on **replay** tuples, so $p_t$ — including $y_t$ — was generated by the behavior action $a^\beta_t$, not by $\pi_\theta(x_t, z)$.

Define the **causal critic** as the leaky critic marginalized over the leak:

$$
F^{c}(x, p^{c}, a, z) \;:=\; \mathbb E_\omega\Bigl[F^\star\bigl(x, p^c, Y(Z, a, \omega), a, z\bigr)\Bigr] \;=\; \mathbb E\bigl[T_t \bigm| x_t = x, p^c_t = p^c, a_t = a\bigr],
$$

the second equality by the tower property. By Proposition 1, $F^c$ is the correct Bellman object.

### 2.2 Lemma 1 (Bypass Identity)

Assume $F^\star$ is $C^1$ in $(y, a)$ on a neighborhood of the support, $Y$ is $C^1$ in $a$, and the derivatives are dominated so differentiation passes under $\mathbb E_\omega$. Then

$$
\boxed{\;\partial_a F^{c}(x, p^c, a, z) \;=\; \underbrace{\mathbb E_\omega\bigl[\partial_a F^\star\bigr]}_{J_a:\ \text{action port}} \;+\; \underbrace{\mathbb E_\omega\bigl[\partial_y F^\star \,\partial_a Y\bigr]}_{J_y Y_a:\ \text{bypass channel}}\;}
$$

*Proof.* Differentiate $F^c = \mathbb E_\omega[F^\star(x, p^c, Y(Z,a,\omega), a, z)]$ in $a$ by the chain rule; exchange derivative and expectation by dominated convergence. $\square$

The total causal sensitivity of the outcome to $a_t$ is conserved, but is *split* between the action port and the channel $a_t \to y_t \to F$. The actor, however, evaluates $F^\star$ on a stored leaf $y_t$: in the computational graph $\partial y_t/\partial a \equiv 0$. Hence

**Theorem 1 (Policy-gradient bias).** Even on the behavior support ($a = a^\beta_t$), the actor's gradient through a leaky critic is

$$
\hat g = \mathbb E\bigl[J_a\bigr]^\top z = \partial_a F^c{}^\top z \;-\; \underbrace{\mathbb E\bigl[\partial_y F^\star\,\partial_a Y\bigr]^\top z}_{\text{bias } b},
$$

and off the behavior support ($\pi_\theta(x_t, z) \ne a^\beta_t$) an additional mismatch arises because $y_t$ encodes the consequences of $a^\beta_t$ (Section 2.5). $\square$

### 2.3 Theorem 2 (Total Degeneracy under a State-Revealing Leak)

**Premise (state-revealing).** There is a measurable map $\Phi$ with $s_{t+1} = \Phi(x_t, p^c_t, y_t)$ almost surely.

This holds in V3 whenever any of the following are present: Groups 1–5 logged post-action (trivially); Group 21 at substep $t + \tfrac14$ while in end-stop contact (stop force $k_s\delta + d_s\dot\delta$ inverts to $(q, \dot q)$ given $\theta$); Group 20 under world-wrench projection with known $F^W$ (the projection reveals $q_{t+k}$ up to a reflection that $x_t$ resolves).

**Theorem 2.** Under the state-revealing premise and $\omega \perp a_t \mid Z_t$:

(a) $T_t \perp a_t \mid (x_t, p^c_t, y_t)$.

(b) $F^\star(x, p^c, y, a, z) = \mathbb E[T_t \mid x, p^c, y]$ for every $a$ in the conditional support of $a_t$ given $(x, p^c, y)$. Where that support has non-empty interior, $\partial_a F^\star = 0$ (**zeroing**). Where it is a single point $a = A(x, p^c, y)$ (when $y$ determines $a$), every function $F^\star + (a - A(x,p^c,y))\, c(x, p, z)$ with arbitrary $c$ attains the same loss, so $\partial_a F^\star = c$ is **unidentified** and is fixed by architecture, initialization, weight decay and SGD implicit bias, not by data (**corruption**).

(c) In the zeroing case, $\hat g \equiv 0$: the actor receives no learning signal through $F$.

(d) If the premise holds on every transition, the leaky Bellman operator reduces to the behavior Bellman operator $\mathcal T^\mu$. Its unique fixed point is the successor measure of the replay mixture $\mu$ (`1/3` rule + `2/3` historical policies), which does not depend on $z$: **$z$-collapse**.

*Proof.* (a) Given $(x_t, p^c_t, y_t)$, $s_{t+1}$ is fixed, so $g_{13,t+1}$ and $x_{t+1}$ are fixed. $p^c_{t+1}$ depends on $(s_{t+1}, \xi_{t+1}, \theta)$, and $\xi_{t+1}$ is exogenous. $y_{t+1}$ depends on $(Z_{t+1}, a^\beta_{t+1}, \omega')$ with $a^\beta_{t+1} = \mu(x_{t+1}, \varepsilon_{t+1})$. None of these depends on $a_t$ except through $s_{t+1}$, which is fixed. Hence $T_t$ is conditionally independent of $a_t$.
(b) Conditional expectation of a variable independent of $a_t$ given the other inputs does not vary with $a_t$; the non-identification statement follows because the loss only evaluates $F$ on the support.
(c) Immediate from (b) and the actor formula.
(d) If $F$ ignores its action port at every state, then $\bar F(x_{t+1}, p_{t+1}, \pi_\theta(x_{t+1},z), z) = \bar F(x_{t+1}, p_{t+1}, \cdot, z)$, and the successor states are drawn from replay generated by $\mu$. The recursion $F = \mathbb E[B(g_{t+1}) + \gamma \bar F \mid x, p]$ then has the $\gamma$-contraction fixed point $\sum_k \gamma^k\, \mathbb E^\mu[B(g_{t+k+1}) \mid x_t, p_t]$, in which $z$ does not appear. $\square$

**Remark (one step suffices).** Theorem 2 needs only that the leak reveals $s_{t+1}$; the window length $K$ does not matter. Shortening the window from $K = 10$ to $K = 1$ is therefore **not** a mitigation.

**Remark (regime selectivity).** In E0 free space, Group 21 reaction windows are near zero and carry no state information, so the degeneracy concentrates in E1 (stop contact), E2 (obstacle contact), and E3 with world-frame or motion-signed loads. These are exactly the strata where V3 must learn holding and escape. This is *consistent with* the `0` load-hold and recovery counts in `baseline/03` but is **not evidence for** them; Issue 1's schedule desynchronization is an independently sufficient documented cause.

### 2.4 Partial Leak: Closed-Form Attenuation and Sign Inversion

Project onto the actor-relevant scalar $r = z^\top T_t$. Take a locally linear-Gaussian model around a state:

$$
r = c\,a + w, \qquad y = \lambda_a\,a + \lambda_w\,w + \nu, \qquad a \sim \mathcal N(\bar a, \sigma_a^2),\ w \sim \mathcal N(0, \sigma_w^2),\ \nu \sim \mathcal N(0, \sigma_\nu^2),
$$

mutually independent. Here $c$ is the true causal action sensitivity ($\partial_a F^c{}^\top z = c$), $w$ is exogenous outcome noise (unmodeled disturbance, contact restitution scatter), $\lambda_a$ is the direct action-to-reaction gain, $\lambda_w$ is the gain with which the leak reveals $w$, and $\nu$ is leak measurement noise.

**Proposition 2.** With $\kappa = \dfrac{\lambda_w^2 \sigma_w^2}{\lambda_w^2 \sigma_w^2 + \sigma_\nu^2} = \dfrac{\mathrm{SNR}}{1 + \mathrm{SNR}}$, $\mathrm{SNR} = \lambda_w^2\sigma_w^2/\sigma_\nu^2$:

$$
F^\star = \mathbb E[r \mid a, y] = c\,a + \frac{\kappa}{\lambda_w}\bigl(y - \lambda_a a\bigr),
\qquad
J_a = c - \kappa\frac{\lambda_a}{\lambda_w},
\qquad
J_y = \frac{\kappa}{\lambda_w},
\qquad
J_y Y_a = \kappa\frac{\lambda_a}{\lambda_w}.
$$

*Proof.* $w \mid (a, y)$ is Gaussian with mean $\kappa (y - \lambda_a a)/\lambda_w$; substitute into $r = c a + w$. $\square$

The bypass identity $J_a + J_y Y_a = c$ holds exactly. Two physically distinct regimes follow:

- **Outcome-measuring leak** ($\lambda_a = c\,\lambda_w$, i.e. $y$ is a noisy copy of the future outcome, as for G20 world-wrench projections or G1–G5 post-action): $J_a = (1-\kappa)\,c$. The **action-port retention** is
  $$
  \chi := \frac{J_a}{J^{c}_a} = 1 - \kappa = \frac{1}{1 + \mathrm{SNR}} \xrightarrow{\ \sigma_\nu \to 0\ } 0.
  $$
  Simulator-logged forces are noise-free ($\sigma_\nu = 0$), so in simulation $\chi = 0$ exactly whenever $\lambda_w \neq 0$: this is the zeroing case of Theorem 2.
- **Reaction-dominated leak** (stiff end-stop or rigid contact: $c \to 0$ because the joint is blocked, while $\lambda_a \gg 0$ because pushing harder raises the reaction force): **sign inversion** occurs iff
  $$
  \kappa\,\frac{\lambda_a}{\lambda_w} > c,
  $$
  and then $J_a < 0 < c$. Holding the reaction force fixed, a larger command can only be "explained" by a less favorable disturbance, so the critic learns that pushing harder makes the outcome worse. This corrupts E1 limit-escape and E2 contact-force modulation gradients specifically.

### 2.5 Degeneracy Condition in Jacobian Norms

Let $J^c_a = \partial_a F^c$, $J_a = \mathbb E_\omega[\partial_a F^\star]$, $J_{\mathrm{fut}} = \partial F^\star / \partial p_{\mathrm{fut}} \in \mathbb R^{16 \times d_{\mathrm{fut}}}$ with $d_{\mathrm{fut}} = 560$ (Groups 20–21), and $Y_a = \partial p_{\mathrm{fut}} / \partial a_t \in \mathbb R^{d_{\mathrm{fut}}}$, all in normalized input units. Taking norms in Lemma 1 (vector case) gives the two-sided bound

$$
1 - \frac{\|J_{\mathrm{fut}}\|_2 \|Y_a\|_2}{\|J^c_a\|_2} \;\le\; \chi_2 := \frac{\|J_a\|_2}{\|J^c_a\|_2} \;\le\; 1 + \frac{\|J_{\mathrm{fut}}\|_2 \|Y_a\|_2}{\|J^c_a\|_2}.
$$

**Definition ($\varepsilon$-degeneracy).** $F$ is $\varepsilon$-degenerate at a state if $\|J_a\|_2 \le \varepsilon \|J^c_a\|_2$.

**Corollary 1 (Measurable degeneracy statistic).** Define

$$
D \;:=\; \frac{\|J_{\mathrm{fut}}\|_2\, \|Y_a\|_2}{\|J_a\|_2}.
$$

Then $\varepsilon$-degeneracy implies $D \ge (1 - \varepsilon)/\varepsilon$. For example, $\varepsilon = 0.2$ implies $D \ge 4$. Conversely, a small bypass channel, $\|J_{\mathrm{fut}}\|_2 \|Y_a\|_2 \le \varepsilon \|J^c_a\|_2$, guarantees $\chi_2 \ge 1 - \varepsilon$ (no degeneracy).

*Proof.* From Lemma 1, $\|J^c_a\| \le \|J_a\| + \|J_{\mathrm{fut}}\|\|Y_a\|$. If $\|J_a\| \le \varepsilon\|J^c_a\|$ then $\|J_{\mathrm{fut}}\|\|Y_a\| \ge (1-\varepsilon)\|J^c_a\| \ge \frac{1-\varepsilon}{\varepsilon}\|J_a\|$. The converse is the lower bound above. $\square$

Expressed purely through the two critic Jacobians named in the brief, $\varepsilon$-degeneracy requires

$$
\frac{\|\partial F/\partial a_t\|_2}{\|\partial F/\partial p_{\mathrm{fut}}\|_2} \;\le\; \frac{\varepsilon}{1 - \varepsilon}\,\|\partial p_{\mathrm{fut}}/\partial a_t\|_2,
$$

so the ratio of critic Jacobian norms must be read **against the simulator's action-to-window sensitivity** $\|Y_a\|_2$. A small ratio alone is not diagnostic (the window may be large-scale but action-insensitive); a small ratio together with a large $\|Y_a\|_2$ is. Section 5 therefore measures all three.

### 2.6 Bellman Residual Consequences

1. **Inflated factual accuracy.** The factual TD residual of the leaky critic is lower than the causal critic's by exactly $\mathrm{AEV}$ (Section 1.5). In the linear-Gaussian model this is $\kappa\,\sigma_w^2$. This is the "inflated training-time critic accuracy" of Issue 4, made quantitative.
2. **Counterfactual bias at the actor's action.** At $a' = \pi_\theta(x_t, z) \ne a^\beta_t$, with stale $y_t = Y(Z_t, a^\beta_t, \omega)$:
   $$
   F^\star(a', y_t) - \mathbb E[r \mid a'] = \kappa\frac{\lambda_a}{\lambda_w}\bigl(a^\beta_t - a'\bigr) + \kappa\Bigl(w + \frac{\nu}{\lambda_w}\Bigr),
   $$
   so the expected squared counterfactual error exceeds the causal critic's by $\kappa^2 (\lambda_a/\lambda_w)^2\, \mathbb E(a' - a^\beta)^2$, growing with the policy–behavior gap. The `1/3` rule partition maximizes that gap once $\pi_\theta$ departs from the rule controller.
3. **Bootstrap contamination.** The target $\bar F(x_{t+1}, p_{t+1}, \pi_\theta(x_{t+1}, z), z)$ reads $y_{t+1}$, which encodes $a^\beta_{t+1..t+K}$. The backup evaluates a hybrid of $\pi_z$'s action port and $\mu$'s consequences, and in the state-revealing limit reduces to $\mathcal T^\mu$ (Theorem 2d).

These three signatures (factual residual down, counterfactual residual up, $z$-sensitivity down) are jointly diagnostic, and each is pre-registered in Section 5.

---

## 3. Serious Alternative Considered and Rejected

Per method v1.0 §11.5, this draft names three alternatives. The first two were given serious consideration and are rejected with proofs; the third was partly attractive and is rejected on scope grounds.

### 3.1 Alternative A: Keep Future Windows, Stop-Gradient Them w.r.t. $a_t$

**Proposal.** Retain Groups 20–21 as logged, but wrap them in `detach()` / $\operatorname{sg}(\cdot)$ so that "the action gradient cannot flow through the future forces".

**Lemma 2 (Stop-gradient is a no-op).** In replay-based training, $y_t$ is a leaf tensor loaded from the buffer. For both the critic loss $\mathcal L_F(\eta)$ and the actor objective $J(\theta)$, $\nabla_\eta \mathcal L_F[\operatorname{sg}(y)] = \nabla_\eta \mathcal L_F[y]$ and $\nabla_\theta J[\operatorname{sg}(y)] = \nabla_\theta J[y]$.

*Proof.* $y_t$ is not a function of $\eta$ or $\theta$ in the graph; $\operatorname{sg}$ is the identity in the forward pass and changes only derivatives with respect to graph ancestors of $y_t$, of which there are none. $\square$

Therefore the critic's population minimizer is unchanged, $J_a$ and $J_{\mathrm{fut}}$ are unchanged, and Theorems 1–2 apply verbatim. The proposal confuses **graph-gradient flow** with **statistical conditioning**. The bias of Section 2 is produced by $F$ conditioning on $y_t$ in the forward pass, not by any derivative path through $y_t$. In fact, the bias term $b$ in Theorem 1 is precisely the missing $\partial_a Y$ path; stop-gradient asserts that this missing path should stay missing.

**Variants also rejected.**
- *Detach the compressor features of $y$ (freeze the $5065 \to 512$ rows reading $y$).* $F$ still conditions on $y$ through a fixed random projection, and the fusion MLP `[1024, 1024, 512]` learns to read it; only the rate changes.
- *Dropout or noise injection on $y$.* This lowers $\mathrm{SNR}$, so $\chi = 1/(1+\mathrm{SNR})$ improves continuously, but $\chi \to 1$ only as $\mathrm{SNR} \to 0$, which is masking with extra variance. The sign-inversion region $\kappa\lambda_a/\lambda_w > c$ shrinks but does not vanish for stiff stops at any fixed noise level.
- *Recompute $y$ counterfactually for $\pi_\theta$'s action by re-simulating (making $\partial_a Y$ available).* This restores the bypass term, but requires a snapshot-restore simulation of $K$ steps per actor sample, under $\pi_\theta$'s *future* actions as well, which turns the critic into model-based value expansion. It also still feeds endogenous future reactions into $F$, so it does not satisfy Charter boundary 2's requirement to *separate* exogenous schedule parameters from endogenous reactions. Out of scope and not admissible.

The spike includes an `L-sg` arm whose pre-registered prediction is **indistinguishability from arm L** (Gate G-8). Any measurable divergence falsifies Lemma 2's premise, meaning some path computes $y$ in-graph, which would itself be a defect to report.

### 3.2 Alternative B: Mask Groups 18–21 Entirely; Carry All Load Information in Group 22 EMA

**Proposal.** Zero all `726` dims of Groups 18–21 and rely on Group 22's causal EMAs and multi-scale summaries (`243` dims, 320 ms) for load disambiguation. This is attractive because it is trivially causal and needs no generator refactor.

**Lemma 3 (Schedule-phase aliasing).** Let $Z = (s, \xi, \theta)$ and $Z' = (s, \xi', \theta)$ share the same past trajectory over the 320 ms window (hence identical $x_{137}$, Group 22, and every past-measurable field) but differ in a schedule-phase component of $\xi$, e.g. release countdowns $n \ne n'$. If $M^{\pi}(Z, a, \cdot) \ne M^{\pi}(Z', a, \cdot)$, then any critic $F$ whose inputs exclude $\xi$ satisfies
$$
\max\bigl\{\|F(Z) - M(Z)\|,\ \|F(Z') - M(Z')\|\bigr\} \;\ge\; \tfrac12\,\|M(Z) - M(Z')\|.
$$

*Proof.* $F(Z) = F(Z')$ since the inputs coincide; apply the triangle inequality. $\square$

**Premises hold in V3.** In E3, a sustained bias held for $\ge 25$ steps drives every EMA with time constant $\le 320$ ms to its steady state, so states at hold step $j$ and $j'$ share Group 22 while the remaining hold time $25 - j$ differs. In E4, the pre-release states are identical up to the countdown. A release within the effective horizon $1/(1-\gamma)$ changes the successor measure through the post-release transient. The countdown is pre-sampled by the generator, so it is $\xi_t$-measurable but independent of the past. Additionally, Alternative B deletes the **scene allocation one-hot**, the **sign mode**, and the **application mode**, all of which live in Group 18 and are exogenous Markov state.

Alternative B therefore trades a causality violation for a Markov violation. It reintroduces exactly the "temporary disturbance pulse that is about to release" aliasing that `baseline/01` §3.1 cites as the reason privileged inputs exist. **Rejected.** It is retained as spike arm `Z` to measure the cost (Gate G-6 probes).

### 3.3 Alternative C: Keep the *Realized* Exogenous Future Window When the Generator Is State-Independent

**Proposal.** Where $h$ does not depend on $s$ (fixed-sign joint-torque bias, ramps, sinusoids), keep the realized $\tau_{\mathrm{ext}, t+1:t+K}$ instead of the envelope $\Psi_t$.

**Analysis.** Here $\partial_a Y = 0$, so the bypass term vanishes and Theorem 1's gradient bias is zero. If $\xi$ is deterministic given its parameters, the realized window equals $\Psi_t$ anyway. If $\xi$ has post-$t$ randomness, the critic conditions on $\omega_{t+1:t+K}$ (clairvoyance): its gradient is unbiased in expectation, but its Bellman fixed point conditions on more than $Z_t$, its factual EV is inflated, and the deployed actor, which can never see $\omega$, is trained against a hindsight target.

**Rejected** for three reasons:
1. Admissibility would have to be certified per generator mode, and three of the five profile/application modes (motion-signed, world-wrench, state-triggered release) fail it.
2. It makes H1's EV comparison ambiguous.
3. The envelope $\Psi_t$ already carries all of the Bellman-relevant content (Proposition 1).

It is kept as diagnostic spike arm `X` (ungated).

---

## 4. Candidate Necessity Claims (Appendix B)

All claims enter as **Candidate**. Grade-1 locking requires independent proof check and human-lead signature (B.9.2).

### C-B01-P-01 — Action-Port Non-Identifiability under State-Revealing Privileged Leakage

| Field | Content |
|---|---|
| **Premises** | (P1) A critic $F(x, p, a, z)$ is trained by any loss whose population minimizer is $\mathbb E[T_t \mid x, p, a, z]$ (MSE regression, FB measure loss with $\Sigma_B$ invertible), on replay generated by a behavior policy $\mu$. (P2) $p_t = (p^c_t, y_t)$ with $y_t = Y(Z_t, a_t, \omega)$, $\omega \perp a_t \mid Z_t$. (P3, state-revealing) $s_{t+1}$ is a measurable function of $(x_t, p^c_t, y_t)$ on a set $S$ of transitions of positive measure. (P4) The actor's gradient is $\partial_a F$ evaluated on stored $p_t$. |
| **Conclusion shape** | **Impossibility.** On $S$, no population-optimal critic has an identified, non-zero action-port derivative: $\partial_a F^\star = 0$ where the conditional support of $a_t$ has interior, and $\partial_a F^\star$ is unidentified by data otherwise. If $S$ has full measure, the leaky Bellman operator equals $\mathcal T^\mu$ and its fixed point is $z$-independent. |
| **Grade** | **Grade 1** (follows from conditional independence and the tower property; Theorem 2). |
| **Implementation independence** | Holds for any function class, optimizer, or critic architecture (MLP, transformer, kernel, tabular), and for classical fitted-Q or TD($\lambda$) regressors. |
| **Scope** | Off-policy actor-critic and FB training with privileged critic inputs. It does not cover on-policy methods that recompute $y$ for the evaluated action. |
| **Operational test** | Spike Gates G-1/G-3: on strata where Step 0 certifies (P3), arm L must show $\varepsilon$-degeneracy ($D \ge 4$, i.e. $\chi \le 0.2$) or sign-agreement collapse ($\mathrm{SA} \le 0.70$). |
| **Falsifier** | A converged leaky critic on a stratum certified state-revealing (Step 0: $s_{t+1}$ recoverable from $(x_t, p^c_t, y_t)$ with $R^2 \ge 0.99$ by a held-out regressor), with factual TD residual within 5% of its minimum, that nevertheless shows $\chi \ge 0.8$ and $\mathrm{SA} \ge 0.85$ against finite-difference ground truth. Such a counterexample would mean a premise fails, for example (P1) because a strong inductive bias dominates before convergence. It must be logged as a scope narrowing (B.9.6), not dismissed. |

### C-B01-P-02 — Bypass Conservation Invariant and Acausal Variance Accounting

| Field | Content |
|---|---|
| **Premises** | (P1)–(P2), $Y$ and $F^\star$ $C^1$ with dominated derivatives; $(x_t, p^c_t)$ sufficient for $Z_t$ (Proposition 1). |
| **Conclusion shape** | **Invariant.** (i) $\partial_a F^c = \mathbb E_\omega[\partial_a F^\star] + \mathbb E_\omega[\partial_y F^\star\,\partial_a Y]$: total action sensitivity is conserved and only redistributed by leakage. (ii) The TD residual increase under sanitization equals $\mathrm{AEV} \ge 0$, and no admissible input can recover it. |
| **Grade** | **Grade 1** (Lemma 1, Corollary of Proposition 1). |
| **Operational test** | Gate G-4: bypass-identity residual $\mathrm{BIR} = \|J^C_a - (J^L_a + J^L_{\mathrm{fut}} \hat Y_a)\|/\|J^C_a\| \le 0.30$ (finite-sample, finite-capacity tolerance). Gate G-6: EV drop from L to C is bounded by the separately estimated AEV. |
| **Falsifier** | $\mathrm{BIR} > 0.5$ with both critics within 5% of their own minimum TD residual, on states where $\hat Y_a$ is estimated with relative standard error $< 10\%$. This would indicate a missing pathway (e.g. a leak outside Groups 20–21 not caught by Step 0) or failure of the smoothness premise, such as contact discontinuities. Either way, the claim is narrowed to smooth strata. |

### C-B01-P-03 — Exogenous Schedule Phase Is an Obligatory Critic Input for E3/E4

| Field | Content |
|---|---|
| **Premises** | Disturbance schedules with pre-sampled phase (hold duration, release time) that is not measurable from the past window, and a discount horizon $1/(1-\gamma)$ longer than the residual phase. |
| **Conclusion shape** | **Functional role (lower bound).** Any causal privileged critic that achieves Bellman error below $\tfrac12 \|M(Z) - M(Z')\|$ on phase-aliased pairs must realize schedule-phase estimation from $\xi_t$ (Lemma 3). |
| **Grade** | **Grade 2** candidate. The lower bound itself is Grade 1, but whether V3's E3/E4 schedules actually satisfy the premises depends on B02's schedule design, so the role is structural rather than unconditional. |
| **Operational realization test** | (i) A linear probe on $F$'s 512-D compressor output recovers the E4 release countdown with MAE $\le 1$ control step. (ii) **Intervention:** permuting Group 18 timers across E4 states changes $F$'s TD residual on those states by $\ge 10\%$ (Gate G-7). |
| **Falsifier** | Arm Z (no Groups 18–21) or arm C−ξ (timers and $\Psi$ zeroed) matching arm C's E3/E4 factual and counterfactual TD residual within 5%. If B02 adopts state-triggered release, the premise fails by construction, and the role transfers to "trigger rule + causal progress counter" (Section 1.3). |

---

## 5. Pre-Registered Empirical Spike Protocol

### 5.1 Compute Environment Statement

The drafting host has **no CUDA device** (`nvidia-smi` absent) and **no PyTorch installation**. The protocol is therefore written to be device-agnostic (`device = "cuda" if torch.cuda.is_available() else "cpu"`). Tier S is budgeted to run on CPU; Tier V uses CUDA when available, with a documented reduced-update CPU fallback. The runner must record `torch.__version__`, device, thread count, and determinism flags in the spike ledger. Per §12.2, execution is the experiment runner's role; this author does not execute.

### 5.2 Step 0 — Bitwise Action-Invariance Audit (BAIA) and Manifest Reconciliation

1. Dump the V3 schema manifest and map every one of the 5,065 slots to a group and a field name. Reconcile with the nominal widths of Section 1.4, and record any discrepancy.
2. Draw $N_0 = 4{,}096$ snapshots stratified over E0–E4 × 144 configurations (≥ 5 per cell where reachable; Issue 3's 720-cell matrix is the sampling frame). For each snapshot:
   - Restore, then assemble $p_t$ with the **current** (leaky) collector under $a_t \in \{a^\beta_t, a^\beta_t \pm 0.25\}$ and, independently, under perturbed $a_{t+1:t+K-1}$, using common random numbers.
   - A field is **action-variant** if any bit differs across the perturbations.
   - Test **exogeneity**: $\xi_{t+1}$ must be bitwise invariant to $a_t$ for all generator modes.
   - Test **state-revealing**: fit a held-out ridge/MLP regressor $s_{t+1} \leftarrow (x_t, p^c_t, y_t)$ and record $R^2$ per stratum. This certifies premise (P3) of C-B01-P-01 per stratum.
3. **Output:** a per-field leak map (the empirical version of the Section 1.4 table). **Gate G-0:** arm C's constructor must show 0 action-variant fields on all snapshots, and $\xi_{t+1}$ must be invariant. Failure blocks all later gates.

### 5.3 Arms

All arms keep the exact V3 $F$ architecture (input `5,219`, `2,805,008` params), the same initialization, and the same seeded batch stream.

| Arm | $p$ fed to $F$ | Purpose |
|---|---|---|
| **L** | Current leaky $p_{5065}$ | Baseline leak |
| **C** | $p^{\mathrm{causal}}_{5065}$ (Section 1.5) | Proposed sanitization |
| **L-sg** | L with `detach()` on Groups 20–21 | Tests Alternative A (Lemma 2) |
| **Z** | C with Groups 18–21 zeroed (EMA-only) | Tests Alternative B (Lemma 3) |
| **C−ξ** | C with Group 18 timers and Group 20 $\Psi$ zeroed | C-B01-P-03 intervention |
| **X** | C with G20 = realized window only for state-independent modes | Alternative C diagnostic (ungated) |

### 5.4 Two Tiers

- **Tier S (synthetic, CPU, controllable ground truth).** A PyTorch single-joint plant
  $J\ddot q = S u - b\dot q - \tau_c \tanh(\dot q/\epsilon) - m g r_{\mathrm{com}}\cos q + \tau_{\mathrm{stop}}(q,\dot q) + \tau_{\mathrm{contact}} + \tau_{\mathrm{ext}}$,
  4 semi-implicit substeps of 5 ms, with spring-damper stops and obstacles. It spans 12 configurations: 3 capacity tiers $C_0 \in \{3, 6, 9\}$ × 2 link lengths × 2 stroke profiles. The E0–E4 generators cover all five profile families, both sign modes, and both application modes. The $p_{5065}$ tensor is laid out in the V3 22-group slot order; channels the toy plant lacks are zero-filled identically in all arms. Behavior $\mu$ = `rule_calibration` (`baseline/02` §5.1) with Gaussian exploration ($\sigma = 0.15$) mixed `1/3 : 2/3` with a random-init frozen actor, mirroring the replay split. Budget: batch 256, 10,000 updates per run, about 0.1 s/update on CPU (estimate), 5 seeds for L/C and 3 for the other arms (22 runs, ~6 CPU-hours, parallelizable).
- **Tier V (V3 pipeline).** Uses the V3 replay buffer (`98,304` transitions) and simulator snapshot/restore (bitwise resume is verified, `resume_diff_norm = 0.0`). Settings: 20,000 updates with CUDA, or 5,000 on CPU (fallback documented); 5 seeds for L/C, 3 for the rest.

In both tiers, **$B_\omega$ and $\pi_\theta$ are frozen** (Tier V: the 101-update checkpoint; Tier S: a random-init $B$ orthonormalized to $\|\Sigma_B - I\|_F \le 0.1$). This makes the spike pure policy evaluation of $F$, so all arms share identical targets up to their own bootstrap. Report $\|\Sigma_B - I\|_F$; if $> 0.1$, use the full measure-loss form for residuals.

### 5.5 Measurements

Use a held-out set $\mathcal H$ of 512 states per regime (2,560 total), with 8 latents per state: 4 from $\mathcal U(\mathcal S^{15}(4))$ and 4 from $z = \operatorname{proj}(B_\omega(g^{\mathrm{des}}))$ with static holding targets $\dot q^\star = 0$, $\widehat{\ddot q}{}^\star = 0$. All quantities are measured in normalized input units.

| Symbol | Definition |
|---|---|
| $j_a$ | $\partial (F^\top z)/\partial a$ (scalar, actor-relevant) and $\|\partial F/\partial a\|_2$ (16-vector) |
| $\|J_{\mathrm{fut}}\|_2$ | spectral norm of $\partial F/\partial p_{G20 \cup G21} \in \mathbb R^{16\times 560}$ |
| $\hat Y_a$ | simulator sensitivity $(p^L_{\mathrm{fut}}(a{+}\delta) - p^L_{\mathrm{fut}}(a{-}\delta))/2\delta$, $\delta = 0.05$, snapshot-restore with CRN |
| $q'_{\mathrm{FD}}$ | ground-truth action slope: $(\hat Q_z(a{+}0.1) - \hat Q_z(a{-}0.1))/0.2$, with $\hat Q_z = \sum_k \gamma^k B_\omega(g_{t+k+1})^\top z$ over 16 CRN rollouts under $\pi_z$, horizon 150 steps (Tier S: all of $\mathcal H$; Tier V: 256 states) |
| $\chi$ | median over $\mathcal H$ of $\lvert j_a^L\rvert / \lvert j_a^C\rvert$ |
| $D$ | $\|J^L_{\mathrm{fut}}\|_2 \|\hat Y_a\|_2 / \|J^L_a\|_2$ (Corollary 1) |
| SA | sign agreement $P[\operatorname{sign}(j_a) = \operatorname{sign}(q'_{\mathrm{FD}})]$ on states with $\lvert q'_{\mathrm{FD}}\rvert > 2\,\mathrm{SE}$ |
| BIR | $\|J^C_a - (J^L_a + J^L_{\mathrm{fut}}\hat Y_a)\|_2 / \|J^C_a\|_2$ on states with $\|J^C_a\|$ above its 20th percentile |
| $\delta_f$ | factual TD residual $\mathbb E\|F(u_t) - B(g_{t+1}) - \gamma\bar F(u_{t+1})\|^2$ |
| $\delta_{cf}$ | counterfactual TD residual: $a' = \operatorname{clip}(a^\beta + \mathcal U[-0.3, 0.3])$, re-simulate $s'$, $g'$ from snapshot; arms L/L-sg are fed the **stale** $p_t$ (as at actor time), arm C the (invariant) $p^{\mathrm{causal}}_t$ |
| $R_{cf}$ | $\delta_{cf}/\delta_f$ |
| EV | TD-target explained variance per regime |
| Probes | linear probe on the 512-D compressor output: E0–E4 balanced accuracy; E4 release-countdown MAE (control steps) |
| $z$-sens | $\mathbb E_{z,z'}\|F(u;z) - F(u;z')\|/\|F\|$ (detects $z$-collapse, Theorem 2d) |

### 5.6 PyTorch Measurement Core

```python
import torch
from torch.func import jacrev, vmap

FUT_IDX = slice(G20_START, G21_END)  # 560 slots from the reconciled manifest

def critic_jacobians(F, x, p, a, z, chunk=128):
    """x:[N,137] p:[N,5065] a:[N,1] z:[N,16], all normalized; F returns [N,16]."""
    def f1(x1, p1, a1, z1):
        return F(x1[None], p1[None], a1[None], z1[None])[0]
    out = []
    for s in range(0, x.shape[0], chunk):
        sl = slice(s, s + chunk)
        J_p, J_a = vmap(jacrev(f1, argnums=(1, 2)))(x[sl], p[sl], a[sl], z[sl])
        J_a = J_a.squeeze(-1)                                   # [n,16]
        J_fut = J_p[:, :, FUT_IDX]                              # [n,16,560]
        out.append(dict(
            ja_z=(J_a * z[sl]).sum(-1),                         # d(F^T z)/da
            ja_norm=J_a.norm(dim=-1),
            jfut_spec=torch.linalg.matrix_norm(J_fut, ord=2),
            J_a=J_a, J_fut=J_fut))
    return {k: torch.cat([o[k] for o in out]) for k in out[0]}

@torch.no_grad()
def window_sensitivity(env, snaps, a, build_p_leaky, delta=0.05):
    """Finite-difference dp_fut/da_t with common random numbers."""
    rows = []
    for snap, a0 in zip(snaps, a):
        env.restore(snap); p_plus = build_p_leaky(env, a0 + delta)
        env.restore(snap); p_minus = build_p_leaky(env, a0 - delta)
        rows.append((p_plus[FUT_IDX] - p_minus[FUT_IDX]) / (2 * delta))
    return torch.stack(rows)                                    # [N,560]

def bypass_identity_residual(jl, jc, Y_a):
    bypass = torch.einsum("nij,nj->ni", jl["J_fut"], Y_a)       # J_fut @ Y_a
    return (jc["J_a"] - (jl["J_a"] + bypass)).norm(dim=-1) / jc["J_a"].norm(dim=-1)

def degeneracy_D(jl, Y_a):
    return jl["jfut_spec"] * Y_a.norm(dim=-1) / jl["ja_norm"].clamp_min(1e-12)
```

Determinism: `torch.use_deterministic_algorithms(True)`, fixed seeds per (arm, seed), identical batch index streams across arms, float32 throughout, float64 for the finite-difference simulator sensitivities.

### 5.7 Pre-Registered Gates

Statistics: per-seed medians over $\mathcal H$ (or the stated stratum), aggregated across seeds with a 95% bootstrap CI. A gate **passes** only if the conservative CI bound clears the threshold. Strata "E1–E3" means E1 ∪ E2 ∪ E3.

| Gate | Quantity | Threshold | Tests |
|---|---|---|---|
| **G-0** | BAIA on arm C | 0 action-variant fields; $\xi_{t+1}$ invariant | Construction validity (blocking) |
| **G-1** | Leak materiality, arm L, E1–E3 | $D \ge 4$ **or** $\mathrm{SA}_L \le 0.70$ | C-B01-P-01 applicability |
| **G-2** | Restoration, arm C | $\mathrm{SA}_C \ge 0.85$ overall and $\ge 0.80$ in each of E0–E4; median $\lvert j^C_a\rvert/\lvert q'_{\mathrm{FD}}\rvert \in [0.5, 2.0]$ | Sanitized action port is causal |
| **G-3** | Retention, E1–E3 | $\chi \le 0.5$ (predicted; conditional on G-1) | Theorem 2 / Proposition 2 |
| **G-4** | Bypass identity | median BIR $\le 0.30$ | C-B01-P-02 mechanism |
| **G-5** | Bellman residuals | $R_{cf}^{C} \le 1.25$ in every regime; $R_{cf}^{L} \ge 1.5$ in E1–E3; $\delta_{cf}^C < \delta_{cf}^L$ | Section 2.6 (1)–(2) |
| **G-6** | Disambiguation preserved | Arm C: E0–E4 probe balanced accuracy $\ge 0.98$; E4 countdown MAE $\le 1$ step; $\mathrm{EV}_C/\mathrm{EV}_L \ge 0.98$ on E0. Arm Z: countdown MAE $\ge 3$ steps **or** E3/E4 $\delta_{cf}^Z \ge 1.10\,\delta_{cf}^C$ | Proposition 1; rejection of Alternative B |
| **G-7** | Phase intervention | E4 $\delta_f^{C-\xi} \ge 1.10\,\delta_f^C$ **and** timer permutation raises arm C E4 residual by $\ge 10\%$ | C-B01-P-03 |
| **G-8** | Stop-gradient null | $\lvert\chi_{L\text{-}sg} - \chi_L\rvert$ and $\lvert\mathrm{SA}_{L\text{-}sg} - \mathrm{SA}_L\rvert$ inside the seed CI | Lemma 2 (Alternative A) |
| **G-9** | $z$-collapse | $z$-sens of arm L on E1–E3 $\le 0.5\times$ arm C (predicted, reported) | Theorem 2d |
| **H1 report** | $\mathrm{EV}_C/\mathrm{EV}_L$ overall and per regime, with $\widehat{\mathrm{AEV}}$ | Reported against 0.95; interpreted per Section 1.5 | Charter H1 |

### 5.8 Decision Rules

| Outcome | Interpretation | Action |
|---|---|---|
| G-0 fails | Sanitized constructor still action-dependent | Fix the collector ordering or preview function; rerun Step 0 only |
| G-0, G-2, G-5(C), G-6 pass; G-1, G-3 pass | Leak was material; sanitization restores the causal action port without losing disambiguation | Adopt $p^{\mathrm{causal}}$ for full V3 training; submit C-B01-P-01/02 for Grade-1 proof check |
| G-0, G-2, G-5(C), G-6 pass; G-1 fails | Leak immaterial at this training scale (premise P3 not met in practice, or not reached within the update budget) | Adopt $p^{\mathrm{causal}}$ anyway on Charter boundary 2 grounds (it is costless per G-6); log a scope narrowing for C-B01-P-01 |
| G-2 fails in some regime with G-0 passing | The causal critic is under-informed or under-trained in that regime | Inspect the probe gates: if G-6 fails, a disambiguating variable is missing from the table, so revise Section 1.4; if G-6 passes, it is a capacity or budget issue, not causality |
| G-4 fails with G-1 passing | An unaccounted leak pathway exists, or smoothness fails at contacts | Re-run BAIA on Groups 1–17; narrow C-B01-P-02 to smooth strata |
| G-8 fails | `detach` changed behavior, so $y$ is computed in-graph somewhere | File an implementation defect; Lemma 2's premise is violated, but the conclusion that stop-gradient does not remove conditioning bias is unaffected |
| G-6/G-7 fail for arm Z and C−ξ (they match C) | Schedule phase not Bellman-relevant under current schedules | Downgrade C-B01-P-03; re-test after B02 fixes the Issue 1 schedule |

Thresholds above are frozen at submission of this draft. Any change after data is seen must be filed as a method issue (§10.2) rather than applied silently.

---

## 6. Interfaces and Non-Goals

- **Deployment boundary.** Only $F_{\eta_1}, F_{\eta_2}$ inputs change. $B_\omega(g_{13})$ and $\pi_\theta(x_{137}, z_{16})$ (`281,617` params) are untouched, and the export check of `baseline/03` remains valid.
- **Parameter budget.** Unchanged (`5,891,633` total online), because sanitization preserves the 5,065-slot width.
- **Dependencies.** Section 1.3 creates a hard interface with B02. A state-triggered E3/E4 schedule changes the Group 18 content (trigger parameters + causal progress counter) and makes any future release time inadmissible. Issue 6 interacts with the masked-slot normalizer freeze.
- **Non-claims.** No statement here claims that the leak caused the `0` coverage counts or the `5.89–13.88 rad/s` holding RMSE. No statement relies on the 101-update smoke run as evidence of convergence (Charter boundary 4).
