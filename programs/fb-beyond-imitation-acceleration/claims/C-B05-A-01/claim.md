# Claim C-B05-A-01

- **Author**: Author A (Claude Opus)
- **Packet**: `B05`
- **State & Grade**: Grade 2 (Candidate, downgraded/merged with C-B05-B-02)
- **Conclusion Shape**: Estimator Bias
- **Premises**: Unweighted survivor-only replay regression without an external failure-probability estimator on transitions with positive severe_penetration probability p > 0.
- **Conclusion**: Censoring credible severe_penetration transitions induces positive value optimism bias p(Q_cont - Q_fail) > 0.
- **Falsifier**: An unweighted survivor-only critic estimator that identifies Q*(s,a) across two plants differing only in terminal penetration probability p.
