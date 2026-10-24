# Candidate Q (Packet B04): Composing Frozen Local Motor-Unit Representations into Multi-Joint Limb Controllers Under Coupled Loads

- **Packet**: `B04` · **Author track**: Primary Author A · **Method Version**: v1.0 (`1ce8d1b3…11f7`)
- **Inherited ledger**: `X-BASE-001..005`; decisions `D-B01-001`, `D-B02-001`, `D-B03-001`
- **Frozen inputs read**: `PROGRAM_CHARTER.md`, `packets/B04/brief.md`, `baseline/01` (§2–§4), `baseline/02` (read only for §2.1 `g13` / §2.2 `x137` / §4 configuration ranges; it is cited where used), `baseline/03` (Issue #9), `B01/B02/B03 decision.md`.
- **Author-side calculation artefacts** (not the official spike; they back the numbers quoted in §1 and the gates in §6): `drafts/A/coupling_envelope.py` → `coupling_envelope.out.json`, `drafts/A/inertia_ratio.py` → `inertia_ratio.out.json` (numpy only, CPU, under 1 s).

## 0. Summary of the Position

1. **Reduction (§1).** For a hip–knee limb on a passive vertical rail, the effective external torque that each frozen unit "sees" in its own local EOM (`baseline/01` §3.1) splits into three classes that differ structurally: **(X) exogenous-to-unit** terms driven by the other joint or the base; **(S) self-correlated** terms proportional to the unit's own $\ddot q_j$ or $\dot q_j$, which act as a plant-parameter change and are not a disturbance; **(K) constraint** terms from the foot contact, including a closed-chain internal-force mode. Only class X has the same structure as the E3/E4 generators, which are open-loop in the exogenous state $\xi_t$ after the B01 causal partition. For the knee, a *housing-transport identity* (C-B04-Q-02) collapses all parent motion into two quantities: an effective gravity $g^{\mathrm{eff}} = \vec g - a_K$ at the knee point, and the housing angular acceleration $\dot\omega_P$. As a result, base heave acts on a unit exactly like a change in gravity, takeoff acts like an E4 release edge, and touchdown acts like an impulse plus an E3 load onset.
2. **Envelope verdict (reference leg, §1.5).** Free-space tracking coupling stays at or below $0.29\,S_{\max}$ up to 3 Hz, inside the E3 amplitude. The bandwidth condition binds before the amplitude condition does. The knee demand in a payload squat crosses the E3 ceiling $|u^\star| = 0.92$ between 2 and 3 kg of payload. Landing contact torque averaged over 20 ms is $1.06$–$1.39\,S_{\max}$ even for drops of 5–15 cm. That is outside E3, and it is inside E4 only if the manifest's impulse bound is at least that large. In stance, the knee's reflected inertia is $1.6$–$19\times$ its free-swing value.
3. **Amplitude coverage is not enough (C-B04-Q-01).** Charter H4's proviso ("coupling forces represented inside E2/E3") cannot be certified by amplitude alone. Class S changes the loop gain, and class K adds a neutral or ramping internal-force mode (C-B04-Q-03) that no passive single-unit scene contains. The coverage certificate has four parts: amplitude, bandwidth, inertia ratio, and constraint mode.
4. **Benchmark (§3).** `LIMB2-v1` closes Audit Issue #9. It has 3 tasks × nominal plus transfer cells, 7 arms (A, B, C plus 4 controls), a fixed fairness contract (identical 282-D observation, 50 Hz, equal trainable parameters within 1%, equal environment steps and HP-search budget), and pre-registered predictions per cell, each conditioned on that cell's envelope class.

---

## 1. Multi-Body Coupling Dynamics Reduction

### 1.1 Plant and coordinates

The plant is a planar serial limb in the sagittal plane. The base (pelvis) of mass $m_b$ (plus payload $m_p$) slides on a passive frictionless vertical rail with height $y$, and its attitude is locked. This is the canonical minimal hopper: it gives real stance and flight phases without a floating-base attitude DoF, so the 2-DoF actuated structure stays clean.

- Hip $j=1$: housing $P_1$ = base, driven link $D_1$ = thigh (length $l_1$, mass $m_1$, COM $l_{c1}$, central inertia $I_1$, knee motor mass lumped into $m_1$). Angle $q_1$ is the absolute thigh angle measured from downward vertical.
- Knee $j=2$: housing $P_2$ = thigh = $D_1$, driven link $D_2$ = shank + foot (length $l_2$, $m_2$, $l_{c2}$, $I_2$). Angle $q_2$ is relative.
- Geared drives (ratio $n$, rotor inertia $J_r$). The hip rotor sits on the base (absolute rotor angle $n q_1$). The knee rotor sits on the thigh (absolute rotor angle $q_1 + n q_2$). This matches B02's $J_{\mathrm{nom}} = I_{D,zz} + n_g^2 J_{\mathrm{rotor}}$.
- Generalized coordinates $Q = (y, q_1, q_2)$. Actuation $B\tau = (0, S_1 u_1, S_2 u_2)$ with $S_j = S_{\max,j} = 1.25\,C_{0,j}$.
- Foot point $f = \bigl(l_1 s_1 + l_2 s_{12},\; y - l_1 c_1 - l_2 c_{12}\bigr)$ with $s_1=\sin q_1$, $s_{12}=\sin(q_1+q_2)$, and similarly for $c$. Contact force $\lambda = (\lambda_x, \lambda_z)$ is unilateral, $\lambda_z \ge 0$, $|\lambda_x| \le \mu\lambda_z$. Foot Jacobian:
$$
J_c(Q) = \begin{bmatrix} 0 & l_1 c_1 + l_2 c_{12} & l_2 c_{12} \\ 1 & l_1 s_1 + l_2 s_{12} & l_2 s_{12}\end{bmatrix}.
$$

### 1.2 Exact Euler–Lagrange equations

$M(Q)\ddot Q + C(Q,\dot Q) + G(Q) = B\tau + J_c^\top\lambda$. Write $a \equiv m_1 l_{c1} + m_2 l_1$ and $h \equiv m_2 l_1 l_{c2}\sin q_2$:

$$
M = \begin{bmatrix}
m_b{+}m_p{+}m_1{+}m_2 & a s_1 + m_2 l_{c2} s_{12} & m_2 l_{c2} s_{12}\\
\cdot & I_1{+}m_1 l_{c1}^2{+}I_2{+}m_2(l_1^2{+}l_{c2}^2{+}2 l_1 l_{c2}\cos q_2){+}(n^2{+}1)J_r & I_2{+}m_2(l_{c2}^2{+}l_1 l_{c2}\cos q_2){+}n J_r\\
\cdot & \cdot & I_2{+}m_2 l_{c2}^2{+}n^2 J_r
\end{bmatrix},
$$
$$
C = \begin{bmatrix} a c_1\dot q_1^2 + m_2 l_{c2} c_{12}(\dot q_1{+}\dot q_2)^2 \\ -h\,(2\dot q_1\dot q_2 + \dot q_2^2) \\ h\,\dot q_1^2\end{bmatrix},\qquad
G = \begin{bmatrix} (m_b{+}m_p{+}m_1{+}m_2)\,g \\ g\,(a s_1 + m_2 l_{c2} s_{12}) \\ g\, m_2 l_{c2} s_{12}\end{bmatrix}.
$$
The $\dot y\dot q$ cross terms cancel exactly ($\partial M_{y1}/\partial q_2 = \partial M_{y2}/\partial q_1 = m_2 l_{c2}c_{12}$), so no velocity product involves $\dot y$. Friction $b_j\dot q_j + \tau_{\mathrm{fric},j}$ is per joint and identical in the chain and in single-unit training, so it is omitted below.

### 1.3 Mapping into the local unit EOM

Each frozen unit $j$ was trained against the local EOM (`baseline/01` §3.1):
$$
J^{\mathrm{tr}}_j\,\ddot q_j + b_j\dot q_j + \tau_{\mathrm{fric},j} + \tau^{\mathrm{tr}}_{\mathrm{grav},j}(q_j) - \tau_{\mathrm{ext},j} = S_j u_j ,
$$
where $J^{\mathrm{tr}}_j$ is the configuration's nominal inertia and $\tau^{\mathrm{tr}}_{\mathrm{grav},j}$ is the gravity profile of its fixed housing. Row $j$ of the chain EOM is rewritten in exactly this form by defining the **effective external torque**
$$
\boxed{\tau^{(j)}_{\mathrm{ext,eff}} = \underbrace{-\textstyle\sum_{k\ne j} M_{jk}\ddot Q_k}_{\tau^{(j)}_{\mathrm{inertial}}}\;\underbrace{-\,(M_{jj}(Q)-J^{\mathrm{tr}}_j)\,\ddot q_j}_{\tau^{(j)}_{\mathrm{self}}}\;\underbrace{-\,C_j}_{\tau^{(j)}_{\mathrm{Coriolis}}}\;\underbrace{-\,(G_j(Q)-\tau^{\mathrm{tr}}_{\mathrm{grav},j}(q_j))}_{\tau^{(j)}_{\mathrm{grav}}}\;+\;\underbrace{(J_c^\top\lambda)_j}_{\tau^{(j)}_{\mathrm{contact}}}}
$$
This is an identity, not an approximation. It was checked on 2000 random $(Q,\dot Q,\ddot Q,\lambda,J^{\mathrm{tr}},\tau^{\mathrm{tr}}_{\mathrm{grav}})$ draws with maximum residual $7.1\times10^{-15}$ N·m (`coupling_envelope.out.json: identity_residual_max`). The brief's four torques are the four labelled terms. The proposal adds a fifth, $\tau_{\mathrm{self}}$, because it behaves differently from the others (§1.4).

**Knee ($j=2$), explicit form.**
$$
\tau^{(2)}_{\mathrm{ext,eff}} = -\bigl[I_2 + m_2(l_{c2}^2 + l_1 l_{c2}\cos q_2) + nJ_r\bigr]\ddot q_1 \;-\; m_2 l_1 l_{c2}\sin q_2\,\dot q_1^2 \;-\; m_2 l_{c2}\,s_{12}\,(g+\ddot y) + \tau^{\mathrm{tr}}_{\mathrm{grav},2}(q_2) + l_2\,(c_{12}\lambda_x + s_{12}\lambda_z),
$$
with $\tau_{\mathrm{self}}^{(2)} \equiv 0$ whenever $J^{\mathrm{tr}}_2 = M_{22}$. That holds because $M_{22}$ is configuration-independent, so in free swing the knee unit's inertia is exactly a single-unit inertia.

**Hip ($j=1$), explicit form.**
$$
\tau^{(1)}_{\mathrm{ext,eff}} = -M_{12}(q_2)\ddot q_2 - (M_{11}(q_2) - J^{\mathrm{tr}}_1)\ddot q_1 + h(2\dot q_1\dot q_2 + \dot q_2^2) - (a s_1 + m_2 l_{c2}s_{12})(g+\ddot y) + \tau^{\mathrm{tr}}_{\mathrm{grav},1}(q_1) + (l_1c_1{+}l_2c_{12})\lambda_x + (l_1s_1{+}l_2s_{12})\lambda_z .
$$
**Descriptor assignment (pre-registered, `D-ASSIGN-1`).** The hip unit's static descriptor in `x137` is set to the thigh alone ($L_D = l_1$, $r_{\mathrm{com},D}$ = thigh COM). The shank is therefore entirely a distal load. With this choice $J^{\mathrm{tr}}_1 \equiv M_{11}(q_2^{\mathrm{nom}})$ at $q_2^{\mathrm{nom}} = 1.0$ rad. `D-ASSIGN-2` (lumped rigid thigh+shank at $q_2^{\mathrm{nom}}$) is a registered secondary ablation only.

### 1.4 Structural lemmas (see §5 for claims)

**(L1) Base heave is gravity modulation.** In both rows, $\ddot y$ appears only in the combination $(g+\ddot y)$. Proof: $M_{jy} = \partial(\text{COM heights})/\partial q_j \cdot m = G_j/g$. A unit therefore cannot distinguish base vertical acceleration from a change in gravity magnitude. Consequences:
- In flight, $\ddot y \approx -g$, so the gravity torque on both units nearly vanishes. **Takeoff is a gravity-bias release edge** of magnitude $|G_j(Q)|/S_j$. Structurally this is E4 (a step release of a load the unit had been holding).
- **Touchdown is an impulsive onset** of $(g+\ddot y)$ several times $g$ together with $\tau_{\mathrm{contact}}$. Structurally this is E2 (knee: contact at its own tip, since the foot is the shank tip) plus E3 onset. For the hip it has *no E2 analogue*: the contact point is not on $D_1$. That makes it a pure distal-load event, comparable only to E3/E4.

**(L2) Housing-transport identity (knee).** In vector form, the knee row is exactly
$$
\tau^{(2)}_{\mathrm{ext,eff}} = -m_2\bigl[r_{c2}\times(a_K - \vec g)\bigr]_z - (I_2 + m_2 l_{c2}^2 + nJ_r)\,\dot\omega_{P_2} + \tau^{\mathrm{tr}}_{\mathrm{grav},2} + \tau^{(2)}_{\mathrm{contact}},
$$
where $a_K$ is the absolute acceleration of the knee point and $\dot\omega_{P_2} = \ddot q_1$. The bilinear Coriolis term $2\omega_P\dot q_2$ of the transport acceleration contributes zero moment about the knee because $r_{c2}\times r_{c2}=0$. Parent angular velocity enters only through the centripetal part $l_1\dot q_1^2$ of $a_K$. This explains why the knee row has no $\dot q_1\dot q_2$ term.

The identity has a practical consequence. **Everything the knee unit needs to know about the moving housing is the 2-D vector $g^{\mathrm{eff},M} = R_M^\top(\vec g - a_K)$ and the scalar $\dot\omega_P$.** In single-unit training, $\|g^{\mathrm{eff}}\| = 9.81$ with a fixed direction per stroke profile, and $\dot\omega_P = 0$. Single-unit coverage of the knee in a chain is therefore exactly the question whether E3/E4 torque schedules span the torque signals generated by the excursions of $(\|g^{\mathrm{eff}}\|, \angle g^{\mathrm{eff}}, \dot\omega_P)$. This defines the minimal statistics to log (§3.5). It is also the justification for the rejected alternative in §4.

**(L3) Three structural classes.**

| Term (unit $j$) | Class | Depends on own action $a_{j,t}$ through | E-regime analogue | Envelope coordinate |
|---|---|---|---|---|
| $-M_{jk}\ddot q_k$, $-M_{jy}\ddot y$ | X (exogenous-to-$j$) | other unit / base only (one-step causal) | E3 bias/ramp/sinusoid; E4 edges | amplitude, spectrum |
| $C_j$ terms in $\dot q_k$ only ($h\dot q_1^2$ for knee) | X | other unit only | E3 | amplitude, spectrum |
| $C_j$ terms in $\dot q_j$ (hip: $h\dot q_2^2$ is X, $2h\dot q_1\dot q_2$ is S) | S (self-correlated) | own velocity | none: parameter change | velocity-gain ratio |
| $-(M_{jj}(Q)-J^{\mathrm{tr}}_j)\ddot q_j$ | S | own acceleration | none: inertia change | inertia ratio $\rho_j = M_{jj}/J^{\mathrm{tr}}_j$ |
| $-(G_j - \tau^{\mathrm{tr}}_{\mathrm{grav},j})$ | X (from $q_k$, $\ddot y$) / quasi-static | weakly via $q_j$ | E3 (gravity re-phasing / magnitude) | amplitude, slew |
| $(J_c^\top\lambda)_j$ in stance | K (constraint) | jointly with other unit | E2 (knee only, tip contact); none for internal force | amplitude, impulse, null-mode |

B01 adopted an open-loop envelope $\Psi_t = \psi(\xi_t,k)$ for the E3/E4 generators. Their torque is therefore conditionally independent of the unit's own action given $\xi_t$. Class S and class K violate this by construction, so no amplitude setting of the E3 generator reproduces them. This is the core of C-B04-Q-01.

**(L4) Closed-chain stance null mode.** With the foot pinned ($\dot f = 0$) and base attitude locked, the stance manifold is 1-D (coordinate $s$, tangent $\varphi = dQ/ds$). The static torque solving $G = B\tau + J_c^\top\lambda$ is non-unique along the 1-D *internal-force direction* $\nu = -(J_c^\top)_{q,x}$, which corresponds to a horizontal foot force reacted by the rail. For the reference leg at $q_2=1.2$, $\nu/S = (-0.037,\,-0.028)$ per newton: 10 N of internal force shifts hip/knee demand by $0.37/0.28\,S_{\max}$ without moving the limb. If the units hold integral-like state (explicitly, or by recursion through the $u_{\mathrm{prev}}$ channel of `x137`), the integrator combination along $\nu$ is unobservable from the motion. It is neutral under kinematically consistent targets and ramps linearly under inconsistent ones (C-B04-Q-03; verified in §1.5).

### 1.5 Quantification against E0–E4 envelopes

**Reference leg `LIMB2-REF`.** The masses and inertias are assumptions of this proposal, chosen to lie inside the B02 seed ranges; they are not values from the frozen documents. $l_1=l_2=0.25$ m ($L_D \in [0.08,0.45]$ ✓), $l_{c1}=0.6l_1$, $l_{c2}=0.5l_2$, $m_1=0.60$, $m_2=0.25$, $m_b=1.5$ kg, $I_i = m_i l_i^2/12$, $n=9$, $J_r=5\times10^{-5}$ kg·m². Capacities: hip $C_0=9$ ($S=11.25$), knee $C_0=6$ ($S=7.5$) N·m.

**E-envelope coordinates (from the frozen docs).** E3: net required command $|u^\star| \in [0.25, 0.92]$, $|\tau_{\mathrm{ext}}| \ge 0.25S$, sustained ≥25 steps (D-B02-001 §2.1). E4: step release of an E3-class load followed by a quiet recovery window. E2: passive spring-damper obstacle at the driven link inside the stroke. The E3 sinusoid/ramp bandwidth $\Omega_{E3}$, the E4 impulse bound $\hat I_{E4}$, and the E2 stiffness range $[k_{E2}^{\min}, k_{E2}^{\max}]$ are **not numerically fixed in the frozen docs**. The certificate (§1.6) reads them from the B02 `make_program` manifest and never assumes them.

All values below are $\max|\cdot|/S_{\max,j}$.

*T1 free-space tracking* (base fixed, $q_1 = 0.6\sin\omega t$, $q_2 = 1.0 + 0.5\cos\omega t$):

| $f$ | hip inertial | hip self | hip Coriolis | hip $u_{\mathrm{req}}$ | knee inertial | knee Coriolis | knee grav | knee $u_{\mathrm{req}}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 Hz | 0.005 | 0.002 | 0.003 | 0.075 | 0.008 | 0.004 | 0.020 | 0.039 |
| 1.0 Hz | 0.022 | 0.008 | 0.012 | 0.049 | 0.033 | 0.015 | 0.020 | 0.058 |
| 2.0 Hz | 0.088 | 0.030 | 0.047 | 0.374 | 0.130 | 0.059 | 0.020 | 0.202 |
| 3.0 Hz | 0.198 | 0.068 | 0.107 | **0.920** | 0.294 | 0.133 | 0.020 | 0.443 |

Inertial and Coriolis coupling both scale as $f^2$. The knee's amplitude crossover with the E3 ceiling is near 5 Hz, and the hip's total demand reaches $0.92$ at 3 Hz. **The binding constraint below 3 Hz is bandwidth, not amplitude.** A unit can compensate an exogenous torque only after estimating it from `x137`. The causal 5-point filter delay (≈10 ms) plus one control step (20 ms) gives $\tau_d \approx 30$ ms. Even an ideal disturbance observer therefore leaves an uncompensated residual fraction $r(f) = |1-e^{-i2\pi f\tau_d}| = 2\sin(\pi f\tau_d)$: **0.19 at 1 Hz, 0.56 at 3 Hz, 0.91 at 5 Hz.**

*T2 payload squat, static hold at $q_2 = 1.2$, foot under hip, $\lambda_x=0$*: hip $u = -0.06$. Knee $u$ = **0.41 / 0.60 / 0.78 / 0.97** for payload 0 / 1 / 2 / 3 kg. The 3 kg cell exceeds the E3 ceiling 0.92 and is `INFEASIBLE_CONFIG` by B02's own rule. With knee $C_0=3$ ($S=3.75$), payload 0 already requires $0.82$ (EDGE), and 1 kg requires $1.19$ (OUT). Stance reflected inertia on the knee coordinate, $\varphi^\top M\varphi$ versus free $M_{22}$, is $\rho = 1.6, 4.8, 9.4$ at $q_2 = 0.4, 1.2, 2.0$ with no payload and $2.1, 9.1, 19.0$ with 2 kg. This is class S, far outside any plausible $J^{\mathrm{tr}}$ spread for one descriptor. The hip's free-swing self-inertia ratio over $q_2\in[0.1,2.0]$ is only $M_{11}^{\max}/M_{11}^{\min} = 1.63$.

*T3 drop landing* (joint-PD stand-in, ground $k=2\times10^4$ N/m, $c=150$ N·s/m): peak $|\tau_{\mathrm{contact}}|/S$ over 20 ms windows is hip/knee **1.06/1.07** (5 cm), **1.39/1.10** (10 cm), **1.21/1.08** (15 cm). Peaks over 5 ms substep windows reach 1.21–2.73. Contact torque above $S_{\max}$ means the joint is back-driven or hits a stop. This is OUT of E3 amplitude, and it is inside E4 only if $\hat I_{E4} \ge 1.1\,S\cdot 20$ ms. Takeoff gravity release for the knee equals its stance load (0.41–0.78), which is E4-amplitude-compatible.

*Sampled-loop sensitivity to class S.* A surrogate unit is used here: a 50 Hz PD servo tuned for $J^{\mathrm{tr}}$ (2 Hz, $\zeta=0.7$) with one-step actuation delay. It is stable only for $\rho \ge 0.41$. At $\rho = 0.25$ the spectral radius is 1.25, so the loop diverges from arbitrarily small amplitude. At $\rho = 20$ the spectral radius is 0.993, which means effective damping is about $0.16$ and the 1/e time is about 2.8 s. A unit certified only near $\rho \approx 1$ thus loses its holding and tracking quality in stance even when every amplitude test passes.

### 1.6 Coverage certificate (pre-registered evaluator, eval-only privileged logging)

For each benchmark cell and joint $j$, the evaluator computes the following from the simulator's *evaluation* logs. These logs are never fed to $\Pi$, $B_\omega$ or $\pi_\theta$, which preserves Charter §2.1.

| Code | Condition | IN | EDGE | OUT |
|---|---|---|---|---|
| A-AMP | $P_{99.9}\,|u_{\mathrm{req},j}|$ and $P_{99.9}\,|\tau_{\mathrm{ext,eff}}^{X+K}|/S_j$ | ≤ 0.85 | (0.85, 0.92] | > 0.92 |
| A-BW | fraction of class-X power above $\Omega_{E3}$ (manifest) | ≤ 0.10 | (0.10, 0.30] | > 0.30 |
| A-IMP | max 20 ms-mean $|\tau_{\mathrm{contact}}|/S_j$ vs $\hat I_{E4}/(S_j\cdot 20\,\mathrm{ms})$ | ≤ 0.8× bound | ≤ 1× | > bound |
| A-RHO | $\rho_j(t) = M^{\mathrm{eff}}_{jj}(t)/J^{\mathrm{tr}}_j$ vs training hull $[\rho^{\min}_c, \rho^{\max}_c]$ from the 36-seed table for descriptor-neighbors of $c_j$ | inside | within 1.25× outside | beyond |
| A-NULL | stance internal-force drift $|\dot\lambda_x|$ (N/s, hold phases) | ≤ 1 | ≤ 5 | > 5 or any slip |

A cell is IN only if all codes are IN. $M^{\mathrm{eff}}$ is $M_{jj}$ in flight and the stance-manifold projection in stance. **Each prediction in §3/§6 is conditioned on the cell's certificate**, which makes the composition hypothesis falsifiable cell by cell instead of in aggregate.

---

## 2. Upper-Layer Calling Architecture Comparison

### 2.1 Common substrate (identical for every arm)

- Physics at 1 ms internal step, encoders sampled at 200 Hz, control boundaries at **50 Hz** (`baseline/01` §2.3). Each joint's `x137` is built by the unchanged V3 feature code, including calibration, the 5-point $\widehat{\ddot q}$, the stop margins and the static descriptor.
- **One shared frozen unit** $(B_\omega,\pi_\theta)$ (281,617 params) is instantiated at both joints and distinguished only by each joint's static descriptor. This is the strict modular-reuse test. A per-joint-specialized pair is a registered secondary only. Weights are hashed at load and re-hashed at the end of every run, and a mismatch fails the run (`FROZEN_HASH_MISMATCH`).
- **Observation** $O_{\mathrm{limb},t} = [x^{(1)}_{137,t},\, x^{(2)}_{137,t},\, c_t] \in \mathbb{R}^{282}$, where $c_t$ is an 8-D task command (§3.3). The previous applied torque is already inside each `x137` ($u_{\mathrm{prev}}$ and the fast/slow $u$ history), so no arm receives its own previous *upper* action. This keeps observation dimension identical across action spaces of different sizes. No base height, contact flag or force enters $O$.

### 2.2 Arms

| Arm | Upper output | Execution path to $u_j$ | Purpose |
|---|---|---|---|
| **A** | $\zeta^{(1)},\zeta^{(2)}\in\mathbb{R}^{16}$ | $z^{(j)} = 4\zeta^{(j)}/(\lVert\zeta^{(j)}\rVert+10^{-8})$; $u_j = \pi_\theta(x^{(j)}_{137}, z^{(j)})$ | Mode A (brief) |
| **B** | $(q^\star_j, \dot q^\star_j, \ddot q^\star_j)_{j=1,2} \in\mathbb{R}^6$ | kinematic completion $g^{\mathrm{des}}_{13} = \mathcal K_c(q^\star,\dot q^\star,\ddot q^\star; L_D)$ via `baseline/01` §2.4 (tip pos/vel/acc), then B03 $T_\kappa$ if the units were trained with it; $z = B_\omega(g^{\mathrm{des}})$; $u_j = \pi_\theta(x, z)$ | Mode B (brief) |
| **C** | $u\in[-1,1]^2$ (tanh) | direct | Baseline C (brief) |
| C-PD | $(q^\star_j,\dot q^\star_j)$ | B02 `rule_calibration` servo (inertia-scaled PID + bias + anti-windup) | Is a classical servo with the B interface enough? |
| A-rand | as A | randomly initialized, frozen $(B,\pi)$ of identical architecture | Is the gain from the learned representation or from the reparameterization? |
| C-big | as C | trainable params = $P_A$ + 281,617 | "Equal total parameters" reading of H4 |
| B-blend | $M=3$ candidate $g$ + weights | `baseline/01` §4 eq. (blend) | Mode 3, secondary only |

$\mathcal K_c$ makes $g^{\mathrm{des}}$ internally consistent, so Mode B never queries $B_\omega$ off the kinematic manifold of `g13`. Mode B's 6-D action is the *reduced* outcome. Expanding to 13 free fields would let the upper layer request kinematically impossible outcomes.

### 2.3 Fairness contract (scored dimension: 25%)

| Control | Contract |
|---|---|
| Observation and history | Identical 282-D $O$, identical normalizer (running mean/var, frozen after 20k warmup steps, same for all arms), identical 480 ms history depth, since it lives inside `x137`. |
| Control rate and latency | 50 Hz for all arms; the action computed at boundary $t$ is applied over $(t, t+1]$ for every arm; the units add no extra latency, because $\pi_\theta$ is evaluated in the same tick. |
| Trainable parameters | Actor trunk MLP with 2 hidden layers + LayerNorm + SiLU. Width $w_{\mathrm{arm}}$ is the smallest integer giving $|P_{\mathrm{arm}} - P_A|/P_A \le 1\%$ for actor and twin critics separately. Counts are logged in the manifest. Frozen unit params are reported, not counted (C-big covers the alternative reading). |
| Algorithm | SAC, UTD = 1, batch 256, replay $10^6$, $\gamma = 0.99$, Polyak 0.005. Same code path; only the action head dimension differs. |
| HP search budget | Identical 12-point grid per arm: lr $\{1,3,10\}\times10^{-4}$ × target entropy $\{-0.5d_a, -d_a\}$ × reward scale $\{1, 5\}$, each on 3 tuning seeds × 0.5M steps on nominal cells, selected by median validation AUC. Tuning seeds are disjoint from test seeds. |
| Update / sample budget | 2M env steps (= 2M gradient updates) per task per seed; 10 test seeds per arm; evaluation every 20k steps with 50 deterministic episodes on held-out episode keys. |
| Exploration geometry | A explores on $\mathcal S^{15}(4)$ through $\zeta$-Gaussian projection, B/C in a box. The entropy target is the only per-arm-tuned exploration knob, and it is inside the shared grid. |
| Pretraining disclosure | The H4 endpoint is *downstream* environment steps. The units' pretraining transitions ($W_{\mathrm{unit}}$) and wall-clock are disclosed alongside, with an amortization line $W_{\mathrm{unit}}/N_{\mathrm{tasks}}$. |

### 2.4 Analytic comparison of what each arm can and cannot do

1. **Expressivity at equal rate.** $x^{(j)}_{137}\subset O$, so any Mode A closed loop $u = \pi_\theta(x, \Pi(O))$ is a function of $O$ and lies in C's policy class given capacity. **A cannot beat C asymptotically on expressivity.** Any H4 gain is an optimization/sample-efficiency effect, coming from a structured action space with built-in local feedback. The reverse inclusion fails wherever $\pi_\theta(x,\cdot)$ is not onto $[-1,1]$. Pre-registered diagnostic: *reachability* $R(x) = |\mathrm{range}_{z}\,\pi_\theta(x,z)|/2$, from 4096 sphere samples, on visited states. Wherever $R < 0.9$, A and B carry an asymptotic ceiling relative to C. This is expected in exactly the OUT-amplitude cells, through B02's tanh saturation (Issue #8).
2. **Decoupling.** C sees both joints and can learn computed-torque-style feed-forward ($-M_{21}\ddot q_1$ from joint 1's $\widehat{\ddot q}$). Each unit sees only its own `x137` and treats coupling as an unknown external load, with residual $r(f)$ (§1.5). The upper layer in A/B can pre-compensate only through the units' response map. **Prediction**: A/B lead C early on IN cells, and C closes or reverses the gap at 2M steps in cells with significant class-X power above about 2 Hz.
3. **Mode A off-image risk.** The upper layer may command $z\notin B_\omega(\mathcal G_{\mathrm{feasible}})$, where $\pi_\theta$ was never trained. *Off-image fraction* is the share of commanded $z$ whose cosine distance to the nearest of $10^5$ pre-computed $B_\omega(\mathcal K_c(\cdot))$ samples exceeds the 99th-percentile nearest-neighbor distance within that set. It is logged for A, A-rand and B. B is structurally 0.
4. **Mode B transfer advantage.** $q^\star$ means the same thing when $L_2$ or $C_0$ changes, and the frozen unit absorbs the change through its descriptor. In Mode A, $z$ is meaningful across morphologies only to the extent B03's configuration-matched factorization holds. **Prediction**: B ≥ A on zero-shot retention.
5. **Closed-chain null mode (A/B only).** Units that integrate will ramp internal force under target inconsistency (L4). C has no integrators unless it learns them. A-NULL is logged for all arms. **Prediction**: A/B show larger hold-phase $|\dot\lambda_x|$ than C early in training, and this diminishes only if the upper layer learns null-space regulation. C-PD (explicit integrators) is the positive control that exhibits the mode.

---

## 3. Standardized 2-DoF Transfer Benchmark Specification (`LIMB2-v1`, closes Audit Issue #9)

### 3.1 Plant

| Item | Nominal | Notes |
|---|---|---|
| Base | $m_b = 1.5$ kg on passive vertical rail; attitude locked; rail friction 0 | $y\in[0.10, 0.70]$ m; termination $y<0.12$ |
| Thigh | $l_1 = 0.25$, $m_1 = 0.60$ (incl. knee drive), $l_{c1} = 0.15$, $I_1 = m_1l_1^2/12$ | hip stops $q_1 \in [-1.4, 1.4]$ rad |
| Shank+foot | $l_2 = 0.25$, $m_2 = 0.25$, $l_{c2} = 0.125$, $I_2 = m_2l_2^2/12$; foot sphere $r = 0.015$ m | knee stops $q_2 \in [0.05, 2.40]$ rad |
| Drives | $n = 9$, $J_r = 5\times10^{-5}$; hip $C_0 = 9$, knee $C_0 = 6$ ($S=1.25C_0$) | friction per V3 seed table of the matching unit configuration |
| Ground | penalty contact $k = 2\times10^4$ N/m, $c = 150$ N·s/m, $\mu = 0.8$ (simulator-agnostic; MuJoCo implementations must map to an equivalent `solref`/`solimp` and report the map) | flat, $z=0$ |
| Sensors | encoder 14-bit/rev, velocity noise $\sigma = 0.02$ rad/s, calibration $(s,\beta)$ randomized per episode and correctly calibrated | identical pipeline to single-unit V3 |

**Seed-hull gate.** Each joint's (descriptor, mass, inertia, friction) must fall inside the convex hull of the 36 V3 geometry seeds, or the cell is labelled `OUT_OF_SEED_HULL`, reported, and excluded from H4 primary endpoints.

**Unit prerequisite gate.** The frozen unit must satisfy B02 `coverage_ready = true` (720-cell joint array) and static-hold RMSE < 0.35 rad/s on the B02 canonical panel *before* any primary B04 run. Otherwise B04 primary runs are `BLOCKED_UNCONVERGED_UNIT` (Charter §2.4). Surrogate-unit runs must be labelled as surrogates.

### 3.2 Tasks (episode = fixed number of 50 Hz steps; all generators via Philox `make_program(run_seed, task, cell, episode_id, variant)` as in D-B02-001)

| Task | Setup | Command $c_t$ (8-D, zero-padded) | Reward per step | Primary metric / success |
|---|---|---|---|---|
| **T1 FREE-TRACK** (500 steps) | base locked with foot clear; reference = sum of 3 sines per joint, frequencies drawn from {0.5, 1, 1.5, 2} Hz train / {2.5, 3} Hz test, amplitudes hip ≤0.6, knee ≤0.5 rad around $q_2=1.0$ | $(q^{\mathrm{ref}}_{1,2}, \dot q^{\mathrm{ref}}_{1,2})$, task one-hot(3), phase | $-\sum_j \mathrm{wrap}(q_j-q^{\mathrm{ref}}_j)^2/0.05^2 - 0.01\lVert u\rVert^2$ | RMS error; success RMS ≤ 0.05 rad |
| **T2 SQUAT-HOLD** (300 steps) | foot on ground; payload $m_p$ on base: train {0, 0.5, 1, 1.5, 2} kg; height $h^\star$: stand ($q_2=0.4$) 1 s → squat to $q_2=1.2$ in 1 s → hold 2 s → rise 1 s → hold 1 s | $(h^\star, \dot h^\star)$, one-hot, phase | $-(h-h^\star)^2/0.01^2 - 0.01\lVert u\rVert^2 - 5\cdot\mathbb 1_{\mathrm{slip}}$; $h$ from joint kinematics | height RMSE ≤ 1 cm and hold-phase $\dot q$ RMSE < 0.35 rad/s, both joints |
| **T3 LAND-HOP** (250 steps) | (a) drop from foot clearance $h_0$ ∈ {0.05, 0.10} m train; stabilize to stand; (b) commanded periodic hop apex clearance {0.03, 0.06} m | $(h^\star_{\mathrm{apex}}$ or stand$)$, mode bit, one-hot, phase | stand: as T2; hop: $-(\text{apex}-h^\star)^2/0.01^2$ per apex, $-10$ per stop slam ($>0.05$ rad penetration), $-50$ on collapse | landing success = no collapse, no slam, $\lvert\dot q\rvert$ < 0.35 within 0.5 s; hop apex error ≤ 1 cm over 4 s |

$h$ is computed from joint angles and calibrated link lengths. Both are proprioceptive, and the link lengths are in the `x137` descriptor. **No contact flag is provided.**

### 3.3 Cell grid and pre-registered envelope classes

| Cell group | Values | Expected class (`LIMB2-REF`, §1.5) |
|---|---|---|
| T1 nominal | ≤2 Hz | IN (A-AMP), A-BW depends on $\Omega_{E3}$ |
| T1 test | 2.5–3 Hz | EDGE/OUT (hip $u_{\mathrm{req}}$ → 0.92) |
| T2 nominal | payload 0–2 kg | knee A-AMP IN→EDGE (0.41→0.78); A-RHO OUT at deep squat (ρ up to 9–19) |
| T2 stress | payload 2.5, 3 kg | OUT (0.87 / 0.97, the latter `INFEASIBLE_CONFIG`) |
| T3 nominal | 5–10 cm | A-IMP OUT unless $\hat I_{E4}$ ≥ observed |
| T3 test | 15 cm | OUT |
| **Morphology transfer (zero-shot)** | $L_2$ ∈ {0.18, 0.32, 0.40}; knee $C_0$ ∈ {3, 9}; hip $C_0 = 6$; plus $(L_2{=}0.32, C_0^{\mathrm{knee}}{=}3)$ | recomputed by the certificate; knee $C_0{=}3$ with payload ≥1 kg OUT |

All transfer values stay inside the unit's $L_D \in [0.08,0.45]$ and $C_0$ tiers, so **the units are in-distribution locally while the chain dynamics change**. This is the separation the transfer test needs.

### 3.4 Training regimes and transfer protocol

- **R-NOM**: upper trained on nominal morphology only. Zero-shot evaluation on every transfer cell, with each joint's `x137` descriptor updated to the true new calibration. This is legitimate calibration, applied identically to all arms.
- **R-MULTI**: upper trained on $L_2\in\{0.22, 0.25, 0.28\}$, knee $C_0 \in \{6\}$. Tested on extrapolation $\{0.18, 0.32, 0.40\}$ and $C_0\in\{3,9\}$.
- **Few-shot**: from the R-NOM checkpoint, $10^5$ steps of fine-tuning per transfer cell, with the upper layer trainable (A/B) or the whole policy trainable (C) and units still frozen.

### 3.5 Metrics and statistics

- **Sample efficiency (primary)**: $N_\theta$ = env steps until the 5-evaluation moving median first meets the task success criterion (§3.2), censored at 2M. Also normalized-return AUC over 2M steps.
- **Asymptote**: return at 2M steps (non-inferiority margin 5%).
- **Transfer**: zero-shot retention $\eta_{ZS} = R_{\mathrm{cell}}/R_{\mathrm{nom}}$; few-shot $N_\theta$ within $10^5$.
- **Diagnostics (always logged)**: per-cell certificate (§1.6), the L2 statistics $(\lVert g^{\mathrm{eff},M}\rVert, \angle g^{\mathrm{eff},M}, \dot\omega_P)$ histograms per unit, reachability $R$, off-image fraction, internal-force drift $|\dot\lambda_x|$, slip count, unit saturation rate $P(|u|>0.9)$, `FROZEN_HASH` checks.
- **Statistics**: 10 seeds per arm. Primary contrasts are A vs C and B vs C on $\log N_\theta$, using a seed-level bootstrap 95% CI with censored values set to 2M (conservative against A/B) and Holm correction over {A,B} × {T1,T2,T3} on IN cells. Transfer contrasts use $\eta_{ZS}$ differences with the same procedure.
- **Decision rules (H4)**:
  - **Supported**: on IN cells, for ≥2 of 3 tasks, the upper CI of $\log(N_\theta^{A\text{ or }B}/N_\theta^{C}) < \log 0.8$, with asymptotic non-inferiority.
  - **Falsified**: on IN cells, for ≥2 tasks, the lower CI is > 0 for *both* A and B.
  - **Supported-but-not-representational**: A-rand or C-PD is within the tie band of the winning modular arm (|Δ log N| CI contains 0 and |point| < log 1.1).
  - **Out-of-scope** (does not count for or against H4): OUT cells. For these the pre-registered prediction is the *direction* in §6 P2.

### 3.6 Closure criteria for Audit Issue #9

Issue #9 is closed when all of the following hold:
1. `LIMB2-v1` env + this spec are committed with a content hash, with seeds and `make_program` keys recorded.
2. The §1.6 certificate is computed for every cell and archived.
3. All 7 arms run end-to-end with deterministic resume (`resume_diff_norm = 0`, as in V3).
4. The evaluator's positive control (C-PD solves T1 nominal and T2 payload 0 to success) and negative control (random fixed $z$ fails all success criteria) pass.
5. The frozen-hash audit passes on every run.

Scientific evaluation of H4 additionally requires the unit prerequisite gate (§3.1).

---

## 4. Serious Alternative Considered and Rejected

**Alternative: augment each unit with housing-motion inputs and a moving-housing training regime ("E5_MOVING_HOUSING").** Lemma L2 shows that the knee unit's entire parent-motion dependence is carried by $g^{\mathrm{eff},M}$ (2-D) and $\dot\omega_P$ (1-D). Adding these three channels to the actor input, measured by a housing IMU, and training on a new regime where the housing is driven along random heave/pitch trajectories (an E5 drawing $\lVert g^{\mathrm{eff}}\rVert \in [0, 4g]$ and $\dot\omega_P$ up to the T3 values) would turn class-X coupling from an unobserved disturbance into an observed input. The unit could then feed-forward cancel it instead of estimating it with lag $\tau_d$, which removes the $r(f)$ residual. This is the most principled fix the reduction suggests, and the proposal takes it seriously.

**Why rejected for B04:**
1. **It changes the deployed contract.** `x137` is a frozen 137-D schema, and Charter §2.1 limits deployed modules to `x137`/`g13`. Adding an IMU channel is a schema change (140-D), not a composition test. It would also invalidate the B02 720-cell coverage and B03 rank analyses already accepted.
2. **It violates the brief's frozen-reuse constraint in spirit.** It requires retraining $(B,\pi)$ for chain operation, so B04 would test "units trained for chains", not "single-actuator units composed into chains". H4's claim is about the latter.
3. **It cannot fix class S or class K.** The extra inputs inform the unit about *exogenous* parent motion. They give no information about the unit's own reflected inertia in stance ($\rho$ up to 19, which depends on the closed chain and on the base/payload mass) or about the internal-force null mode, which needs a coordination signal across units. The main out-of-envelope phenomena of T2/T3 would remain.
4. **It confounds the ablation.** C would need the same IMU signal to stay fair, which changes the baseline as well.

**Retained as contingency.** If the B04 main study finds H4 falsified on IN cells *and* the A-BW diagnostic explains the gap (the modular deficit concentrates where class-X power exceeds $\Omega_{E3}$), E5 with the 3 extra channels is the pre-registered first candidate for a later packet. The logged L2 statistics (§3.5) define its training ranges directly.

*Also rejected, briefly*:
- **Residual torque on top of units** ($u = \pi_\theta(x,z) + \delta u$). The residual can absorb the whole task, so no outcome would be attributable to the representation.
- **Downstream fine-tuning of $(B,\pi)$.** Excluded by the brief.
- **Computed-torque decoupling inside the units using the other joint's state.** This breaks locality: a unit would read another unit's `x137`, and the module stops being a single-actuator representation.

---

## 5. Candidate Necessity Claims

### `C-B04-Q-01` — Amplitude-envelope inclusion is insufficient to certify H4's coverage proviso (requested: Candidate, Grade 1)

**Premises.**
- (P1) Each deployed unit is a frozen, time-invariant map $u_t = \pi_\theta(x_{137,t}, z_t)$.
- (P2) E3/E4 external torques in training are generated open-loop from exogenous generator state: $\tau_{\mathrm{ext},t} = \psi(\xi_t, k)$ with $\tau_{\mathrm{ext},t} \perp a_{t'} \mid \xi$ for all $t' \ge$ onset (the D-B01-001 causal partition).
- (P3) In the chain, $\tau^{(j)}_{\mathrm{ext,eff}}$ contains $\tau_{\mathrm{self}} = -(M^{\mathrm{eff}}_{jj}(Q) - J^{\mathrm{tr}}_j)\ddot q_j$ (§1.3), with $M^{\mathrm{eff}}_{jj}$ ranging over $[\rho^{\min}, \rho^{\max}]\,J^{\mathrm{tr}}_j$ along task trajectories.

**Claim.**
- (a) $\tau_{\mathrm{self}}$ is not in the support of any E3/E4 generator law, *for any amplitude setting*, because it is a function of the unit's own action through $\ddot q_j$, which contradicts P2.
- (b) There exist a frozen unit satisfying P1 and a chain trajectory along which $\sup_t|\tau^{(j)}_{\mathrm{ext,eff}}|/S_j$ is arbitrarily small at onset (so every amplitude test passes) while the local closed loop is unstable.
- (c) Hence any certificate of H4's proviso must include an inertia-ratio condition (A-RHO) and, in stance, a constraint-mode condition (A-NULL) in addition to amplitude and bandwidth.

**Proof sketch.**
- (a) follows directly from P2 and P3.
- (b) is a constructive counterexample. Take a 50 Hz PD with one-step delay tuned for $J^{\mathrm{tr}}$ (2 Hz, $\zeta = 0.7$). Its sampled closed loop is stable only for $\rho \ge 0.406$, with spectral radius 1.25 at $\rho = 0.25$ (`inertia_ratio.out.json`). The loop is linear, so instability is independent of the initial amplitude $\varepsilon$, while $|\tau_{\mathrm{self}}| \propto \varepsilon$ at onset.
- (c) Amplitude and bandwidth are properties of the torque signal. Stability under class S is a property of the loop, so signal-only tests cannot decide it.

**Scope limits.** (b) is an existence statement. It does not claim that the trained V3 unit is unstable at any particular $\rho$; that is measured by A-RHO in §6. An adaptive unit that infers inertia from history is covered by the same argument outside the $\rho$-hull it was trained on.

**Falsifier.** A demonstration that, for the trained V3 unit, A-AMP ∧ A-BW alone predict per-cell modular performance as well as the full certificate does. Concretely: adding A-RHO/A-NULL to a logistic predictor of the "modular arm reaches $N_\theta$" outcome across cells gives ΔAUC < 0.02. This would make the claim empirically vacuous for V3, though not false.

### `C-B04-Q-02` — Housing-transport identity (requested: Candidate, Grade 1, derivation)

**Premises.** Planar serial chain; joint $j$ carries a single rigid distal body (mass $m$, COM vector $r_c$ from the joint, inertia $I^J$ about the joint, rotor $(n, J_r)$ on the housing); friction identical to training.

**Claim.** The unit's effective external torque is exactly
$$-m\,[r_c\times(a_J - \vec g)]_z - (I^J + nJ_r)\,\dot\omega_P + \tau^{\mathrm{tr}}_{\mathrm{grav}} + \tau_{\mathrm{contact}},$$
with no bilinear term in $(\omega_P, \dot q_j)$. Hence:
- (i) Base heave enters only as $g\to g+\ddot y$.
- (ii) Flight converts held gravity load into an E4-type release.
- (iii) $(g^{\mathrm{eff},M}, \dot\omega_P)$ are sufficient statistics of parent motion for unit $j$.

**Proof.** The absolute COM acceleration is $a_J + \dot\omega\times r_c - \omega^2 r_c$ with $\omega = \omega_P + \dot q_j$. The terms $-\omega^2 r_c$ and the transport Coriolis term are parallel to $r_c$, so their moment vanishes. The remainder expands to $M_{21}\ddot q_1 + h\dot q_1^2 + M_{2y}\ddot y + G_2$. Numerically, the row identity holds to $7\times10^{-15}$.

**Necessity reading.** Any envelope comparison for distal units that tracks parent $\omega_P$ separately from $a_J$ double-counts. Any comparison that ignores $\ddot y$ misses the dominant T3 effect.

**Limits.** Distal *articulated* subsystems, such as the hip carrying a moving knee, require the full $M_{12}\ddot q_2$ and $h$ terms (§1.3). The identity is stated for the knee and for any terminal joint.

### `C-B04-Q-03` — Closed-chain integral null mode (requested: Candidate, Grade 1, conditional)

**Premises.**
- (P1) Stance with foot pinned and base attitude locked, giving a 1-D manifold with tangent $\varphi \in \mathbb{R}^2$ (joint space) and internal-force direction orthogonal to it.
- (P2) Each unit realizes integral action on its own position error: $\dot I_j = q^\star_j - q_j$ enters $u_j$ with gain $k_i$, explicitly or via the $u_{\mathrm{prev}}$ recursion.
- (P3) The linearized setting.

**Claim.** The combination $w = \varphi_2 I_1 - \varphi_1 I_2$ satisfies $\dot w = \varphi_2 q_1^\star - \varphi_1 q_2^\star$, independently of the motion. It is constant (neutral, unobservable from $s$) under kinematically consistent targets and grows linearly at rate $k_i\,|\varphi_2 q^\star_1 - \varphi_1 q^\star_2|$ under inconsistency. Internal force grows until saturation or slip. With leaky integration (time constant $T$), $w$ is bounded by $k_i T|\varphi_2 q^\star_1 - \varphi_1 q^\star_2|$.

**Verification.** In the author calculation (`null_mode`), consistent targets give $w \equiv 0$. With inconsistency 0.02 rad, $k_i w = -1.60$ at 2 s and $-3.20$ at 4 s, against an analytic $-0.8\,t$. With $T = 0.48$ s, the bound is $-0.384$ and the simulation gives $-0.3839$.

**Necessity reading.** Single-unit E0–E4 environments are passive (E1/E2) or open-loop (E3/E4, by P2 of A-01), and contain no second actuated integrator. No single-unit training signal therefore regulates this mode. A composition protocol must log it (A-NULL), and it should leave the upper layer an observable symptom. Here the symptom is the units' $u$ history drifting along $\nu$, which is in $O$.

**Falsifier.** A trained V3 unit pair in T2 hold showing $|\dot\lambda_x| \le 1$ N/s under deliberately inconsistent Mode B targets (δ = 0.02 rad) would show that P2 does not hold for V3 units. The claim would then not apply to V3, although it stays true as a conditional statement.

---

## 6. Pre-Registered Empirical Spike Protocol

### 6.1 `B04-SPIKE` (CPU, numpy, no trained units required; ≤ 5 min)

The spike verifies the *mechanism* claims and the benchmark plumbing. It does **not** test H4. That needs converged frozen units, which do not exist yet: the V3 run is a 101-update smoke test (Charter §2.4).

| Gate | Procedure | Pass criterion | Failure consequence |
|---|---|---|---|
| **S-G1** reduction identity | 2000 random states on `LIMB2-REF` and on 3 transfer morphologies; compare full-EOM torque with local-EOM + $\tau_{\mathrm{ext,eff}}$; also the L2 vector form for the knee | max residual ≤ $10^{-9}$ N·m | §1.3/C-B04-Q-02 withdrawn |
| **S-G2** envelope table reproduction | recompute §1.5 tables with fixed seed `20261023`, 3 reruns | bitwise-identical JSON; monotone in $f$ (T1) and payload (T2); knee squat $u$ crosses 0.92 between 2 and 3 kg | §1.5 numbers withdrawn and certificate thresholds re-derived |
| **S-G3** amplitude-insufficiency counterexample | surrogate 50 Hz PD (2 Hz, ζ = 0.7, 1-step delay) on $\rho\in\{0.25, 0.5, 1, 4, 20\}$; initial $\varepsilon = 10^{-3}$ rad | divergence (≥ $10^3\varepsilon$ in 5 s) at $\rho = 0.25$ with onset $|\tau_{\mathrm{self}}|/S \le 10^{-2}$; bounded at $\rho\in\{0.5, 1, 4, 20\}$; spectral radius matches simulation within $10^{-3}$ | C-B04-Q-01(b) downgraded to Grade 2 |
| **S-G4** null mode | linear closed-chain PI pair: consistent / δ = 0.02 / leaky $T = 0.48$ s | $|k_iw| \le 10^{-9}$; slope within 1% of analytic; leaky plateau within 1% of $k_iT\,|\varphi_2q^\star_1-\varphi_1q^\star_2|$ | C-B04-Q-03 withdrawn |
| **S-G5** fairness-contract audit | instantiate all 7 arms' networks and observation builders | $O$ dim = 282 for all; actor and critic trainable counts within 1% of A; frozen-hash check round-trips; identical physics/control timing constants | benchmark not released |
| **S-G6** evaluator controls (plumbing, surrogate units allowed and labelled) | 20 episodes T1 nominal + T2 payload 0 with C-PD; 20 with random fixed $z$ through A-rand | C-PD meets success criterion in ≥ 18/20; random-$z$ meets it in 0/20 | evaluator bug; block release |

Outputs go to `packets/B04/spikes/B04-SPIKE/VERDICT.json` with per-gate values, seeds, script hashes and device. The spike passes only if S-G1..S-G6 all pass. Reported numbers may not be tuned after the first run. A rerun is allowed only for a declared bug fix, and both runs are archived.

### 6.2 Main study pre-registration (runs after the unit prerequisite gate, §3.1)

| ID | Prediction (direction fixed now) | Test | Refutation |
|---|---|---|---|
| **P1** (H4) | On IN cells, A and B reach $N_\theta$ in ≤ 0.8× C's steps on ≥2/3 tasks, asymptotically non-inferior (5%) | §3.5 decision rules | §3.5 "Falsified" |
| **P2** (envelope dependence) | The modular advantage $\log(N^{C}_\theta/N^{B}_\theta)$ decreases with the certificate's exceedance score (sum of normalized code excesses) | Spearman over all cells, one-sided, 10 seeds | $\rho_S \ge 0$ with $p > 0.05$, or significant opposite sign |
| **P3** (transfer) | Zero-shot retention: $\eta^B_{ZS} \ge \eta^C_{ZS} + 0.10$ and $\eta^B_{ZS} \ge \eta^A_{ZS}$ on IN transfer cells (R-NOM) | paired bootstrap over seeds | lower CI of $\eta^B - \eta^C$ ≤ 0 on ≥ half the IN transfer cells |
| **P4** (bandwidth) | In T1, the A/B tracking error residual follows $r(f)$ within a factor 1.5 at $f\in\{1, 2, 3\}$ Hz, and C's asymptotic error at 3 Hz is lower than A/B's | per-frequency error ratio | ratio outside [1/1.5, 1.5] at ≥ 2 frequencies |
| **P5** (null mode) | T2 hold-phase $|\dot\lambda_x|$: C-PD > A ≈ B > C at 0.2M steps; A/B decline by 2M | ranks across seeds | C-PD not the largest (indicates evaluator/logging fault) |
| **P6** (representation, not reparameterization) | A beats A-rand by ≥ 1.25× in $N_\theta$ on IN cells | §3.5 statistics | A-rand within tie band → "not representational" ruling |
| **P7** (descriptor) | `D-ASSIGN-1` ≥ `D-ASSIGN-2` for hip-dominated T1 cells | secondary, reported only | none (exploratory) |

**Compute envelope.** 7 arms × 3 tasks × 10 seeds × 2M steps ≈ 420 runs, plus the HP grid (12 × 3 seeds × 0.5M per arm-task), plus transfer evaluation (deterministic, inexpensive) and few-shot ($10^5$ × cells × seeds). GPU per `gpu_experiments/` convention. If only CPU is available, P1–P3 run first at 1M steps with censoring at 1M declared in advance, and P4–P7 are deferred.

**Integrity rules.**
- Units are hash-locked and frozen throughout, including during few-shot.
- No privileged field enters $O$.
- The certificate uses evaluation-only logs.
- OUT cells never enter the H4 primary decision.
- Any change to thresholds, cells or arms after the first primary run voids that run's primary status.
