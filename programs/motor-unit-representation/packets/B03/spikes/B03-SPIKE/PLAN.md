# Spike Plan B03-SPIKE — Rank-16 Cross-Morphology Capacity

**Experiment ID**: `B03_RANK16_144_MORPHOLOGY_ERANK`
**Device Preference**: CPU/CUDA PyTorch SVD diagnostics.

## Pass Gates
- G1: Under proposed nondimensionalization / stratified \(\mathcal{L}_{\mathrm{orth}}\), worst-group \(\operatorname{erank}(\Sigma_B^{(k)}) \ge 12/16\).
- G2: Global unstratified baseline shows at least one group with \(\operatorname{erank}<10\) or successor relative error \(>0.20\).
- G3: Tip kinematic information retained: zero-shot decoding of nondimensional tip velocity RMSE below a preregistered threshold vs angular-only ablation.
