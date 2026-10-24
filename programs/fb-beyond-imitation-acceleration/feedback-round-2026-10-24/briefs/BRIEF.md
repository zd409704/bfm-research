# Feedback Round Brief — Framework Review and Minimal Validation

**Program**: `fb-beyond-imitation-acceleration`
**Round id**: `feedback-round-2026-10-24`
**Trigger**: Owner feedback correcting research mainline after B01–B05 delivery.
**Execution state**: `IN_PROGRESS`

## Goal

Independent dual-author review of the corrected training framework, then a minimal decisive experiment plan. Do not reopen sealed B01–B05 adversarial packets as new science; reclassify their evidence scope.

## Author tracks

- Author A: Claude Opus — `drafts/A/`
- Author B: Codex — `drafts/B/`
- Prompt parity: same brief; outputs differ only by track path.

## Hard constraints

- English only. Operate strictly under `/srv/claude`.
- No commercial robot/product/company brand names; generic home-humanoid / plant-class wording.
- Do not claim B01–B05 GPU/script PASS as framework validation.
- Do not invent production code paths outside `/srv/claude`; cite existing program files under this tree; mark production-climb verification as planned external steps.

## Read first

1. `briefs/OWNER_FEEDBACK_EN.md` (this round)
2. `../PROGRAM_CHARTER.md`
3. `../program-ledger.md`
4. `../synthesis/B01-synthesis.md` … `B05-synthesis.md` (skim for sealed norms)
5. `../gpu_experiments/README.md` and result JSON scopes only as local checks

## Deliverables per author

Write under your draft directory:
- `FRAMEWORK_REVIEW.md` — answers owner sections on causal chain, theory/implementation/empirical layers, value judgment
- `GAP_TABLE.md` — mechanism vs what exists in this research tree / known missing production pieces
- `CORRECTED_CONCLUSIONS.md` — B01–B05 re-slotting
- `MINIMAL_EXPERIMENTS.md` — choose A/B/C priorities with pre-registered thresholds
- `STATUS.md` — short completion note

After both drafts seal, orchestration runs cross-review and adjudication (agy + Sonnet) unless owner narrows the round.

## Orchestration note (2026-10-24)

Draft phase sealed. Blind cross-review prompts launched: `prompts/FR-review-A-on-B.txt` (Claude) and `prompts/FR-review-B-on-A.txt` (Codex). Adjudication (agy + Sonnet) follows after both reviews seal.
