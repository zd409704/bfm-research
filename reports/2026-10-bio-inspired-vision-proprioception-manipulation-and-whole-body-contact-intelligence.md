# From Perception to Contact

## A Bio-Inspired Vision–Proprioception–Manipulation Architecture and Whole-Body Contact Intelligence for Robots

**An objective technical report**

---

## Executive Summary

This report synthesizes current research on biological vision, proprioception, robot manipulation, and whole-body locomotion into a single architectural position:

**A robot that perceives, predicts, and acts in a closed loop — rather than one that first builds a complete model of the world and then plans over it — is better positioned to manipulate objects and to move its whole body through complex environments.**

Three claims organize everything that follows:

1. **Manipulation is not object recognition.** It is the progressive establishment of a controllable relationship among body, object, and environment. The state a robot should maintain is therefore an *interaction-centric belief* — what can be contacted, where, with what expected physical outcome, and with what uncertainty — rather than a purely geometric 3D reconstruction.

2. **Perception, prediction, and action form one loop.** Biological systems continuously predict the sensory consequences of their own motion and update their beliefs from prediction errors. Attention, heavyweight perception, and replanning should be *triggered by prediction error*, not run uniformly on every frame.

3. **Whole-body locomotion over obstacles is the same problem at a larger contact surface.** Climbing, vaulting, crawling, and bracing are sequences of contact-state transitions. Given a pretrained behavioral foundation model (BFM) that supplies balance, motion continuity, and transitions between postures, the missing research layer is not a new locomotion policy but *contact reasoning*: perceiving which body part should contact which environmental feature, in which order, and verifying each contact before proceeding.

Part I develops the architecture for vision-based manipulation. Part II extends the same principles to whole-body contact intelligence for climbing and obstacle traversal.

---

# Part I — A Bio-Inspired Vision–Proprioception–Manipulation Architecture

## 1. The core thesis

The conventional manipulation pipeline is:

> RGB → object detection → 3D reconstruction → pose estimation → motion planning → inverse kinematics → grasp

The alternative proposed here is a progressive, closed-loop process. To pick up a cup, a robot does not need to understand "a complete cup" at the outset. It needs to establish, step by step:

- a relatively stable entity exists there;
- how far it is from the hand;
- which surface can be contacted;
- whether visual change during approach matches prediction;
- whether contact actually occurred;
- whether the object moves with the hand after contact;
- whether the current grip force is sufficient;
- whether the object has effectively become part of the robot's own control chain.

The last step is the most important: **the essence of manipulation is not identifying objects, but progressively establishing a controllable body–object–environment relationship.** This is much closer to how animals operate than "build a complete 3D model first."

## 2. What biological vision actually teaches

### 2.1 Structure can substitute for learned representation

The Drosophila visual system comprises roughly 53,000 visual neurons in about 732 types, with different neuron types directly implementing different visual computations. The FlyVis research line constrained a network with the real fly connectome — permitting only connections that actually exist — and trained it on an optic-flow task. ON/OFF pathway separation, temporal filtering, T4/T5 direction selectivity, local motion detection, and global optic-flow representations *emerged from the structure*.

The design principle for robotics: **motion-related representations do not have to be learned inside a large generic vision model; they can be forced into existence by architecture.** A lightweight, structured front-end can deliver optic flow, looming, and motion boundaries at high rate and low cost, reserving large models for where they are actually needed.

### 2.2 Vision answers three different questions

Biological vision is not one module. It simultaneously addresses:

1. **What is out there?** — objects, edges, colors, categories, structure. (This is what modern VLMs, SAM, and DINO-style encoders do well.)
2. **Where am I relative to it?** — optic flow, ego-motion, depth, surface orientation, time-to-collision, heading. (Insects excel here.)
3. **What can I do to it?** — reach, grasp, push, pull, rotate, insert, support, cut. (This is what manipulation actually cares about.)

The primate visual system reflects the same division: the dorsal stream is largely *vision for action*, the ventral stream *vision for perception*, and parietal–motor circuits directly convert visual input into sensorimotor representations for reaching and grasping. "Knowing what a cup is" and "knowing where to grasp it" are not the same visual problem, and a robot's architecture should not treat them as one.

### 2.3 Proprioception belongs inside the visual system

In mouse V1, close to half of the neurons studied are jointly modulated by optic-flow speed *and* running speed. Even "visual cortex" already computes *how much the world is moving plus how much I am moving*.

The robotic consequence is a change of status for ego-motion: robot ego-motion should not be treated as noise corrupting vision (to be stabilized away), but as a **conditioning variable of visual understanding itself** — vision interpreted *given* the body's own motion, joint state, and motor commands (efference copy). Head motion during walking, for example, is then informative rather than a disturbance.

## 3. The state to maintain: interaction-centric world state

Typical robot vision builds records of the form `object: {class, position, orientation}`. For manipulation this is insufficient. A more appropriate structure is an **object belief** with fields such as:

- **Identity:** probable class or "unknown," with confidence.
- **Geometry:** surfaces, edges, openings, axes, handles, convexity.
- **Dynamic state:** position, velocity, angular velocity.
- **Physical belief:** mass, friction, stiffness — each possibly unknown; articulated or rigid; fixed or movable.
- **Interaction:** graspable regions, support relations, candidate contact points, reachable regions, collision regions.
- **Relations:** on(table), inside(box), touching(wall), connected(hinge), held_by(robot).
- **Uncertainty:** separate confidences for geometry, pose, and physical properties.

Crucially, many of these values are *unknown at first sight — for animals as well*. They are resolved through action, not through longer observation.

## 4. Affordance is more actionable than classification

"This is a pair of scissors" does not tell a robot what to do. What matters is: here it can be gripped; here force can be applied; here it can rotate; this part is a blade; this part can cut. Recent manipulation research is moving in exactly this direction: systems such as OmniManip have the vision-language model output an *interaction point, a direction, and spatial constraints* — object-centric interaction primitives — while a low-level 6D tracking layer executes the motion. The division of labor is principled:

> **The language model decides what relationship should hold, and where; the geometry/control system decides how to achieve it accurately.**

## 5. After contact, vision becomes secondary

Animals do not operate by "look → compute position → grasp." They look, approach, contact, touch, adjust, and only then operate. Before contact, vision dominates. After contact, the decisive signals are tactile and proprioceptive: vision can estimate a cup's size, position, material, and probable weight, but it cannot determine its actual friction coefficient, its actual mass, whether it is slipping, or whether the grasp is stable. Those are only knowable through action.

Human manipulation research is unambiguous on this point: grip force is jointly feedforward- and feedback-controlled, and slip-related signals from skin receptors trigger rapid grip-force corrections. Recent (2025) robotics work explicitly models this slip response. A manipulation platform therefore needs, beyond stereo vision, fingertip pressure sensing, 6-axis force/torque sensing, tactile sensing, and slip detection — their addition produces a qualitative, not incremental, improvement.

## 6. Perception redefined: action is part of sensing

A robot that cannot tell visually whether a box is fixed can push it lightly and observe: if it moves, increase force; if it does not, update `movable = false` and revise the estimate of its mass and fixation. This is **active perception / sensorimotor inference**: actions are chosen partly for the information they return. Perception is accordingly defined not as passive reconstruction, but as the maintenance of beliefs that are continuously tested by action.

## 7. The robot needs a predictive self model

A robot should continuously know where its hand is, where it is moving, how its joints are moving, which visual changes it caused itself, and what counts as its own body versus the environment. This is more than forward kinematics: it is a *predictive* model that, given a motor command, forecasts the resulting proprioceptive and visual state, and compares the forecast with reality. The residual drives belief updates. Robotic research has demonstrated that a robot can learn its own morphology and dynamics from vision and use the learned model for motion planning — a self model need not be fully hand-engineered.

## 8. Three world models, plus a contact state

### Model A — Fast visual dynamics (50–200 Hz)

Contrast, optical flow, motion boundaries, looming, local depth change, ego-motion residuals, unexpected motion. Analogous to the retina and fly motion circuits. It does not care whether something is an apple or an orange — only *where change is occurring*.

### Model B — Body–space model (20–100 Hz)

Camera pose, hand pose, object 3D positions, surfaces, contact geometry, relative trajectories, fusing stereo, learned 3D predictors, point tracking, SLAM, and proprioception. Feed-forward 3D models such as VGGT — which jointly predict camera parameters, depth, point maps, and 3D point tracks — are valuable here, but as **spatial evidence providers**, not as the whole of perception.

### Model C — Interaction world model

The most important layer. Its state is not "objects and poses" but a **potential-interaction graph**: for each object, reachability, grasp options with scores per grasp site (e.g., handle 0.82, body 0.61), moveability, an estimated mass range, support relations, contents (often unknown), and the current relation to the robot (e.g., "hand approaching").

### Contact state — the fourth representation

Once contact is established, the representation itself changes: the system estimates a coupled hand–object–support structure, and the object enters the robot's control system. A grasped tool becomes, functionally, an extension of the body: the self model must be updated so that the effective endpoint, collision geometry, reachability, and force transmission all reflect the tool. This dynamic body extension is the core of tool use, and it has no analogue in a static "grasp pose" representation.

## 9. Where VLA models fit — and where they do not

Vision-language-action (VLA) models are the most visible current route: OpenVLA (7B parameters, ~970k robot episodes), Octo (27M/93M parameters, ~800k episodes, with explicit support for cameras, proprioception, and force/torque inputs and new action spaces), π₀ (VLM plus flow matching for continuous actions across embodiments), π₀.₅ (adding web data, object detections, semantic subtasks, and multi-robot data; demonstrated long-horizon housekeeping in unseen homes), and GR00T N1/N1.5 (similarly combining a vision-language backbone with action generation and learning from human egocentric video).

These systems solve: *given this image and instruction, what action distribution is plausible?* What a robot ultimately needs is different: *a causal understanding of itself, the object, and the consequences of acting.* Latent world models such as V-JEPA 2 — which learn video dynamics in latent space and have demonstrated zero-shot robot planning — point at the missing piece: the ability to ask "if my hand moves 5 cm left, what happens?", roll out candidate actions, and select by predicted outcome (a world-model/MPC structure).

**Recommendation:** a VLA should not be the whole robot brain. Its best role is as a **semantic skill generator**: given the current interaction graph, a language goal, and visual semantic features, it outputs interaction primitives — `grasp(handle)`, `rotate(cap)`, `push(drawer)`, `insert(peg, hole)` — which a sensorimotor layer then executes and corrects. The successes of π₀, π₀.₅, and GR00T demonstrate that VLAs are strong general priors; they also demonstrate the importance of heterogeneous sensory/action data, subtask structure, and embodiment information — precisely the things the layered architecture supplies.

## 10. Two time scales, and skills as contact-event sequences

The architecture separates into two systems, mirroring animals:

- **Slow system (intent/semantics, ~1–10 Hz):** VLM/VLA/LLM decomposes goals into subtask sequences ("put the cup in the box" → find cup → grasp handle → lift → move → release) and maintains task-level context.
- **Fast system (sensorimotor, ~50–1000 Hz):** executes approach and contact under continuous feedback — the target moved, correct; contact made, decelerate; pressure insufficient, increase force; slip detected, raise grip force; object struck the box edge, comply.

Animal dexterity comes mostly from the second layer.

Correspondingly, manipulation should not be represented as one long trajectory. A skill is better defined as a **sequence of contact events with expected sensory signatures**: a goal relation to establish ("stable contact with handle"), expected events (visual distance decreases; contact = true; normal force rises; relative hand–object motion ≈ 0), and controllers (visual servoing, impedance, grip-force control). If the expected events do not occur, the belief — not just the trajectory — is re-estimated immediately. Human manipulation research supports this view: actions are segmented by contact events, and each contact event is simultaneously an action outcome and a piece of sensory evidence.

## 11. Worked example: picking up a screwdriver

1. **Perception:** a long, thin object is segmented; the semantic system labels it "possibly screwdriver" — but the manipulation system does not require the label to be certain. It extracts an axis, a handle region, a tip, and surfaces, and forms an interaction belief.
2. **Phase 1 — visual closed-loop approach:** the hand moves under visual servoing; the system predicts the visual change and compares it with observation; discrepancies immediately revise the target.
3. **Phase 2 — pre-contact:** below ~2 cm distance, control switches toward contact-anticipating gains and speeds.
4. **Phase 3 — contact:** fingertip tactile signals provide new evidence ("the object surface is actually here"), correcting the visual pose belief.
5. **Phase 4 — grasp:** fingers close; the robot lifts 1 cm and tests the prediction that the object will follow. If it does not, the grasp has failed and is re-attempted with an updated belief.
6. **Phase 5 — physics identification:** from force/torque transients, mass is estimated; from small lateral perturbations, compliance; from slip, friction.
7. **Phase 6 — tool incorporation:** the self model is updated — the effective endpoint is now the screwdriver tip, not the hand, and subsequent visual control is referenced to the tip. This update *is* the essence of tool use.

## 12. Engineering the vision stack

- **Layer 1 — structured front-end, no large model:** contrast, temporal filtering, optical flow, and looming computed by a lightweight, fly-inspired front-end that can run at 100–200 Hz cheaply. Anomalous change defines an attention region of interest; only then is heavy perception invoked. Running SAM/VLM on every full frame is neither necessary nor affordable.
- **Layer 2 — object-centric perception on demand:** within the attention region, detection/grounding (e.g., RF-DETR, GroundingDINO-class models) plus segmentation (SAM-class) plus stereo/depth yields a 3D object; geometric features — lines, planes, surfaces, axes, edges, handles, openings, contact regions — are extracted as **action geometry primitives**, complementing rather than replacing learned perception.
- **Depth is not the core state.** Absolute depth matters less than relative, body-referenced quantities. The fast control loop should operate on ego-centric/body-centric representations; world-centric representations should be retained in parallel for memory, navigation, task planning, and object permanence.
- **Two resolutions of world:** a low-precision global world (table, chair, cup, drawer, robot — sufficient for planning and permanence) and a high-precision active workspace (current hand, target object, nearby obstacles, contacted objects, tool) maintained at millimeter-to-centimeter fidelity. This split greatly reduces computation.
- **Prediction-error-driven attention:** the system predicts the next observation; if the error is small, nothing is re-perceived; if large, attention, high-resolution perception, object-belief update, and replanning are triggered in cascade. This is a robotic form of predictive coding. It is close in spirit to predictive processing, active inference, sensorimotor-contingency theory, and enactive perception — but engineering value is obtained by implementing belief + forward prediction + prediction error + belief update directly, without committing to a full free-energy-principle implementation.

## 13. Functional correspondence with biology

The mapping is functional, not anatomical mimicry:

| Biological function | Robotic counterpart |
|---|---|
| Retina | Contrast / temporal filtering |
| T4/T5 motion circuits | Optical flow / motion detection |
| Optic-flow integration | Ego-motion estimation |
| Proprioception | Encoders / IMU / joint torque |
| Tactile afferents | Fingertip / contact sensors |
| Spinal reflexes | Local force / grip loops |
| Cerebellar-like prediction | Forward dynamics model |
| Dorsal vision | Reach/grasp geometry |
| Ventral vision | VLM / object semantics |
| Motor cortex | Skill / action policies |
| High-level cognition | VLM/LLM planner |

The governing principle: **do not put everything into one neural network. Biology does not work that way either.**

## 14. The core latent state: interaction belief

The central state variable of the architecture is an **interaction belief** that continuously answers: Who am I (body state)? What am I doing? Where is my hand? Where is the target? What is my current relation to it? What is the current contact relation? What do I predict will happen next? What actually happened? Where does reality disagree with prediction? This is a substantially richer and more manipulation-relevant state than the image-plus-language conditioning used by most current VLA systems.

## 15. Training: learn from the robot's own sensorimotor stream

Training should target *prediction of interaction outcomes*, not world recognition in the abstract. A robot that continually looks, reaches, touches, pushes, pulls, grasps, lifts, rotates, and releases generates a stream of (state, action, outcome) triples that require no human annotation. The core loss is prediction error over sensory and physical consequences, not only action imitation. This addresses a structural weakness of the VLA route — its dependence on large volumes of expert teleoperation data. Even small exploratory actions (move wrist, touch object, push, release) are valid training data, and a robot produces them all day.

Imitation learning retains a role as a **skill prior**: Diffusion Policy demonstrated the strength of action-distribution modeling for manipulation across benchmarks, and RVT-2 showed that an explicit 3D manipulation representation reaches fine manipulation with few demonstrations. In this architecture, imitation supplies priors over *how skills look*; self-supervised sensorimotor learning supplies *what actions cause*.

## 16. Novel objects, and what "physical intelligence" means

Confronted with an unseen object, a label-driven system asks "have I seen this before?" The interaction-driven system asks "what structure does it have?" — cylindrical, rigid, graspable, rotatable, connected to another body — and then *tests*: a structure that affords rotation about an axis is inferred to be a knob-like control by acting on it. Function is inferred from structure plus interaction, not from a label alone.

Physical intelligence is accordingly defined not as bigger perception or bigger action models, but as the learned, closed-loop coupling among body, action, and environmental consequence. Insects, rodents, humans, and robots fit one framework — belief (self + world + goal) → prediction → expected sensation → action and attention → body acts on world → sensation (vision/proprioception/touch) → prediction error → belief update — differing mainly in belief complexity, memory length, action repertoire, and abstraction capacity. The closed-loop principle itself appears conserved.

## 17. Proposed stack and first experiments

A concrete five-layer "bio-manipulation stack":

| Layer | Rate | Contents |
|---|---|---|
| L0 — Reflex | ~1 kHz | Joint torque, impedance, force, slip, collision responses |
| L1 — Sensorimotor | 50–200 Hz | Optic flow, hand/object tracking, visual servoing, contact events |
| L2 — Interaction state | 20–50 Hz | Objects, affordances, relations, contacts, physical beliefs |
| L3 — Skill | 5–20 Hz | Reach, grasp, push, pull, rotate, insert, tool use |
| L4 — Cognitive | 1–5 Hz | VLM/VLA, task graph, goals, reasoning |

A dexterous hand is not required to validate the core ideas: a 7-DoF arm with a two-finger gripper suffices for an initial primitive set (reach, touch, push, pull, grasp, lift, rotate).

**Experiment 1 — open-ended tabletop exploration.** On a table: a cup, a block, a bottle, a sponge, a hammer, and one unknown object; no CAD models. The instruction is simply "explore these objects," using look/touch/push/grasp/lift/rotate. The system incrementally builds object beliefs (movable = yes; mass ≈ 300 g; rigid = yes; grasp locations; friction). A follow-up instruction — "put the objects that can be picked up into the box" — then tests whether the acquired beliefs support task execution. This is a strong research benchmark for the whole architecture.

**Experiment 2 — tool discovery.** The robot is given a stick, a hammer, a scraper, and a hook, with no tool labels, and a goal it cannot reach directly ("bring the distant object here"). Success requires discovering, through interaction, that an object extends its effective reach — i.e., updating the self model from "hand endpoint" to "tool-tip endpoint." Achieving this reliably would be more scientifically valuable than training another generic VLA.

---

# Part II — Whole-Body Contact Intelligence: Climbing and Obstacle Traversal

## 18. Climbing is contact planning first, motion generation second

Whole-body climbing, vaulting over obstacles, squeezing through gaps, bracing against walls, and contacting the environment with hands, knees, hips, and forearms suit the framework of Part I even better than gripper manipulation, because their essence is not generating a graceful trajectory but **continuously establishing, releasing, and transferring contact relations between the body and the environment**.

Consider a human climbing onto an 80 cm platform. The process decomposes into a contact chain: approach → judge that the height exceeds leg-lift range → judge that a hand can reach the top edge → right-hand contact → confirm the contact is reliable → left-hand contact → shift the body forward → lift the right foot → knee/foot contact with the platform → move the center of mass onto the platform → progressively unload the hands → stand up. Formally, the robot passes through contact states C₀ → C₁ → … → Cₙ, e.g.:

- C₀ = {LFoot, RFoot}
- C₁ = {LFoot, RFoot, RHand}
- C₂ = {LFoot, RFoot, RHand, LHand}
- C₃ = {RFoot, RHand, LHand, LKnee}

**Climbing is first a contact-planning problem, and only then a motion-generation problem.** This decomposition is empirically supported: WoCoCo decomposes whole-body humanoid tasks into sequential contact stages and demonstrated cliffside climbing, parkour jumping, and box loco-manipulation without a motion prior.

## 19. The role of a behavioral foundation model (BFM)

A pretrained behavioral foundation model — BFM-Zero (LeCAR Lab) is the reference example; it supports test-time behavior optimization via state rewards, including locomotion, arm control, body height, and skill composition — supplies exactly what happens *inside* a contact stage: given a target body state or reward, it produces stable, continuous, natural whole-body motion, including balance and posture transitions. The pipeline that this report argues for is therefore:

> Vision → environmental geometry → contactable regions (affordance) → contact planner → next body–environment relation → BFM reward/target → BFM → joint action

The BFM is **not** responsible for deciding how to climb. Its job: given the next intended body state and contact relation, achieve it stably and naturally.

**Do not hand the BFM a complete target pose.** Feeding vision → full-body pose → BFM degrades the system into motion imitation. Instead, give the BFM *sparse body–environment constraints*, for example:

- right_hand: target = obstacle.edge_1, contact = true
- pelvis: height > 0.65 m
- COM: forward progress > 0.15 m
- left_foot: maintain_contact = true
- right_foot: free
- torso: uprightness > 0.4
- collision: forbidden = head

with a composed reward R = w₁·R(hand contact) + w₂·R(COM) + w₃·R(pelvis) + w₄·R(stability) + w₅·R(collision avoidance). The BFM finds the intervening whole-body motion itself. Sparse relational goals generalize far better than hard-specified joint targets.

## 20. Body affordance and the contact map

The affordance concept of Part I extends from grippers to the whole body. Where a gripper affordance reads "handle → graspable, button → pushable, lid → rotatable," a body affordance reads:

- ledge → hand-graspable, forearm-supportable
- platform → foot-supportable, knee-supportable
- wall → hand-supportable, shoulder-contactable
- gap → jumpable; bar → hangable; low obstacle → vaultable; opening → crawlable

Formally, affordance is a function A(p, b) of an environmental point/feature p and a body part b — e.g., A(edge, RHand) = 0.92, A(surface, RFoot) = 0.85, A(surface, Knee) = 0.76. Animals, on this view, do not primarily see "a 0.82 m × 0.4 m × 1.2 m box"; they see *what can be stepped on, grabbed, and braced against*.

Perception should therefore output not a terrain heightmap — the standard of perceptive locomotion (depth → heightmap → footsteps), which suffices for walking but not for climbing — but a **whole-body contact map**: a set of geometric features, each carrying a normal, a height, an area, a friction belief, and per-body-part affordance scores (e.g., surface_01: normal [0,0,1], height 0.72 m, friction belief medium, foot support 0.88, knee support 0.79, hand support 0.91, elbow support 0.55; edge_03: grasp scores left hand 0.84 / right hand 0.91, pull direction [−0.3, 0, 0.95]).

It is also unnecessary to begin by classifying obstacle *categories* (box, wall, step, rock). Extracting planes, edges, surfaces, and free space, then judging affordance from geometry — horizontal surface → foot support; vertical edge → hand support/grasp; slope → crawl/step; narrow gap → squeeze; overhang → hang — is both simpler and more general. These are the same line/junction/plane geometric primitives as in Part I, now serving as whole-body action geometry.

## 21. Whole-body interaction belief and the contact graph

The core state generalizes Part I's interaction belief:

**B^WB = [Self, Environment, Contacts, Dynamics, Goal]**

- **Self:** joint positions/velocities, IMU, COM, momentum; per-limb reachability; body collision geometry.
- **Environment:** not a full mesh — only nearby planes, edges, surfaces, gaps, and free space.
- **Contacts:** the current contact set with forces (e.g., LFoot on surface_A at 62 N; RFoot on surface_A at 71 N; RHand on edge_B at 34 N; LHand free).
- **Dynamics:** slip probability, friction, support stiffness, surface motion.
- **Goal:** e.g., pelvis above the obstacle, forward velocity, final stance stable.

Climbing is then the evolution of a **contact graph** G_t = (BodyParts, Surfaces, Contacts): stage 0, feet↔ground; stage 1, feet↔ground + hands↔obstacle; stage 2, one foot↔obstacle + hands↔obstacle + one foot↔ground; stage 3, feet↔obstacle + hands↔obstacle; stage 4, feet↔obstacle and stand. The high-level planner plans only the sequence G₀ → G₁ → …; everything else is delegated to the BFM.

The dimensionality argument is decisive: direct trajectory planning searches over q₁:ₜ with tens of degrees of freedom × hundreds of timesteps (≈ 30 × 500 = 15,000 dimensions), whereas a contact graph transition is specified by a handful of relations (RHand→edge1, LHand→edge2, RFoot→platform, pelvis→above platform) — tens of dimensions or fewer — with the BFM mapping contact goals to whole-body motion.

## 22. State of the art (2025–2026)

Recent results show the field converging on perception-driven whole-body skills:

- **Light-Loco-Parkour:** a single perceptive whole-body policy using only onboard depth and a velocity command autonomously selects walking, balancing, climbing, stepping down, and vaulting — no runtime motion graph, skill labels, or hard-coded gates — with zero-shot generalization to real robots indoors and outdoors.
- **Perceptive Humanoid Parkour (PHP):** motion matching composes human atomic skills into a motion-tracking RL expert, distilled into a depth-based student; on a Unitree G1 it climbed a 1.25 m obstacle — about 96% of the robot's height — and adapts in real time over long obstacle courses.
- **WholeBodyLocomotion:** a motion generator + RL tracker + onboard perception stack achieving box climbing, vaulting, stairs, and mixed terrain on real hardware.
- **Humanoid Parkour Learning:** end-to-end vision-based whole-body control in which the humanoid autonomously selects crossing motions without a motion prior.

The architecture proposed here agrees with this trajectory (planner/generator + tracker) but pushes one step further: most current systems run Depth → Motion → Tracker, whereas the proposal is **Perception → Affordance → Contact Graph → BFM**, with prediction error closing the loop (Section 23).

## 23. Event-based control: prediction error instead of time scripts

For sim-to-real transfer this distinction is critical. A *time-scripted* motion ("at t = 0.8 s the right hand should be here; at t = 1.2 s the leg moves; at t = 1.8 s the pelvis rises") fails wholesale if friction differs, the obstacle is displaced by 4 cm, a hand slips, or the body collides en route. An *event-based* state machine — establish right-hand contact → contact confirmed → establish left-hand contact → load-bearing confirmed → lift right leg — is indifferent to timing; what matters is the event.

Concretely: motion "phase" should be defined by contact/event state, not by phase = t/T. Phase 1 ends when RHandContact = true **and** force > F_min; phase 2 loads the right arm until F_hand > F_support; only then is the leg lifted. If the BFM executes a reach and the predicted contact does not occur, the system stops, looks again, updates the edge pose, and reaches again — the same predict → act → observe → error → update-belief loop as Part I, applied to whole-body locomotion.

In this framing the BFM becomes a **contact-conditioned motion solver**: input (current state, contact goal, motion goal), output joint action. Given a goal such as "right-hand contact with edge_1 = true; head height > 0.6 m; COM forward +0.15 m; left-foot contact = true; stability = true," the BFM itself resolves waist rotation, knee flexion, contralateral arm swing, and COM adjustment — the real value of a foundation behavior prior.

Equally important is what a BFM *cannot* do alone: it does not know where the right hand should grab, when to start climbing, or whether a surface will slip. Without perception, affordance, and contact-planning layers above it, one has a body with rich motion ability that does not know how to use its environment.

## 24. Control rates

| Tier | Rate | Responsibility |
|---|---|---|
| Motor / BFM control | ~1000 Hz | q, q̇, τ, IMU; balance and force control |
| Contact manager | 50–100 Hz | Contact state, force, slip, COM, reachability |
| Vision + planner | 10–30 Hz | Geometry, contact candidates, next contact selection |
| VLM | 1–5 Hz | Strategy-level judgments: climb? crawl? is this surface probably fragile? |

Large models must not enter the fast loop. After contact, vision recedes: if vision reports hand contact but joint torque implies F ≈ 0, the hand is not load-bearing; if F_t/F_n approaches the friction limit μ, slip risk is high and the fast layer — not a planner — responds immediately: increase normal force, change contact, lower the COM, or cancel the leg lift.

## 25. Worked example: climbing a 0.60 m box

1. Vision measures h = 0.60 m; nominal step capability h_step ≈ 0.25 m → normal walking is not viable.
2. Affordance evaluation: top surface is foot-supportable; top edge is hand-supportable → the planner issues contact goal C₁: RHand → edge.
3. The BFM executes Reach(RHand, edge) while keeping both feet stable.
4. Contact is detected, but force < 10 N — not yet load-bearing → shift the COM forward.
5. Arm force reaches F = 35 N → support confirmed.
6. The planner issues RFoot → top; the BFM automatically bends the knee, rotates the waist, lifts the leg, loads the arm, and maintains balance.
7. Foot contact with force above threshold.
8. Load transfer: hand → foot.
9. Both feet on top; hands released; the BFM returns to upright locomotion.

No full trajectory was ever planned.

## 26. One formalism for many behaviors — including falls

Step-over (low obstacle), hand-supported vault (medium), climb (high), jump + hand catch + pull (very high), crouch/crawl (narrow gap), grab + swing (bar) are all transitions from a current contact graph to a goal contact graph; no separate policy per obstacle type is required. This is the same reason a single parkour policy can switch among walk/balance/climb/step-down/vault.

The formalism also rehabilitates "failure" contacts. Conventional humanoids treat torso, knee, or hand ground contact as failure. Animals and humans kneel, lie prone, sit, brace, roll, and lean. Research on full-body ground contacts (Embrace Contacts) studies exactly this: real human motion heavily exploits extra body contacts. The conceptual change: **intentional contact ≠ collision**, and body collision should not be uniformly penalized.

Robots should therefore define **contactable body surfaces** — palm, forearm, elbow, knee, shin, foot, hip, back, shoulder — each with a contact capability profile: maximum force, preferred direction, friction, damage risk, compliance (palm: grasp/support; forearm: support/sliding; knee: support; back: lean/support; head: forbidden). Combining body surfaces {b₁…bₙ} with environment features {e₁…eₘ} yields a **body affordance map**, a matrix A_ij = Affordance(b_i, e_j) over which the planner searches for feasible contacts. An illustrative matrix (rows: body part; columns: edge / top surface / wall):

| Body part | Edge | Top | Wall |
|---|---|---|---|
| Palm | 0.94 | 0.82 | 0.73 |
| Foot | 0.21 | 0.96 | 0.05 |
| Knee | 0.15 | 0.83 | 0.30 |
| Forearm | 0.73 | 0.68 | 0.84 |
| Back | 0.01 | 0.32 | 0.77 |

Finally, the affordance model should be **learned about the robot's own body**, not only hard-coded: by testing Reach(b_i, p) and measuring achievable contact forces, the robot builds a *self affordance model* — it comes to understand what its own body parts can do, in the same terms as it understands the environment.

## 27. Emergent strategy discovery

With a self model plus affordance map, strategies need not be hand-coded rules. Facing a 0.90 m platform: the planner tries foot → top and finds it unreachable per the self model; hand → edge is reachable; once the hand contact is established, the new body configuration raises pelvis height; foot → top is recomputed and is now reachable. "Grab first, then step" *emerges* from search over the affordance matrix — replacing programmer rules of the form `if height > 0.6: use_hand()`.

## 28. Training curriculum

End-to-end training on arbitrary obstacles is not advisable. Four stages:

**Stage 1 — BFM contact primitives (no vision; exact simulator geometry).** Train two families of primitives — Reach(body part, target) and MaintainContact(body part, target) — across eight canonical relations: hand-touch, hand-support, hand-pull, foot-step, foot-push, knee-support, forearm-support, body-lean. Only body-part ↔ environment relations are trained, not "climbing." The single most important skill is **load transfer** (feet → hands+feet → hands+knee → feet): the robot must learn to shift weight from legs to arms, trained with a dedicated reward on hand force targets or on COM position relative to the support polygon / contact wrench cone.

**Stage 2 — Contact sequences.** In the manner of WoCoCo, train transitions C_i → C_{i+1} over given sequences (feet-ground → feet-ground + RHand-wall → feet-ground + both-hands-wall → both-hands-wall + RFoot-platform → both-feet-platform), rather than whole climbs. Sequences can be auto-generated.

**Stage 3 — Geometry randomization.** Domain-randomize height, width, slope, edge shape, friction, surface, compliance, and position (e.g., box height h = 0.2–1.0 m). The robot must adapt its strategy to geometry: Geometry → Contact Strategy.

**Stage 4 — Vision last.** Only now add depth/RGB → geometry, starting with depth alone. The end-to-end alternative (depth → BFM) is demonstrably viable (Humanoid Parkour Learning), but depth → contact features → contact planner is preferable for interpretability and debuggability.

**First-version vision can be deliberately small:** depth input at 64×64 or 128×128; classical or lightweight computation of surface planes, edges, normals, clearance, and reachability; output N×K contact candidates, each with position, normal, size, body part, confidence, and reachability, from which the planner selects. RGB semantics come later and serve as a *physical prior* — glass lowers support confidence; a metal railing raises grasp confidence; a curtain implies low load-bearing — which is the one place a VLM adds clear value, and still not as an action generator.

## 29. System architecture and distillation policy

**Teacher pipeline:** perfect simulator geometry → contact candidate generator → contact planner (heuristics / search / RL) → contact goal → BFM → robot action, with contact/body state fed back to the planner. **Student:** a network mapping (depth + proprioception + goal) → (contact goal / BFM prompt), distilled from the planner first; only if needed, a further compression to (depth + proprioception) → BFM latent. This mirrors the recent parkour pipeline pattern (skill composition → tracking expert → DAgger + RL distillation into a depth-based multi-skill student).

**Do not distill the BFM away prematurely.** The BFM is the stability insurance layer; the component actually being trained is the contact planner. Distilling planner + BFM into one student is appropriate only once the system is mature — otherwise, when something fails, it is impossible to attribute the failure to perception, contact choice, motion, balance, or dynamics.

## 30. Benchmarks and rewards

**Stage-1 benchmark — five geometries only** (no outdoor testing), all with parameter randomization:

1. Box climb, 0.2–0.8 m.
2. High wall/ledge (hand grasp + pull + foot support).
3. Vault (hand-supported).
4. Low tunnel (crouch / knee-and-hand crawl).
5. Gap / stepping stones (balance + reach/contact).

The success criterion is architectural: *one* policy/planner decides walk / step / vault / climb / crawl from geometry alone, with no human-supplied skill labels.

**Stage-2 benchmark — arbitrary obstacles:** randomly generated boxes, steps, bars, walls, holes, slopes, narrow paths, and overhangs, never trained by category. The planner sees only geometry + affordance; the goal is given as a pelvis target ("get over there"); the robot chooses the contact sequence itself.

**Rewards should stay generic.** For planner + BFM, a single core reward suffices:

R = R_progress + R_contact + R_stability + R_goal − R_risk,

with R_progress = d_{t−1}(goal) − d_t(goal); R_contact rewarding establishment of the intended contact; R_stability a function of COM, momentum, and the contact set; R_risk penalizing unintended collision, slip, joint limits, and excessive torque. Per-skill rewards (climbing_reward, vault_reward, crawl_reward) should be explicitly avoided — they reintroduce human-defined skills through the back door.

**Next modeling step — a contact forward model.** A learned model F_θ(B_t, C_next) → B̂_{t+H} predicts the state resulting from a candidate next contact, enabling candidate comparison before execution — e.g., C₁ = RHand(edge A) vs. C₂ = LHand(edge B), scored by predicted foot reachability and stability, choosing C* = argmax_C P(success | B_t, C). This approaches genuine world-model planning over contacts.

**Active whole-body perception.** If the robot cannot see the top of a platform, it can raise its head, or place a hand on the edge and lift its body, to gain a new camera viewpoint — action improving perception, the same animal visual closed loop as in Part I.

## 31. Research positioning

The resulting research direction can be named **Perceptive Whole-Body Contact Intelligence**: neither "humanoid locomotion" nor "humanoid parkour imitation," but the study of how a robot learns *where, when, and with which body part to contact the environment*, while a foundation behavior model solves *how to move*. The full system:

> Goal ("get over this obstacle") → local 3D perception (depth/stereo/RGB) → surfaces / edges / free space → whole-body affordance map → contact graph planner ("what contact next?") → contact goal → BFM (stability / transitions / motion) → robot → sensing (vision / IMU / joint and contact sensing) → interaction belief (prediction vs. reality) → back to the contact graph planner.

The five questions that deserve the research effort are: How should the environment be represented? How does the robot discover where contact is possible? Which body part should make contact? After contact, how is its reliability confirmed? How is the next contact chosen? A BFM converts the answers — sparse interaction intentions — into stable, continuous, natural whole-body motion. The problem is thereby transformed from *Vision → 30-DoF motion* into *Vision → Contact strategy → BFM*.

The same language covers far more than climbing: standing, walking, parkour, fall recovery, crawling, door pushing, box carrying, wall bracing, bimanual manipulation, and tool use are all describable as continuous change in the relations among body, environment, and contact. **Their common language is not "motion," but contact.**

---

## References (as cited in the source discussion)

- FlyVis / Drosophila connectome-constrained vision models; NeuroMechFly v2 (closed-loop vision–olfaction–motor-feedback simulation), *Nature* (2024–2025).
- Mouse V1 joint optic-flow/running-speed modulation study, *Nature*.
- OmniManip — object-centric interaction primitives for manipulation (arXiv).
- VGGT — feed-forward 3D reconstruction and point tracking (arXiv).
- OpenVLA (openvla.github.io); Octo (octo-models.github.io); π₀ and π₀.₅ (arXiv; PMLR); GR00T N1/N1.5 (NVIDIA Research).
- V-JEPA 2 (Meta AI) — latent video world model with zero-shot robot planning.
- Diffusion Policy (diffusion-policy.cs.columbia.edu); RVT-2 (GitHub).
- BFM-Zero — *A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning* (LeCAR Lab; github.com/LeCAR-Lab/BFM-Zero).
- WoCoCo — *Learning Whole-Body Humanoid Control with Sequential Contacts* (PMLR v270, zhang25a).
- Light-Loco-Parkour (arXiv, as cited: 2608.02653); Perceptive Humanoid Parkour (arXiv, as cited: 2602.15827); WholeBodyLocomotion (wholebodylocomotion.github.io); Humanoid Parkour Learning (PMLR v270, zhuang25a); Embrace Contacts — humanoid shadowing with full-body ground contacts (PMLR v305, zhuang25b).

## Notes on this report

- This report is an objective reorganization of a research discussion. All references to specific companies, products, internal platforms, and any particular team's existing assets have been removed or generalized (e.g., "a behavioral foundation model" in place of any claim of possession); the technical content is presented as generally applicable research analysis.
- Quantitative values (frequencies, forces, affordance scores, episode counts) are carried over from the source discussion. Bibliographic details — in particular the arXiv identifiers of the two 2026 parkour papers — are reproduced as cited in the source and were not independently re-verified for this report.
