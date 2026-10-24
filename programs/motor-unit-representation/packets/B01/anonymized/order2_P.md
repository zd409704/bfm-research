# Candidate P (Packet B01): Privileged Forward Input Causality, Exogenous vs Endogenous Future Load Boundaries, and 22-Group Schema Audit

**Author:** Primary Author B. **Status:** proposal; all necessity claims are Candidate. **Packet:** B01. **Method:** v1.0, `1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`.

**Recommendation.** Preserve the `5065`-D interface, but make its contents a versioned, pre-action snapshot. Retain verified current and historical physical state; replace the entire `726`-D Groups 18–21 block with a causal disturbance-generator encoding and deterministic padding. No realized post-action contact, friction, stop, or external reaction value may enter the snapshot. The relevant boundary is dependence on the action being evaluated, not whether a field is named “future” or “force.” A scheduled release countdown can be admissible; an apparently current constraint force computed after latching the candidate action is not.

The proposal uses the five frozen context files and the pinned method's §11.5 and Appendix B. It does not infer implementation details from another author or from the V3 smoke test. The frozen specification provides exact **block** widths, but does not provide individual widths, offsets, or field names for Groups 1–21. Consequently, the audit below specifies all 22 group decisions and a deterministic field-admission rule; it does not fabricate a verified field-level manifest. Binding this rule to the implementation manifest is a mandatory acceptance gate.

## 1. Formal Causality Partition of p_5065 Across All 22 Schema Groups

### 1.1 Decision boundary and structural model

Let \(t\) mean the control boundary immediately **before** choosing and applying \(a_t\). Let \(\mathcal H_t^-\) contain the initial conditions, physical states, generator states, measurements, and completed transitions available by that boundary. Past actions through \(a_{t-1}\) belong to this information set; the current action and its realized consequences do not. Four completed 5 ms physics substeps from the preceding 20 ms interval are admissible history. Four substeps obtained by advancing the simulator with \(a_t\) are not.

Write the augmented pre-action state as \(S_t=(s_t,\xi_t,m_t)\), where \(s_t\) contains robot, obstacle, contact, actuator, and persistent solver state; \(\xi_t\) contains the exogenous disturbance process; and \(m_t\) contains any required history/filter state. A causal structural model is

\[
\xi_{t+1}=G(\xi_t,\epsilon_{t+1}),\qquad
s_{t+1}=T(s_t,a_t,\xi_t,\epsilon_{t+1},\nu_{t+1}),
\]
\[
y_{t+1}=R(s_t,a_t,\xi_t,\epsilon_{t+1},\nu_{t+1})
\equiv y_{t+1}(s_t,a_t,\xi_t)\quad\text{when innovations are fixed}.
\]

Exogeneity requires the **interventional** invariant

\[
P(\xi_{t+1}\mid\xi_t,s_t,\operatorname{do}(a_t=a))
=P(\xi_{t+1}\mid\xi_t)
\quad\text{for every admissible }a.
\]

Thus \(P(\xi_{t+1}\mid\xi_t)\) is independent of \(a_t\), with innovations drawn independently of the action conditional on the stated state. Merely observing a weak correlation with action is insufficient. A pre-sampled open-loop bias, sinusoidal phase oscillator, or time-triggered release process can satisfy this definition. A load that releases when the robot crosses a position threshold does not: its physical/controller state belongs to \(s_t\), and its future release event must be predicted from the transition. The state of such a reactive generator at \(t\) is still admissible; its counterfactual response cannot be treated as an exogenous fixed schedule.

For contact, a simplified reaction is

\[
q_{t+1}=q_t+\Delta t\,v_t+\Delta t^2 J^{-1}(Sa_t+\tau_t),\qquad
y_{t+1}=k[q_{t+1}-q_{\max}]_++c[v_{t+1}]_+.
\]

Away from switching surfaces, \(D_{a_t}y_{t+1}\) is generally nonzero when the stop is engaged. Velocity-dependent friction, contact impulses, and forces projected through a future robot orientation have the same problem. Even a world-frame force schedule independent of the robot can produce an **endogenous** future joint torque through its action-dependent moment arm. Retain the world-frame schedule and current geometry; do not retain the realized future projection.

A feature \(c_t=C(\mathcal H_t^-)\) is admissible only if it is available before action selection and invariant when the collector restores the same snapshot and changes \(a_t\). Causal availability is necessary but not sufficient for Markov sufficiency: the retained state must also determine the next-state distribution. An EMA is causal but need not be a sufficient state statistic. The Markov claim below is conditional on the complete persistent simulator/generator state being represented or predictively redundant given \((x_t,p_t^{\mathrm{causal}})\).

### 1.2 Complete boundary audit and admission policy

Use zero-based, half-open offsets. The frozen totals imply the following exact **aggregate** intervals:

| Groups | Aggregate interval | Width |
|---|---|---:|
| 1–6 | `[0:1920)` | 1,920 |
| 7–12 | `[1920:2944)` | 1,024 |
| 13–17 | `[2944:4096)` | 1,152 |
| 18–21 | `[4096:4822)` | 726 |
| 22 | `[4822:5065)` | 243 |

Let \(I_i=[b_{i-1},b_i)\) denote each actual manifest group, with \(b_0=0\), \(b_6=1920\), \(b_{12}=2944\), \(b_{17}=4096\), \(b_{21}=4822\), and \(b_{22}=5065\). Intermediate boundaries are unresolved by the frozen documents. The six items named for Groups 1–6, for example, cannot be asserted to correspond one-to-one to group numbers without the manifest.

The table assigns a default classification to **each** group under its frozen semantics. `R` means **retain-as-is**, collected at the pre-action boundary; `G` means **replace-by-causal-generator-state-at-t**, using the replacement construction below. `M` means **mask**, and is a mandatory slice-level override whenever the stated provenance test fails. A group containing an `M` slice is reported as mixed in the implementation audit, never silently certified as fully retained.

| Group | Class | Content supported by frozen specification and required boundary test |
|---:|:---:|---|
| 1 | R | Member of trajectory/solver block: retain only completed substeps ending at or before \(t^-\); mask any candidate-action rollout slice. |
| 2 | R | Same trajectory/solver block: position/velocity or other member fields require actual sample-time provenance, not a replay-row timestamp alone. |
| 3 | R | Same block: acceleration/filter entries must use a left-sided stencil through \(t^-\); mask centered or post-action samples. |
| 4 | R | Same block: actuator-force entries must describe the completed interval or pre-latch actuator state; mask values computed with \(a_t\). |
| 5 | R | Same block: constraint forces/impulses must be pre-action or from completed solves; mask forces from the solve producing \(s_{t+1}\). |
| 6 | R | Same block: solver residuals, warm starts, and substep state must precede candidate-action evaluation; mask post-solve diagnostics. |
| 7 | R | Member of plant-parameter block: static mass/inertia/geometry values are causal; verify exact field membership from manifest. |
| 8 | R | Same plant block: retain fixed inertia/COM or other declared parameters, without outcome-fitted values from the current transition. |
| 9 | R | Same plant block: retain friction/damping coefficients and pre-action internal friction state; mask realized future friction. |
| 10 | R | Same plant block: retain backlash/compliance parameters and current internal state; mask future deflection/reaction samples. |
| 11 | R | Same plant block: retain thermal/drive/saturation state at \(t^-\); mask thermal or saturation updates caused by \(a_t\). |
| 12 | R | Same plant block: retain nominal capacity/calibration and remaining verified pre-action parameters; mask provenance-unknown entries. |
| 13 | R | Member of contact/stop block: retain current obstacle geometry and signed distances, not distances after candidate-action rollout. |
| 14 | R | Same contact/stop block: retain verified pre-action or historical forces; mask forces from the new transition. |
| 15 | R | Same contact/stop block: retain current contact Jacobians/projections; mask evaluations at future robot geometry. |
| 16 | R | Same contact/stop block: retain current penetration, relative velocity, and spring/damper state; mask future penetration and reaction. |
| 17 | R | Same contact/stop block: retain current active masks and persistent solver/contact state; mask future contact activation flags. |
| 18 | G | Replace its portion of `[4096:4822)` by the corresponding portion of the canonical generator encoding; discard original future-force entries. |
| 19 | G | Same replacement rule, including zero padding; retain schedule information only through the canonical pre-action encoding. |
| 20 | G | Same replacement rule; reactive-generator state is tagged separately from open-loop schedule state. |
| 21 | G | Same replacement rule; current regime and release/recovery state are encoded from physical generator state, not future success labels. |
| 22 | R | Retain the `243`-D privileged EMA/history state through \(t^-\); mask any summary updated with the current transition, forward window, or episode-wide hindsight statistic. |

The examples in rows 1–17 specify tests for the named **block**, not an invented assignment of subfields to group IDs. Every actual field must be joined to a record `(group_id, start, stop, source, sample_time, action_latch_time, update_order, frame, units, normalization, R/G/M)`. This join, and assertions on all \(5065\) positions, resolve exact slices before implementation acceptance. No field escapes inspection because its group is outside 18–21.

For an unverified historical/current slot, masking is the safe interim behavior; it is not evidence that Markov sufficiency survived. If masking removes necessary persistent state, the schema binding fails and must be repaired before training. A stale replay record lacking a recoverable pre-action snapshot cannot be repaired by shifting its timestamp or setting future values to their empirical mean. Recollect it or exclude it from the causal experiment.

### 1.3 Explicit sanitized construction

Define \(c_j(\mathcal H_t^-)\) to be the correctly timestamped value of physical/history field \(j\), and \(m_j\in\{0,1\}\) its static manifest admission mask. The mask is fixed per schema version, not chosen from a future outcome. Construct

\[
p^{\mathrm{causal}}_{5065,t}
=\operatorname{concat}\left(
\{m_jc_j(\mathcal H_t^-)\}_{j=0}^{4095},
E_{726}(s^{\mathrm{gen}}_t,\xi_t),
\{m_jc_j(\mathcal H_t^-)\}_{j=4822}^{5064}
\right).
\]

Here masked positions are exactly zero **after** normalization as well as at the raw input adapter. Normalizer updates use only causal training snapshots, balanced across rule/policy partitions and the declared regime distribution. No future value determines normalization statistics. Constant padding receives no data-derived mean or scale.

For the open-loop scalar torque family explicitly described in the baseline, propose the following concrete replacement layout, relative to `[4096:4822)`. This is a **new** layout, not a claim about old offsets:

| Relative slots | New contents |
|---|---|
| `[0:5)` | Current E0–E4 one-hot, checked against actual scene/generator state. |
| `[5:8)` | Encoding-valid bit, control interval, current episode time. |
| `[8:16)` | Bias \(b\), ramp slope \(r\), sinusoid amplitude \(A\), angular frequency \(\omega\), \(\sin\phi_t\), \(\cos\phi_t\), onset countdown, release countdown. |
| `[16:24)` | Pulse magnitude, pulse onset countdown, pulse duration, elapsed pulse time, post-release bias, post-release ramp slope, load age, recovery age. |
| `[24:32)` | Eight flags: bias enabled, ramp enabled, sinusoid enabled, pulse enabled, load active, release occurred, open-loop schedule, reactive generator. |
| `[32:40)` | Current commanded exogenous torque, ramp accumulator, waveform clock, remaining scheduled duration, release-transition mode code, force-frame code, application-point code, stochastic-generator family code. |
| `[40:64)` | Declared generator-specific current state/transition parameters, with fixed semantic indices in the new manifest; zero for the deterministic scalar-torque template. |
| `[64:726)` | Deterministic zero padding for that template. |

For example, an active combined waveform is reconstructed from \(b_t+r_tu+A\sin(\phi_t+\omega u)\) and its onset/release/pulse gates at elapsed time \(u\). Phase, ramp accumulator, and countdowns advance from their current state without a robot action. A deterministic future schedule could legally be reconstructed from this state, but no future-window array is needed. The mapping fixes countdown units, phase convention, post-release behavior, and event-update order in the manifest. Inactive slots are zero with flags distinguishing inactive events from an event occurring now.

The eight flags and physical contact fields distinguish simultaneous phenomena; the scene one-hot is a sampling/regime tag, not an assertion that a scene contains only one force type. A release countdown is admissible only for a clock-triggered release. For threshold-triggered release, use the reactive-generator flag, current threshold/controller state, and current physical state; do not encode the realized remaining time to release.

For a richer supported generator, `[40:726)` may encode a declared finite-dimensional causal state, including stochastic transition parameters, external-body state, or reactive controller memory. Its field map must be frozen **before** training, fit the `726`-D allocation, and pass the same action-invariance test. The scalar template does not establish sufficiency for arbitrary multi-event, vector-force, or feedback generators. If the needed state does not fit or is unrecorded, the fixed-width sufficient-state requirement fails; silently truncating it is prohibited. Fresh stochastic innovations are integrated over, not retrieved from later rollout logs. A pre-sampled schedule counts as present state only if it genuinely existed in the environment at \(t\); a retrospectively recovered random seed is not a license to expose unrealized innovations.

The new block is split back across the original \(I_{18},\ldots,I_{21}\) boundaries by intersection with `[4096:4822)`. This preserves all 22 original tensor boundaries once their widths are supplied, even if a field crosses an old group boundary. The replay schema version changes, but the privileged compressor input remains `5065`. Checkpoints or replay normalizers from the original semantics are not resumed as if compatible.

### 1.4 Regime sufficiency and collection order

| Regime | Causal information retained for disambiguation |
|---|---|
| E0 | Geometry, inertia, gravity-related physical state, friction/drive state, absence of active external loading and obstacle contact. |
| E1 | Stop positions, current margins/penetration/velocity, stop parameters and active constraints; future stop force is predicted. |
| E2 | Current obstacle/contact geometry, material parameters, current/past contact and slip state; future contact response is predicted. |
| E3 | Active generator, bias/ramp/phase, load age, scheduled duration/release state, plus current physical response. |
| E4 | Actual release/pulse event state, time since release, current residual motion/contact state, and preceding load/impulse memory. |

Identical recent proprioception can coexist with different release countdowns or stop/contact geometry; these remain distinguishable. Regime one-hot labels alone do not prove this property. Audit Issue #1 makes step-level synchronization an explicit prerequisite: an episode labeled E3 without its scheduled load is a mislabeled sample, not successful disambiguation. Preserve the declared E0–E4 regimes while recording the real component states and ages.

Collection order is: finish the preceding physics interval; update causal filters and EMA using that completed interval; snapshot \((x_t,s_t,\xi_t,m_t)\); pack and seal \(p_t^{\mathrm{causal}}\); choose \(a_t\); execute physics; compute \(g_{t+1}\); form the next pre-action snapshot \(p_{t+1}^{\mathrm{causal}}\). A reaction produced by \(a_t\) can enter \(p_{t+1}^{\mathrm{causal}}\) as current/history state, but cannot enter \(p_t^{\mathrm{causal}}\). Pack copied arrays, not mutable simulator views that later become post-action values.

All new state is confined to the training-only forward critics. \(\pi_\theta(x_{137},z_{16})\) and \(B_\omega(g_{13})\) keep their existing inputs and `281,617` combined deployed parameters. No auxiliary privileged estimator is added to the deployed path.

## 2. Bellman Bias and Action-Jacobian Degeneracy Proof

### 2.1 Intended Bellman object and retrospective conditioning

For fixed latent \(z\), let \(b(g)\in\mathbb R^{16}\) be the frozen backward feature used for this argument. The causal successor critic satisfies

\[
F^\pi(S,a,z)=\mathbb E\left[b(g_{t+1})+\gamma(1-d_t)
F^\pi(S_{t+1},\pi(x_{t+1},z),z)\mid S_t=S,\operatorname{do}(a_t=a)\right].
\]

This equation describes the successor-feature component relevant to the argument; it does not assert an undocumented exact V3 loss implementation. For an FB occupancy formulation, the same conditioning argument applies to its vector or query-dependent TD target. The deployed actor uses the scalarization \(Q_z=F^\top z\); ignoring the actor's separate tanh saturation, its critic contribution is \(J_aF^\top z\).

Let \(L_t=p_{\mathrm{future},t}=h_K(S_t,a_t,a_{t+1:t+K-1},\varepsilon)\) be a realized endogenous future window generated under behavior policy \(\mu\). Regression on it estimates

\[
\widetilde F(S,a,l,z)=\mathbb E_\mu[Y^\pi_t\mid S_t=S,a_t=a,L_t=l],
\]

where \(Y_t^\pi\) is the Bellman target. This conditional target differs in general from \(\mathbb E[Y_t^\pi\mid S,\operatorname{do}(a)]\), because \(l\) reveals selected transition outcomes and, for \(K>1\), consequences of behavior-policy continuation. The conditional discrepancy is

\[
\Delta(S,a,l)=\mathbb E[Y_t^\pi\mid S,a,L=l]-\mathbb E[Y_t^\pi\mid S,\operatorname{do}(a)].
\]

In a fully observed randomized-action setting, averaging over the **correct action-dependent distribution** of \(L\) can give zero mean discrepancy by iterated expectation. Thus leakage does not imply that every on-policy scalar Bellman expectation is biased. The failure is that the standard actor update holds the recorded \(l\) fixed while varying \(a\), and target backups may hold a behavior-generated window fixed while substituting the target action/policy. These are generally incompatible counterfactuals, even when replay TD residual is zero.

More explicitly, if

\[
\bar F(S,a)=\int \widetilde F(S,a,l)\,P(dl\mid S,\operatorname{do}(a)),
\]

then differentiating also differentiates the distribution of \(L\). Under a smooth density this adds \(\mathbb E[\widetilde F\,\partial_a\log p(L\mid S,a)]\); under a reparameterization it adds the chain-rule term below. Treating replay \(L\) as a constant omits that term. Conditioning next-step critics on windows generated under \(\mu\) instead of the queried continuation policy produces an additional policy-dependent discrepancy. No such endogenous window is a policy-independent pre-action state variable.

### 2.2 Constructive zero-residual, arbitrary-gradient proof

Consider a deterministic one-step terminal system, which is a special case of the Bellman equation at any \(\gamma\). Let \(S\) contain a scalar bias \(b\), let \(a\in(-1,1)\), and define an endogenous reaction \(l=b+a\). Let the terminal feature be \(Y=v(b+a)\), with fixed nonzero \(v\in\mathbb R^{16}\) and \(v^\top z\ne0\). For every scalar \(c\), the critic

\[
F_c(S,a,l)=v\left[(1-c)(b+a)+cl\right]
\]

has **exactly zero Bellman residual on every physically consistent tuple** \(l=b+a\). Nevertheless,

\[
J_aF_c=(1-c)v,\qquad J_lF_c=cv,\qquad
\frac{d}{da}F_c(S,a,h(S,a))=v.
\]

At \(c=1\), the actor receives zero gradient although the true scalar action gradient is \(v^\top z\). At \(c>1\), the gradient reverses sign. At arbitrary \(c\), action sensitivity is unidentifiable from these perfectly fitted value observations. Adding a scalar function times \(l-h(S,a)\) to a critic changes off-manifold partial derivatives without changing any observational Bellman fit. This is a function-identification defect, not a consequence of a particular neural architecture.

If the replay action is \(a_b\) and the actor queries \(a'\) with \(l_b=b+a_b\) held fixed, then

\[
F_c(S,a',l_b)-F^\pi(S,a')=cv(a_b-a').
\]

The scalarized error is \(c(v^\top z)(a_b-a')\), despite zero replay residual. Repeating this construction at a bootstrapped next state yields a target error multiplied by \(\gamma(1-d)\). The terminal example alone already proves that a small observed Bellman residual cannot certify a correct policy gradient.

### 2.3 Quantitative degeneracy conditions and limits

At a differentiable point, define \(J_a\in\mathbb R^{16\times1}\), \(J_L\in\mathbb R^{16\times m}\), and \(H_a=D_a h_K\in\mathbb R^{m\times1}\), with \(S,z\) and future policy/noise convention fixed. If the fitted on-manifold critic agrees locally with the causal target, then

\[
J_{\mathrm{physical}}=J_a+J_LH_a,\qquad
g_{\mathrm{physical}}-g_{\mathrm{partial}}=(J_LH_a)^\top z.
\]

Use spectral norms for matrices and Euclidean norms for vectors. Since V3 has one action, \(\|J_a\|_2\) is unambiguous. A sufficient vector degeneracy condition is

\[
\|J_a\|_2\le\epsilon\|J_LH_a\|_2,\qquad
\|J_LH_a\|_2>0,\qquad 0\le\epsilon<1.
\]

It implies

\[
\|J_{\mathrm{physical}}\|_2\ge(1-\epsilon)\|J_LH_a\|_2,\qquad
\frac{\|J_a\|_2}{\|J_{\mathrm{physical}}\|_2}\le\frac{\epsilon}{1-\epsilon}.
\]

For example, \(\epsilon=0.05\) bounds the partial action sensitivity by `5.27%` of the physical sensitivity. For the actual actor direction, measure the analogous projected condition \(|J_a^\top z|\le\epsilon|(J_LH_a)^\top z|\), with a nonzero projected denominator. A large vector norm need not project onto the sampled \(z\).

The requested raw comparison is

\[
R_{a/L}=\frac{\|J_a\|_2}{\|J_L\|_2+\delta},\qquad
\|J_LH_a\|_2\le\|J_L\|_2\|H_a\|_2.
\]

Small \(R_{a/L}\) is a **screen**, not proof of degeneration: \(H_a\) may be zero for an exogenous schedule, or its range may lie in a null direction of \(J_L\). Action and privileged fields must be scaled consistently before norms are compared. Report derivatives per one declared training-set standard deviation and the composed product in physical-action units. In the example with unit \(H_a\), \(R_{a/L}=|1-c|/|c|\) ignoring \(\delta\); at \(c=1\) it is exactly zero.

Sanitization guarantees independence from **forbidden realized future inputs**, not a nonzero action Jacobian. A correct critic may have zero action derivative in a truly immobile saturated contact state or for a latent orthogonal to the response. Underfitting can also erase action sensitivity after sanitization. This is why the experiment uses independent counterfactual response derivatives and a causally controllable evaluation subset. The proposal does not claim that all leaky critics inevitably collapse, or that removing leakage alone establishes control convergence.

## 3. Serious Alternative Considered and Rejected

### 3.1 Keep future windows but stop their gradients

**Alternative.** Preserve the original future windows for their predictive information, but feed `p_future.detach()` into the critic and forbid autograd from traversing the physics collector. This keeps critic input dimensions, replay format, and apparent TD accuracy unchanged. It is a serious candidate because stop-gradient is routinely used to isolate bootstrap targets and would be inexpensive here.

**Rejection.** Recorded replay tensors ordinarily already have no autograd link to the original action. Detaching the input does not remove the critic's dependence on its **value**. In the \(c=1\) counterexample, \(F=v\,\mathrm{detach}(l)\) still has zero replay residual and \(\partial F/\partial a=0\); all parameter gradients needed to learn the shortcut remain available. Detachment deletes exactly the \(J_LH_a\) route needed to differentiate a recomputed consequence, while retaining its target information. It therefore cannot restore the desired derivative or pre-action information boundary. Reading a detached tensor's autograd gradient as zero would also produce a misleading “leakage eliminated” diagnostic; the experiment re-leafs the value to measure functional input sensitivity.

One could instead regenerate \(L\) for every queried action and differentiate through the full rollout, including continuation-policy effects. That is an action-conditioned dynamics model, not the original fixed privileged-state critic. It can be causally valid when supplied only pre-action state, but introduces model/solver differentiation and contact-switching issues, and no longer meets the proposed minimal adapter repair. It is not ruled out as a future implementation class.

### 3.2 Move all load information into Group 22 EMA

**Alternative.** Mask Groups 18–21 completely and rely on the `243`-D historical summary, contact state, and proprioception. This eliminates future-window handling and retains a compact causal load estimate.

**Rejection under the stated environment class.** Construct two generators with identical physical trajectories, applied loads, and all EMA inputs up to \(t\), but distinct pre-sampled release times: one releases next step; the other holds for 30 further steps. Their Group 22 states and \(x_t\) are identical. Their next-step conditional load distributions differ, so their Bellman targets differ for a suitable feature direction. A deterministic predictor of that common input must return the same value in both cases. For equally likely scalar targets \(u\) and \(v\), its minimum mean squared error is \((u-v)^2/4\). No EMA decay selection fixes a missing future schedule parameter that has never influenced the past. Retaining the causal release state removes this particular aliasing. The argument requires differing targets; a representation blind to load response would evade the example by abandoning the intended competence.

Group 22 remains useful for recovery and hidden-history estimation, but history alone is not a general substitute for known current generator state. This rejection is confined to generators with independent hidden schedule differences. In a restricted environment where generator state is determined by retained history, the alternative could be sufficient.

These alternatives satisfy method §11.5 within this proposal. Agreement with a brief-supplied causal boundary would constitute framed agreement, not independent evidence of necessity.

## 4. Candidate Necessity Claims (Appendix B)

### C-B01-P-01 — Observational Bellman fit does not identify a partial action gradient through an endogenous proxy

- **State / grade:** Candidate, Grade 1; no lock or veto authority is asserted.
- **Premises:** (i) A continuously variable action lies in an open interval; (ii) training inputs include a deterministic differentiable endogenous proxy \(L=h(S,a)\); (iii) training constrains critic values only on that consistency manifold; (iv) the admissible function class contains two differentiable extensions that agree on the manifold but differ in their partial action derivative, as the family \(F_c\) does; (v) the actor differentiates with respect to \(a\) while holding recorded \(L\) fixed; (vi) the true target has a nonzero derivative in at least one tested latent direction. No off-manifold constraints, structural derivative restriction, or recomputation through \(h\) are supplied.
- **Conclusion shape — impossibility:** Values/Bellman residuals on this manifold alone cannot uniquely identify the partial action derivative required by that actor update. There exist indistinguishable zero-residual critics yielding zero, correct, and reversed actor gradients. Therefore no guarantee of gradient correctness can follow from such value fit alone.
- **Derivation:** Section 2.2 constructs the indistinguishable \(F_c\) family. The construction applies to any function approximator admitting those extensions, including classical differentiable regressors; it is not a neural-network-specific theorem.
- **Scope:** A non-identifiability result, not a universal optimizer-collapse claim. It does not prohibit an endogenous prediction computed internally from causal state and candidate action. It does not prohibit exogenous schedule state for which \(D_a h=0\).
- **Operational test:** Implement \(c\in\{0,1,2\}\) with identical valid \((S,a,L)\) tuples; verify matching predictions and residuals, then measure their distinct partial action derivatives and matching total derivatives. Test off-manifold actor queries separately.
- **Falsifier:** An error in the explicit equal-value/different-gradient construction under these premises invalidates the proof. More generally, demonstrate unique partial-derivative identification using only the stipulated manifold values over the stipulated function class, without adding derivative constraints or removing admissible extensions. Finding one well-trained leaky critic with correct gradients does **not** falsify a non-identifiability claim; finding that the real V3 class/data lack premise (iv) or (iii) defeats applicability and must be recorded as a scope failure.
- **Promotion requirement:** Independent proof verification and the human lead's signature under Appendix B.9. A passing spike cannot promote this claim to Locked.

### C-B01-P-02 — Distinguishing generator states is necessary for state-specific load prediction

- **State / grade:** Candidate, Grade 1, conditional information lower bound.
- **Premises:** Two equally likely pre-action physical/generator states map to the same retained observation, their scalar Bellman target means are \(u\ne v\), and the predictor receives no further distinguishing information. Loss is squared error on that common observation. Any intrinsic target noise is additional.
- **Conclusion shape — lower bound:** Mean prediction error is at least \((u-v)^2/4\). Achieving a strictly smaller error requires information distinguishing these states, or a change to the target/task or state distribution.
- **Derivation:** Minimize \(\tfrac12(f-u)^2+\tfrac12(f-v)^2\) over \(f\); its minimum occurs at \((u+v)/2\). Randomizing the predictor cannot lower the bound.
- **Operational test:** The paired release-countdown construction in §3.2 fixes identical retained histories while varying the current release state. Measure the target separation using repeated physical continuations and then compare predictors with and without that state.
- **Falsifier:** A predictor beating the bound on a balanced population with genuinely identical retained inputs and verified target means, without extra information, would contradict the claim. Nonidentical inputs, unequal sampling, or finite-sample uncertainty invalidate the test rather than establish a counterexample.
- **Scope / implementation independence:** Some sufficient distinguishing information is necessary, not this exact `726`-D encoding, a specific EMA, or a named neural module. This claim also remains Candidate pending independent review and signature.

The charter's `>95%` explained-variance preservation hypothesis and the engineering thresholds below remain phenomenological tests. Neither follows as a theorem from these claims. No inherited ledger claim is changed by this author proposal.

## 5. Pre-Registered Empirical Spike Protocol

### 5.1 Status, hypothesis, and fixed arms

**Execution status:** protocol only; no learned-critic or physics experiment is reported as run. A read-only environment probe on 2026-10-23 found `python3` available and `torch` absent (`torch_installed: False`); the `python` executable was absent. CUDA availability is consequently **unverified**, not established as false. The spike is specified for CPU and needs no CUDA. At execution, record the PyTorch version, `torch.cuda.is_available()`, device count, selected device, and determinism settings. If CUDA is unavailable, explicitly record that fact and run on CPU. Installation/setup belongs to the designated experiment runner.

**Mechanism hypothesis:** realized endogenous future fields can dominate critic sensitivity while hiding action dependence; replacing them with causal generator state removes this route and recovers a physically correct partial action gradient without materially sacrificing causal target prediction. This is separate from proving converged motor control.

Freeze seeds `101, 202, 303, 404, 505`. Permit one registered training attempt per seed and arm; infrastructure failures remain logged and do not authorize selecting a better seed. Use three arms with identical physical transitions, target-construction rules, optimizer schedule, and paired initial weights:

1. **RAW:** original Groups 18–21, including separately identified endogenous future slices.
2. **DETACH:** same values as RAW, explicitly detached. This is a negative control and should be equivalent to normal replay input handling.
3. **CAUSAL:** the replacement in §1.3, with all other groups identically repaired to the verified pre-action contract in **every** arm. This isolates the effect of Groups 18–21.

RAW/DETACH exist only as controlled diagnostic arms. Hold \(B\), the evaluation policy, and latent samples fixed across arms to avoid changing target coordinates or action distributions. Test both forward heads separately; do not hide a failing head by averaging. First run the exact \(F_c\) diagnostic; then train the actual V3 forward architecture if its implementation is available. A smaller surrogate may validate instrumentation but cannot stand in for V3 evidence.

### 5.2 Exact diagnostic and physical sampling

**Stage A: analytic control.** In FP64 CPU PyTorch, choose \(v=e_1\), \(z=4e_1\), \(b\sim U[-0.5,0.5]\), \(a\sim U[-0.8,0.8]\), and \(l=b+a\), for `1,024` samples per seed. Embed \(l\) in an identified diagnostic future coordinate and use fixed zero padding elsewhere. Evaluate \(F_c\) for \(c=0,1,2\). This directly tests the theorem and metric implementation; it is not a trained-model result. The analytic causal comparator is \(F=v(b+a)\) built from pre-action \(b\) and \(a\), with no dependence on \(l\).

**Stage B: physical paired snapshots.** Require `4` independently generated training episodes and `2` held-out episodes for each of the `144 × 5 = 720` configuration/regime cells. Use `64` transitions per episode, comprising `184,320` training and `92,160` held-out transitions before provenance exclusions. These can be streamed into the bounded replay ring; they do not require expanding the `98,304`-transition replay capacity. Preserve the `1/3` rule and `2/3` policy sampling split and scene quotas `20/15/20/15/30%` during updates; report evaluation both equally weighted over the 720 cells and weighted by the declared quotas. Split by episode and generator seed, never by adjacent rows. Pre-action snapshots must include enough simulator state to restore contact/solver history exactly. This deliberately small episode panel is a causal diagnostic; its cell counts are not the program's behavioral readiness counts.

Use a synchronized E3/E4 schedule that actually produces a sustained interval of at least 25 steps and a release/recovery interval. At each selected snapshot, restore the same state and common exogenous randomness for action branches. Preserve a local grid of actions including \(a\), \(a\pm0.01\), and \(a\pm0.02\) when within `[-1,1]`. This creates action intervention support instead of relying only on unrelated replay actions. Record a joint 720-cell sample ledger and all exclusions. Missing cells or unsynchronized regimes block a full-regime conclusion.

Choose `2` held-out interior-action snapshots per cell for Jacobians (`1,440` total), one from each held-out episode. Fix two latent vectors per snapshot: one sampled uniformly on \(\mathcal S^{15}(4)\) and one held-out target-encoded latent, with no privileged conditioning. Never choose \(z\) after inspecting a model's gradients. Use the same indices and latents for all arms.

**Training prescription:** train each twin forward critic for `2,000` updates, batch `128`, Adam at `3e-4`, no weight decay, using the same frozen \(B\), frozen behavior/evaluation policy, transition/latent draws, and replay order across arms. Freeze normalizers from causal training data; RAW future-field scales use training-only data and are documented separately. Use the minimal successor TD loss with \(\gamma=0.95\), a target-critic EMA coefficient `0.01`, and the vector squared Bellman error from §2.1. Each head bootstraps from its own target copy; resulting numerical training targets can differ by arm. The independent evaluation target in §5.5 is shared. This is a specified diagnostic loss, not a claim that it reproduces an unspecified production FB loss. Any later production-loss validation is a separately labeled run. Evaluate at update 0 and 2,000; do not select the best intermediate checkpoint. Failure to fit within this bounded spike is reported, not repaired through unregistered extra updates. Record wall time and resource use; CPU execution may still be substantial for the full V3 critics.

### 5.3 PyTorch measurement contract

Use a public wrapper around each actual critic with signature `F(x, p, a, z) -> (16,)`; set evaluation mode and freeze all running statistics. Let `idx_future` contain **only audited endogenous future fields** from the original Groups 18–21. Do not combine exogenous schedules and endogenous reactions into one reported future norm. Let `sanitize(raw, current)` replace the entire block from an independently saved pre-action generator snapshot `current`; it must never derive replacements from `raw[idx_future]`.

The following kernel is executable once those adapters and manifest indices are supplied. It computes exact small-output Jacobians; batch it over samples, not over a training-mode network with cross-sample normalization:

```python
import torch
from torch.func import jacrev

def sensitivity(F, x, p_raw, a, z, idx_future, sanitize, current,
                a_scale, future_scales, causal):
    # a: (1,), p_raw: (5065,), outputs: (16,); all are floating tensors.
    # Re-leaf raw values: this probes functional dependence even for DETACH.
    a0 = a.detach().clone()
    p0 = p_raw.detach().clone()

    def value(aa, pp):
        packed = sanitize(pp, current) if causal else pp
        return F(x, packed, aa, z).reshape(16)

    Ja, Jp = jacrev(value, argnums=(0, 1))(a0, p0)
    JL = Jp[:, idx_future]
    Ja_std = Ja * a_scale
    JL_std = JL * future_scales[None, :]
    A = torch.linalg.vector_norm(Ja_std)
    P = torch.linalg.matrix_norm(JL_std, ord=2)
    g = (Ja.T @ z).reshape(())
    return {"Ja": Ja, "JL": JL, "A": A, "P": P,
            "ratio": A / (P + 1e-12), "actor_gradient": g}
```

Here \(J_L\) in CAUSAL is the derivative of the **composite sanitized model with respect to original forbidden input values**; it must be zero. Derivatives with respect to the new generator-state slots are measured separately and may be large. Comparing those legal-state derivatives to the original future-force derivatives as though they were the same quantity would be invalid. If `idx_future` is empty, the tested implementation lacks the claimed leak and the RAW mechanism test is not applicable.

Compute \(H_a\) from simulator branches as \([L(a+h)-L(a-h)]/(2h)\), with the same future policy and random innovations; record \(\|J_LH_a\|_2\), \(\|J_a\|_2\), and their latent projections. Compute the reference derivative \(D_{\mathrm{ref}}\) from branch returns under the fixed evaluation policy:

\[
G_H=\sum_{k=0}^{H-1}\gamma^k(1-d_{<k})B(g_{t+k+1}),\qquad
D_{\mathrm{ref}}=\frac{\mathbb E G_H(a+h)-\mathbb E G_H(a-h)}{2h}.
\]

Use \(H=200\), \(\gamma=0.95\), and `16` common-random-number continuations per action for stochastic scenes (one for deterministic scenes). With \(\|B\|=4\), omitted return norm is at most \(4\gamma^{200}/(1-\gamma)<0.0029\). This bounds values, not derivative error; also compare \(H=100\) versus 200 and \(h=0.01\) versus 0.02. Include a snapshot in the smooth derivative gate only when both derivative comparisons differ by at most `10%` of the reference norm and reference uncertainty is at most `10%`. Define the controllable subset by \(\|D_{\mathrm{ref}}\|_2\ge0.05\) per unit normalized action. Define the scalar sign subset additionally by \(|D_{\mathrm{ref}}^\top z|\ge0.05\). These inclusion rules depend only on independent physical references, not critic outputs.

At contact switches, report one-sided finite changes and their prediction errors separately; do not interpret a discontinuity as an autograd failure. If fewer than `50%` of selected snapshots overall, or fewer than `10%` in any regime, meet the smooth/controllable criteria, mark the derivative test underpowered. A large number of immobile stop samples cannot be used to manufacture a successful nonzero-gradient gate.

### 5.4 Quantitative gates

All thresholds below are pre-registered engineering criteria. Report the complete distribution by seed, head, regime, and configuration, together with paired differences. For statistical claims use `2,000` episode-cluster bootstrap resamples within each configuration/regime cell, followed by paired resampling of the five training seeds; preserve branch pairings. Report 95% intervals, including per-regime results. No threshold may be chosen after seeing the Jacobians.

| Gate | Pass criterion | Failure interpretation |
|---|---|---|
| Provenance and packing | All 5,065 positions assigned once; widths sum to `4,822 + 243`; all retained values precede action latch; manifest and normalizer hashes recorded. | Audit incomplete; no claim of an exact sanitized schema. |
| Counterfactual invariance | Across action branches, packed \(p_t^{\mathrm{causal}}\) is identical for identical snapshots; FP32 maximum absolute difference ≤ `1e-7`. Changing arbitrary forbidden future values leaves outputs invariant to the same tolerance. | Remaining leak, aliasing of mutable buffers, or nondeterministic packing. |
| Analytic control | For all \(c\), maximum prediction/residual error ≤ `1e-10` in FP64; \(J_a=(1-c)v\), \(J_L=cv\), and total derivative \(v\) agree within `1e-10`. | Proof implementation or measurement failure; stop learned-critic interpretation. |
| Forbidden sensitivity | CAUSAL \(\|J_L\|_2\le10^{-10}\) in FP64 evaluation for every tested sample; random future-field finite perturbations agree with this result. | Adapter failed; legal generator-state gradients are exempt. |
| RAW bypass reproduction | In at least `4/5` seeds and each head, at least `25%` of smooth controllable samples have \(\|J_a\|_2\le0.1\|J_LH_a\|_2\), with nonzero omitted projected sensitivity where scalar failure is claimed. Also report standardized \(R_{a/L}\). | Shortcut not reproduced in this learned model; do not claim an empirical cure merely because CAUSAL masks an input. |
| Action derivative recovery | CAUSAL median relative vector error \(\|J_a-D_{\mathrm{ref}}\|_2/\|D_{\mathrm{ref}}\|_2\le0.20\), 90th percentile ≤ `0.50`; median norm ratio lies in `[0.8,1.2]`; scalar sign agreement ≥ `95%` on the sign subset. Each head and at least `4/5` seeds must pass; no regime median vector error may exceed `0.35`. | Remaining critic/representation/coverage problem; masking alone is insufficient. |
| Paired causal improvement | When RAW bypass reproduces, CAUSAL reduces median vector derivative error by at least `30%` relative to RAW, and the 95% interval for the paired improvement excludes zero. DETACH differs from RAW median error by no more than `5%` under deterministic paired runs. | No demonstrated gradient benefit, or invalid negative-control implementation. |
| Bellman consistency | Held-out causal counterfactual normalized RMS Bellman residual ≤ `0.15` for CAUSAL; no regime exceeds `0.25`; CAUSAL is not more than `0.02` worse than RAW when RAW is queried with fixed recorded future windows under the same action interventions. | Fit/backup accuracy is inadequate or the proposed repair sacrifices too much accuracy. |
| H1 prediction preservation | Held-out target explained-variance ratio \(EV_{\mathrm{CAUSAL}}/EV_{\mathrm{RAW}}>0.95\), with 95% lower confidence bound > `0.95`; require \(EV_{\mathrm{RAW}}>0.20\) for an interpretable ratio. Report all regimes; a regime loss exceeding `0.05` absolute EV blocks full-regime acceptance. | H1 unconfirmed or falsified in this panel; do not relabel poor RAW fit as preservation. |

### 5.5 Bellman residual and explained-variance definitions

Freeze a common reference target before comparing arms. Use a reference evaluator \(\widehat F_{\mathrm{ref}}^\pi(S',\pi(x',z),z)\) estimated by independent physical Monte Carlo continuations with the same fixed \(B,\pi,\gamma\), and form

\[
Y_{\mathrm{ref}}=B(g_{t+1})+\gamma(1-d_t)\widehat F_{\mathrm{ref}}^\pi(S_{t+1},\pi(x_{t+1},z),z).
\]

Estimate its conditional mean by repeated branches as needed; use common reference samples for all arms. Report Monte Carlo uncertainty and do not count irreducible target noise as approximation bias. For model prediction \(\widehat F\), define

\[
\mathrm{NRBR}=\sqrt{\frac{\mathbb E\|\widehat F-Y_{\mathrm{ref}}\|_2^2}
{\mathbb E\|Y_{\mathrm{ref}}-\mathbb EY_{\mathrm{ref}}\|_2^2+10^{-12}}},\qquad
EV=1-\frac{\operatorname{tr}\operatorname{Cov}(Y_{\mathrm{ref}}-\widehat F)}
{\operatorname{tr}\operatorname{Cov}(Y_{\mathrm{ref}})+10^{-12}}.
\]

Report mean vector bias alongside EV because EV alone ignores constant prediction offsets. Mark a near-zero target-variance cell undefined rather than divide it into a favorable score.

Measure two distinct panels: (i) **factual prediction**, where each RAW future window corresponds to the recorded action, used for the charter's H1 comparison; (ii) **actor-query counterfactuals**, where RAW retains the recorded window but the simulator independently evaluates the new action, used for causal Bellman consistency. CAUSAL retains the same pre-action state in both panels. Also report each arm's ordinary self-bootstrapped TD residual, but do not use it as the sole acceptance criterion: the proof supplies a critic with zero such residual and a wrong gradient. If a sampled factual RAW window reveals stochastic innovation, H1 can fail because that information was never causally predictable; report the gap rather than restoring the forbidden preview.

### 5.6 Outputs, stop conditions, and interpretation

The designated runner should freeze adapters and the exact invocation in the experiment plan before execution. Proposed invocation after implementation is `python3 run_b01_causality_spike.py --device cpu --seeds 101 202 303 404 505 --arms raw detach causal --updates 2000 --gamma 0.95 --output results/`; this names a proposed harness, not an existing file. Record the command, dependency versions, source/schema hashes, snapshots/episode identifiers, sampled latent vectors, normalizer statistics, arm configs, and any deviation. Produce per-sample Jacobian/finite-difference metrics, per-cell provenance/count ledgers, residual/EV tables, raw seed results, and a machine-readable gate verdict. Missing physics code, manifest, checkpoint compatibility, or PyTorch is reported as a setup block, never as a passing run.

The author writes only this proposal. The experiment runner owns code and execution artifacts under the method's write-permission rules; this proposal does not modify the sealed spike plan or publish a claim lock. Failure of the analytic/invariance gates stops scientific interpretation. Failure of a learned-critic gate leaves the empirical repair unverified, even if the causal boundary proof remains sound.

Passing this spike would support a causal forward-input repair and a measured gradient benefit for the tested distribution. It would not establish `coverage_ready`, converged holding, the remaining eight audit repairs, or multi-joint transfer. Those require their own real-physics evidence, including all 720 configuration/regime cells and the program's load-hold/recovery gates. The existing 101-update V3 result remains pipeline verification only.
