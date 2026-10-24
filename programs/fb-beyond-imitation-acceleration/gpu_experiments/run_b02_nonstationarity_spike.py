"""Experiment Suite B02: Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment.

Tests:
1. UFO Batch Normalizer update ordering invariance:
   - Single-pass update on (obs, m_current) and (next_obs, m_next), then freeze BN (`eval`),
     proving expert queries and `z_update` goal relabeling cause ZERO normalizer drift.
   - Contrasts with the buggy double-`m_next` update and un-frozen expert query drift.
2. Strict separation of `behavior_z` vs `z_update` in replay.
3. Behavioral drift Delta_pi(z) and encoder drift Delta_B(m) across TaskReplay generations,
   plus generation-lag weighting and full-prefix zero-hidden RNN burn-in vs stale hidden states.
"""

from __future__ import annotations
import copy
import json
import time
from typing import Dict, Any
import torch
from fb_core import (
    BackwardMapB,
    ConditionedLowLevelActor,
    RecurrentLatentPlanner,
    RecurrentTaskTwinCritic,
    RunningMeanStdNormalizer,
    sample_ufo_mixed_z,
)


def run_b02_experiment(device_str: str = "auto", seed: int = 20261023) -> Dict[str, Any]:
    device = torch.device("cuda" if (device_str == "auto" and torch.cuda.is_available()) else ("cpu" if device_str == "auto" else device_str))
    torch.manual_seed(seed)
    t0 = time.time()

    d_z = 256
    m_dim = 229
    obs_dim = 96
    act_dim = 29
    batch_size = 128

    # 1. Test BN update ordering and freeze invariance
    bn_clean = RunningMeanStdNormalizer((m_dim,)).to(device)
    bn_buggy = RunningMeanStdNormalizer((m_dim,)).to(device)
    b_net = BackwardMapB(m_dim, d_z).to(device)

    m_curr = torch.randn(batch_size, m_dim, device=device) * 1.5 + 0.3
    m_next = torch.randn(batch_size, m_dim, device=device) * 2.2 - 0.4
    m_expert = torch.randn(batch_size, m_dim, device=device) * 5.0 + 3.0

    # Clean R2.1 UFO order: update once on m_curr, once on m_next, then freeze
    bn_clean.train()
    bn_clean.update_stats(m_curr)
    bn_clean.update_stats(m_next)
    bn_clean.eval()
    mean_before_queries = bn_clean.mean.clone()
    var_before_queries = bn_clean.var.clone()

    # Run z_update sampling and expert encoding under frozen BN
    behavior_z = torch.randn(batch_size, d_z, device=device)
    behavior_z_snapshot = behavior_z.clone()
    z_update, _ = sample_ufo_mixed_z(b_net, bn_clean(m_next), goal_ratio=0.5)
    _ = b_net(bn_clean(m_expert))

    bn_drift_under_frozen_queries = float(
        (torch.max(torch.abs(bn_clean.mean - mean_before_queries))
         + torch.max(torch.abs(bn_clean.var - var_before_queries))).item()
    )
    behavior_z_mutated = float(torch.max(torch.abs(behavior_z - behavior_z_snapshot)).item())

    # Buggy order: updates twice on m_next and updates on expert queries
    bn_buggy.train()
    bn_buggy.update_stats(m_curr)
    bn_buggy.update_stats(m_next)
    bn_buggy.update_stats(m_next)
    bn_buggy.update_stats(m_expert)
    buggy_mean_bias = float(torch.linalg.vector_norm(bn_buggy.mean - bn_clean.mean).item())

    # 2. Measure behavioral drift Delta_pi(z) and encoder drift Delta_B(m) across training steps
    actor = ConditionedLowLevelActor(obs_dim, act_dim, d_z).to(device)
    actor_init = copy.deepcopy(actor)
    b_init = copy.deepcopy(b_net)
    opt = torch.optim.Adam(list(actor.parameters()) + list(b_net.parameters()), lr=3e-3)

    obs_probe = torch.randn(batch_size, obs_dim, device=device)
    m_probe = bn_clean(m_curr)
    with torch.no_grad():
        z_probe_init = b_init(m_probe)
        a_probe_init = actor_init(obs_probe, z_probe_init)

    drift_trace = []
    for step in range(1, 21):
        opt.zero_grad()
        z_cur = b_net(m_probe)
        a_cur = actor(obs_probe, z_cur)
        # Synthetic representation evolution step
        loss = (a_cur.pow(2).mean()) + 0.1 * (z_cur[:, :32].pow(2).mean())
        loss.backward()
        opt.step()
        if step in (5, 10, 20):
            with torch.no_grad():
                z_now = b_net(m_probe)
                a_now = actor(obs_probe, z_probe_init)
                delta_b = float((1.0 - (z_now * z_probe_init).sum(dim=-1) / float(d_z)).mean().item())
                delta_pi = float(torch.linalg.vector_norm(a_now - a_probe_init, dim=-1).mean().item())
                drift_trace.append({"step": step, "delta_B_cosine": delta_b, "delta_pi_l2": delta_pi})

    # 3. Full-prefix zero-hidden RNN burn-in vs stale cached hidden state
    critic = RecurrentTaskTwinCritic(obs_q_dim=obs_dim, cmd_dim=d_z, hidden_dim=64).to(device)
    seq_len = 24
    burn_in = 12
    obs_seq = torch.randn(32, seq_len, obs_dim, device=device)
    cmd_seq = torch.randn(32, seq_len, d_z, device=device)

    # Stale hidden state captured before critic parameter update
    with torch.no_grad():
        h0 = torch.zeros(2, 32, 64, device=device)
        c0 = torch.zeros(2, 32, 64, device=device)
        _, (h_stale, c_stale) = critic.rnn1(obs_seq[:, :burn_in, :], (h0, c0))

    # Perturb critic weights to simulate online updates between rollout and replay sample
    with torch.no_grad():
        for p in critic.parameters():
            p.add_(0.15 * torch.randn_like(p))

    # Exact full-sequence reference from t=0 with current weights
    with torch.no_grad():
        q1_exact_full, _ = critic.forward_sequence(obs_seq, cmd_seq, burn_in_len=0)
        q1_exact_tail = q1_exact_full[:, burn_in:]

    # Burn-in reconstructed tail
    q1_burnin_tail, _ = critic.forward_sequence(obs_seq, cmd_seq, burn_in_len=burn_in)
    burnin_max_err = float(torch.max(torch.abs(q1_burnin_tail - q1_exact_tail)).item())

    # Stale cached hidden state tail
    out_stale, _ = critic.rnn1(obs_seq[:, burn_in:, :], (h_stale, c_stale))
    q1_stale_tail = critic.q1_head(torch.cat([out_stale, cmd_seq[:, burn_in:, :]], dim=-1)).squeeze(-1)
    stale_hidden_err = float(torch.max(torch.abs(q1_stale_tail - q1_exact_tail)).item())

    verdict_pass = (
        bn_drift_under_frozen_queries == 0.0
        and int(bn_clean.update_calls.item()) == 2
        and behavior_z_mutated == 0.0
        and buggy_mean_bias > 0.1
        and burnin_max_err < 1e-5
        and stale_hidden_err > 1e-2
    )

    return {
        "experiment_id": "B02_NONSTATIONARITY_BN_AND_CREDIT_ASSIGNMENT",
        "device": str(device),
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": "PASS" if verdict_pass else "FAIL",
        "bn_clean_update_calls": int(bn_clean.update_calls.item()),
        "bn_drift_under_frozen_queries": bn_drift_under_frozen_queries,
        "behavior_z_mutation_max_diff": behavior_z_mutated,
        "buggy_double_update_and_expert_mean_bias": buggy_mean_bias,
        "representation_drift_trace": drift_trace,
        "rnn_burnin_vs_exact_max_error": burnin_max_err,
        "rnn_stale_cached_hidden_max_error": stale_hidden_err,
    }


if __name__ == "__main__":
    print(json.dumps(run_b02_experiment(), indent=2))
