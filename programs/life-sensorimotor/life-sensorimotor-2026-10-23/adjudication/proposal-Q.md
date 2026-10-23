# Proposal Q

## Thesis (first lock)

**First lock: S0a, a bounded-response viability contract.** Split S0 into:

- **S0a:** establish which disturbances the body can tolerate, how long correction may be delayed, and who owns that correction.
- **S0b:** select and validate reflex, impedance, or other implementations that satisfy the contract.

The first research packet should certify S0a with a minimal corrective controller. It should not attempt to lock a particular impedance architecture, locomotion policy, or contact representation.

The necessity is conditional but concrete: **when admissible disturbances require incompatible corrections before a deadline, a body whose effective response arrives after that deadline cannot guarantee the specified envelope.** Better locomotion or richer contact semantics cannot repair an already missed physical deadline.

This makes S0a the first **acceptance gate**, not a universal developmental sequence. If existing hardware or control already satisfies it, certify that implementation and advance. Passive mechanics can discharge part or all of the obligation.

S1 locomotion and S2 contact observability remain separate subsequent gates. S0a needs enough feedback to correct body error; it does not require identifying contact state.

**Status:** proposed mainline, provisional pending adjudication and spike. All necessity claims below remain Candidate.

## Necessity argument (Appendix B)

### A narrow Grade-1 candidate

Consider one normalized unstable body mode:

\[
\dot{x}=a x+u+d,\qquad |x|\le b,
\]

with \(a=10\,\mathrm{s}^{-1}\), \(b=0.01\), actuator bound \(|u|\le3\), and \(x(0)=0\).

At \(t=0\), an unobserved disturbance becomes either \(d=+D\) or \(d=-D\), where \(D=1\). Assume the two worlds induce identical applied control until time \(L\). This includes arbitrary predictive or randomized controllers when their available information cannot distinguish the worlds; fix the same random realization in both.

Subtracting their trajectories gives:

\[
x_+(L)-x_-(L)=\frac{2D}{a}(e^{aL}-1).
\]

Both trajectories can belong to \([-b,b]\) only if:

\[
\frac{D}{a}(e^{aL}-1)\le b.
\]

Therefore a necessary condition is:

\[
L\le L^*=\frac{\ln(1+ab/D)}{a}=9.531\text{ ms}.
\]

With a 20 ms interval during which applied control cannot distinguish the disturbances, at least one trajectory has magnitude at least \(0.02214\), exceeding the envelope.

This is an impossibility result for the stated plant, disturbance set, information restriction, and objective. It is independent of controller family. It is **not** a universal humanoid bandwidth theorem.

### What follows—and what does not

The functional obligation is to provide sufficiently prompt disturbance-dependent correction **or** alter the premises through passive stabilization, larger tolerance, reduced disturbances, or predictive information that actually distinguishes the worlds.

A 250 Hz body controller is one implementation candidate. Neither 250 Hz nor an explicit reflex module follows uniquely from the proof. A nominally 50 Hz policy with faster embedded feedback must be assessed using that faster feedback’s effective response.

The ordering argument is consequently:

1. Establish the physical envelope and its response obligation.
2. Demonstrate that some available body mechanism satisfies it.
3. Admit S1/S2 components only within that established envelope.

This justifies a prerequisite gate. It does not prove that research on S1 or S2 must wait, or that their representations are unnecessary.

## Interface contracts

The rates below are proposed engineering budgets, subject to measurement. The scalar proof does not establish robot-specific values.

| Interface | Signals and semantics | Rate / deadline class | Owner |
|---|---|---|---|
| Sensors → body loop | Timestamped joint position/velocity, IMU, available actuator measurements, validity and age; explicit units and frames | Acquisition around 1 kHz; initial body update target 250 Hz; measure total sensor-to-actuator delay | Body loop |
| Body correction → actuators | Bounded commands; applied-command estimate; saturation and execution status | Fast class, ≥200 Hz target; independently enforce certified response deadline | Body loop exclusively |
| Policy → body loop | Bounded reference, timestamp, expiry, requested envelope ID | Approximately 50 Hz; asynchronous to stabilization | S1 policy requests; body loop accepts, clips, or rejects |
| Body loop → policy | Tracking residual, constraint margin where justified, saturation, accepted reference, `valid / degraded / outside-envelope` | Approximately 50 Hz; faults available immediately locally | Body loop owns measurements and enforcement |
| Body loop → Scene Graph | Timestamped body pose/twist estimate with uncertainty and frame; envelope status; optional event observations with provenance | Approximately 20–50 Hz summaries; event-driven updates | Body owns source estimates; Scene Graph owns persistent relations |
| Body loop → Life Core | Capability availability, fault summaries, recovery outcome, envelope version | Slow/event-driven; approximately 1–5 Hz sufficient initially | Life Core owns task decisions, never deadline-critical correction |

Additional rules:

- The interface must distinguish **measured**, **estimated**, and **unavailable** fields.
- A residual or saturation event is not automatically a contact event.
- S0a exports no mandatory contact latent, object identity, or contact relation.
- Expired references invoke a locally validated fallback. “Hold position” is not assumed universally safe.
- Upper-layer interruption must not interrupt the corrective loop.
- Simulator ground truth is evaluator-only. It cannot enter candidate-controller inputs.
- Until whole-body validation exists, exported status means “inside the tested envelope,” not a general safety guarantee.

## Claims table (id, grade, state Candidate/Locked, scope, falsifier)

| ID | Grade | State | Scope and necessity claim | Falsifier / boundary |
|---|---:|---|---|---|
| B-N1 | 1 | Candidate | For the stated scalar plant and indistinguishable disturbance pair, guaranteed invariance requires \(L\le L^*\). | An admissible common applied-control history keeping both trajectories inside the envelope beyond \(L^*\), or an error in the trajectory-separation derivation. |
| B-N2 | 2 | Candidate | For a body envelope containing disturbances with incompatible required corrections, the implementation must realize timely disturbance-dependent correction or an equivalent physical mechanism. | A system satisfying that same envelope without either function; changing the disturbance set or tolerance narrows scope rather than refutes the original premises. |
| B-N3 | 2 | Candidate | If upper-layer stalls can exceed the certified response allowance, the corrective function must remain operational during those stalls. | A system tolerating the stipulated stalls and disturbances despite losing every timely corrective or stabilizing mechanism. Separate software processes are not required. |
| B-N4 | 3 | Candidate | Evolutionary ordering motivates testing stabilization before richer sensorimotor composition. It supplies no obligatory chronology. | Historical revision changes the motivation; successful alternative development defeats any proposed universal-order upgrade. |

B-N1 is eligible for a narrow principle lock after independent proof review. A successful simulator run cannot perform that promotion.

The **implementation decision** may be locked after the prescribed review and spike while B-N2/B-N3 remain Candidate. That distinction must appear in `decision.md`.

## Minimal spike (commands/metrics/pass-fail; sim OK)

**Question:** Can a small body-local corrective loop satisfy the declared envelope, while the analytic bound correctly excludes a controller whose applied action remains uninformed for 20 ms?

This is a CPU-only scalar witness, not a humanoid validation. No training, BFM integration, external packages, or paid compute is required.

**Pre-registration**

- Plant and bounds: exactly those in B-N1.
- Episode length: 250 ms.
- Disturbance: constant \(+1\) or \(-1\), beginning at phase 0, 1, 2, or 3 ms.
- Sensor delay: 0 or 1 ms.
- Integration resolutions: 1 and 0.5 ms; exact integration between command changes.
- Candidate: 250 Hz feedback, \(u=\operatorname{clip}(-200x_{\mathrm{delayed}},-3,3)\).
- Comparators: 50 Hz feedback; no feedback; evaluator-only disturbance oracle.
- All initial states: zero. Broader initial-state coverage is a later gate.
- Record every trajectory, command, sensed state, disturbance, and condition.

**Pass requires all of the following:**

1. Every candidate episode satisfies \(\max_t|x(t)|\le0.01+10^{-10}\).
2. Every oracle episode satisfies the same envelope, confirming available actuation can solve these instances.
3. The phase-zero, zero-delay 50 Hz and no-feedback cases violate the envelope.
4. The measured phase-zero 50 Hz state at 20 ms agrees with the analytic magnitude \(0.0221403\ldots\) within \(10^{-9}\).
5. Candidate peak magnitudes agree across integration resolutions within \(5\times10^{-4}\).
6. Every applied command respects \(|u|\le3\).

The oracle is a diagnostic, not an admissible solution. The 50 Hz comparison illustrates the bound; its failure alone cannot establish necessity.

**Exact deferred execution:** after selection, the experiment runner executes this block from `/srv/claude`. It writes the specification’s complete harness and artifacts under the run root.

```bash
cd /srv/claude
mkdir -p research/life-sensorimotor-2026-10-23/spikes/B
cat > research/life-sensorimotor-2026-10-23/spikes/B/run.py <<'PY'
import csv
import json
import math
from pathlib import Path

out = Path(__file__).resolve().parent
a, D, bound, umax = 10.0, 1.0, 0.01, 3.0
results = []

with (out / "trajectories.csv").open("w", newline="") as f:
    log = csv.writer(f)
    log.writerow(["arm", "dt", "delay", "phase", "sign",
                  "t", "x", "sensed_x", "u", "d"])

    for dt in (0.001, 0.0005):
        rho = math.exp(a * dt)
        gain = math.expm1(a * dt) / a
        for delay in (0.0, 0.001):
            lag = round(delay / dt)
            for phase in (0.0, 0.001, 0.002, 0.003):
                onset = round(phase / dt)
                for sign in (-1, 1):
                    for arm in ("fast", "slow", "blind", "oracle"):
                        period = {
                            "fast": 0.004, "slow": 0.020,
                            "blind": 0.020, "oracle": dt
                        }[arm]
                        stride = round(period / dt)
                        k = (a / (1 - math.exp(-a * period))
                             if arm == "slow" else 200.0)
                        x, u, sensed = 0.0, 0.0, 0.0
                        history = [x]
                        peak, peak_u, x20 = 0.0, 0.0, None

                        for i in range(round(0.250 / dt)):
                            d = sign * D if i >= onset else 0.0
                            if i % stride == 0:
                                sensed = history[max(0, i - lag)]
                                if arm == "blind":
                                    u = 0.0
                                elif arm == "oracle":
                                    u = -200.0 * x - d
                                else:
                                    u = -k * sensed
                                u = max(-umax, min(umax, u))

                            log.writerow([arm, dt, delay, phase, sign,
                                          i * dt, x, sensed, u, d])
                            x = rho * x + gain * (u + d)
                            history.append(x)
                            peak = max(peak, abs(x))
                            peak_u = max(peak_u, abs(u))
                            if i + 1 == round(0.020 / dt):
                                x20 = x

                        log.writerow([arm, dt, delay, phase, sign,
                                      0.250, x, sensed, u, d])
                        results.append(dict(
                            arm=arm, dt=dt, delay=delay, phase=phase,
                            sign=sign, peak=peak, peak_u=peak_u, x20=x20
                        ))

def rows(arm):
    return [r for r in results if r["arm"] == arm]

expected20 = D * math.expm1(a * 0.020) / a
slow_witness = [r for r in rows("slow")
                if r["phase"] == 0 and r["delay"] == 0]
blind_witness = [r for r in rows("blind")
                 if r["phase"] == 0 and r["delay"] == 0]

grid_deltas = []
for r in rows("fast"):
    if r["dt"] != 0.001:
        continue
    mate = next(s for s in rows("fast")
                if s["dt"] == 0.0005
                and all(s[key] == r[key]
                        for key in ("delay", "phase", "sign")))
    grid_deltas.append(abs(r["peak"] - mate["peak"]))

checks = {
    "candidate_envelope":
        all(r["peak"] <= bound + 1e-10 for r in rows("fast")),
    "oracle_feasible":
        all(r["peak"] <= bound + 1e-10 for r in rows("oracle")),
    "slow_witness_fails":
        all(abs(r["x20"]) > bound for r in slow_witness),
    "blind_witness_fails":
        all(abs(r["x20"]) > bound for r in blind_witness),
    "analytic_bound_agrees":
        all(abs(abs(r["x20"]) - expected20) <= 1e-9
            for r in slow_witness),
    "resolution_agrees": max(grid_deltas) <= 5e-4,
    "actuator_bounds": all(r["peak_u"] <= umax for r in results),
}
summary = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "necessary_latency_seconds": math.log1p(a * bound / D) / a,
    "expected_abs_x_at_20ms": expected20,
    "max_grid_peak_difference": max(grid_deltas),
    "cases": results,
}
payload = json.dumps(summary, indent=2)
(out / "metrics.json").write_text(payload + "\n")
print(payload)
raise SystemExit(0 if all(checks.values()) else 1)
PY
python3 research/life-sensorimotor-2026-10-23/spikes/B/run.py
```

**Outcome interpretation:** PASS establishes a sufficient implementation for this finite test set and checks the analytic witness. FAIL rejects this implementation or exposes a harness/proof mismatch; it does not authorize threshold adjustment.

No experiment has been executed for this proposal. If selected but not run before the deadline, deposit this section as `spikes/PLAN.md` and mark the design provisional.

## Failure modes & reversibility

- **Artificial envelope:** the scalar tolerance is a declared research fixture. Its response deadline cannot be transferred to the target plant without identifying relevant dynamics, disturbances, and tolerances.
- **Unmodeled coupling:** scalar success omits joint coupling, unilateral contacts, friction, falls, and actuator dynamics. Next validation must include a physically grounded multi-body envelope.
- **Infeasible actuation:** some disturbances exceed available authority regardless of speed. An oracle failure exposes this problem; increasing control frequency is not the remedy.
- **Nominal rate mistaken for latency:** hardware acceptance must measure acquisition, computation, communication, and actuator response together. The spike measures simulated time only.
- **Overcorrection:** fast feedback can amplify noise or inject energy. Noise, compliance, and actuator lag must be added before a hardware lock.
- **A redundant new controller:** existing motor control or passive mechanics may already satisfy S0a. Certify and reuse them.
- **Stale upper-layer requests:** body-local expiry and fallback behavior must be tested before integration.

Reversal is cheap: retain the timestamped contract and logs, replace the controller, or narrow the envelope through an explicit decision amendment. No learned representation or Scene Graph schema depends on this scalar implementation.

## Stackability to S3–S7

| Stage | What S0a supplies | Additional gate still required |
|---|---|---|
| S1 | Bounded reference interface and measured correction limits | Locomotion viability across support changes |
| S2 | Time-aligned body measurements and residual provenance | Contact distinguishability, uncertainty, and failure cases |
| S3 | Applied commands and timestamped sensory outcomes | Predictive accuracy under intervention |
| S4 | Action bounds and local interruption authority | Information gain within a validated probing envelope |
| S5 | Execution feedback for attempted relations | Evidence that contact relations are controllable |
| S6 | Body-motion estimates, frames, and timing | Self-motion-conditioned visual estimation |
| S7 | Capability status and recovery outcomes | Deferred composition, memory, and decision criteria |

No later stage may silently enlarge the certified operating envelope. Proposed enlargements require new tests and explicit versioning.

## Explicit non-claims

- S0a is not a complete definition of life-like competence.
- A particular reflex architecture, impedance law, or numerical frequency is not universally necessary.
- The evolutionary ladder is not a theorem about development or training order.
- Contact reactivity does not establish an estimated contact latent.
- This proposal does not rehabilitate frozen pretrained BFM plus a contact planner.
- Scalar success does not establish humanoid stability, household safety, or comparative superiority.
- Spike performance cannot promote a Candidate principle into Locked necessity.
- This proposal makes no S7 architecture decision and claims no completed experiment.
