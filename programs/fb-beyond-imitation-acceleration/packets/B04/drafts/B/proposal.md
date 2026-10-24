# Proposal B (Packet B04): Differentiable World-Model Rollouts vs. FB Long-Horizon Bootstrapping

Author: Primary Author B. Status: theoretical proposal and pre-registration; no experiment was executed.
Frozen basis: PROGRAM_CHARTER.md, B01-synthesis.md, B04/brief.md, baseline/01, and baseline/03.
Scope resolution: the user's four-arm definitions below govern; baseline/03 §6 uses different arm names and is not silently treated as the same experiment.
Recommendation: test short causal rollouts with an FB tail; select the horizon from measured gradient error and cost, rather than presuming that 8 or 16 wins.

## 1. Exact Pathwise Policy Gradient Decomposition and Error Bounds

**Coordinates and objective.** Fix the representation, command, initial distribution, and reference policy parameters $\theta_0$ for one gradient evaluation.
Let $s\in\mathbb R^{d_s}$, $a\in\mathbb R^{d_a}$, $\theta\in\mathbb R^{d_\theta}$, $z,\bar B(m)\in\mathbb R^{d_z}$, and $m=M(s)\in\mathbb R^{229}$ or $\mathbb R^{277}$.
The deployed policy sees only causal $o_{\rm low}=O(s)$; derivatives below include $O_s$, and $B$ sees only single-frame root-relative motion.
Write $f(s,a,\xi)$ for reparameterized dynamics, with parameter-independent noise $\xi$; deterministic dynamics are the special case.
For the exact benchmark set $r_z^*(s')=\bar B(M(s'))^\top\Sigma_{\bar B}^{-1}z$, with full-rank $\Sigma_{\bar B}$ on the evaluated support.
Rank deficiency restricts identifiable commands to the support projection; damping alone does not identify nullspace commands.
Let $p(s,a)\in[0,1]$ be the true conditional probability of continuing **after** emitting the current transition reward.
Thus a finite physical failure contributes its arrival reward, has no subsequent reward, and has zero continuation value.
The following soft-survival representation assumes conditional termination has been integrated out consistently with the transition kernel.
It is exact for the smooth killed-process benchmark below; a sigmoid surrogate of a deterministic contact boundary adds a separate smoothing bias.
Define $c_0=1$, $c_{t+1}=c_t p_t$, $a_t=\pi_\theta(s_t,z)$, and
$$J_\infty(\theta,z)=\mathbb E_{\mu,\xi}\sum_{t\ge0}\gamma^t c_t r_z^*(s_{t+1}),\qquad 0<\gamma<1.$$
Assume dominated differentiation, bounded relevant derivatives, and convergent discounted sensitivities; these conditions can fail at hard impacts.

**Exact forward sensitivity.** With column gradients, define $P_t=\partial_\theta\pi_\theta(s_t,z)|_{s_t}\in\mathbb R^{d_a\times d_\theta}$ and $K_t=\partial_s\pi_\theta(s_t,z)$.
Let $S_t=D_\theta s_t$, $A_t=D_\theta a_t=K_tS_t+P_t$, and $C_t=D_\theta c_t$ (a row vector).
For a detached initial state, $S_0=C_0=0$, and
$$S_{t+1}=(f_s+f_aK_t)S_t+f_aP_t,\qquad C_{t+1}=p_tC_t+c_t(p_sS_t+p_aA_t).$$
Consequently the exact gradient is
$$g_\infty=\mathbb E\sum_{t\ge0}\gamma^t\left[c_t S_{t+1}^{\top}\nabla r_z^*(s_{t+1})+r_z^*(s_{t+1})C_t^\top\right].$$
Equivalently, let $Q^{\theta_0}_z(s,a)$ hold every policy parameter after the current action fixed at $\theta_0$.
Its action derivative includes future **state-mediated** feedback through $K_t$, survival, and rewards.
At $\theta=\theta_0$, the adjoint/policy-gradient decomposition is
$$g_\infty=\mathbb E\sum_{t\ge0}\gamma^t c_t P_t^\top\nabla_a Q^{\theta_0}_z(s_t,a_t).$$
This equality follows by assigning each occurrence of the direct parameter injection $P_t$ in the sensitivity recurrence its downstream adjoint.

**Standard FB comparison.** Scalarize each twin before taking the minimum: $Q_F(s,a,z)=\min_k F_k(s,a,z)^\top z$.
Its frozen-weight update is $g_0=\mathbb E_\mu P_0^\top\nabla_a Q_F(s_0,a_0,z)$, precisely the requested one-action derivative.
Even an exact $Q_F=Q^{\theta_0}_z$ omits $\sum_{t\ge1}\gamma^tc_tP_t^\top Q_a$ for this fixed-start objective.
It does not omit long-horizon consequences of perturbing $a_0$; those already belong to $Q_a$.
This is not a universal defect of deterministic policy gradients: sampling the normalized discounted on-policy occupancy and scaling by $1/(1-\gamma)$ recovers the full gradient.
Replay sampling generally differs from that occupancy; report this distribution mismatch separately from derivative approximation.

**Hybrid derivative.** During update $u$, freeze $W_u$ and all target weights, and use
$$\widehat J_H=\mathbb E\left[\sum_{t=0}^{H-1}\gamma^t\hat c_t\bar B(M(\hat s_{t+1}))^\top W_u z+\gamma^H\hat c_H\bar Q_F(\hat s_H,\pi_\theta(\hat s_H,z),z)\right].$$
Here $W_u$ is the matrix denoted $W_t$ in the brief; its index is an optimizer update, not an imagined time step.
Writing $\hat r_t=\bar B(M(\hat s_{t+1}))^\top W_uz$ and $\bar Q=\bar Q_F(\hat s_H,a_H,z)$ gives
$$\hat g_H=\mathbb E\left[\sum_{t<H}\gamma^t(\hat c_t\hat S_{t+1}^\top\nabla\hat r_t+\hat r_t\hat C_t^\top)+\gamma^H\{\bar Q\hat C_H^\top+\hat c_H[\hat S_H^\top\bar Q_s+\hat A_H^\top\bar Q_a]\}\right].$$
The terminal policy call contributes $P_H$: this formula differentiates $H+1$ policy calls, including $a_H$, and $H$ model transitions.
At $H=0$ it reduces to the frozen target-critic version of the standard FB derivative.
With exact dynamics, survival, coordinates, and an exact frozen-policy $Q^{\theta_0}_z$, Bellman expansion gives
$$g_H^{\rm oracle}=\mathbb E\sum_{t=0}^{H}\gamma^tc_tP_t^\top Q_a^{\theta_0},\qquad g_\infty-g_H^{\rm oracle}=\mathbb E\sum_{t>H}\gamma^tc_tP_t^\top Q_a^{\theta_0}.$$
An exact terminal value is therefore not an exact shared-parameter gradient: its internal future-policy parameter dependence remains frozen.
If $\|P_t\|\le P$, $\|Q_a\|\le A$, and $p_t\le\bar p$, the omitted-policy tail is at most $T_H=PA(\gamma\bar p)^{H+1}/(1-\gamma\bar p)$.

**What an error bound must assume.** Probability calibration alone and scalar TD residuals cannot bound pathwise gradients.
For example, $\hat p=p+\delta\sin(\omega a)$ has probability error at most $\delta$ but derivative error $\delta\omega$.
Define $\epsilon_c=\max(\|\hat p-p\|_\infty,\|D_{s,a}\hat p-D_{s,a}p\|_\infty)$; also report its value and derivative components separately.
Define $\epsilon_J=\|D_{s,a}\hat f-D_{s,a}f\|_\infty$ and $\epsilon_s=\|\hat f-f\|_\infty$ on a common verified rollout tube.
Define $\epsilon_F=\max_k\|\bar F_k^\top z-Q_z^{\theta_0}\|_{C^1(s,a)}$ there, including target-policy lag, representation residual, and pessimism.
A scalar value residual alone is insufficient: $\delta\sin(\omega a)$ gives the same counterexample.
Both state and action derivatives are needed at $H>0$; at $H=0$ the critic action-derivative residual suffices.
At twin ties use the implementation's deterministic branch/subgradient; a uniform bound for both twins bounds either choice.

**Explicit compounding bound.** Augment $x=(s,c)$ and define the closed-loop map $G_\theta(x)=(f(s,\pi_\theta(s)),cp(s,\pi_\theta(s)))$.
Let $q_\theta(x)=c\,r_z^*(f(s,\pi_\theta(s)))$ and $v_\theta(x)=c\,Q_z^{\theta_0}(s,\pi_\theta(s))$.
On the tube suppose $\|G_x\|,\|\hat G_x\|\le L$, $\|G_\theta\|,\|\hat G_\theta\|\le U$, and derivatives of $G$ are $K_G$-Lipschitz.
Let $\epsilon_0=\|\hat G-G\|_\infty\le C_0(\epsilon_s+\epsilon_c)$ and $\epsilon_D=\max(\|\hat G_x-G_x\|,\|\hat G_\theta-G_\theta\|)\le C_D(\epsilon_J+\epsilon_c)$.
Constants depend on bounded policy derivatives and $f_a,p_a$, not on $H$; derivatives are compared at the same input.
Put $A_t(L)=\sum_{i=0}^{t-1}L^i$, $M_t=UA_t(L)$, $\delta_t=\epsilon_0A_t(L)$, and $E_0=0$.
Coupling true and model trajectories with identical noise yields $\|x_t-\hat x_t\|\le\delta_t$, $\|D_\theta x_t\|,\|D_\theta\hat x_t\|\le M_t$, and
$$E_{t+1}=LE_t+[\epsilon_D+K_G\delta_t](1+M_t),\qquad \|D_\theta\hat x_t-D_\theta x_t\|\le E_t.$$
Assume $q_x,q_\theta$ are bounded by $R_1$ and $K_r$-Lipschitz, and $v_x,v_\theta$ by $V_1$ and $K_v$-Lipschitz.
Let $\eta_r=\max(\|\hat q_x-q_x\|,\|\hat q_\theta-q_\theta\|)$ and $\eta_v=\max(\|\hat v_x-v_x\|,\|\hat v_\theta-v_\theta\|)$ at common inputs.
Then $\eta_r\le C_r(\epsilon_s+\epsilon_J+\epsilon_W)$, $\eta_v\le C_v\epsilon_F$, with $\epsilon_W=\|W_u-\Sigma_{\bar B}^{-1}\|$.
These constants require bounded feature derivatives; for normalized $B$, small pre-normalization norms must be excluded or stabilized.
Termwise differentiation and the triangle inequality give the usable horizon-dependent bias envelope
$$\|\mathbb E\hat g_H-g_\infty\|\le B_H:=T_H+\sum_{t<H}\gamma^t[(\eta_r+K_r\delta_t)(1+M_t)+R_1E_t]+\gamma^H[(\eta_v+K_v\delta_H)(1+M_H)+V_1E_H].$$
At $H=0$, the sharper comparison is $\|g_0-g_\infty\|\le PA\gamma\bar p/(1-\gamma\bar p)+P\epsilon_F$.
When $L=1$, $M_t=Ut$, $\delta_t=t\epsilon_0$, and $E_t\le\epsilon_D[t+Ut(t-1)/2]+K_G\epsilon_0[t(t-1)/2+Ut(t-1)(2t-1)/6]$.
For $L>1$, $A_t=(L^t-1)/(L-1)$ exposes potentially exponential growth; $\gamma^H$ need not overcome contact amplification.
Thus no bound depending only on $(H,\epsilon_J,\epsilon_c,\epsilon_F)$ is valid without state-value error, whitening error, and regularity assumptions.

**Variance and selection.** For $N$ independent start/noise samples conditional on a fixed fitted model, $\mathrm{MSE}(\bar g_H)=\|\mathbb E\hat g_H-g_\infty\|^2+\operatorname{tr}\operatorname{Cov}(\hat g_H)/N$.
Using common bounds for true and approximate reward/tail derivatives, define $G_H=\sum_{t<H}\gamma^tR_1(1+M_t)+\gamma^HV_1(1+M_H)$.
Then $\operatorname{tr}\operatorname{Cov}(\hat g_H)\le\mathbb E\|\hat g_H\|^2\le G_H^2$; correlations within a trajectory are retained.
Across fitted-model seeds add the between-model variance by total variance; it does not disappear by enlarging one model's minibatch.
For budget $T$, use $N_H=\lfloor T/\tau_H\rfloor$ and compare $B_H^2+G_H^2/N_H$ as a conservative diagnostic, alongside measured MSE.
Evaluate $H\in\{1,4,8,16,32\}$: increasing $H$ suppresses $T_H$, exposes additional policy injections, and increases model/contact error and cost.
There is no theorem that variance decreases with $H$ or that $H=8,16$ must win; both are pre-registered hypotheses.

## 2. Controlled Four-Arm Experimental Architecture and Stop-Gradient Specification

All arms share plant, causal observation/action maps, $F/B/\pi$ sizes, replay, seeds, initial weights, optimizer settings, and evaluation starts.
Use $H$ solely for differentiated model transitions; $n$ denotes a critic-target propagation length.
| Arm | Critic training | Actor derivative | Sweep |
|---|---|---|---|
| A | Standard one-step real FB density loss | $P_0^\top\nabla_a\min_kF_k^\top z$ | $H=0$ |
| B | Real-segment $n$-step FB propagation | Exactly A | $n=1,4,8,16,32$; actor $H=0$ |
| C | Local model $n$-step $F$ target, anchored by real FB loss | Exactly A | $n=1,4,8,16,32$; actor $H=0$ |
| D | Same real one-step FB loss as A | Causal whitened hybrid $\hat g_H$ | $H=1,4,8,16,32$, with $H=0$ control |
An additional paired D test uses the identical online critic snapshot at $H=0$; report the standard online-versus-target critic difference separately.
A–B isolates real propagation; B–C compares target sources subject to off-policy coverage; A–D isolates actor rollout with unchanged critic loss.
C–D alone changes two factors; additionally evaluate both actor derivatives on the same frozen critic/model/start batches to isolate differentiation.
Keep representation networks present in all four arms; measure FB/Gram/model/actor overhead separately rather than attributing it to a task-conditioning change.
The single-task/no-F variants from baseline/03 §6 are optional auxiliary baselines, not replacements for these four arms.

**Targets and off-policy validity.** Write $\phi_u(s')=W_u\bar B(M(s'))$ and $d_i=1-\mathrm{terminated}_i$ for valid real transitions.
In target coordinates, for an on-policy segment,
$$Y^{(n)}=\sum_{i=0}^{n-1}\gamma^i\left(\prod_{j<i}d_j\right)\phi_u(s_{i+1})+\gamma^n\left(\prod_{j<n}d_j\right)\bar F(s_n,\bar\pi(s_n,z),z).$$
Each twin uses its own vector target; pessimistic minimum is applied only after scalar projection for actor/value reporting.
B keeps the standard real density loss and adds a unit-weight $\|F_k-Y_k^{(n)}\|^2$ in a common target-coordinate snapshot.
C uses the same loss coefficient and formula, with the first actual $(s_0,a_0)$ followed by causal model transitions and soft survival.
Coordinate drift and damped $\phi_u$ make these auxiliary targets approximate; measure their Bellman splice residual rather than declaring exact equivalence.
B must not treat an arbitrary replay segment as a rollout of freshly relabeled $z$.
The primary deterministic implementation cuts before the first continuation action inconsistent with the current target policy, including policy-version and macro-command changes.
Thus with fresh 50/50 relabeling many B targets have $n_{\rm eff}=1$; publish the full $n_{\rm eff}$ histogram and do not claim a multi-step benefit from nominal $n$.
A separate matched-segment diagnostic collects continuations under the frozen evaluation policy and command for all arms and charges every extra real step.
That diagnostic evaluates propagation on fixed commands; it does not replace the mandated 50/50 relabeling in primary training.
If stochastic likelihood correction is added later, it requires a separate registration; command equality alone never certifies off-policy validity.

**Model and training.** Use an ensemble of five residual MLPs, each input $d_s+d_a$, SiLU widths $[512,512,256]$, outputs $d_s$ normalized state deltas plus one survival logit.
Predict $\hat s'= \hat s+\mu_\Delta+\sigma_\Delta\odot\Delta_\psi(\operatorname{norm}(\hat s),a)$; normalize orientation coordinates with a differentiable valid-chart map.
Inputs include only current causal physical state or causal belief, including observed terrain where available; no future demonstration or replay next-frame feature is an input.
For partial observability use a causal recurrent state, with 16 real-prefix burn-in steps detached at the rollout boundary; reject missing-prefix segments.
On valid contiguous replay segments unroll eight recorded actions and minimize
$$\mathcal L_{\rm wm}=\tfrac18\sum_{i=0}^{7}v_i\left[\|\widehat{\Delta s}_i-\Delta s_i\|_{\sigma_\Delta^{-2}}^2+\|\hat b_{i+1}-b_{i+1}\|_2^2+\operatorname{BCE}(\hat p_i,d_i)\right],$$
where $b$ denotes differentiable body positions and $v_i$ marks existing valid transitions, including the first physical terminal transition.
No loss uses a fabricated post-terminal next state; truncate shorter segments and normalize by the number of valid terms.
Train members on seeded bootstrap samples, Adam $10^{-3}$, batch 256, one model update per shared learner update; freeze normalization during actor unroll.
BCE fits probabilities but does not certify survival derivatives; validate action/state perturbation responses separately.

**Exact gradient boundaries.** During an actor pass, set model, survival head, $\bar B$, and both $\bar F$ weights to requires_grad=False, with eval-mode BN.
Detach $s_0,z,W_u$, replay statistics, target-selection decisions, and ensemble-member selection; keep all rollout states and policy calls connected.
Do not place model/reward/terminal forward evaluation under no_grad: frozen weights must retain their input Jacobians.
Keep $D_\theta\pi_\theta(\hat s_t,z)$ and $\partial_s\pi_\theta$ at every $t=0,\ldots,H$; no detach at the terminal action.
During model fitting update only model weights; during critic fitting detach all target rolls, target actions, rewards, survival weights, and target representations.
The standard FB representation loss still trains online $B$; actor updates never train $B$ through reward inflation.

For $j<t$, the full causal survival derivative is
$$D_{a_j}c_t=\sum_{\ell=j}^{t-1}\left(\prod_{\substack{k<t\\k\ne\ell}}p_k\right)D_{a_j}p_\ell,\qquad D_{a_j}p_\ell=p_{\ell,s}D_{a_j}s_\ell+p_{\ell,a}D_{a_j}a_\ell.$$
At $\ell=j$, $D_{a_j}s_j=0$ and $D_{a_j}a_j=I$; later terms include closed-loop state propagation and policy feedback.
The local frozen-future partial is only $(\prod_{k<t,k\ne j}p_k)p_{j,a}$; using it alone drops downstream hazard changes.
Use multiplicative recurrence rather than division by $p_\ell$, which fails at zero survival.
Hard booleans have zero derivative almost everywhere and undefined boundary derivatives, so their imagined product cannot supply the required survival chain rule.
Actual real terminal masks remain correct for stopped critic targets; imagined soft survival is a differentiable expected-continuation model, not permission to continue after real failure.

**B01 and contact safeguards.** Use the target-$B$ FP64 Gram EMA ($\beta=0.01$, initial $I$, valid batch 1024) and
$$\ell_u=\max(10^{-3},0.05-s_{\min},(s_{\max}-100s_{\min})/99),\qquad W_u=(\widehat\Sigma_u+\ell_u I)^{-1}.$$
Compute $W_uz$ by Cholesky solve; retain B01's split-half threshold 0.15, 200-update hysteresis, and twice-replay-99.9%-leverage cutoff.
Closed gates route the whole command to A; never replace the tail with zero or secretly shorten the objective after seeing its gradient.
Keep raw spherical commands at other whitening sites; refresh z_update by the frozen-BN 50/50 rule without overwriting behavior_z.
Update online BN once on current and once on next batches, then freeze; task $Q$ uses actual executed macro commands/actions.
For short macro truncation $k<K$, use the actual duration, reward, and $\gamma^k$; never label time-limit truncation a physical failure.
Smooth-contact derivatives are local surrogate derivatives; hard impacts require event/saltation treatment or a declared surrogate-bias panel.
Record Jacobian norms, ensemble disagreement, and unclipped gradients; clip actor gradient norm to 10 only for training and report clip frequency.
Finite severe penetration beyond 0.03 m is committed as terminated with zero absorption potential; NaN/Inf, lost contacts, or solver divergence are invalid and halt the panel.
Select the largest admissible horizon only if its held-out measured error/cost criterion improves; otherwise retain A.

## 3. Serious Alternative Considered and Rejected

**Alternative: predict $B$ directly**, $\hat b_{t+1}=T_{\rm lat}(\bar B(m_t),a_t)$, eliminating full-state reconstruction and its cost.
This is attractive because the reward is linear in $b$ and a compact transition may reduce variance and memory.
The method v1.0 §11.5 alternative-analysis requirement is addressed by an explicit impossibility witness and a stated scope of rejection.
Take two states with identical single-frame kinematics $m$ and action $a$, but different observed terrain heights.
One foot hits an obstacle on the next step; the other swings freely, producing $b'_1\ne b'_2$ and possibly different survival.
Because the input pair $(\bar B(m),a)$ is identical, every deterministic $T_{\rm lat}$ must output the same $u$ in both cases.
The triangle inequality proves $\max(\|u-b'_1\|,\|u-b'_2\|)\ge\|b'_1-b'_2\|/2$.
A stochastic latent predictor fits a mixture but cannot choose the conditional mode without the omitted terrain/belief; its conditional transition error remains irreducible.
Hence a B-only Markov world model cannot uniformly reproduce this task family's reward and survival transitions, even with infinite data.
Reject this specific sufficient-state assumption, not latent models generally: augmenting the latent with causal environment/belief variables may remove the obstruction.
The full causal-state model is selected because its residual error can in principle shrink with data; the omitted-variable lower bound cannot.

**Secondary alternative: omit the FB terminal tail.** Its gradient error includes the derivative of every reward at and after $H$.
A system storing $a_0$ and emitting reward only at $H+1$ has zero unbootstrapped head gradient but nonzero $\gamma^H\partial r_{H+1}/\partial a_0$.
This proves no uniform long-horizon guarantee for the tail-free estimator; it remains a useful cost/gradient diagnostic, not the proposed reusable FB architecture.

## 4. Candidate Necessity Claims (Appendix B)

**C-B04-B-01 — direct parameter-path coverage. Necessity grade: Grade 1 (conditional mathematical necessity).**
Premises: differentiability and dominated convergence above; fixed-start objective; exact frozen-policy terminal critic; exact causal dynamics/survival; fixed representation.
Additional premise: $R_{>H}=\mathbb E\sum_{t>H}\gamma^tc_tP_t^\top Q_a$ is nonzero.
Conclusion shape: the frozen-tail hybrid cannot equal $\nabla_\theta J_\infty$; exactness requires representing $R_{>H}$, or a separately justified occupancy/gradient correction.
Proof: $g_\infty-g_H^{\rm oracle}=R_{>H}$; for the one-action FB derivative take $H=0$.
Operational test: compute full autodiff, oracle frozen-tail gradients, and isolated time-indexed policy-parameter injections on paired starts.
Falsifier: an error exceeding $10^{-6}$ relative between the measured gradient difference and summed omitted injections with all premises verified.
Nonzero omitted terms may cancel in expectation, violating the additional premise; an occupancy-weighted actor is outside this claim, not a counterexample.

**C-B04-B-02 — head/tail coordinate compatibility. Necessity grade: Grade 1 (conditional algebraic necessity).**
Premises: full-rank Gram, exact rank-$d_z$ FB factorization, all commands, and reachable one-step expected features spanning $\mathbb R^{d_z}$.
Conclusion: a linear reward head $\bar B^\top Mz$ spliced to unchanged $F^\top z$ is Bellman-consistent for every command only if $M=\Sigma_{\bar B}^{-1}$.
Proof: one-step Bellman subtraction gives $\mathbb E[\bar B(s') ]^\top(M-\Sigma_{\bar B}^{-1})z=0$; both spanning conditions force the matrix to vanish.
Operational test: perturb a nonspherical Gram, verify the one-step splice identity, then compare raw and whitened hybrid objectives and gradients.
Falsifier: a distinct $M$ satisfying every identity under verified spanning and rank premises; finite damping is an explicitly measured approximation.
Neither claim establishes learning speed, safe deployment, or a universal optimal horizon.

## 5. Pre-Registered Empirical Spike Protocol

**Plant and seeds.** Implement in PyTorch FP64 a unit-mass vertical contact plant $s=(q,v)$, timestep $\Delta=0.01$, action $a=20\tanh u$.
Use $d_\tau(q)=\tau\log(1+\exp(-q/\tau))$, $N=k d_\tau(q)+b\,\sigma(-q/\tau)\tau_v\log(1+\exp(-v/\tau_v))$.
Set $v'=v+\Delta(a-9.81+N)$, $q'=q+\Delta v'$, $k=1000$, $b=20$, $\tau=0.005$, $\tau_v=0.1$, and $\gamma=0.97$.
Define exact smooth continuation $p(s,a)=\sigma((q'(s,a)+0.03)/0.003)$, emitted transition reward followed by probabilistic termination.
This integrated-hazard benchmark is distinct from the hard severe-penetration replay panel; compare both, but claim exact gradients only for the smooth benchmark.
Sample 1024 paired test starts with $q\sim U[-0.02,0.20]$, $v\sim U[-1,1]$; split by trajectory and seed, never by overlapping windows.
Use seeds 0–9, a tanh policy MLP $[32,32]$ taking $(q,v,z)$, and four-dimensional spherical commands.
For a controlled coordinate test embed $(q,v)$ in an otherwise zero 229-dimensional motion vector and use $\bar B=2u/\|u\|$, $u=A(\sin q,\cos q,\sin v,\cos v)$.
Use $A=I$ and $A=\operatorname{diag}(1,1,0.2,0.05)$; estimate and report actual Gram eigenvalues on 100,000 independent valid replay samples.
This toy has no claim to humanoid coverage; its only purpose is contact/survival gradient verification.

**Oracle and learned panels.** Compute ground-truth full-policy autodiff through 1024 true steps; repeat at 2048 and require relative gradient change below $10^{-4}$.
If convergence fails, report an unresolved long-horizon reference rather than label either finite gradient exact.
Check 20 seeded parameter-space directions by central differences at $h=10^{-4},10^{-5},10^{-6}$, requiring best relative discrepancy below $10^{-4}$.
Construct the oracle terminal $F^\star$ by accumulating exact feature returns and multiplying by $\Sigma^{-1}$ under detached $\theta_0$ continuation-policy weights.
Retain its state/action input derivatives; do not detach feedback state paths. Differentiate the outer terminal action under online $\theta$.
First use exact $W=\Sigma^{-1}$ and identical oracle twins; then add B01 damping, learned twins, and target lag as separately labeled conditions.
Train the specified learned ensemble on 100,000 real transitions with a fixed 80/10/10 trajectory split, 20,000 updates, no test-based early stopping.
Fit twin FB critics with the real density objective; inspect $C^1$ critic residuals against oracle readouts on held-out states.
Controlled perturbations $\hat f=f+\alpha e_v\sin(v+a/20)$ and $\operatorname{logit}\hat p=\operatorname{logit}p+\beta a/20$ use $\alpha,\beta\in\{0,10^{-4},10^{-3},10^{-2}\}$.
Measure the resulting $\epsilon_s,\epsilon_J,\epsilon_c$ on test tubes; never equate perturbation amplitude with derivative error.
Evaluate A at $H=0$, whitened D and raw-head D at every $H\in\{1,4,8,16,32\}$, and tail-free rollouts with the same starts/noise.
Raw-head D retains $F^\top z$ so it is the intended splice-mismatch control; also include a fully raw-coordinate tail as an objective-change control.
For B/C test all registered $n$, explicitly including 1 and 32; report primary relabeling and separate matched-segment results.

**Metrics, gates, and decisions.** Report gradient cosine, norm ratio, absolute error, relative error $\|\hat g-g_\infty\|/\max(\|g_\infty\|,10^{-8})$, and minibatch gradient variance.
Use 100 independent batches of 64 starts per seed; exclude near-zero reference gradients only from cosine and report their count.
Report paired seed-level bootstrap 95% intervals, model/critic/Jacobian/survival errors, gate routes, contact regime, and measured damping splice error.
Verify C-B04-B-01's injection identity and C-B04-B-02's splice identity before interpreting learning outcomes.
Pre-register a short-horizon win only if some $H\in\{4,8,16\}$ lowers paired MSE by at least 20% against both A and D32, with the paired 95% interval excluding zero.
For the anisotropic panel, whitening succeeds only if paired MSE improves by at least 20% over the raw-head control; otherwise reject that empirical prediction.
Select $H$ using validation only, then lock it for testing; report every tested horizon, including null and adverse results.
Benchmark equal-real-data and equal-total-GPU-second budgets separately, with synchronized CUDA events and wall-clock timing including collection, Gram, model fitting, and backward passes.
Publish environment transitions, imagined transitions, differentiated policy calls, peak memory, updates, and component timing; do not multiply unrelated throughput/sample gains.
Online follow-up budgets are 200,000 real transitions and separately 3,600 GPU seconds per arm/seed, with evaluations every 10,000 transitions or 180 seconds respectively.
Reject any panel with future-reference leakage or numerical corruption; report terminal-mask and survival-detach ablations as deliberate incorrect-gradient controls.
Deliver gradients/metrics and a machine-readable verdict only after execution; this proposal asserts no measured speedup, learned traversal, or ball-striking competence.

