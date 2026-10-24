# Claim C-B03-B-01

- **Author**: Author B (Codex gpt-6-astra)
- **Packet**: `B03`
- **State & Grade**: Grade 1 (Candidate, tighten-premises)
- **Conclusion Shape**: Lower Bound
- **Premises**: Two contact regimes C in {1,2} with P(C=1|U_t)=P(C=2|U_t)=1/2 at identical actor input U_t=(o_low, z_t) requiring distinct optimal torque commands ||tau_1 - tau_2||_2 = Delta > 0.
- **Conclusion**: Every measurable policy tau_hat(U_t) satisfies E[||tau_hat(U_t) - tau_C||_2^2 | U_t] >= Delta^2 / 4.
- **Falsifier**: A measurable function of U_t alone achieving conditional MSE < Delta^2 / 4 on balanced contact pairs.
