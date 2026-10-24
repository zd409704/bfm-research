# Pre-Registered Spike Plan: `B05-SPIKE`

**Packet**: `B05`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Mechanism Under Test**: R2.1 4-substep terminal boundary state machine (`invalid` strictly dominates `severe_penetration` $> 0.03$ m, which strictly dominates `success` and `timeout`) on real MuJoCo 3.17 substeps plus `PoolQuotaSchedule` (`4096` rows) and two-panel `95%` Wilson lower-bound curriculum unlock.

## 1. Metrics and Pass Thresholds
1. **Test 1 (Credible Failure Commit)**: Substep 1 penetration $> 0.03$ m with finite states/contacts across all 4 substeps yields `status == 'severe_penetration'`, `terminated == True`, `commit_to_replay == True`, `phi_next == 0.0`, and `substeps_checked == 4`.
2. **Test 2 (Post-Penetration Corruption Override)**: Substep 1 penetration $> 0.03$ m followed by Substep 3 `NaN` or Substep 4 contact buffer overflow (`ncon >= nconmax`) yields `status == 'invalid'`, `commit_to_replay == False`, `update_normalizers == False`, and `step_counter_unchanged == True`.
3. **Test 3 (Curriculum & Quota Accounting)**: Exact `4096`-row sum across 2, 5, and 7 unlocked heights, and 95% Wilson score lower bound threshold verified at `79/100` (`>= 0.70`) vs `78/100` (`< 0.70`).

## 2. Execution Command & Bounds (§12.2)
- Seed: `42`
- Maximum attempts: `2`
- Exact command: `/srv/claude/.venv/bin/python /srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b05_r21_verification_suite.py`
