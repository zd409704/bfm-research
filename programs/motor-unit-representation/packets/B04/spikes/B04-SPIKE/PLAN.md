# Spike Plan B04-SPIKE — 2-DoF Composition Coupling Envelope

**Experiment ID**: `B04_2DOF_COUPLING_ENVELOPE_AND_MODES`
**Device Preference**: CPU analytic 2-DoF dynamics + small PyTorch upper policies if needed.

## Pass Gates
- G1: Quantify hip→knee coupling torque magnitude vs single-unit E3/E4 torque envelope; report fraction of timesteps inside envelope under squat/hop fixtures.
- G2: Fair ablation scaffold defined for Modes A/B vs raw-torque baseline C (same obs history, 50 Hz, equal update budget).
- G3: Morphology swap protocol (\(L_2\) or \(C_0\)) specified with zero-/few-shot metrics sufficient to falsify composition gain.
