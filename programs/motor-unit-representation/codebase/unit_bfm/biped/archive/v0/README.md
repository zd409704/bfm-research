# Four-motor hip-knee biped: geometric prototype v0

Model: `models/biped_4dof.urdf`. Uses meters, kilograms, seconds, radians.

The model is used to view structures and prepare follow-up portfolio experiments and has not yet been trained in double-footing strategies or proved capable of walking. V2 weights and unit training codes are maintained.

## Structure and parameters

5 rigid bodies, 4 driven joints, no ankle joints; lower leg box ends directly grounded. The left and right legs share the same pelvis, and the thighs belong to the D side of the hip unit and the P side of the knee unit respectively, and the mass is not counted twice.

| Rigid body | Dimensions | Mass |
|---|---|---:|
| pelvis | Total height 0.25 m; upright 0.04 × 0.04 × 0.21 m; beam 0.04 × 0.16 × 0.04 m | 1.0 kg |
| Left/right thigh | 0.04×0.04×0.30 m each | 0.50 kg each |
| Left/right calf | 0.04×0.04×0.30 m each | 0.25 kg each |

The total mass is **2.5 kg**, the total straight leg height is **0.85 m**, the distance between the left and right hips is **0.12 m**, and the hip points are in the same position front and back. 1 kg of pelvis is divided into 0.9 kg for the pole and 0.1 kg for the beam; the combined COM is 0.1325 m above the center of the hip, and the inertia is calculated by the parallel axis theorem. Each leg has uniform box inertia. The articulating cylinder is a visual marker only and does not add collision geometry or additional mass; the mass here is a lumped parameter assumption that encompasses the driver, not a procurement hardware specification.

The coordinates are x forward, y left, z upward, and the origin of pelvis is at the center of the two hips. All joints rotate around +y; the zero position is the torso up and the legs straight down. A negative hip angle causes the thighs to move forward; a positive knee angle causes the calves to bend backward relative to the thighs. The four joints retain [-1.2, 1.2] rad, and are not changed to unidirectional knee restraint without authorization.

The rated upper limit of each joint is 6 N·m, the damping is 0.03 N·m·s/rad, and the dry friction is 0.02 N·m. URDF required `velocity=12 rad/s` is the declared value of this geometry prototype; V2 does not have such a hard speed limit for training. If the subsequent emulator actually performs speed limiting, it needs to be verified as a new condition.

# Relationship to Existing V2

- Thighs 0.30 m, 0.50 kg are in the P/D base length and mass range of V2 at the same time, calf is also in the D range.
- The overall high and high quality of pelvis falls within the numerical range, but horizontal bias of beams, left and right branches and hips is the new combination geometry; V2 did not train the feet, nor did it have a box-type pelvis structure.
- The import of a lower layer must be calculated from the actual adjacent conjunction COM, Iyy and structure fields, especially the hip P, which shares pelvis and cannot copy the centre of a single pole or fill the entire downstream leg in a LINK mass.
- The four execution units can share frozen Actor/B weights and each maintains history; joint axes, zero positions, result fields and normalization must be aligned with V2.

# UURDF without expressed simulation settings

This file does not contain world fixed joints, and pelvis is the model root. URDF only describes the mechanism: the viewer can fix the root for pose checking; subsequent sagittal plane simulations should give the root three undriven degrees of freedom in x/z/pitch, rather than welding the torso to the world. If free roots are used, the additional lateral/roll/yaw must be handled by explicit planar constraints.

URDF does not implement V2's armature=0.003 kg·m², 1 kHz drive, 100 Hz request, 10 ms first-order response, and delay queue. These must be completed at the simulation actuator level. MuJoCo's soft limit margin=0.03 rad, friction model, contact parameters and ground must also be provided by the scene configuration. Do not substitute the URDF's effort field for the actual torque limit.

Adjacent boxes near joints are articulated connections and require consistent adjacent rigid body collision filtering; the true collision of non-adjacent rigid bodies and the ground is retained. The static preview only calculates forward kinematics, does not solve for collision, equilibrium or dynamics, and is not a walking demonstration.

## Inspection and data export

Execute in the warehouse root directory:

```bash
unit_bfm/.venv/bin/python unit_bfm/biped/inspect_model.py
```

The program reads the actual URDF, checks the rigid body tree, joint number, positive definite inertia, mass and geometric inertia consistency; imports it with MuJoCo and cross-checks the positive kinematics across multiple sets of poses. Output `model.json` and `validation.json` for preview and review. This check does not run training or physical stepping.
