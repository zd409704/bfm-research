# Pre-Registered Spike Plan: `B02-SPIKE`

**Packet**: `B02`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Mechanism Under Test**: UFO single-pass Batch Normalization update order (`(obs, m_current)` once, `(next_obs, m_next)` once, then `eval` freeze), strict `behavior_z` vs `z_update` separation, online drift metrics $(\Delta_B, \Delta_\pi)$, and full-prefix zero-hidden RNN burn-in.

## 1. Metrics and Pass Thresholds
1. **BN Freeze Invariance**: Zero drift ($0.0$) in running mean/var during `sample_ufo_mixed_z` and expert frame encoding, with `update_calls == 2`.
2. **Behavior Latent Immutability**: `max_abs_diff(behavior_z_after, behavior_z_before) == 0.0`.
3. **Full-Prefix Zero-Hidden RNN Burn-In Exactness**: `max_abs_diff(q_burnin_tail, q_exact_full_tail) < 1e-5` vs stale cached hidden state error `> 1e-2`.

## 2. Execution Command & Bounds (§12.2)
- Seed: `20261023`
- Maximum attempts: `2`
- Exact command: `/srv/claude/.venv/bin/python /srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b02_nonstationarity_spike.py`
