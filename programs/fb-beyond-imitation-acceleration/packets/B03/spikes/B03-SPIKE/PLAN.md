# Pre-Registered Spike Plan: `B03-SPIKE`

**Packet**: `B03`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Mechanism Under Test**: Kinematic-only $B(m)$ contact aliasing across distinct physical contact regimes (air swing vs `0.40` m box support vs `0.60` m impact), perceptive context disambiguation via $o_{\mathrm{low}}$ in $\pi_\theta(o_{\mathrm{low}}, z)$, and the isokinematic multi-force command bottleneck.

## 1. Metrics and Pass Thresholds
1. **Kinematic $B$-Space Aliasing**: Identical body kinematics $m$ across distinct contact contexts yield `max_abs_diff(B(m)_ctx1, B(m)_ctx2) == 0.0`.
2. **Perceptive Disambiguation**: Conditioned on context in $o_{\mathrm{low}}$, $\pi_\theta(o_{\mathrm{low}}, z)$ achieves action MSE `< 0.01` across distinct obstacle heights/contact regimes for a shared target $z$.
3. **Isokinematic Multi-Force Bottleneck**: Under identical $(o_{\mathrm{low}}, m_{\mathrm{next}})$ requiring two distinct contact force modes, a single kinematic $z = B(m_{\mathrm{next}})$ exhibits irreducible action MSE `> 0.40`.

## 2. Execution Command & Bounds (§12.2)
- Seed: `20261023`
- Maximum attempts: `2`
- Exact command: `/srv/claude/.venv/bin/python /srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b03_contact_aliasing_spike.py`
