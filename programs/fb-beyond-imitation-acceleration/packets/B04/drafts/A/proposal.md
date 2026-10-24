# Proposal A (Packet B04): Differentiable World-Model Rollouts vs. FB Long-Horizon Bootstrapping

- **Author**: Primary Author A. **Inherits**: `D-B01-001` (target-coordinate Gram tracker $W_t=(\widehat\Sigma_t+\ell_t I)^{-1}$, four-site whitening contract, leverage routing).
- **Arm labels**: this proposal uses the packet-assignment labels (A = 1-step FB, B = $n$-step real FB target, C = model $n$-step FB target, D = pathwise hybrid). They **supersede** the `baseline/03` §6 labels (single-task WM / multi-task WM / ...). §2.4 gives the mapping so adjudicators can compare.
- **Evidence status (Charter §2.5)**: everything below is derivation plus a pre-registered protocol. The existing `B04-SPIKE/VERDICT.json` is a CPU smoke test (3.5 s). I read it as a contract check, not evidence for H3. The reasons are in §5.0.

## 1. Exact Pathwise Policy Gradient Decomposition and Error Bounds

**Setting.** Deterministic true plant $s_{t+1}=f(s_t,a_t)$, deterministic actor $a_t=\pi_\theta(s_t,z)$, and per-step command reward $r_z(y)=B(y)^\top\Sigma_B^{-1}z$. Termination is a hazard with survival probability $p^\star(s,a)\in[0,1]$, and the alive weight is $c^\star_t=\prod_{j<t}p^\star(s_j,a_j)$. The objective is
$$J_\infty(\theta,z;s_0)=\textstyle\sum_{t\ge0}\gamma^t c^\star_t\, r_z(s_{t+1}),\qquad Q^\star(s,a)=r_z(f(s,a))+\gamma p^\star(s,a)V^\star(f(s,a)),\quad V^\star(s)=Q^\star(s,\pi_\theta(s,z)).$$
The reward on the transition into a terminal state counts, and the bootstrap is masked. This matches the FB diagonal pull-up on committed `severe_penetration` rows with $\Phi_{\mathrm{next}}=0$.

**Exact split at any horizon $H\ge0$.** Write $V^\star(s_0)=\sum_{t<H}\gamma^t c^\star_t r_z(s_{t+1})+\gamma^H c^\star_H V^\star(s_H)$ and differentiate. $\theta$ enters through every action $a_t$ and also through the explicit $\theta$ inside $V^\star(\cdot)$:
$$\nabla_\theta J_\infty=\underbrace{\sum_{t<H}\gamma^t D_\theta\pi_t^{\!\top}\, g^\star_t}_{T_{\mathrm{head}}(H)}\;+\;\gamma^H c^\star_H\underbrace{\sum_{k\ge0}\gamma^k\Big(\textstyle\prod_{i<k}p^\star_{H+i}\Big) D_\theta\pi_{H+k}^{\!\top}\nabla_aQ^\star(s_{H+k},a_{H+k})}_{T_{\mathrm{tail}}(H)\;=\;\partial_\theta V^\star(s)|_{s=s_H}\ \text{(DPG at }s_H)}$$
Here $D_\theta\pi_t=\partial_\theta\pi_\theta(s_t,z)\in\mathbb R^{d_a\times|\theta|}$, and $g^\star_t=\partial/\partial a_t\,[\sum_{k=t}^{H-1}\gamma^{k-t}c^\star_k r_z(s_{k+1})+\gamma^{H-t}c^\star_H V^\star(s_H)]$ is taken through the closed-loop sensitivities $\partial s_k/\partial a_t=\big(\prod_{i=t+1}^{k-1}A_i\big)\partial_af_t$, with $A_i=\partial_sf_i+\partial_af_i\,\partial_s\pi_i$.

**(a) Standard 1-step FB derivative ($H=0$).** $\hat g_A=D_\theta\pi_0^{\top}\nabla_a\min_kF_k(s_0,a,z)^\top z$. This keeps only the $k=0$ term of $T_{\mathrm{tail}}(0)$, so it drops every future Jacobian $D_\theta\pi_t$ with $t\ge1$:
$$\nabla J_\infty-\hat g_A=\underbrace{\textstyle\sum_{k\ge1}\gamma^k(\prod_{i<k}p^\star_i)D_\theta\pi_k^\top\nabla_aQ^\star_k}_{\text{per-state truncation},\ \|\cdot\|\le G_\pi Q'_a\gamma/(1-\gamma)}+\underbrace{D_\theta\pi_0^\top(\nabla_aQ^\star_0-\nabla_a\textstyle\min_kF_k^\top z)}_{\le G_\pi\epsilon_F^a}.$$
The first term is **not** a bias of the actor update *in population*. Averaged over $s_0\sim d^{\pi_z}_\gamma$ it is exactly a rescaling: $\mathbb E_{d^{\pi_z}_\gamma}[\hat g_A]=(1-\gamma)\nabla\mathbb E_{d_0}J_\infty$ (deterministic PG theorem). The real population bias of Arm A is therefore
$$\mathrm{bias}_A\le G_\pi\big[\epsilon_F^a+Q'_a\,\|\rho-d^{\pi_z}_\gamma\|_{\mathrm{TV}}/(1-\gamma)\big].$$
The mismatch term is never small for relabeled $z_{\mathrm{update}}$, because replay $\rho$ was produced by `behavior_z`$\ne z_{\mathrm{update}}$ (Charter §2.2). Consequence for evaluation: per-start-state cosine against $\nabla J_\infty(s_0)$ is the wrong yardstick for Arm A. §5 reports both the per-state and the occupancy-aggregated comparison.

**(b) Hybrid $H$-step estimator.** Model rollout $\hat s_{t+1}=\hat s_t+\sigma_\Delta W_\psi(\hat s_t,a_t)+\mu_\Delta$ with $\hat s_0=\mathrm{sg}(s_0)$. Motion features $\hat m_{t+1}=\kappa(\hat s_{t+1})$, where $\kappa$ is the deterministic root-relative kinematics map ($229$/$277$ dims). Soft survival $c_t=\prod_{j<t}\hat p_{\mathrm{surv}}(\hat s_j,a_j)$. Then
$$\hat J_H=\sum_{t=0}^{H-1}\gamma^t c_t\,\bar B(\hat m_{t+1})^\top W_t z+\gamma^Hc_H\min_k\bar F_k(\hat s_H,\pi_\theta(\hat s_H,z),z)^\top z,\qquad \hat g_D=\nabla_\theta\hat J_H .$$
$\hat g_D$ equals $T_{\mathrm{head}}(H)$ with every true quantity replaced by its model/critic surrogate, plus the $k=0$ term of $T_{\mathrm{tail}}(H)$ only. Population weighting of DPG terms over $\rho$: true $\sum_{t\ge0}\gamma^tP^t_\pi\rho$ versus hybrid $\sum_{t\le H}\gamma^t\hat P^t_\pi\rho$. The model therefore applies on-policy occupancy correction for exactly $H$ steps, and the residual mismatch shrinks only by the factor $\gamma^{H+1}$.

**Error budget.** Assumptions:
- Closed-loop Lipschitz constant $\|A_i\|\le L$, $\|\partial_af\|\le K_a$, $\|D_\theta\pi\|\le G_\pi$, $\|\nabla_s r_z\|\le R'$.
- Model Jacobian error $\|\hat A_i-A_i\|,\|\partial_a\hat f-\partial_af\|\le\epsilon_J^{\mathrm{eff}}(i)=\epsilon_J+\beta\|\hat s_i-s_i\|$, where $\beta$ is the Hessian-Lipschitz constant and $\|\hat s_i-s_i\|\le\epsilon_f\sum_{j<i}L^j$.
- Survival errors $|\hat p-p^\star|\le\epsilon_c$ and $\|\nabla\log\hat p-\nabla\log p^\star\|\le\epsilon_c'$.
- Critic errors $\|\nabla_a\bar F^\top z-\nabla_aQ^\star\|\le\epsilon_F^a$ and $\|\nabla_s[\bar F^\top z](s,\pi(s))-\nabla_sV^\star\|\le\epsilon_F^s$.
- Splice residual $\eta_W=\|\Sigma_B(W_t-\Sigma_B^{-1})\|$ (B01 §1.2.3). Write $u=\gamma L$.

Telescoping $\prod\hat A-\prod A$ gives $\|\partial\hat s_k/\partial a_t-\partial s_k/\partial a_t\|\le(k-t)\,\epsilon_J^{\mathrm{eff}}(L+\epsilon_J^{\mathrm{eff}})^{k-t-1}$, and therefore
$$\|\hat g_D-\nabla J_\infty\|\le\underbrace{G_\pi\epsilon_J R'\,S_1(H)}_{E_J}+\underbrace{G_\pi(\epsilon_c R_{\max}H+\epsilon_c'V_{\max})\,S_0(H)}_{E_c}+\underbrace{\gamma^H G_\pi\big(\epsilon_F^a+\epsilon_F^s K_a\Lambda_H\big)}_{E_F}+\underbrace{G_\pi Q'_a\tfrac{\gamma^{H+1}}{1-\gamma}}_{E_{\mathrm{trunc}}\ (\text{per-state})}+E_W,$$
with the following ingredients:
- $\Lambda_H=\sum_{t<H}L^{H-t-1}$ ($=H$ at $L=1$) and $S_0(H)=\sum_{t<H}\gamma^t\le\min(H,\tfrac1{1-\gamma})$.
- $S_1(H)=\sum_{t<H}\gamma^t\sum_{n=1}^{H-t}n\,u^{n-1}$, which is $\le S_0(H)/(1-u)^2$ if $u<1$ and $\le\tfrac12H^2(H+1)u^{H-1}$ if $u\ge1$.
- The terminal state-gradient Jacobian error, $\gamma^HG_\pi Q'_sH\epsilon_J u^{H-1}$, is absorbed into $E_J$.
- $E_W\le G_\pi R'\eta_W S_1(H)/\min(1,R')$, which vanishes when $W_t=\Sigma_B^{-1}$. Unwhitened rollouts set $W_t=I$, so $\eta_W=\|\Sigma_B-I\|$, which can be $O(1)$ (B01 Kantorovich bound).

**Horizon tradeoff over $H\in\{1,4,8,16,32\}$ (worked at $\gamma=0.99$).**

| $H$ | $\gamma^H$ (critic weight) | $\gamma^HH$ ($E_F^s$ multiplier, $L{=}1$) | $\gamma^{H+1}$ (residual mismatch) | $S_1(H)$, $u{=}1$ | $S_1(H)$, $u{=}1.1$ |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.990 | 0.99 | 0.980 | 1 | 1 |
| 4 | 0.961 | 3.84 | 0.951 | 19.9 | 23.0 |
| 8 | 0.923 | 7.38 | 0.914 | 118 | 168 |
| 16 | 0.851 | 13.6 | 0.843 | $\approx 7.9\!\times\!10^2$ | $\approx1.7\!\times\!10^3$ |
| 32 | 0.725 | 23.2 | 0.718 | $\approx5.5\!\times\!10^3$ | $\approx3.1\!\times\!10^4$ |

What the table implies:
1. At $\gamma=0.99$, $H=32$ removes only 27.5% of the critic's weight. Over this sweep the hybrid's gain **cannot** come mainly from "trusting $\bar F$ less".
2. The critic *state*-gradient term $\gamma^HH\epsilon_F^s$ **grows** for every $H<1/|\ln\gamma|\approx99.5$. $\nabla_s\bar F$ is never fit by FB TD, so $\epsilon_F^s$ is plausibly large (claim C-B04-A-01).
3. $E_J$ grows at least cubically in $H$, and exponentially once contacts make $u>1$.

Whatever accuracy $\hat g_D$ gains has to come from the model-reward head replacing $\epsilon_F^a$ on the first $H$ terms, plus the $H$-step occupancy correction. Both are bounded above by the $1-\gamma^H$ share of the value. The predicted optimum is an interior $H^\star$ where $dE_J/dH$ meets the head gain. With the spike's empirical $\|\hat s_H-s_H\|\approx0.03H$ (the $u\approx1$ regime), that optimum is $H^\star\in[8,16]$. This prior is consistent with H3, but it remains a hypothesis.

## 2. Controlled Four-Arm Experimental Architecture and Stop-Gradient Specification

**2.1 Shared substrate (identical across all arms).** All arms share:
- the same plant, observation/action contract, `FBReplay`, and $z_{\mathrm{update}}$ 50/50 sampler under two-pass frozen BN;
- the same $F,B$ widths, Gram tracker, and twin critics $\bar F_{1,2}$;
- the same world model, $W_\psi:\ (\hat s_t,a_t)\mapsto$ normalized $\Delta s$ plus survival logit $\ell_t$, an MLP `[512,512,256]` with SiLU and LayerNorm. It is **trained in every arm**, including A and B where it is never consumed. This equalizes representation and compute overhead, so that wall-clock differences isolate how the model is *used*.

The model loss on real $K{=}8$-step replay segments, with $\hat s_0=s_0$, autoregressive inputs, and no $m_{t+1..}$ input (zero future leakage), is
$$\mathcal L_\psi=\tfrac1K\sum_{k<K}\big[\|\hat\Delta_k-\Delta_k\|^2+\lambda_\kappa\|\kappa(\hat s_{k+1})-m_{k+1}\|^2+\lambda_c\,\mathrm{BCE}(\sigma(\ell_k),1-d_k)\big].$$
The supervision rules are:
- The target $m_{k+1}$ only *supervises*; it never enters $W_\psi$.
- Segments stop at the first terminal: steps after $d_k=1$ are masked with the *real* boolean. That is legal here because those booleans are data and carry no gradient.
- `invalid` rows are never in replay (Charter §2.4).

Reporting: env steps, imagined steps, gradient steps, and GPU-seconds. Arms are matched on GPU-seconds (primary) and on env steps (secondary).

**2.2 Arms.** $n$ and $H$ share the sweep $\{0,1,4,8,16,32\}$. $H{=}0$ is Arm A, and $n{=}1$ reduces B and C to A.

| Arm | $F$ target | Actor objective | Isolates |
|---|---|---|---|
| **A** ($H{=}0$) | 1-step FB measure loss | $\max\ \min_k F_k(s,\pi_\theta(s,z),z)^\top z$ | null baseline |
| **B** ($n$) | $n$-step **real** segment, deterministic trace-cut | as A | faster $F$ propagation, no model |
| **C** ($n$) | 1 real step, then $n{-}1$ **imagined** on-policy steps under $\pi_\theta(\cdot,z_{\mathrm{update}})$, fully detached | as A | on-policy multi-step targets via model |
| **D** ($H$) | as A (1-step) | $\max\hat J_H$ (§1b) | pathwise $H$-step actor derivative |

**$n$-step FB measure loss (Arms B and C).** This is the exact generalization of `baseline/01` §2.4 and needs **no** $\Sigma_B^{-1}$. With $x\sim\rho$ independent,
$$\mathcal L^{(n)}=\mathbb E\big[(F(s,a,z)^\top B(x)-\gamma^n\bar c_n\bar F(s_n,\pi_\theta(s_n,z),z)^\top\bar B(x))^2\big]-2\,\mathbb E\Big[\textstyle\sum_{k<n}\gamma^k\bar c_k\,F(s,a,z)^\top B(s_{k+1})\Big].$$
Per-arm details:
- **Arm B** sets $\bar c_k$ to the real alive mask times the trace indicator $\prod_{1\le i\le k}\mathbf 1[\|a_i-\pi_\theta(s_i,z)\|_\infty\le\delta_a]$, with $\delta_a=0.05$. The effective length is $n_{\mathrm{eff}}=$ the first cut. For uniform-sphere $z_{\mathrm{update}}$, $n_{\mathrm{eff}}\to1$ almost surely. This is a predicted failure mode, not a bug, and the mean $n_{\mathrm{eff}}$ is logged per $z$-source. Without the cut, the target would estimate the *behavior* policy's successor measure.
- **Arm C** sets $\bar c_k=\mathrm{sg}(c_k)$ and $s_{k+1}\leftarrow\mathrm{sg}(\hat s_{k+1})$ for $k\ge1$, with $s_1$ real. The diagonal term on imagined states uses online $B(\kappa(\hat s_{k+1}))$ with its input detached, so $B$ can be trained toward model artefacts only through its weights. This arm gets a dedicated diagnostic: online $B$'s Gram drift under C versus A.

**2.3 Stop-gradient specification (Arm D actor step).**

| Quantity | Weights | Input gradient | Notes |
|---|---|---|---|
| $\hat s_0$ (replay) | n/a | **sg** | rollout starts only on non-terminal valid rows |
| $W_\psi$, $\hat p_{\mathrm{surv}}$ | frozen | **kept** ($\partial/\partial\hat s,\partial/\partial a$) | eval mode |
| $\pi_\theta(\hat s_t,z)$, $t=0..H$ | **trained** | kept | $a_H$ inside tail also differentiated |
| $\bar B$ | frozen, eval BN | **kept** through $\kappa$ | site (iv) of B01 |
| $W_t$, $z$, $\ell_t$ | sg (FP64 Cholesky, cast) | none | $v_z=\mathrm{cholesky\_solve}(z,L_t)$ |
| $\bar F_{1,2}$ | frozen (target) | kept ($\partial_s,\partial_a$) | $\min_k$ over scalars $\bar F_k^\top z$ |

Gate: if the B01 leverage/split-half gate is closed for a command, that command's loss is routed to the Arm A objective. The routed fraction is logged per $H$.

**Survival chain rule.** Work in log-space, $\log c_t=\sum_{j<t}\log\sigma(\ell_j)$ with $\ell_j=\ell_\psi(\hat s_j,a_j)$:
$$\frac{\partial c_t}{\partial a_j}=c_t\Big[(1-\hat p_j)\,\partial_a\ell_j+\sum_{i=j+1}^{t-1}(1-\hat p_i)\,\partial_s\ell_i\,\frac{\partial\hat s_i}{\partial a_j}\Big],\quad j<t;\qquad \frac{\partial c_t}{\partial a_j}=0,\ j\ge t.$$
The factor $(1-\hat p)$ makes the term bounded and self-damping: no $1/p$ blow-up when $p\to0$. Each $a_j$ therefore receives the summed hazard-avoidance signal $\sum_{t>j}\gamma^t(\partial c_t/\partial a_j)[r_t\text{ or tail}]$, which is a pathwise "do not fall later" gradient.

**Why hard boolean masks cannot be multiplied across imagined steps.** Let $\tilde c_t=\prod_{j<t}\mathbf 1[g(\hat s_j,a_j)>0]$, for example $g=0.03-\widehat{\mathrm{pen}}$. Three problems follow:
1. **Zero pathwise gradient.** $\tilde c_t$ is piecewise constant in $\theta$, so $\partial\tilde c_t/\partial\theta=0$ a.e. Meanwhile $\nabla_\theta\mathbb E_{s_0}[\tilde c_t]=-\sum_{j<t}\oint_{\{g_j=0\}}(\ldots)\,dS\ne0$ is a pure boundary (Dirac) term that the pathwise estimator misses entirely. This is a systematic bias equal to the full hazard-avoidance gradient.
2. **Crossing at a predicted, not credible, termination.** The product turns a model-predicted crossing into an absorbing event. Under Charter §2.4, only a real simulator penetration with finite tensors is a credible termination, and an imagined crossing is a model error with probability $\ge\epsilon_c$.
3. **Error compounding.** With per-step false-positive rate $\epsilon_c$, the hard product's truncation error is $1-(1-\epsilon_c)^t\approx t\epsilon_c$, the same as the soft product. The soft product, however, also carries a gradient. Hard masks remain correct only on *real* segments (Arm B, $\mathcal L_\psi$), where no gradient flows through them.

**Contact stiffness rule.** Per step, estimate $\hat\sigma_t=\|\hat A_t v\|/\|v\|$ with one JVP power-iteration step, $v$ warm-started. If $\prod_{i\le t}\hat\sigma_i>\Lambda_{\max}=10$, apply sg to $\hat s_{t+1}$ in the *backward* pass only, while forward values are kept. This truncates the gradient horizon, not the value horizon. The realized gradient horizon $H_{\mathrm{grad}}\le H$ is logged.

**2.4 Mapping to `baseline/03` §6.** b03-Arm A (single-task WM, $H{=}32$) has no FB, so it is excluded by the B04 core question. b03-B and b03-C (multi-task WM, $H\in\{32,1\}$) correspond to Arm D with $\bar F$ replaced by a $z$-conditioned $V_\phi$, so I add them as the D-control "**D-V**". b03-D is Arm D. A factorial note: {B, C targets}$\times${pathwise actor} is left for B05, since I judge it lower priority.

## 3. Serious Alternative Considered and Rejected

**Alternative L: latent backward dynamics** $\hat B_{t+1}=T_{\mathrm{lat}}(B_t,a_t)$, with rewards $\hat B_{t+1}^\top W_tz$. It avoids full-state reconstruction. I reject it for three reasons.

*(L1) It is non-Markov and has an irreducible error floor.* $B_t=B(\kappa(s_t))$ is a function of single-frame kinematics. It excludes velocities' hidden components, contact state, obstacle and ball state (Charter §2.3), and it is not injective on $s$. For any predictor, by the law of total variance,
$$\mathbb E\|T_{\mathrm{lat}}(B_t,a_t)-B_{t+1}\|^2\ \ge\ \mathbb E\big\|\mathbb E[B_{t+1}\mid s_t,a_t]-\mathbb E[B_{t+1}\mid B_t,a_t]\big\|^2=:\mathcal A>0$$
whenever two states with equal $B$ but different velocity or contact map to different successors. This happens generically: a crouch descending and a crouch ascending share a frame. A full-state $W_\psi$ has floor $0$ on a deterministic plant. The aliasing also enters the Jacobian, so $\epsilon_J^{\mathrm{lat}}$ does not vanish with data.

*(L2) It breaks the closed loop.* $a_t=\pi_\theta(o_{\mathrm{low},t},z)$ needs $o_{\mathrm{low}}$, and the terminal tail needs $\bar F(\hat s_H,\cdot)$. The latent model must therefore either feed $B$ to the actor, which violates the actor input contract and the 1-step/Arm-A comparability, or decode $s$, which is a full-state model plus an extra error source.

*(L3) It is gauge non-stationary.* For any invertible $A$, $(AB,A^{-\top}F)$ is an equivalent FB solution (`baseline/01` §3.3), and $B_\omega$ drifts through such transforms during joint training. A latent model fit in $B_{\omega_{t-\tau}}$ coordinates incurs error $\|(A_\tau-I)\|\,\|B\|$ after a lag $\tau$, so it must be retrained at the FB update rate. The state model $W_\psi$ is invariant: the reward head re-reads $\bar B_t(\kappa(\hat s))$ with the current target net.

**Alternative U: unbootstrapped $H$-step rollout** (Track 3). I reject it by counterexample. Take a chain with two first actions: "safe", which gives $r=\epsilon$ per step forever, and "commit", which gives $r=0$ for $H$ steps and then $r=1$ forever. The truncated objective prefers safe for every $\epsilon>0$. The true objective prefers commit iff $\gamma^H>\epsilon$; at $\gamma=0.99$, $H=32$ that means $\epsilon<0.72$. The truncated optimum is wrong on an open set. Obstacle commitment and recovery-from-fall have exactly this delayed structure. The bias is $\ge\gamma^H|V_{\min}|$ in value, it does not vanish for any finite $H$, and it is retained only as the "D, no tail" ablation in §5.

## 4. Candidate Necessity Claims (Appendix B)

Grade convention used here: **Grade 1** means deductive from the stated premises. **Grade 2** means it additionally requires an empirical premise, which is then tested.

**C-B04-A-01 (Terminal-critic state-gradient amplification).**
- *Premises:*
  - (P1) $\gamma\in(0,1)$, closed-loop $L\ge1$ over the rollout.
  - (P2) $\bar F$ is trained only by value-level FB TD, so $\epsilon_F^s$ is not controlled by the loss.
  - (P3, empirical) critic state-gradient errors along $\partial\hat s_H/\partial\theta$ accumulate coherently and do not cancel (Grade-2 premise).
- *Conclusion shape:* the critic-attributed gradient error $E_F(H)=\gamma^H(\epsilon_F^a+\epsilon_F^sK_a\Lambda_H)$ is nondecreasing on $H\in[1,H_c]$ iff $\epsilon_F^sK_a(1-H|\ln\gamma|)\ge|\ln\gamma|\,\epsilon_F^a$ (at $L{=}1$). At $\gamma=0.99$, $H_c\ge32$ whenever $\epsilon_F^sK_a\ge0.015\,\epsilon_F^a$. Hence any H3 gain over $H\le32$ must be explained by the head terms ($\epsilon_F^a$ replacement and occupancy correction), **not** by reduced critic reliance. *Grade 2.* The bound itself is Grade 1.
- *Operational test:* oracle substitution (§5.3). Replace $\bar F$ in the tail by the oracle $Q^\star$ (autograd through the true plant) and record $\Delta_F(H)=\mathrm{relL2}(\hat g_D)-\mathrm{relL2}(\hat g_D^{F\to\star})$.
- *Falsifier:* $\Delta_F(32)<0.8\,\Delta_F(4)$, with the 95% bootstrap CI over 5 seeds excluding $0.8$, on the critic that passes the quality gate.

**C-B04-A-02 (Soft survival is necessary for pathwise hazard avoidance).**
- *Premises:* termination is a threshold event on $\hat s$, and the actor update is purely pathwise.
- *Conclusion:* with hard multiplied masks, the survival component of $\hat g_D$ is $0$ a.e. while the true one is nonzero. *Grade 1.*
- *Operational test:* on states within 2 steps of a penetration crossing, compute $\cos(\hat g_D^{\mathrm{hard}}-\hat g_D^{\mathrm{nosurv}},\,g^\star_{\mathrm{surv}})$.
- *Falsifier:* a nonzero hard-mask survival component, which would indicate an implementation leak, or soft $\cos\le0.2$.

**C-B04-A-03 (Whitening necessity is $\kappa$-conditional).** This is inherited from B01 site (iv).
- *Conclusion:* the whitened-minus-unwhitened cosine gap at fixed $H$ is $\approx0$ at $\kappa(\Sigma_B)=1$ and grows with $\kappa$. *Grade 1* in population.
- *Falsifier:* a gap $>0.05$ at $\kappa=1$. That would mean the spike's whitening effect, 0.415 vs 0.050 at $H{=}8$, is an artefact rather than splice repair.

## 5. Pre-Registered Empirical Spike Protocol

**5.0 Reading of the existing spike.** I treat it as smoke-level only, for four reasons:
1. $H{=}0$ cosine $=-0.002$ says the spike's critic carried no action-gradient information, which reflects an untrained or uncalibrated $\bar F$, not FB.
2. relL2 is $\ge0.85$ at every $H$, and $1.024$ at $H{=}32$ despite the highest cosine (0.556), so magnitudes are wrong.
3. `best_short_horizon_hybrid_cosine` reports the $H{=}8$ value although $H{=}16,32$ scored higher.
4. Its state error $\approx0.031H$ does usefully fix the $u\approx1$ regime used in §1.

**5.1 Plant (PyTorch, float64, fully differentiable).** A planar 5-DoF hopper-torso:
- State $s\in\mathbb R^{12}$ (pose, velocities, contact-relevant heights), action $a\in[-1,1]^3$, $dt=0.02$.
- Soft penalty ground contact $f_n=k\,\mathrm{softplus}(-y/\varepsilon)\varepsilon$ with $k\in\{10^3,10^4\}$ (two stiffness levels set $u$), and smoothed friction $\mu f_n\tanh(v_x/v_0)$.
- Penetration hazard $p^\star=\sigma((0.03-\mathrm{pen})/\tau)$ with $\tau=0.005$.
- Motion map $\kappa$: root-relative link kinematics, 24 dims.
- $B^\star$: frozen random 2-layer MLP, then a linear map with condition number $\kappa(\Sigma_B)\in\{1,30,300\}$ (calibrated on $\rho$ after projection to $\sqrt{d_z}\mathcal S^{d_z-1}$), with $d_z=32$.
- Policy $\pi_\theta$: fixed, a pretrained mid-quality checkpoint (1/3 of training), $\theta$ frozen during measurement.

**5.2 Learned components (5 seeds).**
- $\bar F$: trained with 1-step FB on $\rho$ produced by a *different* behavior $z$ mixture. **Critic quality gate**: $R^2(\bar F^\top z,\ \text{MC return})\ge0.8$ on held-out data, else the run is void.
- $W_\psi$ (§2.1): trained on $\{10^4,10^5,10^6\}$ transitions, so $\epsilon_J$ is varied. $\epsilon_J,\epsilon_c,\epsilon_F^{a},\epsilon_F^{s}$ are *measured* by JVP against the true plant on held-out states.

**5.3 Estimators at fixed $\theta$** ($N=1024$ starts $\times$ 64 commands, half sphere and half $B(m_{\mathrm{demo}})$):
- (i) $H{=}0$: $\hat g_A$.
- (ii) $\hat g_D$ for $H\in\{1,4,8,16,32\}$, whitened with $W_t$.
- (iii) the same, unwhitened ($W_t=I$).
- (iv) D-no-tail.
- (v) D with hard masks.
- (vi) D-V.
- (vii) oracle substitutions, swapping one at a time $W_\psi\to f$, $\hat p\to p^\star$, $\bar F\to Q^\star$, $W_t\to\Sigma_B^{-1}$, which yields $E_J,E_c,E_F,E_W$ per $H$.

The ground truth $g^\star$ is autograd through the true plant to $T=460$ ($\gamma^T<0.01$) with soft $p^\star$, checked against central finite differences on 16 random $\theta$-directions (rel. dev. $<10^{-4}$).

**5.4 Metrics.** Cosine and relL2 against $g^\star$:
- **per-state** ($s_0$-wise, then averaged);
- **occupancy-aggregated** (sum over a batch drawn from $d^{\pi_z}_\gamma$ vs. from $\rho$; this is the fair metric for Arm A, see §1a).

Also reported: $H_{\mathrm{grad}}$, gate-routed fraction, imagined steps/s, and GPU-seconds.

**5.5 Pre-registered decisions (5 seeds, 95% bootstrap CI).**
- **H3 supported** iff $H^\star=\arg\min_H\mathrm{relL2}_{\mathrm{agg}}\in\{8,16\}$ *and* $\mathrm{relL2}_{\mathrm{agg}}(H^\star)\le0.8\min\{\mathrm{relL2}_{\mathrm{agg}}(\hat g_A),\ \mathrm{relL2}_{\mathrm{agg}}(\text{no-tail},H{=}32)\}$, at both stiffness levels and the median $\epsilon_J$.
- **H3 refuted** iff $\hat g_A$ is within CI of the best $\hat g_D$ under aggregation, or if $H^\star=32$.
- Whitening: C-B04-A-03 (gap $\ge0.10$ at $\kappa=300$, $\le0.05$ at $\kappa=1$).
- Survival: C-B04-A-02.
- Critic: C-B04-A-01.
- No result here licenses any claim about obstacle traversal or ball striking (Charter §2.5). A pass only unlocks the full four-arm GPU training protocol of §2, at matched GPU-seconds.
