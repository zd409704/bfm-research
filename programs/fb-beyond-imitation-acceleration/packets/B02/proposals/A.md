# Proposal A (Packet B02): Breaking Imitation Ceilings via Unindexed Single-Frame Prompts, Relabeling, and Joint Training Non-Stationarity

- **Packet**: `B02` — Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment in Joint FB + Task-Q + Planner Training
- **Author slot**: Primary Author A (solo draft, §4 Step 2; isolation per §11.1)
- **Method version**: v1.0 (`1ce8d1b3…3d11f7`)
- **Frozen context read**: `PROGRAM_CHARTER.md`, `synthesis/B01-synthesis.md`, `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md` (the brief; the path `packets/B02/brief.md` named in my task prompt does not exist), `baseline/02-fb-paradigm-beyond-imitation-and-exploration.md`, `baseline/04-joint-fb-ball-striking-v2-architecture.md`, `baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md`, `packets/B02/spikes/B02-SPIKE/PLAN.md`, pinned method §11.5 and Appendix B. No other draft directory was read or listed.
- **Companion artifacts (this directory only)**: `spike_sketch.py` (an author reference implementation of §5) and `spike_sketch_output.json` (CPU dry-run output, `verdict: PASS`). **Status of these numbers:** they come from author-side synthetic CPU checks of closed forms and test mechanics. They are **not** the registered `B02-SPIKE` run (§12.2) and are not evidence that anything has been learned (Charter §2.5).

### 0. Summary of position

1. **Separate the two regimes.** In the step action-$Q$ regime (ball striking, $K_{\mathrm{hold}}=1$), replay age adds **zero** Bellman-target bias, because the label is the executed physical action. In the macro-$z$ regime (obstacle traversal, $K=10$), the label is a *command*, and its meaning is set by the current low-level conditional $p_\theta(\tau\mid H,z)$. That is the only place staleness bias enters (§1.1–1.2).
2. **$B$ drift is not the cause of macro-critic staleness. $\pi$ drift is.** For a fixed executed vector $z_{\mathrm{actual}}$, the target's conditional distribution does not depend on $\omega$ at all (Prop. 1.2). $\Delta_B$ is a *diagnostic of why* $\pi$ moves. Because of an exact $O(d_z)$ gauge symmetry of the joint objective (Prop. 1.4), it cannot certify staleness. The certificate is the per-row KL / $\chi^2$ between the stored behaviour Gaussian and the current actor. Both are computable **without parameter snapshots** from two new immutable replay columns (`behavior_mu`, `a_raw`).
3. **Mitigation.** Use a **generation-level drift-gated replay horizon** (not a row-level gate, which would introduce selection bias). Add the exact short-macro discount $\gamma^k$, full-prefix zero-hidden burn-in with shared-prefix deduplication, and an optional truncated-IS arm inside the gate. `behavior_z` / `z_actual` stay write-once.
4. **Normalizer contract.** I give closed forms for the stationary bias of every contract violation (double `m_next`, relabel-time update, expert-query update, train-mode batch statistics), plus a telescoping identity that sizes $\mu_{\mathrm{next}}-\mu_{\mathrm{cur}}$ exactly. Expert encoding under train-mode batch statistics is the severe case: relative input error $\approx 3/(2n_e)$, i.e. 19% at $n_e=8$.

---

## 1. Exact Mathematical Analysis of Joint Training Non-Stationarity and Prompt Drift

### 1.0 Notation and standing assumptions

- Latent sphere $\mathcal{S}^{d_z-1}(\sqrt{d_z})$ with $d_z=256$ (obstacle) or $100$ (ball). $\operatorname{proj}(x)=\sqrt{d_z}\,x/\|x\|_2$.
- Low-level actor: a diagonal Gaussian in **pre-clip** action space, $\pi_\theta(\cdot\mid o,z)=\mathcal{N}(\mu_\theta(o,z),\operatorname{diag}\sigma_\theta^2(o,z))$, then $a_{\mathrm{applied}}=\operatorname{clip}(a_{\mathrm{raw}},-1,1)$. (If R2.1 uses a deterministic actor with additive exploration noise $\sigma$, set $\sigma_\theta\equiv\sigma$; every formula below still holds.) **$\theta$ includes the actor's observation-normalizer state**, because the deployed map $(o,z)\mapsto\mu$ depends on it.
- Macro row (obstacle, R2.1 `TaskReplay`): $(H_t, c_t^{\mathrm{geom}}, z_{\mathrm{actual}}, R^{(k)}, H_{t+k}, c_{t+k}^{\mathrm{geom}}, d, k, \texttt{generation})$, where $k\in\{1,\dots,K\}$, $R^{(k)}=\sum_{j=0}^{k-1}\gamma_{\mathrm{task}}^j r_{t+j}$, and $d=$`terminated`. $z$ is held for the macro.
- Macro target (baseline 05 §2; the prompt's $P_\psi$ is the **target** planner $P_{\bar\psi}$ in the baseline, and I use the baseline form):
$$
y \;=\; g(\tau) \;:=\; R^{(k)} + \gamma_{\mathrm{task}}^{k}(1-d)\,\bar V(H_{t+k}),\qquad \bar V(H)=\min_{j=1,2}Q_{\bar\phi_j}\big(H,c^{\mathrm{geom}},P_{\bar\psi}(H)\big).
$$
- "then" = the parameters $(\omega_{t-\Delta},\theta_{t-\Delta})$ at collection; "now" = $(\omega_t,\theta_t)$. The environment (including the per-episode fixed height $h$, which is exposed to $Q$ via $c^{\mathrm{geom}}$ and to $\pi$ via `scan`) is stationary. The curriculum changes the *distribution* of $h$, not the transition kernel given $h$.

**Observability note.** Both critics' histories contain the previous actions: `last_action[29]` (obstacle $o$) and `actions[29]` (ball $o^{\mathrm{low}}\subset o^Q$). The macro critic's history also contains $z_{t-1}$. The filtering belief $p(s_t\mid H_t)$ over hidden simulator state is therefore a function of the action-observation history alone and **does not depend on the behaviour policy**. Without action inputs this would fail: $p(s_t\mid o_{0:t})$ depends on the policy that generated the observations. This is a premise of everything below.

### 1.1 Regime split: why the step action-$Q$ critic has no age bias

For ball striking, the row is $(H^Q_t,a_t,r_t,H^Q_{t+1},d_t)$ with $a_t$ the **executed** action. Write $\mathcal{T}Q(H,a)=\mathbb{E}[r+\gamma(1-d)Q(H',\pi_{\bar\theta}(o',P_{\bar\psi}(H'^{\mathrm{plan}}))+\epsilon)\mid H,a]$. The conditional law of $(r,H',d)$ given $(H,a)$ is environment-only (observability note). Hence for every generation lag $\Delta$:
$$
\mathbb{E}_{\text{row from }\theta_{t-\Delta}}[y\mid H,a]-\mathcal{T}Q(H,a)=0 .
$$
Non-stationarity in this regime is limited to (i) the target action map $\pi_{\bar\theta}\circ P_{\bar\psi}$, which is re-evaluated with current target weights and slowed by the task-only EMA $\bar\theta$ (baseline 04 §4.2), and (ii) coverage: old rows are on the wrong *state-action distribution*, not the wrong *operator*. **Consequence: the drift gate of §2.2 must not be applied in the $K_{\mathrm{hold}}=1$ regime.** It would discard unbiased data. Only the diagnostics (§2.1) and burn-in (§2.3) apply there.

### 1.2 Macro-$z$ regime: the exact staleness bias

Define the macro operator under low-level parameters $\theta$:
$$
(\mathcal{T}_\theta Q)(H,z)=\mathbb{E}_{\tau\sim p_\theta(\cdot\mid H,z)}[g(\tau)],\qquad
p_\theta(\tau\mid H,z)=\prod_{j=0}^{k-1}\pi_\theta(a_{t+j}\mid o_{t+j},z)\,P(o_{t+j+1}\mid H_{t+j},a_{t+j}).
$$
A row of lag $\Delta$ is an unbiased sample of $\mathcal{T}_{\theta_{t-\Delta}}Q$, not of $\mathcal{T}_{\theta_t}Q$. The **per-row conditional target bias** is
$$
b_\Delta(H,z)\;=\;\mathbb{E}_{p_{\theta_{t-\Delta}}}[g]-\mathbb{E}_{p_{\theta_t}}[g].
$$

**Proposition 1.2 (B-drift invariance of macro labels).** For fixed $\theta$ (actor and its normalizer), $b_\Delta(H,z)$ is independent of $(\omega_{t-\Delta},\omega_t)$, including the motion-normalizer state.

*Proof.* $p_\theta(\tau\mid H,z)$ contains $\pi_\theta$ and $P$ only. $B_\omega$ is used in rollout only to *choose* $z$ at the boundary (`expert`/`near`), i.e. it enters the distribution of the conditioning variable, not the conditional. $g$ uses $Q_{\bar\phi},P_{\bar\psi}$, neither of which reads $B$. ∎

So "historical `behavior_z` executed under older $(\omega,\theta)$" is stale **only through $\theta$**. The $\omega$-dependence of a stored expert row (its vector was $B_{\omega_{t-\Delta}}(m_{\mathrm{demo}})$) is harmless *as long as the label is kept as the executed vector*. Rejected alternative §3.1 shows that re-encoding destroys this property.

**Exact KL of the macro trajectory law.** Dynamics cancel in the likelihood ratio (same $P$), so the chain rule gives, exactly,
$$
\mathrm{KL}_\Delta(H,z):=\mathrm{KL}\big(p_{\theta_{t-\Delta}}\|p_{\theta_t}\big)=\mathbb{E}_{p_{\theta_{t-\Delta}}}\Big[\sum_{j=0}^{k-1}\kappa_j\Big],\quad
\kappa_j=\sum_{i=1}^{29}\Big[\log\tfrac{\sigma^{\mathrm{now}}_{i}}{\sigma^{\mathrm{then}}_{i}}+\tfrac{(\sigma^{\mathrm{then}}_i)^2+(\Delta\mu_{i})^2}{2(\sigma^{\mathrm{now}}_i)^2}-\tfrac12\Big],
$$
with $\Delta\mu=\mu_{\theta_t}(o_{t+j},z)-\mu_{\theta_{t-\Delta}}(o_{t+j},z)$. For a shared fixed $\sigma$: $\kappa_j=\|\Delta\mu_j\|^2/(2\sigma^2)=\Delta_\pi(o_{t+j},z)^2/(2\sigma^2)$, where $\Delta_\pi$ is the brief's behavioural drift. Clipping is a deterministic post-map applied identically to both laws, so by data processing the KL of the *applied*-action trajectory law is $\le$ this pre-clip value.

**Two bias bounds (both exact inequalities).**
1. Pinsker / total variation: $|b_\Delta|\le \operatorname{span}(g)\,\mathrm{TV}\le\operatorname{span}(g)\sqrt{\mathrm{KL}_\Delta/2}$.
2. Cauchy–Schwarz / $\chi^2$. With $\rho=dp_{\theta_t}/dp_{\theta_{t-\Delta}}=\prod_j \pi_{\theta_t}(a_{\mathrm{raw},j}\mid\cdot)/\pi_{\theta_{t-\Delta}}(a_{\mathrm{raw},j}\mid\cdot)$ and $\mathbb{E}_{\mathrm{then}}[\rho]=1$:
$$
|b_\Delta|=\big|\operatorname{Cov}_{\mathrm{then}}(1-\rho,g)\big|\le\sqrt{\operatorname{Var}_{\mathrm{then}}(g)\;\chi^2(p_{\theta_t}\|p_{\theta_{t-\Delta}})},\qquad \chi^2=\mathbb{E}_{\mathrm{then}}[\rho^2]-1 .
$$
   For one Gaussian step with shared $\sigma$, $\mathbb{E}[\rho_j^2\mid o]=\exp(\|\Delta\mu_j\|^2/\sigma^2)=e^{2\kappa_j}$. Over a macro, $\chi^2\le\exp\big(\sum_j\sup_o\|\Delta\mu_j\|^2/\sigma^2\big)-1$. Equality ($\chi^2=e^{2\mathrm{KL}}-1$) holds when $\Delta\mu$ is state-independent.

The $\chi^2$ form is the useful one because it scales with $\mathrm{sd}(g)$ rather than the worst-case span. In the author dry run (synthetic 10-step plant, $\sigma=0.2$, 20 000 MC rollouts per row, `spike_sketch_output.json`):

| Injected actor drift | $\overline{\mathrm{KL}}$ (nats/macro) | observed $\lvert b\rvert$ | $\chi^2$ bound | Pinsker bound | $\hat\chi^2$ |
|---|---:|---:|---:|---:|---:|
| 0.001 | 0.015–0.019 | ≤ 0.021 | 0.07–0.09 | 1.7–1.8 | 0.03–0.04 |
| 0.003 | 0.10–0.11 | ≤ 0.045 | 0.20–0.23 | 4.3–4.5 | 0.20–0.26 |
| 0.01 | 1.1–2.2 | ≤ 0.077 | 1.6–2.8 | 14–20 | 12–49 |

Both bounds held on all 9 rows. The $\chi^2$ bound is 15–25× tighter than Pinsker, but it is still a worst-case certificate and runs 3–10× above the observed bias. $\hat\chi^2$ explodes once KL exceeds about 1. This matters for the IS arm (§2.2, §3.4).

**Fixed-point error under an age mixture.** Let replay ages have data-weights $w_\Delta(H,z)$ and let $\mathcal{T}_{\mathrm{mix}}=\sum_\Delta w_\Delta\mathcal{T}_{\theta_{t-\Delta}}$. Both $\mathcal{T}_{\mathrm{mix}}$ and $\mathcal{T}_{\theta_t}$ are sup-norm contractions with modulus $\gamma_{\mathrm{eff}}=\sup_{H,z}\mathbb{E}[\gamma_{\mathrm{task}}^k(1-d)\mid H,z]$. Interior macros give $\gamma^K_{\mathrm{task}}$; timeout-truncated short macros can raise this toward $\gamma_{\mathrm{task}}$. Therefore
$$
\|Q_{\mathrm{mix}}^\star-Q_{\theta_t}^\star\|_\infty\le\frac{\sup_{H,z}\sum_\Delta w_\Delta(H,z)\,|b_\Delta(H,z)|}{1-\gamma_{\mathrm{eff}}}\le\frac{\sup\sum_\Delta w_\Delta\sqrt{\operatorname{Var}_\Delta(g)\,\chi^2_\Delta}}{1-\gamma_{\mathrm{eff}}}.
$$
This uses the "frozen target" idealisation, with $\mathcal{T}$ evaluated on a fixed $\bar V$. With $\gamma_{\mathrm{task}}=0.99$ and $K=10$, $1/(1-\gamma^{10})\approx 10.5$: staleness bias is amplified about 10× at the fixed point.

**Exact staleness variance (law of total variance).** For the regression target at $(H,z)$:
$$
\operatorname{Var}_{\mathrm{mix}}(y\mid H,z)=\underbrace{\textstyle\sum_\Delta w_\Delta\operatorname{Var}_\Delta(g)}_{\text{within-generation}}+\underbrace{\textstyle\sum_\Delta w_\Delta\big(m_\Delta-\bar m\big)^2}_{\text{between-generation ("staleness variance")}},\quad m_\Delta=\mathbb{E}_{\theta_{t-\Delta}}[g],\ \bar m=\textstyle\sum w_\Delta m_\Delta .
$$
The second term is irreducible noise for the critic regression. Its minimiser is $\bar m$, which is biased by $\bar m-m_0=\sum_\Delta w_\Delta b_\Delta$.

### 1.3 Prompt drift: exact identities for $\Delta_B$

With $\|B\|_2=\sqrt{d_z}$ for both encoders, the brief's encoder drift satisfies, exactly,
$$
\Delta_B(m)=1-\tfrac{1}{d_z}\langle B_{\omega_t}(m),B_{\omega_{t-\Delta}}(m)\rangle=1-\cos\alpha_m,\qquad \|B_{\omega_t}(m)-B_{\omega_{t-\Delta}}(m)\|_2^2=2d_z\,\Delta_B(m).
$$
**Calibration against the deliberate `near` perturbation.** `near-z` rotates by $\alpha\in[10^\circ,20^\circ]$, i.e. $\Delta\in[1-\cos10^\circ,1-\cos20^\circ]=[0.0152,0.0603]$. An expert prompt whose encoder drift exceeds $0.0152$ has moved further than the smallest exploration perturbation the program deliberately injects. I use this as the *alarm* level for expert-prompt drift. It is not a gate (Prop. 1.2).

### 1.4 The gauge symmetry: why $\Delta_B$ cannot certify staleness

**Proposition 1.4 (exact $O(d_z)$ symmetry of the joint objective).** Take $R\in O(d_z)$ and the transformation
$B\mapsto RB$, $F(o,a,z)\mapsto RF(o,a,R^\top z)$, $\pi(o,z)\mapsto\pi(o,R^\top z)$, $P\mapsto RP$, $Q(H,c,z)\mapsto Q(H^R,c,R^\top z)$, where $H^R$ feeds $R^\top z_{t-1}$. It leaves invariant, in distribution, the FB loss (baseline 04 §4.1), $\mathcal L_{\mathrm{orth}}$, the actor loss $\min_k F_k^\top z$, the `z_update` law (uniform sphere part: isotropic; goal part: $RB(m)$ rotates with $B$), the `near` law (isotropic tangent noise), the B01 whitening (covariant: $W\mapsto RWR^\top$), and the macro critic and planner losses. It is realised in parameter space by absorbing $R$ into the last linear layer of $B$ and $P$ and the first $z$-input linear layer of $F,\pi,Q$. This works because $\operatorname{proj}$ is rotation-equivariant and every pre-linear operation acts on non-$z$ inputs. ∎

*Premise to verify in code:* no per-coordinate operation acts on $z$ before its first linear layer. Example: an input normalizer over a concatenated $(o,z)$ vector breaks the symmetry. If one exists, Prop. 1.4 fails and the B-drift decomposition below is reported but not interpreted.

*Consequence.* Minibatch gradients are not invariant (the sampled $z_{\mathrm{random}}$ vectors do not rotate), but their expectation is orthogonal to the orbit. Gradient noise therefore drives a zero-curvature **random walk along the gauge orbit**. This is a conjecture about the dynamics, to be measured, not a theorem. Along that walk, $\Delta_B$ can be large with zero physical change, while every stored $z_{\mathrm{actual}}$ becomes stale *because* $\pi$ co-rotates: $\pi_{\mathrm{now}}(o,z)=\pi_{\mathrm{then}}(o,R^\top z)\neq\pi_{\mathrm{then}}(o,z)$. Hence:

- **Gauge/deformation split (exact).** On a probe set, let $\hat R=\arg\max_{R\in O(d_z)}\sum_i\langle B_{\mathrm{now}}(m_i),RB_{\mathrm{then}}(m_i)\rangle=UV^\top$, where $U\Sigma V^\top=\mathrm{SVD}(\sum_iB_{\mathrm{now}}B_{\mathrm{then}}^\top)$. Define $\Delta_B^{\mathrm{def}}=1-\tfrac1{Nd_z}\sum_i\langle B_{\mathrm{now}},\hat RB_{\mathrm{then}}\rangle$ and $\Delta_B^{\mathrm{gauge}}=\Delta_B^{\mathrm{tot}}-\Delta_B^{\mathrm{def}}\ge0$ ($R=I$ is admissible). Dry run: under a synthetic pure rotation, $\Delta_B^{\mathrm{tot}}=1.027$ and $\Delta_B^{\mathrm{def}}=-7\times10^{-11}$.
- **Gauge-aligned behavioural drift.** $\Delta_\pi^{\hat R}(o,z)=\|\mu_{\mathrm{now}}(o,\hat Rz)-\mu_{\mathrm{then}}(o,z)\|$. If $\Delta_\pi^{\hat R}\ll\Delta_\pi$, staleness is mostly gauge. That fact is useful (§3.3), but it does not license relabeling under the current charter.

### 1.5 Normalizer ("BN") contract: exact distribution shift and variance error

The baseline normalizers (`obs_normalizer`, `motion_normalizer`) are running mean/variance input normalizers; $B$ uses LayerNorm internally. I treat two implementations, since the R2.1 class is not specified in the frozen set: **(C)** count-weighted cumulative merge (Welford/Chan), and **(E)** EMA with momentum $\beta$ (`torch.nn.BatchNorm1d` running statistics, PyTorch default $\beta=0.1$). The contract per `FBAgent.update` is: motion normalizer gets $m_{\mathrm{cur}}$ once and $m_{\mathrm{next}}$ once (likewise `obs`/`next_obs`), then freeze (`eval`/`no_grad`) for `z_update`, expert/`near` encoding, the target $\bar B$ pass, and all evaluation.

**(C) stationary statistics.** If update calls feed sources $s$ with row counts $c_s$ per update, the cumulative estimator converges to the mixture moments
$$
\hat\mu_\infty=\sum_s\tfrac{c_s}{C}\mu_s,\qquad \hat\sigma^2_\infty=\sum_s\tfrac{c_s}{C}\big(\sigma_s^2+(\mu_s-\hat\mu_\infty)^2\big),\qquad C=\textstyle\sum_s c_s .
$$

| Violation | Per-update sources | Stationary mean | Bias vs contract $\mu^\star=\tfrac12(\mu_c+\mu_n)$ |
|---|---|---|---|
| Contract | $m_c\!:\!n,\ m_n\!:\!n$ | $\tfrac12(\mu_c+\mu_n)$ | 0 |
| Double `m_next` | $m_c\!:\!n,\ m_n\!:\!2n$ | $\tfrac13\mu_c+\tfrac23\mu_n$ | $\tfrac16(\mu_n-\mu_c)$ |
| Update during `z_update` relabel (`m_next[perm]` is the same multiset) | same as double `m_next` | same | $\tfrac16(\mu_n-\mu_c)$ |
| Update during expert/near queries, $n_e$ rows/update | $+\ \rho_{\mathrm{demo}}\!:\!n_e$ | $\frac{n(\mu_c+\mu_n)+n_e\mu_{\mathrm{demo}}}{2n+n_e}$ | $\frac{n_e}{2n+n_e}(\mu_{\mathrm{demo}}-\mu^\star)$ |

Variance error: substitute the row's source weights into $\hat\sigma^2_\infty$. Each violation adds the cross term $\tfrac{c_s}{C}(\mu_s-\hat\mu)^2$ and reweights the within-source variances. Dry run for the combined bug (relabel + 8 expert rows per update, $\mu_c=0$, $\mu_n=0.3$, $\mu_{\mathrm{demo}}=1$, $n=256$): predicted $0.20825$, measured $0.20844$.

**Telescoping identity (sizes $\mu_n-\mu_c$ exactly).** For any replay content that is a union of contiguous segments $\mathcal{G}$ (whole episodes, or FIFO-truncated episodes), the multisets $\{m_{\mathrm{next}}\}$ and $\{m_{\mathrm{cur}}\}$ differ only at segment ends:
$$
\mu_n-\mu_c=\frac{1}{N}\sum_{G\in\mathcal G}\big(m_{\mathrm{last}}(G)-m_{\mathrm{first}}(G)\big)=\frac{1}{\bar L}\Big(\overline{m}_{\mathrm{last}}-\overline{m}_{\mathrm{first}}\Big),
$$
where $\bar L$ is the mean segment length (dry-run error $7.8\times10^{-8}$). The "last" frames are disproportionately committed failure frames (`severe_penetration`, falls) and success frames; the "first" frames are standing resets. **Quantitatively, the double-`m_next` bias in (C) is small**, $\approx\|\bar m_{\mathrm{last}}-\bar m_{\mathrm{first}}\|/(6\bar L)$ (sub-1% of $\sigma$ for $\bar L\gtrsim100$ on most coordinates), but it is **deterministic and sign-coherent**: it shifts the normalizer toward failure kinematics. Expert-query contamination is not small: $\mu_{\mathrm{demo}}$ is a single 0.704 m traversal clip, far from replay early in training, so its bias is $O(n_e/2n)\cdot\|\mu_{\mathrm{demo}}-\mu^\star\|$. It also makes the backward map depend on the demonstration distribution through the normalizer, which violates the spirit of Charter §2.1–2.2: demonstrations as prompts only.

**(E) EMA fixed point at read time.** With a periodic call pattern, the running mean read after the last call of each update converges to
- contract $[c,n]$: weight on $\mu_n$ $=\dfrac{1}{2-\beta}$ ($0.5263$ at $\beta=0.1$; dry run $0.5262$);
- double-next $[c,n,n]$: weight on $\mu_n$ $=\dfrac{2-\beta}{3-3\beta+\beta^2}$ ($0.7011$; dry run $0.7011$).

The bias is therefore $0.175(\mu_n-\mu_c)$ at $\beta=0.1$: about 1.05× the (C) value ($1/6\approx0.167$). Note that even the *correct* EMA weights `m_next` slightly more than $\tfrac12$. That is a read-time-phase property of EMA and not a violation.

**Train-mode batch statistics (the severe case).** If `encode_motion` or `sample_ufo_mixed_z` runs a true `BatchNorm` in train mode, the output normalizes with **the query batch's own** mean and variance. Per coordinate, $\tilde x_{\mathrm{wrong}}=a\tilde x+b$ with $a=\sigma/\hat\sigma_b$ and $b=(\mu-\hat\mu_b)/\hat\sigma_b$, and $\mathbb{E}\|\tilde x_{\mathrm{wrong}}-\tilde x\|^2=\sum_i\mathbb{E}[(a_i-1)^2\tilde x_i^2+b_i^2]\approx D\cdot\frac{3}{2n_e}$ for in-distribution Gaussian batches: $1/(2n_e)$ from the scale and $1/n_e$ from the shift. Dry run: $0.194$ vs $0.1875$ at $n_e=8$, and $0.0235$ vs $0.0234$ at $n_e=64$. On top of this, the systematic term $a_i=\sigma_{\rho,i}/\sigma_{\mathrm{demo},i}$, $b_i=(\mu_{\rho,i}-\mu_{\mathrm{demo},i})/\sigma_{\mathrm{demo},i}$ re-centres demo frames on *the demo distribution*. The encoding also becomes non-idempotent and batch-composition-dependent: $z_{\mathrm{exp}}$ for frame $m$ depends on which other envs hit a boundary in the same step. $n_e=1$ is undefined (zero variance).

**Propagation to $z$.** For input perturbation $\delta\tilde x$, to first order $\mathbb{E}\|\delta B\|^2\approx\operatorname{tr}(J_B\operatorname{Cov}(\delta\tilde x)J_B^\top)+\|J_B\mathbb{E}\delta\tilde x\|^2$, and $\Delta_B=\mathbb{E}\|\delta B\|^2/(2d_z)$ by §1.3. The spike measures $\Delta_B$ directly rather than relying on the linearisation.

### 1.6 Short macros, terminal boundary, and RNN state

- **Short-macro discount.** For $k<K$: (i) termination (incl. `severe_penetration`, $\Phi_{\mathrm{next}}=0$) gives $y=R^{(k)}$; (ii) timeout truncation gives $y=R^{(k)}+\gamma^k\bar V(H_{t+k})$. Using $\gamma^K$ on a truncated row has exact bias $(\gamma^k-\gamma^K)\bar V$. Treating truncation as termination has bias $-\gamma^k\bar V$. Rows containing an `invalid` transition never exist (Charter §2.4); the uncommitted episode is discarded whole, so burn-in never sees a fabricated prefix.
- **Stale cached hidden states.** A hidden state cached at collection is $h_{t_0}^{\mathrm{then}}=f_{\phi_{t-\Delta}}(x_{0:t_0})$. Using it with current weights computes neither $Q_{\phi_t}$ nor $Q_{\phi_{t-\Delta}}$ on $H_{t_0}$. Its error has no general bound below the network's sensitivity to $\phi$; dry run (2-layer LSTM-128, 200 Adam steps at $3\cdot10^{-4}$): max error $1.10$. Full-prefix recomputation from $(h_0,c_0)=0$ with current weights is exact by construction (dry run: $0.0$).

---

## 2. Algorithmic Design for Non-Stationarity Mitigation and Controllability Diagnostics

### 2.0 New immutable replay columns (write-once, collection-time only)

In `TaskEpisodeReplay` (per control step) and `FBReplay`, alongside the existing `behavior_z`/`z_actual`, `generation`, `source`:

| Column | Shape | Content | Consumers |
|---|---|---|---|
| `behavior_mu` | `[29]` fp16 | pre-noise actor mean $\mu_{\theta_{\mathrm{then}}}(o_t,z_{\mathrm{actual}})$ in pre-clip space | diagnostics D2, gate M1, IS arm M3 |
| `behavior_log_std` | `[29]` fp16, or scalar per generation if $\sigma$ fixed | $\log\sigma_{\theta_{\mathrm{then}}}$ | same |
| `a_raw` | `[29]` fp16 | pre-clip sampled action (`a_applied` already stored) | IS arm M3 |
| `prompt_anchor_z` | `[d_z]` fp16, `expert`/`near` rows only | $z_{\mathrm{exp}}=\operatorname{proj}B_{\omega_{\mathrm{then}}}(m_{\mathrm{demo}})$ before the `near` rotation | D3 |
| `prompt_frame_id` | `int16`, `expert`/`near` rows only | NPZ row index | D3 **logging only** |

**Firewall on `prompt_frame_id`.** Charter §2.3 forbids frame indices as *network inputs*. The column is excluded from every input schema, and a schema test asserts that no module's `forward` signature or input-spec registry references it. Storage: about 59 floats per step ≈ 120 B fp16. At 50k macros × 10 steps that is about 60 MB, which fits the existing replay budget.

**Immutability enforcement.** Buffers are allocated once. `sample()` returns `.clone()`d views, never storage aliases. `FBAgent.update` asserts `z_update.data_ptr()` is disjoint from replay storage. In debug/CI mode, a per-row CRC32 over (`behavior_z`, `behavior_mu`, `a_raw`) is checked on each sample. The macro target and the critic/planner burn-in read `z_actual`/`z_{t-1}` from these columns only.

### 2.1 Online diagnostic suite

All diagnostics run under `torch.no_grad()` (except D4, which uses `torch.func.jvp`), with all normalizers frozen. Their outputs never enter any loss, normalizer, or replay. Cadence is in FB updates.

**D1 — Normalizer contract guard (every update, O(1)).** Per normalizer, `update_calls` delta must equal exactly 2 inside `FBAgent.update` and 0 elsewhere. A 64-bit hash of `(mean,var,count)` must be identical before and after every `encode_motion`, `sample_ufo_mixed_z`, target pass, and evaluation panel. A violation raises the contract error and halts the run. It is logged as a contract breach, distinct from `invalid` physics.

**D2 — Behavioural drift $\Delta_\pi$ and trajectory KL, snapshot-free (every $U_d=250$ updates).** For each live generation bucket $g$ (R2.1 `generation` tag; buckets of 1 000 macros if the tag is finer), sample $n_g=32$ macro rows. Compute $\mu_{\theta_t}(o_{t+j},z_{\mathrm{actual}})$ for $j<k$ and report:
- $\Delta_\pi^{\mathrm{rms}}(g)=\big(\operatorname{mean}_{\mathrm{rows},j}\|\mu_{\theta_t}-\texttt{behavior\_mu}\|^2\big)^{1/2}$;
- $\overline{\mathrm{KL}}_g=\operatorname{mean}_{\mathrm{rows}}\sum_{j<k}\kappa_j$ (exact Gaussian formula, §1.2);
- $\hat\chi^2_g=\operatorname{mean}_{\mathrm{rows}}\rho^2-1$ with $\log\rho=\sum_j[\log\pi_{\theta_t}(a_{\mathrm{raw},j})-\log\pi_{\mathrm{then}}(a_{\mathrm{raw},j})]$, both from stored columns;
- the age profile $\overline{\mathrm{KL}}$ vs $\Delta=t-g$, split by `source`.

Dry run: the stored-column $\Delta_\pi$ equals snapshot recomputation to $0.0$.

**D3 — Encoder drift $\Delta_B$ with gauge split (every $U_d$ updates).**
- *Prompt drift, snapshot-free:* for sampled `expert`/`near` rows, $\Delta_B^{\mathrm{prompt}}=1-\langle B_{\omega_t}(m_{\mathrm{demo}}[\texttt{prompt\_frame\_id}]),\texttt{prompt\_anchor\_z}\rangle/d_z$. Alarm at $>1-\cos10^\circ=0.0152$ (§1.3).
- *Replay-frame drift:* keep a geometric ring of $B$ snapshots (weights + motion-normalizer stats) at ages $\{1,2,4,8,16,32\}$ buckets. $B$ is small: about 0.13 M params (obstacle) or 0.54 M (ball), so 6 snapshots ≤ 13 MB. Each snapshot carries a fixed probe set of 4 096 valid committed `m_next` frames taken at snapshot time. Report $\Delta_B^{\mathrm{tot}},\Delta_B^{\mathrm{def}},\Delta_B^{\mathrm{gauge}}$ via the $d_z\times d_z$ Procrustes SVD (§1.4).
- *Gauge-aligned behavioural drift* $\Delta_\pi^{\hat R}$ on the D2 rows, using the Procrustes $\hat R$ from the snapshot nearest in age.

**D4 — Action sensitivity (every $U_d$ updates).** On 512 $(o,z)$ pairs (recent replay $o$; $z$ drawn equally from executed planner $z$, expert $z$, and the uniform sphere), estimate the tangent-projected Jacobian norm with $r=4$ Hutchinson probes:
$$
S_\pi=\mathbb{E}\big[\|J_z\mu_\theta(o,z)\,P_\perp(z)\|_F\big],\quad \|JP_\perp\|_F^2=\mathbb{E}_{v\sim\mathcal N(0,I)}\|J\,P_\perp v\|^2,\quad P_\perp=I-zz^\top/d_z .
$$
Each probe is one `torch.func.jvp`. Also report the per-radian gain $\sqrt{d_z}\,\|JP_\perp u\|$ for unit tangent $u$, which is directly comparable to the 10–20° `near` rotation, and the tanh/clip saturation fraction $\Pr(|\mu_i|>0.99)$, which suppresses $S_\pi$ independently of $z$-semantics.

**D5 — Multi-step trajectory divergence / controllability (every 50 000 control steps).** Use a dedicated pool of 64 diagnostic envs that never write replay or normalizers and run with frozen weights. From cloned simulator states sampled from recent episodes (MuJoCo `mjData` copy), roll out $K$ and $5K$ steps with command pairs at angles $\alpha\in\{0^\circ,10^\circ,20^\circ,45^\circ,90^\circ\}$, in two modes: (i) stochastic with independent noise; (ii) deterministic means. Report
$$
\mathcal D_k(\alpha)=\tfrac1k\textstyle\sum_{j\le k}\|\tilde m^{(1)}_j-\tilde m^{(2)}_j\|_2/\sqrt{D_m}\ \ (\text{frozen-normalized motion}),\qquad \mathcal C(\alpha)=\mathcal D_k(\alpha)/\mathcal D_k(0^\circ)\ \text{(stochastic mode)} .
$$
**Alarms:** $\mathcal C(20^\circ)<1.2$ ("$z$ ignored": the `near` exploration is behaviourally void); non-monotone $\mathcal D^{\det}(\alpha)$; or $\|\nabla_zQ_{\phi_1}\|$ large while $\mathcal C\approx1$, which by C-B02-A-03 means the planner gradient is pure critic error.

**Overhead budget (target < 5 % wall-clock per update; to be measured in the GPU stage of §5, not asserted).** Rough estimate, assuming the R2.1 residual 2048×6 actor (≈ 25 M params) and FB batch 1 024 with two residual F heads. A full FB update is ≳ 1 TFLOP. Per diagnostic tick, D2 runs $\le50\cdot32\cdot10=16\,000$ actor forwards ≈ 0.8 TFLOP; amortised over $U_d=250$ that is ≈ 0.3 %. D3 and D4 together add ≈ 0.2 %. D5 runs on separate envs every 50k steps, and its wall-clock share is reported separately. M1 adds no per-update cost beyond D2. M3 adds $B_Q\cdot K$ actor forwards per critic update (≈ 1–2 %).

### 2.2 Mitigation: drift-gated replay horizon (macro-$z$ regime only)

**M1 — Generation-level gate (primary).** Every $U_d$ updates, after D2:
```
g_cut ← oldest bucket g such that KL̄_{g'} ≤ ε_KL for every bucket g' ≥ g        # contiguous from newest
g_cut ← min(g_cut, newest − G_min + 1)  and enforce |admitted| ≥ N_min               # floors
g_cut ← max(g_cut, g_cut_prev)                                                        # monotone: no re-admission
admitted ← { rows : generation ≥ g_cut }  ∩  FIFO window (50k macros, baseline)
critic TD batches sample uniformly from `admitted`; planner (delay=2) samples H_t from the same set
```
Defaults: $\varepsilon_{\mathrm{KL}}=0.02$ nats/macro, $G_{\min}=2$, $N_{\min}=8\,192$ macros. At $\varepsilon=0.02$ and state-independent $\Delta\mu$, $\chi^2=e^{0.04}-1\approx0.04$, so the certificate is $|b_g|\le0.2\,\mathrm{sd}(y)$. The dry run observed about 10× below the certificate. The value is pre-registered with a sweep $\{0.01,0.02,0.05,0.2,\infty\}$ ($\infty$ = baseline FIFO).

*Why generation-level, not row-level.* $\mathrm{KL}_{\mathrm{row}}$ is computed on the row's own realised states $o_{t+j}(\tau)$, so gating on $\mathbf 1[\mathrm{KL}_{\mathrm{row}}\le\varepsilon]$ conditions on $\tau$. The admitted target is then $\mathbb{E}_{\mathrm{then}}[g\mid H,z,\mathrm{KL}_{\mathrm{row}}(\tau)\le\varepsilon]\ne\mathbb{E}_{\mathrm{then}}[g\mid H,z]$: a new selection bias. For example, low-KL trajectories may be precisely the ones that fell early, with $k$ small and few steps to diverge. The generation gate depends only on the bucket index and on other rows' statistics: with $n_g=32$ out of ~1 000 rows per bucket, the influence is ≤ 3 %, and it is removed entirely by drawing the D2 sample from a held-aside 3 % of each bucket that is never used for TD. So it introduces no within-row selection.

**M2 — Exact short-macro discount and burn-in (mandatory, both regimes).** Per §1.6, always use $\gamma^k_{\mathrm{task}}$ with the stored $k$ and $(1-\texttt{terminated})$. Unit-test both bug forms. Burn-in is in §2.3.

**M3 — Truncated importance weights inside the gate (ablation arm, not default).** Weight each admitted row's TD loss by $\bar\rho=\min(\rho,\bar c)$ with $\bar c=2$, using stored `a_raw`/`behavior_mu`/`behavior_log_std`. Inside the gate $\chi^2\lesssim0.04$, so truncation is rarely active and the arm is close to unbiased. It is not default because: (i) its variance grows as $e^{2\mathrm{KL}}$, which in the dry run gave $\hat\chi^2=12$–$49$ at KL 1.1–2.2 and IS error up to about 8× the plain-MC SE; (ii) the gate already holds the residual bias within the certificate. M3 exists to test whether that residual is practically material.

**M4 — Soft lag weighting (ablation arm, brief option b).** Sample admitted rows with probability $\propto\exp(-\overline{\mathrm{KL}}_g/\varepsilon_{\mathrm{KL}})$ instead of a hard cut. This is still generation-level, so there is no selection bias.

**What is deliberately *not* done.** `z_actual`/`behavior_z` are never rewritten, rotated, re-encoded, or shadowed. The critic input is always the executed vector (Charter §2.2). No pre-training or freezing of $B_\omega,\pi_\theta$ (brief §2). The gate touches only *which* rows train $Q$/$P$. `FBReplay` and the FB/actor losses are untouched, because FB updates relabel with fresh `z_update` and are off-policy-correct by construction.

### 2.3 Full-prefix zero-hidden burn-in with exact shared-prefix deduplication

For each sampled slice $[t_0,t_0+L)$ of an episode:
1. Group the sampled slices by episode id. For each episode, unroll **once** from $(h_0,c_0)=0$ at step 0 to $\max t_0$ under `no_grad`, recording the hidden state at every requested $t_0$. This is exact, because it is the same computation as per-slice burn-in, and it costs $O(\sum_{\mathrm{episodes}}\max t_0)$ rather than $O(\sum_{\mathrm{slices}}t_0)$.
2. Inputs are the stored executed stream $(o_t,\ z_{t-1}=\text{executed }z_{\mathrm{actual}},\ \texttt{first\_flag})$, never `z_update` or a re-encoded prompt.
3. Run separate unrolls for the online $Q_{\phi_{1,2}}$, target $Q_{\bar\phi_{1,2}}$, online $P_\psi$ (planner loss), and target $P_{\bar\psi}$ (target $z$), each with its current weights. The target $H_{t+k}$ uses the target unroll continued past $t_0+L$ where needed.
4. BPTT over $[t_0,t_0+L)$ only.

No hidden state is ever persisted in replay. A versioned hidden-state cache is not exact under per-step weight updates, so it is rejected.

---

## 3. Serious Alternative Considered and Rejected

Per method §11.5. §3.1 is the primary rejected alternative; §3.2–3.4 are further rejections, with reasons.

### 3.1 Rejected (primary): retrofitting historical `behavior_z` by re-encoding through the current $B_\omega$

*Proposal under consideration.* At TD time, replace a row's label $z_{\mathrm{actual}}$ with $z'=\operatorname{proj}B_{\omega_t}(m^\dagger)$. Here $m^\dagger$ is either (a) the demo frame the prompt came from (`expert`/`near` rows), or (b) a realised frame of the macro (e.g. $m_{t+k}$) for rows with no demo source. The motivation is to "refresh" stale commands into current coordinates (brief option (c)).

*Why rejected.*
1. **It adds bias where there was none.** Take the regime where only $B$ has drifted ($\Delta_\pi\equiv0$). By Prop. 1.2, keeping $z_{\mathrm{actual}}$ gives $b=0$ exactly. Case (a) gives the target $\mathcal T_\theta Q(H,z_{\mathrm{actual}})$ attached to input $z'$, with bias $\mathcal T_\theta Q(H,z_{\mathrm{actual}})-\mathcal T_\theta Q(H,z')$. That is nonzero whenever $\mathcal T_\theta Q(H,\cdot)$ is non-constant on the arc of length $\alpha=\arccos(1-\Delta_B)$. To first order it equals $\langle\nabla_z\mathcal T Q,\ z_{\mathrm{actual}}-z'\rangle$, with $\|z_{\mathrm{actual}}-z'\|=\sqrt{2d_z\Delta_B}$. Dry run: keeping gives a bias of exactly $0$ under common random numbers; re-encoding at $\Delta_B=0.018$ (≈ 10.9°) gives $0.0154\pm0.0042$ (3.7 SE). Re-encoding is strictly dominated whenever $\Delta_\pi=0$. When $\Delta_\pi\ne0$, it has no reason to help either: the stale component is $\theta$-driven, and the re-encoded vector is a different command that neither $\pi_{\mathrm{then}}$ nor $\pi_{\mathrm{now}}$ executed.
2. **Case (b) is hindsight relabeling of a task critic.** $z'(\tau)$ is a function of the outcome, so the admitted conditional is $\mathbb{E}_{\mathrm{then}}[g\mid H,z,\,B(m_{t+k}(\tau))=\zeta]$, not $\mathcal T Q(H,\zeta)$. HER-style relabeling is valid only when the reward is defined by the relabeled goal. Here $r^{\mathrm{task}}$ is fixed and $z$ is a command, so the relabel is biased by construction. It also cannot reproduce a planner row at all, and planner rows are 70 % of rows after $S_{\mathrm{ramp}}$.
3. **It violates the frozen contract.** Charter §2.2 requires that $Q$ train on the executed $z_{\mathrm{actual}}$ and that labels are never overwritten. A shadow column read by $Q$ is the same violation in a different place.
4. **It cannot address the dominant mechanism.** Under gauge drift (Prop. 1.4), a refreshed $z'=B_{\omega_t}(m)$ is rotated *with* $B$. Yet the row's return came from $\pi_{\mathrm{then}}(\cdot,z_{\mathrm{actual}})$, and $\pi_{\mathrm{now}}$ applied to $z'$ reproduces $\pi_{\mathrm{then}}(\cdot,z_{\mathrm{actual}})$ only if $\pi$ is exactly gauge-equivariant *and* $B$ is a pure rotation. That is the $\Delta_\pi^{\hat R}\approx0$ case, which is measured (D3), not assumed.

### 3.2 Rejected: freeze a pre-trained imitation $B_\omega/\pi_\theta$ before task training

Freezing gives $\Delta_\pi\equiv\Delta_B\equiv0$, and all staleness bias vanishes. It is rejected because: (i) it violates brief §2 ("must not introduce pre-training stages or freeze $B_\omega/\pi_\theta$"); (ii) it removes the mechanism the program studies (baseline 02 §3.3): $B$ must keep grounding *newly discovered* postures such as hand support and stumble recovery, and a frozen $B$ fitted on an 859-frame, single-height (0.704 m) support has only its support projection identifiable (C-B01-B-02), so planner commands off that support have arbitrary meaning; (iii) a pre-training stage on the demo distribution makes the demo the *training* distribution of $B$ rather than a prompt source, which edges toward the imitation-anchored regime of the AMP/pretrained-skill column in baseline 02 §2. Point (iii) is a design-philosophy argument, not a theorem, and I record it as such.

### 3.3 Not adopted (requires a charter amendment): gauge-aligned critic input $\hat R\,z_{\mathrm{actual}}$

If D3 shows $\Delta_\pi^{\hat R}\ll\Delta_\pi$, feeding $Q$ the gauge-aligned vector $\hat Rz_{\mathrm{actual}}$, while storing $z_{\mathrm{actual}}$ immutably, would remove most staleness at no data cost. It is not adopted because Charter §2.2 requires $Q$ to train on $z_{\mathrm{actual}}$ itself. If the GPU stage measures $\Delta_\pi^{\hat R}/\Delta_\pi<0.3$ on ≥ 2 of 3 seeds, I recommend opening a method issue (§10.2). This is a measurement-gated follow-up, not a proposal to violate the contract.

### 3.4 Rejected as primary: row-level KL gate and untruncated per-row IS

Row-level gating introduces trajectory-selection bias (§2.2). Untruncated IS is unbiased but has variance factor $e^{2\mathrm{KL}}$, which becomes uninformative at the KL values that FIFO replay reaches. Both are retained only as an ablation arm (M3) or as a negative control.

---

## 4. Candidate Necessity Claims (Appendix B)

All are proposed at **Candidate** state. Locking requires independent verification and the human lead's signature (B.9.2).

### C-B02-A-01 — Macro-label invariance and executed-label obligation

- **Grade**: 1 (theorem-like). **Conclusion shape**: invariant + obligation.
- **Premises.**
  - P1: The macro critic's target is $g(\tau)=R^{(k)}+\gamma^k(1-d)\bar V(H_{t+k})$, evaluated with current networks.
  - P2: The environment transition and reward kernel, given the action-observation history, is stationary and independent of $(\omega,\theta)$.
  - P3: Within a macro, actions are drawn from $\pi_\theta(\cdot\mid o,z)$ with $z$ held fixed. $B_\omega$ does not enter $\pi_\theta$'s inputs or the rollout except through the choice of $z$ at boundaries.
  - P4: Histories include past actions and past executed $z$.
  - P5: $\pi_{\theta_t}\ll\pi_{\theta_{t-\Delta}}$ (e.g. both Gaussian).
- **Conclusion.**
  - (a) The conditional staleness bias $b_\Delta(H,z)$ of a stored row with executed label $z$ depends on $(\omega_{t-\Delta},\omega_t)$ not at all, and on $\theta$ only through $p_\theta(\tau\mid H,z)$.
  - (b) $|b_\Delta|\le\min\{\operatorname{span}(g)\sqrt{\mathrm{KL}_\Delta/2},\ \sqrt{\operatorname{Var}_{\mathrm{then}}(g)\chi^2_\Delta}\}$, with $\mathrm{KL}_\Delta$ given by the exact chain-rule sum of per-step actor KLs.
  - (c) Obligation: when $\theta_{t-\Delta}=\theta_t$, the only label $\zeta$ for which the row is an unbiased sample of $\mathcal T_{\theta_t}Q(H,\zeta)$ for all $Q$ is $\zeta=z$ up to $\mathcal T Q$-level sets. Any relabeling map $\zeta=f(\omega_t,\text{stored data})$ is biased unless $\mathcal T_{\theta_t}Q(H,\cdot)$ is constant on $\{z,\zeta\}$.
- **Implementation independence.** It holds for any parametrisation of $F,B,\pi,Q,P$ and for classical option-critic / SMDP methods. It is a statement about SMDP labels.
- **Operational test.** `B02-SPIKE` (c): keep-label bias $=0.0$ exactly under common random numbers with $B$ drifted and $\pi$ fixed; re-encode bias $>3$ SE; both bounds hold on all drift rows.
- **Falsifier.** A system satisfying P1–P5 where re-encoded labels are unbiased with $\mathcal TQ(H,z)\ne\mathcal TQ(H,\zeta)$. Any such case must violate a premise, most plausibly P3 if $B_\omega$ or its normalizer feeds the actor, or P4 if histories omit actions. A premise violation narrows scope (B.9.6 counter).

### C-B02-A-02 — Single-pass normalizer invariant

- **Grade**: 1. **Conclusion shape**: invariant.
- **Premises.**
  - P1: A running normalizer of type (C) count-weighted or (E) EMA($\beta$).
  - P2: The contract issues exactly one update on $m_{\mathrm{cur}}$ and one on $m_{\mathrm{next}}$ per FB update, then freezes.
  - P3: Replay is a union of contiguous segments.
- **Conclusion.**
  - (a) The frozen state is invariant (bitwise) under any number of `z_update`, expert, `near`, target, or evaluation queries.
  - (b) Any additional call pattern shifts the stationary statistics by exactly the mixture formulas of §1.5. The double-`m_next` (C) bias is $\tfrac16(\mu_n-\mu_c)$, where $\mu_n-\mu_c=\tfrac1N\sum_G(m_{\mathrm{last}}-m_{\mathrm{first}})$. The (E) read-time weights are $1/(2-\beta)$ vs $(2-\beta)/(3-3\beta+\beta^2)$.
  - (c) Train-mode batch statistics on a query batch of size $n_e$ give per-coordinate relative input error $\to 3/(2n_e)$ for in-distribution Gaussian batches, plus a systematic demo-recentring term.
- **Operational test.** `B02-SPIKE` (a1)–(a5).
- **Falsifier.** A normalizer of type (C)/(E) where an extra call with $\mu_s\ne\hat\mu$ leaves the stationary mean unchanged; or replay content where the telescoping identity fails, which can only happen with non-contiguous storage (scope note).

### C-B02-A-03 — Zero controllability makes the planner gradient pure critic error

- **Grade**: 1. **Conclusion shape**: impossibility.
- **Premises.** P1–P4 of C-B02-A-01, and a set $\mathcal Z\subset\mathcal S^{d_z-1}(\sqrt{d_z})$ on which $p_\theta(\tau\mid H,z)$ does not depend on $z$.
- **Conclusion.** $\mathcal T_\theta Q(H,\cdot)$ is constant on $\mathcal Z$ for every $Q$. Hence at any fixed point the true $\nabla_z Q^\star(H,z)\cdot u=0$ for tangent directions $u$ within $\mathcal Z$, and any nonzero planner gradient component along $\mathcal Z$ is critic approximation error carrying no task information. No critic architecture or planner optimiser can extract task signal from $z$-directions that $\pi$ ignores.
- **Operational test.** D5 controllability ratio $\mathcal C(\alpha)$ together with $\|P_\perp\nabla_zQ_{\phi_1}\|$. A regime with $\mathcal C\approx1$ and large $\|\nabla_zQ\|$ is the predicted pathology. Intervening on $z$ along such a direction must leave measured MC return unchanged within CI.
- **Falsifier.** An intervention study where a $z$-direction with $\mathcal C(\alpha)\approx1$ (within CI) produces a statistically significant change in MC task return. That would indicate that D5's metric misses a behaviourally relevant channel (e.g. contact force not visible in $m$, cf. B03), and it narrows the operational test rather than the theorem.

### C-B02-A-04 (supporting) — $O(d_z)$ gauge symmetry; $\Delta_B$ is not a staleness certificate

- **Grade**: 1 for the symmetry (Prop. 1.4); the diffusion conjecture is *not* claimed. **Conclusion shape**: invariant.
- **Premises.** The baseline 04/05 losses, the B01 four-site whitening, and isotropic `z_random`/`near` laws. No per-coordinate operation on $z$ before its first linear layer.
- **Conclusion.** The joint objective is invariant under the $O(d_z)$ action of Prop. 1.4. Consequently, for every $\epsilon>0$ there exist parameter pairs with $\Delta_B^{\mathrm{tot}}\ge1-\epsilon$ and identical task-relevant behaviour as a function of $B$-coordinates, and pairs with $\Delta_B=0$ on a probe set but $\Delta_\pi>0$. So no function of $\Delta_B$ alone bounds $b_\Delta$.
- **Operational test.** The spike's Procrustes check, plus a parameter-space rotation test: apply $R$ to the absorbing layers and verify the loss is unchanged to fp32 tolerance on a fixed batch with correspondingly rotated `z_random`.
- **Falsifier.** A loss term in the frozen baselines that is not rotation-invariant, which narrows scope to the invariant subgroup.

---

## 5. Pre-Registered Empirical Spike Protocol

Aligned with `packets/B02/spikes/B02-SPIKE/PLAN.md`: seed `20261023`, max 2 attempts, command `/srv/claude/.venv/bin/python …/gpu_experiments/run_b02_nonstationarity_spike.py`. The runner implements this protocol at the registered path (§12.2). My `spike_sketch.py` is a reference implementation of the CPU stage and may be adopted verbatim or rewritten. Its dry-run output is shown for calibration only. The PLAN's three metrics are the minimal pass set. Items marked **[A+]** are additions this proposal asks the adjudicator to register; they do not alter the PLAN thresholds.

### 5.1 Stage S (CPU, deterministic, < 2 min)

Dimensions are the real ones: $D_m=229$, $d_z=256$, $|a|=29$, $K=10$, LSTM-128 ×2 over 135-dim inputs, $T=600$.

**(a) Single-pass normalizer freeze vs double-update drift.**
- a1 *(PLAN-1)*: over 400 FB updates, each followed by `sample_ufo_mixed_z` and 8 expert encodings, max |Δ(mean, var, count)| after freeze $=0.0$, and `update_calls` per update $=2$. Dry run: `0.0`, `[2]`.
- a2 [A+]: the bug arm (auto-updating normalizer left in train mode) is detected (drift $>0$), and its stationary mean is within $5\cdot10^{-3}$ of the closed form $\frac{2n\mu_n+n_e\mu_{\mathrm{demo}}}{3n+n_e}$. Dry run: $0.20844$ vs $0.20825$.
- a3 [A+]: the EMA read-time weights are within $5\cdot10^{-3}$ of $1/(2-\beta)$ and $(2-\beta)/(3-3\beta+\beta^2)$. Dry run: $0.52625/0.52632$, $0.70108/0.70111$.
- a4 [A+]: telescoping identity error $<10^{-4}$. Dry run: $7.8\cdot10^{-8}$.
- a5 [A+]: train-mode batch-statistics relative error within 25 % of $3/(2n_e)$ for $n_e\in\{8,64\}$. Dry run: $0.194/0.1875$, $0.0235/0.0234$.

**(b) `behavior_z` immutability vs overwrite corruption.**
- b1 *(PLAN-2)*: after 20 FB updates with `z_update` sampling, `max_abs_diff(behavior_z_after, behavior_z_before) == 0.0`, and the storage of `z_update` is disjoint (`data_ptr`). Dry run: `0.0`.
- b2 [A+]: the overwrite-bug arm is detected. Dry run: $7.06$ max diff, 70.6 % of rows corrupted, mean cosine of corrupted rows to the original $5\cdot10^{-4}$, i.e. the label is replaced by an essentially orthogonal command.
- b3 [A+]: the critic-target code path reads the replay `z_actual` tensor (asserted by identity), not the update batch's `z_update`.

**(c) Online $(\Delta_B,\Delta_\pi)$ drift tracking.** [A+, all]
- c1: stored-column $\Delta_\pi$ equals snapshot recomputation, max error $<10^{-6}$. Dry run: $0.0$.
- c2: across injected actor drifts $\{10^{-3},3\cdot10^{-3},10^{-2}\}$ × 3 rows, both bounds hold: $|b|\le\text{bound}+3\,\mathrm{SE}$. The protocol records bound slack, which is informative and not a pass criterion.
- c3: $B$ drifted with $\pi$ fixed: keep-label bias $=0.0$ under common random numbers, and re-encode bias $>3$ SE at $\Delta_B\in[0.01,0.03]$. Dry run: $0.0$; $0.0154\pm0.0042$ at $\Delta_B=0.018$.
- c4: the identity $\|B_{\mathrm{now}}-B_{\mathrm{then}}\|^2=2d_z\Delta_B$ holds within $10^{-3}$ (fp32). Dry run: $1.2\cdot10^{-4}$.
- c5: under a synthetic pure rotation, Procrustes gives $|\Delta_B^{\mathrm{def}}|<10^{-6}$. Dry run: $7\cdot10^{-11}$.
- c6: the parameter-space rotation test of C-B02-A-04 shows FB+actor loss invariance $<10^{-4}$ relative. This is not in the sketch; the runner must implement it against `fb_core.py`.

**(d) Full-prefix zero-hidden burn-in vs stale cached hidden state.**
- d1 *(PLAN-3)*: `max_abs_diff(q_burnin_tail, q_exact_full_tail) < 1e-5` over 16 episodes with $t_0\in[100,568)$ and $L=32$. Dry run: $0.0$.
- d2 *(PLAN-3)*: the stale cached hidden state after the pre-registered drift (200 Adam steps, lr $3\cdot10^{-4}$, on a fixed regression) has error $>10^{-2}$. Dry run: $1.10$.
- d3 [A+]: shared-prefix deduplicated burn-in equals per-slice burn-in, max error $<10^{-6}$. This is not in the sketch; the runner implements it.

**Verdict rule.** PASS iff every PLAN item passes. [A+] items are reported individually. A failing [A+] item does not fail the PLAN verdict, but it marks the corresponding §1 formula as *unverified* in synthesis.

### 5.2 Stage G (GPU, integration; beyond the spike and gated by the adjudicator)

Obstacle traversal R2.1, heights `{0.10, 0.20}`, 3 seeds per arm, compute-matched at $2\cdot10^6$ committed control steps. Arms:
- (A0) baseline FIFO 50k;
- (A1) M1 gate at $\varepsilon=0.02$;
- (A2) M1 at $\varepsilon=0.05$;
- (A3) M1 + M3 IS;
- (A4) M4 soft weighting;
- (N) negative control: re-encode expert labels (§3.1(a)), implemented as a *shadow critic* trained alongside A0 that never drives the planner, so the contract stays intact in the acting system.

- **Primary endpoint (value calibration, not task success).** Every 100k steps, from 256 frozen-weight diagnostic-env states, run 32 MC rollouts per $(H,z)$ under $\pi_{\theta_t}$, using planner $z$ for the first macro and then $P_\psi$. Measure the calibration error $\epsilon_Q=\mathbb{E}|Q_{\phi_1}(H,c,z)-\hat G^{\theta_t}_{\mathrm{MC}}(H,z)|$ normalised by $\mathrm{sd}(\hat G)$.
- **Pre-registered prediction.** A1 reduces mean $\epsilon_Q$ vs A0 by $\ge15\%$ (paired over seeds × checkpoints; one-sided Wilcoxon, $p<0.05$), with admitted-set size $\ge N_{\min}$ for $\ge90\%$ of the run.
- **Falsifier.** $\epsilon_Q(\mathrm{A1})\ge\epsilon_Q(\mathrm{A0})$, or D2 shows $\overline{\mathrm{KL}}\le0.02$ for all ages of the FIFO window. In that case staleness is immaterial at this training speed, and M1 should be dropped as unnecessary.
- **Secondary endpoints.** The KL-vs-age profile; $\Delta_B^{\mathrm{gauge}}/\Delta_B^{\mathrm{tot}}$ (tests the gauge-diffusion conjecture); $\Delta_\pi^{\hat R}/\Delta_\pi$ (trigger for §3.3); D4 $S_\pi$ and saturation; D5 $\mathcal C(\alpha)$; the measured diagnostic overhead against the < 5 % budget; and the shadow critic N's $\epsilon_Q$ vs A0, where C-B02-A-01(c) predicts N is worse.
- **No claim of traversal learning or of superiority over PPO/AMP is made or implied by Stage G** (Charter §2.5). Its endpoints are value-calibration and diagnostic quantities only.

### 5.3 Failure modes and edge cases covered

- Short macros: termination vs timeout (§1.6, M2).
- `severe_penetration` rows: committed, $\Phi=0$, included in D2/M1 like any row.
- `invalid` rows: never present; the episode is discarded, so burn-in never sees a partial fabricated prefix.
- Gate starvation: floors $G_{\min}$, $N_{\min}$; starvation is logged.
- Ball-striking regime: no gate (§1.1); diagnostics and burn-in only.
- Singular-sensitivity regime (tanh saturation): reported separately in D4.
- $n_e=1$ train-mode BN: undefined; caught by D1.
- Symmetry-breaking per-coordinate $z$ preprocessing: C-B02-A-04 premise check.
- FIFO-truncated episodes: the telescoping identity is stated over segments.
