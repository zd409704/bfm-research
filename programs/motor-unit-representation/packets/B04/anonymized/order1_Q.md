# Candidate Q (Packet B04): Composing Frozen Local Motor-Unit Representations into Multi-Joint Limb Controllers Under Coupled Loads

Author track: B. Status: proposal and preregistration; no downstream experiments are claimed. Method version: v1.0. Scope: two actuated planar joints, including a passive vertical base coordinate for physical squat and flight. All quantities below use SI units.

The proposed test is whether a single, independently qualified local checkpoint, instantiated at hip and knee with frozen weights and preprocessing, reduces downstream learning cost relative to torque control. The central distinction is between an **exact scalar torque reduction**, which is available, and **distributional coverage of the resulting closed-loop disturbance**, which must be measured. A matching peak torque alone does not establish coverage or stability.

Frozen sources read: `PROGRAM_CHARTER.md`; `packets/B04/brief.md`; `baseline/01-motor-unit-proprioception-and-representation-design.md`; `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md`; decisions `D-B01-001`, `D-B02-001`, and `D-B03-001`. No other B04 author draft is used. B02's CPU scheduler/rule surrogate and B03's candidate-level mechanism spike do not establish a converged deployment checkpoint. The 101-update V3 smoke run is not an eligible confirmatory checkpoint.

## 1. Multi-Body Coupling Dynamics Reduction

### 1.1 Coordinates, energies, and exact fixed-base equations

Let world axes be horizontal x and upward y. The hip is at `(0,h)`; first take h constant. Joint q1 is the first link angle from +x, and q2 is the relative knee angle. Write θ=q1+q2, e(α)=(cos α,sin α), and e_perp(α)=(-sin α,cos α). Links have lengths L1,L2, masses m1,m2, COM distances c1,c2, and planar COM inertias I1,I2. A point payload mp is rigidly attached at the foot. Bodies are rigid; joint transmissions are ideal torque sources. Rotor inertia is zero in this benchmark; adding rotor dynamics requires an explicitly revised mass matrix, not silently adding diagonal inertia to a moving-stator model.

Positions are r1=(0,h)+c1 e(q1), r2=(0,h)+L1 e(q1)+c2 e(θ), and rf=(0,h)+L1 e(q1)+L2 e(θ). Define

- A=I1+m1 c1²+(m2+mp)L1²;
- D=I2+m2 c2²+mp L2²;
- H=L1(m2 c2+mp L2);
- K=m1 c1+(m2+mp)L1, and d=m2 c2+mp L2.

The kinetic energy is T=½ qdotᵀ M(q) qdot and the configuration-dependent potential is V=g[K sin q1+d sin θ]. Thus the Euler–Lagrange equations, with viscous/Coulomb friction f and stop torque τstop, are

    M(q) qddot + c(q,qdot) + G(q) + f(qdot)
        = S u + Jf(q)^T Ff + τstop,

    M = [[A+D+2H cos q2, D+H cos q2],
         [D+H cos q2,    D]],

    c = [-H sin q2 (2 qdot1 qdot2 + qdot2²),
          H sin q2 qdot1²],

    G = g [K cos q1+d cos θ, d cos θ]^T,

    Jf = [[-L1 sin q1-L2 sin θ, -L2 sin θ],
          [ L1 cos q1+L2 cos θ,  L2 cos θ]].

Here S=diag(C01,C02), u∈[-1,1]², and Ff=(Ft,Fn) is the force **on the robot**. These equations include distal joint motor reaction through the coupled dynamics; adding a separate `-τ2` to the first generalized equation would double-count internal actuation. Payload inertia and gravity are explicit, not an independently sampled “external force.”

For ideal unilateral ground, yf≥0, Fn≥0, yf Fn=0, and |Ft|≤μFn, with impact law specified separately. The executable benchmark instead uses the fully specified compliant contact below. In either case, contact torque is JfᵀFf; the two local torques are correlated projections of the same force.

### 1.2 Mapping to the frozen local motor equation

Take the unloaded, isolated-link reference inertias J01=I1+m1c1² and J02=I2+m2c2². Use local gravity terms G01=m1gc1 cos q1 and G02=m2gc2 cos θ, with knee gravity expressed through its actual housing attitude. For j≠k define signed right-hand-side contributions

    τinertial,j = -(Mjj-J0j) qddotj - Mjk qddotk,
    τCoriolis,j = -cj,
    τgrav,j     = -(Gj-G0j),
    τcontact,j  = (Jf^T Ff)j,
    τext,j      = τinertial,j+τCoriolis,j+τgrav,j+τcontact,j.

Then, exactly in continuous time,

    J0j qddotj + bj qdotj + τfric,j + G0j - τext,j
        = C0j uj + τstop,j.

Moving τstop to the left gives the corresponding E1 local equation. This has the sign convention of baseline/01 §3.1. In particular a positive external torque reduces the actuator effort required to hold against positive gravity torque. B02 uses its own signed gravity-load symbol in its generator formula; implementations must convert signs through this equilibrium identity, not copy that formula without its convention.

The decomposition fixes the meaning of J0. Alternatively setting Jeff=Mjj moves the self-acceleration term into local inertia, but changes the local plant with posture. One cannot make coupling disappear by relabeling Jeff while retaining an unmeasured training-inertia assumption. Estimated acceleration from x137 gives only a filtered diagnostic approximation to this identity; solver acceleration is used for the physics audit and is never an actor input.

For the knee, P2=D1. Its joint-center acceleration at fixed hip is

    aP2=L1[qddot1 e_perp(q1)-qdot1² e(q1)].

For a distal vector r in housing coordinates, the world acceleration is

    aD=aP2+R1[a_rel+2ω1×v_rel+α1×r+ω1×(ω1×r)].

The four extra terms are translation, Coriolis, Euler, and centrifugal acceleration. Relative local tip velocity and acceleration in g13 remain the calibrated housing-frame quantities; substituting world tip acceleration would change the frozen interface. Parent motion therefore changes dynamics without necessarily being identifiable from one local observation.

### 1.3 A physical hopping extension with only two actuators

A fixed hip can strike or lift its foot but cannot undergo body flight. For squat and hopping, mount a nonrotating hip carriage of mass mb on a frictionless vertical rail. This adds passive h, not a third motor. Let mt=mb+m1+m2+mp, a(q)=[K cos q1+d cos θ, d cos θ]ᵀ, and

    ch=-K sin q1 qdot1²-d sin θ (qdot1+qdot2)².

The exact three-coordinate equations are

    [[mt, a^T], [a, M]] [hddot, qddot]^T
      + [ch+mt g, c+G+f]^T
      = [Fn, S u+Jf^T Ff+τstop]^T.

The horizontal rail reaction does no work in the permitted coordinates. The local reduction above acquires `-aj hddot` in τinertial,j. Eliminating h yields the joint mass matrix `M-aaᵀ/mt` and the corresponding load term `-(a/mt)(Fn-ch-mt g)` on the right. Both forms must agree numerically. In free fall gravity can largely cancel through the base-acceleration term; treating fixed-base gravity plus ground reaction as the whole load is incorrect. Analyses report fixed-base and rail results separately.

### 1.4 Quantitative envelope comparison

For bounds |qdotj|≤Vj, |qddotj|≤Aj, |hddot|≤Ab, and contact magnitude ||Ff||≤Fmax, conservative component bounds are

    |τinertial,1| ≤ (A+D+2|H|-J01) A1+(D+|H|) A2+(K+d) Ab,
    |τinertial,2| ≤ (D-J02) A2+(D+|H|) A1+d Ab,
    |τCoriolis,1| ≤ |H|(2V1 V2+V2²),
    |τCoriolis,2| ≤ |H| V1²,
    |τgrav,1| ≤ g[(m2+mp)L1+d],
    |τgrav,2| ≤ g mp L2,
    |τcontact,1| ≤ (L1+L2) Fmax,
    |τcontact,2| ≤ L2 Fmax.

These triangle bounds are conservative and generally not attained simultaneously. At the nominal parameters of §3, with mp=0.20, V1=V2=4 and A1=A2=20, A=0.197333, D=0.069333, H=0.088, J01=0.053333 and J02=0.037333. The fixed-base inertial bounds are 10.93 N m at hip and 3.79 N m at knee; Coriolis bounds are 4.22 and 1.41 N m; added-gravity bounds are 5.69 and 0.785 N m. Dividing by nominal C0=9 gives (1.22,0.42), (0.47,0.16), and (0.63,0.087), respectively. These are illustrative bounding calculations, not rollout statistics. A 30 N contact can project up to 24 and 12 N m: even moderate force can exceed actuator capacity, although force direction and posture often reduce the actual moment.

B02 specifies **net equilibrium actuator demand** tiers m∈[0.25,0.92], both load signs, ≥25-step sustained windows, and ≥20-step post-release windows. It does not certify that all arbitrary external torques in ±0.92 C0 were learned. Neither the frozen sources nor the B02 decision provide measured maximum contact impulse, torque slew, moving-parent acceleration, or action-conditioned coupling coverage. Those quantities must not be invented.

| Local regime | Plausible limb analogue | Conditions for a coverage claim; common failure |
|---|---|---|
| E0 free motion | Slow unloaded tracking | Inertia/gravity and state histories match the trained support. “No foot contact” alone does not imply E0: distal acceleration can dominate. |
| E1 stops | Either joint at its calibrated stop | Same normalized margins, approach speed and stop compliance; simultaneous stops plus contact can be an unseen compound event. |
| E2 contact | Stance and compliant touchdown | Match contact moment, stiffness/damping, force direction, duration, lever arm, and contact-state-conditioned transitions. Two independent E2 marginals do not certify shared-contact coupling. |
| E3 sustained load | Squat hold/persistent payload | ≥0.5 s plateau, correct sign and equilibrium demand, sufficient torque reserve, plus matched state/inertia/parent-motion histories. Large oscillatory coupling is not an E3 hold merely because its mean is constant. |
| E4 release/recovery | Toe-off, unload and landing recovery | Actual load removal followed by ≥0.4 s quiet recovery; match impulse and release slew. Repeated impacts without a quiet interval are a separate out-of-envelope condition. E4 is not synonymous with any impulse. |

For each unit log component torques and the combined demand. At 20 ms control intervals define λ=τext/C0, slew `s=|λt-λt-1|`, impulse `i=|∫τext dt|/(C0·0.02)`, demand `r=|J0 qddot+f+G0-τext|/C0`, and residual-contact impulse separately. Also log normalized inertia Mjj/J0, cross coefficient Mjk/sqrt(Mjj Mkk), state/stop margins, dwell, housing acceleration, and neighbor phase. Capacity feasibility uses r, not |τext| alone. For static holds require r≤0.92; exceeding this is an actuator feasibility violation, not evidence against a learned representation.

Build a reference envelope only from real, checkpoint-associated E0–E4 physics trajectories over the full 144×5 cells, keeping failed attempts. For each configuration and regime report min/max and 0.5/99.5 percentiles of the above quantities, plus joint bins of (state, load sign, demand tier, inertia, dwell/impulse). A window is *amplitude-compatible* only if it passes these marginal bounds; call it *empirically supported* only if its joint-bin occupancy and one-step conditional response also pass §6. Outside any certified interval is OOD; empty bins or missing moving-parent data mean UNKNOWN, never implicit support. Compare local regimes separately and report hip/knee joint event combinations. E3 exogenous schedules cannot by themselves certify action-dependent neighbor or contact loads. Independent local stability is insufficient to prove stability of their interconnection.

## 2. Upper-Layer Calling Architecture Comparison

### 2.1 Interfaces and frozen boundary

| Arm | Learned upper output at 50 Hz | Fixed adapter and local execution | Principal uncertainty |
|---|---|---|---|
| A | 32 unconstrained scalars, split into two 16-vectors | z=4v/||v||; π(x137,z) for each joint | Full sphere access can select poorly trained latent directions. |
| B | 26 scalars, split into desired g13 vectors | Deterministic physical-consistency projection Pκ, frozen outcome normalizer/Tκ and B; radius-4 projection, then π | B's image can restrict reachable latent commands; a desired response is not an inverse-dynamics guarantee. |
| C | 2 scalars | tanh to u1,u2; same torque latch and capacity | Must learn local regulation and coordination jointly. |

At ||v||<10^-8 use 4e1; log its frequency. The denominator is not `||v||+epsilon` outside this branch, so radius is exactly four. Do the same for a near-zero B output. A and B share the same checkpoint at both joints, separate causal history buffers, and no inter-joint weight adaptation. Freeze B, actor, normalizer statistics, B03 Tκ conventions, any λ-anchor parameters and recurrent state update rules. Calibration supplies actual geometry/capacity only through the existing approved schema. Updating those measured constants after a hardware swap is calibration, not fitting; adding learned slots is prohibited. Optimizers contain only upper-policy/value parameters, and file hashes plus parameter-byte hashes are checked throughout.

Pκ is a fixed metric projection onto the attainable **kinematic** g13 manifold in the export manifest: select bounded q*, qdot*, qddot* and normalized torque u*, reconstruct all dependent sine/cosine and tip position/velocity/acceleration fields using baseline/01, and apply B03 Tκ exactly once. Formally minimize squared normalized distance to the raw 13-vector over q* within the stroke with 0.05 rad margin, |qdot*|≤8, |qddot*|≤80, and |u*|≤1; lexicographic tie-break on (q*,qdot*,qddot*,u*). This defines a deterministic adapter without adding a learned decoder. Use 33 equally spaced q initializations over the allowed interval with the other three free coordinates initialized to zero; run bounded SLSQP for at most 200 iterations per start with objective tolerance 10^-8, select the lowest feasible objective and apply the stated tie-break within 10^-8. Freeze the numerical-library version in the manifest; report projection residual and solver failures. If all starts fail, apply the previous valid target (the stationary reset target initially) and count an adapter failure. Do not supply contact force or true equilibrium torque to the target constructor. A nonconforming/missing 13-field manifest causes SCHEMA_INCOMPATIBLE before training; inventing a new order is not allowed.

Baseline/01 calls its three interfaces mathematically equivalent, but that is not established: B∘Pκ need not be onto the latent sphere and weighted blending need not recover arbitrary commands. Here C means **raw torque**, as requested by B04, not baseline/01's third, blending interface. This experiment directly tests these different admissible action sets.

### 2.2 Information, timing, learning and parameter controls

All arms receive exactly `O=(x137,1,x137,2,h,hdot,d16)` of dimension 292. The rail coordinates are common proprioceptive encoders; for fixed-base trials they are constants. d16 is the task descriptor: three task one-hot entries; sine/cosine of reference phase; current q* (2) and qdot* (2); current h*,hdot*; q*(t+0.1) (2); h*(t+0.1); remaining episode time; and reference frequency. Reference lookahead is an exogenous task command, not future reaction information. No mode receives payload identity, contact flag/force, solver state, estimated true mass, or future coupling torque. The exact same x values and preprocessing are delivered to C. Local actors see only their own x137 and z16; B sees only the local desired g13. The upper critic uses the same O as the upper policy.

All upper decisions and local actors run once per 20 ms; torques are held for the interval. Physics runs at 0.25 ms, encoders at 5 ms; x137 is sampled according to its frozen 20 ms/slow-summary manifest. Five 5 ms velocity samples span 20 ms, not 40 ms: the contradictory prose in baseline/01 does not override its filter formula. For all arms, fill buffers with 0.32 s of recorded stationary proprioception at the reset pose with zero motor action and a temporary reset fixture locking the joints and rail. Remove the fixture at t=0; it supplies no task-time stabilization and its forces never enter deployed observations. Set all initial velocities to zero, expose no future samples, and start the first valid task interval at release.

Primary learning uses PPO, separate policy/value MLPs, tanh hidden units, two 256-unit hidden layers, Gaussian raw upper actions followed by the arm's deterministic adapter. Each policy has exactly **140,000 trainable scalar parameters including its learned diagonal log standard deviations**. Obtain equality by a fixed binary mask on the second hidden weight matrix, pruning exactly `dense_policy_parameter_count-140000` entries by increasing SHA256(row,column,"B04-mask-v1"), preserving diagonal entries and at least one connection per row/column. The dense policy counts for A/B/C are 149,056/147,508/141,316, so the respective masks remove 9,056/7,508/1,316 weights. All remaining parameters participate in computation; no dead padding parameters. Output widths are 32,26,2. Freeze and publish the masks before training. The same unmasked value network is used in every arm. Report total and trainable counts, adapter cost and inference latency. For C add a separately labeled **total-deployment-budget** control with 421,617 trainable policy parameters via a wider masked MLP (292→544→544→2), counting the shared local checkpoint once in A/B. Also report the physical two-copy footprint 563,234 if weight sharing is disabled. This prevents an upper-parameter comparison from hiding the local prior's capacity advantage.

Use 2,048 transitions per collection batch, 10 PPO epochs, minibatch 256, Adam 3e-4, γ=0.99, GAE λ=0.95, clip=0.2, value coefficient 0.5, entropy coefficient 0.001 per action dimension (average entropy), gradient norm cap 0.5, initial log standard deviation -0.5, orthogonal weight initialization (hidden gain sqrt(2), policy head 0.01, value head 1), zero biases, no optimizer schedule. Freeze common observation scaling; use angles in radians, rail height in metres, velocities in units of 4 rad/s and 1 m/s, time divided by 10, and frequency divided by 2. x uses the checkpoint's scaler. Rewards are not normalized; advantages are normalized within each batch. Every arm receives identical physics-transition and optimizer-step budgets, reset distributions, reward functions and seeds. Exploration dimensionality is an inherent interface difference and must be reported; a sensitivity arm tunes initial exploration on separate development seeds to match initial torque variance, with the same three-trial tuning allowance for each arm.

Primary sample efficiency counts downstream transitions. Also report the local pretraining physics cost once, total compute, and an amortization curve versus number of downstream morphologies. A secondary raw-policy pretraining control gets the same local-trajectory dataset and compute cap; its behavior-cloning procedure is frozen on development seeds. It is not required to share the modular architecture. Claims must distinguish reusable-prior benefit from total-training-cost benefit. No privileged information or online local fine-tuning enters any confirmatory arm.

## 3. Standardized 2-DoF Transfer Benchmark Specification

### 3.1 Canonical physical instance and numerical contract

Nominal values: L1=L2=0.40 m; m1=1.00 kg; m2=0.70 kg; ci=Li/2; Ii=miLi²/12; mb=2.00 kg; mp=0 unless a task specifies otherwise; C01=C02=9 N m; g=9.81 m/s². Joint friction is `0.03 qdot+0.02 tanh(qdot/0.01)` N m. Stops are q1∈[-2.8,0.5], q2∈[0.05,2.8]. Outside the interval use restoring stiffness 400 N m/rad and damping 4 N m s/rad, with damping only while moving farther into violation. No imposed joint velocity clamp, actuator delay, torque slew limiter, or artificial gravity compensation is used.

The rail is unbounded except for termination at h<0.20 or h>1.50 m. Only the foot point collides; the links have no collision shapes. For foot penetration δ=-yf>0,

    Fn=max(0,20000 δ-100 vydot),
    Ft=-0.8 Fn tanh(vxdot/0.01).

Otherwise both forces are zero. This is compliant dissipative contact, without a separate restitution impulse or force clip. The floor is y=0. Point-foot normal/tangential velocities use the full `(h,q)` Jacobian. E1 stops and E2 ground contact are logged independently. Use float64 semi-implicit Euler: evaluate forces at the beginning of each 0.25 ms step, solve the coupled mass matrix for acceleration, update velocity then position. Record simulator/code/dependency hashes and contact parameters in the run manifest. Re-run numerical validation at 0.125 ms; a >5% change in contact impulse or task success is NUMERICS_UNRESOLVED and blocks confirmatory contact conclusions.

Define a centered stance with desired foot (0,0) by inverse kinematics for a prescribed hip height Ht:

    q2*=acos((Ht²-L1²-L2²)/(2L1L2)),
    q1*=-π/2-atan2(L2 sin q2*,L1+L2 cos q2*).

This selects the same bent-knee branch across morphologies. Derivatives of this known trajectory give qdot*. For stance initialization choose H0=0.60 m, pose q*(H0), h=H0-δ0 and zero velocities, with δ0=(mb+m1+m2+mp)g/20000. This is an initial geometric compression, not a hidden controller. The first motor action is learned. No reference policy stabilizes a reset.

### 3.2 Three task families

Each episode lasts 10 s/500 control steps. Failures terminate early and contribute zero success, with maximum loss imputed for the remaining steps when computing episode scores; no survivor-only averaging. Training resets use the specified bounded variations; fixed evaluation episode seeds reproduce them exactly.

1. **Free-space tracking (fixed hip).** Set h=1.20, mp=0 and disable ground contact. Let qbar=(-2.05,1.00), q1*=qbar1+0.25 sin(2πft+φ), q2*=qbar2+0.30 sin(2πft+φ+π/2). At reset draw f uniformly from {0.25,0.50,1.00} Hz and φ uniformly on [0,2π), set q=q*(0), qdot=0. Success requires full-episode pooled joint RMSE≤0.10 rad, 95th-percentile absolute joint error≤0.20 rad, no termination, and saturation on <10% of joint-time samples. Report tracking separately for each frequency. Evaluation additionally tests f=1.50 Hz as a declared high-coupling stress tier.

2. **Payload squat/hold (passive rail).** Draw attached foot payload mp uniformly from {0,0.10,0.20} kg at reset; its mass is constant throughout the episode. From H0=0.60 descend to 0.45 over t∈[1,3] using quintic smoothstep `s(v)=10v³-15v⁴+6v⁵`, hold during [3,6], rise over [6,8], then hold to 10. References use Ht and the IK above. This foot payload changes distal inertia; it is not mislabeled as a torso load. Success requires joint RMSE≤0.10 rad during movement, height RMSE≤0.02 m overall, and during both static windows [4,6] and [9,10]: velocity RMSE≤0.35 rad/s, mean absolute joint error≤0.05 rad, contact present ≥95% of samples, and foot |x|≤0.05 m. Report net demand and saturation in these windows; require no termination. A torso payload is an optional separate experiment, not pooled into this one.

3. **Ground-impact hop/landing (passive rail).** Use mp=0. During [0,1] squat from 0.60 to 0.50; during [1,1.25] extend toward 0.70 with quintic interpolation; after 1.25 keep a tucked relative-pose target q*(0.55). The exogenous height target is 0.75 during [1.25,2.0], transitions to 0.55 during [2.0,2.5], and remains there. After 2.0 use q*(0.55) throughout. One hop per episode; no state-triggered reference changes and no event flag to the policy. Success requires a flight interval of ≥0.10 s (Fn<1 N at physics samples), upward hip velocity at flight onset, apex h≥0.72 m, recontact before 3.0 s, and a final quiet hold [4,10] with h RMSE≤0.03 m, joint velocity RMSE≤0.35 rad/s, |xfoot|≤0.05 m and contact ≥95%. Peak Fn must be ≤6 mt g, penetration ≤0.02 m, and no termination. Separate landing-only diagnostic episodes reset h=0.85 with pose q*(0.55), zero velocity, and constant h*=0.55; these are not mixed with hop success or its training reward.

All tasks terminate at a stroke excursion >0.10 rad, |qdotj|>30 rad/s, rail boundary violation, penetration >0.05 m, nonfinite state, or failed linear solve. The latter two are simulator failures and are reported separately from controller failures. Train/evaluate each task with a separate upper policy; no unreported curriculum.

Per-step reward is `exp(-E)-0.002 mean(u²)-0.002 mean((u-ut-1)²)-0.05 mean(1[|u|>0.98])`, with termination penalty -10. Let `Eq=mean(((q-q*)/0.10)²)` and `Ev=mean(((qdot-qdot*)/0.35)²)`. Tracking uses E=Eq+0.1Ev. Squat uses E=Eq+0.1Ev+((h-h*)/0.03)²+(xfoot/0.05)². Hop uses E=0.2Eq+((h-h*)/0.05)², adding 0.1Ev after t=4. These rewards are identical across interfaces. Physical success predicates, rather than reward magnitude, determine the primary result. An inverse-dynamics trajectory feasibility audit precedes controller training; impossible reference demands are reported, not silently repaired after seeing arm scores.

### 3.3 Morphology transfer and audit output

Train upper policies on nominal L2,C0 only. Zero-shot tests use the full 3×3 grid L2∈{0.32,0.40,0.48} and knee C02∈{6.75,9.00,11.25}, including paired changes. C01 remains 9. On length changes hold m2 fixed and recompute c2,I2 as a uniform rod; this isolates geometric/inertial change from extra mass. Foot payload location follows the new L2. Recompute reference IK for the same world-height task, update genuine calibration constants through existing local preprocessing, and freeze all learned quantities. No new normalizer fitting, latent search on test episodes, local adaptation, or checkpoint selection is allowed. Report every cell, including nominal, and mark whether the swapped geometry/capacity was present in local pretraining. “Unseen by the upper policy” is not automatically “unseen by the local module.” A separate both-unseen panel requires a checkpoint whose original training split excluded those geometries.

Report zero-shot success retention (swapped minus nominal success), absolute RMSE, force/impulse, saturation, supported-window fraction and per-joint coupling distributions. Fine-tuning, if run, trains **only** the upper policy for exactly 102,400 additional transitions per cell and uses new adaptation seeds; evaluate at 0,25,600,51,200 and 102,400. Keep this secondary to zero-shot results.

Closing Issue #9 has two levels. This proposal supplies the canonical physics, task, interface, metric and falsification specification. Engineering closure additionally requires a versioned executable environment, reset replay tests, numeric residual checks, frozen checkpoint hashes, the full task×mode×seed×morphology result table and a machine-readable verdict. A specification or CPU surrogate alone must not mark empirical transfer validated.

## 4. Serious Alternative Considered and Rejected

A credible alternative is a centralized computed-torque/MPC layer that estimates M,c,G and contact, cancels cross-joint dynamics, and presents nearly isolated plants to local actors. It can exploit the exact model above and may outperform all three learning arms with less data. It is rejected as the primary composition test because the cancellation itself supplies the missing load model; success would no longer isolate reuse of the frozen proprioceptive local representation. Oracle contact compensation would also violate the equal-information control. An optional model-based positive control may use the known benchmark model and true state, clearly labeled privileged, solely to assess task feasibility. It cannot count as evidence for H4.

Likewise, fine-tuning local actors on the serial chain would be a useful engineering extension but answers a different question and is excluded here. If moving-parent loads prove unsupported, the legitimate next step is to collect a separately versioned single-unit training distribution with moving housings, retrain upstream, freeze a new checkpoint, and repeat the preregistered comparison. It is not permissible to repair the local module between downstream test cells and call that zero-shot reuse.

## 5. Candidate Necessity Claims

### C-B04-Q-01 — Same-input incompatible-action obstruction

**Status:** Candidate; Grade-1 conditional algebraic claim, not a claim that all coupling is unobservable or that x137 must be enlarged.

**Premises.** Consider two admissible downstream states with identical *entire available causal information* to the composed deterministic policy, including both local histories, common rail sensors, task descriptor, recurrent state if any, and calibration. Thus they induce the same z and the same applied action u at a selected joint. Over the next step, take equal positive scalar effective inertia J and identical other terms, but hidden net load torques ℓa and ℓb. Let the desired angular acceleration be the same in both states. Assume both required actions are individually within the actuator range and the local linear acceleration relation is exact for this comparison.

**Statement.** If |ℓa-ℓb|>2Jε, no such controller can guarantee acceleration error ≤ε in both states. Under equal prior probability, its expected squared acceleration error is at least `(ℓa-ℓb)²/(4J²)`.

**Proof.** The two resulting accelerations under the same action differ by `(ℓa-ℓb)/J`. Two intervals of radius ε about the same target cannot contain both when their separation exceeds 2ε. For squared error the optimum common prediction is the midpoint; the residual variance is the stated bound. More generally let Uε(s) be the set of actions achieving the task tolerance in state s. A common-input robust controller requires `intersection_s Uε(s)` to be nonempty. No independent-load envelope can overcome an empty intersection.

**Scope/counterexample.** Neighbor histories can make upper inputs distinguishable, allowing z to carry advance coordination information even though the local actor lacks direct neighbor sensors. A local-only alias therefore does not establish this result for the whole architecture. Raw baseline C has the same information obstruction. The argument requires neither new force sensors nor a particular representation; sensing, a richer causal history, conservative task tolerances, or coordination can avoid its premises. State-independent low-amplitude coupling is a counterexample to any unconditional “parent-motion sensing is necessary” claim.

**Test and falsifier.** In §6 construct matched observable reset histories with a hidden payload or contact variation and individually feasible but disjoint action tolerance sets. A controller producing distinct first actions with byte-identical full inputs indicates leakage/nondeterminism and invalidates the test. Once inputs become distinguishable, successful recovery is allowed. The claim would be inapplicable if action sets overlap or the equal-J premise fails; use the general set-intersection version rather than forcing the scalar bound.

### C-B04-Q-02 — Joint support is necessary for a distribution-free transfer certificate

**Status:** Candidate; narrowly scoped logical claim. Identical marginal distributions of hip load and knee load permit different joint laws (for example equal-sign versus opposite-sign load pairs), hence neither per-joint E0–E4 quota counts nor marginal peak bounds determine the serial-chain transition law. A claim of guaranteed performance for every compatible joint law therefore needs additional restrictions on coupling/conditional response, or a robustness argument covering all such laws. It does **not** follow that measured joint support is necessary for every successful controller: a sufficiently robust policy can succeed outside its data support. The empirical support test here is a qualification of evidence, not a theorem equating OOD with failure.

The transfer gain itself remains a Grade-2 empirical hypothesis: under feasible, empirically supported loads, A or B reaches a common success threshold with at least 20% fewer downstream samples than C and retains performance after calibrated morphology swaps. Neither this hypothesis nor a universal stability guarantee is elevated to a necessity claim.

## 6. Pre-Registered Empirical Spike Protocol

### 6.1 Stage 0: freeze and qualify before downstream scores

Seal source revision, environment manifest, observation/outcome slot manifests, parameter masks, all seeds, contact law, criteria and one local checkpoint before collecting confirmatory results. The checkpoint must have a real-physics 144×5 qualification artifact, both load signs, B02 load/recovery windows and static-hold guards, zero-velocity RMSE<0.35 rad/s in its prescribed panel, and B01 deployment purity. B03 preprocessing must match the export schema; its rank-floor hypothesis remains conditional. A surrogate or `coverage_ready` boolean without qualifying real rollouts is insufficient. If no eligible checkpoint exists, execute mechanics/interface diagnostics only and report `BLOCKED_LOCAL_QUALIFICATION`; do not substitute the smoke checkpoint into a scientific H4 verdict.

### 6.2 Stage 1: mechanics, causality and coverage spike

Use float64 analytic and numerical checks at 1,000 seeded states with q in the inner 80% of the stroke, |qdot|≤4, random u, mp∈{0,0.2}, and fixed/rail bases. Seeds are 41000–41999. Verify M symmetry and positive definiteness; independently finite-difference T,V to check Euler–Lagrange terms; solve forward dynamics and require relative local/global EOM residual≤10^-9; compare Schur elimination to the full solve; and verify `qdotᵀJᵀF=(Jqdot)ᵀF`, adding hdot Fn for the rail, within 10^-10 relative tolerance (denominator at least 1). Finite-difference checks use tolerance 10^-5. Check contact is unilateral/dissipative and the integrated dynamics converges under halved timestep. Test zero payload, qdot=0, no contact, q2≈0, gravity-free flight, and nonzero base acceleration explicitly.

Run a **mechanism spike**, not convergence training: 32 reset seeds per task, 10 s each, with an analytic reference tracker and the frozen A/B/C interfaces driven by fixed scripted commands. Scripts are for coverage acquisition and wiring checks; they do not determine H4 success. Sweep fixed-base tracking frequency {0.25,0.5,1,1.5}, mp={0,0.2}, and landing height {0.75,0.85,0.95}. Preserve all failures, unfeasible trials and missed event windows. Log substep dynamics and interval-aligned x,g,z,u, action-latch timestamps, component torque and contact impulse. Verify no current-interval solver reaction reaches an action already latched, in accordance with B01. F and p5065 are absent from deployed inference; audit forward argument shapes and randomize inaccessible simulator fields to test output invariance.

Construct the envelope from upstream real rollouts, not these downstream probes. Joint-bin matching uses 5 equal-width bins over each training 0.5–99.5 percentile interval for calibrated q, qdot, r and Mjj/J0, plus sign and regime; dwell/impulse must also lie within the training interval. Require ≥20 independent source episodes in each matched bin. Report coverage fraction, unknown fraction, and confidence bounds; no dropping empty cells. For bins with adequate support, compare standardized next-step `(qdot,qddot,u)` conditional means and covariance against source holdouts; require each mean discrepancy≤0.25 source standard deviations and covariance Frobenius discrepancy≤25% of source covariance norm (floor 10^-6). Match z as well using cosine similarity≥0.95 and at least 20 episodes, or mark response support UNKNOWN. These stringent checks may fail; they are a falsifiable qualification rather than permission to inflate an envelope. No finite empirical check proves equality of transition laws.

An operational supported-load panel requires ≥95% of each joint's windows supported and no unclassified high-impulse event; keep all other episodes in the overall result and separate them in attribution. Construct the same-input action-set test from C-B04-Q-01 with two simulator branches, recording first-action equality and feasible action intervals. Joint-load correlation, neighbor-action sensitivity and reaction delay are diagnostic quantities, never fed to local modules.

### 6.3 Stage 2: bounded downstream learning comparison

Train A,B,C and total-budget C on each task for **2,048,000 transitions** each: 1,000 collection iterations and 80,000 optimizer minibatch steps, since each iteration has 10×8 minibatches. Use ten paired training seeds 100–109; simulator episodes are keyed independently by `(task,seed,episode_index)` so differing failure lengths do not shift future scenario draws. Evaluate every 102,400 training transitions, including zero, on 100 fixed task episodes keyed 20000–20099. These evaluations do not enter training. Final transfer tests use 100 fresh episodes per morphology cell keyed 30000–30099; landing-only diagnostics use 40000–40099. Development/tuning seeds are 1–3 and never join confirmatory confidence intervals.

Primary endpoint: restricted sample-to-threshold T80, the first evaluation with ≥80% episode success maintained for the next two evaluations; last two evaluation points cannot newly qualify. If never achieved, assign the horizon 2,048,000 and mark right-censored. Publish both restricted means and a survival curve; never discard unsuccessful seeds. Secondary endpoints are success-curve AUC divided by the horizon, final success, task-specific RMSE, return, energy `∫|τ qdot|dt`, impulse, saturation and failure reasons. Count environment steps rather than wall-clock simulator parallelism; also report wall time and inference cost.

Primary contrasts A−C and B−C use paired seeds. Bootstrap 10,000 times over training seeds, retaining all episodes/cells within a seed; use 97.5% intervals for the two primary contrasts. Do not treat episode-level samples as independent trained controllers. A transfer-gain PASS for an arm requires: upper confidence bound on restricted-mean T80 ratio≤0.80; lower bound on equal-weight mean nominal final success≥0.80; and lower bound on mean zero-shot success difference (swapped minus nominal)≥-0.10. Report every task and cell, and require no individual task's nominal success mean<0.70. Pooled performance cannot conceal a failed task. Repeat these comparisons to the total-budget C as a capacity sensitivity analysis; a reversal narrows the claim to equal upper learning budgets. Report both-unseen morphology results separately when available.

A supported, physically feasible panel in which both modular arms have an interval excluding the stipulated 20% gain rejects the **specified effect-size version** of H4; it does not prove no smaller benefit exists. If all arms fail, the checkpoint is unqualified, numeric checks fail, or support is unknown, the result is INCONCLUSIVE with the corresponding reason. An OOD failure falsifies unrestricted reuse for that panel but not the charter's conditional inside-distribution hypothesis. Conversely, a PASS supports this finite benchmark and checkpoint only, not arbitrary multi-joint stability or bipedal locomotion.

### 6.4 Required artifacts and stopping rules

The eventual runner must emit `manifest.json`, checkpoint/preprocessing hashes, `physics_checks.json`, `qualification_144x5.json`, `envelope_reference.json`, episode-level parquet/CSV, `learning_curves.csv`, `transfer_grid.csv`, action-set alias test records, and `VERDICT.json`. Verdict fields distinguish `mechanics`, `interface_purity`, `local_qualification`, `support`, `numerics`, `sample_efficiency`, and `zero_shot_transfer`; each contains PASS/FAIL/UNKNOWN/BLOCKED and evidence paths. Record all hardware, software, run time, aborted runs and requested versus completed budgets. Do not fabricate empty result files or mark this proposal as an executed spike.

Stop only for declared numerical invalidity, unavailable qualifying checkpoint, or budget completion; preserve artifacts and failure reasons. Repairing a bug requires a new manifest and rerunning affected paired arms. Thresholds, checkpoint selection and task definitions cannot be changed after viewing confirmatory arm differences. This protocol keeps every local (B,π) frozen and makes Audit Issue #9 actionable without mistaking a scheduler surrogate, dynamics identity, or amplitude-overlap plot for demonstrated modular transfer.
