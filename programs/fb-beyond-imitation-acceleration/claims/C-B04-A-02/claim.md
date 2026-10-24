# Claim C-B04-A-02

- **Author**: Author A (Claude Opus)
- **Packet**: `B04`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Necessity
- **Premises**: Pathwise automatic differentiation of H-step imagined returns across state-dependent terminal hazard boundaries g(s,a) = 0.
- **Conclusion**: Multiplying hard boolean indicator masks prod 1[g(s_j,a_j)>0] yields zero pathwise gradient almost everywhere and misses the Dirac boundary integral; smooth survival probabilities p_hat_surv in (0,1) with closed-loop chain rule are necessary for pathwise hazard avoidance.
- **Falsifier**: A hard-indicator pathwise estimator without surrogate/score-function terms producing non-zero hazard-avoidance gradients away from g(s,a)=0.
