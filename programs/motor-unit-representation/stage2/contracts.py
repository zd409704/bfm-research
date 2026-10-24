"""Re-export of the B01–B04 merge norms.

The implementation lives in ``unit_bfm.v3.stage2_norms`` so the V3 learner
and this gate suite share one contract. Sibling import style is preserved
for ``python run_stage2.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

_CODEBASE = Path(__file__).resolve().parents[1] / "codebase"
if str(_CODEBASE) not in sys.path:
    sys.path.insert(0, str(_CODEBASE))

from unit_bfm.v3.stage2_norms import (  # noqa: E402
    FUTURE_SLICE,
    LAGGED_SLICE,
    P_DIM,
    SCENE_ID,
    SCENES,
    VARIANTS,
    DualPartitionNormalizer,
    SupportSampler,
    demand_label,
    equilibrium_label,
    frozen_local_hash,
    logit_path_alive,
    make_program,
    marginals_do_not_certify_joint,
    matched_pair_mask,
    nondim_v3_g,
    participation_ratio,
    philox_digest,
    rule_step,
    sanitize_privileged,
    sanitize_privileged_tensor,
    schema_guard_g,
    single_link_gravity,
    t_kappa,
    t_kappa_inverse,
)

__all__ = [
    "FUTURE_SLICE",
    "LAGGED_SLICE",
    "P_DIM",
    "SCENE_ID",
    "SCENES",
    "VARIANTS",
    "DualPartitionNormalizer",
    "SupportSampler",
    "demand_label",
    "equilibrium_label",
    "frozen_local_hash",
    "logit_path_alive",
    "make_program",
    "marginals_do_not_certify_joint",
    "matched_pair_mask",
    "nondim_v3_g",
    "participation_ratio",
    "philox_digest",
    "rule_step",
    "sanitize_privileged",
    "sanitize_privileged_tensor",
    "schema_guard_g",
    "single_link_gravity",
    "t_kappa",
    "t_kappa_inverse",
]
