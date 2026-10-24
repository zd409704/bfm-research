# Claim C-B02-A-02

- **Author**: Author A (Claude Opus)
- **Packet**: `B02`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Invariant
- **Premises**: Running input normalizer (count-weighted Welford or EMA(beta)) updated once on m_cur and once on m_next per FB update then frozen (eval/no_grad) across contiguous replay segments.
- **Conclusion**: (a) Frozen normalizer state is bitwise invariant under arbitrary z_update, expert, near, target, and evaluation queries. (b) Double m_next update shifts stationary mean by (mu_n - mu_c)/6 (cumulative) or ((2-beta)/(3-3*beta+beta^2) - 1/(2-beta))(mu_n - mu_c) (EMA), with telescoping difference mu_n - mu_c = (1/N) sum_G (m_last(G) - m_first(G)). (c) Train-mode batch-statistics query of size n_e incurs relative input error -> 3/(2 n_e).
- **Falsifier**: An extra normalizer update with mu_s != mu_hat that leaves stationary mean unchanged.
