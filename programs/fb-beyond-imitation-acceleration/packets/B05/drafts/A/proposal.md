# Proposal A (Packet B05): Falsifiable Verification Protocols for Beyond-Imitation Competence and Training Acceleration

- **Author**: Primary Author A · **Packet**: `B05`
- **Frozen inputs**: Charter §2–§4; `baseline/02` §5–§6; `baseline/03` §2.2, §5; `baseline/05` §5.2, §6; `synthesis/B01` §1–§2.1.
- **Scope**: (i) a closed-form, order-independent terminal classifier for one `0.02 s` control step; (ii) transactional replay/normalizer quarantine; (iii) exact integer quota accounting over `num_envs = 4096`; (iv) pre-registered Wilson, multi-seed and four-dimensional compute gates.
- **Non-claim**: nothing here asserts that traversal is learned or that FB beats any baseline (Charter §2.5).
- **Evidence status**: `spikes/B05-SPIKE/VERDICT.json` = `PASS` in `elapsed_sec = 0.009`.
  - That runtime is consistent only with deterministic logic fixtures, not MuJoCo stepping.
  - It is treated as evidence for the classifier, quota and Wilson logic, **not** for real-backend physics. §5 pre-registers the real-backend re-run.

---

## 1. Exact Substep Terminal-Boundary State Machine and Data Quarantine Specification

**1.1 Predicates.** One control step at $t$ runs substeps $j\in\{1,2,3,4\}$ (`mj_step`, $\Delta t_{\mathrm{phys}}=0.005$ s), then a post-step check $j=F$.
Let $x_b^{(j)}$ be the world position of body $b$ after substep $j$ ($x_b^{(0)}$ = committed state at $t$), and let $d_c^{(j)}$ be the signed distance of contact $c$.

| Predicate | Definition | Category |
|---|---|---|
| $N_j$ | any NaN/Inf in `qpos`, `qvel`, `qacc`, `cfrc_ext`, $d^{(j)}_{1:\texttt{ncon}}$ | corruption |
| $J_j$ | $\max_b\|x_b^{(j)}-x_b^{(j-1)}\|_2>0.50$ m (implies $\ge100$ m/s in 5 ms) | corruption |
| $V_j$ | $\max_i|\dot q_i^{(j)}|>100$ rad/s over the 29 joints | corruption |
| $O_j$ | $\texttt{ncon}_j\ge\texttt{nconmax}$ or the `mjWARN_CONTACTFULL` counter increments | corruption (contacts possibly dropped) |
| $D_j$ | the `mjWARN_BADQACC` counter increments | corruption (solver divergence) |
| $P_j$ | $\max_c(-d_c^{(j)})>0.03$ m | credible failure candidate |

- $\mathrm{Bad}_j := N_j\lor J_j\lor V_j\lor O_j\lor D_j$.
- The equality $\texttt{ncon}=\texttt{nconmax}$ counts as overflow, because a full buffer cannot be told apart from a truncated one.
- $\mathrm{Bad}_F$ adds: $m_{t+1}\notin\mathbb{R}^{229}$ or a wrong observation schema or index; $|\texttt{time}_F-\texttt{time}_0-0.02|>10^{-9}$; a missing pre-reset final state.

**1.2 Transition table.** Latch $\lambda_0=\textsf{running}$. For $j=1..4$:

| $\lambda_{j-1}$ | $\mathrm{Bad}_j$ | $P_j$ | Action | $\lambda_j$ |
|---|---|---|---|---|
| any | 1 | any | stop stepping; log `offending_substep=j`, all predicates and an `mjData` dump; raise halt | $\textsf{invalid}$ (absorbing) |
| `running` | 0 | 1 | latch `failure_reason=severe_penetration` with $j^\star=j$; **keep stepping** | $\textsf{severe\_penetration}$ |
| `severe_penetration` | 0 | any | keep stepping; the latch never clears | $\textsf{severe\_penetration}$ |
| `running` | 0 | 0 | continue | $\textsf{running}$ |

At $F$, rules are applied in order:

1. $\mathrm{Bad}_F\Rightarrow\textsf{invalid}$.
2. Otherwise, $\lambda_4=\textsf{severe\_penetration}\Rightarrow\textsf{severe\_penetration}$.
3. Otherwise, the ordered event chain (baseline/05 §5.1) reports success $\Rightarrow\textsf{success}$.
4. Otherwise, $t+0.02\ge12.0$ s $\Rightarrow\textsf{timeout}$.
5. Otherwise $\textsf{running}$.

Other §5.1 failures (standing on the box, crawling, bypass) are handled like $\textsf{severe\_penetration}$ but rank below it.

**Proposition 1 (closed form and strict dominance).** Let $\mathcal B=\bigvee_{j\in\{1..4,F\}}\mathrm{Bad}_j$ and $\mathcal P=\bigvee_{j\le4}P_j$, taken over the substeps actually executed. Then
$$
\ell^\star=\begin{cases}\textsf{invalid}&\mathcal B\\ \textsf{severe\_penetration}&\neg\mathcal B\land\mathcal P\\ \textsf{success}&\neg\mathcal B\land\neg\mathcal P\land\mathrm{succ}_F\\ \textsf{timeout}&\neg\mathcal B\land\neg\mathcal P\land\neg\mathrm{succ}_F\land t_F\ge12\\ \textsf{running}&\text{otherwise,}\end{cases}
\qquad \textsf{invalid}\succ\textsf{severe\_penetration}\succ\textsf{success}\succ\textsf{timeout}\succ\textsf{running}.
$$

*Proof.* Induction on $j$ with the invariant
$$
\bigl(\lambda_j=\textsf{invalid}\iff\textstyle\bigvee_{i\le j}\mathrm{Bad}_i\bigr)\ \land\ \bigl(\neg\textstyle\bigvee_{i\le j}\mathrm{Bad}_i\Rightarrow(\lambda_j=\textsf{severe\_penetration}\iff\textstyle\bigvee_{i\le j}P_i)\bigr).
$$
- *Base case:* holds trivially for $\lambda_0$.
- *Row 1* makes $\textsf{invalid}$ absorbing, which preserves the first conjunct.
- *Rows 2–4* OR-accumulate $P$ and never return to $\textsf{running}$, which preserves the second.
- *Early stopping* after $\mathrm{Bad}_j$ cannot change $\ell^\star$, because $\mathcal B$ is already true.
- *Rule $F$* applies the stated lexicographic order. ∎

*Corollaries.*

- **C1 (order independence).** Penetration at $j^\star=1$ followed by NaN at $j=3$ gives $\textsf{invalid}$, exactly as NaN at $j=1$ does.
- **C2 (penetration beats success).** Success and penetration in the same step give $\textsf{severe\_penetration}$, so no committed success can contain a penetration.
- **C3 (success beats timeout).** A success event at the 12 s boundary is labelled $\textsf{success}$.

**1.3 Transactional quarantine.** Substeps write only into a per-env uncommitted transaction $\tau_e$. The batched step $\{\tau_e\}_{e<4096}$ is **all-or-nothing**.

- **Reject.** If any $\ell^\star_e=\textsf{invalid}$, discard all 4096 transactions. The following remain bitwise unchanged:
  - `FBReplay` and `TaskReplay`;
  - `obs_normalizer` and `motion_normalizer`;
  - the target-$\bar B$ Gram tracker $\widehat\Sigma_t$ (B01 §2.1);
  - the committed counter $S$ and the curriculum ledgers.

  Set `valid_sample=False`, write diagnostics and halt the run or panel. Resume is allowed only from the last checkpoint at a committed $S$. A single corrupt env implies possible global solver corruption, so its siblings are not trusted either.
- **Commit.** Otherwise, each env appends $(o_t,a_t^{\mathrm{applied}},o_{t+1}^{\mathrm{pre}},m_t,m_{t+1}^{\mathrm{pre}},\texttt{behavior\_z},r_t,\texttt{terminated},\texttt{truncated},\texttt{failure\_reason},\texttt{valid\_sample}{=}\text{True})$, and then $S\leftarrow S+1$.
  - `pre` = the real state before reset. The reset observation feeds only the next policy call and is never stored.
  - Normalizers update once on $(o_t,m_t)$ and once on $(o^{\mathrm{pre}}_{t+1},m^{\mathrm{pre}}_{t+1})$, per baseline/05 §4.
- **Failure rows.** `severe_penetration` rows carry `terminated=True`, `truncated=False`, $c:=1-\texttt{terminated}=0$, $\Phi_{t+1}=0$, and $r_t=\alpha(0-\Phi_t)-c_{\mathrm{ctrl}}$.
  - FB target: $\bar B(m^{\mathrm{pre}}_{t+1})+\gamma\,c\,\bar F(o^{\mathrm{pre}}_{t+1},\pi_\theta(o^{\mathrm{pre}}_{t+1},z_{\mathrm{update}}),z_{\mathrm{update}})$. The failure frame stays in the successor measure and the bootstrap stops.
  - Task macro (truncated at $k<K=10$): $(H_{\mathrm{start}},c^{\mathrm{geom}},z_{\mathrm{actual}},R_{\mathrm{macro}}=\sum_{i<k}\gamma_{\mathrm{task}}^ir_{t+i},H_{\mathrm{final}},k,\texttt{terminated}=1)$, with target $R_{\mathrm{macro}}+\gamma^k_{\mathrm{task}}\cdot0$.
  - Timeout rows keep $c=1$ and the true $\Phi_{t+1}$.

**1.4 Why credible penetrations must enter both buffers.**

- A row with $\neg\mathcal B$ is a resolved MuJoCo soft-contact transition: a hard impact of the simulated plant. It belongs to the MDP the deployable policy faces; it is not an artefact.
- Let $p(H,z)$ be the probability of a credible failure inside a macro, $Q_{\mathrm{fail}}$ the expected target on failing macros, and $Q_{\mathrm{cont}}$ the expected target on the rest. Then $Q^\star=(1-p)Q_{\mathrm{cont}}+pQ_{\mathrm{fail}}$.
- Censoring failing rows makes the regression converge to $\tilde Q=Q_{\mathrm{cont}}$, so
$$
\tilde Q-Q^\star=p\,(Q_{\mathrm{cont}}-Q_{\mathrm{fail}})\ \ge\ 0,
$$
  which is largest on the highest-hazard latents. $P_\psi$ maximises $\tilde Q$ and is therefore pushed towards them (optimism under censoring).
- FB side: censoring removes failure frames from $\rho$. Then $\Sigma_B=\mathbb E_\rho[BB^\top]$ (B01 §1) never spans them, $z_{\mathrm{goal}}$ relabels never point at them, and $F^\top z$ extrapolates with no anchor at the boundary the actor must avoid.
- Early in training, an untrained actor collides often (baseline/02 §5), so censoring would discard a large share of the Stage-0 data.

## 2. Exact 4096-Environment Pool Quota Accounting and Multi-Seed Statistical Gates

**2.1 Allocation (pure integers, $N=4096$).**

- *Notation.* Active heights are $h_1<\dots<h_k$: frontier $h_k$, low pair $\{h_1,h_2\}=\{0.10,0.20\}$, intermediates $\mathcal I=\{h_3..h_{k-1}\}$.
- *Split rule.* The remainder goes to the higher heights:
$$
\mathrm{Split}(M,n)_i=\lfloor M/n\rfloor+\mathbf 1\!\left[i>n-(M\bmod n)\right],\qquad \textstyle\sum_{i=1}^n\mathrm{Split}(M,n)_i=n\lfloor M/n\rfloor+(M\bmod n)=M.
$$
- *Case $k=2$:* $q=\mathrm{Split}(N,2)$.
- *Case $k\ge3$:*
  - frontier $q_k=N\gg1=2048$ (50%);
  - low pair $L=\lfloor2N/10\rfloor=819$ (20%) if $\mathcal I\neq\emptyset$, otherwise $L=N-2048$;
  - intermediates $I=N-2048-L=1229$ (30%), with $q_{\mathcal I}=\mathrm{Split}(1229,|\mathcal I|)$ and $q_{1,2}=\mathrm{Split}(L,2)$.
- *Pre-registered choice:* when $\mathcal I=\emptyset$, the 30% share goes to the low pair as an anti-forgetting reserve.
- *Exactness:* $\sum_hq_h=2048+L+(N-2048-L)=N$ identically, and $\min_hq_h\ge245>0$. No floating-point rounding is involved.

| Stage | Active pool (m) | $k$ | Quota $q$ (ascending $h$; **frontier** bold) | $\sum$ |
|---|---|---:|---|---:|
| 0 | {0.10, 0.20} | 2 | 2048, 2048 | 4096 |
| 1 | {0.10..0.30} | 3 | 1024, 1024, **2048** | 4096 |
| 1 | {0.10..0.40} | 4 | 409, 410, 1229, **2048** | 4096 |
| 1 | {0.10..0.50} | 5 | 409, 410, 614, 615, **2048** | 4096 |
| 2 | {0.10..0.60} | 6 | 409, 410, 409, 410, 410, **2048** | 4096 |
| 2 | {0.10..0.70} | 7 | 409, 410, 307, 307, 307, 308, **2048** | 4096 |
| 3 | {0.10..0.80} | 8 | 409, 410, 245, 246, 246, 246, 246, **2048** | 4096 |

- **Spike match.** The $k=2,5,7$ rows match `VERDICT.json` exactly.
- **Stage 3 is a separately labelled extension arm only.** Training on 0.80 m moves 0.80 out of the baseline/05 §6.2 OOD panel and turns 0.75 into an interpolation height. That arm may claim OOD only at $h=0.05$ and $D\in\{0.25,0.45\}$.
- **Env mapping.** With prefix sums $Q_i=\sum_{j\le i}q_j$ ($Q_0=0$, $Q_k=4096$), env $e$ targets $h_i$ iff $Q_{i-1}\le e<Q_i$. This is a bijection onto $[0,4096)$: no env is dropped and none overflows.

**2.2 `PoolQuotaSchedule` credit state.**

- *Quota epoch.* One epoch is `quota_epoch_control_rows = 4096` committed rows, i.e. one fully valid batched step, so $\sum_hr_h=4096$.
- *Deficit ledger.* $D_h\leftarrow D_h+q_h-r_h$. Since $\sum q=\sum r$, the invariant $\sum_hD_h\equiv0$ holds.
- *Height choice at reset.* Height is fixed per episode, so stage changes apply at each env's next reset. A resetting env takes $h=\arg\max_hD_h/q_h$, with ties going to the higher $h$. Every env always holds a height, so **no `paused` state exists** and no quota starvation is possible.
- *Rejected batches.* `invalid` batches never touch $D$.
- *Resume hash.* SHA-256 over canonical JSON of $(k,\text{stage},q,D,\texttt{pass\_streak},\texttt{hold},\text{panel history},S,\text{RNG states})$. It must be identical before save and after `--resume`.

**2.3 Wilson unlock gate.** Panels use 100 independent ground starts per height, 100% planner, frozen weights and BN, and zero replay writes. With $z=1.959964$:
$$
\mathrm{LB}(s,n)=\frac{\hat p+\frac{z^2}{2n}-z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}}{1+z^2/n},\qquad \mathrm{LB}(78,100)=0.689296<0.70\le\mathrm{LB}(79,100)=0.700200.
$$
- *Integer check.* $\mathrm{LB}$ is monotone in $s$, so the gate is implemented as $s\ge79$, with no float comparison.
- *Panel = void* if it contains any `invalid` step. The panel halts, is neither pass nor fail, and is re-run on **the same seeds**, so the denominator never shrinks.
- *Panel = pass* iff all three hold: $s_{h_k}\ge79$; zero `severe_penetration` on success episodes (asserted, Cor. C2); no confirmed forgetting.
- *Confirmed forgetting:* $\hat p_h<\hat p_h^{\mathrm{ref}}-0.10$ for some $h\in\{0.10,0.20\}$ on two consecutive panels, where the reference is the panel at the last unlock. It sets `hold=1`, which freezes unlocking with quotas unchanged. `hold` clears after one panel without such a drop.
- *Unlock* iff `pass_streak = 2` over non-overlapping panels every 100,000 committed steps. A fail resets the streak to 0; a void panel leaves it unchanged.

**2.4 Multi-seed competence gate.** Use $S_{\mathrm{seed}}=8$ independent seeds.

- *Competence at $h$:*
  - per-seed final ID panel $s_h\ge79/100$ on $\ge7/8$ seeds (one-sided exact sign test against a 0.5 per-seed pass rate: $p=9/256=0.035$);
  - zero `invalid` steps in every panel.
- *Beyond imitation at $h$:*
  - competence at $h$, plus $|h-0.7045|\ge0.20$ m, under 100% planner control;
  - the pooled planner-minus-`expert`-source success difference (same seeds; `expert` arm evaluated with $p_{\mathrm{expert}}=1$) has a Newcombe 95% CI lower bound $>0$.
- *Reported but not gating:* interpolation and OOD panels.

**2.5 Three-intervention acceleration and four-dimensional ledger.** Arms:

- $\mathrm I_0$: R2.1 FB.
- $\mathrm I_1$: Gram-whitened intrinsic reward (B01 §2).
- $\mathrm I_2$: $n$-step real-trajectory FB (baseline/03 Track 1).
- $\mathrm I_3$: $H\in\{8,16\}$ world-model hybrid with FB tail (Track 2).

| Ledger dim | Definition | Rule |
|---|---|---|
| $E$ real env steps | committed control rows; rejected rows $E_{\mathrm{rej}}$ logged separately | a run is valid only if $E_{\mathrm{rej}}=0$ |
| $M$ imagined steps | $\sum\text{batch}\times H$, including detached critic-target rollouts | $E{+}M$ ratio must be $\ge1$ |
| $V$ peak VRAM | max over processes of `max_memory_allocated` (GiB) | $\le$ pre-declared device cap |
| $T$ GPU wall-clock | GPU-hours summed over devices, incl. world-model fitting and panels | primary acceleration metric |

- *Time to gate.* $\tau_x(h)$ is the value of ledger coordinate $x$ at the first two-panel unlock of $h$. Seeds that never unlock are censored at the common budget $T_{\max}$.
- *Acceleration.* $\mathrm I_i$ accelerates at $h$ iff all three hold:
  - $\tau_T^{(0)}/\tau_T^{(i)}>1$ on $\ge7/8$ seed-paired runs;
  - the $E{+}M$ ratio is $\ge1$ (no relabelling of imagined cost as "sample efficiency");
  - $V\le$ cap, and $\mathrm I_i$ still passes §2.4 at the end of training.
- *Reporting.* All four coordinates are reported for every arm. Omitting any of them voids the arm.

## 3. Serious Alternative Considered and Rejected

**A1 (primary). Silently discard every frame with penetration $>0.03$ m, keep running, never halt.** This is attractive: it removes the `R2_FINAL` step-9 halts and keeps $\rho$ "clean". It is rejected for three reasons:

1. *Censoring bias.* By §1.4, $\tilde Q-Q^\star=p(Q_{\mathrm{cont}}-Q_{\mathrm{fail}})\ge0$. The bias is maximal on high-hazard latents, which $P_\psi$ then prefers.
2. *Missing terminal.* The pre-impact TD target at $t-1$ bootstraps through $F(s_t,\pi(s_t),z)$ with the penetrating action, and no row anywhere contradicts it.
3. *Contract violations.*
   - The logs cannot tell discarding apart from the `invalid` path, violating Charter §2.4 (credible failure must be recorded as a termination).
   - Evaluation must either drop penetrating episodes from the denominator (forbidden by brief §2) or count failures that never appeared in training.

**A2. Soft penalty for NaN/Inf or `ncon ≥ nconmax` without halting.**

- An EMA normalizer $\mu\leftarrow(1-\beta)\mu+\beta x$ with a single non-finite $x$ stays non-finite forever. The same holds for $\widehat\Sigma_t$. Rejection must therefore precede every statistic, and zero-fill imputation fabricates states (brief §2).
- Overflow drops contacts, so $s_{t+1}$ comes from a different dynamics. A penalty would put value on a simulator artefact that correlates with contact count, which trains against multi-contact hand-on-box support, the very beyond-imitation mode of baseline/02 §6.2.

**A3. Competence measured by demonstration pose-tracking RMSE.**

- *Not sufficient.* Two rollouts within link RMSE $\epsilon\ge0.03$ m of the demo can differ in contact depth by more than the penetration threshold, so RMSE cannot certify contact feasibility.
- *Not necessary.* The only demo is at $h=0.7045$. A correct step-over at $h=0.10$ needs no 0.70 m clearance and scores badly.
- *Requires a phase index.* RMSE needs a frame alignment, which the unindexed single-frame $B$ deliberately lacks.
- *Rewards the forbidden.* Its optimum is pure imitation, which Charter §2.1 forbids and which makes "beyond imitation" self-refuting.
- *Permitted use:* RMSE and nearest-demo distance may be reported as novelty diagnostics only.

## 4. Candidate Necessity Claims (Appendix B)

**C-B05-A-01: committing credible failures is necessary for unbiased task value.**

- *Necessity grade:* **Grade 1** (analytic, given the premises).
- *Premises:*
  - (P1) Rows with $\neg\mathcal B$ are transitions of the simulated MDP.
  - (P2) The macro-critic and FB targets apply the mask $(1-\texttt{terminated})$.
  - (P3) A set of $(H,z)$ of positive measure has hazard $p>0$ and $Q_{\mathrm{fail}}<Q_{\mathrm{cont}}$.
- *Conclusion shape:* every replay filter that removes credible `severe_penetration` rows has a critic fixed point with pointwise bias $p(Q_{\mathrm{cont}}-Q_{\mathrm{fail}})>0$ on that set. Committing to **both** buffers is necessary for unbiased $Q$ and for $\rho$ to support the failure boundary.
- *Operational test:*
  - commit vs. drop arms, 8 seeds, $2\times10^6$ committed steps on Stages 0–1;
  - on held-out planner rollouts, bin histories by Monte-Carlo hazard $\hat p$;
  - measure $\hat Q_1(H,z_{\mathrm{actual}})-G^{\mathrm{MC}}$ per bin.
- *Falsifier (either suffices):*
  - in the drop arm, the 95% CI of the bias in bin $\hat p\ge0.2$ contains 0 on $\ge7/8$ seeds;
  - the drop arm's planner penetration rate is not higher than the commit arm's (Newcombe lower bound $\le0$).

**C-B05-A-02: pre-statistic rejection with strict `invalid` dominance is necessary.**

- *Necessity grade:* **Grade 1**.
- *Premises:* (P1) EMA statistics are updated before any downstream filter; (P2) IEEE-754 arithmetic.
- *Conclusion:* any policy that lets a non-finite row reach a normalizer leaves it permanently non-finite. The Prop. 1 classifier with atomic batch rejection is therefore necessary.
- *Falsifier:* under alternative A2, an injected-NaN fixture leaves the normalizer finite after $10^3$ further updates.

## 5. Pre-Registered Empirical Spike Protocol

**Backend and logging.**

- MuJoCo **3.17** Python bindings, CPU, `float64`, with an instrumented 4-substep `mj_step` loop.
- Each test logs its predicate vectors and SHA-256 of both replays, both normalizers, $\widehat\Sigma$ and the schedule state.
- Any single assertion deviation fails the whole suite.
- `elapsed_sec` is mandatory, and a run under 1 s is labelled `logic-only`.

**Test 1: credible `severe_penetration` commit.**

- *Fixture:* the 29-DoF plant (fallback: a free capsule) driven at $-8$ m/s into a fixed box with soft `solref`, so that $P_{j^\star}$ is true at some $j^\star\le3$ while all $\neg\mathrm{Bad}_j$ conditions hold and $\texttt{ncon}<\texttt{nconmax}$.
- *Assert:* `status=severe_penetration`, `terminated=True`, `truncated=False`, `valid_sample=True`, `commit_to_replay=True`, $\Phi_{\mathrm{next}}=0$, `substeps_checked=4`.
- *Assert:* FBReplay and TaskReplay each grow by exactly 1, the normalizer counts by 1, and $S$ by 1.
- *Assert:* the stored $o_{t+1}$ is bitwise equal to the pre-reset state, the env resets afterwards, and the macro row has $k<10$ with target mask 0.

**Test 2: post-penetration corruption overrides `severe_penetration`.**

- *Fixture (2a):* reuse the Test 1 fixture so that $P$ latches at $j^\star\in\{1,2\}$, then a post-step hook sets `qvel[0]=NaN` after substep 3.
- *Fixture (2b):* compile with a reduced `nconmax` (or enforce a harness cap) so that $O_4$ fires after the latch.
- *Fixture (2c):* inject a 0.6 m body jump or a 150 rad/s joint velocity after the latch.
- *Assert:* `status=invalid`, `valid_sample=False`, `commit_to_replay=False`, `update_normalizers=False`, and `offending_substep` equal to the injected substep (3 or 4).
- *Assert:* the halt flag is raised, no reset observation is fabricated, all state hashes are bitwise unchanged, and $S$ is unchanged.
- *Exhaustive logic check:* all $2^4(P_{1..4})\times2^5(\mathrm{Bad}_{1..4,F})\times2(\mathrm{succ})\times2(\text{timeout})=2048$ predicate patterns must equal the closed form of Prop. 1.

**Test 3: exact 4096 quota and Wilson gating.**

- *Quotas:* for $k\in\{2,\dots,8\}$, assert $\sum q=4096$, $\min q>0$, and an exact match to the §2.1 table, including the spike's 2-, 5- and 7-height vectors.
- *Ledger:* over $10^4$ synthetic epochs with random resets and stage changes, assert $\sum_hD_h=0$ and that no env is ever left without a height.
- *Wilson:* assert $\mathrm{LB}(78,100)=0.689296\pm10^{-6}$ (fail) and $\mathrm{LB}(79,100)=0.700200\pm10^{-6}$ (pass).
- *Panel sequences:*
  - (pass, pass) unlocks;
  - (pass, fail, pass) does not;
  - (pass, void, pass) unlocks only after a same-seed re-run of the void panel;
  - a two-panel low-height drop $>10$ pp sets `hold`.
- *Resume parity:* schedule hash and 6-optimizer state hashes are equal across save and `--resume`.

**Decision rule.**

- The suite passes iff Tests 1–3 pass on the real backend.
- The existing `logic-only` VERDICT upgrades no §4 claim.
- A pass licenses only §1–§2 contract conformance. It never licenses claims of learning, competence or acceleration (Charter §2.5).
