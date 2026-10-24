# Candidate (Packet B03): Hierarchical Task Coupling Under Partial Observability and Contact Dynamics

Primary Author B; frozen-context proposal; no training or new spike execution is claimed.
Decision: preserve motion-only $B$; distinguish missing information, inaccessible actions, and critic/planner learning failure before changing control frequency.
Sources: [Charter](../../../../PROGRAM_CHARTER.md), [B01 synthesis](../../../../synthesis/B01-synthesis.md), [B03 brief](../../brief.md), and frozen baselines [02](../../../../baseline/02-fb-paradigm-beyond-imitation-and-exploration.md), [04](../../../../baseline/04-joint-fb-ball-striking-v2-architecture.md), [05](../../../../baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md).
The proposal supplies the serious-alternative analysis requested under method v1.0 §11.5; it does not assume additional unstated method requirements.

## 1. Formal Information-Theoretic and Observability Analysis of Kinematic-Only B(m)

Let physical state $X=(q,v,g,\lambda,\chi)$ contain generalized configuration/velocity, geometry, contact wrench, and hidden material/actuator state.
Let $M=\kappa_D(X)$ be the frozen single-frame descriptor, $D\in\{229,277\}$, and $E=B_{\omega,\nu}(M)$ with fixed weights and normalization statistics $\nu$.
For traversal, $D=67+18(3+6)=229$, $d_z=256$, radius $16$; v2 ball striking declares $D=277$, $d_z=100$, radius $10$.
Use the task-specific v2 dimensions rather than baseline 02's generic assertion that both tasks use 256 latent coordinates.
Schema caveat: baseline 04's enumerated motion fields sum to 278, and its nominal 93-D actor fields sum to 107; these must be reconciled before simulator integration.
This proposal proves statements for the declared abstract descriptor sizes; it does not silently delete a field or claim that inconsistent production schemas were validated.

**Proposition 1 — exact forced aliasing boundary.**
Define $x\sim_\kappa x'$ iff $\kappa_D(x)=\kappa_D(x')$ and $x\sim_B x'$ iff $B(\kappa_D(x))=B(\kappa_D(x'))$.
Then $\sim_\kappa\subseteq\sim_B$, because a deterministic function assigns a single output to a single input.
Consequently, for admissible snapshots $x_{\rm air},x_{.40},x_{.60}$ with identical descriptors,
$$m_{\rm air}=m_{.40}=m_{.60}=m_\star\quad\Longrightarrow\quad B(m_{\rm air})=B(m_{.40})=B(m_{.60}),\qquad\max_{i,j}\|B(m_i)-B(m_j)\|_2=0.0.$$
The regimes are free-air flight, compliant support on a $0.40$ m box, and rigid impact on a $0.60$ m box; their geometry/contact metadata never enters this equality.
Interpret impact at a specified pre-impact instant, with impulse determining the subsequent velocity jump; equal frames do not require equal accelerations or equal next frames.
Different root translations/box placement and contact internal states can realize identical root-relative frames; the 277-D descriptor's base-height channel must also match.
This is conditional on identical complete descriptors, not merely identical joint angles, nor an assertion that every arbitrary posture realizes all three regimes.
There may be additional learned collisions between distinct descriptors; the converse implication is unjustified unless $B$ is injective on the relevant descriptor support.
Conversely, any two different descriptors can be separated by some motion-only map: equality of $M$ is exactly the aliasing forced by the input contract.
For approximately matched frames, a local Lipschitz bound gives $\|B(m)-B(m')\|\le L\|m-m'\|$, not exact zero.
Freeze BN, dropout, and weights: changing encoder state between queries invalidates the comparison.

Let $C$ denote contact regime, with logarithms in nats.
The Markov chain $C\to M\to E$ gives $I(C;E\mid M)=0$ and $I(C;E)\le I(C;M)$.
In a balanced matched-frame triad, $M=m_\star$, hence $I(C;E)=0$, $H(C\mid E)=\log3$, and optimal classification accuracy is $1/3$.
Outside this controlled distribution, kinematics may correlate with contact, so claiming globally $I(C;E)=0$ would be false.
Any deterministic Gram correction $WB(m)$ preserves equality; B01 whitening cannot recover omitted contact information.

**Proposition 2 — exact controller information boundary.**
Write deployable history $\mathcal H_t=(o_{0:t}^{\rm deploy},a_{0:t-1},z_{0:t-1})$, $z_t=P_\psi(\mathcal H_t)$, and actor information $U_t=(o_t^{\rm low},z_t)$.
Let $\mathcal A^\star(x,\iota)$ be acceptable physical actions for hidden state $x$ and task intention $\iota$, including actuator and safety constraints.
A deterministic memoryless actor can satisfy every case iff each information fiber admits a common action:
$$\forall u:\quad \bigcap_{(x,\iota):\,U(x,\iota)=u}\mathcal A^\star(x,\iota)\ne\varnothing,$$
subject to existence of a measurable selector and sufficient network capacity.
Necessity follows because the actor emits one action at $u$; sufficiency follows by choosing a common action on each fiber.
For unique desired commands $A^\star$, squared-error optimality instead has the exact Bayes decomposition
$$\mathbb E\|f(U)-A^\star\|^2=\mathbb E\,\mathrm{tr}\operatorname{Cov}(A^\star\mid U)+\mathbb E\|f(U)-\mathbb E[A^\star\mid U]\|^2.$$
Thus zero error is possible iff $\operatorname{Cov}(A^\star\mid U)=0$ almost surely; unrelated private randomization cannot reduce this lower bound.
Perceptive context resolves aliasing when scans/ball state/history identify the required action sufficiently, even with the same $B(m_\star)$.
Different geometry readings alone are insufficient if hidden friction, preload, stiffness, or task intention still requires incompatible actions.
An RNN can exploit past action-response measurements only if the relevant state is identifiable before the decision deadline; unseen independent disturbances defeat arbitrary memory.
Privileged $F/Q$ inputs improve conditional value estimates but cannot transmit unavailable facts to a deployable actor at execution.

**Isokinematic multi-force bottleneck.**
At a fixed posture and terrain geometry, constrained dynamics satisfy
$$\mathcal M(q)\ddot q+c(q,\dot q)=S^\top\tau+J(q)^\top\lambda,\qquad J\ddot q+\dot J\dot q=0.$$
Different admissible loads or intentions may require $\tau_1\ne\tau_2$ while all observed kinematics and geometry agree.
For identical desired acceleration, differences obey $S^\top(\tau_1-\tau_2)+J^\top(\lambda_1-\lambda_2)=0$, where feasible.
Redundant contacts can change internal wrench without requiring distinct commands; distinct measured forces alone therefore do not prove a control bottleneck.
Require distinct necessary actuator commands, or disjoint acceptable-action sets, rather than simply $\lambda_1\ne\lambda_2$.
For an equally likely hidden binary load with identical $U$ and unique targets $\tau_\pm$, every torque controller satisfies
$$\inf_f\mathbb E\|f(U)-\tau_C\|^2=\tfrac14\|\tau_+-\tau_-\|^2.$$
For position-command actors, apply this bound to required position targets, or explicitly convert via fixed invertible PD gains at the matched $(q,\dot q)$.
A hidden actuator state can itself change torque for the same command; audit that state before interpreting an action-space bound as a torque-space bound.
The bound is irreducible relative to the available information, not an unconditional limitation of all kinematic-latent architectures.
A planner is free to choose $z_+\ne z_-$ off the demonstration image when its history reveals the load/intention.
Even then, feasibility also requires $\mathcal R_\theta(o)=\{\pi_\theta(o,z):z\in\mathcal S^{d_z-1}(\sqrt{d_z})\}$ to intersect the desired action set.
Locally, inaccessible force directions are detected by $\delta\tau\notin\operatorname{im}(D_aT\,D_z\pi_\theta\,\Pi_z)$, with $\Pi_z=I-zz^\top/d_z$.
This rank test is local only; a failed local search is not proof of global impossibility.
Finally, if every available action has the same future $B$-feature occupancy but different force outcomes, FB rewards cannot identify a preferred force policy.
That is an objective-identifiability failure; distinct latents may still exist, but FB-only actor training supplies no preference among those force-equivalent solutions.

## 2. Comparative Architecture Analysis: Macro-Step Latent Value vs Action-Level Task Value

Use separate causal recurrent states $h_t^P$ and $h_t^Q$; the latter may include permitted privileged information $c_t$.
A shorthand $P(o_{\rm task})$ denotes the causal recurrent summary, not a replacement of v2's LSTM by a memoryless planner.
Define $\gamma=\gamma_{\rm task}$; $d$ means true termination, never timeout alone.

| Contract | Design 1: R2.1 traversal | Design 2: v2 ball striking |
|---|---|---|
| Decision | $z=P_\psi(h_t^P)$ held for $K=10$ controls, $0.20$ s | $z=P_\psi(h_t^P)$ each control, $K=1$, $0.02$ s |
| Critic action | Actual executed macro $z_{\rm actual}\in\mathbb R^{256}$ | Applied physical action $a_{\rm applied}\in\mathbb R^{29}$ |
| Inputs | Recurrent history plus privileged geometry for $Q$ | Separate recurrent deployable planner / privileged critic streams |
| Planner derivative | $D_\psi P^\top\nabla_zQ_1(h^Q,c,z)$ | $D_\psi P^\top D_z\pi_\theta^\top\nabla_aQ_1(h^Q,a)$ |
| Main limitation | Commitment delay and changing intra-macro policy | Actor Jacobian rank/saturation and rapid latent switching |

For Design 1, use each actual duration $1\le k\le10$ and discounted reward sum
$$R_{t:k}=\sum_{j=0}^{k-1}\gamma^j r_{t+j},\qquad y_t^z=R_{t:k}+\gamma^k(1-d_{t+k})\min_iQ_{\bar\phi_i}(h_{t+k}^Q,c_{t+k},P_{\bar\psi}(h_{t+k}^P)).$$
Train both heads on $(h_t^Q,c_t,z_{\rm actual},R_{t:k},k,h_{t+k}^Q,c_{t+k},d)$; never substitute $z_{\rm update}$.
A timeout uses the true pre-reset final history and bootstraps; a true terminal absorbs and does not bootstrap.
Arbitrary replay-slice endings inside a held macro are not new decisions: retain the held latent and remaining duration or exclude these cuts.
The baseline treats timeout as a decision boundary for continuation; any alternative preserving residual hold requires that residual in the bootstrap state.
Update the recurrent history on every control step, including observations during a held latent.

For Design 2, maintain the task-only EMA actor $\pi_{\bar\theta}$ as well as target planner and critics:
$$a'=\operatorname{clip}\{\pi_{\bar\theta}(o_{\rm low}',P_{\bar\psi}(h^{P'}))+\operatorname{clip}(\epsilon,-c,c),-1,1\},$$
$$y_t^a=r_t+\gamma(1-d_{t+1})\min_iQ_{\bar\phi_i}(h_{t+1}^Q,a'),\qquad \mathcal L_P=-\mathbb E Q_{\phi_1}(h_t^Q,\pi_\theta(o_t^{\rm low},P_\psi(h_t^P))).$$
Freeze $\theta,\phi$ parameters during the planner update while preserving $D_z\pi_\theta$ and $\nabla_aQ$; placing the actor call inside no_grad would destroy the intended gradient.
Targets are detached; planner gradients flow through its current recurrent training segment, not through environment transitions or privileged feature construction.
Low-level updates remain $-\mathbb E\min_i[F_i(o_F,\pi_\theta(o_{\rm low},z_{\rm update}),z_{\rm update})^\top z_{\rm update}]$.
Take scalar inner products before the ensemble minimum; no demonstration action regression or pose-tracking reward is introduced.

**Unification and controlled bridge.**
Both critics evaluate options: $Q^{(K)}(h,z)$ integrates the closed-loop actor under a commitment rule until the next permitted planner decision.
With $K=1$, fixed $\theta$, and identical continuation policy/information, $Q^{(1)}(h,z)=Q^a(h,\pi_\theta(o_{\rm low},z))$.
This identity additionally requires the first physical action to be sufficient for subsequent evolution; if recurrent updates retain $z$ independently of $a$, include that memory in the action critic state or do not assert equality.
It also assumes deterministic execution or integration over the same action noise; TD3 target smoothing is a regularized approximation.
For $K>1$, $Q^a(h,a_t)$ alone does not encode the subsequent $K-1$ held-latent actions, so the one-step chain rule is not the macro policy gradient.
Bridge first by separate $K=1$ and $K=10$ experiments on the same task, with identical rewards, action bounds, observation channels, and committed control-step budgets.
An optional contact-sensitive controller chooses the next hold duration $k_{\rm plan}\in\{1,10\}$ using deployable history only; store $(z_{\rm actual},k_{\rm plan},k_{\rm actual})$.
Train a duration-conditioned option critic, or include the fixed stopping rule in its definition; a changed duration policy changes the value function.
Unexpected causal event interruption closes a macro at actual $k$ and triggers a new decision; critic targets use $\gamma^k$ and the same interruption rule.
This bridge is a new ablation, not a silent change to frozen R2.1 or v2; shortening holds cannot solve hidden-load indistinguishability.
Keep $B$ motion-only throughout; contact estimates from past sensor/action response belong in deployable history if actually available, and privileged forces remain confined to allowed training modules.

**Replay, representation, and causality.**
Reconstruct each online/target RNN from zero over the complete episode prefix under frozen-weight no_grad burn-in, then BPTT the sampled segment.
Do not share hidden states between networks or carry them across resets; reset ball kick flags/timers before constructing initial observations.
Maintain immutable behavior labels, raw $(m_t,m_{t+1})$, and two real-data normalization passes; demonstrations never update normalizers.
Keep the 50/50 random-sphere/current-$B(m_{\rm next}[perm])$ update mixture and unfiltered expert/near/planner rollout schedule; no static admission or support-intent inference.
A shorter task replay window and actor EMA mitigate nonstationarity but do not prove Bellman stationarity or eliminate replay-distribution bias.
B01 permits unchanged $F^\top z$ actor readouts and raw demo prompts; do not whiten these or confuse contact aliasing with covariance rank loss.
If a later bridge adds model rollouts, use target-coordinate $\bar B^\top Wz$ rewards and the B01 gated terminal splice; no model rollout is needed here.
Finite credible severe penetration is a committed failure with absorption; invalid physics overrides it, rejects the whole transition, excludes normalization updates, and halts the affected run.

## 3. Serious Alternative Considered and Rejected

**Alternative A: augment the backward target to $B'(m,g,\lambda,b)$ with heightfields, contact wrench, and ball coordinates.**
Its serious advantage is that geometry and force-specific target rewards become representable, potentially distinguishing support, impact, and desired load.
However, the available demonstration provider supplies only $m$; an implementation would need an extension $e(m)=(m,\hat g(m),\hat\lambda(m),\hat b(m))$.
Take two physically admissible source worlds with the same $m$ and different $\lambda$: no deterministic $\hat\lambda(m)$ can equal both.
More generally, positive $H(g,\lambda,b\mid M)$ prevents universally correct recovery; random imputation restores uncertainty, not the missing realized context.
Appending the current environment instead encodes a scene-conditioned command, changes the demonstration semantics, and still cannot identify a hidden load from a heightfield.
Therefore this is rejected as incompatible with the frozen encoder/NPZ contract and insufficient as a universal observability fix, not as universally inferior RL.
The rejection is falsifiable in a different program: annotated source forces and permitted task-conditioned targets remove the compatibility argument.

**Alternative B: a recurrent monolithic task policy with identical deployable observations.**
This removes the restricted latent action image and can outperform a poorly conditioned hierarchy; it deserves a compute-matched experimental comparator.
It cannot overcome Proposition 2: identical available histories still imply the same conditional action distribution and the same hidden-load risk floor.
Replacing the hierarchy also abandons the specified demonstration-as-prompt and FB research question, so it is rejected as the proposal's implementation, not dismissed on performance grounds.
The chosen alternative is separate information routing into the existing actor/planner/critics, with explicit tests for latent controllability and information insufficiency.

## 4. Candidate Necessity Claims (Appendix B)

**C-B03-CAND-01 — information separation is necessary for incompatible contact commands.**
Premises: fixed deterministic encoder; identical complete $M$; identical deployable histories and task commands; hidden balanced load $C\in\{-,+\}$ independent of policy randomization; unique feasible required torque targets separated by $\Delta>0$.
Conclusion shape: $B$ separation is exactly zero and every deployable hierarchy has $\mathbb E\|\hat\tau-\tau_C\|^2\ge\Delta^2/4$; achieving zero error requires additional distinguishing information or relaxing the command requirements.
Necessity grade: **Grade 1**, a conditional mathematical necessity established by functional equality and conditional-variance decomposition.
Operational test: exact duplicated descriptors/histories, balanced paired loads, audited actuator conversion, and the analytic torque-risk experiment in §5.
Falsifier: paired population risk strictly below $\Delta^2/4$ with all premises verified; inspect leaked regime bits, correlated randomness, actuator state, and error normalization before declaring a counterexample.
Scope: different planner latents based on distinguishable histories violate a premise and are an expected escape, not a falsifier.

**C-B03-CAND-02 — context sufficiency requires action availability as well as information.**
Premises: observable causal context makes the required action deterministic; the fixed actor's latent action image contains that action; a measurable planner selector exists.
Conclusion shape: a hierarchy with motion-only $B$ can represent zero-error contact-specific execution; neither $B$ augmentation nor a contact-specific demonstration is necessary.
Necessity grade: **Grade 1** for the two feasibility conditions; successful learning is not part of the theorem.
Operational test: the constructed contextual controller plus latent-search and Jacobian diagnostics below.
Falsifier: verified premises with no selectable zero-error action; optimization failure alone does not falsify existence.

## 5. Pre-Registered Empirical Spike Protocol

This is a prospective replication/extension, specified after reading the permitted existing verdict; its thresholds are not retroactive preregistration of that run.
The existing JSON reports CPU PASS, $B$ max difference $0.0$, perceptive action MSE $0.0003300176467746496$, and multi-force MSE $0.8953267335891724$.
It supplies no seeds, force separation, normalization convention, or uncertainty; its last number cannot establish the bound without those premises.
No new scripts or experiments are executed in this proposal-writing task.

**Fixed setup.**
Use PyTorch CPU float64, deterministic algorithms, seeds $\{11,23,37,53,71\}$, $N=4096$ matched base frames, and disjoint base-frame IDs for train/test splits.
Test $(D,d_z)=(229,256),(277,100)$ with frozen eval-mode encoders; clone each generated frame exactly across three regimes.
Random vectors test the encoder contract only; additionally use valid extracted kinematic frames when the schema audit and simulator adapters are available.
No descriptor is augmented with regime labels; synthetic metadata is stored in separate tensors and never used to filter demonstration candidates.
Use explicit sum-over-actuators risk in normalized torque units; a library elementwise MSE on 29 channels must be multiplied by 29.

**(a) Exact aliasing and negative controls.**
Construct $m_{\rm air}=m_{\rm compliant\,0.40}=m_{\rm rigid\,0.60}$ with torch.clone; compare all encoder outputs and require maximum absolute difference exactly $0.0$.
Repeat across encoder seeds and a fixed frozen normalization transform; test terrain/ball/force metadata perturbations with descriptor unchanged.
A negative control changes a descriptor coordinate and records resulting separation without requiring injectivity of a random network.
Report failures as encoder-contract or determinism failures, never as evidence that kinematics recovered unobserved forces.

**(b) Perceptive disambiguation as a representability experiment.**
Use a controlled single-actuator fixture embedded in 29 channels: $\ddot q_1=a_1+c$, with context $c\in\{-1,0,1\}$ visible in an independent sensor channel.
The three regime labels index known dynamics offsets; they do not assert that real height scans directly reveal compliance.
At matched $q,\dot q$ and desired zero acceleration, the frozen constructed actor $\pi(o,z)=-c\,e_1$ succeeds while the context-blind optimal actor emits zero.
Balanced risk is exactly $0$ versus $2/3$; require numerical risks $\le10^{-12}$ and $|R_{\rm blind}-2/3|\le10^{-12}$.
Implement the actor as nn.Linear with fixed weights; no supervised action training or changes to the FB actor objective are permitted.
This tests the existence of context-sensitive execution, not its emergence under joint FB training; shuffled context must destroy the advantage.

**(c) Hidden multi-force lower bound, using identical geometry and sensor histories.**
Set hidden load $s\in\{-1,+1\}$, $\ddot q_1=a_1-s$, required $\tau_s=s e_1$, and expose neither $s$ nor a correlated past response.
For each base frame include both loads with identical actor inputs and fixed shared latent; $\Delta=2$ and the risk floor is $1$.
The following PyTorch core evaluates the exact paired identity, avoiding finite-sample claims about an optimizer reaching the Bayes solution:
~~~python
N, A = 4096, 29
u = torch.zeros(N, A, dtype=torch.float64)
v = torch.zeros_like(u); v[:, 0] = 1
def paired_risk(a):
    return (((a-v).square().sum(-1) + (a+v).square().sum(-1))/2).mean()
assert torch.allclose(paired_risk(u), torch.tensor(1., dtype=u.dtype))
a = torch.randn(N, A, dtype=u.dtype)
assert torch.allclose(paired_risk(a), 1 + a.square().sum(-1).mean())
~~~
Require identity residual $\le10^{-10}$ for every seed; report the minimum, mean, and per-seed results without selecting the best run.
Escape control: reveal $s$ causally to the planner and use $z_s=\sqrt{d_z}\,s e_1$, $\pi(o,z)=(z_1/\sqrt{d_z})e_1$; risk must become zero.
A second escape reveals a prior load-response observation to an RNN; a newly randomized load after that observation must restore the bound.
The constructed controls certify the conditional theorem and its boundaries, not full contact dynamics or learned humanoid success.

**Simulator extension and diagnosis, separately gated.**
After schema reconciliation, collect valid paired hand-support/obstacle-impact and ball-impact snapshots; record wrench, action, geometry, causal history, and subsequent kinematics.
Use same-state simulator branching for action comparisons; do not label near-matched frames as exact duplicates or force matching through invalid resets.
On heights $0.30$–$0.70$ and ball impacts, evaluate a fixed 128-latent candidate bank per snapshot with independent repeated branches and identical budgets across ablations.
A successful candidate with poor planner choice indicates a planning/ranking opportunity; failure of this finite search does not prove the latent image is empty.
Measure $F^\top z$ calibration against realized discounted feature rewards with B01-compatible coordinates, and $Q$ rank correlation against realized task returns.
Mask/shuffle scan or ball context separately in $F$ and $\pi$; large residuals with actor reachability intact implicate prediction/conditioning rather than backward aliasing.
Compare causal-history load prediction with a privileged-load diagnostic oracle to quantify remaining observability; oracle success is not deployable performance.
Match $K=1$, $K=10$, and adaptive-hold arms by committed physics steps, optimizer steps, and seeds; report wall time and actual decision counts separately.
Keep all primary numerical gates above fixed; simulator return comparisons report paired seed differences and 95% intervals without claiming necessity from significance.
Credible severe penetration remains a valid failed trial; invalid corruption halts the panel with its denominator retained as incomplete, never silently dropped.
Full traversal/striking claims require the charter's multi-seed training and held-out gates, including planner-only evaluations and the traversal Wilson-bound curriculum criteria.
