# Synthesis B05 — Autonomous 3D Obstacle Traversal R2.1 Terminal Boundary (`severe_penetration` vs `invalid`) and Multi-Height Curriculum Verification

- **Decision ID**: `D-B05-001`
- **Packet ID**: `B05`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (`gemini-4-argon-high`, Order 1: `P=A, Q=B`): `packets/B05/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B05/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B05/spikes/B05-SPIKE/VERDICT.json` (`PASS`) and NVIDIA L4 GPU (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `63.0 / 100.0` (Substep 30, UFO 9, Curric 11, Verif 13) | `63.0 / 100.0` (Substep 29, UFO 12, Curric 12, Verif 10) | **63.0 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `86.0 / 100.0` (Substep 31, UFO 20, Curric 18, Verif 17) | `80.0 / 100.0` (Substep 28, UFO 20, Curric 16, Verif 16) | **83.0 / 100.0** |

- **Winning Track**: **Proposal B (`codex` `gpt-6-astra`)** by a unanimous cross-family, order-invariant margin of **+20.0 points** (`+23.0` in Order 1, `+17.0` in Order 2; pre-registered tie margin `5.0`).
- **Disposition**: **`Recommend: Proposal B` with Mandatory Merges from Proposal A and Blind Reviews**.

---

## 2. Key Adjudication Findings & Mandatory Merges Adopted into Synthesis

1. **Exact 4-Substep Priority State Machine & Deferred Transactional Quarantine (`Proposal B` §1)**:
   - Over all 4 physics substeps $j \in \{1, 2, 3, 4\}$ (`4 x 0.005 s = 0.02 s`) and post-step audit `final`, the step status evolves via the monotone max-latch $s_j = \max(s_{j-1}, e_j)$ under strict total order:
     $$
     \textsf{invalid} \succ \textsf{severe\_penetration} \succ \textsf{success} \succ \textsf{timeout} \succ \textsf{running}.
     $$
   - **Mandatory full 4-substep execution**: detecting `penetration_depth > 0.03 m` at substep $j < 4$ latches `severe_penetration` but **never** exits the substep loop early; if substep 3 or 4 subsequently exhibits `NaN`/`Inf`, `mjWARN_BADQACC` solver divergence, or `mjWARN_CONTACTFULL` buffer overflow, `invalid` strictly overrides `severe_penetration`.
   - **Deferred transactional commit**: Credible `severe_penetration` transitions (`valid_sample=True, terminated=True`) are committed to both `FBReplay` and `TaskReplay` with terminal value multiplier $\Phi(s_{t+1}) = 0$ and measured `m_next[229]`, providing essential negative boundary support. Conversely, `invalid` transitions (`valid_sample=False`) abort before any write to `FBReplay`, `TaskReplay`, normalizers, $\widehat{\Sigma}_t$, or committed step counter $S$, and immediately halt the affected run/panel.
2. **Active Curriculum Quota Conservation (`PoolQuotaSchedule`) & Two-Panel Wilson Gate (`Proposal B` §2)**:
   - Across `quota_epoch_control_rows = 4096`, active heights $H_{\mathrm{act}}$ partition environments into `50%` frontier ($2048$), `20%` low-height reserve ($\{0.10, 0.20\}\text{ m} \to 409, 410$), and `30%` intermediate heights (`1229` split via remainder-conserving largest-remainder / prefix rules: e.g., 5 heights $\to 409, 410, 614, 615, 2048$; 7 heights $\to 409, 410, 307, 307, 307, 308, 2048$; exact sum $= 4096$).
   - Explicit credit counters $C_h$ and in-flight reservations $R_h$ ($0 \le R_h \le C_h$) replenish atomically when $\sum_h C_h = 0$ and wake paused workers, eliminating quota-starvation deadlocks.
   - Unlock requires two consecutive `100%`-planner evaluation panels (`eval_interval_control_steps = 100,000`, $n=100$ episodes per active height) achieving 95% Wilson score lower bound $\ge 0.70$ (**$\ge 79/100$ successes**, `0.7002 >= 0.70`, whereas `78/100 -> 0.6893` fails) with zero `invalid` steps and zero single-panel $> 10\text{ pp}$ low-height regression against the non-decreasing low-height reference.
3. **Mandatory Merges from Proposal A and Blind Reviews**:
   - **Merge 1 (MuJoCo Warning-Counter Grounding & `suspect` Verification from Proposal A)**: Gate finite jump/velocity/contact-count heuristics ($J_j > 0.50\text{ m}$, $V_j > 100\text{ rad/s}$, $\texttt{ncon}_j = \texttt{nconmax}$) on solver warning counters (`mjWARN_BADQACC`, `mjWARN_CONTACTFULL`) and residual checks so violent but physically valid falls are never misclassified as `invalid`.
   - **Merge 2 (All-or-Nothing 4096-Env Vector Batch Abort + Reservation Release)**: Specify explicit per-env staging buffers $\{\tau_e\}_{e<4096}$ so an `invalid` fault in any environment aborts the uncommitted vector step across all 4096 envs, releases in-flight reservations $R_h$, and preserves bitwise-identical normalizers and RNG state.
   - **Merge 3 (Stop-Gradient $\operatorname{sg}(B_\omega(m_{\mathrm{next}}[\mathrm{perm}]))$ & Forced-Impact Real-Backend Fixture)**: Include explicit stop-gradient on the online-$B$ half of `z_update`, unfiltered `[T, 229]` `CandidateProvider` assertion, Proposal A's deterministic $-8\text{ m/s}$ forced-impact MuJoCo 3.17 fixture, and 2048-pattern Boolean state-machine verification.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B05-A-01`**: `downgrade` / `tighten-premises` (Merged into `C-B05-B-02`; requires explicit unweighted survivor-only estimator and no-external-hazard-model premises).
- **`C-B05-A-02`**: `tighten-premises` (Stay `Candidate` Grade 1; narrow from whole-batch rejection to pre-statistic transactional quarantine under IEEE-754 arithmetic).
- **`C-B05-B-01`**: `tighten-premises` (Stay `Candidate` Grade 1; proof verified with post-step `final` audit witness replacing substep $j=2$ witness).
- **`C-B05-B-02`**: `Stay Candidate` Grade 1 (Proof verified; two observationally equivalent censored plants prove survivor-only replay cannot identify $Q(s,a) = (1-p)r - pM$).
- **`C-B05-B-03`**: `Stay Candidate` Grade 2 (Within-family empirical necessity claim for boundary coverage under matched attempted steps $N_{\mathrm{real}}$).

---

## 4. Empirical Verification Summary (`B05-SPIKE` & NVIDIA L4 GPU)

Verified on both CPU (`packets/B05/spikes/B05-SPIKE/VERDICT.json`, `PASS`) and **Google Colab NVIDIA L4 GPU** (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`):
- **Test 1 (Credible `severe_penetration` commit)**: 4 substeps checked, `status = severe_penetration`, `terminated = True`, `commit_to_replay = True`, `phi_next = 0.0`.
- **Test 2a (Post-penetration `NaN` at substep 3)**: `status = invalid`, `commit_to_replay = False`, `update_normalizers = False`, `step_counter_unchanged = True`, `offending_substep = 3`.
- **Test 2b (Post-penetration contact buffer overflow at substep 4)**: `status = invalid`, `offending_substep = 4`.
- **Test 3 (Curriculum Wilson gate & 4096-env quotas)**: `wilson_lb95(78/100) = 0.689296 < 0.70` (reject), `wilson_lb95(79/100) = 0.700200 >= 0.70` (unlock); exact 4096-env quota conservation across 2 heights (`2048 + 2048 = 4096`), 5 heights (`409 + 410 + 614 + 615 + 2048 = 4096`), and 7 heights (`409 + 410 + 307 + 307 + 307 + 308 + 2048 = 4096`).
