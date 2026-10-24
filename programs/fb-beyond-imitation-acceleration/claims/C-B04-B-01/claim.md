# Claim C-B04-B-01

- **Author**: Author B (Codex gpt-6-astra)
- **Packet**: `B04`
- **State & Grade**: Downgraded (Autodiff Verification Identity)
- **Conclusion Shape**: Identity
- **Premises**: Exact dynamics f and exact value tail Q^{theta_0} at fixed start state s_0 with non-zero post-H policy sensitivity R_{>H} != 0.
- **Conclusion**: The truncated H-step gradient differs from the infinite-horizon fixed-start gradient by g_infty - g_H = R_{>H}.
- **Falsifier**: Retained as a 1e-6 autodiff verification check rather than a necessity claim.
