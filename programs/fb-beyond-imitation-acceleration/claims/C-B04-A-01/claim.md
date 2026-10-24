# Claim C-B04-A-01

- **Author**: Author A (Claude Opus)
- **Packet**: `B04`
- **State & Grade**: Grade 2 (Candidate, tighten-premises)
- **Conclusion Shape**: Error Amplification Envelope
- **Premises**: H-step pathwise rollout with terminal FB critic bootstrap gamma^H F_bar(s_H, pi_theta(s_H,z), z)^T z, Jacobian growth L >= 1, and directional coherence cos(nabla_s F_bar - nabla_s V*, d s_H / d theta) >= c_min > 0.
- **Conclusion**: Terminal critic state-gradient error scales as gamma^H H epsilon_F^s K_a and increases with H for H <= 1/|ln gamma| whenever epsilon_F^s K_a >= |ln gamma| epsilon_F^a.
- **Falsifier**: Oracle critic substitution showing isolated terminal critic error vector norm decreasing monotonically between H=4 and H=32 under positive directional coherence.
