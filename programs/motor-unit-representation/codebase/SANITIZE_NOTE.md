# Sanitize note — motor-unit FB experiment tree

- **Source**: local mirror of a motor-unit forward-backward (FB) experiment tree (raw download kept outside this research tree).
- **Destination**: `/srv/claude/research/motor-unit-representation/codebase/unit_bfm/`
- **Sanitize date**: 2026-10-24 01:58 EDT
- **What was stripped / changed**:
  - Removed download provenance file that named an external source.
  - Removed Chinese master synthesis; replaced with English pointer to `../synthesis/` (B01–B04).
  - Translated or replaced remaining CJK / fullwidth punctuation in docs, handoffs, and the eval web UI strings.
  - Scrubbed absolute local machine paths and hostnames from docs, JSON audits, and biped model metadata; replaced with relative placeholders (`biped/models/...`, `artifacts/...`, `.venv/bin/python`, etc.).
  - Removed external web / citation URLs from documentary markdown (local `127.0.0.1` eval-app addresses kept for run instructions).
  - No commercial robot / joint product or company names were present after scrub; package import name `unit_bfm` retained so code remains runnable.
- **Unchanged**: Python package layout and `unit_bfm.*` imports; tests, configs, `v3/`, and English technical docs content aside from the scrub above.
- **Relocated**: this copy now lives at `programs/motor-unit-representation/codebase/unit_bfm/` in the research repository. Stage-2 learner hooks are in `unit_bfm/v3/stage2_norms.py`, `learner.py`, `networks.py`, and `fb_loss.py`.
