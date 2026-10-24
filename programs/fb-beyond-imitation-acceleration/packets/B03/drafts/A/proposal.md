# Proposal A (Packet B03): Hierarchical Task Coupling Under Partial Observability and Contact Dynamics

- **Author**: Primary Author A. **Inputs**: Charter §2–§4; `D-B01-001`; baselines 02/04/05; `B03-SPIKE/VERDICT.json`.
- **Scope statement (Charter §2.5)**: every result below is either deductive (marked *Prop.*) or a pre-registered test. Nothing here claims that traversal or striking has been learned.
- **Thesis**: Aliasing in the *current* frame $B(m_t)$ does not matter for control. What matters is whether two contact intents produce different *future kinematic occupancy*. That gives three cases: **R** (geometry-resolved: fixed by $o_{\mathrm{low}}$ inside $\pi_\theta$ and $F$), **K** (kinematically distinguishable: fixed by the planner's choice of $z$), and **I** (isokinematic: no channel built on $B$ can fix it). Only Case I is an irreducible bottleneck. Its exact boundary is a rank condition on the contact Jacobian.

---

## 1. Formal Information-Theoretic and Observability Analysis of Kinematic-Only B(m)

**Setup.** Write the full simulator state as $s=(\xi,\varsigma,\lambda)$. Here $\xi$ is robot kinematics (floating base $\in SE(3)$, $q,\dot q\in\mathbb{R}^{29}$, base twist), $\varsigma$ is the exogenous scene (box height $h$, the box pose relative to the robot, ball state), and $\lambda$ is the active contact set with its wrenches. The descriptor is $m=\Phi_D(\xi)$. Let $G_D$ be the group of world transformations that $\Phi_D$ ignores:
- $D=229$ (`m[229]`: $v_H,\omega_H,g,q,\dot q$, 18 heading-frame link poses): $G_{229}=\{(x,y,z,\psi)\}$. This covers planar translation, **vertical translation** and yaw, because `m[229]` contains no base-height channel.
- $D=277$: $G_{277}=\{(x,y,\psi)\}$, because `base_height[1]` pins the vertical offset. Baseline 04 uses flat ground, so in this case the aliasing runs over $\varsigma_{\mathrm{ball}}$ and $\lambda$ rather than over the support height.

**Prop. 1.1 (exact aliasing fibre).** Take any weights $\omega$ and normalizer statistics in `eval` mode (frozen running mean and std, LayerNorm being per-sample). If $\xi'=g\cdot\xi$ for some $g\in G_D$, then $\Phi_D(\xi')=\Phi_D(\xi)$, and therefore $B_\omega(\Phi_D(\xi'))=B_\omega(\Phi_D(\xi))$ exactly. The fibre $\mathcal{A}(m)=\Phi_D^{-1}(m)\times\{\text{all }\varsigma,\lambda\}$ is therefore collapsed to one point in $B$-space.
*Proof.* $B_\omega\circ\Phi_D$ is a deterministic composition, and every argument it reads is $G_D$-invariant. $\square$

**Corollary 1.2 (three-regime construction, $D=229$).** Fix one posture $\xi^\star$ whose lowest foot sole is $\Delta_f$ below the root. Build three scenes:
- (F) free flight: root at world height $z_r>\Delta_f+0.70$, $\lambda=\varnothing$.
- (S) compliant support on the 0.40 m box: $z_r=0.40+\Delta_f$, sole on the top face, $\lambda_S\neq0$.
- (I) rigid impact on the 0.60 m box: same posture, translated so the shin touches the front face $x_{\mathrm{front}}$, giving an impulsive $\lambda_I$.

All three differ only by an element of $G_{229}$ plus a change in $(\varsigma,\lambda)$. So $\|B(m_F)-B(m_S)\|=\|B(m_S)-B(m_I)\|=0$, with zero tolerance in FP64. In FP32 this holds when the rows share a forward call and deterministic algorithms are enabled; batched-GEMM reordering can otherwise produce differences around $10^{-7}$. The run's `VERDICT.json` reports `b_space_kinematic_aliasing_max_diff = 0.0`, which matches this result but is not independent evidence for it.

**Edge case.** In `train` mode, batch statistics make $B$ depend on what else is in the batch. Prop. 1.1 is stated for the frozen-BN encoding used at Sites (i) and (ii) of `D-B01-001`.

**Prop. 1.3 (information bound).** Let $C$ be the contact regime. Because $C\to\Xi\to M\to Z=B(M)$ is a Markov chain:
- $I(C;Z\mid M)=0$ and $I(C;Z)\le I(C;M)$.
- Any decoder $\hat c(z)$ has error at least $P_{\mathrm{err}}\ge\mathbb{E}_m[1-\max_c p(c\mid m)]$.
- On the fibres of Cor. 1.2 with regimes equiprobable, $P_{\mathrm{err}}\ge 2/3$.

$B$ can therefore act only as a *statistical* proxy for contact (some postures are correlated with contact in replay). It can never separate states within a fibre.

**Single-frame vs. occupancy aliasing.** Contact changes $\ddot q$, so it changes $m_{t+1}$, even though it does not change $m_t$. The FB value $F(o,a,z)^\top z=\Psi(o,a,z)^\top\Sigma_B^{-1}z-h^\top\Sigma_B^{-1}z$ (`D-B01-001` §1.1) is computed over *future* frames. Hence an intent is $z$-addressable iff its occupancy $\Psi$ differs, not iff $B(m_t)$ differs.

### 1.1 Three-case resolution theorem

Split $o_{\mathrm{low}}=(\xi_p,e)$, where $\xi_p$ is proprioception plus `last_action` and $e$ is exteroception (`scan[S]`, `scan_valid[S]`, `goal_dir[2]`; or `ball_state[9]`, `kick_leg[2]`). Let $a^\star(s,c)$ be the action that is task-optimal under contact intent $c$.

**Prop. 1.4.** A deterministic $\pi_\theta$ can realize $a^\star$ iff $a^\star$ is $\sigma(o_{\mathrm{low}},z)$-measurable. Three cases exhaust the possibilities:
- **Case R (geometry-resolved).** $c=\kappa(\xi_p,e)$, i.e. posture plus local geometry fix the regime. Example: Cor. 1.2, where the scan under the sole reads $0.40$ (S), the front face sits at the shin (I), or the ground is $\gg\Delta_f$ away (F).
  - *Necessary and sufficient*: $e$ is an input to **both** $\pi_\theta$ and $F$, and $\kappa$ is measurable at the scan's resolution.
  - Why $F$ also needs $e$: if $F$ lacked it, $\nabla_aF^\top z$ would be the regime-mixture gradient $\sum_cp(c\mid\xi_p)\nabla_aF_c^\top z$, which is biased toward the majority regime.
  - Failure mode: if the scan spacing $\delta_s$ exceeds the contact-feature size (e.g. the front-edge offset $<\delta_s$), $\kappa$ is not measurable and aliasing reappears *at the perception level*. Baseline 04 has no history in $\pi_\theta$, so contact onset must also be inferable from $(\dot q,a_{t-1})$.
- **Case K (kinematically distinguishable intent).** Here $(\xi,e)$ is the same but $c\in\{c_1,c_2\}$ with $\Delta_K:=\|\Sigma_B^{-1/2}(\Psi^{c_1}-\Psi^{c_2})\|>0$. Example: hand push-off vs. swing-over at the same pre-contact posture on the same box, where the torso trajectories differ.
  - The intent is carried by $z$. Command $z_i\propto\Sigma_B^{-1/2}$-aligned with $\Psi^{c_i}$: $z_1$ prefers $c_1$ by a margin $\ge\Delta_K^2/(2\sqrt{d_z})$ once $h$ is small.
  - The planner can select this because it sees $H_t$; $B(m_t)$ is not involved.
- **Case I (isokinematic multi-force).** Here $(\xi_\tau)_{\tau\ge t}$ is identical under $c_1,c_2$ but the wrenches differ. Then $\Psi^{c_1}=\Psi^{c_2}$, so $F^\top z$ is identical **for every $z$**. FB training gives $\theta$ no gradient along the force difference.

**Prop. 1.5 (exact boundary of Case I).** Floating-base dynamics give $M\ddot q+b=S^\top\tau+J_c^\top\lambda$ with $S^\top\in\mathbb{R}^{35\times29}$ and $J_c^\top\in\mathbb{R}^{35\times n_c}$. For fixed kinematics $(q,\dot q,\ddot q)$, the admissible $(\tau,\lambda)$ form an affine set of dimension
$$\dim\mathcal{N}=29+n_c-\operatorname{rank}[S^\top\ J_c^\top]\ \ge\ n_c-6,$$
intersected with the friction cones. When the contact is sticking and the intersection has nonempty relative interior, every point of it is **exactly isokinematic** for all future time.
- Flight ($n_c=0$) and single-foot support ($n_c=6$, full-rank base block): $\dim\mathcal{N}=0$, so Case I is empty.
- Double support ($n_c=12$): $\ge6$. Feet plus one hand point contact ($n_c=15$): $\ge9$.

Joint-PD actuation $\tau=K_p(a-q)-K_d\dot q$ is a bijection between $\tau$ and $a$, so distinct internal forces need distinct actions, with $\Delta a=K_p^{-1}\Delta\tau\neq0$. For a binary intent with prior $p$, every deterministic $\pi(o_{\mathrm{low}},z)$ incurs the Bayes floor
$$\mathbb{E}\|\pi-a^\star\|^2\ \ge\ p(1-p)\|K_p^{-1}\Delta\tau\|^2.$$

**Ball striking is $\varepsilon$-isokinematic.** Changing kick-leg impedance at impact changes the effective mass $m_{\mathrm{eff}}$, and $v_{\mathrm{out}}=(1+e_r)\frac{m_{\mathrm{eff}}}{m_{\mathrm{eff}}+m_b}v_{\mathrm{foot}}$. The robot's own kinematic deviation is $O(m_b/m_{\mathrm{eff}})$, so the FB value gap is $\le\varepsilon\|\Sigma_B^{-1}z\|$ while the task gap is $O(1)$. The bottleneck ratio $\rho=\Delta Q_{\mathrm{task}}/\Delta(F^\top z)$ diverges as $\varepsilon\to0$.

---

## 2. Comparative Architecture Analysis: Macro-Step Latent Value vs Action-Level Task Value

**Design 1 (R2.1 traversal).** $z_t=P_\psi(h_t)$ is held for $k\le K=10$ steps. The return is $R_{\mathrm{macro}}=\sum_{j<k}\gamma_{\mathrm{task}}^jr_{t+j}$ and the target is
$$y^{(1)}=R_{\mathrm{macro}}+\gamma_{\mathrm{task}}^k(1-d)\min_i Q_{\bar\phi_i}(h_{t+k},c^{\mathrm{geom}}_{t+k},P_{\bar\psi}(h_{t+k})).$$
The critic trains on $z_{\mathrm{actual}}$, and the planner gradient is $(\partial_\psi P)^\top\nabla_zQ_\phi$.
- Truncation $k<K$ (termination, `severe_penetration` with $\Phi_{\mathrm{next}}=0$, or timeout) uses $\gamma^k$ with the true $k$.
- `invalid` rows never enter `TaskReplay`.

**Design 2 (v2 striking).** $K_{\mathrm{hold}}=1$ and $z_t=P_\psi(o_{\mathrm{task}})$. The target is $y^{(2)}=r_t+\gamma(1-d)\min_kQ_{\bar\phi_k}(H',\pi_{\bar\theta}(o',P_{\bar\psi}(H'))+\epsilon)$, and the planner gradient is
$$\nabla_\psi Q_\phi\bigl(o_{\mathrm{task}},\pi_\theta(o_{\mathrm{low}},P_\psi(o_{\mathrm{task}}))\bigr)=(\partial_\psi P)^\top\,(J_z\pi_\theta)^\top\,\nabla_aQ_\phi,$$
with $\theta$ frozen inside this loss.

**Prop. 2.1 (unification).** Define the induced macro critic $Q^{\pi,K}(h,z):=\mathbb{E}^{\pi_\theta(\cdot,z)}[\sum_{j<k}\gamma^jr_{t+j}+\gamma^kV(h_{t+k})]$. For deterministic $\pi_\theta$ and $K=1$, $Q^{\pi,1}(h,z)=Q^{\mathrm{act}}(h,\pi_\theta(o,z))$. **Design 2 is therefore Design 1 at $K=1$, with the critic factored through the action.** The two designs differ along three axes:

| Axis | Design 1 $Q(h,z)$ | Design 2 $Q(h,a)$ |
|---|---|---|
| $\theta$-drift of critic semantics | $\partial_\theta Q^{\pi,K}\neq0$: a stale $z\mapsto$ behaviour map, bounded by the 50k window | $Q^{\mathrm{act}}$ is $\theta$-invariant at step $t$; drift enters only through the bootstrap via $\bar\theta$ |
| Credit horizon | $K$ steps per backup, suited to the 0.2 s traversal phases | 1 step, suited to the 5-step impact window |
| Case-I visibility | Blind: $z\mapsto a$ is FB-trained, so it is indifferent on $\mathcal{N}$ | Sees $a$, so it can value $\Delta a\in K_p^{-1}\mathcal{N}_\tau$ |

**Prop. 2.2 (shared reachable-set bottleneck).** In both designs the first-step actions the planner can reach form $\mathcal{A}(o)=\pi_\theta(o,\mathcal{S}^{d_z-1}(\sqrt{d_z}))$, a manifold of dimension at most $d_z-1$.
- Let $n_a$ be a Case-I direction. $\mathcal{L}_\pi$ carries no signal along $n_a$, so the extent of $\mathcal{A}(o)$ along $n_a$ is set by initialization and incidental generalization, not by the task. Formally, $\langle\nabla_\theta\mathcal{L}_\pi,\ \partial_\theta\pi\cdot n_a\rangle$ has zero population mean.
- If $\langle a^\star-\pi(o,z),n_a\rangle$ is bounded away from $0$ on $\mathcal{A}(o)$, **no planner, in either design, reaches $a^\star$.**
- The only legal channel that injects task signal along $n_a$ is the Charter's *optional task-critic gradient in single-step action-$Q$ variants*: $\mathcal{L}_\pi + \beta\,(-Q_{\phi_1}(H,\pi_\theta(o,z_{\mathrm{actual}})))$. Design 2 admits it; Design 1 does not.

**Bridge rule (Action-Anchored Macro Critic, AAMC).**
- Critic input: $Q_\phi(h_t,c^{\mathrm{geom}}_t,z,\alpha)$, where $\alpha$ is the macro's first action.
  - TD training uses the logged $\alpha=a^{(0)}_{\mathrm{applied}}$ (a new immutable `TaskReplay` field; `behavior_z` is untouched).
  - The planner loss uses $\alpha=\pi_\theta(o_t,P_\psi(h_t))$ with $\theta$ frozen.
  - The target uses $\alpha'=\pi_{\bar\theta}(o_{t+k},z'),\ z'=P_{\bar\psi}(h_{t+k})$.
- At $K=1$, AAMC reduces to Design 2. At $K>1$ it keeps macro credit and adds a $\theta$-drift anchor: $\alpha$ fingerprints what $z$ currently means.
- **Switching criterion.** Let $\tau_{\mathrm{dec}}$ be the decisive interval, estimated from the replay autocorrelation of $\partial r/\partial a$.
  - $\tau_{\mathrm{dec}}\le 3$ steps (impact): use $K=1$ and enable $\beta>0$.
  - $\tau_{\mathrm{dec}}\ge K$ (traversal phases): use $K=10$, $\beta=0$.
  - In traversal, Case K covers push-off vs. swing-over. Case I there (hand/foot load sharing) matters only through slip or penetration, which shows up kinematically or as termination and is therefore credited by $Q$.
- **No-leakage contract.**
  - $B_\omega$ input stays `m[229|277]`.
  - $c^{\mathrm{geom}}$ goes only to $Q$; `scan` and `ball_state` go only to $\pi,F,P,Q$.
  - $\mathcal{L}_{\mathrm{plan}}$ has stop-grad on $\theta,\eta,\omega$. $\mathcal{L}_Q$ updates only $\phi$. The $\beta$-term updates only $\theta$, never $\omega$ or $\eta$.
  - Expert and near prompts remain $\operatorname{proj}(B_\omega(m_{\mathrm{demo}}))$.
  - Each module's history is rebuilt by the zero-hidden full-prefix burn-in (baseline 04 §4.3).

---

## 3. Serious Alternative Considered and Rejected

**Alternative (method v1.0 §11.5).** Contact- and scene-augmented backward map $B'_\omega(m,c)$, where $c\in\{\lambda,\ \text{scan},\ h,\ \text{ball\_state}\}$.

**Prop. 3.1 (prompt-side impossibility).** Suppose $B'$ depends on $c$ nontrivially. Demonstration NPZs contain only `qpos`/FK and therefore have no $c_{\mathrm{demo}}$. Any demo-compatible prompt is then $z_{\mathrm{exp}}=B'(m_{\mathrm{demo}},\bar c(m_{\mathrm{demo}}))$ for some imputation rule $\bar c$. But $B''(m):=B'(m,\bar c(m))$ is a function of $m$ alone, so it has exactly the fibres of Prop. 1.1.
- **The augmentation adds zero information on the prompt side.**
- It also adds an off-support risk: if $\bar c$ is a fill value that never appears in replay, the prompt leverage $B'^\top W_tB'/d_z$ (`D-B01-001` §2.2) is uncontrolled. Marginalizing instead requires $p(c\mid m)$, which cannot be estimated from kinematic-only demos.
- This violates Brief §2 and Charter §2.3. $\square$

**Prop. 3.2 (exogenous-rank waste and unreachable relabels).** Let $h$ be constant per episode and independent of actions, and take any direction $u$ with $u^\top B'(m,h)=f(h)$.
- Then $F^\top u=f(h)/(1-\gamma_{\mathrm{FB}})$ regardless of the action, so $\nabla_aF^\top u=0$. Those $\Sigma_B$ eigendirections cost capacity in $d_z$ while carrying zero control signal. Under $\mathcal{L}_{\mathrm{orth}}$ they also compete with controllable directions for $\operatorname{tr}\Sigma_B=d_z$.
- Under the 50% permuted-goal relabel of Charter §2.2, the relabelled goal has the wrong $h$ with probability $1-\sum_hp(h)^2$. With uniform sampling over the 7-height bank that is $6/7\approx85.7\%$: most goal relabels become unreachable along $u$.
- `ball_state` is controllable after impact, so this argument is weaker for the ball. Prop. 3.1 still rules it out.

**Secondary alternative: an end-to-end monolithic task RL actor $\pi(o,\cdot)$.** This removes $z$, so `expert`/`near` seeding, phase-free stitching (baseline 02 §3.2) and the H4 schedule all disappear. It is exactly compute-matched baseline (a)/(d) of baseline 02 §6.4. As a null baseline it is kept; as an architecture it is rejected because it is not a resolution of B03.

**Rejected as well: contact-flag channels in $m$.** Even an observable binary flag fails. Demo flags derived from FK foot height are unreliable on the 0.704 m box (Prop. 3.1 again), and the flag cannot address Case I, where the contact set is the same and only the wrench varies.

---

## 4. Candidate Necessity Claims (Appendix B)

**C-B03-A-01 — Isokinematic blindness of FB-only channels (Grade 1, deductive).**
- *Premises.*
  - (P1) $B$ reads only $m=\Phi_D(\xi)$.
  - (P2) $\theta$ is updated only by $\mathcal{L}_\pi=-\min_k F_k^\top z$.
  - (P3) Some task-relevant state has a sticking contact set with $\dim\mathcal{N}>0$ (Prop. 1.5, e.g. $n_c>6$ with a full-rank base block).
  - (P4) The task-optimal internal force differs across episodes that share $(o_{\mathrm{low}},\text{scene})$.
- *Conclusion.* $\mathbb{E}[\nabla_\theta\mathcal{L}_\pi]$ has no component that orders actions along $K_p^{-1}\mathcal{N}_\tau$, and every deterministic $\pi(o_{\mathrm{low}},z)$ incurs the Bayes floor of Prop. 1.5. **It is necessary** that either (i) some module input outside $B$ makes the intent $\sigma(o_{\mathrm{low}})$-measurable, or (ii) an action-level task gradient (Design 2 / AAMC with $\beta>0$) reaches $\theta$. The planner choice of $z$ alone is insufficient (Prop. 2.2).
- *Operational test.* Spike (c) and (d) below.
- *Falsifier.* Either of the following refutes the claim:
  - A pure-FB actor ($\beta=0$) achieves a state-conditional action variance along $n_a$ that tracks the internal-force label, with probe MSE $\le0.5\times$ floor, without $c$ in any input.
  - An FB value gap $|F^\top z(a_1)-F^\top z(a_2)|>10^{-3}|F^\top z|$ appears on exactly isokinematic branches.

**C-B03-A-02 — Perceptive sufficiency for geometry-resolved aliasing (Grade 2, empirical).**
- *Premises.* Case R holds (Prop. 1.4), $e$ goes to both $\pi_\theta$ and $F$, and the scan resolution is $\le$ the contact-feature size.
- *Conclusion.* Aliasing in $B$ over {flight, 0.40 support, 0.60 impact} costs no task performance relative to an oracle that additionally feeds $c$ to $\pi$ and $F$, never to $B$.
- *Test.* A 3-arm ablation (full / scan withheld from $F$ only / scan withheld from $\pi$ and $F$) on the ID and interpolation panels at 0.30–0.70 m. Each arm uses 5 seeds, matched compute, and the Wilson LB on success.
- *Falsifier.* Full-arm success falls more than 10 pp below the oracle with non-overlapping 95% intervals, **and** diagnostics $D_P$ and $D_F$ (§5) are both negative.

**C-B03-A-03 — Prompt-side impossibility (Grade 1).** Every demo-compatible encoder is $m$-measurable on demo prompts (Prop. 3.1). *Falsifier:* exhibiting a demo-NPZ-only encoder whose prompts separate any pair in a $G_D$-orbit.

---

## 5. Pre-Registered Empirical Spike Protocol

**Harness.** `spikes/B03-SPIKE-A/run.py`. Settings: PyTorch, CPU, `torch.use_deterministic_algorithms(True)`, FP64 for the identity checks, seeds $\{0,\dots,4\}$. Output goes to `VERDICT.json`, with every threshold below written to the file **before** the run.

**What this spike can and cannot show (Charter §2.5).** It establishes mechanism and contract only. All "probe" regressions are diagnostic heads detached from $\pi_\theta$'s training graph. They are **not** a BC loss on the system actor.

**Note on the existing VERDICT.** `irreducible_isokinematic_multi_force_mse = 0.895` cannot be interpreted without its analytic floor. This protocol always reports the probe MSE alongside $L^\star$.

**(a) Kinematic-only $B$ contact aliasing.**
- Generate $N=4096$ postures $\xi^\star$ (random $q$ within joint limits, random twist). For each, build F/S/I copies via $G_{229}$ (Cor. 1.2) and, for $D=277$, via ball-present/ball-absent copies with $G_{277}$.
- Encode with $B_\omega$: `[512,512,256]` LN+SiLU, spherical projection, $d_z\in\{256,100\}$. Use weights at random init and after 500 synthetic FB updates, with BN frozen.
- **Pass:** $\max\|B(m_F)-B(m_S)\|_\infty=\max\|B(m_S)-B(m_I)\|_\infty=0$ exactly.
- **Positive controls (the test must not be vacuous):**
  - A perturbation $q_1{+}10^{-3}$ gives separation $>10^{-8}$.
  - For $D=277$, a vertical translation changes `base_height`, so separation $>0$.
  - If either control is $0$, the result is VOID.

**(b) Perceptive disambiguation in $\pi_\theta(o_{\mathrm{low}},z)$.**
- Synthetic regime dynamics on a 35-DoF linearization: $a^\star_c=q+K_p^{-1}(\tau^\star_c+K_d\dot q)$, with $\tau^\star_c$ solving $S^\top\tau+J_c^\top\lambda_c=M\ddot q_c+b$ for $c\in\{F,S,I\}$. The scan is synthesized from the $G_D$ offset (S: top face at the sole; I: front face at the shin).
- Probe: MLP$(o_{\mathrm{low}},z{=}B(m))$, `[256,256]`, 3000 Adam steps.
- **Pass, both required:**
  - With scan: NMSE $\le0.01$.
  - Scan zeroed: NMSE $\ge0.9\,L^\star_{\mathrm{mix}}/\operatorname{Var}(a^\star)$, where $L^\star_{\mathrm{mix}}=\mathbb{E}_m\operatorname{tr}\operatorname{Cov}(a^\star\mid m)$ is computed in closed form.
- A third arm withholds scan from $F$ only, in a linear-FB toy on a 3-regime chain MDP. **Pass:** the cosine between $\nabla_aF^\top z$ and the regime-specific oracle gradient falls from $\ge0.95$ (full) to $\le\max_c p(c\mid\xi_p)+0.05$ (ablated).

**(c) Isokinematic multi-force lower bound.**
- Double-support-plus-hand contact. Compute $\mathcal{N}_\tau$ by SVD of $[S^\top\ J_c^\top]$.
  - **Gate:** the numerical rank deficiency must equal the predicted $\dim\mathcal{N}$. Expected values: 0 for flight, 0 for a single foot, $\ge6$ for double support, $\ge9$ for feet plus hand.
- Labels: $\Delta\tau=f\,n_\tau$, $n_\tau\in\mathcal{N}_\tau$ unit, $c\in\{\pm\}$, $p=\tfrac12$, kinematics identical. The analytic floor is $L^\star=\tfrac14\|K_p^{-1}\Delta\tau\|^2/29$ per dimension.
- **Pass, all required:**
  - Probe MSE $\in[0.95L^\star,1.05L^\star+\sigma^2_{\mathrm{noise}}]$.
  - Positive control: appending privileged $c$ gives MSE $\le0.01L^\star$. This shows the floor is informational, not a capacity limit.
  - FB indifference: in the linear-FB toy, $|F^\top z(a_+)-F^\top z(a_-)|\le10^{-6}|F^\top z|$ over 1000 $z\sim\mathcal{S}^{d_z-1}$.
- **$\varepsilon$-variant (striking).** Sweep $m_b/m_{\mathrm{eff}}\in\{10^{-3},10^{-2},10^{-1}\}$. **Pass:** $\rho$ is monotonically decreasing in $m_b/m_{\mathrm{eff}}$.

**(d) Failure-attribution diagnostics, carried forward to GPU runs (Brief deliverable 2).**
- $D_P$ (planner selection): the normalized gap $(\max_{z\in\mathrm{CEM}_{64\times8}}Q_1(h,c,z)-Q_1(h,c,P(h)))/|Q_1|$ on failed 0.30–0.70 m episodes. $D_P>0.1$ flags planner failure.
- $D_F$ (perception use): $\mathbb{E}|F^\top z(o)-F^\top z(o_{\mathrm{scan\text{-}shuffled}})|/\mathbb{E}|F^\top z|$. $D_F<0.02$ flags that $F$ ignores the scan.
- $D_B$ (missing features in $B$): for a failed state, take the counterfactual successful privileged wrench. If its $\mathcal{N}$-component carries $>50\%$ of $\|\Delta\tau\|$ and the regression from $(o_{\mathrm{low}},z)$ attains only $\ge0.8L^\star$, attribute the failure to Case I.
- The attribution order is $D_F\to D_P\to D_B$. A failure is labelled B-aliasing **only if** $D_F$ and $D_P$ are both negative.

**Overall verdict.** PASS iff (a), (b) and (c) pass on all 5 seeds and every positive control fires. Any VOID control makes the verdict INCONCLUSIVE, not PASS.
