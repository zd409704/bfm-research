# Brief B02: E0–E4 Scene Synchronization, Inertia-Scaled Rule Calibration Wiring, and Coverage Gate Closure

**Packet ID**: `B02`
**Status**: `IN_PROGRESS`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`
**Tie Margin**: `5.0` points out of `100.0`
**Baseline References**: `baseline/02-v3-asymmetric-network-and-training-specification.md`, `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md` (Audit Issues #1, #2, #3, #5, #6, #8)

---

## 1. Problem Statement

In the V3 short-run verification ledger (`baseline/03`), `coverage_ready = false` because `sustained_load_hold_count = 0`, `post_load_recovery_count = 0`, and zero-velocity holding RMSE remains `5.89–13.88 rad/s`. Six interrelated engineering and algorithmic defects (Audit Issues #1, #2, #3, #5, #6, and #8) drive this failure:
1. Step-level external torque generators are not synchronized with `E3_SUSTAINED_LOAD` ($\ge 25$ steps) and `E4_POST_LOAD_RECOVERY` scene labels (#1).
2. The analytical `rule_calibration` controller (static gravity/load bias + inertia-scaled PD + anti-windup integral) is not wired into the P0 warmup collector or the `32,768` rule replay partition (#2).
3. The $144 \times 5 = 720$-cell cross-coverage matrix (`configuration_group x scene_regime`) is not tracked as a hard gate (#3).
4. The frozen $\dot{q}=0$ diagnostic panel injects moving targets rather than static holding targets (#5).
5. Batch normalizers drift between the `32,768` rule partition and `65,536` policy partition (#6), and $\tanh$ saturation stalls actor recovery under high E3 loads (#8).

**Core Question**: What exact synchronized state-machine specification for E0–E4 scene generators, `rule_calibration` rollout wiring, normalizer updating, and $144 \times 5$ cross-coverage accounting guarantees closure of all readiness gates within bounded CPU FP32 replay (`98,304` transitions)?

---

## 2. Hard Constraints & Non-Goals

- Must strictly preserve the bounded CPU FP32 replay cap (`32,768` rule + `65,536` policy = `98,304` transitions, $\le 4.10\text{ GB}$ tensor memory).
- Must cover all `144` morphology-stroke groups (`36` geometry seeds $\times$ `4` stroke profiles across $C_0 \in \{3, 6, 9\}\text{ N}\cdot\text{m}$).

---

## 3. Deliverables Required from Primary Authors

1. **Synchronized E0–E4 Step-Level Generator Contract**: Specify deterministic episode-level and step-level torque/contact schedules for E0 (`20%`), E1 (`15%`), E2 (`20%`), E3 (`15%`), and E4 (`30%`) so that every E3 episode contains a guaranteed $\ge 25$-step sustained-load window and every E4 episode contains a guaranteed load-release transition and $\ge 20$-step recovery window.
2. **Rule Calibration Wiring & Anti-Saturation Actor Loss**: Specify how `rule_calibration` populates the `32,768` rule buffer across all $720$ `(config, scene)` cells, how normalizer statistics are computed without rule/policy covariate shift, and how pre-activation penalty or target smoothing resolves $\tanh$ saturation (#8).
3. **Frozen Static-Holding Evaluation Specification**: Define the exact static-equilibrium target vector $g_{13}^{\mathrm{hold}}(q^\star)$ and pass threshold ($\dot{q}=0$ RMSE $< 0.35\text{ rad/s}$ across E0, E3, E4).

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Resolution of Audit Issues #1, #2, #3, #5, #6, #8 | 35% | Every listed defect has an exact, non-handwavy algorithmic and code-level fix. |
| 720-Cell Cross-Coverage Guarantee | 25% | Guarantees minimum transition quota in every `(144 config x 5 scene)` cell. |
| Memory & Compute Compliance | 20% | Stays strictly inside `98,304` transitions and `4.694 GB` peak RSS. |
| Spike Falsifiability | 20% | Pre-registers exact pass criteria for `coverage_ready = true` and $\dot{q}=0$ RMSE. |
