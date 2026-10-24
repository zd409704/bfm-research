# Pre-Registered Spike Plan: `B04-SPIKE`

**Packet**: `B04`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Mechanism Under Test**: Controlled 4-arm ablation comparing first-action FB successor derivative ($H=0$) against $H \in \{1, 4, 8, 16, 32\}$ causal world-model pathwise rollouts with whitened intrinsic rewards and terminal FB bootstrap $\gamma^H F(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)^\top z$.

## 1. Metrics and Pass Thresholds
1. **Short-Horizon Hybrid Gradient Superiority**: $\max_{H \in \{4, 8\}} \cos(\nabla_\theta J_H^{\mathrm{hybrid}}, \nabla_\theta J^{\mathrm{true}}) > \cos(\nabla_\theta J_{H=0}^{\mathrm{FB}}, \nabla_\theta J^{\mathrm{true}})$.
2. **Long-Horizon Compounding Error Monotonicity**: Compounded state rollout error at $H=32$ strictly exceeds $H=8$ without future reference motion hints.

## 2. Execution Command & Bounds (§12.2)
- Seed: `20261023`
- Maximum attempts: `2`
- Exact command: `/srv/claude/.venv/bin/python /srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b04_four_arm_ablation.py`
