# Roster Contract (Frozen Before Step 2 of Packet B01)

**Method Version**: v1.0 pinned (`pinned/orchestrating-ai-research-teams.v1.0-1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7.md`, sha256 `1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Program**: `motor-unit-representation`
**Freeze Epoch**: `1792809557`
**Run Deadline Epoch**: `1792895957`

## 1. Heterogeneous Three-Family Slot Bindings (Appendix A.5)

| Slot | Role & Scope | Model Family & Exact Identifier | Reasoning / Effort | Sandbox & Writable Roots | Invocation Template |
|---|---|---|---|---|---|
| **Orchestrator & Author A** | Packet Briefs, Solo Draft A (`packets/<ID>/drafts/A/proposal.md`), Cross-Review (`reviews/review-A-on-B.md`) | Anthropic Claude (`claude --model opus`) | `medium` | `cwd=/srv/claude`; isolated write to `packets/<ID>/drafts/A/` during Step 2 | `cd /srv/claude && /home/box/.local/bin/claude -p --model opus --effort medium --dangerously-skip-permissions --permission-mode bypassPermissions < prompt.txt` |
| **Competing Author B** | Solo Draft B (`packets/<ID>/drafts/B/proposal.md`), Cross-Review (`reviews/review-B-on-A.md`) | OpenAI Codex (`codex -m gpt-6-astra`) | `high` (`model_reasoning_effort=high`) | `cwd=/srv/claude`; isolated write to `packets/<ID>/drafts/B/` during Step 2 | `cd /srv/claude && /home/box/.local/bin/codex exec -C /srv/claude -m gpt-6-astra -c model_reasoning_effort=high -s workspace-write --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --add-dir /srv/claude < prompt.txt` |
| **Cross-Family Adjudicator 1** | Independent Third-Family Packet Adjudicator (`P/Q` and `Q/P` order-swapped) & Claim Adjudicator | Third-Party Family (`agy`) | `high` (`--effort high`) | `cwd=/srv/claude`; reads sealed anonymized candidates `P` and `Q` | `cd /srv/claude && /home/box/.local/bin/agy --effort high --dangerously-skip-permissions --add-dir /srv/claude -p="$(cat prompt.txt)"` |
| **Order-Swapped Adjudicator 2** | Secondary Packet Adjudicator (`P/Q` and `Q/P` order-swapped) | Anthropic Claude (`claude --model sonnet`) | `medium` | `cwd=/srv/claude`; reads sealed anonymized candidates `P` and `Q` | `cd /srv/claude && /home/box/.local/bin/claude -p --model sonnet --effort medium --dangerously-skip-permissions --permission-mode bypassPermissions < prompt.txt` |
| **Experiment Runner** | Pre-registered Spike Execution (`packets/<ID>/spikes/<SPIKE_ID>/`) & Colab GPU Training Package (`gpu_experiments/`) | Anthropic Claude (`claude --model sonnet`) + Python/PyTorch | `medium` | Writes only inside `packets/<ID>/spikes/` and `gpu_experiments/` per §12.2 | `cd /srv/claude && /srv/claude/.venv/bin/python ...` |
| **Claim Adjudicator (Opus Claims)** | Cross-family claim state transitions (Appendix B.9) | OpenAI Codex (`codex -m gpt-6-astra`) + `agy` | `high` | Reads claim record + evidence only | Cross-family vs claim author |
| **Claim Adjudicator (Astra Claims)** | Cross-family claim state transitions (Appendix B.9) | Anthropic Claude (`claude --model opus`) + `agy` | `medium` / `high` | Reads claim record + evidence only | Cross-family vs claim author |

## 2. Parity & Isolation Rules (§11 & Appendix A.5)
1. **Prompt Parity (§11.4)**: Author A and Author B prompts for each packet are instantiated from a single template and differ only in track label (`A` vs `B`) and target output path (`drafts/A/proposal.md` vs `drafts/B/proposal.md`). The diff is filed before execution.
2. **Drafting Isolation & Publish-After-All (§11.1–§11.2)**: Neither author reads the sibling draft directory during Step 2. Both drafts are SHA256-sealed into `logs/seal.log` upon completion and copied to `packets/<ID>/proposals/A.md` and `packets/<ID>/proposals/B.md` only after both tracks finish.
3. **Blind Cross-Review (§4 Step 3)**: Reviewer A (`claude --model opus`) critiques Proposal B (`reviews/review-A-on-B.md`), and Reviewer B (`codex -m gpt-6-astra`) critiques Proposal A (`reviews/review-B-on-A.md`) without seeing each other's review. Both reviews are sealed before Step 4.
4. **Cross-Family Order-Swapped Adjudication (§4 Step 4)**: Candidates are anonymized as `Candidate P` and `Candidate Q` (and swapped in a second pass) and scored independently by `agy` (third model family that authored neither proposal) and order-swapped `claude --model sonnet`.
