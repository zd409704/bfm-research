# Roster contract (frozen before Step 2 of first packet)

**Method:** v1.0 pinned sha256 `1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`  
**Run:** life-sensorimotor-2026-10-22-principle  
**Deadline epoch:** 1792708988

| Slot | Binding | Effort / tools | Notes |
|---|---|---|---|
| Orchestrator | Claude Opus | medium; may deposit transcripts | Does not sole-score own authorship |
| Author A | Claude Opus | medium; isolated `drafts/A` | Different tree from B |
| Author B | Codex gpt-6-astra | high; isolated `drafts/B` | Different family from A |
| Experiment runner | Claude Sonnet | medium; spikes only per PLAN | No brief/rubric/claim-state edits |
| Claim adjudicator (Opus-authored claims) | Codex gpt-6-astra high | read claim + evidence only | Cross-family vs author |
| Claim adjudicator (Astra-authored claims) | Claude Opus medium | read claim + evidence only | Cross-family vs author |
| Packet adjudicator | Order-swap Sonnet P/Q unless Class-2 dual applied | medium | Disclose family confound if same as Author A |

**Parity:** author prompts equal length/structure aside from identity; seal+publish-after-all; append-only logs.
