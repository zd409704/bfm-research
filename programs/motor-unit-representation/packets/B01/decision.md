# Packet B01 Decision — Privileged Forward Input Causality, Exogenous vs Endogenous Future Load Boundaries, and 22-Group Schema Audit

- **Decision ID**: `D-B01-001`
- **Packet ID**: `B01`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (Order 1: `P=A, Q=B`): `packets/B01/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B01/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B01/spikes/B01-SPIKE/VERDICT.json` (`PASS`, CPU)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `87.05 / 100.0` | `77.0 / 100.0` (as Q) | **82.025 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `82.90 / 100.0` | `71.0 / 100.0` (as P) | **76.95 / 100.0** |

- **Winning Track**: **Proposal A (`claude` Opus)** by mean margin **+5.075** (≥ tie margin `5.0`).
- **Order notes**: Order 1 raw Δ=`+4.15` is inside the tie band (A primary / B mandatory merge); Order 2 recommends A (`Q`) by `+6.0`. Cross-order mean clears the win threshold.
- **Disposition**: **`Recommend: Proposal A` with Mandatory Merges from Proposal B and Blind Reviews**.

---

## 2. Key Adjudication Findings & Mandatory Merges

1. **Causal partition of `p_5065` (base = Proposal A)**:
   - Adopt A's per-group retain / replace / mask table with width-preserving replacements: lagged impulse-average + final-substep forces (contact block), Group 18 exogenous timers/modes, Group 20 open-loop envelope `Ψ_t=ψ(ξ_t,k)`, Group 21 past-reaction mirror, Group 6 masked with frozen normalizer `(0,1)`.
   - **Merge from B**: Explicit 5,065-slot manifest join schema `(group_id,start,stop,source,sample_time,action_latch_time,update_order,frame,units,normalization,R/G/M)` and `[0:40)` Group-18 flag/timer/phase/mode layout; classify state-triggered release progress counters as endogenous generator state, not exogenous `ξ_t`.

2. **Action-Jacobian degeneracy**:
   - Keep A's bypass identity / linear-Gaussian attenuation and stop-gradient no-op lemma.
   - **Tighten**: Theorem 2(a) premise must require sufficiency of the full target-generating state (including `ξ_{t+1}`), not physical `s'` alone (verified counterexample from Review B-on-A). Split interior-support zeroing vs singleton-support non-identifiability. Gate G-1 uses composed ratio `‖J_fut Y_a‖₂ / ‖J_a‖₂`, not the submultiplicative product of norms.

3. **Spike protocol (merged)**:
   - Keep A's arms L / C / L-sg / Z / C−ξ / X plus Step-0 BAIA.
   - **Merge from B**: Stage-A analytic FP64 `F_c` control, independent branch-return `D_ref`, EXO-PREVIEW arm, underpowered-subset rules, factual vs counterfactual residual panels, shared reference target for AEV/BIR.

4. **Hard constraints preserved**: Deployed `B_ω`, `π_θ` remain 100% free of privileged inputs; E0–E4 Markov observability retained via causal `ξ_t` + current/historical contact/load carriers.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B01-A-01`**: `tighten-premises` (withdraw Grade-1 lock until full target-state sufficiency premise repaired; stay Candidate).
- **`C-B01-A-02`**: `tighten-premises` (restrict AEV identity to common fixed target + nested information sets).
- **`C-B01-A-03`**: `Candidate` stay Grade 2 (correct EMA saturation premise ~21% residual at 320 ms / 25 steps).
- **`C-B01-B-01`**: `tighten-premises` (remove circular premise (iv); merge with A-01 singleton-support branch).
- **`C-B01-B-02`**: `Candidate` stay (sound `(u−v)²/4` lower bound).

---

## 4. Empirical Verification Summary (`B01-SPIKE`)

Executed via `/srv/claude/research/motor-unit-representation/gpu_experiments/run_b01_future_force_jacobian_spike.py` (`VERDICT.json`, status `PASS`, device `cpu`; CUDA unavailable on this host):

- G1 leak ratio `‖∂F/∂p_future‖/‖∂F/∂a‖ ≈ 12.97 ≥ 5` (`PASS`)
- G2 causal ratio `≈ 0.012 ≤ 1` (`PASS`)
- G3 Bellman residual bias reduction `≈ 9.77× ≥ 2×` (`PASS`)
- G4 deployed modules structurally free of `p` (`PASS`)

Colab/GPU package path reserved under `gpu_experiments/` for re-run when CUDA is available; CPU results are honest and gate-complete for this packet.
