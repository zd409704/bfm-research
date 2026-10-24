# STATUS — Author A draft (feedback-round-2026-10-24)

**State:** COMPLETE (draft sealed for cross-review). Sibling `drafts/B/` was not read.

## Outputs
- `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/drafts/A/FRAMEWORK_REVIEW.md`: causal-chain review (theory / implementation / empirical layers), all required review questions, value judgment
- `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/drafts/A/GAP_TABLE.md`: mechanism vs production vs this tree, with priorities
- `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/drafts/A/CORRECTED_CONCLUSIONS.md`: B01–B05 and H1–H4 re-slotted as theory / local check / pending real experiment
- `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/drafts/A/MINIMAL_EXPERIMENTS.md`: E0 gate + E1 (A) first; E2 (B) staged; C pre-registered and deferred; production evidence plan
- `/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24/drafts/A/STATUS.md`: this file

## Headline judgment
**Revise-then-continue, bounded small scale.**
- Most promising benefit: reward-free relabeled reuse of all real experience, plus macro-level credit assignment.
- Strongest objection: z-controllability in real physics is unevidenced, and there is no planner-z exploration (time-based schedule), so the planner may only exploit a thin demo-anchored tube of z.
- Decisive checks: E0 (controllability ratio ≤ 0.80) and E1 (T70 ratio ≤ 0.67 vs the best direct-action RL, including a correlated-noise null).

## New corrections found in this review (beyond owner list)
- B03 "irreducible floor 0.9105" sits above the setup's actual bound of 0.5625 (targets ±0.75), so the synthesis claim that it "matches the bound" is wrong. The B03 aliasing 0.0 is tautological (identical input tensor).
- B04 toy uses action dim 12 and d_z 64; its whitened ground truth favors the whitened arm by construction; every arm has rel-L2 error ≈ 1.

## Not done / limits
- No experiments run; all training is a planned external step. Production code was not inspected (it is outside `/srv/claude`); production facts come from the owner audit and baselines.
- No push to any remote. All writes are under `/srv/claude`.
