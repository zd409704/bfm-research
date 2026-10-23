# Brief — Implementing life-like sensorimotor competence

Platform framing: generic home humanoid / target plant only; no named robot or company.

**Run id:** life-sensorimotor-2026-10-23  
**Canonical root:** `/srv/claude/research/life-sensorimotor-2026-10-23/`  
**Hard wall clock:** start ~2026-10-23 03:07 CST → **deadline 2026-10-23 06:07 CST (3 hours)**. If incomplete at deadline: write `progress.md`, pause all agents, do not start new steps.  
**Human lead:** zhang david (via Grok Bot Claude专用 1). Agents do not change this brief without an explicit amendment note.

## Problem statement

**Unknown:** What is a *scientific, iteratively falsifiable* path to implement life-like perception–action competence on a home humanoid—i.e., capabilities that arise by stacking evolved sensorimotor competences rather than by a single end-to-end policy?

We already have (context, not free to rewrite):
- An evolutionary capability ladder draft (S0 reflex/impedance → S1 proprioceptive locomotion base → S2 contact observability → S3 forward sensory prediction → S4 active probing → S5 contact-as-controllable-relation → S6 self-motion-conditioned vision → S7 composition + memory/decision).
- Two adversarial reviews of related BFM / bio-inspired reports (consensus: contact *reactivity* holds; “contact is a necessary latent already estimated” does *not*; frozen pretrained BFM + contact planner as stated is *not* feasible; biology is motivation only).

**Decide in this run:** For the *next locked research mainline*, which **one primary subproblem packet** should be executed first, with what **interface contracts**, what **necessity claims (Appendix B grades)**, and what **minimal spike**—such that later stages can stack without skipping gates.

## Constraints and non-goals

**Hard constraints**
1. Follow `notes/orchestrating-ai-research-teams.md` (six-step cycle + Appendix A roster + Appendix B necessity protocol). Chat is not source of truth; only files under this run root are.
2. All agent work cwd `/srv/claude`. Do not write user-facing Chinese deliverables under `/srv/claude` (English research artifacts only here). Mirror a short `progress.md` / final `decision.md` copy to `/workspace/adversarial-reviews/life-sensorimotor-2026-10-23/` when pausing or locking.
3. Communicate with Claude and Codex **in English only** (write prompts in English; do not add meta-instructions about language).
4. Wall clock ≤ 3 hours. Prefer completing Brief→Draft→Review→Adjudication→Spike plan (+ spike *code/sim stub* if time). Full robot experiments are out of scope for this wall clock.
5. Do not commit/push the `bfm-research` git repo. Do not spend paid cloud GPU beyond local box CPU/GPU already available without human approval.
6. Do not treat Grade-3 evolutionary stories as Locked necessity. Do not promote benchmark-like rhetoric into necessity without Appendix B upgrade.

**Non-goals**
- Full product architecture rewrite
- Training a new BFM from scratch in this run
- Claiming comparative superiority vs Light-Loco-Parkour / PHP without a spike
- Settling S7 (Life Core) before S0–S2 gates

## Role roster (Appendix A) — three models, all run under `/srv/claude`

| Slot | Model | How to invoke | Must not |
|---|---|---|---|
| **Orchestrator** | Claude Opus 5.5 (`--model opus --effort medium`) | `cd /srv/claude && claude -p --model opus --effort medium ...` | Sole-adjudicate a proposal it authored on the *same* packet |
| **Competing author** | Codex `gpt-6-astra` high | `cd /srv/claude && codex exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only ...` (write mode only for experiment runner path; authors use read-only + deposit via orchestrated file writes if sandbox blocks) | See the other draft during Step 2 |
| **Experiment runner** | Claude Sonnet 5.5 (`--model sonnet`) | `cd /srv/claude && claude -p --model sonnet --effort medium ...` | Edit `brief.md` / rubric scores / redefine goals |

If sandbox prevents Codex from writing files: Orchestrator may *deposit* Codex stdout into `proposals/` and `reviews/` verbatim. Authors still must not see each other’s drafts during drafting (separate prompts, no shared context).

**Competition requirement:** Proposals A and B must come from **different model families** (Opus track vs Astra track).

## Subproblem packet (this run)

**Packet P1 — First competence to lock for life-like sensorimotor stacking**

Produce competing proposals that answer:

1. Which stage among S0–S2 (or a justified split/merge) is the **correct first lock**, and why in necessity terms (Appendix B), not only engineering convenience?
2. What **interface contracts** does that stage expose upward (signals, rate class, ownership: body loop vs Scene Graph vs Life Core)?
3. What **Candidate/Locked necessity claims** apply (grade 1/2/3 + scope)?
4. What is the **minimal spike** (sim-only OK) with pre-registered pass/fail metrics executable within leftover wall clock or as a deferred spike plan?

## Rubric (fixed before drafts — do not change mid-contest)

Score each proposal 1–5 per row; low scores need a concrete objection.

| Dimension | Question |
|---|---|
| Constraint fit | Obeys hard constraints and non-goals? |
| Falsifiability | Can a defined spike show failure within days, not months? |
| Evidence demand | How much data/compute/hardware to validate? Lower demand better if equal force. |
| Failure modes | Dominant failures named and mitigable? |
| Integrability | Respects body vs Scene Graph vs Life Core ownership? |
| Latency / criticality class | Right real-time vs offline tier (reflex ≥200 Hz class vs ~50 Hz policy vs slow cognition)? |
| Complexity cost | Extra machinery justified? |
| Reversibility | Cheap to abandon if wrong? |
| Necessity discipline (Appendix B) | Avoids Grade-3-as-law; states grades; does not confuse sufficiency with necessity? |
| Stackability | Enables later S3–S7 without requiring them prematurely? |

## Spike criteria (for recommended candidate only)

A spike “passes” only with filed metrics/logs under `spikes/`:

- Either: a runnable local script/sim harness that measures the pre-registered metric and prints a machine-readable summary, **or**
- If wall clock insufficient: a complete `spikes/PLAN.md` with exact commands, metrics, and pass/fail lines — then `decision.md` marks design **provisional** (methodology: spike or it didn’t happen).

## Artifact format (minimal starter kit)

```
brief.md                          # this file
proposals/A.md                    # Orchestrator-track OR Opus competing draft
proposals/B.md                    # Astra competing draft (isolated)
reviews/A-on-B.md                 # objections keyed to rubric rows
reviews/B-on-A.md
decision.md                       # filled rubric, Recommend/Alternate/Reject, spike result or provisional
progress.md                       # required if pausing at deadline
principles/claim-*.md             # optional Appendix B claim records
logs/                             # raw model transcripts
```

## Deadline behavior

At deadline epoch in `deadline_epoch.txt`: stop new model calls; flush `progress.md` with completed steps, open artifacts, next action; copy progress + decision (if any) to `/workspace/adversarial-reviews/life-sensorimotor-2026-10-23/`. Leave agents paused.



## Timebase (amended)
All wall-clock times for this run use **box-local America/Toronto**. Hard deadline epoch unchanged: `1792706829` (= 2026-10-22 18:07:09 EDT box-local).
