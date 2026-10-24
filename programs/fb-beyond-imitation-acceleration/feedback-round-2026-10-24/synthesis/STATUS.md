# STATUS — orchestrator synthesis, feedback-round-2026-10-24

**State:** `SYNTHESIS SEALED — AWAITING OWNER DISPOSITION`
**Date:** 2026-10-24
**Owner call:** **REVISE-THEN-CONTINUE.** Both adjudications reached this call independently, so it was not overridden.

## Written this step

All five files are under `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/synthesis/`:

| File | Content |
|---|---|
| `DISPOSITION.md` | Owner call and the conditions that would change it; per-file hybrid base; deduplicated fix list MX-1…MX-12 (3 CRITICAL, by intersection of both adjudications); decisive assumptions D1–D5; residual disagreements R1–R6; staged spend gate S0→S3 with cost ranges |
| `MERGED_GAP_TABLE.md` | 32 rows (G01–G32), labelled O/R/S/P for provenance and P0–P2 for priority, with an origin column |
| `MERGED_CORRECTED_CONCLUSIONS.md` | Per-number B01–B05 re-scoping ledger; H1–H4 status; draft-claim premise repairs; source verification of the B01/B03/B04 script facts |
| `MERGED_MINIMAL_EXPERIMENTS.md` | Single revised plan:<br>• Stage-0 entry integrity gate;<br>• two-tier A (15M → 100M per run) with AUC primary and censor-aware T70;<br>• fault protocol;<br>• DA-C and A-I controls;<br>• repaired E0;<br>• conditional Z2;<br>• causal C with C-rand and C-pos;<br>• cost ceilings;<br>• evidence bundle |
| `STATUS.md` | This file |

Inputs read:
- `briefs/BRIEF.md`, `briefs/OWNER_FEEDBACK_EN.md` and `../PROGRAM_CHARTER.md`;
- both adjudications;
- both blind reviews (mandatory-fix sections);
- the draft A/B experiment, gap, conclusions and framework files, for concrete values;
- read-only source lines in `gpu_experiments/run_b01_*.py`, `run_b03_*.py` and `run_b04_*.py`;
- the program ledger, for headline numbers.

## Compliance

- All reads and writes stayed under `/srv/claude`.
- No training was run, no code was executed against research artifacts, and nothing was pushed to any remote.
- The only computations were stand-alone arithmetic for Wilson bounds and t-quantiles.
- The text is English only, with generic home-humanoid / plant-class wording. Accelerator and simulator brand names that appear in the ledger were deliberately not reproduced.
- B01–B05 script/accelerator PASS is treated as local-check evidence only, throughout.
- Sealed packets were not reopened. The ledger was not edited; the reconciliation is to be appended later.

## Residual disagreements carried forward (detail in DISPOSITION §5)

- **R1** Fallback single base: agy names draft A, Sonnet names draft B. Resolved by per-file hybrid.
- **R2** Budget anchors (agy) vs throughput-derived caps (Sonnet). Resolved as anchors that act as ceilings, frozen after measurement.
- **R4** A-F′ standing arm vs routing. Routing to a conditional Z2 was chosen. This is an orchestrator choice within options both adjudications allowed.

## What remains for the production climb (PLAN ONLY — planned external steps, none executed)

1. **Owner decision** on this disposition and approval of the S0 + S1 hour ceilings (≤8 h; ~6–70 accelerator-hours, to be re-quoted after S0).
2. **S0 entry integrity gate** on the production chain (`MERGED_MINIMAL_EXPERIMENTS.md` §1, audits E-1…E-11):
   - resolve the module and entrypoint identities (G01);
   - add telemetry patches (executed-z source tags; planner-z knob present but off; off-support z log);
   - run the fixtures;
   - measure throughput;
   - freeze caps in the manifest.
3. **Freeze the manifest:**
   - arm definitions (A-F, A-D, A-DC, A-I);
   - V task balance tolerances;
   - E0 feature standardization;
   - source-ramp unit;
   - seed streams 24000–24010.
4. **S1:** setup seeds, then 4 × 5 test runs at the 15M cap, E0 at 25 / 50 / 100%, and the interim report. If triggered, run the **Z2** diagnostic.
5. **S2** (only if the L-gate passes and the owner approves the re-quoted spend): seed count fixed from the Stage-1 SD, extension to the 100M cap, then the confirmatory A verdict.
6. **S3 C** (only if the controllability and competence gates pass): donor pool, the 4 branches, fresh V planners, the three retention senses, and the C verdict.
7. **Return path:** summaries and manifests under `feedback-round-2026-10-24/evidence/…`, plus a `VERDICT.md` per check, applying the pre-registered rules verbatim.
8. **Bookkeeping, after the owner accepts:**
   - an append-only `program-ledger.md` reconciliation that cites `MERGED_CORRECTED_CONCLUSIONS.md`;
   - H4 marked incomplete pending real training;
   - H1 marked untested and deprioritized.

Nothing in this round fills an empirical cell of the causal chain.
