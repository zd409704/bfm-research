# Brief — Life-like sensorimotor program (Principle-track primary)

Platform framing: generic home humanoid / target plant only; no named robot or company.

**Run id:** `life-sensorimotor-2026-10-22-principle`  
**Canonical root:** `/srv/claude/research/life-sensorimotor-2026-10-22-principle/`  
**Method:** v1.0 pinned at `pinned/orchestrating-ai-research-teams.v1.0-1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7.md` (sha256 in `pinned/method.sha256`).  
**Hard wall clock:** deadline epoch `1792708988` = **2026-10-22 18:43:08 America/Toronto (EDT)**. At deadline: stop new model calls; flush `progress.md`; do not start new packets.  
**Human lead:** zhang david (via Grok Bot). Agents do not change this brief without an explicit Class-2 amendment note.  
**Prior packet:** inherit by ID from `inherited-ledger-P1.md` (P1 provisional Recommend B/S0a acceptance-gate; all claims Candidate). Do not paraphrase prior conclusions.

## Problem statement

**Unknown:** What transferable **necessity constraints** (Appendix B) and which **first mainline packet(s)** should govern a scientific, iteratively falsifiable program for life-like perception–action competence on a home-humanoid-class plant—capabilities that stack by evolved sensorimotor stages rather than a single end-to-end policy?

This run is **Principle-track primary**: phenomenology and implementation proposals are allowed only after (or tightly coupled to) claim records that state premises, grade, scope, and falsifier. A score or spike alone must not promote necessity.

**Decide across as many packets as fit before the wall clock** (no fixed packet count):
1. Which Candidate claims from P1 (and any new ones) survive Principle-track scrutiny; which edges of the S0–S7 *planning* ladder can be upgraded Grade 3→2/1 vs stay quarantined.
2. For each eligible packet: Recommend / Alternate / Reject with gates before ranking (B.9.5 / §4 Step 4).
3. Minimal spikes only for recommended candidates; PASS validates the harness, not hardware transfer.

## Constraints and non-goals

**Hard constraints**
1. Follow the pinned methodology end-to-end: §4 cycle, §10–13, Appendix A roster, **Appendix B Principle track (especially B.5–B.9)**.
2. All agent cwd and file writes under `/srv/claude` only. No writes under `/workspace` or elsewhere. English research artifacts only under this root.
3. Prompts to Claude/Codex/Gemini: write the task only; never discuss locale, translation, or how to phrase answers.
4. Wall clock ≤ 3 hours to epoch `1792708988`. Unlimited packets within that budget; prefer completing Principle claim packets before large phenomenology bake-offs.
5. Do not commit/push `bfm-research`. No paid cloud GPU without human approval.
6. No Grade-3 evolutionary story as Locked necessity. No named robot, product, or company in any artifact.
7. Claim state changes only per B.9 (claim adjudicator ≠ claim author; Grade-1 lock needs human signature—**do not claim Locked Grade-1 without human lead**; leave as Candidate + recommended-for-lock).
8. S0a-first from P1 is an **acceptance-gate recommendation**, not a Locked necessity ordering (inherit D-P1-001 Provisional).

**Non-goals**
- Full product architecture rewrite
- Training a new foundation locomotion model from scratch
- Claiming comparative superiority vs published parkour baselines without a spike
- Settling late-ladder composition/memory before early gates have Principle support
- Signing Grade-1 locks without the human lead

## Role roster (Appendix A + B.9)

Record frozen contract in `roster.md` before Step 2 of the first packet.

| Slot | Model | Invoke from `/srv/claude` | Must not |
|---|---|---|---|
| **Orchestrator** | Claude Opus (`--model opus --effort medium`) | `claude -p --model opus --effort medium ...` | Sole-adjudicate a proposal it authored; change claim state as if it were claim adjudicator on its own claims |
| **Competing author A** | Claude Opus medium (isolated draft tree) | same family as Orchestrator when Orchestrator does not author; if Orchestrator authors A, bind separate adjudicator | See other draft during Step 2 |
| **Competing author B** | Codex `gpt-6-astra` high | `codex exec -m gpt-6-astra -c model_reasoning_effort="high" ...` | See other draft during Step 2 |
| **Experiment runner** | Claude Sonnet medium | `claude -p --model sonnet --effort medium ...` | Edit brief/rubric; redefine goals; change claim state |
| **Claim adjudicator** | Must be a **different model family** from the claim author for that claim (Astra for Opus-authored claims; Opus or Sonnet for Astra-authored claims—prefer Astra↔Opus cross-family). Record binding per claim in `claims/` | Author the claim it adjudicates; promote to Locked Grade-1 without human signature |

Competition: proposals on a packet from **different model families**. Isolation: separate draft dirs, seal+publish-after-all, order-swap adjudication (Class-1). Class-2 dual cross-family adjudication: apply only if wall clock allows and log it; otherwise order-swap + disclose confound.

## Program structure (unlimited packets within wall clock)

Suggested order (Orchestrator may reorder with rationale in `progress.md`, but may not treat planning order as necessity—B.8.3):

1. **Packet Prin-1 — Claim hygiene on inherited P1 claims**  
   For each C-P1-* : confirm premises, grade, scope, falsifier; quarantine Grade-3; nominate upgrades; claim adjudicator rules Candidate stay / recommend-for-lock / retire-nominate. No Grade-1 Locked without human.

2. **Packet Prin-2 — Ladder-edge necessity**  
   For edges among S0a/S0b/S1/S2 (planning ladder only): each edge is its own claim; default Grade 3; attempt upgrade arguments; citation-ablation test (B.8.7).

3. **Packet Eng-1 — Next mainline after P1**  
   If Prin packets leave S0a as acceptance gate only: competing proposals for the next engineering packet (likely S2a contact observability floor per P1 Alternate), with interface contracts and spike—**gated by** any surviving Principle claims.

Continue Eng/Prin packets until deadline. Each packet: Brief amendment note (append-only) → Solo drafts → Blind review → Adjudication (gates before ranking) → Spike if recommended → Lock/provisional + ledger update.

## Rubric (fixed; do not change mid-contest without Class-2)

Score 1–5; low scores need a concrete objection. Gates (Appendix B) apply **before** ranking.

| Dimension | Question |
|---|---|
| Constraint fit | Obeys hard constraints and non-goals? |
| Principle integrity | States grades; separates necessity vs sufficiency; no Grade-3-as-law; claim artifacts complete? |
| Falsifiability | Defined spike or counterexample search can fail within days? |
| Evidence demand | Data/compute/hardware demand; lower better if equal force |
| Failure modes | Dominant failures named and mitigable? |
| Integrability | Clear ownership of body loop vs scene publication vs decision core (generic names only) |
| Latency / criticality | Right tier (fast reflex vs policy vs slow cognition)? |
| Complexity cost | Extra machinery justified? |
| Reversibility | Cheap to abandon if wrong? |
| Stackability | Enables later stages without requiring them prematurely? |

## Spike criteria

Filed under `spikes/<packet-id>/` with sealed `PLAN.md` before run:
- Runnable local harness + machine-readable verdict, **or**
- Complete PLAN only → decision **provisional**
- PASS = harness only; never hardware transfer
- Counterexample searches for claims are experiments under §12.2

## Artifact layout

```
brief.md, roster.md, progress.md, program-ledger.md
inherited-ledger-P1.md
pinned/
claims/C-*/claim.md, upgrade-log.md, violations.md
packets/<id>/{proposals,reviews,adjudication,decision.md,spikes,logs}
principles/   # optional indexes
method-issues/
logs/
```

## Deadline behavior

At epoch `1792708988`: stop new model calls; write `progress.md` with completed packets, open claims, next action; leave agents paused. Research agents must not write outside `/srv/claude`.
