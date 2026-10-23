# Spike PLAN — Recommended candidate B / S0a (amended)

**Sealed before runner start.** Hash this file into `logs/seal.txt` before any `spikes/` code execution.  
**Maximum attempts:** 3  
**Runner may:** write harness under `spikes/`, fix bugs to match this plan.  
**Runner must not:** change metric, threshold, seeds, attempt cap, or mechanism under test. If blocked → `spikes/BLOCKED.md`.

## Goal

Provide a *discriminating* mechanical check of Proposal B’s response-deadline claim on the scalar fixture, plus a humanoid-plausible LIP re-derive — addressing adjudication amendments (latency sweep near L*, not vacuous PASS-by-construction).

## Fixture A — scalar plant (from Proposal B)

- Plant: \(\dot x = a x + u + d\), \(a=10\,s^{-1}\) (Proposal B’s stated fixture; **not** claimed to be the target plant).
- Envelope: \(|x(t)| \le b\) with \(b=0.01\) (as in B), disturbance class as in B’s spike section unless stated.
- Analytic \(L^* = \ln(1.1)/10 \approx 9.531\,\mathrm{ms}\) (witness; do not retune to pass).

### Metric A1 — latency sweep
- Controllers: zero-order hold effective latency \(\tau \in \{2,5,8,9.5,10,12,15,20\}\,\mathrm{ms}\) (include points below and above \(L^*\)).
- Seeds: 3 (0,1,2) with off-grid disturbance onset (onset not aligned to control grid).
- Noise: additive sensor noise σ=1e-4 on x; actuator lag first-order 2 ms.
- **Metric:** `peak_abs_x` for each (τ, seed).
- **Threshold / verdict rule:**
  - For all seeds: mean `peak_abs_x` at τ≤5 ms must be ≤ b (=0.01).
  - For all seeds: mean `peak_abs_x` at τ≥15 ms must be > b.
  - If both hold → `verdict=PASS` for fixture A discrimination.
  - If either fails → `verdict=FAIL`.
- Null/control: open-loop u=0 at τ=N/A must violate envelope under the same disturbance (else fixture invalid → `verdict=INVALID`).

## Fixture B — LIP placeholder (humanoid-plausible)

- Use \(a=\sqrt{g/z_c}\) with \(z_c=0.9\,\mathrm{m}\), \(g=9.81\) → \(a \approx 3.30\,s^{-1}\).
- Compute \(L^*_{LIP}\) under the **same relative envelope construction** as B-N1 (document formula in script output).
- **Metric B1:** printed `L_star_lip_ms`.
- **Threshold:** none for PASS/FAIL of S0a lock; **observation only**. If `L_star_lip_ms > 20`, print `flag=POLICY_50HZ_MAY_SUFFICE` (supports adjudication falsifier #2 as *evidence to reopen*, not auto-fail of fixture A).

## Commands

```bash
cd /srv/claude
python3 research/life-sensorimotor-2026-10-23/spikes/run_s0a.py
```

Must print one JSON line to stdout:
`{"metric":"discriminating_latency_sweep","threshold":"tau<=5ms peak<=0.01 AND tau>=15ms peak>0.01","fixture_A_peaks":{...},"L_star_ms":9.531,"L_star_lip_ms":...,"flag":"...","verdict":"PASS"|"FAIL"|"INVALID"}`

Also append the same line to `spikes/runs.log`.

## Pass/fail for decision.md

- Quote the JSON `verdict` line verbatim.
- Narrative without that line does not count.
- Even on PASS: packet decision stays **Provisional** regarding hardware transfer; PASS only validates the amended scalar discrimination harness.
