# Candidate Q (Packet B03): Rank-16 Bilinear Bottleneck Across 144 Morphology-Stroke Regimes and Orthonormalization Regularization

- **Packet**: `B03` · **Role**: Primary Author A · **Method Version**: v1.0 (`1ce8d1b3…11f7`)
- **Inherited ledger**: `X-BASE-001`..`X-BASE-005`; decisions `D-B01-001` (causal $p_{5065}$ partition), `D-B02-001` (E0–E4 generator, 720-cell coverage gate, dual-partition normalizer).
- **Fixed constraints honored**: $d_z = 16$; deployed budget `281,617` = `74,000` ($B_\omega$) + `207,617` ($\pi_\theta$), unchanged; $B_\omega$ still receives **only** $g_{13}$; $g_{13}$ schema and replay storage unchanged.
- **Evidence status**: Every number in §1 labeled *exact* follows from the kinematic contract in `baseline/01` §2.4 or from a stated theorem. Numbers labeled *model* or *synthetic* come from idealized calculations I ran in FP64. They illustrate mechanisms and are not evidence about V3 physics. No spike has been executed for this proposal.

---

## Summary of the position

1. **The $\sqrt{1-16/144}$ objection is real, but it is aimed at the wrong mechanism.** The baseline answers it with two mechanisms (`baseline/02` §6): shared outcome coordinates, and configuration conditioning of $F$ and $\pi$. I prove that the second has **zero** effect on the bound (Corollary 1a): the bound already lets the left factor vary freely per state-action. I also prove that the first **fails for raw $g_{13}$**. Every outcome of configuration $k$ satisfies $\|(p_{\mathrm{tip},x}, p_{\mathrm{tip},y})\| = \rho_k$ exactly, so configurations with distinct lever arms have *disjoint* outcome supports. Under V3's **pooled** reference measure $\rho$, this forces an RMS relative successor error of at least $\sqrt{1 - 16/36} \approx 0.745$ for **any** $B$, any preprocessing of $g_{13}$, and any conditioning of $F$ (Corollary 1b, claim `C-B03-Q-01`). H3's $<0.20$ target is therefore unreachable as V3 is currently specified.
2. **The escape is a configuration-matched reference measure.** The negative term of the FB measure loss must draw $s''$ from the same configuration as the anchor transition. The loss then splits into 144 per-configuration problems, and the floor becomes each configuration's own spectral tail beyond 16 (Theorem 2). Under that reference, FB's identification condition becomes $\Sigma_B^{(k)} = I_{16}$ for **every** $k$. So **stratified orthonormalization is not a heuristic patch for Audit Issue #7: once the bound is escaped, the FB objective requires it.**
3. **Per-configuration orthonormalization is the per-configuration effective rank, exactly.** Because of the sphere projection, $\|\Sigma_B^{(k)} - I\|_F^2 = 256/\mathrm{PR}_k - 16$ (Proposition 1). Global orthonormalization guarantees only $\mathrm{PR}_k \ge 16\pi_k$, which is vacuous at $\pi_k = 1/144$ (Proposition 2, claim `C-B03-Q-02`). Inverse-probability weighting fixes quota drift. It cannot fix the *intrinsic* lever-arm anisotropy: in the model of §1.4, a shared linear head is limited to max–min $\mathrm{PR} \le 10.8$ when 8 of the 16 directions are tip-driven.
4. **Nondimensionalization is useful only in a specific, testable form.** The only scale $B$ can observe in $g_{13}$ is $\rho = \|p_{\mathrm{tip},xy}\|$. I propose a parameter-free, invertible re-coordinatization $T_\kappa$ applied inside $B$'s forward pass. It divides tip quantities by $\rho$, rescales time by an allometric factor $(\rho/\rho_{\mathrm{ref}})^{\kappa}$, and writes an explicit scale ratio $\lambda = \log(\rho/\rho_{\mathrm{ref}})$ into the identically-zero $v_z$ slot. It is bijective on the kinematic manifold, so no tip or lever-arm information is lost. I also show that the naive choice ($\kappa = 0$, divide by $L_D$ only) can **worsen** cross-configuration dispersion. In a synthetic generator it gave 50× dispersion against 18× for raw $g_{13}$. So $\kappa$ is pre-registered and selected from P0 rule data.
5. **Recommended design (d)**: configuration-matched FB reference, plus per-configuration scene/partition inverse-probability-weighted orthonormalization (unbiased U-statistic), plus a PR hinge at 13, plus $T_\kappa$, plus a training-only $\lambda$-anchor. It adds zero deployed parameters. A CPU spike pre-registers per-configuration $\mathrm{PR} \ge 12$ (which implies entropy erank $\ge 12$), worst-configuration successor error, zero-shot decoding on held-out geometry seeds, and a theorem-consistency gate.

---

## 1. Singular-Value Decomposition of the 144-Configuration Outcome Operator

### 1.1 Exact kinematic factorization of $g_{13}$

Let the zero-angle tip vector be $r_D^0 = (\rho\cos\varphi_0,\ \rho\sin\varphi_0,\ h)$, with lever arm $\rho = \rho_k$, phase $\varphi_0$ and axial offset $h$. The planar case of `baseline/02` §4.1 has $\rho = L_D$ and $h = 0$. Write $c = \cos q_c$, $s = \sin q_c$, $c_\vartheta = \cos(q_c + \varphi_0)$, $s_\vartheta = \sin(q_c + \varphi_0)$, $\omega = \dot q_c$, $\alpha = \widehat{\ddot q}$. From `baseline/01` §2.4, with rotation about $\hat u = e_z$:

$$
g_{13}(q,\omega,\alpha;k) = \big[\,c,\ s,\ \omega,\ \alpha,\ \ \rho c_\vartheta,\ \rho s_\vartheta,\ h,\ \ -\rho\omega s_\vartheta,\ \rho\omega c_\vartheta,\ 0,\ \ -\rho(\alpha s_\vartheta + \omega^2 c_\vartheta),\ \rho(\alpha c_\vartheta - \omega^2 s_\vartheta),\ 0\,\big].
$$

This gives the decomposition $g = E_{\mathrm{ang}}\,a(q,\omega,\alpha) + \rho_k\,E_{\mathrm{tip}}\,b(q,\omega,\alpha) + h_k e_7$. The lever arm $\rho_k$ enters **multiplicatively** on the tip block and nowhere else. The following facts are exact.

- **(F1) Dead and constant slots.** $v_{\mathrm{tip},z} \equiv 0$ and $\widehat a_{\mathrm{tip},z} \equiv 0$ for every configuration and every step. $p_{\mathrm{tip},z} \equiv h_k$ is constant within a configuration. Three of the 13 coordinates therefore carry no within-configuration information.
- **(F2) Per-configuration linear rank ≤ 8 (≤ 9 if $h_k \neq 0$).** The tip position is a rotation of $(c, s)$, so it adds nothing linearly. The velocity block adds 2 functions ($\omega s_\vartheta$, $\omega c_\vartheta$) and the acceleration block adds 2 combinations. So $\operatorname{rank} \mathbb E_k[g g^\top] \le 8$. My FP64 check over 144 synthetic configurations returned rank exactly 8 for every configuration.
- **(F3) Pooled rank ≤ 10.** Across configurations, $\rho_k c_\vartheta$ and $\rho_k s_\vartheta$ decouple from $c, s$, adding 2 directions. Define the stacked outcome operator
  $$\mathcal O = \big[\sqrt{\pi_1}\,S_1^{1/2}\ \big|\ \cdots\ \big|\ \sqrt{\pi_{144}}\,S_{144}^{1/2}\big] \in \mathbb R^{13 \times (13\cdot 144)},\qquad S_k = \mathbb E_k[g g^\top].$$
  It satisfies $\mathcal O \mathcal O^\top = \bar S = \sum_k \pi_k S_k$, and
  $$\bar S = E_{\mathrm{ang}}\bar H_{aa}E_{\mathrm{ang}}^\top + E_{\mathrm{ang}}\bar H^{(1)}_{ab}E_{\mathrm{tip}}^\top + E_{\mathrm{tip}}\bar H^{(1)\top}_{ab}E_{\mathrm{ang}}^\top + E_{\mathrm{tip}}\bar H^{(2)}_{bb}E_{\mathrm{tip}}^\top,\qquad \bar H^{(j)}_{\cdot\cdot} = \sum_k \pi_k \rho_k^j\, \mathbb E_k[\cdot\,\cdot^\top].$$
  $\mathcal O$ therefore has **at most 10 nonzero singular values** (11 with axial offsets). The standardized pooled spectrum from my synthetic generator was $[1.94, 1.82, 1.75, 1.72, 1.00, 1.00, 0.28, 0.24, 0.19, 0.08, 0, 0, 0]$. As a *linear* object, the 144 configurations share an outcome span of at most 10 dimensions and cannot be mutually orthogonal.
- **(F4) Radial shells are exact and disjoint.** Every outcome of configuration $k$ satisfies $\|(g_5, g_6)\|_2 = \rho_k$. Configurations with distinct lever arms therefore have **disjoint outcome supports** in $\mathbb R^{13}$, and in any injective re-coordinatization of $\mathbb R^{13}$. This is the measure-theoretic content of the brief's "radial shells".
- **(F5) How $L_D$ couples with angular rates depends on the regime.** Suppose angular rates scale as $\omega \propto \rho^{-\kappa}$ and $\alpha \propto \rho^{-2\kappa}$ across geometries. Then $p_{\mathrm{tip}} \propto \rho$, $v_{\mathrm{tip}} \propto \rho^{1-\kappa}$ and $\widehat a_{\mathrm{tip}} \propto \rho^{1-2\kappa}$. Three regimes give:
  - gravity-dominated (pendulum, Froude scaling): $\kappa = \tfrac12$;
  - actuator-limited with a point payload ($J \propto \rho^2$): $\kappa = 1$;
  - actuator-limited uniform rod ($J \propto \rho^3$): $\kappa = \tfrac32$.

  Only $p_{\mathrm{tip}}$ has the strict linear-in-$L_D$ shell scaling the brief describes. At $\kappa = 1$, raw $v_{\mathrm{tip}}$ is already scale-free and the angular block is not. **Consequence:** "divide the tip block by $L_D$" is not automatically an equalizer, and §2.4 pre-registers $\kappa$ instead of assuming it.

**Synthetic illustration (not V3 evidence).** I used kinematics with $J \propto \rho^2$, three capacity tiers, four strokes and 36 lever arms on $[0.08, 0.45]$ m. The ratio of largest to smallest within-configuration trace of the standardized input covariance was:

| Raw $g_{13}$ | $T_{\kappa=0}$ | $T_{1/2}$ | $T_1$ | $T_{3/2}$ |
|---:|---:|---:|---:|---:|
| 17.6× | 50.3× | 22.3× | 6.3× | 21.1× |

Matching $\kappa$ to the true scaling cuts dispersion about 3×. The wrong $\kappa$ makes it worse than doing nothing. The residual 6.3× comes from stroke and capacity, which no function of $g_{13}$ can observe. That residual is the job of stratified orthonormalization (§2).

### 1.2 What the $\sqrt{1 - 16/144}$ bound actually says: Ky Fan generalization

Let $\nu$ be the reference measure of the FB measure loss on outcome space. Let $M^{(k)}$ be the configuration-$k$ successor operator, whose rows are the successor densities (with respect to $\nu$) of state-action pairs of configuration $k$. Define the normalized outcome-side Gram
$$W_k = M^{(k)*}M^{(k)}/\|M^{(k)}\|_{HS}^2 \succeq 0,\qquad \operatorname{tr} W_k = 1.$$
A shared $B: g_{13} \to \mathbb R^{16}$ spans a subspace $V \subset L^2(\nu)$ with $\dim V \le 16$. The left factor $F(x, p, a, z)$ is **free per state-action**, which is strictly more freedom than "configuration-conditioned".

**Theorem 1 (exact rank-16 floor).** For each $k$, $\min_F \|M^{(k)} - F^\top B\|^2_{HS}/\|M^{(k)}\|^2_{HS} = 1 - \operatorname{tr}(P_V W_k)$. Hence
$$\min_{\dim V \le 16}\ \frac1K\sum_k \mathrm{err}_k^2 \;=\; \sum_{i > 16} \lambda_i(\bar W),\qquad \bar W = \frac1K \sum_k W_k.$$
*Proof.* The optimal $F$ projects each row onto $V$. Averaging gives $1 - \operatorname{tr}(P_V \bar W)$, and the Ky Fan maximum principle says $\max_{\operatorname{rank} P = 16} \operatorname{tr}(P\bar W) = \sum_{i\le 16}\lambda_i(\bar W)$. ∎

The baseline value $0.9428$ is the special case $W_k = u_k u_k^\top$ with orthonormal $u_k$, so $\bar W = P_{144}/144$. The bound depends **only on the spectrum of $\bar W$**.

**Corollary 1a (conditioning the left factor cannot help).** Theorem 1 already optimizes $F$ independently for every row. Conditioning $F$ or $\pi$ on geometry, capacity or $p_{5065}$ therefore cannot lower the floor at all. Mechanism 2 of `baseline/02` §6 is irrelevant to the bound. Only the outcome side ($B$ and $\nu$) can change it.

**Corollary 1b (pooled reference with support-disjoint configurations).** Let $\nu = \sum_k \pi_k \nu_k$ be pooled, as in V3 (`baseline/02` §5.2). Partition configurations into support classes $j = 1..K_s$ of sizes $m_j$, with disjoint outcome supports. Then $W_k = P_{j(k)} W_k P_{j(k)}$ with mutually orthogonal indicator projections, so $\bar W$ is block diagonal with block traces $m_j/K$. Each block contributes at most its trace to the top 16, so
$$\Big(\frac1K\sum_k \mathrm{err}_k^2\Big)^{1/2} \;\ge\; \Big(1 - \tfrac1K \textstyle\sum_{j \in J_{16}} m_j\Big)^{1/2},$$
where $J_{16}$ indexes the 16 largest classes. By F4, raw $g_{13}$ has $K_s$ equal to the number of distinct lever vectors. With 36 seeds × 4 strokes ($m_j = 4$) this gives **RMS error ≥ $\sqrt{1 - 64/144} = 0.745$**, so some configuration has error at least 0.745 > 0.20.

This holds for **any** architecture of $B$, any preprocessing of $g_{13}$ (including any nondimensionalization, with or without $\lambda$), and any $F$. If $B$ is made $\rho$-blind, the same bound reappears as posterior attenuation, because $B \circ T'$ is still a function of $g_{13}$. Mechanism 1 of `baseline/02` §6 ("shared physical outcome coordinates") is therefore **violated by raw $g_{13}$**: the coordinates are shared, but the supports are not.

*Why the bound bites.* The pooled FB measure term $\mathbb E_{s''\sim\nu}[(F^\top B(s''))^2]$ penalizes configuration $k$'s successor prediction for assigning mass to **other configurations' outcomes**. To zero that spill-over, $F_k$ must be orthogonal to $\{B(s'') : s'' \notin \operatorname{supp}\nu_k\}$, and those values span all 16 dimensions. Two-shell check with $d_z = 1$: the best error is $\tfrac12 = 1 - 1/2$ under the pooled reference, and $0$ when the reference is restricted to the anchor's own shell.

**Theorem 2 (configuration-matched reference removes the cross-configuration floor).** Draw the measure-term sample $s''$ from $\nu_k$, the anchor's own configuration. The loss then decouples into $K$ problems in $L^2(\nu_k)$, and
$$\mathrm{err}_k^2 \;\ge\; \sum_{i > 16} \lambda_i\big(W_k^{(\nu_k)}\big).$$
A single $B$ attains all $K$ floors simultaneously if and only if its restriction to $\operatorname{supp}\nu_k$ spans the top-16 eigenspace of $W_k^{(\nu_k)}$ for every $k$. Support disjointness no longer hurts: it actually frees the restrictions. The cross-configuration price moves from an *information-theoretic floor* to a *capacity and smoothness requirement* on $B$, which a spike can measure. The FB identification condition, $\Sigma_B$ relative to the reference measure equal to $I$, becomes
$$\Sigma_B^{(k)} := \mathbb E_{g\sim\nu_k}\big[B(g)B(g)^\top\big] = I_{16}\qquad \forall k.$$
**This is stratified orthonormalization, derived rather than assumed.**

*Calling-mode compatibility (`baseline/01` §4).*
- Goal mode: the reward embedding of a Dirac goal is $\nu(g^{\mathrm{des}})B(g^{\mathrm{des}})$, a positive multiple of $B(g^{\mathrm{des}})$ under any reference. After sphere projection, $z = B(g^{\mathrm{des}})$ is **unchanged**.
- Blend mode: the weights $w_m$ are reinterpreted against the unit's own outcome distribution $\nu_k$ instead of a pool dominated by other units' visitation. I regard this as a semantic correction. It is listed as a disclosed change.
- No deployed interface changes. The reference measure is a training-only sampler.

### 1.3 Per-configuration effective rank: exact identities

Define:
- the entropy effective rank $\operatorname{erank}_H(\Sigma) = \exp(-\sum_i p_i\log p_i)$ with $p_i = \lambda_i/\operatorname{tr}\Sigma$;
- the participation ratio $\mathrm{PR}(\Sigma) = (\operatorname{tr}\Sigma)^2/\operatorname{tr}\Sigma^2$.

Rényi entropies are non-increasing in their order, so $\operatorname{erank}_H \ge \mathrm{PR}$. **A PR gate is conservative for the entropy erank.** Because $B_\omega(g) \in \mathcal S^{15}(4)$, $\operatorname{tr}\Sigma_B^{(k)} = 16$ exactly for every $k$, on any distribution.

**Proposition 1 (orthonormality loss equals per-group rank).** $\|\Sigma_B^{(k)} - I\|_F^2 = \operatorname{tr}(\Sigma_B^{(k)})^2 - 16 = 256/\mathrm{PR}_k - 16$. The gate $\mathrm{PR}_k \ge 12$ is equivalent to $\|\Sigma_B^{(k)} - I\|_F^2 \le 16/3$.

**Proposition 2 (global orthonormality is per-group vacuous; exact statement of Audit Issue #7).** If $\sum_k \pi_k \Sigma_B^{(k)} = I$ exactly, then $\pi_k\Sigma_B^{(k)} \preceq I$. So $\lambda_{\max}(\Sigma_B^{(k)}) \le 1/\pi_k$ and $\mathrm{PR}_k \ge \operatorname{tr}/\lambda_{\max} \ge 16\pi_k$. The bound is tight: take $\Sigma_B^{(k)} = \pi_k^{-1}P_k$ with $P_k$ coordinate projections of rank $16\pi_k$ on disjoint coordinate sets. What this guarantees in practice:
- per configuration ($\pi_k = 1/144$): nothing;
- scene aggregates at nominal quotas (E1/E3 at 15%): $\mathrm{PR} \ge 2.4$;
- during P0 ramp-up with E0 inflated to 50%: E0 keeps $\mathrm{PR} \ge 8$, while E1–E4 are unconstrained. That is the domination described in Audit Issue #7.

**Proposition 3 (Jensen ordering).** $\|\Sigma_B - I\|_F^2 \le \sum_k \pi_k \|\Sigma_B^{(k)} - I\|_F^2$, by convexity of $X \mapsto \|X - I\|_F^2$. Stratified orthonormalization implies global orthonormalization. The converse is false (Proposition 2).

**Proposition 4 (necessary input spread versus Lipschitz constant).** Write $\Sigma_B^{(k)} = m_k m_k^\top + C_k$. Then $\lambda_{\max} \ge \|m_k\|^2$, so $\mathrm{PR}_k \le 256/\|m_k\|^4$. Hence $\mathrm{PR}_k \ge p$ implies $\operatorname{tr}C_k \ge 16(1 - p^{-1/2})$. If $B$ is $\ell$-Lipschitz in its normalized input $\hat g$, then $\operatorname{tr}C_k \le \ell^2 \operatorname{tr}\operatorname{Cov}_k(\hat g)$. So
$$\mathrm{PR}_k \ge 12 \;\Rightarrow\; \ell^2\, \operatorname{tr}\operatorname{Cov}_k(\hat g) \ge 11.38.$$
A configuration whose normalized outcomes occupy a small input region forces a larger $\ell$. **The cross-configuration dispersion of $\operatorname{tr}\operatorname{Cov}_k(\hat g)$ is therefore the input-design quantity to minimize.** This is the criterion used to select $\kappa$ in §2.4.

**Proposition 5 (affine floor).** If $B$ is affine in $g_{13}$ before projection, then $\operatorname{rank}\Sigma^{(k)} \le 9$ by F2. A per-configuration $\mathrm{PR} \ge 12$ therefore *requires* $B$ to unfold each configuration's 3-dimensional outcome manifold nonlinearly into at least 12 directions. The gate measures $B$'s nonlinear capacity, not input rank.

### 1.4 Exact per-configuration erank under global, inverse-probability-weighted and stratified orthonormalization (feature model)

**Model.** Take penultimate features $\phi \in \mathbb R^m$ and a trainable linear head $W$, and let $\Phi_k = \mathbb E_k[\phi\phi^\top]$. Exact orthonormalization under weights $w$ gives $W\Phi_w W^\top = I$ with $\Phi_w = \sum_k w_k\Phi_k$. Hence
$$\Sigma_B^{(k)} = Q^\top \Phi_w^{-1/2}\Phi_k\Phi_w^{-1/2}Q,$$
where $Q$ is the selected 16-dimensional frame. This is exact. Now specialize to commuting second moments: $n_a$ directions driven by angular features, with $\Phi_k$-eigenvalue independent of $k$, and $n_t = 16 - n_a$ directions driven by tip position, with eigenvalue $\propto \rho_k^2$ (F5, the exact case). Under global whitening, the per-configuration eigenvalues are $1$ ($\times n_a$) and $x_k = \rho_k^2/\mathbb E_w[\rho^2]$ ($\times n_t$).

| $n_t$ | worst-config PR ($\rho = 0.08$) | worst-config $\operatorname{erank}_H$ | PR at $\rho = 0.45$ | max–min PR, best shared linear head |
|---:|---:|---:|---:|---:|
| 0 | 16.00 | 16.00 | 16.00 | 16.00 |
| 2 | 14.30 | 14.56 | 13.71 | 14.27 |
| 4 | 12.60 | 13.13 | 13.17 | 12.66 |
| 6 | 10.92 | 11.73 | 13.24 | 11.34 |
| 8 | 9.24 | 10.37 | 13.58 | 10.76 |
| 10 | 7.58 | 9.09 | 14.08 | 11.34 |
| 12 | 5.98 | 8.00 | 14.66 | 12.66 |

Configurations are uniform over 36 lever arms; values are exact within the model. The short-link configuration fails $\mathrm{PR} \ge 12$ once $n_t \ge 5$.

The last column optimizes the tip-to-angular head gain ratio over $[10^{-3}, 10^{3}]$ (20,001-point log grid) to maximize the smaller PR of the two extreme configurations, $\rho = 0.08$ and $\rho = 0.45$. No shared linear head reaches $\mathrm{PR} \ge 12$ for both extremes when $6 \le n_t \le 10$; the best is 10.76 at $n_t = 8$.

Exact consequences within the model:
1. **Inverse-probability weighting is a no-op on intrinsic scale.** IPW changes $w$. Under D-B02-001's balanced 720-cell quotas, configurations are already sampled uniformly, so $\mathbb E_w[\rho^2]$ is unchanged and the table is **identical** under (a) and (b). IPW repairs *sampling drift*: the literal Issue #7 mechanism of early P0/P1 quota deviation. It does not repair *lever-arm anisotropy*: the brief's tension 1.
2. **Stratified orthonormalization with a shared linear head is not enough either.** For commuting $\Phi_k$, the ratio of a direction's eigenvalue between two configurations is invariant under any shared head. The best achievable max–min PR is 10.76 < 12 at $n_t = 8$, and it stays below 12 for $6 \le n_t \le 10$. The $\rho$-factorization must happen **in the trunk or at the input**: either learned (the trunk computes a division by $\rho$) or hand-coded ($T_\kappa$).
3. **With $T_\kappa$ at the matching $\kappa$, $x_k \equiv 1$ and $\mathrm{PR}_k = 16$ in the model.** Residual anisotropy from stroke and capacity remains, and the stratified loss handles it.

The model is an idealization: real $\Phi_k$ do not commute, and $n_t$ is unknown. It is used to state *which* lever moves *which* quantity. The spike (§5) measures the real values.

---

## 2. Stratified Orthonormalization & Nondimensionalization Proposal

### 2.1 Strata and nominal reference

| Symbol | Meaning |
|---|---|
| $k \in \{1..144\}$ | configuration (36 geometry seeds × 4 strokes) |
| $e \in \{E0..E4\}$ | scene, nominal quotas $q_e = (0.20, 0.15, 0.20, 0.15, 0.30)$ |
| $r \in \{\mathrm{rule}, \mathrm{policy}\}$ | replay partition, nominal $(1/3, 2/3)$ |
| $\sigma = (e, r)$ | within-configuration stratum, $w_\sigma = q_e\cdot\pi_r$ |
| $\nu_k$ | **nominal configuration reference** $= \sum_\sigma w_\sigma\,\nu_{k,\sigma}$ |

Every gate in §5 is evaluated under the $\nu_k$ just defined.

**Weighted unbiased Gram statistic.** Take a sample set partitioned into strata $\sigma$ with counts $n_\sigma \ge 2$ (present strata only) and renormalized weights $\tilde w_\sigma = w_\sigma/\sum_{\sigma'\,\mathrm{present}} w_{\sigma'}$. Define
$$\widehat U = \sum_{\sigma\neq\sigma'}\frac{\tilde w_\sigma\tilde w_{\sigma'}}{n_\sigma n_{\sigma'}}\sum_{i\in\sigma,\,j\in\sigma'}(B_i^\top B_j)^2 \;+\; \sum_\sigma \frac{\tilde w_\sigma^2}{n_\sigma(n_\sigma-1)}\sum_{i\neq j\in\sigma}(B_i^\top B_j)^2 .$$
If samples within each stratum are i.i.d., $\mathbb E[\widehat U] = \operatorname{tr}\big((\sum_\sigma \tilde w_\sigma\Sigma_\sigma)^2\big)$ **exactly**, because $\mathbb E[(B_i^\top B_j)^2] = \operatorname{tr}(\Sigma_\sigma\Sigma_{\sigma'})$ for independent $i, j$. With the sphere constraint, $\widehat U - 16$ is an unbiased estimate of $\|\Sigma - I\|_F^2$ and, by Proposition 1, of $256/\mathrm{PR} - 16$.

### 2.2 Option (a): global mini-batch $\mathcal L_{\mathrm{orth}}$ (V3 status quo)

$$\mathcal L^{(a)} = \frac{1}{N(N-1)}\sum_{i\neq j}(B_i^\top B_j)^2 - \frac{2}{N}\sum_i \|B_i\|^2 \;=\; \widehat{\operatorname{tr}\Sigma^2} - 32 \quad(\text{sphere}),$$
with a pooled reference $\nu$ in the FB measure term.

- It regularizes the empirical batch mixture, which drifts from nominal during P0/P1 (Issue #7).
- It guarantees only $\mathrm{PR}_k \ge 16\pi_k$ per group (Proposition 2).
- Through its pooled reference, it is subject to Corollary 1b: RMS successor error ≥ 0.745.

### 2.3 Option (b): scene-and-capacity inverse-probability-weighted global $\mathcal L_{\mathrm{orth}}$

Use $\widehat U$ over pooled strata $\sigma = (e, \mathrm{tier}, r)$ with nominal weights. Then $\mathcal L^{(b)} = \widehat U - 16$, with weights clipped at $\tilde w_\sigma/(n_\sigma/N) \le 10$ and the effective sample size $N_{\mathrm{eff}} = (\sum\omega_i)^2/\sum\omega_i^2$ logged.

- **Required companion:** the **FB measure term must use the same weights**. Otherwise $\Sigma_B \approx I$ holds with respect to one measure while $F^\top B$ is fit against another, and FB's identification condition is broken.
- Effect: restores $\Sigma_B \approx I$ relative to the nominal pooled $\nu$, which fixes the literal quota-drift mechanism of Issue #7.
- Limits: it is still pooled, so Corollary 1b applies. It is still global, so Proposition 2 applies. It is a no-op on lever-arm anisotropy (§1.4, consequence 1).

### 2.4 Option (c): nondimensionalized $g_{13}$ plus explicit scale ratio ($T_\kappa$)

**Admissibility.** $B$ may see only $g_{13}$ (charter boundary 1), and the only physical scale observable in $g_{13}$ is $\hat\rho = \max(\|(g_5, g_6)\|_2,\ \varepsilon_\rho)$ with $\varepsilon_\rho = 0.04$ m. On-manifold, $\hat\rho = \rho_k$ exactly (F4). Inertia, capacity and payload are **not** observable from $g_{13}$. Admissible time scalings are therefore exactly the one-parameter family $\tau(\rho) = \tau_0(\rho/\rho_{\mathrm{ref}})^{\kappa}$. The choice $\kappa = \tfrac12$ is Froude scaling with $\tau_0 = \sqrt{\rho_{\mathrm{ref}}/g}$.

**Definition.** $T_\kappa$ is a fixed, parameter-free layer at the input of $B$, so $B_\omega(g) := \tilde B_\omega(T_\kappa(g))$. Let $f = (\hat\rho/\rho_{\mathrm{ref}})^{\kappa}$, $\rho_{\mathrm{ref}} = \sqrt{0.08\cdot0.45} = 0.1897$ m, and let $\Omega = \omega_{\mathrm{ref}}/f$ and $A = \alpha_{\mathrm{ref}}/f^2$, where $\omega_{\mathrm{ref}}, \alpha_{\mathrm{ref}}$ are global constants frozen from the P0 rule partition.

| Slot | Raw $g_{13}$ | $T_\kappa(g)$ | Physical meaning after $T_\kappa$ |
|---:|---|---|---|
| 1–2 | $c, s$ | $c, s$ | joint angle |
| 3 | $\omega$ | $\omega/\Omega$ | angular rate in allometric time units |
| 4 | $\alpha$ | $\alpha/A$ | angular acceleration, same units |
| 5–7 | $p_{\mathrm{tip}}$ | $p_{\mathrm{tip}}/\hat\rho$ | tip position in link lengths (direction plus $h/\rho$) |
| 8–9 | $v_{\mathrm{tip},xy}$ | $v_{\mathrm{tip},xy}/(\hat\rho\,\Omega)$ | tip velocity in reference tip-speed units (Froude number when $\kappa = \tfrac12$) |
| 10 | $v_{\mathrm{tip},z} \equiv 0$ | $\lambda = \log(\hat\rho/\rho_{\mathrm{ref}}) \in [-0.864, +0.864]$ | **explicit scale ratio (lever arm)** |
| 11–13 | $\widehat a_{\mathrm{tip}}$ | $\widehat a_{\mathrm{tip}}/(\hat\rho\, A)$ | tip acceleration in reference units (in units of $g$ when $\kappa = \tfrac12$ and $\alpha_{\mathrm{ref}} = g/\rho_{\mathrm{ref}}$) |

**Properties.**
- **Dimensional consistency.** $\widehat a/\rho$ contains $\alpha$ and $\omega^2$, and both scale as $f^{2}$, so every $\kappa$ is consistent.
- **Bijectivity.** On the kinematic manifold $\{v_z = 0\}$, $T_\kappa^{-1}$ is explicit: $\rho = \rho_{\mathrm{ref}}e^{\lambda}$, $p = \rho\,\hat p$, $v = \rho\,\Omega\,\hat v$ with $v_z = 0$, $\widehat a = \rho A\hat a$. The FP64 round-trip error was $1.1\times10^{-13}$. An off-manifold $v_z \neq 0$ (a schema violation) is asserted against in the data pipeline and logged, not silently absorbed.
- **Budget.** Zero parameters. The input stays 13-dimensional, so $B$'s parameter count is identical.
- **Schema.** Replay stores raw $g_{13}$, so the V3 manifest, D-B02-001's canonical $g_{\mathrm{hold}}$ and all evaluators are untouched. D-B02-001's normalizer contract applies to $T_\kappa(g)$, whose statistics no longer depend on the seed mix.

**Pre-registered $\kappa$ selection.** Grid $\kappa \in \{0, \tfrac12, 1, \tfrac32\}$. Choose
$$\kappa^\star = \arg\min_\kappa D(\kappa),\qquad D(\kappa) = \frac{\max_k \operatorname{tr}\operatorname{Cov}_k(\hat g_\kappa)}{\min_k \operatorname{tr}\operatorname{Cov}_k(\hat g_\kappa)},$$
using standardized $T_\kappa(g)$ on **P0 rule-partition data from training seeds only**. Freeze $\kappa^\star$ before any $B$ training. Ties go to the smaller $\kappa$. The criterion is exactly the quantity Proposition 4 says controls the Lipschitz demand.

**What (c) does and does not do.**
- (c) removes lever-arm-induced dispersion when $\kappa$ matches.
- (c) cannot remove stroke or capacity dispersion, which are unobservable in $g_{13}$.
- (c) **cannot affect Corollary 1b.** With $\lambda$, supports remain disjoint. Without $\lambda$, the bound returns through posterior attenuation.
- The brief's target, "all 144 share $\Sigma_B^{(k)} \approx I_{16}$", is **not** delivered by (c) alone. It requires (d).

### 2.5 Recommended design (d): configuration-matched reference + per-configuration stratified IPW orthonormalization + $T_{\kappa^\star}$

**Batch construction.**
- $N = 1024$ = 16 configuration blocks × 64 samples. Configurations are cycled uniformly without replacement, so each is visited every 9 updates and the capacity tiers and strokes are balanced exactly.
- Within a block, draw by stratum at nominal $w_\sigma$, with integer allocation 13/10/13/10/18 across scenes, each split 1:2 rule:policy. Inverse-probability weighting corrects rounding and any shortfall.
- A stratum with $n_\sigma < 2$ is dropped and the weights renormalized; log `b03_stratum_missing`. If a block's present nominal mass is below 0.7, skip that block's orthonormalization term; log `b03_block_skipped`. D-B02-001's 720-cell gate makes both cases rare after P0.

**FB measure term (training-only change).** For anchor $i$ in block $k$, the negative samples $j$ come from **the same block** with weights $\tilde w_{\sigma_j}/n_{\sigma_j}$:
$$\mathcal L_{\mathrm{FB}} = \frac{1}{|K_b|}\sum_{k\in K_b}\Big[\sum_{i,j\in k}\omega_i\omega_j\big(F_i^\top B_j - \gamma\,\bar F_i'^{\top}\bar B_j\big)^2 - 2\sum_{i\in k}\omega_i\,F_i^\top B(g_{i,t+1})\Big].$$
B01's causal $p_{5065}$ partition is used unchanged inside $F_i$.

**Orthonormalization term.** Let $\widehat U_k$ be the §2.1 statistic on block $k$, and keep a per-configuration exponential moving average $\tilde U_k \leftarrow (1-\nu_{\mathrm{ema}})\,\mathrm{sg}(\tilde U_k) + \nu_{\mathrm{ema}}\widehat U_k$ with $\nu_{\mathrm{ema}} = 0.05$. The 144 values are scalars; diagnostics additionally store 144 matrices of size 16×16. Then
$$\mathcal L_{\mathrm{orth}}^{(d)} = \frac{1}{|K_b|}\sum_{k\in K_b}\Big[\underbrace{(\widehat U_k - 16)}_{=\ \widehat{\|\Sigma_B^{(k)}-I\|_F^2}} \;+\; \beta_h\big((1-\nu_{\mathrm{ema}})\,\mathrm{sg}(\tilde U_k) + \nu_{\mathrm{ema}}\widehat U_k - 256/13\big)_+\Big],\qquad \beta_h = 1.$$
The hinge activates exactly when the running estimate of $\mathrm{PR}_k$ drops below 13, one unit of margin above the gate. The coefficient $\beta_{\mathrm{orth}}$ is unchanged from V3. By Proposition 3, global orthonormality under the pooled nominal $\nu$ is implied and needs no separate term.

**$\lambda$-anchor (training-only).** A linear head $h_\lambda: \mathbb R^{16}\to\mathbb R$ (17 parameters, not deployed) with $\mathcal L_\lambda = \mathrm{mean}_i(h_\lambda(B_i) - \lambda_i)^2$ and $\beta_\lambda = 0.1$. Under the configuration-matched reference nothing else forces $z$ to carry the lever arm, and absolute tip semantics from $z$ alone need it (§2.6).
- Cost: $\lambda$ is constant within a configuration, so an exact anchor confines within-configuration variance to the hyperplane orthogonal to the anchor direction. This costs at most about 1 unit of $\mathrm{PR}_k$, keeping $\mathrm{PR}_k \le 15$ plus a small term along that direction.
- A spike arm turns the anchor off.

**Parameter accounting.**
- $\tilde B_\omega$ keeps V3's architecture and 13-dimensional input. $T_\kappa$ has 0 parameters. $h_\lambda$ and $F$ are training-only.
- **Deployed total stays 281,617.**
- Audit note: by my arithmetic, the stated $B$ architecture (`13→128→256→128→16` with three LayerNorms) has 70,800 parameters, not 74,000. That 3,200 gap predates this packet and is outside B03's scope. My design does not change the count, whatever its true value.

### 2.6 Comparison and preservation of tip kinematic information

| Criterion | (a) global | (b) IPW global | (c) $T_\kappa$ + pooled IPW | **(d) recommended** |
|---|---|---|---|---|
| Fixes P0/P1 quota drift (Issue #7 literal) | no | **yes** | yes | **yes** |
| Fixes lever-arm anisotropy (brief tension 1) | no | no (§1.4) | yes if $\kappa$ matches | **yes** |
| Per-configuration erank guarantee | none ($\ge 16\pi_k$) | none | none | **direct**: $\widehat U_k$ ↔ $\mathrm{PR}_k$, hinge at 13 |
| Escapes Corollary 1b floor (≥ 0.745) | no | no | no | **yes** (Theorem 2) |
| Tip and lever-arm semantics | raw | raw | bijective + $\lambda$ | bijective + $\lambda$ + anchor |
| Deployment purity and budget | ✓ | ✓ | ✓ (0 params) | ✓ (0 deployed params) |
| Stroke and capacity residual dispersion | unhandled | unhandled | unhandled | stratified loss |

**Tip semantics.**
- **Information is preserved.** $T_\kappa$ is a bijection on the kinematic manifold, and F1–F2 show that raw tip slots contain exactly angular kinematics × the static lever vector. So no lever-arm, tip-velocity or tip-momentum information is discarded: $p_{\mathrm{lin}} = m_{\mathrm{eff}} v_{\mathrm{tip}}$, with $\rho$ recovered from $\lambda$.
- **Goal mode.** The upper layer still writes $g^{\mathrm{des}}$ in physical SI units, including tip targets. $T_\kappa$ maps them, so a 1 m/s tip-speed target becomes different $\omega/\Omega$ on short and long links, as it physically should.
- **Decoding mode.** Physical tip quantities are recovered as $T_\kappa^{-1}(\text{probe}(z))$. The $\lambda$-anchor makes $\rho$ decodable from $z$ without consulting the unit descriptor. Spike gate G4 tests this on **unseen** geometry seeds.

---

## 3. Serious Alternative Considered and Rejected

**Alternative: per-configuration output whitening.** Set $B_k(g) = 4\cdot\mathrm{normalize}(\widehat\Sigma_k^{-1/2}B(g))$, either post hoc after training or as a learned adapter. Each deployed unit stores one symmetric 16×16 matrix.

*Why it is serious.* It makes $\Sigma_B^{(k)} = I$, and so $\mathrm{PR}_k = 16$, **by construction** for every configuration. It is cheap and needs no change to the training loss. Each deployed unit is a single configuration, so a single matrix suffices. It would trivially pass any erank-only gate.

*Why it is rejected.*
1. **Budget.** It adds 136 deployed parameters per unit, which violates the fixed 281,617 total.
2. **It cannot create information, and it games the gate.** Suppose $\Sigma_B^{(k)}$ has 4 directions with eigenvalue 0.01. Whitening scales them ×10. Those directions hold whatever small, possibly noise-dominated variation $B$ produced. By Proposition 4, the effective Lipschitz constant grows by $\lambda_{\min}^{-1/2}$, so outcome perturbations of encoder-noise size produce large angular changes of $z$. Effective rank measures spread, not information. **Lesson adopted:** every erank gate in §5 is paired with decoding-accuracy and Lipschitz anti-gaming gates (G4, G6).
3. **It does not touch Corollary 1b.** If $F$ is trained against a pooled reference, the 0.745 floor is unchanged, because whitening is a per-configuration linear map inside $V$ and Theorem 1 already optimizes over those. If it is trained against a configuration-matched reference, it is redundant with the stratified loss.
4. **It fragments $z$ semantics across units.** The same physical outcome $g$ maps to different $z$ in different units through unit-specific rotations. That works against the cross-unit composition targeted by B04/H4.

**Other alternatives, rejected more briefly.**
- **$\rho$-blind $B$ (drop $\lambda$, nondimensional input only).** It maximizes sharing, but $z$ alone then loses the lever arm (rubric dimension 3). Corollary 1b still binds under a pooled reference. It survives only as the spike arm A4−λ.
- **Configuration-conditioned $B$ (mixture-of-experts or a geometry embedding into $B$).** Violates the $B_\omega(g_{13})$ interface (charter boundary 1) and the budget.
- **Raising $d_z$.** Forbidden by the brief.
- **Fixed Froude scaling ($\kappa = \tfrac12$) as the default.** Premise-dependent: it is correct only for gravity-dominated configurations (F5). It is kept as a point on the pre-registered $\kappa$ grid.

---

## 4. Candidate Necessity Claims

All claims enter as **Candidate**. Grade-1 locking requires an independent proof check and the human-lead signature (Appendix B.9.2).

### C-B03-Q-01: Pooled-reference rank floor under support-disjoint configurations

| Field | Content |
|---|---|
| **Premises** | (P1) The FB-type loss represents successor densities against a reference measure $\nu$; relative error is the HS norm in $L^2(d_k\otimes\nu)$, averaged with equal weight over configurations. (P2) $B: g_{13}\to\mathbb R^{16}$ is shared and the left factor is unrestricted per state-action. (P3) $\nu = \sum_k\pi_k\nu_k$ is pooled across configurations. (P4) The configurations partition into support classes $j$ of sizes $m_j$ whose outcome supports under $\nu$ are pairwise disjoint. For raw $g_{13}$ this holds exactly by F4 whenever lever vectors differ. |
| **Conclusion shape** | **Impossibility.** $\big(\frac1K\sum_k\mathrm{err}_k^2\big)^{1/2} \ge \big(1 - \frac1K\sum_{j\in J_{16}}m_j\big)^{1/2}$. For 36 lever arms × 4 strokes this is $\ge 0.745$. The bound holds for every architecture or preprocessing of $B$, including nondimensionalization with or without $\lambda$, and for every conditioning of $F$ or $\pi$. Corollary: H3 ($<0.20$ for all configurations) is unreachable unless the reference is matched per configuration or per support class (Theorem 2). |
| **Grade** | **Grade 1** (Ky Fan maximum principle plus block-diagonality; Theorem 1 and Corollary 1b). |
| **Implementation independence** | Any function class for $B$ and $F$, any optimizer, any $d_z$ (replace 16 by $d_z$). |
| **Scope** | Successor-measure factorizations with a shared outcome encoder. It does not cover methods that condition $B$ on configuration identity (excluded by charter boundary 1), and it does not cover a configuration-matched reference. |
| **Operational test** | Spike G3: every pooled-reference arm satisfies RMS $\varepsilon^{\mathrm{pool}} \ge \sqrt{\sum_{i>16}\lambda_i(\bar W)} - 0.01$, and the computed bound is $\ge 0.70$ on the surrogate. |
| **Falsifier** | A pooled-reference arm whose measured B-limited error falls below the computed bound, with support disjointness certified (lever arm recovered from outcomes with $R^2 \ge 0.999$). Because the conclusion is a theorem, such a result means an estimation bug or a premise failure, for example tip noise that blurs the shells so (P4) fails. It must be logged as a premise or scope narrowing (B.9.6), not dismissed. |

### C-B03-Q-02: Global orthonormality cannot certify per-group effective rank; per-group Gram is per-group PR

| Field | Content |
|---|---|
| **Premises** | Outputs lie on $\mathcal S^{d_z-1}(\sqrt{d_z})$, and groups are mixture components with weights $\pi_k$. |
| **Conclusion shape** | **Identity plus tight bound.** (i) $\|\Sigma^{(k)} - I\|_F^2 = d_z^2/\mathrm{PR}_k - d_z$. (ii) Exact global orthonormality implies only $\mathrm{PR}_k \ge d_z\pi_k$, and this is tight. (iii) $\operatorname{erank}_H \ge \mathrm{PR}$. So any per-group erank gate needs a per-group term. A global term, whether inverse-probability weighted or not, is insufficient in principle. |
| **Grade** | **Grade 1** (Propositions 1–3). |
| **Implementation independence** | Any encoder, and any estimator of the Gram matrix. |
| **Scope** | Sphere-projected encoders. Without the projection, (i) becomes $\|\Sigma - I\|^2 = \operatorname{tr}\Sigma^2 - 2\operatorname{tr}\Sigma + d_z$, and the PR link needs a trace term. |
| **Operational test** | Spike: in arms A0/A1 the global $\|\Sigma - I\|_F^2$ meets V3 tolerance while $\min_k\mathrm{PR}_k < 12$ for at least one configuration. This exhibits (ii) and is a consistency check, not pass-critical. Relation (i) is checked numerically on every arm to within $10^{-4}$. |
| **Falsifier** | A numerical violation of (i) or (ii) beyond FP tolerance means an implementation error, since the statements are algebraic. |

### C-B03-Q-03: Lever-arm factorization is an obligatory functional role for uniform per-configuration rank

| Field | Content |
|---|---|
| **Premises** | (P1) Tip outcome channels scale as $\rho_k^{1-j\kappa}$ (F5). (P2) The reference is configuration-matched and the goal is $\min_k\mathrm{PR}_k \ge 12$ across $\rho_{\max}/\rho_{\min} = 5.6$. (P3) Reweighting acts on mixture weights only. |
| **Conclusion shape** | **Functional role.** The encoder must realize a factorization of lever-arm scale out of the tip channels: explicitly (as in $T_\kappa$) or implicitly (a learned, $\rho$-invariant hidden representation). Reweighting, whether IPW or stratified with a shared linear head, cannot substitute: in the commuting model the max–min PR is $\le 10.8$ at $n_t = 8$ (§1.4). |
| **Grade** | **Grade 2** Candidate. Within the commuting feature model the result is Grade 1. Whether real MLP features satisfy that model is empirical. |
| **Operational realization test** | Either $T_\kappa$ is present, or in arm A3 (raw input with the stratified loss) a linear probe on $\tilde B$'s first hidden LayerNorm output predicts $\lambda$ while the ρ-equivariance residual stays low (§5.5 metric E). If the role is "implicit" with no probe evidence, it counts as missing. |
| **Falsifier** | Arm A3 matches A4 on G1, G2 and G4, within 0.5 PR, 0.02 $\varepsilon$ and 0.02 $R^2$, **and** shows no $\rho$-invariant hidden representation. Then the role is not obligatory in this regime, and the claim is narrowed to "helpful". |

---

## 5. Pre-Registered Empirical Spike Protocol

### 5.1 Compute environment and honesty statement

- **Hardware.** CPU only; CUDA was unavailable on this host for B01 and B02. Training runs in FP32; analytic checks, statistics, SVDs and bounds run in FP64.
- **Script.** New script `gpu_experiments/run_b03_config_matched_erank_spike.py`, writing to `packets/B03/spikes/B03-SPIKE/{PLAN.md, VERDICT.json, runs.log}`.
- **The existing `run_b03_rank16_erank_spike.py` does not conform and must not be used as evidence.** It draws tip vectors as independent Gaussian noise scaled by $L$, which violates F1–F4: no rigid-body coupling, no exact shells, no rank ≤ 8 structure. It trains on only 3 lengths, applies the stratified loss in both arms, and uses a pooled reference.
- **Physics.** The generator is a **reduced surrogate**, not the V3 physics collector. A PASS is Candidate evidence only. Locking any claim beyond its Grade-1 algebra requires a re-run on D-B02-001's merged physics collector. Charter boundary 3 coverage metrics remain B02's responsibility and are not claimed here.

### 5.2 Surrogate data generator

- **Plant.** Single revolute link. Control at 50 Hz, with 4 semi-implicit substeps at 200 Hz. Inertia $J = I_{D,zz} + n_g^2J_{\mathrm{rotor}}$ with payload. Gravity, viscous and Coulomb friction, and spring-damper end stops. Capacity tier $C_0 \in \{3, 6, 9\}$ N·m, $S_{\max} = 1.25C_0$.
- **Configurations.** 36 seeds with **distinct** $L_D$ on a log grid over $[0.08, 0.45]$ m, independently drawn payload mass and COM, tier $= $ seed mod 3; 4 stroke profiles per seed, giving 144 configurations.
- **Scenes.** E0–E4 per D-B02-001: net-equilibrium sustained load with alternating sign, deterministic release edge plus recovery window, and a contact spring wall. The external-torque generator is causal.
- **Behavior policy.** The D-B02-001 rule controller (scene-dependent feedforward gain $\kappa$; E3 = 1, E4 = 0) with random targets, plus 30% Ornstein–Uhlenbeck exploration.
- **Volume.** Per configuration × scene: 600 training and 400 test transitions, 720,000 in total. Per configuration, 2,048 held-out outcomes at nominal $w_\sigma$ for rank statistics.
- **Held-out geometry.** 8 of the 36 seeds (interior $L_D$ values, seed indices $\{2, 6, 11, 15, 20, 24, 29, 33\}$) are excluded from all training, including $\kappa$ selection and normalizer statistics. That is 32 held-out configurations.

### 5.3 Ground-truth successor operators and B-limited error

Training is μ-successor FB, i.e. evaluation of the behavior policy. This isolates outcome-representation capacity from actor learning; it is a limitation, see §5.8.

- Per configuration, fit 256 k-means cells on test outcomes in $T_{\kappa^\star}$ space. Monte-Carlo the discounted occupancy from 256 anchor state-actions with horizon 150 and $\gamma = 0.98$, giving $M^{(k)}\in\mathbb R^{256\times256}$ as densities with respect to the cell masses of $\nu_k$.
- **Configuration-matched error** $\varepsilon_k^{\mathrm{cm}}(B)$: the closed-form weighted least-squares residual of $M^{(k)}$ on cell-averaged $B$ features in $L^2(\nu_k)$, with a free left factor per row.
- **Pooled error** $\varepsilon_k^{\mathrm{pool}}(B)$: the same, in $L^2(\nu)$ over the union of all $144 \times 256$ cells, with $M^{(k)}$ zero on other configurations' cells.
- **Oracle floor** $\sum_{i>16}\lambda_i(W_k)$ per configuration, and the **theorem bound** $\sum_{i>16}\lambda_i(\bar W)$ for the pooled case.

### 5.4 Training and arms

All arms use V3's exact $\tilde B$ architecture with identical parameter count and $d_z = 16$. $F$ is training-only: a causal-$p$ compressor plus MLP $[512, 512] \to 16$. Target networks with $\tau = 0.005$, Adam at $10^{-4}$, 30,000 updates at batch size 1024, **3 seeds per arm**. The P0 ramp is simulated by drawing 50% E0 for the first 3,000 updates, to reproduce Issue #7.

| Arm | Input | FB reference | $\mathcal L_{\mathrm{orth}}$ | Purpose |
|---|---|---|---|---|
| A0 | raw $g_{13}$ | pooled | (a) global | V3 status quo |
| A1 | raw | pooled, IPW | (b) | brief option (b) |
| A2 | $T_{\kappa^\star}$ | pooled, IPW | (b) | brief option (c) |
| A3 | raw | config-matched | (d) stratified + hinge | is $T_\kappa$ necessary? (C-B03-Q-03) |
| **A4** | $T_{\kappa^\star}$ | config-matched | (d) + hinge + $\lambda$-anchor | **primary proposal** |
| A4−λ | $T_{\kappa^\star}$ | config-matched | (d) + hinge | cost and benefit of the anchor |
| A4-κ½ | $T_{1/2}$ (Froude) | config-matched | (d) + hinge + anchor | κ sensitivity (skipped if $\kappa^\star = \tfrac12$) |
| A4-shuf | $T_{\kappa^\star}$ | blocks with **shuffled** configuration labels, i.e. effectively pooled | (d) | negative control for C-B03-Q-01 |
| W | A0 + post-hoc per-configuration whitening | pooled | (a) | anti-gaming control (§3) |

### 5.5 Metrics

- **A. Per-group rank.** $\mathrm{PR}_k$ from the unbiased $\widehat U$ on 2,048 held-out outcomes at nominal $w_\sigma$, and $\operatorname{erank}_H$ from the plug-in $\Sigma_B^{(k)}$. Reported for 144 configurations (primary), for 720 configuration × scene cells (reported only), and for aggregates: 5 scenes, 3 tiers, 4 strokes. 95% intervals from 1,000 bootstrap resamples within configuration.
- **B. Successor error.** $\varepsilon^{\mathrm{cm}}_k$, $\varepsilon^{\mathrm{pool}}_k$, and the oracle floor (§5.3). Summaries: worst-configuration maximum and RMS.
- **C. Zero-shot decoding.** Probes (2-layer MLP, 64 hidden units) from frozen $z$ to $T_{\kappa^\star}(g)$ slot groups and $\lambda$, trained on the 28 training seeds and tested on the 8 held-out seeds. $R^2$ per group. Physical $(p, v, \widehat a)_{\mathrm{tip}}$ reconstructed via $T^{-1}$, with relative RMSE.
- **D. Anti-gaming.** A Lipschitz proxy $\ell_{99}$: the 99th percentile of $\|B(g) - B(g')\|/\|\hat g - \hat g'\|$ over within-configuration nearest-neighbour pairs.
- **E. ρ-equivariance residual (for C-B03-Q-03).** For arm A3: the $R^2$ of $\lambda$ from first-hidden-layer features, and the relative change in those features under a synthetic $\rho$-rescaling of the tip block at fixed angular outcome.

### 5.6 Pre-registered gates (primary arm A4; all 3 seeds must pass)

| Gate | Criterion | Pass-critical |
|---|---|---|
| **G1 per-group erank** | $\min_{k\le144}\mathrm{PR}_k \ge 12.0$ (point) **and** every configuration's lower 95% bound $\ge 11.5$. By Rényi monotonicity this implies $\operatorname{erank}_H \ge 12/16$. Scene, tier and stroke aggregates: $\mathrm{PR} \ge 13.0$. **Zero-shot:** $\min\mathrm{PR}_k \ge 12.0$ on the 32 held-out configurations. | yes |
| **G2 worst-group successor error** | $\max_k\varepsilon_k^{\mathrm{cm}} \le 0.20$ gives **PASS** (supports H3 on the surrogate); $\le 0.30$ gives **PARTIAL** (H3 not supported, but design (d) may proceed). In both cases also require $\max_k\varepsilon_k^{\mathrm{cm}}(\mathrm{A4}) \le 0.6\,\max_k\varepsilon_k^{\mathrm{cm}}(\mathrm{A0})$. | yes (≥ PARTIAL) |
| **G3 theorem consistency** | For every arm, $\mathrm{RMS}_k\,\varepsilon_k^{\mathrm{pool}} \ge \sqrt{\sum_{i>16}\lambda_i(\bar W)} - 0.01$; a violation makes the run **INVALID**. The computed bound is $\ge 0.70$, which certifies premise (P4) on the surrogate; otherwise report the premise status. A4-shuf: $\max_k\varepsilon^{\mathrm{cm}} \ge 0.70$. | yes (validity) |
| **G4 decoding / tip semantics** | Held-out seeds: $R^2 \ge 0.95$ for $(c, s)$, $\omega/\Omega$, $\alpha/A$ and $\lambda$. Physical tip $p$, $v$, $\widehat a$ relative RMSE $\le 0.10$ via $T^{-1}$. A4's decoding $R^2$ within 0.02 of A0 on every group, i.e. no information loss. | yes |
| **G5 analytic and budget** | $T$ round-trip $\le 10^{-9}$ (FP64). Per-configuration linear rank of $g_{13}$ $\le 9$. $\tilde B$ parameter count identical across arms. Deployed total 281,617. Proposition 1 identity holds numerically to within $10^{-4}$. | yes |
| **G6 anti-gaming** | $\ell_{99}(\mathrm{A4}) \le 2\times\ell_{99}(\mathrm{A0})$. Arm W must **fail** G4 or G6, which demonstrates that erank-only gates can be gamed. | yes |

### 5.7 Pre-registered decision rules (no post-hoc tuning)

1. **A4 passes G1–G6.** Adopt design (d) with $\kappa^\star$. Under PARTIAL G2, adopt (d) and record H3 as "not supported at 0.20 on the surrogate".
2. **A3 matches A4** within 0.5 PR (G1), 0.02 $\varepsilon$ (G2) and 0.02 $R^2$ (G4). Then $T_\kappa$ is unnecessary: narrow C-B03-Q-03 per its falsifier and adopt A3, which feeds raw $g_{13}$ to $B$ (simpler).
3. **A1 or A2 passes G1 and G2.** This falsifies the §1.4 consequences for this regime: record a scope narrowing of C-B03-Q-03, and note that C-B03-Q-01 then requires a premise audit under G3.
4. **A4 fails G1.** Report FAIL. The single pre-registered fallback is A4 with 720 configuration × scene strata in $\widehat U$ (same hinge), run once. If it also fails, the packet's design recommendation is withdrawn pending a capacity analysis of $\tilde B$ within the fixed budget.
5. **A4−λ beats A4 on G1 by ≥ 0.5 PR with G4 still passing.** Drop the anchor.
6. **G3 is violated in any arm.** The run is INVALID; audit the estimators before interpreting anything.

**Runtime budget.** About 9 arms × 3 seeds × 25 min ≈ 11 CPU-hours. Pre-registered reduction if the budget is exceeded: 15,000 updates for all arms simultaneously, never for a subset.

**VERDICT.json fields.** `kappa_star`, `D_kappa[4]`, `pr_min_cfg`, `pr_lcb_min_cfg`, `erankH_min_cfg`, `pr_min_heldout`, `pr_aggregates{scene,tier,stroke}`, `eps_cm_max`, `eps_cm_rms`, `eps_pool_rms`, `bound_pool`, `oracle_floor_max`, `decode_r2{group}`, `tip_rel_rmse{p,v,a}`, `lip99`, `gates{G1..G6}`, `status ∈ {PASS, PARTIAL, FAIL, INVALID}`, `device`, `surrogate=true`.

### 5.8 What this spike cannot establish

- Converged z-conditioned control. μ-FB is policy evaluation, and charter boundary 4 forbids extrapolating from it.
- V3-physics magnitudes; a re-run on the merged collector is required.
- Composition gains under H4, which belong to B04.
- The configuration-matched reference changes the meaning of blend-mode weights (§1.2). B04 should register whether this helps or hurts composition.
