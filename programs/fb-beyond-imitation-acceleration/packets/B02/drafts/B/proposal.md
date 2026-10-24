# Proposal B (Packet B02): Breaking Imitation Ceilings via Unindexed Single-Frame Prompts, Relabeling, and Joint Training Non-Stationarity

**Author:** Primary Author B. **Status:** independent proposal; no empirical results claimed. **Date:** 2026-10-23. **Inherited result:** `D-B01-001`, as supplied in `synthesis/B01-synthesis.md`; the B01 spike PASS is inherited evidence about B01 only.

The proposed intervention is an immutable execution record, generation-aware task replay, and explicit measurement of changes in the command-to-trajectory map. Preserve joint learning from scratch. Single-frame demonstrations remain exploration prompts; they impose neither action labels nor tracking rewards. Correct normalization and recurrent reconstruction remove avoidable errors, but do not by themselves make the macro transition kernel stationary. This proposal gives exact identities, conditional bounds, and a falsifiable implementation protocol rather than claiming that a finite replay capacity guarantees stability.

**Context provenance and limitations.** Read the charter, B01 synthesis, and baseline 05 at the requested paths. Three requested filenames do not exist in this checkout; the matching documents actually read are:

| Requested path relative to program root | Available document used |
|---|---|
| `packets/B02/brief.md` | `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md` |
| `baseline/02-beyond-imitation-paradigm-and-open-challenges.md` | `baseline/02-fb-paradigm-beyond-imitation-and-exploration.md` |
| `baseline/04-whole-body-ball-striking-v2-design.md` | `baseline/04-joint-fb-ball-striking-v2-architecture.md` |

These are explicit source substitutions, not assertions of byte equivalence. Also read pinned method v1.0, hash `1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`, especially §11.5 and Appendix B. No competing B02 draft, transcript, results, or spike plan was read. Filesystem permissions in this session are unrestricted: behavioral observance of the firewall is not evidence that OS-enforced isolation exists. The orchestrator must audit and apply the method's provisional cap if enforcement is absent. Agreement on constraints already supplied by the brief is framed agreement.

## 1. Exact Mathematical Analysis of Joint Training Non-Stationarity and Prompt Drift

### 1.1 Coordinates, clocks, and the target being estimated

Use `n` for learner generation, `g=n-Δ` for collection generation, and `t` for physical control time. Include running normalizer buffers in the effective parameters: `ω` and `θ` alone do not specify a deployed function. Write these effective maps as $B_n$ and $\pi_n$. Obstacle traversal uses $m\in\mathbb R^{229}$, $z\in\mathcal S^{255}(16)$, $a\in[-1,1]^{29}$, and $K=10$. Ball v2 specifies $m\in\mathbb R^{277}$ and $d_z=100$ in its detailed architecture, unlike baseline 02's generic $256$; use task-specific $d_z$, never silently share checkpoints across those schemas.

Let $\mathcal H_t$ denote the complete causal episode record, including observations, actually executed past commands/actions, reset flags, and permitted critic information. Let $h_t^j=f_{\xi_j}(\mathcal H_t)$ be a particular network's reconstructed recurrent state. The analysis conditions on the same start history and physical-state belief for old and new executions. Compression to $h$ need not be sufficient: hidden-state reconstruction fixes representation staleness, not partial observability or state aliasing. Stationary physical dynamics and reward rules are assumptions, with episode geometry held fixed.

For an actual macro lasting $k\le K$ define

$$R_k=\sum_{i=0}^{k-1}\gamma^i r^{\rm task}_{t+i},\qquad
Y_n(\tau)=R_k+\gamma^k(1-d_k)V_n(\mathcal H_{t+k}),\quad \gamma=\gamma_{\rm task},$$
$$V_n(\mathcal H)=\min_{j=1,2}Q_{\bar\phi_{j,n}}
\left(h^{\bar Q_j}_n(\mathcal H),c^{\rm geom},P_{\bar\psi_n}(h^{\bar P}_n(\mathcal H))\right). \tag{1}$$

All target quantities are detached. The question's $r_{\rm task}$ must mean the discounted macro return when $k>1$. Its online $P_\psi$ form is analyzable by substituting $P_\psi$ into $V_n$; production follows the charter/baseline target planner $P_{\bar\psi}$. For fixed critic hidden states, replacing the target planner by the online planner adds at most $\gamma^k(1-d_k)L_{Q,z}\|P_\psi-P_{\bar\psi}\|$ if both scalar critic heads are $L_{Q,z}$-Lipschitz. This is separate from low-level staleness.

Here $d_k$ is true termination, not timeout. At timeout, use the real pre-reset state and $\gamma^k$ bootstrap; at failure or success termination, zero bootstrap. $k$ is a stopping time under the same physical termination/timeout rule in both executions. Do not condition retrospectively on observing a particular failure length; that would select trajectories. Formulas below cover the distribution over stopped paths; fixed-$k$ bounds apply to scheduled endpoints, and $K$ bounds apply to variable stopping.

### 1.2 Exact macro-kernel shift and its target bias

For fixed executed numeric command $z=z_{\rm actual}$, let $\mathbb P_g^z(d\tau\mid\mathcal H_t)$ be the distribution of the full macro path generated by $\pi_g$. Conditional physical transitions have kernel $p$:

$$d\mathbb P_g^z(\tau\mid\mathcal H_t)
=\prod_{i<k}\pi_g(da_i\mid o_{t+i},z)\,p(ds_{t+i+1},dr_i\mid s_{t+i},a_i), \tag{2}$$

with the common initial belief integrated out and stopping encoded in the path space. The exact conditional bias of an uncorrected historical target relative to today's macro operator is

$$b_{g\to n}(\mathcal H_t,z)
=\mathbb E_g[Y_n]-\mathbb E_n[Y_n]
=\int Y_n(\tau)\,[d\mathbb P_g^z-d\mathbb P_n^z]. \tag{3}$$

This includes changed rewards, changed termination probabilities, and changed endpoint histories. Subtracting only two bootstrap values misses the first two effects. Averaging (3) over the replay generation mixture gives total replay bias. An accurate target critic or a slow target planner does not cancel (3).

If $\mathbb P_n^z\ll\mathbb P_g^z$, define

$$W_{g\to n}(\tau)=\prod_{i<k}
\frac{\pi_n(a_i\mid o_{t+i},z)}{\pi_g(a_i\mid o_{t+i},z)}.
\quad b_{g\to n}=\mathbb E_g[(1-W)Y_n],\quad
\mathbb E_g[WY_n]=\mathbb E_n[Y_n]. \tag{4}$$

No high-level source probability ratio belongs here: this is a conditional operator at the stored command, not an on-policy state-occupancy estimator. Density ratios of normalized $B$ outputs are not substitutes for (4). If collector parameters change inside a macro, use the actual generation $g_i$ and behavior density at every step; a single generation tag then is insufficient.

An exact variance identity, for $\mu_g=\mathbb E_gY_n$, $\mu_n=\mathbb E_nY_n$, is

$$\operatorname{Var}_g(Y_n)-\operatorname{Var}_n(Y_n)
=\int Y_n^2(d\mathbb P_g^z-d\mathbb P_n^z)-b_{g\to n}(\mu_g+\mu_n). \tag{5}$$

For independent conditional samples, historical target-mean MSE is $b_{g\to n}^2+\operatorname{Var}_g(Y_n)/N$. Correlated replay needs the covariance terms too. Unbiased weighting replaces the variance by $\mathbb E_g[W^2Y_n^2]-\mu_n^2$, which can be much larger.

For $|r_i|\le r_{\max}$, $|V_n|\le V_{\max}$, a fixed-$k$ bound is $|Y_n|\le M_k=r_{\max}(1-\gamma^k)/(1-\gamma)+\gamma^k V_{\max}$. For stopping use $M=\max_{1\le k\le K}M_k$. With $\operatorname{TV}(P,Q)=\sup_A|P(A)-Q(A)|$,

$$|b_{g\to n}|\le 2M\operatorname{TV}(\mathbb P_g^z,\mathbb P_n^z)
\le 2M\min\left(1,\sqrt{\tfrac12 D_{\rm KL}(\mathbb P_g^z\|\mathbb P_n^z)}\right),$$
$$D_{\rm KL}(\mathbb P_g^z\|\mathbb P_n^z)
=\mathbb E_g\sum_{i<k}D_{\rm KL}\big(\pi_g(\cdot\mid o_i,z)\|\pi_n(\cdot\mid o_i,z)\big). \tag{6}$$

Equality in the second line uses a common physical kernel and matching action-path support. For pre-squash Gaussian actions with common positive covariance $\Sigma_a$, the summand is exactly $\tfrac12\|\mu_n(o_i,z)-\mu_g(o_i,z)\|_{\Sigma_a^{-1}}^2$. An invertible tanh preserves the ratio. Hard clipping only gives a data-processing bound on applied-action KL; exact weighting remains possible on a stored pre-clipping action path with its known density and common deterministic actuator map. Gaussian densities evaluated at clipped actions are incorrect because clipping creates boundary atoms.

If $\|\mu_n-\mu_g\|_{\Sigma_a^{-1}}\le D_{g,n}$ uniformly on reachable histories, then

$$|b_{g\to n}|\le M\min(2,\sqrt K D_{g,n}). \tag{7}$$

For per-generation uniform increments at most $\delta$, $D_{g,n}\le\Delta\delta$, so choosing $\Delta\le\epsilon/(\sqrt K\delta)$ ensures $|b|\le\epsilon M$. Finite anchor measurements do not establish this uniform premise. Contact-rich deterministic policies can have disjoint path measures and discontinuous outcomes after an arbitrarily small action change: there is no universal smooth-dynamics bound from a measured action L2 distance alone.

### 1.3 Encoder drift is not direct fixed-command transition drift

Define $\Delta_B^{g,n}(m)=1-B_n(m)^\top B_g(m)/d_z$. With exact spherical normalization,

$$\|B_n(m)-B_g(m)\|^2=2d_z\Delta_B^{g,n}(m). \tag{8}$$

If projection uses an epsilon denominator, use the exact squared norm $\|B_n\|^2+\|B_g\|^2-2B_n^\top B_g$ and log norm errors; (8) then has the corresponding norm correction. Reject zero encoder outputs rather than silently calling them spherical commands.

For a newly queried frame $m$, add and subtract $\mu_n(o,B_g(m))$ to get

$$\|\mu_n(o,B_n(m))-\mu_g(o,B_g(m))\|
\le L_{\pi,z}\sqrt{2d_z\Delta_B(m)}+\Delta_\pi(o,B_g(m)), \tag{9}$$

where $\Delta_\pi(o,z)=\|\mu_n(o,z)-\mu_g(o,z)\|$. A fixed stored $z$ bypasses $B$: changing only $\omega$ with actor and observation normalization held fixed leaves (2) unchanged. Encoder drift changes future prompt selection and joint-learning coordinates; actor/observation-normalizer drift changes the execution of old numeric commands. Conversely, zero encoder drift does not imply zero macro bias.

Rotating the encoder and actor's latent coordinates together can preserve new-frame behavior while changing fixed-coordinate replay behavior. Thus Procrustes-aligned encoder drift is a useful secondary gauge diagnostic, but cannot replace raw $\Delta_B$ or $\Delta_\pi$. Consistent with `D-B01-001`, neither expert prompts nor 50/50 FB relabels receive Gram whitening. The B01 nullspace result `C-B01-B-02` also means a well-behaved drift metric cannot establish identifiability of collapsed latent directions.

### 1.4 Exact single-pass normalization violations

Here single-pass means **one current batch plus one next batch per update**, in that order, not one total batch. Analyze an EMA input normalizer with momentum $\alpha\in(0,1)$; write $q=1-\alpha$. Let current and next batch means be $c,n$ and their stored variance statistics be $s_c^2,s_n^2$. Correct running states are

$$\mu_*=q^2\mu_0+\alpha q c+\alpha n,\qquad
v_*=q^2v_0+\alpha q s_c^2+\alpha s_n^2. \tag{10}$$

For an erroneous extra next-batch update,

$$\mu_{\rm dup}=q^3\mu_0+\alpha q^2c+\alpha(1+q)n,
\quad \mu_{\rm dup}-\mu_*=\alpha(n-\mu_*),$$
$$v_{\rm dup}-v_*=\alpha(s_n^2-v_*). \tag{11}$$

For an illegal expert or relabel query batch with statistics $(e,s_e^2)$, replace $n,s_n^2$ on the right of (11) by $e,s_e^2$. After $L$ illegal queries,

$$\mu_L=q^L\mu_*+\alpha\sum_{j=1}^Lq^{L-j}e_j,
\quad v_L=q^Lv_*+\alpha\sum_{j=1}^Lq^{L-j}s_{e_j}^2. \tag{12}$$

The general ordered update formula is $\mu_J=q^J\mu_0+\alpha\sum_{j=1}^Jq^{J-j}b_j$, and likewise for $v_J$. It covers duplicated calls inserted anywhere. A full permutation of `m_next` has identical batch moments, so train-mode relabeling duplicates that update even though the sample order changes. Subsetting before encoding can introduce different moments and sampling noise.

The precise normalized distribution shift can be stated without assuming Gaussian physical frames. For fixed saved buffers, $X\sim\mathcal D$ with mean $a$ and covariance $C$, set $D_v=\operatorname{diag}((v+\varepsilon)^{-1/2})$ and $U=D_v(X-\mu)$. Then

$$\mathcal L(U)=(x\mapsto D_v(x-\mu))_\#\mathcal D,
\quad\mathbb EU=D_v(a-\mu),\quad\operatorname{Cov}U=D_vCD_v. \tag{13}$$

If $X$ has density $p_X$, $p_U(u)=p_X(\mu+D_v^{-1}u)|\det D_v^{-1}|$. Thus the exact covariance error is $D_{v_b}CD_{v_b}-D_{v_*}CD_{v_*}$ and coordinate variance ratio is $(v_*+\varepsilon)/(v_b+\varepsilon)$. The pointwise feature error is

$$U_b-U_*=(D_{v_b}-D_{v_*})(X-\mu_*)-D_{v_b}(\mu_b-\mu_*). \tag{14}$$

Affine BN multiplies by its learned diagonal scale and adds its offset. For the nonlinear encoder, the exact command distribution is the pushforward $\mathcal L(z_b)=(B^{\rm post}_\omega\circ T_b)_\#\mathcal D$; no universal closed-form Gaussian command distribution follows. Actual $\Delta_B$ is evaluated by paired forwards. If its post-normalization map is $L_B$-Lipschitz on the panel, $\|z_b-z_*\|\le L_B\|U_b-U_*\|$; this needs a positive lower bound on pre-projection norms.

For a scalar channel the estimator-variance error is also exact:

$$\operatorname{Var}(\mu_{\rm dup})-\operatorname{Var}(\mu_*)
=(q^2-1)\operatorname{Var}(\mu_*)+\alpha^2\operatorname{Var}(n)
+2\alpha q\operatorname{Cov}(\mu_*,n). \tag{15}$$

The covariance term cannot be dropped: $\mu_*$ already contains $n$, and current/next frames are paired. Under the illustrative stronger assumptions of deterministic $\mu_0$, independent current/next sample means each of variance $\sigma^2/N$, and exactly reusing the next batch, the difference reduces to

$$\frac{\alpha^2\sigma^2}{N}(q^4+2q)>0. \tag{16}$$

Replacing means by sample variances gives the analogous identity for the variance-buffer estimator, with its own covariance terms. Equations (13)–(14) are conditional on saved buffers; if the evaluated batch itself produced the buffers, use their joint distribution instead of treating $X$ as independent. For fixed repeated batch statistics, long-run cycle endpoints satisfy $\mu_*^\infty=(qc+n)/(1+q)$ but $\mu_{\rm dup}^\infty=(q^2c+(1+q)n)/(1+q+q^2)$: double updating systematically increases next-frame weight, even apart from sampling variance.

PyTorch `BatchNorm1d` uses the biased batch variance for a train-mode forward and the unbiased batch variance for its running variance update; evaluation uses running buffers when tracking is enabled. The EMA formulas above use the latter statistic. With `momentum=None`, after $J$ counted batches an extra batch instead shifts the mean by $(e-\mu_*)/(J+1)$; count-based pooled/Welford normalizers require their own merge formulas. `track_running_stats=False` cannot implement frozen-buffer semantics. PyTorch BatchNorm1d documentation.

`torch.no_grad()` disables gradient recording; it does not switch a module to evaluation mode. PyTorch no_grad documentation. A singleton expert query in train-mode BN may error rather than quietly corrupt buffers; both that error and repeated-batch contamination are tested. Training forwards also normalize by query-batch moments, so their immediate output differs from the frozen map even before considering buffer drift.

Finally, if an illegal query changes a fixed-path target from $Y_*$ to $Y_*+e$, its exact target variance change is $2\operatorname{Cov}(Y_*,e)+\operatorname{Var}(e)$. This can have either sign. If the collector also uses changed buffers, add the path-law shift in (3)–(5); it is unjustified to claim that all BN violations always increase task-target variance.

## 2. Algorithmic Design for Non-Stationarity Mitigation and Controllability Diagnostics

### 2.1 Immutable data and exact update order

Keep separate `FBReplay` and `TaskEpisodeReplay`. Each committed physical row contains episode/step IDs, raw permitted observations, `m_current`, `m_next`, `a_applied`, immutable `behavior_z`, termination/truncation flags, and the real pre-reset endpoint. Macro rows additionally store start/end offsets, $k$, discounted $R_k$, source, geometry, and collection generations. An optional correction record stores actual pre-actuator sampled actions and behavior log-densities; never infer behavior density from today's actor. Retain complete prefixes from `step=0` as long as any sampled macro references that episode; eviction operates on whole episodes or reference-counted prefix storage.

Collection snapshots include weights **and buffers**. Updating learner weights continuously is permitted; assigning a fixed collector snapshot for one macro is not a pretraining/freezing stage. If asynchronous collectors cannot do that, store generation and density per control step. Store actual executed prior commands in planner inputs even while reconstructing a history under new planner weights; never replace historical commands with counterfactual planner outputs.

One FB iteration is:

1. Validate real rows. Update observation and motion normalizers once on the current batch and once on the next batch. Track per-module update counts; no invalid row enters either call.
2. Freeze normalizer buffers for every subsequent computation in this iteration. Encode permuted raw `m_next` with the **online** $B_n$ in `eval/no_grad`. Sample a fresh mask and spherical random vectors; construct the 50/50 `z_update` in newly allocated storage. Do not read `behavior_z` to construct it.
3. Use detached `z_update` only in FB and low-level actor losses. The actor maximizes scalar $\min_j F_j(o,\pi(o,z),z)^\top z$, taking the scalar inner products before the minimum. During actor gradients, keep normalizers frozen and critic weights fixed while preserving the derivative through the actor action input. Do not wrap that actor path in `no_grad`.
4. Reconstruct recurrent states and train task critics on `z_actual` (obstacle) or `a_applied` (ball). Target networks, target normalizers, and target planners are detached; target buffers must be versioned and updated by one explicit synchronization rule, never by expert/relabel forwards. For this proposal use exact online-buffer copying at the existing target-update event and the baseline parameter EMA; log the resulting effective target version.
5. Planner updates retain the baseline delay of two task updates. Expert/near collection re-encodes raw, numerically valid, uniformly sampled single frames with current online $B$ in frozen-buffer `eval/no_grad`, with no height, phase, frame index, or task metadata entering $B$. Preserve the scheduled three-way probabilities and 10–20° near perturbations. Evaluation is 100% planner.

Cloning is necessary at the storage boundary: `detach()` alone shares tensor storage. A `z_update.copy_` into a replay view is a violation even if no autograd graph exists. Check tensor bytes and mutation counters before/after all updates. Changing `behavior_z` in a private test copy while holding RNG/raw next frames fixed must leave `z_update` unchanged; conversely it must change the task-critic input.

### 2.2 Online drift and controllability panel

At initialization fix a diagnostic set of 128 valid single frames and 128 permitted observation/command pairs, stratifying commands equally among raw expert, near, planner, and uniform sphere. The uniform component is a diagnostic/FB-update panel, not a fourth rollout source. Keep a second rolling panel of 128 valid replay rows to expose new support. Fix physical units and scales at panel creation, and log both panels separately. Record panel $B_g(m)$ outputs and all fixed-panel actor means at collector snapshot publication; record collection action means alongside executed actions for visited-state drift. Retain the previous trajectory-panel snapshot for paired old/new rollouts. These are diagnostic records, never cached expert prompts used for rollout. Report empty strata as missing, not zero drift.

Every 100 learner updates compute the following with frozen buffers, stratified by source, task height, and collection lag bins `0`, `1–9`, `10–99`, `100–999`, `1000+`:

| Quantity | Exact finite-panel definition | Interpretation and limit |
|---|---|---|
| Encoder drift | Mean, p95, maximum of $\Delta_B^{g,n}(m)$ and the direct squared displacement in (8) | Prompt coordinate motion; retain norm residuals |
| Actor drift | Mean, p95, maximum of $\|\mu_n(o,z_{actual})-\mu_g(o,z_{actual})\|_2$; also divide by $\sqrt{29}$ for RMS action units | Compare means, not two independently sampled actions; include observation-buffer changes |
| Distribution drift | Per-step Gaussian KL when available, empirical path KL sum, log-weight quantiles, and $\mathrm{ESS}=(\sum W)^2/\sum W^2$ | KL on visited rows is an estimate, not a reachable-state supremum |
| Action sensitivity | $S_z=N^{-1}\sum_i\|J_i\|_F$, $J_i=\partial\mu_n(o_i,z_i)/\partial z_i\in\mathbb R^{29\times d_z}$ | Compute exact Jacobians on 8 fixed pairs every 100 updates; this is an empirical expectation |
| On-sphere sensitivity | $S_{\rm tan}=N^{-1}\sum_i\|J_i(I-z_iz_i^\top/d_z)\|_F$ and singular values | Large radial derivatives alone do not give usable command control |

Use `torch.func.jacrev` or 29 reverse-mode output derivatives on the tiny panel; differentiate the deterministic deployed action mean including squashing/clipping. Finite differences at clipping kinks are reported separately. A stochastic Jacobian estimator may be an additional cheap metric, but its squared-norm unbiasedness does not imply that the estimated norm is unbiased.

Every 5,000 learner updates run an isolated trajectory panel from 8 saved simulator states with 4 distinct fixed spherical commands: two expert/near and two broadly separated commands. Use the same initial physical snapshot and paired noise for all commands, horizons $H\in\{1,5,10\}$, frozen weights/buffers, no replay writes. Let $x_h$ contain root displacement, root velocity, joint angles, and foot positions, normalized by a fixed documented diagonal scale matrix $D_x$. Define

$$D_H(z,z')=\frac1H\sum_{h=1}^H\|D_x(x_h^z-x_h^{z'})\|_2^2,\qquad
D_H^{\rm drift}(z)=\frac1H\sum_{h=1}^H\|D_x(x_h^{n,z}-x_h^{g,z})\|_2^2. \tag{17}$$

Keep ended physical states absorbing for distance calculation and report termination disagreement separately; never splice a reset state into a path. Compare distinct-command distance to repeated-same-command controls with independent noise, and also report the paired-noise value. Report contact-event sequence disagreement and action-energy change. High $S_z$ with negligible $D_H$ means actuator-level variation has not produced trajectory diversity; high $D_H$ consisting only of falls is not useful controllability. A rank-$r$ local Jacobian says nothing about global task reachability. For ball striking use ball displacement and contact outcomes as **diagnostic outputs**, never encoder inputs.

A rolling empirical alert triggers if action RMS p95 exceeds `0.05`, $\Delta_B$ p95 exceeds `0.02`, or the paired trajectory distance exceeds twice its prior-generation median plus `1e-6`. These are preregistered engineering thresholds, not necessity claims. Alerts shrink task replay eligibility and request inspection; they never add BC, tracking rewards, task inputs to $B$, or a freeze stage.

### 2.3 Replay horizon: separate age heuristics, conditional bounds, and exact correction

Use a physical storage limit of 50,000 macro rows, subject to complete-prefix retention. Compare three arms on the same collected data:

| Arm | Sampling/weighting | What it establishes |
|---|---|---|
| FIFO | Uniform among stored macros | Capacity limits age only |
| Age | Sample generations with factor $\exp[-(n-g)/1000]$ | Different replay emphasis, no policy correction |
| Proposed | Generation drift gate, with likelihood correction where supported | Explicitly separates measured stability from corrected operator estimation |

For the proposed arm, evaluate generation eligibility on the independent fixed panel before choosing a training minibatch: require p95 action RMS $\le0.05$, p95 $\Delta_B\le0.02$, and generation age $\le1000$ updates. Shorten to the contiguous suffix of generations passing the gate; if none passes, collect fresh data and skip the task update while continuing valid FB learning. This is a sampling rule, not permission to delete committed failures. Preserve source/failure acceptance counts and diagnose loss of coverage. Do not filter individual training paths by their realized reward, termination, likelihood ratio, or TD error, which would change their conditional transition distribution.

**Bound mode.** If an independently justified *uniform* $D_{g,n}$ is available, also require $\sqrt K D_{g,n}\le0.05$. Equation (7) then certifies normalized conditional target bias at most `0.05` without trajectory importance sampling. A finite diagnostic maximum is explicitly not that certificate. Known bounded toy policies in §5 supply a certificate; neural robot policies generally do not. Short windows alone therefore do not prove charter H2.

**Correction mode.** Where the deployed stochastic actor exposes a valid behavior density and common support, compute (4) on the stored complete macro actions with today's actor evaluated at the same stored observations and actual $z$. Use the detached, unnormalized weight in the critic loss:

$$\mathcal L_Q=\frac1N\sum_i W_i\sum_{j=1}^2
\big[Q_{\phi_j}(h_i,z_{actual,i})-\operatorname{sg}(Y_{n,i})\big]^2. \tag{18}$$

This gives the current conditional Bellman regression under historical start-state/command coverage. Stop gradients through $W$, the target, and the low-level actor; $W$ is a measure correction, not a new actor objective. Do not normalize weights by the minibatch sum or clip them while calling the estimator unbiased. Recompute weights after actor updates; never reuse a ratio evaluated at a different target generation. Diagnostics can recommend narrowing subsequent generation eligibility, but must not retroactively remove large-weight training trajectories.

For a common-covariance Gaussian with uniform Mahalanobis mean difference bounded by $D$, conditional second-moment recursion gives $\mathbb E_gW^2\le\exp(KD^2)$, hence variance of a sample mean of $WY$ is at most $M^2\exp(KD^2)/N$. This is a conditional variance guarantee, not something inferred from ESS alone. If practical weight clipping $W_c=\min(W,c)$ is separately ablated, its exact target bias is $-\mathbb E_g[(W-c)_+Y]$ and absolute bias is at most $M\mathbb E_g[(W-c)_+]$; log the omitted mass, do not hide it.

When support or behavior likelihoods are absent, correction mode is **unavailable**, not approximately valid. The empirical gate remains a bounded-compute candidate mitigation with no universal bias certificate. Existing historical rows missing likelihood metadata can still enter the FIFO/gated comparison, but not the exact-correction arm. This conditional design avoids pretending a Gaussian likelihood exists for a deterministic or clipped-command collector.

Never invent a new endpoint $k<K$ merely by cutting an ordinary continuing hold and bootstrapping a fresh planner command. A genuine early macro endpoint uses the recorded $k$ and $\gamma^k$; an arbitrary mid-hold training cut would require a remaining-duration/held-command continuation value, which is outside this baseline. For a nonterminated short endpoint the exponent error from using $K$ would be $(\gamma^K-\gamma^k)V_n$.

### 2.4 Full-prefix recurrent reconstruction and the ball action-Q distinction

For each recurrent module separately, define $u_t$ as its allowed historical input and $h_{t+1}=f_\xi(h_t,u_t)$, $h_0=0$ (both hidden and cell zero for LSTM). For sampled slice $[t_0,t_0+L)$, unroll $u_0,\ldots,u_{t_0-1}$ under that module's current weights/buffers with `no_grad`, detach the resulting state, then run the training slice with gradients. Online planner, both online critics, target planner, and both target critics each reconstruct their own prefix. Use deterministic recurrent evaluation (no dropout), frozen normalizers, causal inputs, and episode masks. Prefix batching/padding is allowed only if masked steps do not update state.

By induction this gives the same hidden state and outputs as a whole-episode unroll with the same weights and inputs. It does **not** give whole-episode BPTT gradients: the prefix is deliberately detached. Comparing old and current full-prefix states yields, under recurrent Lipschitz constants and with buffers included in $\xi$,

$$\|e_{t+1}\|\le L_h\|e_t\|+L_\xi\|\xi_n-\xi_g\|,
\quad\|e_t\|\le L_\xi\|\xi_n-\xi_g\|\sum_{j=0}^{t-1}L_h^j. \tag{19}$$

After injecting the stale state at $t_0$ and using current weights thereafter, its error propagates at most as $L_h^\ell\|e_{t_0}\|$ over $\ell$ further steps. There is no decay guarantee if $L_h\ge1$. Short local burn-in from zero is also not exact unless earlier history is provably irrelevant. Cache only within an unchanged parameter/buffer version; across updates recompute from `step=0`.

Ball v2 has $K_{hold}=1$ and conditions task $Q$ on immutable applied physical action, so its immediate $p(s',r\mid s,a_{applied})$ has no low-level-policy staleness under the stationary-state assumption. Use the dedicated task-only actor EMA $\bar\theta$ with target planner/critics and the specified clipped target smoothing noise. Its target-policy drift is distinct from obstacle macro-kernel drift. For planner updates, freeze actor parameters but preserve $\partial\pi/\partial z$ and $\partial Q/\partial a$. Do not retrofit macro-z replay corrections into that action-Q target.

**Schema limitation.** The frozen ball document labels policy observations as 93 dimensions, while the explicitly listed components sum to 107; it also describes a backward MLP ending in 256 features but a 100-dimensional output sphere. This proposal does not silently resolve those inconsistencies. The B02 contract spike uses internally explicit synthetic dimensions plus the unambiguous obstacle dimensions. A robot integration must first use an authoritative, reconciled schema; no empirical ball result is claimed here.

### 2.5 Cost, failures, and B01 compatibility

Normalizers, byte checks, and logged actor means are inexpensive. Batched correction mode needs up to $K$ actor forwards per macro batch, so its overhead is measured rather than assumed below 5%. Amortize panel forwards over 100 updates, trajectory panels over 5,000, and batch common prefixes by episode. Compare incremental diagnostics/mitigation time against a baseline that **already** performs mandatory full-prefix reconstruction. Report correction-mode and gate-only overhead separately. A mode above 5% fails the brief's overhead gate; reducing test frequency after seeing timings requires a plan amendment.

Finite, valid `severe_penetration` transitions remain committed with `terminated=True`, zero absorption potential, and counted failures; `invalid` overrides penetration, rejects the entire uncommitted control interval from replay/normalizers, and halts the affected run/panel. If an invalid step interrupts a partial macro, do not fabricate a valid macro endpoint; retain earlier valid low-level rows but withhold the incomplete macro target. Repeated failure cannot be hidden by the drift gate or curriculum denominator.

`D-B01-001` remains unchanged: raw spherical expert/relabel commands; scalar conservative FB actor; no inverse Gram inserted into these sites. This proposal introduces no model-based intrinsic reward. If a later hybrid branch is used, it must keep the inherited target-coordinate whitening, damping, support/leverage gates, and stop-gradient rules. Encoder covariance rank and action sensitivity are complementary diagnostics, not interchangeable certificates.

## 3. Serious Alternative Considered and Rejected

### 3.1 Retrofit historical commands using current motion encodings

**Strong version of the alternative.** Store the complete physical macro and re-encode its frames through current $B_n$, then aggregate them into a current-coordinate command $\tilde z$. Train $Q(h,\tilde z)$ on the historical $R_k,h'$; this seems to repair coordinate drift without losing old successes. A learned inverse-dynamics relabeler is a more sophisticated version.

**Why it fails as an exact replacement.** The needed identity is equality of conditional path laws, $\mathbb P_n^{\tilde z}(\cdot\mid\mathcal H)=\mathbb P_g^{z_{actual}}(\cdot\mid\mathcal H)$. Re-encoding an outcome does not imply this identity. In a one-step deterministic counterexample, command $z\in\{-1,+1\}$, old policy $a=z$, new policy $a=-z$, transition $x'=a$, reward $r=a$, and encoder $B_n(x')=x'$ satisfy all relevant causal distinctions. A historical $z=+1$ gives $(x',r)=(+1,+1)$; re-encoding stores $\tilde z=+1$ although the current execution of $+1$ produces reward $-1$. The target error is 2. Increasing the number of observed frames cannot restore a missing equality of policies.

Worse, $\tilde z$ selected from realized successor motion is a descendant of action and environmental noise. Conditioning on it can select favorable stochastic outcomes, whereas choosing the same command before acting cannot select that noise. This is not ordinary reward-goal relabeling: $z$ is the causal macro action. An invertible coordinate transformation $T$ would be valid only with a proved conjugacy $\pi_n(o,Tz)=\pi_g(o,z)$ for every reachable observation, identical actuator/dynamics rules, and consistent transformation of all related objects. General joint learning from scratch supplies none of these premises.

**Decision.** Reject command replacement both because the counterexample defeats its claimed general correctness and because the charter explicitly requires immutable `behavior_z`/`z_actual`. Retain raw frames for fresh FB relabels and fresh expert prompts, not historical action rewriting. This is a rejection within the program; it is not a theorem banning all goal relabeling.

### 3.2 Freeze an imitation-pretrained encoder and low-level actor

This would eliminate actor-induced macro-kernel drift, and can be effective when a fixed repertoire already spans the task. But the brief expressly prohibits pretraining stages and frozen $B/\pi$, and the charter requires joint learning from scratch without BC or pose-tracking fallback. It also cannot guarantee expansion of reachable actions: if the frozen actor produces $a=0$ for every $z$ in a state where success requires $a>0$, no planner can solve that task. This counterexample proves lack of universal sufficiency, not that every frozen repertoire fails. Reject it as an inadmissible mainline and an unsuitable answer to the program's exploration question.

### 3.3 Age-only replay as the serious admissible null

FIFO/age weighting is cheaper than likelihood correction and may win in practice. It has no general drift guarantee: arbitrarily large actor changes can occur in one optimizer step, while an old generation can remain behaviorally identical. Reject it as a *proof* of bounded staleness, retain it as a compute-matched empirical control, and accept it as the engineering winner if the proposed diagnostics/correction fail their registered cost or stability gates. This additional alternative is not settled merely by the brief's immutable-command rule.

## 4. Candidate Necessity Claims (Appendix B)

### C-B02-B-01 — Conditional path-law compatibility is necessary for universally correct unweighted macro targets

- **State/grade:** Candidate, Grade 1; no veto or lock asserted.
- **Explicit premises:** Stationary physical dynamics; fixed start history/belief and actual numeric macro command; two policies inducing probability measures $\mathbb P_g^z,\mathbb P_n^z$ on the same measurable space of paths stopped by $K$; an unweighted historical estimator; correctness demanded for **every bounded measurable path-return functional**. The return class is deliberately stronger than a single fixed task reward.
- **Conclusion shape:** Invariant/obligation: $\mathbb E_g f=\mathbb E_n f$ for every such $f$ if and only if $\mathbb P_g^z=\mathbb P_n^z$. Consequently a universally unbiased method must realize equivalent path laws or an appropriate distribution correction/new-data mechanism; relabeling a numeric command alone supplies neither.
- **Proof:** Equality of measures gives equality of bounded integrals. Conversely choose $f=\mathbf1_A$ for every measurable event $A$; equality of expectations gives equality of probabilities on all events, hence equality of measures. For unequal measures the total-variation supremum supplies a bounded witness. No neural-network architecture is assumed.
- **Operational test:** Enumerate the binary-action macro fixture in §5.5. Compare old/current probability of every path, then use indicators for paths or events with unequal mass. Verify the target discrepancy equals (3), and that valid likelihood weighting removes it.
- **Falsifier:** Exhibit unequal path measures whose integrals agree for every bounded measurable function, or show that the proof/test invoked a return outside its declared class while asserting the narrower task claim. Equal expectations for one constant or accidental task reward are **not** counterexamples to this claim and are not evidence of path-law equality.
- **Scope/upgrade log:** Proposed proof only, scope-narrowing count 0. Does not assert the necessity of importance sampling, a particular architecture, or a specific replay horizon. Independent proof verification and the method's human signature are required for a lock; a spike PASS is not a lock.

### C-B02-B-02 — Query-invariant prompt semantics require query-independent normalization state

- **State/grade:** Candidate, Grade 1, scoped to the EMA normalizer and nondegenerate downstream map.
- **Premises:** Fixed encoder weights and an EMA with $0<\alpha<1$. Allowed query batches can vary one coordinate's mean over an open interval while holding their variances and other coordinates fixed. For some fixed future probe, the downstream prompt map is nonconstant along the resulting curve of normalized probe inputs. Require the probe's prompt to be invariant to arbitrary insertion of these queries.
- **Conclusion shape:** Impossibility: updating running statistics on those queries cannot guarantee this invariance for all allowed batches/probes. Freezing buffers, isolated copies, or exactly restoring state is a necessary functional remedy within this class; `eval()` specifically is not a universal architectural necessity.
- **Proof/test:** Equation (11) maps the allowed mean interval to an interval of running means, while the variance update is common across those queries. By the stated nonconstancy there are two query means producing different probe prompts; they cannot both equal the no-query prompt. §5.2 supplies a two-coordinate constructive witness and the frozen-buffer control.
- **Falsifier:** A counterexample satisfying the nondegeneracy and arbitrary-query premises while preserving every probe output despite nontrivial updates. A constant encoder, $\alpha=0$, equal query moments, or compensating weight changes violates a premise and must be reported as such.
- **Scope/upgrade log:** Candidate only, narrowing count 0. Does not claim that every individual illegal query changes every output, or that buffer drift always increases target variance.

## 5. Pre-Registered Empirical Spike Protocol

### 5.1 Scope, execution contract, and fixed artifacts

This is a proposed registration for the independent runner, not an executed spike or a replacement for an existing orchestrator-owned `PLAN.md`. The author has not inspected B02 results. After selection, the orchestrator can freeze this protocol; the runner writes only within its designated spike directory. No robot competence, baseline superiority, or principle lock follows from these contract tests.

**Configuration:** PyTorch CPU, FP64, one thread, deterministic algorithms, seeds `0,1,2,3,4`; $D_m=229$, $d_z=256$, $d_a=29$, synthetic observation dimension 32 explicitly distinct from any robot schema. Contract toy modules use a motion BN, a `229→256→256` encoder with SiLU and spherical projection, a `288→64→29` tanh actor, and a two-layer LSTM of hidden size 16 with dropout 0 for each recurrent role. Actor input 288 is 32 observation plus 256 latent. Use affine-free `BatchNorm1d(momentum=0.1, eps=1e-5, track_running_stats=True)`. Fixture spherical projection divides by the exact nonzero norm; reject zero vectors, and test epsilon-denominator norm corrections separately. Initialize parameters using the named seed and serialize them before interventions. Also include analytic deterministic fixtures below, whose signal must not depend on random initialization.

Run command proposed for the runner:

```bash
python3 research/fb-beyond-imitation-acceleration/packets/B02/spikes/B02-B-VERIFY/run.py --device cpu --dtype float64 --threads 1 --seeds 0 1 2 3 4 --output research/fb-beyond-imitation-acceleration/packets/B02/spikes/B02-B-VERIFY/artifacts
```

Run from `/srv/claude`. Maximum two complete invocations: initial attempt and one documented harness-only fix; preserve both. A mechanism, seed, threshold, or budget change is a plan amendment, not the permitted fix. Cap each invocation at 15 CPU minutes and 2 GiB; timeout is `INCOMPLETE`, never PASS. Log Python/PyTorch versions, platform, code/config hashes, exact command, start/end UTC, all seeds, per-test metrics, and every exception. Output `metrics.json`, per-seed `.jsonl`, fixture tensors `.pt`, and machine-readable `VERDICT.json` with `PASS`, `FAIL`, or `INCOMPLETE` per family. No cherry-picking seeds.

Floating identity checks use absolute and relative tolerance `1e-10` in FP64 unless a tighter byte identity is specified. Hardware-dependent throughput is a separate result. PyTorch is not installed in the author's current Python environment, and no verification run is claimed; provisioning/execution belongs to the selected runner.

### 5.2 Test A: normalization freeze invariance and intentional corruption

Construct 64-row deterministic batches with alternating $u_i\in\{-1,+1\}$ in every channel: `current=u`, `next=2+2*u`, `expert=-5+3*u`, initial mean 0 and variance 1. Include a second fixture with channel-dependent offsets so normalization changes prompt direction after spherical projection.

1. Clone the model into compliant, duplicate-next, expert-train, and relabel-train arms. Perform current then next updates in every arm. The compliant counter advances exactly 2.
2. In the compliant arm set BN to eval and snapshot **all** buffers; make 100 expert and 100 permuted-next queries under `no_grad`. Require bitwise unchanged buffers/counters and identical outputs on a fixed probe, regardless of query order/count. Permuting a full next batch must simply permute its encoded rows. A later gradient-enabled actor/FB pass with frozen buffers must still produce nonzero parameter gradients where expected.
3. In the duplicate arm update next once more. Analytically $\mu_*=0.2$, $\mu_{dup}=0.38$, difference `0.18` in each fixture channel. Compare all means and variances to (10)–(11), using $64/63$ for the unbiased variance conversion. Counter delta is 3, not 2.
4. Update the expert and relabel arms in train mode and compare to (11)–(12). Demonstrate that `no_grad` alone still mutates buffers. Singleton train-mode BN must raise its expected batch-size error; the compliant singleton query succeeds and mutates nothing.
5. Compute the exact empirical normalized mean/covariance from a **separate** fixed probe dataset using population denominator $N$ and verify (13)–(14) within tolerance. Report $\Delta_B$, feature covariance error, and target variance error using a fixed linear toy target. Do not require variance to increase in every arm.
6. Monte Carlo estimator check: 10,000 independent pairs of 64-row Gaussian scalar batches per seed, reusing each next batch for the duplicate. Compare observed mean-estimator variance difference to (16), requiring absolute discrepancy at most 5 estimated Monte Carlo standard errors plus `1e-8`; report the covariance-term calculation (15) separately. This stochastic gate supplements the deterministic algebra checks.

**Pass rule:** every compliant invariant and formula check passes for every seed, and every intentional violating arm is detected. An alarm that also fires for compliant eval queries fails specificity.

### 5.3 Test B: command immutability and relabel corruption

Create a 256-row replay fixture; assign immutable spherical `behavior_z`, raw next frames, per-step rewards, episode IDs, and macro spans with $k\in\{1,3,10\}$. Snapshot replay tensor bytes and storage identities. Generate 100 relabel batches with fixed RNG state. Require zero writes to behavior storage, no storage alias between temporary relabels and replay commands, norm error below `1e-10`, and exactly reproduced relabels after changing only a **private clone** of behavior commands and resetting RNG. Verify the Bernoulli mask by equality with a reference RNG construction, not by demanding exactly 50% realized samples.

Task-Q mocks record the exact input command/action and target; require equality with the executed record. Then inject `behavior_z.copy_(z_update)` into a private replay copy. The integrity check must fail on the first mutation and the mocked task-Q input must demonstrate the wrong label. The analytic counterexample from §3.1 must produce target discrepancy 2. A further intervention changing raw `m_next` while preserving behavior commands must affect goal relabels in the selected goal branch, establishing that the dependency check is not vacuous.

Include true terminal, timeout, and ordinary full macro cases. For a nonterminated $k=3$ row with $V=2$, test $\gamma=0.99$ and require the target to use $0.99^3$, with the wrong-$K$ discrepancy exactly $2(0.99^{10}-0.99^3)$. For termination require zero bootstrap. Insert `severe_penetration` and `invalid` synthetic flags: the former commits exactly once; the latter commits zero times, updates no buffers, and raises a controlled halt signal.

### 5.4 Test C: drift tracking and controllability with known interventions

Use five copies of identical snapshots: no change; encoder-only change; actor-only change; normalization-only change; coordinated latent rotation. Retain fixed observations/commands and raw frames. In the analytic encoder fixture a two-dimensional orthogonal rotation by $\beta\in\{0,0.05,0.10\}$ acts on vectors wholly in that plane, giving $\Delta_B=1-\cos\beta$. In the actor fixture $\mu(o,z)=\tanh(Az+b)$, compare $\Delta_\pi$ to directly computed changed outputs and exact Jacobian $\operatorname{diag}(1-\mu^2)A$.

Require each known nonzero intervention to be detected above `1e-8` and no-change drift below `1e-10`. Encoder-only changes must leave fixed-numeric-command actions identical. Actor-only changes must leave encoder outputs identical. For $B'=RB$ and $A'=AR^\top$, newly encoded prompt actions must match while selected fixed-numeric commands change. This prevents conflating coordinate consistency with replay consistency.

For trajectory tests use the explicit deterministic plant $x_{h+1}=0.9x_h+a_h$, $x_0=0$, in 29 dimensions. Use $A_{11}=0.2$ and all other entries zero, $z=\pm16e_1$, and $b=0$; compare observed endpoints to $x_H=(1-0.9^H)a/0.1$ at $H=1,5,10$. A collapsed actor $A=0,b=0$ must have zero $S_z$, zero tangent sensitivity, and zero distinct-command divergence; the responsive actor must exceed `1e-6` in all applicable metrics, with a separate non-axis spherical command for the tangent-sensitivity test. Add a saturated actor fixture to show that parameter drift alone need not create action drift. These are controllability diagnostics for the toy plant, not evidence of contact-rich robot control.

### 5.5 Test D: bounded staleness, exact weighting, and the serious age-only null

Use an enumeratable Bernoulli-action plant to eliminate sampling uncertainty. There is one start state, $a_i\in\{0,1\}$ independently conditional on held command, reward $r_i=a_i$, endpoint $x_k=\sum_i a_i$, no termination, and fixed terminal readout $V(x_k)=x_k$. Take $\gamma=0.99$, $K=10$, and generation probabilities $p_g\in\{0.10,0.30,0.50\}$ with $p_n=0.50$. Enumerate all $2^{10}$ paths and repeat at $k=1,3$.

The exact target mean is $C_kp$, where $C_k=\sum_{i=0}^{k-1}\gamma^i+k\gamma^k$. Historical bias is $C_k(p_g-p_n)$. The exact path ratio is $W=(p_n/p_g)^{\sum a_i}[(1-p_n)/(1-p_g)]^{k-\sum a_i}$. Require agreement of the direct means, (3)–(6), and weighted expectation within `1e-10`; report exact variance and ESS under the enumerated measure. Use distinct scalar critic heads whose minimum equals $x_k$ so the twin-target construction is exercised.

For a bound certificate in this fixture, $\operatorname{TV}(\operatorname{Bern}(p_g),\operatorname{Bern}(p_n))=|p_g-p_n|$, so $\operatorname{TV}(\mathbb P_g,\mathbb P_n)\le1-(1-|p_g-p_n|)^k$. With $M=C_k$ the normalized bias bound is $2[1-(1-|p_g-p_n|)^k]$. At $k=10$, the `0.05` normalized-bias gate accepts only $|p_g-p_n|\le1-0.975^{1/10}$. Check just-inside and just-outside values and require exact acceptance decisions and actual bias $\le0.05M$ for accepted generations.

Assign a one-update-old generation $p_g=0.10$ and a 100-update-old generation $p_g=0.50$ to show that age ordering alone is not a drift certificate. Compare FIFO, exponential-age, empirical drift gate, certified fixture gate, and exact importance correction using the same 1,024 enumerated paths per generation. Use equal generation mass before arm-specific eligibility/age factors; set encoder drift to zero and apply the empirical scalar-action threshold $|p_g-p_n|\le0.05$. Fit a constant critic by the exact weighted least-squares normal equation, with no optimizer tuning. The required result is target correctness/bound compliance, **not** an unregistered requirement that gating beat every arm's learning curve. Report bias, variance, and retained generations. For a further failure-coverage fixture, terminate on the first two consecutive actions equal to 1, set that step's reward to -1, keep earlier rewards $a_i$, and zero bootstrap; enumerate the stopped tree and retain all failed paths within an eligible generation. If correction support is deliberately removed ($p_g=0$, $p_n>0$), require `UNSUPPORTED` instead of a fabricated ratio.

### 5.6 Test E: full-prefix zero-hidden burn-in versus stale cached states

Generate 8 episodes with lengths `[32,36,40,44,48,52,60,64]` and sample starts $t_0\in\{0,1,7,23\}$ with training length 8. Save generation-$g$ hidden/cell states. Change recurrent parameters by an independent seeded standard-normal perturbation times `0.05` to obtain generation $n$; set target parameters to $0.99\xi_g+0.01\xi_n$ and reconstruct target prefixes separately.

For each recurrent role, compare: whole-episode unroll at its current parameters; zero-hidden full-prefix reconstruction then training slice; stale cached generation-$g$ state then slice; and zero-hidden local burn-in of only four earlier steps. Require full-prefix hidden/cell states and all slice outputs to match the whole-episode reference within `1e-10` for every seed/start. Check gradients against a reference whole-episode forward **detached at the same slice boundary**, not against full-episode BPTT. Prefix inputs receive no gradients; slice parameters receive finite, nonzero gradients.

Require the stale and local-burn-in controls to show an output mismatch above `1e-7` on at least one nonzero start in each seed. Also use scalar recurrence $h_{t+1}=\lambda h_t+u_t$ with $u_0=1$, all later inputs zero, and change $\lambda_g=0.9$ to $\lambda_n=0.8$. At $t_0=7$, the stale state is $0.9^6$, the current full-prefix state is $0.8^6$, and four-step local burn-in from zero gives zero, providing a deterministic witness. At $t_0=0$ cached zero is expected to match; this is not an error. Test padded batches, reset boundaries, previous **executed** commands, missing-prefix rejection, and accidental sharing of online hidden states with target networks.

### 5.7 Resource and reporting gate

Time 100 warmup and 1,000 measured toy update iterations for baseline, gate-only, and correction modes, alternating order per seed with identical batch shapes and required full-prefix work. Exclude one-time setup, include amortized diagnostics and replay bookkeeping. Report median incremental wall time and a bootstrap 95% interval; the brief's cost pass requires the interval's upper endpoint below 5% for the nominated mode. Toy timing is not a production-GPU certificate. The same threshold must later be measured on the production update before claiming compliance there.

All algebra/contract families A–E must pass across all seeds. The resource gate is reported separately; no mode exceeding it is declared deployment-ready. Every negative control must be detected, including unsupported likelihoods, stale hidden states, double normalization, and label overwrite. Failure returns to adjudication/amendment; the runner does not relax tolerances or silently switch mechanisms.

Passing establishes implementation invariants and synthetic conditional-bias accounting only. Claims of breaking imitation ceilings still require the charter's multi-seed GPU training, held-out height/depth panels, 100% planner evaluation, novel-contact evidence, and compute-matched task baselines. Useful exploration beyond demonstrations remains the scientific hypothesis that these contracts make testable.
