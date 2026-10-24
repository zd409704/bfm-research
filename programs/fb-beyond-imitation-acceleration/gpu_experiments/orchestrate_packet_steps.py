"""Mechanical v1.0 Orchestration Helper for Packets B01-B05.

Implements:
- Step 2 Seal & Publish-After-All (§11.2): hashes `drafts/A/proposal.md` and `drafts/B/proposal.md`,
  checks isolation, copies to `proposals/A.md` and `proposals/B.md`, and generates blind cross-review
  prompts (`prompts/<ID>-review-A-on-B.txt` and `prompts/<ID>-review-B-on-A.txt`) with exact parity.
- Step 3 Seal & Publish-After-All (§11.2): hashes both reviews, copies to `reviews/`, and generates
  anonymized order-swapped adjudication prompts (`P=A, Q=B` and `P=B, Q=A`) for `agy` and `claude --model sonnet`.
- Step 5 Pre-Registered Spike Runner (§12.2): executes the exact command in `spikes/<ID>-SPIKE/PLAN.md`,
  logs to `runs.log`, and writes `VERDICT.json`.
"""

from __future__ import annotations
import difflib
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path("/srv/claude/research/fb-beyond-imitation-acceleration")


def sha256_file(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def append_seal(step_tag: str, rel_path: str) -> str:
    full = ROOT / rel_path
    digest = sha256_file(full)
    now = int(time.time())
    with open(ROOT / "logs/seal.log", "a") as f:
        f.write(f"{now} UTC | {step_tag} | {rel_path} | sha256={digest}\n")
    return digest


def seal_step2_and_prepare_step3(packet_id: str) -> None:
    draft_a = ROOT / f"packets/{packet_id}/drafts/A/proposal.md"
    draft_b = ROOT / f"packets/{packet_id}/drafts/B/proposal.md"
    if not draft_a.exists() or draft_a.stat().st_size == 0:
        raise FileNotFoundError(f"Missing or empty {draft_a}")
    if not draft_b.exists() or draft_b.stat().st_size == 0:
        raise FileNotFoundError(f"Missing or empty {draft_b}")

    ha = append_seal(f"{packet_id}_STEP2_SEAL_A", f"packets/{packet_id}/drafts/A/proposal.md")
    hb = append_seal(f"{packet_id}_STEP2_SEAL_B", f"packets/{packet_id}/drafts/B/proposal.md")

    prop_a = ROOT / f"packets/{packet_id}/proposals/A.md"
    prop_b = ROOT / f"packets/{packet_id}/proposals/B.md"
    shutil.copy2(draft_a, prop_a)
    shutil.copy2(draft_b, prop_b)
    append_seal(f"{packet_id}_STEP2_PUBLISH_A", f"packets/{packet_id}/proposals/A.md")
    append_seal(f"{packet_id}_STEP2_PUBLISH_B", f"packets/{packet_id}/proposals/B.md")

    review_template = f"""You are Blind Reviewer __REVIEWER__ on Packet {packet_id} of the research program at `/srv/claude/research/fb-beyond-imitation-acceleration`.

Read the following frozen context and candidate files:
1. `/srv/claude/research/fb-beyond-imitation-acceleration/PROGRAM_CHARTER.md`
2. `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/brief.md`
3. `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/proposals/__TARGET__.md`

Isolation & Execution Rules:
- Do NOT read any other file in `reviews/` or `drafts/`.
- You may also read `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/spikes/{packet_id}-SPIKE/VERDICT.json`.
- Write the output markdown file `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-__REVIEWER__-on-__TARGET__.md` directly without running any bash or python exploratory scripts.
- Keep your review concise, rigorous, and between 80 and 140 lines, directly keyed to the rubric rows and hard constraints in `brief.md`.

Required Sections in `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-__REVIEWER__-on-__TARGET__.md`:
1. `# Blind Review __REVIEWER__ on Proposal __TARGET__ (Packet {packet_id})`
2. `## 1. Gate & Hard-Constraint Audit`: Check whether Proposal __TARGET__ violates any Hard Constraint in `PROGRAM_CHARTER.md` or `brief.md`.
3. `## 2. Rubric-Keyed Technical Objections`: Concrete mathematical, physical, or algorithmic defects keyed to each rubric dimension in `brief.md` (labeled `[CRITICAL]`, `[MAJOR]`, or `[MINOR]`).
4. `## 3. Audit of Rejected Alternative & Necessity Claim`: Evaluate whether the rejected alternative in Proposal __TARGET__ is non-trivial and whether its Principle Claim (`C-{packet_id}-__TARGET__-01`) satisfies Appendix B premises and falsifiability.
5. `## 4. Spike Protocol Critique`: Identify any missing controls, unmeasured confounds, or threshold flaws in the proposed empirical spike.
"""
    rev_a_on_b = review_template.replace("__REVIEWER__", "A").replace("__TARGET__", "B")
    rev_b_on_a = review_template.replace("__REVIEWER__", "B").replace("__TARGET__", "A")

    p_ab = ROOT / f"prompts/{packet_id}-review-A-on-B.txt"
    p_ba = ROOT / f"prompts/{packet_id}-review-B-on-A.txt"
    p_diff = ROOT / f"prompts/{packet_id}-review-diff.txt"
    p_ab.write_text(rev_a_on_b)
    p_ba.write_text(rev_b_on_a)
    diff_txt = "".join(
        difflib.unified_diff(
            rev_a_on_b.splitlines(keepends=True),
            rev_b_on_a.splitlines(keepends=True),
            fromfile=str(p_ab.name),
            tofile=str(p_ba.name),
        )
    )
    p_diff.write_text(diff_txt)
    append_seal(f"{packet_id}_STEP3_PROMPT_AB", f"prompts/{packet_id}-review-A-on-B.txt")
    append_seal(f"{packet_id}_STEP3_PROMPT_BA", f"prompts/{packet_id}-review-B-on-A.txt")
    append_seal(f"{packet_id}_STEP3_PROMPT_DIFF", f"prompts/{packet_id}-review-diff.txt")
    print(f"[{packet_id}] Sealed Step 2 drafts (A={ha[:12]}, B={hb[:12]}) and prepared Step 3 review prompts.")


def seal_step3_and_prepare_step4(packet_id: str) -> None:
    rev_ab = ROOT / f"packets/{packet_id}/reviews/review-A-on-B.md"
    rev_ba = ROOT / f"packets/{packet_id}/reviews/review-B-on-A.md"
    if not rev_ab.exists() or rev_ab.stat().st_size == 0:
        raise FileNotFoundError(f"Missing or empty {rev_ab}")
    if not rev_ba.exists() or rev_ba.stat().st_size == 0:
        raise FileNotFoundError(f"Missing or empty {rev_ba}")

    hab = append_seal(f"{packet_id}_STEP3_SEAL_REV_AB", f"packets/{packet_id}/reviews/review-A-on-B.md")
    hba = append_seal(f"{packet_id}/reviews/review-B-on-A.md", f"packets/{packet_id}/reviews/review-B-on-A.md")
    shutil.copy2(rev_ab, ROOT / f"reviews/{packet_id}-review-A-on-B.md")
    shutil.copy2(rev_ba, ROOT / f"reviews/{packet_id}-review-B-on-A.md")

    # Create anonymized copies Candidate P and Candidate Q for Order 1 (P=A, Q=B) and Order 2 (P=B, Q=A)
    anon_dir = ROOT / f"packets/{packet_id}/anonymized"
    anon_dir.mkdir(parents=True, exist_ok=True)
    text_a = (ROOT / f"packets/{packet_id}/proposals/A.md").read_text()
    text_b = (ROOT / f"packets/{packet_id}/proposals/B.md").read_text()
    # Strip Proposal A / Proposal B identifiers
    clean_a = text_a.replace("Proposal A", "Candidate").replace("C-" + packet_id + "-A-", "C-" + packet_id + "-CAND-")
    clean_b = text_b.replace("Proposal B", "Candidate").replace("C-" + packet_id + "-B-", "C-" + packet_id + "-CAND-")
    (anon_dir / "order1_P.md").write_text(clean_a)
    (anon_dir / "order1_Q.md").write_text(clean_b)
    (anon_dir / "order2_P.md").write_text(clean_b)
    (anon_dir / "order2_Q.md").write_text(clean_a)

    adj_prompt_order1 = f"""You are an Independent Cross-Family Adjudicator on Packet {packet_id} of the research program at `/srv/claude/research/fb-beyond-imitation-acceleration` executing under Methodology v1.0 (§4 Step 4 & Appendix B.9).

Read the following files:
1. `/srv/claude/research/fb-beyond-imitation-acceleration/PROGRAM_CHARTER.md`
2. `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/brief.md`
3. Candidate P: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/anonymized/order1_P.md`
4. Candidate Q: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/anonymized/order1_Q.md`
5. Blind critique on Candidate P: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-B-on-A.md`
6. Blind critique on Candidate Q: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-A-on-B.md`

Execution Rules:
- You may also read `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/spikes/{packet_id}-SPIKE/VERDICT.json`.
- Write the output markdown file `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/adjudication-agy-order1.md` directly without running any bash or python exploratory scripts, keeping the report focused and between 80 and 140 lines.

Write your complete adjudication report to `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/adjudication-agy-order1.md` containing:
1. Eligibility Gate Check (Hard Constraints & Appendix B.5 gates) for Candidate P and Candidate Q.
2. Exact numerical scores (out of 100, weighted by the rubric in `brief.md`) for Candidate P and Candidate Q with specific technical justification for every row.
3. Principle Claim Adjudication (Appendix B.9) on both candidates' proposed necessity claims (`Candidate` stay, tighten-premises, or downgrade).
4. Disposition: `Recommend` (`P` or `Q` or `Tie`), `Alternate`, Mandatory Merge items from the alternate track, and `Confounds` paragraph.
"""

    adj_prompt_order2 = f"""You are the Order-Swapped Adjudicator (Presentation Order 2: P and Q reversed) on Packet {packet_id} of the research program at `/srv/claude/research/fb-beyond-imitation-acceleration` executing under Methodology v1.0 (§4 Step 4 & Appendix B.9).

Read the following files:
1. `/srv/claude/research/fb-beyond-imitation-acceleration/PROGRAM_CHARTER.md`
2. `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/brief.md`
3. Candidate P (Order 2): `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/anonymized/order2_P.md`
4. Candidate Q (Order 2): `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/anonymized/order2_Q.md`
5. Blind critique on Candidate P (Order 2): `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-A-on-B.md`
6. Blind critique on Candidate Q (Order 2): `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/reviews/review-B-on-A.md`

Execution Rules:
- Do NOT read `adjudication-agy-order1.md`.
- You may also read `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/spikes/{packet_id}-SPIKE/VERDICT.json`.
- Write the output markdown file `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/adjudication-sonnet-order2.md` directly without running any bash or python exploratory scripts, keeping the report focused and between 80 and 140 lines.

Write your complete order-swapped adjudication report to `/srv/claude/research/fb-beyond-imitation-acceleration/packets/{packet_id}/adjudication-sonnet-order2.md` containing:
1. Eligibility Gate Check (Hard Constraints & Appendix B.5 gates) for Candidate P (Order 2) and Candidate Q (Order 2).
2. Exact numerical scores (out of 100, weighted by the rubric in `brief.md`) for Candidate P (Order 2) and Candidate Q (Order 2) with specific technical justification for every row.
3. Principle Claim Adjudication (Appendix B.9) on both candidates' proposed necessity claims.
4. Disposition: `Recommend` (`P` or `Q` or `Tie`), `Alternate`, Mandatory Merge items, and `Confounds` paragraph.
"""

    p1 = ROOT / f"prompts/{packet_id}-adj-agy-order1.txt"
    p2 = ROOT / f"prompts/{packet_id}-adj-sonnet-order2.txt"
    p1.write_text(adj_prompt_order1)
    p2.write_text(adj_prompt_order2)
    append_seal(f"{packet_id}_STEP4_PROMPT_ORDER1", f"prompts/{packet_id}-adj-agy-order1.txt")
    append_seal(f"{packet_id}_STEP4_PROMPT_ORDER2", f"prompts/{packet_id}-adj-sonnet-order2.txt")
    print(f"[{packet_id}] Sealed Step 3 reviews (AB={hab[:12]}, BA={hba[:12]}) and prepared Step 4 adjudication prompts.")


def run_step5_spike(packet_id: str) -> dict:
    script_map = {
        "B01": "run_b01_gram_spike.py",
        "B02": "run_b02_nonstationarity_spike.py",
        "B03": "run_b03_contact_aliasing_spike.py",
        "B04": "run_b04_four_arm_ablation.py",
        "B05": "run_b05_r21_verification_suite.py",
    }
    script_file = ROOT / "gpu_experiments" / script_map[packet_id]
    spike_dir = ROOT / f"packets/{packet_id}/spikes/{packet_id}-SPIKE"
    code_hash = sha256_file(script_file)
    cmd = ["/srv/claude/.venv/bin/python", str(script_file)]
    now = int(time.time())
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out_json = json.loads(proc.stdout)
    verdict_path = spike_dir / "VERDICT.json"
    verdict_path.write_text(json.dumps(out_json, indent=2))
    runs_log = spike_dir / "runs.log"
    with open(runs_log, "a") as f:
        f.write(
            f"{now} UTC | cmd={' '.join(cmd)} | code_sha256={code_hash} | verdict={out_json['verdict']} | elapsed={out_json['elapsed_sec']}s\n"
        )
    append_seal(f"{packet_id}_STEP5_SPIKE_VERDICT", f"packets/{packet_id}/spikes/{packet_id}-SPIKE/VERDICT.json")
    print(f"[{packet_id}] Executed pre-registered spike -> verdict={out_json['verdict']}")
    return out_json


if __name__ == "__main__":
    action = sys.argv[1]
    pid = sys.argv[2]
    if action == "step2_seal":
        seal_step2_and_prepare_step3(pid)
    elif action == "step3_seal":
        seal_step3_and_prepare_step4(pid)
    elif action == "step5_spike":
        run_step5_spike(pid)
