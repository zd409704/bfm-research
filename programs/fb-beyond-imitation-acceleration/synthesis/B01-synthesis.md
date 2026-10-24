# Synthesis B01 — FB Density Factorization, Gram Matrix Conditioning, and Intrinsic Reward Identifiability

- **Packet ID**: `B01`
- **Decision ID**: `D-B01-001`
- **Lead Track**: Proposal B (`codex` `gpt-6-astra`, `85.5/100`) merged with Proposal A (`claude` Opus, `74.5/100`) and Cross-Family Reviews/Adjudications (`agy` `gemini-4-argon-high` + `claude` `sonnet`).
- **Empirical Verification**: `packets/B01/spikes/B01-SPIKE/VERDICT.json` (`PASS`).

---

## 1. Unified Mathematical Theory of FB Coordinate Systems

Let $(\mathcal{X}, ho)$ be the valid replay outcome distribution (including committed `severe_penetration` failure transitions and excluding `invalid` numerical corruption rows), and let $B: \mathcal{X} 	o \mathcal{S}^{d_z-1}(\sqrt{d_z})$ be the single-frame root-relative backward representation ($D \in \{229, 277\}$) satisfying $\|B(x)\|_2^2 = d_z$. Its Gram covariance is
$$\Sigma_B = \mathbb{E}_{y \sim ho}[B(y)B(y)^	op], \qquad \operatorname{tr}(\Sigma_B) = \mathbb{E}_ho[\|B(y)\|_2^2] = d_z.$$
Let $\Psi(s,a,z) = \mathbb{E}^{\pi_z}\left[\sum_{t=0}^\infty \gamma^t B(s_{t+1}) \,\middle|\, s_0=s, a_0=aight]$ denote the discounted feature occupancy vector. Under rank-$d_z$ successor-measure density factorization $m^{\pi_z}(s,a,y) pprox F(s,a,z)^	op B(y)$, the population least-squares minimizer satisfies
$$\Psi(s,a,z) = \Sigma_B F(s,a,z) + h(s,a,z),$$
where $h(s,a,z) = \Psi(s,a,z) - \Sigma_B F(s,a,z)$ is the representation-factorization residual ($h \equiv 0$ at an exact rank-$d_z$ fixed point).

### 1.1 Three Distinct Readouts and Their Exact Dependence on $\Sigma_B$

| Readout Type | Formula | Exact Value under $\Psi = \Sigma_B F + h$ | Requires Explicit $\Sigma_B^{-1}$? |
|---|---|---|---|
| **1. Zero-shot linear task reward** $r(y) = B(y)^	op \lambda$ | $z_r = \mathbb{E}_ho[B(y)r(y)] = \Sigma_B \lambda$, value $F(s,a,z)^	op z_r$ | $\Psi(s,a,z)^	op \lambda - h(s,a,z)^	op \lambda$ | **No** ($\Sigma_B^{-1}$ inside $F$ and $\Sigma_B$ inside $z_r$ cancel identically) |
| **2. In-support single-frame goal density** $r_g(y) = rac{\mathbf{1}_{y=g}}{ho(g)}$ | $z_g = \mathbb{E}_ho[B(y)r_g(y)] = B(g)$, value $F(s,a,z)^	op B(g)$ | $\Psi(s,a,z)^	op \Sigma_B^{-1} B(g) - h^	op \Sigma_B^{-1} B(g)$ | **No** ($z_g = B(g)$ is already the exact dual density prompt) |
| **3. Explicit per-step intrinsic reward** $r_z(y) = B(y)^	op v_z$ in $H$-step rollouts | $\mathbb{E}^{\pi_z}\left[\sum_{t=0}^\infty \gamma^t B(s_{t+1})^	op v_zight]$ | $F(s,a,z)^	op (\Sigma_B v_z) + h^	op v_z$ | **Yes, mandatory**: $v_z = \Sigma_B^{-1} z$ is required so $\Sigma_B v_z = z$ matches the terminal bootstrap $F^	op z$ |

### 1.2 Exact Error Bounds When $\Sigma_B 
eq I_{d_z}$

1. **Per-step intrinsic reward discrepancy**: Comparing raw inner-product reward $	ilde{r}_z(y) = B(y)^	op z$ against the FB-consistent intrinsic reward $r_z^*(y) = B(y)^	op \Sigma_B^{-1} z$:
   - For uniform spherical commands $\mathbb{E}[zz^	op] = I_{d_z}$, the normalized MSE and population cosine are governed by the **harmonic-mean eigenvalue** $\lambda_H = d_z / \operatorname{tr}(\Sigma_B^{-1})$:
     $$\mathrm{NMSE}_{\mathrm{unif}} = rac{\mathbb{E}_{z, y\simho}[(	ilde{r}_z(y) - r_z^*(y))^2]}{\mathbb{E}_{z, y\simho}[r_z^*(y)^2]} = 1 - \lambda_H = 1 - rac{d_z}{\sum_{i=1}^{d_z} \lambda_i^{-1}}, \qquad \cos_{\mathrm{pop}} = \sqrt{\lambda_H}.$$
   - For a specific command $z$, the Kantorovich inequality yields the tight lower bound:
     $$\cos_ho(	ilde{r}_z, r_z^*) = rac{\|z\|_2^2}{\sqrt{(z^	op \Sigma_B z)(z^	op \Sigma_B^{-1} z)}} \ge rac{2\sqrt{\kappa(\Sigma_B)}}{1 + \kappa(\Sigma_B)}.$$
2. **Why $\mathcal{L}_{\mathrm{orth}}$ leaves severe inverse anisotropy (Mechanism of Charter H1)**:
   - Under spherical normalization $\|B(x)\|_2 = \sqrt{d_z}$, the expected orthogonality penalty $\mathcal{L}_{\mathrm{orth}} = rac{1}{2}\mathbb{E}_{x,x'}[(B(x)^	op B(x') - d_z \delta_{xx'})^2]$ is proportional to $\|\Sigma_B - I_{d_z}\|_F^2 = \sum_{i=1}^{d_z} (\lambda_i - 1)^2$.
   - A nearly collapsed eigendirection $\lambda_{d_z} = \delta \ll 1$ contributes at most $(1-\delta)^2 < 1$ to $\|\Sigma_B - I_{d_z}\|_F^2$, whereas its contribution to the intrinsic reward error $\sum_i (\lambda_i - 1)^2/\lambda_i$ scales as $(1-\delta)^2/\delta 	o \infty$.
3. **Exact $H$-step hybrid Bellman splice bias**:
   - Splicing an $H$-step world-model head with linear reward matrix $M$ onto a terminal FB bootstrap $\gamma^H ar{F}(\hat{s}_H, \pi_	heta(\hat{s}_H, z), z)^	op z$ produces the exact Bellman splice discrepancy:
     $$b_H(s,a,z) = \Psi_H(s,a,z)^	op (M - \Sigma_{ar{B}}^{-1}) z - \gamma^H h(\hat{s}_H, a_H, z)^	op \Sigma_{ar{B}}^{-1} z,$$
     where $\Psi_H(s,a,z) = \mathbb{E}\left[\sum_{t=0}^{H-1} \gamma^t ar{B}(\hat{m}_{t+1})ight]$. Setting $M = W_t pprox \Sigma_{ar{B}}^{-1}$ eliminates the first term up to damping and tracker lag.
4. **Nullspace non-identifiability (`C-B01-B-02`)**:
   - When $\operatorname{rank}(\Sigma_B) = r < d_z$, any $n \in \ker(\Sigma_B)$ satisfies $n^	op B(x) = 0$ $ho$-a.s., so $F$ and $F + tn$ produce identical replay inner products $F^	op B(x)$ while differing by $t(n^	op z)$ on $F^	op z$. Only the support projection $P z = \Sigma_B \Sigma_B^+ z$ is identifiable from replay density training.

---

## 2. Concrete Algorithm Specification & UFO Contract Integration

### 2.1 Causal Target-Coordinate Gram Tracker & Dual-Bound Damping
- Track the Gram matrix of the **target** backward network $ar{B}$ in FP64 under `torch.no_grad()` and `eval()` mode (after the two-pass online BN statistics update and freeze), once per update on valid committed `m_next` batches ($N=1024$):
  $$G_t = rac{1}{N}\sum_{i=1}^N ar{B}_t(m_{\mathrm{next}, i})ar{B}_t(m_{\mathrm{next}, i})^	op, \qquad \widehat{\Sigma}_t = \operatorname{sym}\!\left((1-eta_\Sigma)\widehat{\Sigma}_{t-1} + eta_\Sigma G_tight), \quad \widehat{\Sigma}_0 = I_{d_z}, \quad eta_\Sigma = 0.01.$$
- Compute extreme eigenvalues $s_{\min} = \max(\lambda_{\min}(\widehat{\Sigma}_t), 0)$ and $s_{\max} = \lambda_{\max}(\widehat{\Sigma}_t)$, and apply the **dual-bound Tikhonov damping rule**:
  $$\ell_t = \max\!\left(10^{-3},\ 0.05 - s_{\min},\ rac{s_{\max} - 100 s_{\min}}{99}ight), \qquad W_t = (\widehat{\Sigma}_t + \ell_t I_{d_z})^{-1}.$$
  This guarantees $\|W_t\|_2 \le 20$ and $\kappa(\widehat{\Sigma}_t + \ell_t I_{d_z}) \le 100$ for every PSD matrix $\widehat{\Sigma}_t$.
- Factorize $\widehat{\Sigma}_t + \ell_t I_{d_z} = L_t L_t^	op$ via FP64 Cholesky and solve $v_z = \operatorname{cholesky\_solve}(z, L_t)$ in $O(d_z^2)$ per command without materializing an unstable inverse.

### 2.2 Four-Site Whitening & Stop-Gradient Contract
1. **Site (i) `z_update` relabeling**: **No whitening**. Keep 50% $\operatorname{proj}_{\sqrt{d_z}}(\mathcal{N}(0,I))$ + 50% $\operatorname{proj}_{\sqrt{d_z}}(B_\omega(m_{\mathrm{next}}[\mathrm{perm}]))$ under frozen BN.
2. **Site (ii) `expert`/`near` rollout encoding**: **No whitening**. Keep raw $\operatorname{proj}_{\sqrt{d_z}}(B_\omega(m_{\mathrm{demo}}))$ and 10–20° tangent rotation for `near`. Never overwrite `behavior_z`.
3. **Site (iii) 1-step low-level actor**: **No whitening**. Maximize $\min_{k \in \{1,2\}} (F_k(o, \pi_	heta(o,z), z)^	op z)$ with scalar inner product computed **before** $\min$.
4. **Site (iv) $H$-step world-model hybrid rollout**: Apply $r_z(\hat{y}_h) = ar{B}(\hat{m}_{h+1})^	op W_t z$ with `stop_grad` on $W_t$, $z$, and $ar{B}$ weights while preserving pathwise gradients $\partial ar{B}(\hat{m}_{h+1}) / \partial \hat{m}_{h+1}$ into the world model and policy $\pi_	heta$.
5. **Per-Command / Per-State Leverage Routing & Gate Hysteresis**:
   - Monitor state leverage $\ell(\hat{y}_h) = ar{B}(\hat{y}_h)^	op W_t ar{B}(\hat{y}_h)/d_z$ and command gain $g(z) = z^	op W_t z / d_z$.
   - If any rollout state exceeds $2	imes$ the 99.9th percentile of replay leverage or if the whitened split-half gate $\|W_t^{1/2}(\Sigma_{(1)} - \Sigma_{(2)})W_t^{1/2}\|_2 \le 0.15$ is closed (with 200-update dwell-time hysteresis), route the actor update for that command cleanly to the 1-step standard FB actor objective rather than zero-tail truncation.
