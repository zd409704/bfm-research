# Claim C-B02-A-04

- **Author**: Author A (Claude Opus)
- **Packet**: `B02`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Invariant (O(d_z) Gauge Symmetry)
- **Premises**: Frozen UFO FB loss, L_orth, scalar actor loss, isotropic z_random/near laws, covariant B01 whitening, and no per-coordinate preprocessing on z before its first linear layer.
- **Conclusion**: The joint training objective is invariant in distribution under simultaneous orthogonal rotation R in O(d_z) of B, P, and the z-input layers of F, pi, Q; hence encoder drift Delta_B alone cannot bound or certify macro-critic staleness b_Delta.
- **Falsifier**: A term in the frozen joint objective that breaks O(d_z) equivariance when z has no pre-linear coordinatewise transformation.
