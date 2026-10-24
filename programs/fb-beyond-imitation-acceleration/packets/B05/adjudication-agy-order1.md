# Cross-Family Adjudication Report: Packet B05 (Order 1)

- **Adjudicator**: Independent Cross-Family Adjudicator (`agy-order1`)
- **Packet**: `B05` — R2.1 Terminal Boundary (`severe_penetration` vs `invalid`) and Multi-Height Curriculum Verification
- **Candidates Evaluated**: **Candidate P** (`anonymized/order1_P.md`) and **Candidate Q** (`anonymized/order1_Q.md`)
- **Reviews Consulted**: `reviews/review-B-on-A.md` (critique on P), `reviews/review-A-on-B.md` (critique on Q), and `spikes/B05-SPIKE/VERDICT.json` (`elapsed_sec = 0.009`, logic-only contract fixture).

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

| Gate / Constraint | Candidate P | Candidate Q | Assessment Summary |
|---|---|---|---|
| **Charter §2.1**: No BC or pose-tracking fallback | **PASS** | **PASS** | Neither uses action-MSE or tracking rewards; both reject pose-tracking RMSE as a competence gate (P §3 A3; Q §2 l.147, §3 l.188). |
| **Charter §2.2**: Rollout `behavior_z` vs off-policy `z_update` separation | **DEFECT (Major)** | **PASS** | Both preserve `behavior_z` in replay and train $Q$ on `z_actual`. However, P omits the 50/50 UFO `sample_mixed_z` algorithm and off-policy BN ordering, whereas Q specifies both (§1 l.76–78). |
| **Charter §2.3**: Single-frame 229-D motion-only $B(m)$ input | **PASS** | **PASS** | Both restrict $B$ to single-frame root-relative kinematics $m \in \mathbb{R}^{229}$ with no terrain, height, or phase index (P §1.1, §3; Q §1 l.61, l.77). |
| **Charter §2.4 & Brief §2**: `severe_penetration` ($>0.03\text{ m}$) vs `invalid`; check all 4 substeps; no zero-fill or counter advance on `invalid` | **CONDITIONAL PASS** | **CONDITIONAL PASS** | Both preserve the strict $0.03\text{ m}$ threshold, run all 4 substeps after penetration, enforce `invalid > severe_penetration > success > timeout`, commit credible failures (`terminated=True, \Phi_next=0`), and reject `invalid` without advancing $S$. Both include heuristic bounds ($J_j>0.50\text{ m}$, $V_j>100\text{ rad/s}$, $\texttt{ncon}_j \ge \texttt{nconmax}$) requiring warning-counter/residual gating to avoid false halts. |
| **Charter §2.5**: Verified evidence vs unproven claims | **PASS** | **PASS** | Both explicitly classify `B05-SPIKE/VERDICT.json` (`0.009 s`) as deterministic logic-fixture evidence only, making zero claims of learned traversal or GPU acceleration. |
| **Appendix B.5 Gates**: Serious Alternative (§3), Principle Claims (§4), Falsifiable Spike (§5) | **PASS** | **PASS** | Both contain substantive rejected-alternative mathematical derivations, structured necessity claims with falsifiers, and pre-registered verification protocols. |

**Eligibility Verdict**: Both **Candidate P** and **Candidate Q** pass structural eligibility to proceed to rubric scoring; P incurs a severe rubric deduction under Dimension 2 for omitting the UFO/BN update specification.

---

## 2. Rubric Scoring and Technical Justification

| Rubric Dimension | Weight | Candidate P | Candidate Q | Row Winner |
|---|---:|---:|---:|---|
| **1. Substep Priority & Replay Isolation Rigor** | 35% | **30 / 35** | **31 / 35** | **Q (+1)** |
| **2. UFO Relabel & BN Order Fidelity** | 25% | **9 / 25** | **20 / 25** | **Q (+11)** |
| **3. Curriculum & Quota State Completeness** | 20% | **11 / 20** | **18 / 20** | **Q (+7)** |
| **4. Verification Suite Executability** | 20% | **13 / 20** | **17 / 20** | **Q (+4)** |
| **TOTAL SCORE** | **100%** | **63 / 100** | **86 / 100** | **Candidate Q (+23)** |

### Row-by-Row Technical Justification
- **Row 1 — Substep Priority & Replay Isolation Rigor (35%): P = 30/35, Q = 31/35**
  - **Candidate P (30/35)**: Proves lexicographic dominance ($\textsf{invalid}\succ\textsf{severe\_penetration}\succ\textsf{success}\succ\textsf{timeout}\succ\textsf{running}$) by induction (Prop. 1), grounds overflow/divergence in MuJoCo warning counters (`mjWARN_CONTACTFULL`, `mjWARN_BADQACC`) with $10^{-9}\text{ s}$ timing tolerance, and specifies an explicit 4096-env all-or-nothing batch transaction $\{\tau_e\}_{e<4096}$. Docked 5 pts for omitting $P_F$ from the final check domain, treating finite $J_j, V_j$ spikes as unconditional `invalid`, and conflating collection-time input normalizers with replay BN in §1.3 l.83.
  - **Candidate Q (31/35)**: Formulates clean max-latch priority $s_j = \max(s_{j-1}, e_j)$ through $s_{\mathrm{final}} = \max(s_4, e_{\mathrm{final}})$, specifies the $0.75\text{ s}$ stability dwell in exact physics substeps (`150` substeps vs `37` control ticks), and enforces atomic dual-buffer commit IDs with unfinished-macro rollback. Docked 4 pts for leaving vectorized sibling-env rollback granularity ambiguous on single-env `invalid` (Review A-on-B O2), exact float timestamp equality $t_j = t_0 + j\delta$ (O3), and unverified $V_j, J_j, \texttt{nconmax}$ triggers (O1).
- **Row 2 — UFO Relabel & BN Order Fidelity (25%): P = 9/25, Q = 20/25**
  - **Candidate P (9/25)**: Preserves `behavior_z`, macro `z_actual`, and FB target $z_{\mathrm{update}}$ with terminal mask $c = 1 - \texttt{terminated}$ (§1.3 l.81–86), but **completely omits** the UFO `sample_mixed_z` 50/50 mixture (uniform $\mathcal{S}^{255}(16)$ + online $B(m_{\mathrm{next}}[\mathrm{perm}])$), omits off-policy network BN update ordering, and omits `[T, 229]` `CandidateProvider` wiring (Review B-on-A §2.2).
  - **Candidate Q (20/25)**: Explicitly specifies updating BN once on $(o_t, m_t)$ and once on $(o_{t+1}, m_{t+1})$, freezing BN statistics, sampling `z_update` via 50% projected Gaussian and 50% online $B(m_{\mathrm{next}}[\mathrm{perm}])$ on $\mathcal{S}^{255}(16)$, keeping expert encoding in `eval`/`no_grad`, and never overwriting `behavior_z` or `z_actual` (§1 l.76–79). Docked 5 pts for omitting explicit stop-gradient $\operatorname{sg}(B(m_{\mathrm{next}}[\mathrm{perm}]))$, `[T, 229]` `CandidateProvider` naming, and granular BN order test assertions in §5 (Review A-on-B O6, O7).
- **Row 3 — Curriculum & Quota State Completeness (20%): P = 11/20, Q = 18/20**
  - **Candidate P (11/20)**: Provides exact integer `Split(M,n)` quotas for $k\in\{2..8\}$ and exact Wilson threshold $s\ge 79/100$. Docked 9 pts for four flaws (Review B-on-A §2.3): (i) replaces `PoolQuotaSchedule` credit/reservation mechanics with an unreserved reset rule $h=\arg\max_h D_h/q_h$ that allows simultaneous vectorized resets to pile onto one height while contradicting §2.1's prefix bijection; (ii) increments $S$ by 1 per 4096-env batch (§1.3 l.81), confounding `100,000` control rows with vector steps; (iii) requires *two* consecutive panels with $>10\text{ pp}$ drop for "confirmed forgetting" (§2.3 l.147), allowing a panel with active $>10\text{ pp}$ low-height regression to complete `pass_streak=2` and unlock; (iv) permits training on held-out $0.80\text{ m}$ in Stage 3 (§2.1 l.129).
  - **Candidate Q (18/20)**: Models explicit credits $C_h$ and in-flight reservations $R_h$ ($0\le R_h\le C_h$) with atomic replenishment at $\sum_h C_h = 0$ and worker wake-up, preventing `paused` deadlock across variable episode lengths (§2 l.116–120); migrates envs lazily on natural resets; counts individual accepted rows in $S$ with batch splitting at $100,000j$; triggers immediate hold/streak-reset on a single $>10\text{ pp}$ drop; and keeps $0.80\text{ m}$ strictly evaluation-only. Docked 2 pts for re-basing low-height references at each unlock (permitting multi-stage cumulative drift, Review A-on-B O8) and donating $L=3$ empty-middle credits to the frontier `(409,410,3277)` instead of the low-height reserve.
- **Row 4 — Verification Suite Executability (20%): P = 13/20, Q = 17/20**
  - **Candidate P (13/20)**: Defines concrete MuJoCo 3.17 fixtures (Test 1 $-8\text{ m/s}$ box collision, Test 2a/b/c post-penetration NaN/overflow/jump hooks) and an exhaustive 2048-pattern Boolean check of Prop. 1. Docked 7 pts for omitting R2.1 §7's mandatory **panel-continuation denominator test** (proving a `severe_penetration` episode does not halt a 100-seed panel early and stays in $n=100$), testing only static save/load hashes rather than post-resume execution parity, and not wiring through `train.py -> runner.run -> Trainer` (Review B-on-A §2.4).
  - **Candidate Q (17/20)**: Covers all three R2.1 §7 tests including panel continuation to the next seed with denominator 100 on `severe_penetration` vs immediate halt on `invalid` (§5 l.220, l.228), mandates running through `train.py -> runner.run -> Trainer` across all 6 optimizers, and compares 32 post-resume accepted controls, RNG draws, and updates within $10^{-6}$ tolerance (l.231–233). Docked 3 pts for relying on passive random seeds 101–104 for real-backend collision rather than a forced-impact fixture, lacking a negative-control valid-fall test, and using a 32-step resume window that may not cross macro/epoch/eval boundaries (Review A-on-B §4).

---

## 3. Principle Claim Adjudication (Appendix B.9)

| Claim ID | Candidate & Proposed Grade | Adjudication |
|---|---|---|
| **P: `C-B05-CAND-01`** (Committing credible failures necessary for unbiased $Q$) | Candidate P — Grade 1 | **Tighten-Premises** (`Candidate` Grade 1) |
| **P: `C-B05-CAND-02`** (Pre-statistic rejection with strict `invalid` dominance necessary) | Candidate P — Grade 1 | **Tighten-Premises** (`Candidate` Grade 1) |
| **Q: `C-B05-CAND-01`** (Deferred commit under substep corruption) | Candidate Q — Grade 1 | **Tighten-Premises** (`Candidate` Grade 1) |
| **Q: `C-B05-CAND-02`** (Preserve credible failure information for identification) | Candidate Q — Grade 1 | **Stay** (`Candidate` Grade 1) |
| **Q: `C-B05-CAND-03`** (Boundary coverage for reliable obstacle learning) | Candidate Q — Grade 2 | **Stay** (`Candidate` Grade 2) |

### Claim-by-Claim Technical Rationale
- **P `C-B05-CAND-01` (`Tighten-Premises`)**: The single-step bias identity $\tilde Q - Q^\star = p(Q_{\mathrm{cont}} - Q_{\mathrm{fail}}) > 0$ requires adding three unstated premises: unweighted survivor-only regression, absence of an external hazard estimator $\hat p(H,z)$, and a fixed evaluation law. Moreover, committing to `FBReplay` is required for $\Sigma_B$ boundary support rather than task-$Q$ identification, and the empirical falsifier conflates statistical power and planner argmax stability with critic bias.
- **P `C-B05-CAND-02` (`Tighten-Premises`)**: Under IEEE-754 arithmetic and uncheckpointed in-place EMA updates, a single NaN permanently corrupts normalizer moments. However, whole-batch 4096-env rejection and heuristic velocity bounds ($J_j, V_j$) are conservative design choices rather than logical necessities (per-env staging or rollback journals also prevent contamination). Restrict the conclusion to *pre-statistic transactional quarantine of corrupted transitions*.
- **Q `C-B05-CAND-01` (`Tighten-Premises`)**: Explicitly includes the irreversible-mutation premise and rollback equivalence carve-out, making the deduction valid, but its witness ("commit at $j=2$, NaN at $j=3$") is vacuous because $o_{t+1}$ does not exist until $j=4$. Replace the witness with *eager commit at $j=4$ prior to the post-step final audit $e_{\mathrm{final}}$ (observation-schema or reward-finiteness fault)*.
- **Q `C-B05-CAND-02` (`Stay`)**: Explicitly states all required identification premises ($p(D\mid s,a)>0$, unweighted retained-replay estimator, no external failure model) and proves via two observationally equivalent censored plants that survivor-only replay cannot identify $Q(s,a)=(1-p)r - pM$.
- **Q `C-B05-CAND-03` (`Stay`)**: Properly scoped to the frozen architecture, 5-seed protocol, and fixed budgets as a within-family empirical Grade 2 claim; requires matching *attempted* steps $N_{\mathrm{real}}$ in the censoring ablation.

---

## 4. Disposition, Mandatory Merge Items, and Confounds

- **Disposition**:
  - **Recommend**: **Candidate Q** (`anonymized/order1_Q.md`)
  - **Alternate**: **Candidate P** (`anonymized/order1_P.md`)

### Mandatory Merge Items (from Candidate P and Cross-Reviews into Candidate Q)
1. **MuJoCo Warning-Counter Grounding & Suspect-State Verification (from P §1.1 & Review A-on-B O1/O3)**:
   - Incorporate P's explicit `mjWARN_CONTACTFULL` and `mjWARN_BADQACC` counters and timestamp tolerance $|t_F - t_0 - 0.02| \le 10^{-9}$.
   - Route finite threshold exceedances ($J_j > 0.50\text{ m}$, $V_j > 100\text{ rad/s}$, and $\texttt{ncon}_j = \texttt{nconmax}$ without `mjWARN_CONTACTFULL`) to a `suspect` check that verifies solver residuals/warnings before declaring `invalid`, ensuring violent but physically valid falls never halt runs.
2. **Explicit 4096-Env Batch Abort & Reservation Release Semantics (from P §1.3 & Review A-on-B O2)**:
   - Adopt P's explicit per-env transaction buffer $\{\tau_e\}_{e<4096}$ with a batch commit barrier: if any env $e$ resolves to `invalid`, discard the uncommitted vector step across all 4096 envs, release all in-flight reservations $R_h$, leave `FBReplay`, `TaskReplay`, normalizers, $\widehat\Sigma_t$, and $S$ bitwise unchanged, and halt at the last committed barrier.
3. **Explicit Stop-Gradient & UFO/BN Verification Fixtures (from Review A-on-B O6/O7 & Brief §1.2)**:
   - Explicitly write $\operatorname{sg}(B_\omega(m_{\mathrm{next}}[\mathrm{perm}]))$ on the online-encoded half of `z_update`, enforce sequential single-pass BN updates `(o_t, m_t)` then `(o_{t+1}, m_{t+1})` followed by `eval`-mode relabeling, verify unfiltered `[T, 229]` `CandidateProvider` wiring, and add explicit unit assertions for all five UFO/BN invariants in §5.
4. **Forced-Impact Real-Backend Fixture, Full Truth-Table Sweep, and Non-Drifting Low-Height Reference (from P §2.1, §5 & Review A-on-B O8, §4)**:
   - Merge P's deterministic forced-impact fixture (driving the plant/capsule at $-8\text{ m/s}$ into the box so $d > 0.03\text{ m}$ is guaranteed on the real MuJoCo 3.17 backend), P's exhaustive Boolean dominance sweep (extended to include $P_F$ and `severe_penetration` over `success`), P's complete $k\in\{2..7\}$ quota table (resolving $L=3$ to `(1024, 1024, 2048)` while removing `0.80 m` from the training allocator table), an all-time-best/initial unlock reference (plus $x \ge 79$ floor) for $0.10\text{ m}$ and $0.20\text{ m}$ to prevent cumulative multi-stage forgetting drift, and `--resume` checkpoints placed immediately before macro truncation ($k<10$), quota-epoch replenishment, and the $S=100,000$ evaluation split.

### Confounds
Four primary confounds must be controlled during B05 execution and downstream ablation analysis. First, **attempted-vs-committed step censoring confounds**: comparing failure-commit and failure-drop arms at equal *committed* control rows $S$ grants the drop arm free uncounted physical interactions equal to the rejected collision volume; all ablations must match *attempted* transitions $N_{\mathrm{real}}$ and wall-clock GPU time $T_{\mathrm{GPU,total}}$. Second, **heuristic threshold false-halt confounds**: uncalibrated joint-speed ($100\text{ rad/s}$) or contact-count ($\texttt{ncon} = \texttt{nconmax}$) triggers can misclassify valid high-energy box impacts as numerical corruption, halting runs on exploratory falls unless gated by actual solver warning counters (`mjWARN_BADQACC`, `mjWARN_CONTACTFULL`) and calibrated against a negative-control hard-fall panel. Third, **sequential testing and reference-drift confounds**: evaluating every $100,000$ steps across multiple stages inflates cumulative Type-I unlock error (only partially mitigated by `pass_streak = 2`), while re-basing low-height references at each unlock allows up to $9.9\text{ pp}$ unflagged degradation per stage unless anchored to a non-decreasing reference and the $79/100$ Wilson floor. Fourth, **mock-vs-backend verification confounds**: `B05-SPIKE/VERDICT.json` (`0.009 s`) certifies only pure-Python state-machine and quota arithmetic, and must not be treated as evidence of real MuJoCo 3.17 contact physics or production `Trainer` resume equivalence until the merged §5 real-backend suite passes.
