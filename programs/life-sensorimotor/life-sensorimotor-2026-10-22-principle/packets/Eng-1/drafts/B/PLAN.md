# Eng-1 B — Minimal spike PLAN v1

Status: SEALED; deferred-runnable; no experiment executed. Author B, 2026-10-22.
Question: can a finite-horizon envelope certificate remain checkable with coupled dynamics, delayed observations, actuator memory/limits and an explicit mode reset?

## Scope, execution and seal

Only the assigned experiment runner executes after recommendation. This author supplies PLAN only. Before running, verify PLAN.sha256, implement run_spike.py and checker.py under packets/Eng-1/drafts/B/spike/, and seal their hashes and environment in RUN-SEAL.json. All artifacts remain in that directory under /srv/claude. No network, package installation, GPU or hardware. Use installed numerical tools or standard-library arithmetic. Budget: 15 CPU minutes and 1 GiB; exhaustion yields INCOMPLETE, never PASS. Implementation work is not represented as already complete.

Do not edit this plan after a run. Scientific changes require PLAN-v2.md, a new seal and retention of original failures. Optimization may change computation, not the declared sets or decision rules. Tests concern C-Eng1-B-01..03, engineering hypotheses only. D-P1-001 remains Provisional acceptance-gate; no ladder edge gates execution.

## Frozen fixture

Normalized units, synthetic parameters, not target measurements. h=0.001 s, N=200 (0.2 s). This exact discrete recurrence defines the plant; it is not a certified discretization of continuous dynamics:

    x[k+1] = A[m[k]] x[k] + h a[k] + h d[k]
    a[k+1] = 0.5 a[k] + 0.5 v[k]
    v[k] = clip(-K (x[k-j] + n[k]), -2, 2)

A[0]=[[1.0033,0.0004],[0.0002,1.0100]];
A[1]=[[1.0060,-0.0003],[0.0005,1.0080]];
K=diag(20,30). All decimal constants are exact fixture inputs. Clip is componentwise. Applied effort is a; command is v. Initial x[0] lies in [-0.002,0.002]^2; a[0]=0. Every historical x[k], k<0, equals the SAME x[0]. Disturbance d[k] lies in [-0.05,0.05]^2; measurement noise n[k] in [-0.0001,0.0001]^2, independently selectable at each step. These are Cartesian sets, not probabilistic assumptions. Required state envelope: |x_i|<=0.02; command/applied-effort limits: |v_i|,|a_i|<=2.

Sixteen cells: j in {2,5,10,20}, crossed with four mode schedules: all 0, all 1, 0→1 at k=100, 1→0 at k=100. At a transition only, replace x[100] by R x[100]+r, with R=[[1,0.1],[0,1]] and r in [-0.001,0.001]^2. Preserve actuator and prior observation history. Apply reset before the k=100 command and state step; future delayed observations of x[100] use its post-reset value. Check/log both pre-reset and post-reset states. No reset in fixed schedules. Arbitrary switching is outside the admitted language.

Controller receives only delayed noisy x. It receives no mode, reset or disturbance truth. Same fixed K in all cells. The mode schedule is an evaluator premise, not a demonstrated contact-mode estimator. j*h denotes observation age, not total effective latency or the common-input interval of C-P1-001. Log observation time, command issue and a separately. No continuous intersample or infinite-horizon guarantee is sought.

## Certificate algorithm

Augment the state with a and delayed x history. Temporarily remove clip, making the system affine linear for each declared schedule. Propagate center and labeled generators for x[0], each d[k], each n[k], and reset r. Keep generator identities through resets/history; do not replace correlated histories with independent copies. Coordinate support is c_i +/- sum_l |G_il|. This is exact in real arithmetic for affine images of the admitted boxes. No generator truncation or statistical sampling in the certificate path.

Bound x, a and pre-clip v at every step. If all state/effort bounds hold and pre-clip commands remain in [-2,2], saturation is inactive throughout and the affine certificate applies to the clipped controller. Otherwise do not certify: command-bound excess yields UNRESOLVED_SATURATION. Enclosure crossing alone is not an actual violation of a nonlinear clipped system.

Serialize exact model coefficients, uncertainty sets, controller, schedule, delay, hashes, recurrence and bounds. checker.py independently reconstructs the recurrence from inputs, without trusting producer extrema. Use exact rational arithmetic or outward-rounded interval arithmetic with at least 50 decimal digits and directed rounding at EACH operation. A float epsilon added afterward does not qualify. Budget overruns or unresolved arithmetic are explicit unresolved/incomplete results.

When unsaturated support exceeds the state envelope, choose each generator sign to maximize that coordinate at the offending time. Replay the resulting concrete initial state, disturbances and noise in the clipped recurrence with verified arithmetic. Only an actual in-set replay violation earns WITNESS_VIOLATION; otherwise unresolved. Verify all witness inputs and mode transitions belong to the contract. A valid certificate is finite-model sufficiency, not an independent B.9 proof of any necessity claim.

## Controls, audit and mutations

1. Positive control: scalar x[k+1]=0.9*x[k]+w[k], |x[0]|<=0.002, |w[k]|<=0.0001, envelope 0.02, N=200. Must certify; exact bound is 0.9^k*0.002+0.001*(1-0.9^k).
2. Negative control: scalar x[k+1]=x[k]+w[k], x[0]=0, |w[k]|<=0.001, envelope 0.02. All-positive w violates at k=21. Must reject certification and verify witness.
3. Change j in a serialized certificate without regenerating it. Checker must reject hash/recurrence mismatch.
4. Copy a fixed-mode certificate into a transition scenario with reset omitted. Checker must reject, regardless of a nominal rollout's behavior.
5. Feed a controller-input record containing mode/reset/disturbance truth. Interface audit must reject that record.
6. Authority stress: repeat all-0, j=2 with command/applied-effort limits 0.01 and clip adjusted accordingly. Report a valid certificate, verified clipped violation or unresolved saturation honestly; no required failure and no claim that delay alone suffices.
7. Submit a two-transition schedule or enlarged disturbance set under an existing certificate ID. Must return OUT_OF_SCOPE.

Supplementary rollouts: seeds {11,23,47}, one rollout per seed per nominal cell and authority-stress cell. Sample initial/d/noise/reset components uniformly within their sets; log generator and seed. They cannot certify a set or rescue a failed certificate.

## Outputs and frozen verdict

verdict.json fields: plan_hash, implementation_hashes, environment, elapsed_seconds, resource_limits, controls, cells, mutations, harness_verdict, engineering_outcome, limitations. Each cell records schedule, j, contract_hash, status, worst_state_bound, worst_effort_bound, first_violation_step if any, witness_path if any, arithmetic_method and checker_result. Preserve producer/checker logs and all failures.

Cell statuses: VERIFIED_MODEL_CERTIFICATE, WITNESS_VIOLATION, UNRESOLVED_SATURATION, UNRESOLVED_NUMERICS, OUT_OF_SCOPE, INCOMPLETE. No averaged score.

Harness PASS requires correct analytic controls, correct rejection in tests 3/4/5/7, traceable outcomes for all 16 cells and authority stress, and independent verification of every claimed certificate/witness. Unresolved cells may coexist with harness PASS; false acceptance is FAIL; missing outputs/resource exhaustion is INCOMPLETE.

Engineering SUPPORTED additionally requires at least one verified fixed-mode cell and one verified transition cell at the SAME j. Otherwise NOT_SUPPORTED, or INCOMPLETE if execution incomplete. Publish every cell; do not hide failures behind the minimum passing pair. No interpolation to untested delays/schedules.

C-Eng1-B-01 remains unsupported without that pair; a valid replay violating a claimed certificate falsifies its implementation. C-Eng1-B-02 fails if an incompatible certificate passes. C-Eng1-B-03 fails if timing/applied-effort provenance is missing or evaluator truth reaches feedback. No new necessity counterexample search or claim-state transition is performed.

## Interpretation and handoff

PASS = harness only; never hardware transfer. Results cannot promote grades. Runner files evidence; separate adjudication decides disposition. An unsupported result supports trying S2a or an explicitly amended contract, not silently widening limits or deleting transitions. Target application needs measured model/error sets, timing/actuator characterization, mode/reset validation and envelope-owner ratification. Certificate expiry is finite; concatenation requires an independently checked handoff-state inclusion including actuator/history state.
