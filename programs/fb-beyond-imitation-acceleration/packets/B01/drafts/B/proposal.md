# Proposal B (Packet B01): FB Density Factorization, Gram Conditioning, and Intrinsic Reward Identifiability

Author: Primary Author B. Status: independent proposal; all principle claims are **Candidate**. No training or empirical spike results are asserted.

Frozen sources: `PROGRAM_CHARTER.md`, `packets/B01/brief.md`, and baseline 01, 03, and 05 as named in the assignment. Method v1.0 §§11.5, 12.2 and Appendix B were checked against the locally pinned document at `/srv/claude/research/life-sensorimotor-2026-10-22-principle/pinned/orchestrating-ai-research-teams.v1.0-1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7.md`; its SHA256 matches the B01 brief. No competing B01 draft was read or listed. This process has unrestricted filesystem permissions, so behavioral isolation is evidenced by tool calls, not enforced by a read sandbox; under method §11.1, adjudication must remain Provisional unless the orchestrator supplies compliant enforcement evidence. This author neither publishes other drafts nor changes claim states.

**Recommendation.** Preserve the density factorization and its existing command coordinates. Track the target backward map's uncentered Gram matrix and use a damped solve only when converting an FB command into an explicit one-step reward. Do not precondition UFO goal relabeling, demonstration prompts, or the standard actor's final dot product. Enable the hybrid actor only when covariance, damping, and representation-residual diagnostics support the approximation.

## 1. Exact Spectral Error and Bias Derivation

### 1.1 Definitions and the readout distinction that determines the design

Let $d=d_z$, $b_x=B(x)\in\mathbb R^d$, $\|b_x\|^2=d$, and let $\rho$ be the same replay outcome distribution used to define the density factorization. Here “covariance” means the **uncentered** second moment:

$$
\Sigma=\mathbb E_\rho[b_xb_x^\top]=U\Lambda U^\top,
\qquad \Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d),
\qquad \sum_i\lambda_i=d.
$$

Initially assume $\lambda_i>0$, exact factorization, a fixed policy $\pi_z$, and a frozen representation. Write

$$
q=\mathbb E_{\pi_z}\sum_{t\ge0}\gamma^t b_{s_{t+1}}=\Sigma f,
\qquad f=F(s,a,z)=\Sigma^{-1}q.
$$

These are distinct objects: $q$ is a vector of feature returns; $f$ is a vector of density coefficients. The following three values must not be conflated:

| Expression | Meaning under these assumptions |
|---|---|
| $f^\top b_g=q^\top\Sigma^{-1}b_g$ | Correct relative successor density at $g$; also the return of the intrinsic kernel reward $b_y^\top\Sigma^{-1}b_g$ |
| $q^\top b_g=f^\top\Sigma b_g$ | Return of the raw feature-matching reward $b_y^\top b_g$ |
| $f^\top\Sigma^{-1}b_g$ | A different command readout; inserting a second inverse into the density coefficient readout |

For the discrete point reward $r_g(x)=\mathbf1_{x=g}/\rho(g)$, $z_g=\mathbb E_\rho[B(x)r_g(x)]=B(g)$ **exactly**, so baseline 01 §4.2 gives $Q_{r_g}=f^\top b_g$. Thus there is no covariance-induced bias in this single-goal density readout itself. In a rank-limited model it is an approximate density, with representation error that cannot be inferred from the Gram spectrum alone. Continuous-state point queries refer to densities or finite goal neighborhoods, not a positive-probability exact point arrival.

The brief's “unwhitened single-state readout” wording is interpreted as a request to expose these distinctions, not as permission to contradict baseline 01. A properly whitened coordinate pair is

$$
b_x^{\rm w}=\Sigma^{-1/2}b_x,\quad
f^{\rm w}=\Sigma^{1/2}f,\quad
(f^{\rm w})^\top b_g^{\rm w}=f^\top b_g.
$$

Its readout discrepancy is identically zero. These transformed features generally lose the pointwise spherical norm, so this is an analytical identity, not a proposed network change. The exact intrinsic kernel is $k(y,g)=(b_y^{\rm w})^\top b_g^{\rm w}$. It need not be nonnegative or equal the point indicator outside the representable reward subspace, even when its return equals the represented goal value.

### 1.2 Exact eigen-coordinate discrepancies

Use $\hat v=U^\top v$ for eigen-coordinates, keeping policy conditioning $z$ fixed in every comparison. For an arbitrary command,

$$
r_z(y)=b_y^\top\Sigma^{-1}z,
\quad \widetilde r_z(y)=b_y^\top z,
\quad \widetilde r_z-r_z
=\sum_i\hat b_{y,i}\hat z_i(1-\lambda_i^{-1}). \tag{1}
$$

Their exact expected discounted value discrepancy is

$$
\Delta V_z=q^\top(I-\Sigma^{-1})z
=f^\top(\Sigma-I)z
=\sum_i\hat f_i\hat z_i(\lambda_i-1). \tag{2}
$$

Set $z=b_g$ to obtain the raw-kernel goal-return error. For completeness, the literal difference between the requested raw FB readout and a readout with an extra inverse is

$$
f^\top b_g-f^\top\Sigma^{-1}b_g
=\sum_i\hat f_i\hat b_{g,i}(1-\lambda_i^{-1}). \tag{3}
$$

Equation (3) is an exact algebraic discrepancy, **not a correction to the density value**. The extra-inverse readout corresponds to reward $b_y^\top\Sigma^{-2}b_g$ for the same fixed policy. Feeding a transformed command into the policy as well changes the policy, so no same-policy spectral formula alone describes that intervention.

For a fixed command the one-step reward MSE under replay is

$$
E_z=\mathbb E_\rho[(\widetilde r_z-r_z)^2]
=\sum_i\hat z_i^2\frac{(\lambda_i-1)^2}{\lambda_i}. \tag{4}
$$

For independent uniform spherical commands, $\mathbb E[zz^\top]=I$, hence $\mathbb E_z E_z=\sum_i\lambda_i^{-1}-d$. For independent replay-distributed goals $z=b_g$, instead $\mathbb E_g E_{b_g}=\sum_i(\lambda_i-1)^2$. Expert-frame goals need not follow replay, so neither average can be silently substituted for their error.

### 1.3 Cosines, condition number, and effective rank: exact formulas and valid bounds

Define $a=\lambda_{\min}$, $b=\lambda_{\max}$, $\kappa=b/a$, $p_i=\lambda_i/d$, $R=\operatorname{erank}(\Sigma)=\exp(-\sum_i p_i\log p_i)$, and $D=\log(d/R)$. The exact alignment of a raw coefficient and its required dual coefficient is

$$
C(z)=\cos(z,\Sigma^{-1}z)
=\frac{\sum_i\hat z_i^2/\lambda_i}
{\sqrt{\sum_i\hat z_i^2}\sqrt{\sum_i\hat z_i^2/\lambda_i^2}},
\qquad 0\le1-C(z)\le1-\frac{2\sqrt\kappa}{1+\kappa}. \tag{5}
$$

The bound is sharp: a command supported on the extreme eigenspaces with squared mass $a/(a+b)$ in the $a$ eigenspace attains it. One proof treats $1/\lambda_i$ as a random variable weighted by $\hat z_i^2/\|z\|^2$ and uses its bounded support to minimize its mean divided by its root second moment. For projected commands, projection does not repair the angle:

$$
\|\operatorname{proj}(z)-\operatorname{proj}(\Sigma^{-1}z)\|^2=2d[1-C(z)].
$$

Trace normalization gives explicit $\kappa$-only envelopes

$$
a\ge a_\kappa:=\frac{d}{1+(d-1)\kappa},\qquad
b\le b_\kappa:=\frac{d\kappa}{\kappa+d-1}.
$$

Let $\delta=\max_i|\lambda_i-1|$. Since $D=\mathrm{KL}(p\|\mathbf1/d)$, the elementary total-variation/KL bound implies $\delta\le d\sqrt{D/2}$. Therefore define

$$
\epsilon(\kappa,R)=\min\left\{\max(b_\kappa-1,1-a_\kappa),\ d\sqrt{\tfrac12\log(d/R)}\right\}.
$$

Then explicit joint bounds are

$$
|\Delta V_z|\le\epsilon(\kappa,R)\|f\|\|z\|,
\quad |\widetilde r_z-r_z|\le\sqrt d\,\|z\|\epsilon(\kappa,R)/a_\kappa,
\quad E_z\le\|z\|^2\epsilon(\kappa,R)^2/a_\kappa. \tag{6}
$$

The equation (3) magnitude is bounded by $\|f\|\|b_g\|\epsilon/a_\kappa$. If $\epsilon<1$, also apply (5) with $\kappa$ replaced by $\min\{\kappa,(1+\epsilon)/(1-\epsilon)\}$, obtaining an explicit effective-rank-sensitive cosine bound. For larger $\epsilon$ the condition-number bound remains valid.

Effective rank supplies a complementary averaged lower bound. Shannon entropy is at least order-two Rényi entropy, so

$$
\sum_i(\lambda_i-1)^2\ge d^2/R-d,
\qquad
\mathbb E_z E_z\ge\frac{d^2/R-d}{b_\kappa}. \tag{7}
$$

These are bounds, not exact predictions from two summary statistics. Even for the *same* spectrum, an eigenvector command has $C=1$ while an extreme-eigenspace mixture can attain (5); changing $f$ changes the sign or eliminates (2). Also $\Lambda=(\varepsilon,(d-\varepsilon)/(d-1),\ldots)$ has $R\to d-1$ while $\kappa\to\infty$. High $R/d$ alone does not certify invertibility, low variance, or useful gradients. This is especially material at $d=256$.

### 1.4 Why regression cancels, while reward reconstruction does not

For $r(x)=B(x)^\top\lambda$ (here $\lambda$ is a coefficient vector, not an eigenvalue),

$$
z_r=\mathbb E_\rho[B(x)r(x)]=\Sigma\lambda,
\qquad f^\top z_r=q^\top\lambda,
\qquad B(y)^\top\Sigma^{-1}z_r=r(y).
$$

The reward-weighted expectation provides the Gram factor. A single-frame prompt $z_{\rm exp}=\operatorname{proj}(B(m_{\rm demo}))=B(m_{\rm demo})$ supplies no such factor for the *raw feature-matching reward*. That raw reward's correct encoding would be $\Sigma B(m_{\rm demo})$. The prompt already is the encoding of a replay-normalized point preference when the frame is in support, however. Thus “no cancellation for prompts” means that their **per-step reward** is a dual-space kernel, not that their density readout needs another inverse. An out-of-replay-support demonstration is a behavioral prompt only; no exact $1/\rho(g)$ interpretation is available there.

Normalizing a regression vector rescales its value: with $\operatorname{proj}(z_r)=c z_r$, the fixed-policy value becomes $cQ_r$. Changing the policy command may change the policy too. Do not use this rescaling as a reward calibration claim.

### 1.5 Actor gradients, damping, and limits of exactness

For fixed $z$, let $J=D_\theta F(o,\pi_\theta(o,z),z)$, a $d\times n_\theta$ Jacobian with critic parameters frozen. The correct first-action gradient is $g=J^\top z$; the gradient of the raw-reward value is $\widetilde g=J^\top\Sigma z$. With $K=JJ^\top$,

$$
\cos(g,\widetilde g)=\frac{z^\top K\Sigma z}{\sqrt{z^\top Kz}\sqrt{z^\top\Sigma K\Sigma z}},
\quad \|\widetilde g-g\|\le\|J\|\delta\|z\|. \tag{8}
$$

There is no positive gradient-cosine guarantee from $\kappa,R$ alone: take $\Sigma=\operatorname{diag}(1.5,0.5)$, $z=(1,1)$, $J=(1,-2)^\top$; then $g=-1$, $\widetilde g=0.5$ and the cosine is $-1$. For a hybrid rollout, substitute the actual differentiable rollout feature-return Jacobian for $J$ and compare gradients of the same horizon/tail objective. Never compare an $H$-step shared-policy gradient to a first-action derivative as if they were identical.

With the true Gram and damping $\ell=\lambda_{\rm reg}>0$, $W_\ell=(\Sigma+\ell I)^{-1}$:

$$
r_z^\ell-r_z=-\sum_i\hat b_{y,i}\hat z_i\frac{\ell}{\lambda_i(\lambda_i+\ell)},\quad
V_z^\ell-f^\top z=-\sum_i\hat f_i\hat z_i\frac{\ell}{\lambda_i+\ell},\quad
\mathbb E_\rho[(r_z^\ell-r_z)^2]=\sum_i\frac{\ell^2\hat z_i^2}{\lambda_i(\lambda_i+\ell)^2}. \tag{9}
$$

If $\widehat\Sigma=\Sigma+E$, $\|E\|=e<a$, the resolvent identity gives

$$
\|W_\ell-\Sigma^{-1}\|\le\frac{e+\ell}{a(a-e+\ell)}. \tag{10}
$$

Sampling, EMA lag, coordinate drift, and damping are separate error sources. Equation (10) is unavailable when its premise fails, even if Cholesky succeeds.

For approximate factorization, define $h=q-\Sigma f$. Then the exact inverse-reward return is $f^\top z+h^\top\Sigma^{-1}z$. Whitening does not remove $h$ and may amplify it. In singular regimes use the support projector $P=\Sigma\Sigma^+$: $B(y)^\top\Sigma^+z$ identifies only $Pz$. Nullspace coefficients of $F$ are unconstrained by density fitting. Damping gives finite numbers, not recovery of unobserved skills. The inverse-based exact claims require full rank; support-restricted statements require $z\in\operatorname{range}(\Sigma)$ and a specified minimum-norm convention.

## 2. Algorithmic Design for Non-Stationary Online Training

### 2.1 Causal tracker, dimensions, and numerical implementation

Use $d\in\{100,256\}$, $N=1024$, $\beta_\Sigma=0.01$, target-parameter EMA rate $\tau=0.005$, and $\widehat\Sigma_0=I_d$. For a matrix $C_t=[B_{\bar\omega_t}(m'_1),\ldots,B_{\bar\omega_t}(m'_N)]\in\mathbb R^{d\times N}$ of **committed real** next-motion frames, set

$$
\widehat\Sigma_t=(1-\beta_\Sigma)\widehat\Sigma_{t-1}
+\beta_\Sigma C_tC_t^\top/N,\qquad
W_t=(\widehat\Sigma_t+\ell_tI)^{-1}. \tag{11}
$$

All tracker operations are detached. Initialization preserves trace $d$ but creates an explicit, decaying isotropic prior $(1-\beta_\Sigma)^tI$; it is not observational evidence. Do not center features, substitute expert frames, or accumulate imagined frames. Sample from the same marginal $\rho_t$ as the FB density loss; prioritized sampling requires importance weighting to that marginal or a consistent redefinition of $\rho_t$ everywhere.

Accumulate Gram products and EMA in FP64 outside autocast; symmetrize with $(S+S^\top)/2$. For $s_{\min},s_{\max}$ of $\widehat\Sigma_t$, choose the predetermined damping rule

$$
\ell_t=\max\left(10^{-3},\ 0.05-s_{\min},\ \frac{s_{\max}-100s_{\min}}{99}\right). \tag{12}
$$

Thus $\|W_t\|_2\le20$ and $\kappa(\widehat\Sigma_t+\ell_tI)\le100$ in exact arithmetic. Factor $L_tL_t^\top=\widehat\Sigma_t+\ell_tI$ by `torch.linalg.cholesky_ex` and compute $v_z=W_tz$ by `torch.cholesky_solve`; no explicit inverse is necessary. Detach $v_z$ after solving and cast it to the reward computation dtype. Do not normalize $v_z$: normalization would introduce command-dependent reward scaling. On a finite-precision factorization failure, retry once with $10^{-6}I$ added, record the actual total damping, and disable the hybrid step if it still fails. Nonfinite input aborts that update and triggers inspection; it is not repaired by clipping.

Store $O(d^2)$ covariance and factor state (two FP64 matrices: about 156 KiB at 100 and 1 MiB at 256), plus the temporary $O(Nd)$ encodings. Cost is $O(Nd^2+d^3)$ per refresh and $O(d^2)$ per command solve. Dense Cholesky is appropriate at these sizes. The reward uses the solved vector, so each imagined reward costs $O(d)$ beyond the backward-network forward pass. Checkpoint covariance, initialization age, damping, target versions, BN buffers, RNG states, and any gate state; resuming must not reset the covariance prior.

### 2.2 Update order and stop-gradient contract

1. Validate and sample real transitions carrying raw `m_current`, raw `m_next`, observations, applied actions, terminal masks, and immutable `behavior_z`. Reject `invalid` rows before every normalizer/tracker operation. Finite `severe_penetration` final frames remain legitimate samples, including their actual pre-reset next frame.
2. In a statistics-only pass, update online BN **once** on `(obs, m_current)` and **once** on `(next_obs, m_next)`. Use `no_grad`; no optimizer step occurs. Freeze BN running statistics for all remaining forwards. Copy the resulting running buffers once into target modules; target modules never independently train BN. Parameters still use the EMA rule. Record buffer versions because a BN refresh also changes feature coordinates.
3. Under frozen BN and `no_grad`, use **online** $B_\omega$ on a random permutation of replay `m_next`, project to radius $\sqrt d$, and mix with independent uniform-spherical commands using a Bernoulli 0.5 mask. No neighborhood branch is added. Detach the resulting `z_update`.
4. With the current frozen target $\bar B_t$, update (11) from real `m_next` once and compute (12). Freeze the tuple `(target F, target B, target BN, covariance, damping)` for the whole ensuing hybrid objective. The current batch is already observed, so this is causal. The tracker is not advanced on extra loss evaluations.
5. Compute the existing bilinear FB loss with online $F,B$ and `z_update`. Online $F,B$ receive their ordinary gradients, including the original orthogonality loss. Every target Bellman term, including its target action, is evaluated under `no_grad`. Do not insert $W$ into diagonal or off-diagonal density products.
6. For the standard actor update, freeze online $F$ weights and BN while preserving its action-input derivative. Treat `z_update` as constant. Optimize $-\min_k F_k(o,\pi_\theta(o,z),z)^\top z$. Take the scalar dot product per head **before** the minimum; use the active branch subgradient and log ties. Do not wrap this forward in `no_grad`.
7. If the hybrid gate is open, freeze world-model, $\bar B$, and $\bar F$ parameters, but retain derivatives through their **inputs** and every actor call. Initial replay states and commands are detached. Extract predicted root-relative motion $\hat m$ differentiably from the predicted state; compute $\bar B(\hat m)^\top v_z$. Do not detach predicted motion or backward-network outputs. Differentiate neither the solve nor the tracker nor their history. The model receives causal deployable inputs, not future references, obstacle labels in $B$, task phase, or frame indices.
8. After losses and optimizer steps finish, update target **parameters** once with rate $\tau$. Their new coordinates are used on the next update; do not reuse a partially refreshed tuple mid-rollout. The covariance is lagged, not magically transformed by this EMA. Measure that lag as below.

`behavior_z` is never rewritten by these operations. The task critic always uses actual executed macro `z_actual`, or actual applied actions in an action-$Q$ task. No whitened version is substituted into historical task replay.

### 2.3 Exactly where correction enters

| Interface | Decision and reason |
|---|---|
| (i) `z_update` goal relabeling | **No whitening.** Use current online $B$ and the exact UFO 50/50 mixture. Preconditioning would change the command distribution and break the frozen contract. |
| (ii) `expert` / `near` rollout encoding | **No whitening.** Sample valid unindexed frames uniformly; encode online $B$ in eval/no_grad. Preserve the baseline tangent rotation of 10–20 degrees and spherical projection for `near`. Neither geometry filtering nor scene eligibility is introduced. |
| (iii) Standard low-level actor | **No whitening** of the dot-product command in $\nabla_\theta F^\top z$. $F$ already contains the dual factor. Applying $W$ here changes the reward being optimized. |
| (iv) Hybrid explicit intrinsic reward | **Apply the solve**: $r_z(\hat y)=\bar B(\hat m(\hat y))^\top W_tz$. Use target $B$ because both covariance and terminal $\bar F$ are in its coordinate system. Keep the original spherical command as the actor input. |

“Whitening” in (iv) denotes dual conversion by $\Sigma^{-1}$, not replacing $B$ by $\Sigma^{-1/2}B$ inside its forward pass. Expert motion is used solely to select a command; no demonstration tracking or action-MSE objective is added. The source schedule and 100% planner evaluations remain as frozen in baseline 05.

### 2.4 Drift and the damped reward / undamped tail mismatch

Let $\Sigma_t^*=\mathbb E_{\rho_t}[\bar B_t(m)\bar B_t(m)^\top]$. Even unbiased minibatches do not make (11) an unbiased estimate of the *current* matrix when coordinates change. If $\|\Sigma_t^*-\Sigma_{t-1}^*\|\le v$, expected lag is bounded by

$$
\|\mathbb E\widehat\Sigma_t-\Sigma_t^*\|
\le (1-\beta_\Sigma)^t\|I-\Sigma_0^*\|
+\frac{1-\beta_\Sigma}{\beta_\Sigma}v,
$$

plus sampling fluctuations for an individual realization. Target EMA reduces neither replay drift nor BN jumps by theorem. Every 50 updates, use 131072 separately sampled committed frames re-encoded by the **current target** for a calibration Gram; do not update BN or include these diagnostic passes again in the tracker. Record calibration uncertainty by two disjoint half-batches, as well as $\|W_t^{1/2}\Sigma_{\rm cal}W_t^{1/2}-I\|_2$ and the online/target feature discrepancy. Accumulate this calibration in chunks; the large sample is needed to diagnose rare directions rather than confuse an empty small-batch direction with population rank loss. Repeated reuse of the same old encoded vectors is prohibited.

The baseline hybrid objective is

$$
J_H^\ell=\mathbb E\left[\sum_{h=0}^{H-1}\gamma^h\bar B(\hat m_{h+1})^\top W_tz
+\gamma^H\min_k\bar F_k(\hat o_H,\pi_\theta(\hat o_H,z),z)^\top z\right],\quad H\in\{8,16\}.
$$

Its terminal value remains the intrinsic **undamped** FB value. Even with a perfect model and factorization, a damped prefix plus that tail is not an exact Bellman decomposition. Relative to the same hybrid objective with exact $\Sigma_t^{*-1}$ and the same tail, its prefix error is bounded by

$$
|J_H^\ell-J_H^*|\le\frac{1-\gamma^H}{1-\gamma}\sqrt d\,\|z\|\,\|W_t-\Sigma_t^{*-1}\|. \tag{13}
$$

At the true covariance a Bellman-consistent tail for the *damped* reward would instead be $\bar F^\top\Sigma_t^*W_tz$, keeping policy conditioning fixed. Using $\widehat\Sigma_t$ there adds another estimator error and changes the baseline objective. That variant is not silently adopted here. The retained baseline hybrid is explicitly an approximation whose mismatch is measured; the standard actor remains available when it is inaccurate.

Do not enable the hybrid before 500 tracker updates, or when the two calibration halves differ by more than 0.10 relative operator norm, or when either half has $\lambda_{\min}<0.05$, or $\|W_t^{1/2}\Sigma_{\rm cal}W_t^{1/2}-I\|_2>0.50$. Both halves must pass. Also require the spike's reward and gradient gates below, and a held-out normalized feature-return residual $\|q-\Sigma F\|/(\|q\|+10^{-8})\le0.10$ for each critic used as a tail. In real training that residual requires on-policy diagnostic rollouts with a bounded tail estimate; unavailable evidence leaves the hybrid off. Log gate-open fraction, including failures; success conditional on a nearly always closed gate is not acceleration evidence.

On rank deficiency or inadequate coverage, continue ordinary real-transition FB training and the unchanged standard actor; record the limitation rather than claiming recovered nullspace rewards. Use true termination masks to stop intrinsic sums and zero the tail, while time-limit truncation bootstraps from the actual final state. For macro task replay retain actual $k\le K$ and $\gamma_{\rm task}^k$, never substitute $H$ for $k$. RNN history reconstruction and detached prefix burn-in remain necessary for task-$Q$/planner updates; covariance correction does not shorten their history or repair off-policy multi-step trajectories.

## 3. Serious Alternative Considered and Rejected

### 3.1 Hard batch Cholesky / Stiefel projection inside $B$

**Strong version of the alternative.** For each feature minibatch $X\in\mathbb R^{N\times d}$, compute $S=X^\top X/N$ and output $X S^{-1/2}$, or a QR/Stiefel equivalent. This enforces empirical identity Gram whenever $S$ is full rank. It would make raw dot-product rewards correct on that batch and could eliminate a separate reward solve. It is more than increasing a regularization coefficient.

**Why the proposed version is rejected under this packet's contracts.** Three independent counterexamples defeat its claimed guarantee:

1. **Single-frame/batch dependence.** At rollout an expert is encoded as one frame. With $N=1<d$, $\operatorname{rank}(S)\le1$, so exact batch whitening to $I_d$ is impossible. For $N\ge d$, the encoding of a given frame changes when its batch companions change. It is no longer the frozen single-frame map used by collection and replay. A running-statistics substitution restores a single-frame function but abandons exact batch whitening and reintroduces covariance lag.
2. **Spherical normalization is not preserved.** Take $d=2$ and batch rows $\sqrt2e_1,\sqrt2e_1,\sqrt2e_2$. Then $S=\operatorname{diag}(4/3,2/3)$. Whitened squared row norms are $3/2,3/2,3$, not 2. Projecting each row back to radius $\sqrt2$ returns the original batch and its nonidentity Gram. Thus whitening followed by sphere projection does not jointly enforce the two claimed properties. Special tight frames can satisfy both; the counterexample rules out a universal guarantee for replay batches, not their existence.
3. **A forward-only transform breaks the density pairing.** For a constant invertible $A$, retaining density requires $B'=AB$ and $F'=A^{-\top}F$. Changing only $B$ changes Bellman predictions. A batch-dependent $A$ would require coordinated changes to online/target $F$, actor command interpretation, and historical behavior labels. Updating those labels would violate the UFO/task-replay contract. Retaining old labels instead leaves a semantic discontinuity requiring a separate migration design.

These proofs reject *hard batch whitening as a drop-in forward operation*. They do not prove that every globally constrained representation learner is inferior. A jointly trained spherical tight-frame architecture with sufficient support is a legitimate different research program. Here the reward-side solve preserves the current interfaces and exposes its estimation error instead of changing their meaning.

### 3.2 Adaptive orthogonality dual ascent without a reward solve

A second serious alternative updates a multiplier by $\alpha_{t+1}=[\alpha_t+\eta(\|\widehat\Sigma-I\|_F^2-\epsilon)]_+$ and optimizes FB plus $\alpha_t\mathcal L_{\rm orth}$. It could improve representation geometry, so it remains an empirical comparator. It cannot certify correct intrinsic rewards before isotropy has been achieved.

For independent draws under spherical normalization, $\mathbb E[(B(x)^\top B(x'))^2]=\operatorname{tr}(\Sigma^2)$ and the norm term is constant. The population optimum would be $I$ if realizable. But if replay has an atom of probability $p>1/d$, then $\Sigma\succeq p\,b b^\top$ implies $\lambda_{\max}(\Sigma)\ge pd>1$, regardless of the deterministic spherical encoder. With fewer than $d$ distinct frames, rank is at most that count. No multiplier can overcome these information/support constraints. Even when isotropy is feasible, an entirely collapsed normalized encoder has a radial population Gram-loss gradient; spherical projection removes its tangential component. Increasing its multiplier alone does not prove finite-time escape.

Consequently “make orthogonality strong enough and omit the dual conversion at all times” is rejected as a guaranteed solution. Reward-side damping also fails to restore missing support, but it can correct identifiable anisotropic directions immediately, and its failure conditions are explicit. A future bake-off may favor adaptive orthogonality plus a solve; nothing in the theorem forbids that combination. Agreement with the brief on using a covariance tracker counts only as framed agreement under method §11.5, not independent evidence of necessity.

## 4. Candidate Necessity Claims (Appendix B)

### C-B01-B-01 — Unique dual reward for a fixed full-rank FB command

- **State and grade:** Candidate, **Grade 1** (hard necessity under the following premises); not Locked and not a claim that an explicit matrix inverse implementation is necessary.
- **Premises:** A fixed finite outcome space with $\rho(x)>0$; a deterministic feature map with SPD $\Sigma=\mathbb E_\rho[BB^\top]$; exact density factorization for the policies considered; intrinsic rewards restricted to the linear span $r_z(x)=B(x)^\top a_z$. Require the reward encoding to equal the given command for every $z$, equivalently require value equality for a collection of $F(s,a,z)$ vectors spanning $\mathbb R^d$ for each command under examination. The spanning requirement rules out accidental equality on one policy/state pair.
- **Conclusion shape:** **Invariant and obligation:** $\mathbb E_\rho[B r_z]=z$ if and only if $\Sigma a_z=z$, so necessarily $a_z=\Sigma^{-1}z$. Raw coefficients $a_z=z$ work for all commands if and only if $\Sigma=I$. Approximate implementations incur exactly (1)–(4); no choice of network family changes this algebra.
- **Proof:** $\mathbb E_\rho[B(B^\top a_z)]=\Sigma a_z$. Invertibility gives uniqueness. For value equivalence, $f^\top(\Sigma a_z-z)=0$ for a spanning family forces the same vector equality. Conversely that equality implies the correct value for every represented successor vector.
- **Implementation independence:** A linear solve, an implicit learned dual map, an exactly isotropic representation, or exact reward regression can all realize the required functional relation. This is not a necessity claim for EMA, Cholesky, a particular $\beta$, or world models.
- **Operational test:** On exact finite fixtures, solve for $a_z$, measure $\|\Sigma a_z-z\|/\|z\|$, and test rewards and all basis readouts. Require relative residual $\le10^{-10}$ in FP64 for full-rank fixtures with $\kappa\le10^3$; compare to the algebraically predicted raw residual and MSE.
- **Falsifier:** Exhibit an SPD Gram, a command, and coefficients $a_z\ne\Sigma^{-1}z$ satisfying the encoding invariant, or satisfying all spanning value equalities. A singular Gram, a non-spanning query family, an out-of-span reward, or an approximate density fit violates a premise rather than refuting the claim. Finding such cases in actual training limits applicability and must be reported, not hidden by narrowing the statement after the fact.

### C-B01-B-02 — Unobservable latent directions cannot be recovered from replay rewards

- **State and grade:** Candidate, **Grade 1**.
- **Premises:** Same replay measure and deterministic feature interface; $\operatorname{rank}(\Sigma)=r<d$; the only evidence constraining $F$ is its pairing with replay-supported $B(x)$. No additional supervision identifies nullspace coefficients.
- **Conclusion shape:** **Impossibility:** the full readout $F^\top z$ is not identifiable for commands with a nullspace component. Only $Pz$ is identifiable. No damping coefficient creates the missing information.
- **Proof:** If $n\in\ker\Sigma$, then $\mathbb E[(n^\top B)^2]=0$, hence $n^\top B(x)=0$ almost surely. Both $F$ and $F+tn$ have identical replay density predictions for every $t$, while their readouts differ by $t n^\top z$. Pseudoinversion fixes a convention, not an observation.
- **Operational test:** In the rank-16 fixture, perturb every forward prediction by a known null vector and verify unchanged density products but changed null-command readouts. Report support-projected reward error separately from unavailable full-rank error.
- **Falsifier:** A replay-only estimator that distinguishes those two constructed models while all premises and observed products remain identical. New exploration that expands support changes the premises; it is a valid remedy, not a counterexample.

Neither claim may veto another proposal while Candidate. Independent proof checking, adjudicator review, and the human signature required by Appendix B.9 remain outstanding. Benchmark improvements cannot supply those requirements.

## 5. Pre-Registered Empirical Spike Protocol

### 5.1 Question, scope, and registration boundary

**Primary question:** Does a causal target-coordinate Gram solve recover the intrinsic rewards and policy derivatives of the original FB command more accurately than raw dot products under controlled anisotropy and drift, while rejecting singular or overly damped regimes?

This is a self-contained Torch mechanism diagnostic, using synthetic vectors of exactly 229 and 277 motion-feature channels. These vectors have no task labels, reference time, or future information. They are **motion-schema-sized surrogates**, not kinematically valid humanoid recordings. Success establishes algebra, estimator behavior, and gradient consistency. It does not establish learned physical traversal, realistic contact modeling, or acceleration. A physical-data follow-up must use the baseline's actual descriptor extractor and valid replay; dimensional agreement alone is not that validation.

Before execution, the orchestrator must deposit and hash a `spikes/B01-gram/PLAN.md` containing this protocol, a harness implementing it, and dependency versions. This proposal does not claim the harness already exists. The runner may not tune gates after seeing results. Proposed commands, from the program root:

```bash
python3 spikes/B01-gram/verify.py --plan spikes/B01-gram/PLAN.md --device cpu --stage algebra
python3 spikes/B01-gram/verify.py --plan spikes/B01-gram/PLAN.md --device cuda --stage stream
python3 spikes/B01-gram/verify.py --plan spikes/B01-gram/PLAN.md --device cuda --stage gradients
```

Run seeds `1101,1102,1103,1104,1105`, all four $(q,d)\in\{229,277\}\times\{100,256\}$ combinations, one execution per seed/configuration. Maximum two complete attempts: the second is allowed only for a documented harness defect with unchanged mechanism, seeds, and thresholds; retain both attempts. Budget ceiling: 4 GPU-hours and 30 CPU-minutes per complete attempt on one recorded device. A resource overrun is `INCOMPLETE`, not a selective subset pass. The final report includes every cell and all closed-gate intervals.

### 5.2 Fixtures with known answers

**A. Spectral and singular algebra fixtures.** In FP64 build a seeded orthogonal $U$ by QR with a fixed diagonal-sign convention. For $\kappa_0\in\{1,30,1000\}$ define

$$
t_i=\kappa_0^{(i-1)/(d-1)},\quad \lambda_i=d\,t_i/\sum_jt_j,
\quad \rho_i=\lambda_i/d,\quad B(m_i)=\sqrt d\,Ue_i.
$$

Draw $d$ distinct seeded Gaussian prototype descriptors $m_i\in\mathbb R^q$, normalize each to unit norm, and freeze them. The exact Gram is $U\Lambda U^\top$ under the anisotropic replay probabilities $\rho_i$. A separately named stress fixture uses only the first 16 prototypes with positive mass; its true rank is 16. Use 4096 independent spherical commands and 4096 $(f,z)$ pairs. Compute exact weighted MSE over the finite support, rather than using rare sampled states to define ground truth. Evaluate (1)–(10), the extreme-eigenspace cosine witness, both principle claims, and coordinate-pair invariance.

The fixture encoder must accept only the descriptor, not a frame index. For a smooth standalone implementation, set $K_{ij}=\exp(-\|m_i-m_j\|^2)$, $k_j(m)=\exp(-\|m-m_j\|^2)$, solve $KC=V$ with rows $V_i=\sqrt d(Ue_i)^\top$, and define $B(m)=\sqrt d\,k(m)^\top C/\|k(m)^\top C\|$. Check interpolation residual $\le10^{-10}$ and reject ill-conditioned interpolation rather than silently using a pseudoinverse. Prototype indices are simulator bookkeeping only. They are never policy or encoder inputs. This kernel construction is a diagnostic instrument, not a proposed deployed $B$ architecture.

**B. Causal streaming fixture.** For each seed/configuration run 6000 minibatches of $N=1024$ independently sampled real-surrogate descriptors. Updates 0–1999 use $\kappa_0=1$, 2000–3999 use 30, and 4000–5999 use 1000. Change replay probabilities at those boundaries. Rotate the target representation in a fixed plane spanning extreme eigenvectors by 0.0002 radians per update and add a 0.15-radian jump at update 2000. Recompute current $B$ on sampled raw descriptors; do not rotate old stored encodings. This deliberately tests the tracker against prescribed target-coordinate drift rather than assuming that target EMA prevents it. Evaluate current true Gram analytically and the 131072-frame operational calibration every 50 updates. A separate 1000-update rank-16 stream tests rejection. Sample and store all streams once per seed, then replay the identical streams for each arm. For this finite dictionary only, repeated calibration prototypes may be counted and their current encodings evaluated once per distinct descriptor; the weighted Gram must equal the fully expanded sampled Gram. This is an exact computation shortcut, not an oracle replacement for calibration sampling.

**C. Nonorthogonal single-goal reachability and gradients.** Axis-aligned fixtures can make raw goal rewards differ only by a positive scalar for a particular goal, hiding ranking failures. Therefore use a second full-rank dictionary of $d$ prototypes with rows

$$
B(m_i)^\top=\left[\sqrt d\,\frac{(I+0.3R)e_i}{\|(I+0.3R)e_i\|}\right]^\top,
$$

where $R$ is a seeded symmetric Gaussian matrix divided by its spectral norm. Set replay probabilities proportional to $10^{(i-1)/(d-1)}$. Compute its exact Gram directly; it is SPD by construction. Do not reselect $R$ to obtain a favorable result.

Define a finite controlled surrogate with $d$ descriptor states and 29-D actions. With fixed seeded $A\in\mathbb R^{d\times29}$, entries $\mathcal N(0,1/29)$, and unit prototype rows $m_i$, use the exact transition model

$$
P(j\mid i,a)=\operatorname{softmax}_j\left(\log\rho_j+A_j a+0.2m_i^\top m_j\right).
$$

The actor is `Linear(q+d,64) -> Tanh -> Linear(64,29) -> Tanh`, with a fixed seeded initialization. Its input is $(m_i,z)$, and $\gamma=0.9$. The two hidden notions of replay probabilities and transition probabilities must remain separate: the Gram is weighted by the declared replay distribution, not by whichever occupancy happens to arise from the current policy.

For one-step absorbing episodes, $q(i,a)=\sum_jP(j\mid i,a)B(m_j)$ and $F=\Sigma^{-1}q$ are exact. For each of 32 uniformly selected goal states and 16 uniformly selected starts, evaluate the same 256 seeded candidate actions. Compare the maximizer of the raw reward, corrected reward, and $F^\top B(g)$ against the exact maximizer of $P(g\mid i,a)/\rho_g$. Report top-action agreement and normalized regret (oracle gap divided by the range of candidate values, omitting only explicitly logged zero-range cases). This is single-state reachability in the surrogate, not a feature-nearest-neighbor claim or physical success rate.

For gradients, enumerate transitions rather than differentiating sampled categorical states. At each of 32 spherical and 32 single-goal commands, freeze a target policy at initialization, giving $P_0$. With $B$ the $d\times d$ row dictionary, the exact tail feature-return matrix for a current first action is

$$
Q_B^{\rm tail}(\theta)=P_\theta(I-\gamma P_0)^{-1}B.
$$

The inverse continuation is fixed with respect to $\theta$; the terminal first action retains its derivative. Starting from each of 16 states, unroll the distribution $\mu_{h+1}=\mu_hP_\theta$ for $H\in\{1,8,16\}$, accumulate $\gamma^h\mu_{h+1}Bv_z$, and add $\gamma^H\mu_H Q_B^{\rm tail}(\theta)\Sigma^{-1}z$. Compare each arm's autograd vector to this same objective with $v_z=\Sigma^{-1}z$. Separately compare the standard first-action derivative of $F^\top z$ to the exact one-step oracle. Do not conflate these two gradient tests. This exact finite model removes learned-world-model error from the covariance experiment.

Obtain streaming estimates for fixture C using a further fixed 2000-update stationary stream with $N=1024$, the same tracker and per-seed generator; evaluate at updates 1000 and 2000. No goal or action candidate is selected after viewing a metric. A zero oracle-gradient norm below $10^{-10}$ is logged as undefined cosine and evaluated by absolute gradient error instead; undefined cases exceeding 5% fail the gradient panel.

### 5.3 Arms, implementation checks, and compute controls

| Arm | Reward coefficient $v_z$ | Purpose |
|---|---|---|
| RAW | $z$ | Frozen-baseline raw-dot-product null |
| ORACLE | $\Sigma_t^{*-1}z$ | Exact reference, never deployable evidence |
| ORACLE-DAMP | $(\Sigma_t^*+\ell_tI)^{-1}z$ | Isolates damping from estimation |
| EMA-DAMP (proposal) | $(\widehat\Sigma_t+\ell_tI)^{-1}z$ | Causal implementable intervention |
| DIAG-DAMP | $(\operatorname{diag}\widehat\Sigma_t+\ell_tI)^{-1}z$ | Tests whether off-diagonal structure matters |
| STALE-DAMP | Previous stage's end-of-stage full solve, held fixed in the next stage | Tests adaptation rather than mere invertibility |

At the first stage, STALE-DAMP uses $I$ until an end-of-stage snapshot exists. All arms use the same features, policies, commands, sampled data, tail, and damping value from the full tracker; no separate representation learning creates a confound. Singular fixtures omit the undefined full ORACLE and use a separately labeled support oracle. Execute unused full-Gram computations in RAW and DIAG-DAMP to match diagnostic computational budgets; also report their natural uncushioned runtime separately. Equal minibatches and actor evaluations do not imply equal elapsed time.

Core Torch operations, with row-major encoded batch `b` of shape `[N,d]`, are fixed as follows:

```python
with torch.no_grad(), torch.autocast(device_type=device.type, enabled=False):
    b = target_B(m_next).to(torch.float64)  # target_B in eval mode
    gram = b.T @ b / b.shape[0]
    sigma.mul_(0.99).add_(gram, alpha=0.01)
    sigma.copy_(0.5 * (sigma + sigma.T))
    eig = torch.linalg.eigvalsh(sigma)
    reg = max(1e-3, 0.05 - eig[0].item(),
              (eig[-1].item() - 100 * eig[0].item()) / 99)
    L = torch.linalg.cholesky(sigma + reg * eye64)
    v = torch.cholesky_solve(z.detach().double().T, L).T.detach()
# Freeze target_B parameters, not its input derivatives.
b_imagined = target_B(predicted_motion)
reward = (b_imagined * v.to(b_imagined.dtype)).sum(-1)
```

The complete harness must implement the logged retry and rejection rules, not omit them because the pseudocode shows the successful branch. A separate deterministic contract fixture uses the actual update ordering in §2 with BN counters and immutable replay sentinels: exactly two statistics passes, zero expert/imagined/target BN updates, zero gradients into covariance/target parameters, nonzero input gradients through predicted motion, byte-identical stored behavior labels, and the original online-$B$ 50/50 sampling procedure. Save/restore at update 2173 and require the next 100 covariance/solve outputs to agree with uninterrupted execution to FP64 tolerance on the same deterministic backend. One of the finite failure rows is labeled `severe_penetration` and retained; an injected nonfinite row is rejected before any statistics change. This checks data plumbing, not simulator correctness.

### 5.4 Metrics and numerical pass/fail gates

All comparisons use the current exact Gram for fixture ground truth. Report true and estimated **undamped** $\kappa,R$, damping, $\|W\|$, and the effective metric $C_t=W_t^{1/2}\Sigma_t^*W_t^{1/2}$. A lower condition number of $C_t$ does not mean the learned representation's Gram improved. For positive eigenvalues define $R(C_t)$ using eigenvalues normalized by their actual sum; do not assume trace $d$. Rank-zero eigenvalues contribute $0\log0=0$ and make condition number infinite.

Reward metrics are absolute MSE and normalized MSE $\mathbb E[(r_{\rm arm}-r_*)^2]/\max(\mathbb E[r_*^2],10^{-12})$, computed over exact finite replay weights and held-out commands. Gradient metrics are cosine, relative norm error, sign-reversal frequency, and absolute error for near-zero oracle gradients. Report distributions, not only the cosine of averaged gradients.

| Gate | Preregistered rule |
|---|---|
| Algebra and premise validation | Spherical norm and trace relative errors $\le10^{-10}$; equations (1)–(4), (9), and invariant readouts relative errors $\le10^{-10}$ in FP64. For nonzero denominators use $\max(1,|\mathrm{reference}|)$ in relative scalar residuals. No bound violations exceeding $10^{-10}$. Spectral fixture true $\kappa$ within 1% of its specified value and $R$ within $10^{-8}$ of its analytic value. |
| Tracker on full-rank easy/moderate stages | On the last 500 updates of the $\kappa_0=1,30$ stages, median $|\log(\widehat\kappa/\kappa^*)|\le\log1.25$ and median $|\widehat R-R^*|/d\le0.03$. Report 95th percentiles and all transient samples too. |
| Corrected metric | On those same windows, at least 95% of checkpoints have $\kappa(C_t)\le2$ and $R(C_t)/d\ge0.98$. There is no requirement that the original anisotropic Gram become isotropic. |
| Intrinsic reward error | EMA-DAMP normalized MSE $\le0.02$ in both easy/moderate late windows. In the moderate window it must also be $\le0.25$ of RAW MSE. In the isotropic window RAW is the no-benefit null: corrected normalized MSE may exceed RAW by at most 0.02. |
| Drift recovery and usability | Following the update-2000 shift, all moderate-stage tracker, metric, and reward gates must recover by update 2500, and remain satisfied at at least 95% of later checkpoints through 3999. Operational gate-open fraction on updates 2500–3999 must be $\ge0.80$. |
| First-action gradient correctness | Analytic standard $F^\top z$ gradient agrees with the oracle to relative norm error $\le10^{-8}$ in FP64. RAW's discrepancy must match its analytical $J^\top(\Sigma-I)z$ expression to that tolerance. |
| Hybrid gradient accuracy | In fixture C at both evaluation times, every $H$ must have median EMA-DAMP/oracle cosine $\ge0.98$, fifth percentile $\ge0.90$, median relative norm error $\le0.10$, and sign reversals in $<1\%$ of valid cases. Report RAW alongside it, including cases where RAW already passes. |
| Single-goal reachability | Fixture C EMA-DAMP top-action agreement $\ge95\%$, median normalized regret $\le0.01$, and agreement improves by at least 5 percentage points over RAW. If RAW already has $\ge95\%$ agreement, label the benefit hypothesis unsupported on this panel, rather than discarding that seed. ORACLE and exact $F^\top B(g)$ agree to numerical precision. |
| Severe anisotropy and rank deficiency | All solves finite, gain $\le20(1+10^{-6})$, regularized condition number $\le100(1+10^{-6})$. The rank-16 fixture is flagged unsupported within the first diagnostic interval after the 500-update warmup and never certified full-rank thereafter. No accuracy pass is claimed against a nonexistent full inverse. At $\kappa_0=1000$, report bias even when stable; any checkpoint violating the calibration thresholds must keep the operational hybrid gate closed. |
| Contract | All BN, stop-gradient, replay immutability, terminal-boundary, and same-device resume assertions pass. One contract failure fails the proposal's implementation check. |

The full mechanism spike passes only if algebra/stability/contract gates pass for **all** cells and the tracker/reward/gradient/reachability/usability gates pass in at least four of five seeds **separately for every** $(q,d)$ combination. Any failing cell stays in the report. Also give paired seed differences and bootstrap 95% intervals with 10,000 seed-level resamples; these intervals describe uncertainty and do not override the fixed pass rule. The deliberate rank-deficient regime is a rejection test, not an omitted failure. A failure of the reachability improvement gate can coexist with correct algebra; it rejects the claimed practical benefit on that fixture.

### 5.5 Output artifacts, confounds, and decision use

The runner writes `config.json`, `environment.txt`, `runs.log`, per-checkpoint `metrics.jsonl`, per-command reward/gradient records, prototype/stream tensors and hashes, `verdict.json`, and `deviations.md` inside the registered spike directory. Each verdict includes every denominator, seed, gate, maximum attempt count, and failure reason. No scalar score averages away a contract failure. No results are presently available.

This diagnostic deliberately uses exact finite dynamics and controlled encoder drift. It isolates covariance correction but does not test whether a learned world model or learned $F$ has sufficiently accurate derivatives, whether orthogonality training actually produces the posited spectrum, or whether humanoid motion aliasing prevents task success. The proposed gates therefore authorize, at most, a subsequent preregistered integration study. That study must record genuine 229-D/277-D replay spectra, learn $F,B$ from scratch with the frozen contracts, preserve identical replay and compute budgets across reward arms where possible, and evaluate held-out real-policy returns and contact failures. No transfer from this numerical spike to physical task success, multi-seed superiority, or a necessity lock is asserted.

