# Candidate (Packet B01): FB Density Factorization, Gram Conditioning, and Intrinsic Reward Identifiability

**Author**: Primary Author A · **Packet**: `B01` · **Method**: v1.0 (`1ce8d1b3…11f7`) · **Ledger inheritance**: `X-BASE-001`..`X-BASE-005`
**Frozen inputs read**: `PROGRAM_CHARTER.md`, `packets/B01/brief.md`, `baseline/01`, `baseline/03`, `baseline/05`. I also read the pinned method's §11.5 and Appendix B for the claim format.
**Evidence status (Charter §2.5)**: Everything below is derivation or a pre-registered protocol. I ran a float64 NumPy check of the closed-form identities in §1 (Eqs. 1.6, 1.8, 1.10 and the tight Kantorovich extremizer), with $d \in \{100, 256\}$ and anisotropic synthetic spectra up to $\kappa \approx 200$. That check verifies only the algebra. It is **not** evidence about FB training, the conditioning of $\Sigma_B$ in this program, or any task outcome.

---

## 0. Notation and Standing Premises

- $d := d_z \in \{100, 256\}$. $D \in \{229, 277\}$ is the motion-descriptor dimension.
- $\rho$ is the FB-replay next-frame distribution: the distribution of the off-diagonal $x$ in the FB loss. Committed `severe_penetration` rows are included. `invalid` rows and expert frames are never included.
- $B(x) \in \mathbb{R}^d$ with $\|B(x)\|_2 = \sqrt d$ for every $x$. $\Sigma := \Sigma_B = \mathbb{E}_\rho[BB^\top] = U\Lambda U^\top$ with $\Lambda = \operatorname{diag}(\lambda_1 \ge \dots \ge \lambda_d \ge 0)$. Spherical projection gives $\operatorname{tr}\Lambda = d$, so the **arithmetic mean eigenvalue is exactly 1**. $\Sigma$ is SPD, so its singular values $\sigma_i(\Sigma_B)$ in the brief are the $\lambda_i$.
- $\kappa := \lambda_1/\lambda_d$. $p_i := \lambda_i/d$. $\operatorname{erank} := \exp(-\sum_i p_i \log p_i)$. $\lambda_H := d / \operatorname{tr}(\Sigma^{-1})$ is the **harmonic-mean eigenvalue**.
- **Successor features of $B$**: $\Psi(s,a,z) := \mathbb{E}[\sum_{t\ge0}\gamma^t B(s_{t+1}) \mid s,a,\pi_z] = \Sigma F(s,a,z)$ (baseline/01 §3.2). Truncated version: $\Psi_H := \mathbb{E}[\sum_{t<H}\gamma^t B(s_{t+1})]$.
- Eigen-coordinates: $\alpha := U^\top z$, $\beta(y) := U^\top B(y)$, $\psi := U^\top \Psi$. For $z$ uniform on $\mathcal S^{d-1}(\sqrt d)$: $\mathbb{E}[\alpha\alpha^\top] = I$.
- **Premise P-FB** (used wherever "exact" appears): the density Bellman equation holds exactly at rank $d$ for the policy under study, and $\Sigma \succ 0$. Learned FB only approximates P-FB. The spike (§5) measures how far the conclusions survive approximation.

---

## 1. Exact Spectral Error and Bias Derivation

### 1.1 Three objects that the brief conflates

For a latent $z$ and the policy $\pi_z$, baseline/01 §4.2 gives
$$
F(s,a,z)^\top z \;=\; \Psi(s,a,z)^\top \Sigma^{-1} z \;=\; \mathbb{E}\Big[\sum_{t\ge 0}\gamma^t\, \underbrace{B(s_{t+1})^\top \Sigma^{-1} z}_{r_z(s_{t+1})}\Big]. \tag{1.1}
$$
So every latent $z$ is a task whose **weight vector in $B$-coordinates** is $w(z) := \Sigma^{-1} z$. This is the only fact the rest of §1 relies on.

For a single goal frame $g$, two different "goal rewards" are in play:

| Name | Per-step reward on $y$ | Prompt $z$ whose $F^\top z$ is its $Q$ | Meaning |
|---|---|---|---|
| **Density (projected-Dirac) reward** | $k_\Sigma(y,g) := B(y)^\top \Sigma^{-1} B(g)$ | $z = B(g)$ | $L^2(\rho)$ projection of $\mathbf 1_{\{y=g\}}/\rho(g)$ onto $\operatorname{span}\{B_i\}$ |
| **Embedding-matching reward** | $k_I(y,g) := B(y)^\top B(g) = d\cos\angle(B(y),B(g))$ | $z = \Sigma B(g)$ | Peaked exactly at $y = g$ on the sphere |

*Proof of the second column.* Apply reward regression (baseline/01 §4.1). For $r = k_\Sigma(\cdot,g) = B^\top(\Sigma^{-1}B(g))$, $\lambda = \Sigma^{-1}B(g)$ and $z_r = \Sigma\lambda = B(g)$. For $r = k_I(\cdot, g)$, $\lambda = B(g)$ and $z_r = \Sigma B(g)$. $\square$

The quantities the brief asks about then line up as follows:

- **Unwhitened single-state goal readout** $F^\top B(g)$ is the *exact* $Q$ of $k_\Sigma(\cdot,g)$. It is exact as a density readout: $F^\top B(g) = m_z(s,a,g)$ under P-FB with $g \in \operatorname{supp}\rho$. It is **not** the $Q$ of the embedding-matching reward. The discrepancy is
$$
F^\top \Sigma B(g) - F^\top B(g) = F^\top(\Sigma - I)B(g) = \Psi^\top(I - \Sigma^{-1})B(g) = \sum_i \psi_i\,\beta_i(g)\,\Big(1-\tfrac{1}{\lambda_i}\Big). \tag{1.2}
$$
- **Unwhitened one-step intrinsic reward** $\tilde r_z(y) = B(y)^\top z$ has discounted return $\Psi^\top z = F^\top \Sigma z$, not $F^\top z$ (§1.3).
- **Exact whitened reward** $r_z(y) = B(y)^\top\Sigma^{-1}z$ has return $F^\top z$ exactly (Eq. 1.1).
- **Exact whitened goal readout**: if the intended goal semantics is "reach $g$" in the embedding-matching sense, the consistent pair is prompt $z = \Sigma B(g)$, read out by $F^\top \Sigma B(g)$, with per-step reward $B(y)^\top \Sigma^{-1}(\Sigma B(g)) = k_I(y,g)$. The correction applied to the *prompt* is $\Sigma$-**colouring**, not $\Sigma^{-1}$-whitening (§1.4).

### 1.2 Cosine alignment error as a function of $\kappa$ (tight)

**Lemma 1 (Kantorovich–Wielandt).** For SPD $A$ with condition number $\kappa$ and any $v \ne 0$:
$$
\cos\angle(v, Av) = \frac{v^\top A v}{\|v\|\,\|Av\|} \;\ge\; \frac{2\sqrt{\kappa}}{1+\kappa}, \tag{1.3}
$$
with equality at $v \propto \sqrt{\lambda_d}\,u_d + \sqrt{\lambda_1}\,u_1$ when $A = \Sigma^{-1}$. The same bound holds with $A = \Sigma$ ($\kappa(\Sigma^{-1}) = \kappa(\Sigma)$). Numerical check: for $d = 100$ with $\kappa = 28.3$, the extremizer gives $0.18799$ against a bound of $0.18799$. For $d = 256$ the extremizer gives $0.10205$ against $0.10205$.

The lemma yields three alignment errors.

1. **Reward-direction error.** In $B$-feature space, $\tilde r_z$ pulls toward $z$ and $r_z$ pulls toward $\Sigma^{-1}z$. Worst case: $\cos \ge 2\sqrt\kappa/(1+\kappa)$.
2. **Reward-function cosine in $L^2(\rho)$**, for a fixed $z$:
$$
\cos_\rho(\tilde r_z, r_z) = \frac{\mathbb{E}_\rho[\tilde r_z r_z]}{\|\tilde r_z\|_\rho\|r_z\|_\rho} = \frac{z^\top z}{\sqrt{z^\top\Sigma z\;\cdot\;z^\top\Sigma^{-1}z}} \;\ge\; \frac{2\sqrt\kappa}{1+\kappa}. \tag{1.4}
$$
   The inequality is Kantorovich's inequality, which is tight. Note that $\mathbb{E}_\rho[\tilde r_z r_z] = z^\top z = d$ **for every $\Sigma$**.
3. **Goal-misidentification angle.** The reward implied by prompt $z = B(g)$ is $k_\Sigma(\cdot,g)$. Over the sphere $\{u: \|u\| = \sqrt d\}$ it is maximized at $u^\star = \operatorname{proj}(\Sigma^{-1}B(g))$, not at $B(g)$. Hence
$$
\theta_{\rm mis}(g) := \angle\big(B(g), \Sigma^{-1}B(g)\big) \le \arccos\frac{2\sqrt\kappa}{1+\kappa}, \qquad \frac{\max_{\|u\|=\sqrt d} u^\top\Sigma^{-1}B(g)}{k_\Sigma(g,g)} = \frac{1}{\cos\theta_{\rm mis}(g)} \le \frac{1+\kappa}{2\sqrt\kappa}. \tag{1.5}
$$
   The right-hand ratio is the **peak-overshoot ratio**: how much more reward a state in direction $u^\star$ would earn than reaching $g$ itself. It is $5.32$ at $\kappa = 28.3$ and $9.80$ at $\kappa = 96$ (both checked numerically). In leverage form: with $\ell(y) := B(y)^\top\Sigma^{-1}B(y)/d$ and $\mathbb{E}_\rho\ell = 1$, Cauchy–Schwarz in the $\Sigma^{-1}$ metric gives $k_\Sigma(y,g) \le d\sqrt{\ell(y)\ell(g)}$. **Self-identification** ($k_\Sigma(y,g) \le k_\Sigma(g,g)$ for all $y$) is therefore guaranteed when leverage is uniform, which holds iff $\Sigma \propto I$ on the sphere. It can fail as soon as some reachable $y$ has $\ell(y) > \ell(g)$ and points toward $\Sigma^{-1}B(g)$.

### 1.3 Value bias and reward MSE: exact spectral formulas

**Reward MSE (exact, $z$-averaged).** For $z$ uniform on $\mathcal S^{d-1}(\sqrt d)$ and $y \sim \rho$:
$$
\mathbb{E}_{z}\mathbb{E}_\rho\big[(\tilde r_z - r_z)^2\big] = \mathbb{E}_z\big[z^\top(I-\Sigma^{-1})\Sigma(I-\Sigma^{-1})z\big] = \sum_{i=1}^d \frac{(\lambda_i-1)^2}{\lambda_i} = \operatorname{tr}(\Sigma^{-1}) - d, \tag{1.6}
$$
using $\operatorname{tr}\Sigma = d$. Normalizing by $\mathbb{E}_z\mathbb{E}_\rho[r_z^2] = \operatorname{tr}\Sigma^{-1}$:
$$
\mathrm{relMSE} = 1 - \lambda_H, \qquad \cos_{\rm pop} := \frac{\mathbb{E}\,\tilde r_z r_z}{\sqrt{\mathbb{E}\tilde r_z^2\,\mathbb{E} r_z^2}} = \sqrt{\lambda_H}. \tag{1.7}
$$
Numerical check ($n = 2\times10^5$ sphere samples, $2000$ random $z$):

| $d$ | Empirical MSE | $\operatorname{tr}\Sigma^{-1} - d$ | Empirical relMSE | $1 - \lambda_H$ |
|---|---|---|---|---|
| 100 | 135.3 | 136.1 | 0.575 | 0.576 |
| 256 | 388.9 | 386.7 | 0.603 | 0.602 |

**$\kappa$ bounds (tight).** Kantorovich applied to the arithmetic/harmonic mean pair on $[\lambda_d, \lambda_1]$, with arithmetic mean 1, gives
$$
\lambda_H \ge \frac{4\kappa}{(1+\kappa)^2} \;\Longrightarrow\; \mathrm{relMSE} \le \Big(\frac{\kappa-1}{\kappa+1}\Big)^2, \quad \cos_{\rm pop} \ge \frac{2\sqrt\kappa}{1+\kappa}. \tag{1.8}
$$
For a single worst-case $z$, the scale-optimal discrepancy is a **lower** bound that no scalar reward rescaling $c$ can remove (Chebyshev):
$$
\min_{c>0}\max_{\|z\|=\sqrt d}\frac{\|(c\Sigma - I)z\|}{\|z\|} = \min_c \max_i |c\lambda_i - 1| = \frac{\kappa-1}{\kappa+1}. \tag{1.9}
$$

**Effective rank: what it does and does not control.** The exact error is a function of $\lambda_H$. $\operatorname{erank}$ is a function of the Shannon entropy of $p$. These are different spectral functionals, and the honest statement has three parts.

1. *Local regime* ($\lambda_i = 1 + \varepsilon_i$, $\sum_i\varepsilon_i = 0$, $\varepsilon$ small). Here $\log(d/\operatorname{erank}) = \tfrac1d\sum_i\lambda_i\log\lambda_i = \tfrac{1}{2d}\sum_i\varepsilon_i^2 + O(\varepsilon^3)$ and $1/\lambda_H - 1 = \tfrac1d\sum_i\varepsilon_i^2 + O(\varepsilon^3)$. Hence
$$
\mathrm{relMSE} \approx 2\log\frac{d}{\operatorname{erank}(\Sigma_B)} \approx 2\Big(1 - \frac{\operatorname{erank}}{d}\Big). \tag{1.10}
$$
   Numerical check: $d = 256$ with $\operatorname{std}(\varepsilon) = 0.1$ gives $0.00997$ versus $0.00968$.
2. *Globally, erank is not a sufficient statistic*, in either direction:
   - **(a) Near-full erank, total error.** Take $\lambda_d = \epsilon \to 0$ with the rest equal. Then $\operatorname{erank} \to (d-1)\cdot(1+o(1))$ but $\operatorname{tr}\Sigma^{-1} \to \infty$, so $\mathrm{relMSE} \to 1$.
   - **(b) Low erank, moderate error.** Take $d = 256$, $\lambda_1 = 128$, and the rest $\approx 0.502$. Then $\operatorname{erank} \approx 32$ but $\mathrm{relMSE} \approx 0.50$.
3. *Consequence for gates.* $\kappa$ (equivalently $\lambda_d$, since $\lambda_d \ge d/(1 + (d-1)\kappa)$) and $\lambda_H$ govern the error. Erank is a **collapse detector**, not an error predictor. §5 gates on all three but derives pass/fail thresholds from $\kappa$ and $\lambda_H$.

**$H$-step value bias** (hybrid of baseline/03 Track 2 with a raw reward and an exact tail $F^\top z$):
$$
b_H(s,a,z) := \underbrace{\mathbb{E}\Big[\sum_{t<H}\gamma^t \tilde r_z(s_{t+1})\Big] + \gamma^H\mathbb{E}[F^\top z]}_{\text{raw hybrid}} - F(s,a,z)^\top z = \Psi_H^\top(I - \Sigma^{-1})z = \sum_i \psi_{H,i}\,\alpha_i\Big(1 - \frac1{\lambda_i}\Big), \tag{1.11}
$$
$$
|b_H| \le \frac{1-\gamma^H}{1-\gamma}\, d\,\max\Big(\frac1{\lambda_d} - 1,\; 1 - \frac1{\lambda_1}\Big) \le \frac{1-\gamma^H}{1-\gamma}\,(d-1)(\kappa-1). \tag{1.12}
$$
The bias is *structural*, not merely numerical. The raw hybrid splices a truncated return of task $w = z$ (the head) onto a tail of task $w = \Sigma^{-1}z$. Its policy gradient is therefore the gradient of **neither** objective. Under P-FB, $b_H$ vanishes for all $(s,a,z)$ iff $\Sigma = I$, or iff the head is whitened.

**Damping bias.** Let $W_\mu := (\Sigma + \mu I)^{-1}$ (I write $\mu$ for $\lambda_{\rm reg}$ below). It shrinks eigendirection $i$ by $\lambda_i/(\lambda_i + \mu)$, i.e. Tikhonov shrinkage. Its $z$-averaged relative MSE against the exact reward is
$$
\epsilon_{\rm damp}(\mu) = \frac{\sum_i \lambda_i^{-1}\big(\mu/(\lambda_i+\mu)\big)^2}{\sum_i\lambda_i^{-1}}, \tag{1.13}
$$
which is bounded by $\big(\mu/(\lambda_d+\mu)\big)^2$. The worst-case direction cosine of $W_\mu$ follows Eq. 1.3 with $\kappa_\mu := (\lambda_1+\mu)/(\lambda_d+\mu)$.

**Why $\mathcal L_{\rm orth}$ alone leaves this error large (mechanism behind H1).** Under spherical projection, $\mathbb{E}\|B\|^2 = d$ is constant, so the second term of $\mathcal L_{\rm orth}$ has **zero gradient**. In expectation the loss reduces to $\tfrac12\operatorname{tr}(\Sigma^2) - d$ (charter normalization). Its excess over the optimum is $\tfrac12\sum_i(\lambda_i-1)^2$, which weights every eigen-deviation equally and **charges at most $\tfrac12$ for a fully collapsed direction**. The reward error (1.6) weights deviations by $1/\lambda_i$ and is **unbounded** as $\lambda_d \to 0$. A TD-fit/orth trade-off that collapses a few low-variance directions is therefore cheap for the loss and expensive for the intrinsic reward. This is a falsifiable mechanism, and §5 S2 measures it.

### 1.4 Why reward regression cancels $\Sigma^{-1}$, and prompts and intrinsic rewards do not

**Reward regression.** $z_r = \mathbb{E}_\rho[B\,r] = \Sigma\lambda$ and $F = \Sigma^{-1}\Psi$, so $F^\top z_r = \Psi^\top\Sigma^{-1}\Sigma\lambda = \Psi^\top\lambda$. The cancellation happens because **both $\Sigma$ factors are second moments of the same $B$ under the same $\rho$**. The $\Sigma$ in $z_r$ comes from averaging $B\,r$ over $\rho$, and the $\Sigma^{-1}$ in $F$ comes from the $\rho$-normalization of the density $m = M/\rho$. Nothing about $\Sigma$ needs to be known.

**Single-frame demonstration prompt** $z_{\exp} = \operatorname{proj}(B(m_{\rm demo}))$. This prompt is a reward-regression encoding only for $r_g = \mathbf 1_{\{\cdot=g\}}/\rho(g)$, which has two consequences.

- (i) It requires $g \in \operatorname{supp}\rho$. Expert frames are never in FB replay (baseline/05 §4), and early in training the 0.704 m demonstration poses are almost surely off-support. So $\rho(g) = 0$ and the density interpretation is void. $B(g)$ is an extrapolation of $B$, and $F^\top B(g)$ is the value of the kernel $k_\Sigma(\cdot,g)$ and nothing more.
- (ii) Even on support, the implied per-step reward is $k_\Sigma(\cdot,g)$. By (1.5) it peaks at $\operatorname{proj}(\Sigma^{-1}B(g))$, not at $g$. No $\rho$-average sits on the prompt side to supply a compensating $\Sigma$. A single frame is a point evaluation, not a moment. The $\Sigma^{-1}$ inside $F$ is left uncancelled, and it rotates the effective goal.

**Multi-step intrinsic reward** $r_z(y)$. A per-step reward is a *pointwise* function of $y$, not a $\rho$-moment. When a method replaces $F$ by an explicit sum $\sum_t\gamma^t(\cdot)(y_t)$ (world-model head, $n$-step targets), the conversion from $\Psi$-space (sums of $B$) to $F$-space requires multiplying by $\Sigma^{-1}$ explicitly (Eq. 1.1). Nothing else supplies it.

**General typing rule** (used in §2.3):
> $B(y)$, $\Psi$, and prompts $z = B(\cdot)$ live in **feature space**. $F$ lives in **dual space**: $F = \Sigma^{-1}\Psi$. A pairing between the two is consistent iff exactly one $\Sigma^{-1}$ separates a feature-space sum from a latent $z$. $F^\top z$ already contains it. $\sum_t\gamma^t B(y_t)^\top z$ lacks it. $z = \Sigma^{-1}B(g)$ inserts a *second* one: its effective weight is $\Sigma^{-2}B(g)$, the misidentification bound worsens to $\arccos(2\kappa/(1+\kappa^2))$, and so **inverse-whitening the prompt is exactly the wrong correction.**

---

## 2. Algorithmic Design for Non-Stationary Online Training

### 2.1 Causal covariance tracker

**State** (all `torch.float64`, registered as buffers, never requiring grad):
`Sigma_hat [d,d]`, `n_upd` (int), `W [d,d]` (float32 copy), `lam [d]`, `U [d,d]`, `mu` (float), `kappa`, `erank`, `lamH`, `fail_count`.

**Initialization.** `Sigma_hat = I_d`. This is the exact $\operatorname{tr} = d$ prior on the sphere. It makes $W^{(0)} = I/(1+\mu) \approx I$, so whitened and raw rewards **coincide at step 0** and diverge only as evidence accumulates. No warm-up switch and no bias correction are needed.

**Update.** This runs once per `FBAgent.update`, after the two BN updates and under the frozen normalizer. It reuses the target forward pass $\bar B := B_{\bar\omega}(m_{\rm next})$ that the FB loss already computes for the off-diagonal targets, so it adds no extra network passes.
$$
\widehat\Sigma^{(t)} = (1-\beta_\Sigma)\,\widehat\Sigma^{(t-1)} + \beta_\Sigma\,\frac1N\,\bar B^\top\bar B, \qquad \bar B \in \mathbb{R}^{N\times d}. \tag{2.1}
$$
Rows: all $N$ rows of the current FB batch's `m_next`. The permutation is irrelevant for a second moment, and the expert pool is excluded by construction.

**Factorization and damped inverse.** I use symmetric eigendecomposition (`torch.linalg.eigh`, float64). Eigh rather than Cholesky, because the damping rule needs $\hat\lambda_1$ and the gates need $\kappa$, $\operatorname{erank}$, and $\lambda_H$.
$$
\widehat\Sigma^{(t)} = \hat U\hat\Lambda\hat U^\top,\quad \hat\Lambda \leftarrow \max(\hat\Lambda, 0),\quad
\mu_t = \max\Big(\mu_0,\ \frac{\hat\lambda_1}{\kappa_{\rm cap}}\Big),\quad
W^{(t)}_\mu = \hat U\,\operatorname{diag}\Big(\frac{1}{\hat\lambda_i + \mu_t}\Big)\hat U^\top. \tag{2.2}
$$
Defaults: $\mu_0 = 10^{-3}$, $\kappa_{\rm cap} = 10^{3}$, so $\kappa(\widehat\Sigma + \mu I) \le \kappa_{\rm cap} + 1$ always, and $\beta_\Sigma = 0.01$ (half-life $\approx 69$ updates). The brief's form $W_\lambda = (\widehat\Sigma_B + \lambda_{\rm reg}I)^{-1}$ is the special case $\mu_t \equiv \lambda_{\rm reg}$. The rule above adds the relative floor $\hat\lambda_1/\kappa_{\rm cap}$, which caps the amplification $\|W\|$ when $\widehat\Sigma$ is rank-deficient early in training.

**Cost.** Per update: the outer product is $N d^2$ MACs ($6.7\times10^7$ at $N = 1024$, $d = 256$), plus eigh at $O(d^3) \approx 1.7\times10^7$ flops in float64. Memory is $2d^2$ doubles plus $d^2$ floats, i.e. ≤ 1.3 MB at $d = 256$.

- If eigh exceeds 2% of update wall-clock (gated in §5 S1), recompute the factorization every $T_{\rm eig} = 10$ updates and reuse the last $W$ in between. This remains causal.
- **Cholesky form.** If diagnostics are not needed at a given step, `L, info = torch.linalg.cholesky_ex(Sigma_hat + mu*I)` followed by `torch.cholesky_solve` is an equivalent $W$-application path.
- **Woodbury is rejected.** Each EMA step is a rank-$N$ update with $N = 1024 > d$, so Woodbury would invert an $N\times N$ matrix and is strictly worse.

**Causality and batch independence.** The whitening used in update $t$ is $W^{(t-1)}$, the factorization computed *before* the current batch is folded in. $W$ is therefore a function of strictly past replay batches, and it is statistically independent of the current minibatch given the history. Eq. 2.1 runs at the **end** of update $t$.

**Estimator accuracy and drift.** The EMA has effective sample size $N_{\rm eff} = N(2-\beta)/\beta \approx 2\times10^5$, an upper bound because replay rows are correlated. In whitened coordinates the relative perturbation is $\|\Sigma^{-1/2}(\widehat\Sigma - \Sigma)\Sigma^{-1/2}\| \approx 2\sqrt{d/N_{\rm eff}}$ for sub-Gaussian rows, about 0.07 at $d = 256$. The resulting relative error of $W$ is of the same order whenever it is $< 1/2$. With $\Sigma$ drifting at rate $\delta$ per update (operator norm), the EMA lag bias is $\approx \delta(1-\beta)/\beta$. $\beta_\Sigma$ trades lag against noise, and it is ablated over $\{0.003, 0.01, 0.03\}$ in §5. The constraint is $\beta_\Sigma \ge \tau_{\rm target}$: $\widehat\Sigma$ must track $\bar B$ at least as fast as $\bar B$ itself moves.

**Integrity checks.** These classify as *numerical corruption* and are never silently repaired.

1. $|\operatorname{tr}\widehat\Sigma - d|/d \le 10^{-4}$. This is an invariant of sphere rows. A violation implies non-finite or unprojected $\bar B$.
2. All entries finite.
3. `eigh` succeeds.

On failure, keep the last good $W$ and increment `fail_count`. If two consecutive failures occur, halt the run as numerical corruption, mirroring Charter §2.4. The tracker is never fed imagined world-model states, expert frames, or `invalid` rows. Committed `severe_penetration` terminal rows *are* in $\rho$ and therefore in $\widehat\Sigma$.

**Checkpoint/resume.** `Sigma_hat`, `n_upd`, `mu`, last-good `W`, and `fail_count` are saved with the agent. Resuming from a checkpoint that lacks them re-initializes `Sigma_hat = I` and logs `sigma_tracker_reinit=True`.

**Reference implementation** (≈40 lines; drop-in buffer module):
```python
class SigmaTracker(torch.nn.Module):
    def __init__(self, d, beta=0.01, mu0=1e-3, kappa_cap=1e3):
        super().__init__()
        self.d, self.beta, self.mu0, self.kcap = d, beta, mu0, kappa_cap
        self.register_buffer("Sigma", torch.eye(d, dtype=torch.float64))
        self.register_buffer("W", torch.eye(d) / (1 + mu0))   # used at the NEXT update
        self.register_buffer("lam", torch.ones(d, dtype=torch.float64))
        self.register_buffer("fail", torch.zeros((), dtype=torch.long))

    @torch.no_grad()
    def update(self, B_bar_next):                       # [N,d], already on sphere, no grad
        X = B_bar_next.to(torch.float64)
        S = (1 - self.beta) * self.Sigma + self.beta * (X.T @ X) / X.shape[0]
        S = 0.5 * (S + S.T)
        ok = torch.isfinite(S).all() and abs(S.trace().item() - self.d) <= 1e-4 * self.d
        if ok:
            lam, U, info = *torch.linalg.eigh(S), 0
            lam = lam.clamp_min(0.0)
            mu = max(self.mu0, lam.max().item() / self.kcap)
            self.Sigma.copy_(S); self.lam.copy_(lam)
            self.W.copy_(((U / (lam + mu)) @ U.T).to(self.W.dtype))
            self.fail.zero_()
        else:
            self.fail += 1
            if self.fail >= 2:
                raise FloatingPointError("SigmaTracker numerical corruption")

    @torch.no_grad()
    def diagnostics(self):
        lam, d = self.lam.clamp_min(1e-12), self.d
        p = lam / d
        return dict(kappa=(lam.max() / lam.min()).item(),
                    erank=torch.exp(-(p * p.log()).sum()).item(),
                    lamH=(d / (1.0 / lam).sum()).item())
```
(`torch.linalg.eigh` raises on failure. Production code wraps it in `try` and routes failures to the same `fail` path.)

### 2.2 Stop-gradient boundaries and target-network interaction

**Which $B$ is tracked.** $\widehat\Sigma$ tracks $\Sigma_{\bar B}$, the **target** network's Gram matrix. The hybrid tail is $\bar F(\cdot)^\top z$, and the $\Sigma^{-1}$ implicit in $\bar F$ is relative to the $B$ it was bootstrapped against, namely $\bar B$ (baseline/01 §2.4 target $\bar m = \bar F^\top\bar B$). The per-step head reward must use the same pair $(\bar B, \widehat\Sigma_{\bar B})$ so that head and tail encode the same task $w = \Sigma_{\bar B}^{-1}z$. Tracking the online $B_\omega$ would mix two gauges whenever $B_\omega \ne \bar B$.

| Tensor | Gradient flows to | Gradient blocked from |
|---|---|---|
| `Sigma_hat`, `W`, `mu` | — (buffers) | everything |
| FB loss (diag + off-diag + $\mathcal L_{\rm orth}$) | $F_\eta$, $B_\omega$ | `W` does not appear: **FB loss unchanged** |
| 1-step actor loss $-\min_k F_{\eta_k}(o,\pi_\theta(o,z),z)^\top z$ | $\theta$ (via $a$) | $F$ params (frozen in the actor step as in UFO), $z$ |
| Hybrid actor head $\sum_{t<H}\gamma^t\bar B(\hat m_{t+1})^\top W z$ | $\theta$ via $\hat m_{t+1}\to\hat s_t, a_t$ (pathwise through $W_\psi$ and $\bar B$ **inputs**) | $\bar\omega$, $\psi$, `W`, $z$, normalizer stats |
| Hybrid tail $\gamma^H\min_k\bar F_k(\hat s_H,\pi_\theta(\hat s_H,z),z)^\top z$ | $\theta$ via $\hat s_H$ and $a_H$ | $\bar\eta$ |
| $z_{\rm update}$ construction | — (`no_grad`) | everything |

**Normalizers.** $\bar B$ is evaluated on predicted descriptors $\hat m$ in eval mode with the BN/normalizer statistics frozen after the two real-data updates. Imagined $\hat m$ never update normalizers or $\widehat\Sigma$, exactly as expert frames never do. The world model must output the 229-/277-D descriptor $\hat m$, either through a predicted head or a differentiable FK. $\bar B$ still receives motion-only input, so Charter §2.3 holds.

**UFO contract preservation** (each item checked by an assertion in code):

1. `behavior_z` is written at macro boundaries from the three-way mixture. The tracker never reads or writes it.
2. BN is updated once on `(obs, m_current)` and once on `(next_obs, m_next)`, then frozen. The tracker update runs after the freeze and reuses the frozen-stat $\bar B(m_{\rm next})$.
3. `z_update` follows baseline/05 §4.3 **verbatim**: 50% $\operatorname{proj}(\mathcal N(0, I))$, 50% $\operatorname{proj}(B_\omega(\tilde m_{\rm next}[\mathrm{perm}]))$. It is not whitened (§2.3 i).
4. The task critic reads `z_actual` only, and the tracker has no path to $Q$ or to $P_\psi$.

### 2.3 Where whitening is and is not applied

| Site | Apply $W_\mu$? | Reason (§1 reference) |
|---|---|---|
| **(i) `z_update` goal relabeling** | **No** | The FB loss is valid for any $z$-distribution. $z_{\rm update}$ selects *which* tasks are trained and is not a reward computation. Whitening it would change the frozen UFO sampler and couple $z$-sampling to a stochastic estimate. Side effect noted, not corrected: the goal half has second moment $\propto\Sigma$, so it over-samples top eigendirections. The uniform half keeps full-sphere support. |
| **(ii) `expert`/`near` rollout encoding** | **No inverse whitening, ever** (Eq. 1.5 and the typing rule: $\Sigma^{-1}$ doubles the misidentification). **Default: unchanged** raw $\operatorname{proj}(B_\omega(m))$ per baseline/05. **Gated option** $\mathsf{C}$: $\Sigma$-colouring $z = \operatorname{proj}(\widehat\Sigma\,B(m))$, with the `near` rotation applied *after* colouring. Adopted only if §5 S4 passes. | Colouring makes the effective per-step reward $k_I(\cdot,m)$, which peaks at the demo frame. It needs no inversion (a matrix-vector product with bounded $\widehat\Sigma$), so it cannot blow up when $\widehat\Sigma$ is singular. The result stays on the sphere and inside $z_{\rm update}$'s support. `behavior_z`/`z_actual` store the coloured vector actually executed, so $Q$ remains consistent. Planner outputs are never transformed. |
| **(iii) low-level actor gradient** $\nabla_\theta F(o,\pi_\theta,z)^\top z$ | **No** | $F^\top z$ already equals the whitened return (Eq. 1.1). $F^\top Wz$ would optimize $w = \Sigma^{-2}z$ and decouple the actor from the FB TD fixed point. |
| **(iv) $H$-step world-model intrinsic reward** | **Yes, mandatory**: $r_z(\hat y) = \bar B(\hat y)^\top W^{(t-1)}_\mu z$ | Without it, the hybrid head and the $\bar F$ tail encode different tasks. The bias is Eq. 1.11 and cannot be fixed by rescaling (Eq. 1.9). The same rule applies to any $n$-step $F$ target (baseline/03 Track 1): $\phi(y) = W\bar B(y)$. |

**Off-support guard for (iv).** If $\widehat\Sigma$ has near-null directions, then for in-support $y$, $\bar B(y)$ has no energy there, so $1/(\lambda_i + \mu)$ multiplies zero. A world model, however, can be driven by the actor toward $\hat y$ whose $\bar B(\hat y)$ has energy in those directions, where the reward is amplified by up to $(\lambda_1 + \mu)/\mu \le \kappa_{\rm cap}+1$. This is a reward-hacking channel.

- **Detection.** Compute the leverage $\ell(\hat y) = \bar B(\hat y)^\top W\bar B(\hat y)/d$. In-support, $\mathbb{E}_\rho\ell = \operatorname{tr}(W\Sigma)/d \le 1$.
- **Guard.** If $\ell(\hat y_t) > 2\,q_{0.999}\{\ell(\bar B(m_{\rm next}))\}_{\rm batch}$, then that rollout branch from step $t$ onward is masked out of $J_H$ and the event is counted. It is not truncated with a tail bootstrap, because $\bar F$ at an off-support state is equally untrustworthy.
- **Gate.** Masked fraction ≤ 1% (§5 S3).

**Degenerate regimes.**

1. *Random-init $B$* is typically strongly anisotropic. $\mu_t \ge \hat\lambda_1/\kappa_{\rm cap}$ bounds $\|W\| \le \kappa_{\rm cap}/\hat\lambda_1$.
2. *Rank-deficient $\widehat\Sigma$* is handled by `clamp_min(0)` plus $\mu_t$. No inverse of a singular matrix is ever formed.
3. *Abrupt $\rho$ shift* (curriculum unlock) triggers a logged step change in $\kappa$. The EMA lag is bounded by the half-life, and the guard catches off-support imagined states during the transition.
4. *Short macro truncation $k < K$ and RNN prefix burn-in* touch only the task critic/planner path, which this proposal does not modify.

---

## 3. Serious Alternative Considered and Rejected (method v1.0 §11.5)

### 3.1 Alternative R1: hard whitening inside the forward pass of $B$ (batch Cholesky/ZCA or Stiefel projection, then sphere)

**Proposal.** $B(x) = \operatorname{proj}_{\sqrt d}\big(L^{-1}(\tilde B(x) )\big)$, where $LL^\top$ is the Cholesky factor of the batch (or running) Gram matrix of the raw head $\tilde B$. Gradients flow through $L^{-1}$, as in Decorrelated BN or IterNorm. The goal is $\Sigma_B = I$ by construction, so no readout correction would be needed.

**Rejection, by four arguments.**

1. **Whitening and spherical projection cannot both hold under a closed-form linear map.** After $L^{-1}$, the batch Gram matrix is $I$, but the rows have norms $\|L^{-1}\tilde B(x)\|^2 = d\,\ell(x)$ with heterogeneous leverage. Re-projecting to the sphere multiplies row $x$ by $\ell(x)^{-1/2}$, giving $\Sigma_{B} = \tfrac1N\sum_x \ell(x)^{-1}v_xv_x^\top$ with $\tfrac1N\sum_x v_xv_x^\top = I$. This equals $I$ iff $\ell$ is constant on the batch, i.e. iff the input already had uniform leverage. Otherwise the composite is not whitened. Achieving both properties requires an iterative alternating scheme (a Sinkhorn-type equal-norm tight-frame problem), which is neither exact nor closed-form per step. The brief's hard constraint keeps the sphere, so R1 cannot deliver what it promises.
2. **It breaks single-frame encoding semantics.** A batch-whitened $B(x;\text{batch})$ depends on co-batch samples, so `encode_motion` on a single `[1, 229]` expert frame is undefined. The only fix is to use running statistics, which is exactly the tracker of §2.1 moved *inside* the representation, plus argument 3's cost.
3. **It turns the free gauge into a moving TD target.** Every update of the internal whitening matrix applies a gauge transform $B \mapsto A_tB$ to *all* $B$ values at once. FB is invariant only if $F \mapsto A_t^{-\top}F$ simultaneously, which TD cannot do: $\bar F$ was fitted to the old gauge. The bootstrap target becomes $\bar F^\top A_t\bar B$, with relative error $\|A_t - I\|$ per step that is unrelated to any Bellman error. This is largest early in training, precisely when $\kappa$ is large and changing. My design leaves $B$'s gauge untouched and corrects only at the readout sites that need it.
4. **Its backward pass is ill-conditioned exactly when it is needed.** $\partial L^{-1}/\partial\Sigma$ scales with $\|L^{-1}\|^2 \sim 1/\lambda_d$, and eigen/ZCA backprop has $1/(\lambda_i - \lambda_j)$ terms, which explode on near-degenerate spectra. Damping restores stability but reintroduces $\Sigma \ne I$, defeating the purpose. Instability of ZCA backprop was the motivation for IterNorm's Newton iterations, which again yield only approximate whitening.

**Conclusion.** R1 violates the brief's "preserve the bilinear interface and spherical norm" (argument 1), breaks single-frame `encode_motion` (argument 2), and injects non-Bellman TD error (argument 3). Rejected.

### 3.2 Alternative R2: adaptive $\lambda_{\rm orth}$ dual ascent without explicit $\widehat\Sigma^{-1}$

**Proposal.** Treat $\|\Sigma_B - I\|_F^2 \le \epsilon$ as a constraint and raise $\lambda_{\rm orth}$ by dual ascent until it is satisfied, so readouts can stay raw.

**Rejection as a replacement.** It is kept as an optional complement.

1. **It controls the wrong functional.** As shown in §1.3, the constrained quantity is $\|\Sigma - I\|_F^2 = \sum_i(\lambda_i - 1)^2$, while the reward error is $\sum_i(\lambda_i-1)^2/\lambda_i$. Take a spectrum with one direction at $\lambda_d = \delta$ and its trace deficit $1-\delta$ spread evenly over the other $d-1$ eigenvalues. Its Frobenius excess is $(1-\delta)^2 + (1-\delta)^2/(d-1) \le d/(d-1)$, bounded for every $\delta$, while its reward error is $\ge (1-\delta)^2/\delta \to \infty$ as $\delta \to 0$. So a constraint $\|\Sigma - I\|_F^2 \le \epsilon$ with $\epsilon \ge d/(d-1)$ certifies nothing about the intrinsic reward. Excluding $\lambda_d \le \delta$ requires $\epsilon < (1-\delta)^2$, which is effectively an eigenvalue-floor constraint, i.e. a $\kappa$ constraint.
2. **Tracking lag under drift.** With $\rho$ drifting so that the target spectrum moves at rate $\delta$ per update, and orth-gradient contraction rate $\eta\lambda_{\rm orth}$, the steady-state constraint violation is $\gtrsim \delta/(\eta\lambda_{\rm orth})$. Making it small requires $\lambda_{\rm orth}\to$ large, which spends $B$'s capacity on whitening low-variance directions instead of the TD fit. This is a direct trade against the successor-measure objective that the charter treats as primary.
3. **Residual is still uncorrected.** Even at $\kappa = 2$, (1.9) leaves a 33% irreducible worst-direction error in raw readouts. Explicit $W$ removes it up to estimator noise, at $O(d^3)$ cost per update and no change to the FB loss.

**Conclusion.** R2 lowers $\kappa$ but cannot certify readout consistency. I keep the frozen $\lambda_{\rm orth}$ and add explicit $W$ at site (iv). An arm with dual ascent *plus* $W$ is registered in §5 as an ablation, not as the mainline.

---

## 4. Candidate Necessity Claims (Appendix B)

All three claims are **Candidate**. Locking needs independent proof check plus the human lead's signature (B.9). No score in §5 can promote them (B.4).

### C-B01-CAND-01: no scalar-calibrated raw intrinsic reward is FB-consistent when $\kappa > 1$ (Grade 1)

- **Premises.**
  - P1: an exact rank-$d$ FB fixed point for $\pi_z$ on a fixed $\rho$ (P-FB).
  - P2: $\Sigma_B \succ 0$.
  - P3: $\{F(s,a,z): (s,a)\}$ spans $\mathbb{R}^d$ for the $z$ considered.
  - P4: per-step rewards of the linear-readout form $r_M(y) = B(y)^\top Mz$, with $M$ independent of $(s,a,y)$.
- **Conclusion.** This has two shapes: an invariant/obligation and a lower bound.
  - **(a) Obligation.** $\mathbb{E}_{\pi_z}[\sum_t\gamma^tr_M(s_{t+1})] = F(s,a,z)^\top z$ for all $(s,a)$ and all $z$ $\iff$ $M = \Sigma_B^{-1}$.
  - **(b) Lower bound.** For $M = cI$ with any $c > 0$ (raw dot product, any reward scale), there exist $z$ and an $(s,a)$-direction with $|F^\top(c\Sigma - I)z| \ge \frac{\kappa-1}{\kappa+1}\|F\|\|z\|$.
  - **(c) Corollary for hybrids.** An $H$-step head with $M \ne \Sigma^{-1}$ spliced to an $F^\top z$ tail has bias $\Psi_H^\top(\Sigma M - I)\Sigma^{-1}z$ (with $M = I$ this is Eq. 1.11). Under P3 it is nonzero for some $(s,a,z)$.
- **Proof sketch.** The return of $r_M$ is $\Psi^\top Mz = F^\top\Sigma Mz$. Equality with $F^\top z$ for all $F$ in a spanning set forces $(\Sigma M - I)z = 0$ for all $z$, hence $M = \Sigma^{-1}$. For (b), $\max_{\|z\|=1}\|(c\Sigma - I)z\| = \max_i|c\lambda_i - 1| \ge \frac{\kappa-1}{\kappa+1}$ (Chebyshev minimax on $[\lambda_d,\lambda_1]$), and P3 lets $F$ align with $(c\Sigma - I)z$.
- **Grade.** Grade 1: elementary linear algebra under explicit premises, and implementation-independent across any method that reads out $F^\top z$ against per-step $B$-rewards.
- **Operational test.** Use a finite **low-rank** MDP ($|S| = 2048$, $P_\pi = \Phi\Xi^\top$ of rank $\le d$, so $M = (I-\gamma P_\pi)^{-1}P_\pi$ has rank $\le d$), with an anisotropic $\rho$. Compute the exact successor measure, form $m = M\,\mathrm{diag}(\rho)^{-1}$, and factorize it exactly at rank $d$ by SVD. Compute both sides of (a)/(b) in float64. The gap must equal the formula to $10^{-8}$ relative.
- **Falsifier.** A construction satisfying P1–P4 where $\sum_t\gamma^t B^\top z = F^\top z$ for all $(s,a)$ with $\kappa > 1$. Such a construction would show an error in the proof.
- **Scope note.** If learned (approximate) FB shows a gap far below the bound, that is a *scope* finding: P1/P3 are not met. It narrows where the claim applies and does not refute it.

### C-B01-CAND-02: single-frame prompts are self-identifying only under isotropic Gram, and the consistent prompt correction is $\Sigma$-colouring (Grade 1)

- **Premises.** P1 and P2 above. Prompt map $z = A\,B(g)$ with $A$ a fixed linear map. Effective per-step reward is Eq. 1.1.
- **Conclusion.** This has two shapes: an impossibility and an invariant.
  - **Impossibility.** For $A = I$, $\sup_g\theta_{\rm mis}(g) = \arccos\frac{2\sqrt\kappa}{1+\kappa}$, which is zero iff $\kappa = 1$. Inverse whitening ($A = \Sigma^{-1}$) has $\sup_g\theta_{\rm mis} = \arccos\frac{2\kappa}{1+\kappa^2}$, which is strictly worse for $\kappa > 1$.
  - **Invariant.** The effective reward is proportional to $k_I(\cdot,g)$ (peaked at $g$ on the sphere) for every $g$ iff $A = c\,\Sigma$.
- **Grade.** Grade 1: Lemma 1 plus the reward-regression identity.
- **Operational test.** Use a closed-form computation on a trained $B$ checkpoint, with no training required. For each $g$ in a held-out pool, measure $\angle(A B(g), \text{argmax direction of } \Sigma^{-1}AB(g))$ and compare it to the bound.
- **Falsifier.** Any $\Sigma \succ 0$ with $\kappa > 1$ for which $A = I$ yields $\theta_{\rm mis} = 0$ for all $g$ in an open set of directions.

### C-B01-CAND-03: a Gram-tracking role is obligatory for hybrid FB + world-model heads (Grade 2, Candidate)

- **Premises.** The competence class is policy optimization that splices an explicit per-step $B$-reward head of length $H \ge 1$ onto a successor-measure tail, under non-stationary $\rho$ where $\Sigma_{B,\rho_t}$ changes over time.
- **Conclusion (functional completeness).** Any such system must realize a role R-Σ: a causal estimate of $\Sigma_{\bar B,\rho}$ (or of its inverse action on $z$) for **the same $B$ that pairs with the tail**, refreshed at least as fast as $\bar B$ drifts. Without R-Σ, C-B01-CAND-01(c) makes the head/tail splice inconsistent whenever $\kappa_t > 1$.
  - *Admissible realizations:* explicit EMA (this proposal), exact orthonormality maintained at all times (a degenerate realization), or a learned linear head trained by reward regression to $\Sigma^{-1}$.
  - *Not admissible:* "the actor will compensate implicitly" with no test.
- **Operational realization test.** Define the **splice residual** $\varepsilon_{\rm splice} := \mathbb{E}\big|r_z(\hat y_1) + \gamma\bar F(\hat s_1, a_1, z)^\top z - \bar F(s_0,a_0,z)^\top z\big| / \mathbb{E}|\bar F^\top z|$ on real one-step transitions. The role is realized if $\varepsilon_{\rm splice}$ with the role is ≤ 0.5× $\varepsilon_{\rm splice}$ with raw $B^\top z$ whenever $\kappa \ge 10$.
- **Falsifier.** A hybrid without any R-Σ realization whose splice residual and policy-gradient cosine (§5 S3) match the whitened arm at $\kappa \ge 30$. That outcome downgrades the claim or adds a premise, such as "$F$ does not span".
- **Upgrade log.** A serious attempt to build such a counterexample is the R2 arm (dual ascent without $W$) in §5. Its failure or success is logged to `upgrade-log.md`.

---

## 5. Pre-Registered Empirical Spike Protocol (`B01-SPIKE-A`)

**Scope disclaimer (Charter §2.5).** This spike tests numerics, estimator behaviour, and readout consistency on synthetic or replay-derived motion descriptors with known ground truth. Passing it proves nothing about obstacle traversal or ball striking.

**Common settings.**

- **Grid.** $d \in \{100, 256\}$, $D \in \{229, 277\}$, seeds $\{0,1,2,3,4\}$, float64 for all ground-truth quantities and float32 for networks.
- **Hardware and runtime.** One GPU. Total budget ≤ 6 GPU-hours.
- **Compute matching.** All arms within a stage share the identical $B$ checkpoints, $z$ samples, start states, and optimizer steps. Arms differ **only** in the readout matrix.

### 5.0 Data: anisotropic, drifting replay distribution

- **Primary (if available).** Real FB-replay `m_next` dumps from existing CPU smoke runs, plus the 859-frame demo descriptors from `prepare_data.py`. These are used as-is, with no filtering.
- **Fallback (always run, for reproducibility).** A seeded synthetic generator on a $D$-dim descriptor. A latent 12-D skill manifold is mapped through a fixed random 2-layer MLP into $\mathbb{R}^D$, with per-block scales matching the 229-D layout: state[67], link pos[54], rot6d[108]. For 277-D the generator adds a 48-D extension block.
- **Mixture.** $\rho_\tau$ is a mixture over three clusters: `stand` (low variance), `fall` (medium), and `traverse` (high variance, rare). The weights drift linearly over $T = 20{,}000$ updates from $(0.85, 0.12, 0.03)$ to $(0.30, 0.20, 0.50)$, with one **abrupt shift** at $\tau = 12{,}000$ (traverse weight +0.15) to emulate a curriculum unlock.
- **Demo proxy.** 859 frames drawn from a fourth, **off-support** cluster (`demo`, adjacent to `traverse`).
- **Dynamics for pathwise tests.** $m_{t+1} = m_t + 0.02\cdot\tanh(A m_t + G a_t)$ with fixed random stable $A$ and $G \in \mathbb{R}^{D\times 29}$. This dynamics is known, smooth, and differentiable, so world-model error is zero by construction and only the reward readout is tested.

### S0: identity verification (closed form, CPU, seconds)

For trained and controlled-$\kappa$ checkpoints, compute the exact $\Sigma$ on $2^{17}$ samples and evaluate Eqs. 1.4, 1.6, 1.8, 1.11, and C-B01-CAND-01/02 (low-rank finite-MDP version from C-B01-CAND-01's operational test, $|S| = 2048$).

- **PASS:** every identity matches to relative error $\le 10^{-6}$ in float64, and every bound holds on $10^4$ random $z$ and $g$ with the tight extremizer attained to $10^{-6}$.
- **FAIL:** a derivation error. Stop and revise §1.

### S1: tracker accuracy, stability, cost

Run the online $B$ from S2 with the tracker attached. Every 100 updates, compare $\widehat\Sigma$ (and $W^{(t-1)}_\mu$) against the exact $\Sigma_{\bar B,\rho_\tau}$ on $2^{16}$ fresh samples. Ablate $\beta_\Sigma \in \{0.003, 0.01, 0.03\}$.

| Metric | PASS threshold (all seeds, both $d$, $\beta_\Sigma = 0.01$) |
|---|---|
| Whitened-frame error $\|\Sigma^{-1/2}(\widehat\Sigma - \Sigma)\Sigma^{-1/2}\|_{\rm op}$ (median, after 2k updates) | $\le 0.15$ |
| Same metric, 95th percentile within 2k updates after the abrupt shift | $\le 0.50$ |
| Trace invariant $\lvert\operatorname{tr}\widehat\Sigma - d\rvert/d$ | $\le 10^{-4}$ at every update |
| `eigh` failures / non-finite $W$ | 0 |
| Tracker wall-clock / FB update wall-clock | $\le 2\%$ (else use $T_{\rm eig} = 10$ and re-test) |

### S2: does $\mathcal L_{\rm orth}$ leave anisotropy under drift? (H1 premise)

Train a miniature FB system on the S0 dynamics: $B$ is MLP $D\to256\to256\to d$ with input normalizer and sphere projection. $F$ is MLP $(D + 29 + d)\to512\to512\to d$, with an actor and the exact UFO $z_{\rm update}$ sampler (50/50, frozen-BN order), for 20k updates at $N = 1024$. Log $\kappa$, $\operatorname{erank}/d$, $\lambda_H$, and $\operatorname{tr}(\Sigma^2) - d$ every 100 updates.

- **H1-premise CONFIRMED** if, in ≥ 4/5 seeds for each $d$, $\kappa \ge 10$ **or** $\lambda_H \le 0.8$ holds for ≥ 20% of the first 20k updates.
- **H1-premise REFUTED** if $\kappa < 3$ and $\lambda_H > 0.95$ hold throughout, in ≥ 4/5 seeds. In that case whitening is recorded as *unnecessary for this regime*: the tracker ships as a diagnostic only and site (iv) stays raw. This is a legitimate negative outcome.
- **Mechanism check (§1.3).** Report the Spearman correlation between $\operatorname{tr}(\Sigma^2) - d$ and $\operatorname{tr}(\Sigma^{-1}) - d$ across checkpoints. Prediction: $< 0.7$, meaning the orth loss is a poor proxy for reward error. Report-only, not gating.

### S3: intrinsic reward, value bias, and policy-gradient cosine

Use the S2 checkpoints plus a **controlled-$\kappa$ sweep**: $B_\kappa(x) = \operatorname{proj}(D_\kappa B_{\rm S2,final}(x))$, where $D_\kappa$ is diagonal and geometrically spaced so the measured $\kappa \in \{1, 3, 10, 30, 100, 1000\}$.

The arms differ only in the readout matrix $M$ inside $r(y) = \bar B(y)^\top Mz$:

| Arm | $M$ |
|---|---|
| `RAW` | $I$ |
| `EXACT` | $\Sigma^{-1}$, float64, from $2^{17}$ samples |
| `W` | $W^{(t-1)}_\mu$ from the tracker |
| `R2` | $I$, with dual-ascent $\lambda_{\rm orth}$ applied during S2 training |

**Reference objective.** $J^\star(\theta) = \sum_{t<400}\gamma^t\,\bar B(m_{t+1})^\top\Sigma^{-1}z$ with $\gamma = 0.98$ ($\gamma^{400} < 3\times10^{-4}$), on the known dynamics. It is the exact long-horizon objective that $F^\top z$ represents.

**Arm objective.** $J_H^M(\theta) = \sum_{t<H}\gamma^t\bar B(m_{t+1})^\top Mz + \gamma^H\,\mathrm{Tail}^\star(m_H)$ with $H \in \{8,16\}$. $\mathrm{Tail}^\star$ is the exact long-horizon tail from $J^\star$, a stand-in for a perfect $\bar F$, so only the head readout differs between arms.

The policy is a linear-tanh policy $\pi_\theta(m, z)$ with 1,024 start states from $\rho$ and 256 $z$ values (50% uniform, 50% goal-encoded, as in $z_{\rm update}$).

Metrics: (a) reward relMSE vs `EXACT` on $\rho$. (b) $H$-step value bias $|J_H^M - J^\star|/|J^\star|$. (c) $\cos(\nabla_\theta J_H^M, \nabla_\theta J^\star)$, median over $z$. (d) off-support guard masked fraction for `W`.

| Gate | Condition (≥ 4/5 seeds, both $d$, both $D$, $H \in \{8, 16\}$) |
|---|---|
| **G1 theory-match** | `RAW` relMSE equals $1 - \lambda_H$ (Eq. 1.7) within 10% relative, and $\cos_\rho \ge 2\sqrt\kappa/(1+\kappa)$ holds on every $z$ |
| **G2 W-fidelity** | `W` relMSE vs `EXACT` $\le 0.05$ for $\kappa \le 100$ and $\le 0.15$ for $\kappa = 1000$ (damping-limited; compare Eq. 1.13) |
| **G3 value-bias reduction** | $\lvert b_H^{\tt W}\rvert \le 0.5\lvert b_H^{\tt RAW}\rvert$ at every checkpoint with $\kappa \ge 10$ |
| **G4 gradient cosine** | $\cos(\nabla J^{\tt W}_H, \nabla J^\star) \ge 0.95$ (median), **and** $\cos^{\tt W} - \cos^{\tt RAW} \ge 0.05$ at every checkpoint with $\kappa \ge 10$ |
| **G5 guard** | masked fraction $\le 1\%$ of rollout steps for `W` |
| **Null control** | at $\kappa = 1$, all arms agree: $\lvert\cos^{\tt W} - \cos^{\tt RAW}\rvert \le 0.01$ and relMSE $\le 10^{-3}$. Failure indicates an implementation bug, not a finding. |

**Decision rule for site (iv).** Adopt $W$ if S0, S1, G1–G5, and the null control all pass, and S2 confirmed the H1 premise. Keep raw (tracker diagnostic only) if S2 refutes the premise. If G2 or G4 fail while S0/S1 pass, the whitening estimator is inadequate: revise $\beta_\Sigma$, $\kappa_{\rm cap}$, or $\mu_0$ in a new version, never in place. The `R2` arm is logged against C-B01-CAND-03's falsifier: if `R2` meets G3 and G4 without $W$ at $\kappa \ge 30$, the Grade-2 claim is challenged.

### S4: single-state self-identification and reachability (decides the colouring option for site ii)

Prompt arms, each paired with its consistent per-step reward:

| Arm | Prompt | Per-step reward |
|---|---|---|
| `RAWPROMPT` | $z = B(g)$ | $k_\Sigma$ |
| `COLOR` | $z = \operatorname{proj}(\widehat\Sigma B(g))$ | $\approx k_I$ |
| `INVWHITE` | $z = \operatorname{proj}(W B(g))$ | — (negative control; predicted worst) |

Goals $g$: 512 held-out on-support frames plus 512 off-support demo-proxy frames. Candidate pool $Y$: $2^{14}$ frames from $\rho$ plus the demo cluster.

1. **Static self-identification** (top-1): the fraction of $g$ for which $\arg\max_{y\in Y} B(y)^\top\Sigma^{-1}z = g$. Also report the median normalized descriptor distance $\|m_{y^\star} - m_g\|/\mathrm{med\,NN}$ and the measured $\theta_{\rm mis}$ against bound (1.5).
2. **Dynamic reachability.** Adam (lr $10^{-2}$, 200 iterations) optimizes an open-loop 32-step action sequence on the known dynamics, maximizing $\sum_t\gamma^t r(m_{t+1})$ with each arm's effective reward. Success is $\min_t\|m_t - m_g\|_{\rm norm} \le 0.1\,\mathrm{med\,NN}$. Report the 95% Wilson lower bound.

| Gate | Condition |
|---|---|
| **G6 prediction ordering** | Static top-1: `COLOR` ≥ `RAWPROMPT` ≥ `INVWHITE` at every checkpoint with $\kappa \ge 10$, in ≥ 4/5 seeds. A violation falsifies the C-B01-CAND-02 operational prediction and triggers re-examination of P1/P2 scope. |
| **G7 adopt colouring** | `COLOR` − `RAWPROMPT` static top-1 ≥ +20 points **and** dynamic-reachability Wilson LB difference > 0 (i.e. ≥ +10 points with $n = 1024$), on both on-support and off-support goals, at the checkpoints where S2 confirmed anisotropy. Otherwise site (ii) stays raw per baseline/05. |

### Reporting and anti-leakage

- **Deposits.** All metrics go to `packets/B01/spikes/B01-SPIKE/` as CSV per (stage, $d$, $D$, seed, checkpoint), along with the seeded data generator, the commit hash of the tracker module, and the unmodified gate table above.
- **No post-hoc changes.** Thresholds may not be edited after the first run. Any change creates `B01-SPIKE-A-v2` with a logged reason.
- **No leakage.** $\bar B$ receives only $D$-dim descriptors. No obstacle height, scan, ball state, phase, or frame index enters any spike computation.
