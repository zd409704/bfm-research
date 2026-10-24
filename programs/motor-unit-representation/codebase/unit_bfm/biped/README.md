# Quad Motor Hip Knee Biped: V2 Rod Combo v1.1

This version is redesigned based on the existing execution unit: **four joints, five uniform rods, and one planar floating root**. Cancel the combined pelvis and beam of v0; use V2’s original square bar geometry and inertia formulas for the trunk, thighs, and calves. A URDF, an executable MuJoCo scenario, and an access layer for four frozen V2 units are provided. Upper walking strategies have not been trained and standing or walking abilities have not been verified.

## Structure and unit mapping

The units are meters, kilograms, seconds, and radians. All rod sections are **0.04 × 0.04 m** without counterweight.

| Rigid body | Length | Mass | Iyy at COM (kg·m²) |
|---|---:|---:|---:|
| shared trunk pelvis | 0.25 m | 1.00 kg | 0.005341667 |
| Left and right thighs | 0.30 m each | 0.50 kg each | 0.003816667 each |
| Left and right calves | 0.30 m each | 0.25 kg each | 0.001908333 each |

Total mass * * 2.5 kg * *, straight leg height * * 0.85 m * *, left and right hip shaft mounting point spacing * * 0.18 m * *, total collision geometry width * * 0.22 m * *; clear interval between legs is * * 0.14 m * *. Ankleless motor, no extra feet, direct grounding at the end of the calf square rod. The cylinder only marks the joints and the transverse mounting axis, without increasing inertia or collision; the connection adopts the ideal rigidity constraint, and the transverse axis is not the added physical mass. Quality is a centralized parameter assumption, not a hardware assembly design that includes specific motor mounting hardware.

| Unit sequence | Motor | P rod | D rod |
|---|---|---|---|
| 1 | left_hip | shared torso | left thigh |
| 1 | left_knee | left thigh | left calf |
| 3 | right_hip | shared torso | right thigh |
♪ 4 right_knee ♪ Right thigh ♪

The thighs are both hip D and knee P and thus meet the intersection of the two roles: length **0.25-0.40 m**, basic mass **0.40-0.60 kg**. Currently used 0.30 m, 0.50 kg. Torso 0.25 m, 1 kg in P range, calves 0.30 m, 0.25 kg in D range. Sharing the conjunctal body in a physical model counts only once; Do not impersonate the mass of the entire downstream chain as the mass of a single D pole.

Coordinates are x forward, y left, z up, with the pelvis origin at the midpoint of both hips. All motor shafts are + y; zero torso up, legs down. The negative hip angle causes the thigh to swing forward, and the positive knee angle causes the calf to bend backward relative to the thigh. All joints remain * * [− 1.2, +1.2] rad * * with no additional one-way knee limit.

Based on feedback that the hip distance is too narrow, this version widens the legs from y=±0.03 m to **y=±0.09 m**. The axial offset from the trunk COM to the hips is ∓0.09 m; this is outside of the original local structure. It has been compared with the two hip y=0 models to verify that the mass matrix and gravity/velocity offset terms are the same under the x/z/pitch plane constraints. This result does not imply that the three-dimensional dynamics or collision sets are identical, nor does it allow for cancellation of planar constraints. When subsequently adding the mass of the real horizontal axis, bearing or bracket, the trunk inertia needs to be resynthesized and the range verified.

# V2 Interfaces and Dynamics

`design.json` is the design parameter file, `build_model.py` generates `models/biped_4dof.urdf` and `models/biped_4dof.xml`. URDF expression agency; supporting MJCF gives three unactuated degrees of freedom to the torso x/z/pitch, totaling 7 degrees of freedom and 4 drives. Ground contact is handled by a physical solver; adjacent articulating rods exclude collisions and other collisions remain.

`runtime.py` completes the following V2 nominal configuration:

- Physical and drive 1 kHz, unit command 100 Hz; request is `6u N·m`, after delay queue, capacity clipping and first-order response.
- Nominal capacity 6 N · m, response time 10 ms, delay 0 ms; joint damping 0.03, dry friction 0.02, armature 0.003, soft limit margin 0.03 rad.
- Same joint limit solution parameters, ground friction and contact parameters as V2. Nominal dynamics are currently used and bipedal training randomization is not performed.
- `o24` provides the pole's world attitude, COM velocity, actual moment, contact, and interval-averaged environment wrench in V2 field order; includes explicit external forces applied to COM, excluding gravity and internal joint reactions. It still relies on simulated truth values.
- `m28` is calculated from the mass, inertia, relative joint COM, etc. of the actual model, without fictitious equivalent rod parameters. The four rows were compared with the original `Structure.nominal()`.

URDF Mandatory `velocity=12 rad/s` is metadata only; companion emulation does not perform this V2 untrained additional hard speed cap. When importing URDF separately to other emulators, the drive, root constraint and contact configuration should be restored as per this section.

`FrozenBiped` directly loads the existing `candidate_unit_with_schema.pt`, shares frozen Actor/B weights, and handles four joints with four independent history lines. Each time `z[4,16]` is received, it takes 10 ms and returns `feedback[4,197]`. Changing z does not clear the history, it will be cleared only after reset. The example only shows access, not walking commands:

```python
import torch
from unit_bfm.biped.runtime import FrozenBiped

robot = FrozenBiped('unit_bfm/artifacts/rf_v2_full/candidate_unit_with_schema.pt')
feedback = robot.reset () # Initial feedback from four units
z = torch.randn(4, 16) # Demonstrates random intent; the upper policy has not been trained yet
for_in range (4): # Upper layer holds z in four 10 ms steps at 25 Hz
    feedback = robot.step(z)
```

# Reconstruction & Inspection

Execute in the warehouse root directory:

```bash
unit_bfm/.venv/bin/python -m unit_bfm.biped.build_model
unit_bfm/.venv/bin/python -m unit_bfm.biped.inspect_model
unit_bfm/.venv/bin/python -m unit_bfm.biped.audit_range
unit_bfm/.venv/bin/python -m unit_bfm.biped.validate_compatibility
```

- `model.json` / `validation.json`: Export preview data from actual URDF, check geometric inertia, rigid body tree and 36 sets of forward kinematics.
- `range_audit.json`: Reads the 128 structure XML saved by V2 and compares the marginal range of 14 nominal fields; all four units are in range, but not an exact copy of one of the sampled structures in the library.
- `compatibility.json`: Check member full COM inertia tensor, m28, 24 sets of URDF/MJCF attitude, plane inertia equivalence of axial staggering, COM velocity, actuation response and delay, true contact and shared member external force mapping. In addition, 100 control steps (1 second) are run with actual frozen weights, and the results, historical continuity, and weights of four rows of batch calls and four independent units are checked. FP32 batch calculation allows a small amount of rounding error, and the report records the measured error.

** Structure and interface access completed. ** R2 of V2 has a site without an adjacent driver, R3 has a adjacent PD driver without ground; Shared torso, twin legs and multiple learning controllers are still new combinations. The local generation rules are compatible, range of values, and one second of interconnectivity, and cannot be a substitute for standing/walk training and acceptance. The capability validation status of the original candidate weight was not changed by the re-engineering of the model.

The old version of the combined pelvic model and its review is retained at `archive/v0/`; the current entrance always points to this version of the combined rods.
