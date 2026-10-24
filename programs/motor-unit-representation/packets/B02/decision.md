# Packet B02 Decision — E0–E4 Scene Sync, Rule Calibration, Coverage Gates

- **Decision ID**: `D-B02-001`
- **Packet ID**: `B02`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (Order 1: `P=A, Q=B`): `packets/B02/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B02/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B02/spikes/B02-SPIKE/VERDICT.json` (`PASS`, CPU)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `78.00 / 100.0` | `71.0 / 100.0` (as Q) | **74.50 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `78.00 / 100.0` | `80.0 / 100.0` (as P) | **79.00 / 100.0** |

- **Winning Track**: **Tie / Hybrid** (mean margin `+4.50` for B, strictly inside tie margin `5.0`).
- **Order notes**: Order 1 exact numerical tie `78.00` vs `78.00` with P(=A) as Primary Generative / Adaptive-Normalizer / Rule-Transient Base and Q(=B) as Co-Primary Atomic-Storage / Net-Feasibility / Evaluation-Gate Base. Order 2 recommends P(=B) by `+9.0`. Cross-order mean does not clear the win threshold.
- **Disposition**: **`Recommend: Tie / Hybrid`** — merge both scaffolds with mandatory fixes listed below. Treat B as slight mean-score primary for atomic storage / evaluation gates; keep A's generative schedule, adaptive normalizer, and rule-transient scaffolding.

---

## 2. Key Adjudication Findings & Mandatory Merges

1. **E0–E4 generator (hybrid)**:
   - Adopt A's explicit 80-step half-open interval tables and full-rollout certificate with failed-attempt rule.
   - Adopt B's pure `make_program(run_seed, config_id, scene, n, domain, variant)` Philox-4x32 key (add explicit `variant` / `episode_id` so E4-R and E4-RI never collide at ordinal 0).
   - External load: B's net-equilibrium $\tau_{\mathrm{ext}} = -\tau_g(q^\star) - \sigma m S_{\max}$ with $m \in [0.25, 0.92]$; **alternate $\sigma$ deterministically in training** via $\sigma = (-1)^{c+n}$ (or equivalent), redrawing when $|\tau_{\mathrm{ext}}| < 0.25 S_{\max}$ or $|u^\star| > 0.92$ (flag `INFEASIBLE_CONFIG`). Fixes A's single-sign training and B's sign-flip underflow / step-on onset.

2. **Rule calibration wiring**:
   - Adopt A's inertia-scaled PID + bias with explicit $J_{\mathrm{nom}}(c) = I_{D,zz}(c) + n_g(c)^2 J_{\mathrm{rotor}}(c)$.
   - Regime-dependent feedforward: $\kappa=1$ (one-step-delayed $\tau_{\mathrm{ext},t-1}$) in E3; $\kappa=0$ in E4 so the integrator winds during the loaded phase and produces a true post-release recovery (fixes zero-latency feedforward tautology).
   - Pre-roll history fill before `t=0` (from B) so early-window validity masks do not discard rows.
   - Lag rule `τ_ext` knowledge by pre-registered `d` intervals at release edges; exclude k post-edge intervals from logit-imitation.

3. **720-cell coverage gate**:
   - Hard gate on the joint `144×5` array (not marginals). Accept Grade-1 claim that equal marginals do not certify joint coverage.
   - De-synchronize sub-cases: anchor `(j+c) mod 3`, tier `(⌊j/3⌋+⌊c/3⌋) mod 3`; add resident `(scene, anchor, λ, σ)` marginal alongside the 720-cell array.
   - Require ≥1 resident rule witness at `λ=0.92` per configuration (tier-qualified).
   - Window-residency counting: $720×64 = 46{,}080 > 32{,}768$ ⇒ mean witness length ≤ `45.51`; use atomic commit / staging when cell capacity `< 2ℓ_s`.

4. **Normalizer & saturation (#6, #8)**:
   - Dual-partition BN contract with fail-closed refresh; function-preserving normalizer refresh is a registered alternate arm (fix Adam-state transform before later packets).
   - Pre-activation hinge / logit path required: bounded action derivative alone cannot prevent `sech²` squash decay (Grade-1 claim accepted).
   - Saturation-recovery probe as a registered arm with identical smoothing in both arms.

5. **Static-hold panel (#5)**:
   - Single canonical 13-field `g_hold` with zero velocity/acceleration (A); both load signs; position + contact guards.
   - Evaluator negative control + rule positive control (from B); `CONTROL_FAIL` ≠ physical infeasibility.
   - Physics-readback event predicates with `scene_sync_violation_count` (≤1 count per episode per event type).
   - Bounded initialization retries + dedicated reason code; stop-contact alone must not abort.

6. **Memory compliance**:
   - Produce 512-slot provenance audit before sealing memory claims; compute model/target/optimizer bytes from frozen architecture; keep a lossless fallback that needs no slot assumption.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B02-A-01` / `C-B02-P-01` (window-residency / counting)**: `Candidate` Grade 1 — ACCEPT WITH NARROWED SCOPE (explicit disjoint-witness premise; mean bound `45.511`; narrow FIFO impossibility to i.i.d. insertion).
- **`C-B02-A-02` / `C-B02-P-02` (saturation attenuation)**: `Candidate` Grade 1 — REVISE PREMISE (remove claim that finite hinge forces `|y|≤y_max` at stationarity; keep head-Jacobian lower bound inside region + non-binding at holding optima).
- **`C-B02-B-01` / `C-B02-Q-01` (marginal ≠ joint coverage)**: `Candidate` Grade 1 — ACCEPT / ENDORSE (gate must use joint array).
- **`C-B02-B-02` / `C-B02-Q-02` (squash gradient decay)**: `Candidate` Grade 1 — ACCEPT / ENDORSE (bounded critic TD path alone cannot guarantee exit from deep `tanh` saturation).

---

## 4. Empirical Verification Summary (`B02-SPIKE`)

Executed via `gpu_experiments/run_b02_scene_sync_coverage_spike.py` (`VERDICT.json`, status `PASS`, device `cpu`):

- G1 E3 sustained ≥25: `PASS`
- G2 E4 release + recovery ≥20: `PASS`
- G3 144×5 min quota (`filled_min=136`, budget `98,304`): `PASS`; `coverage_ready=true`
- G4 static-hold RMSE < 0.35: E0 `0.0`, E3 rule `≈0.020`, E4 rule `≈0.030` (`PASS`)

Counts: `sustained_load_hold_count=288`, `post_load_recovery_count=288`. Full physics collector wiring remains the engineering merge target; CPU scheduler + rule-calibration RMSE surrogate is gate-complete for this packet.
