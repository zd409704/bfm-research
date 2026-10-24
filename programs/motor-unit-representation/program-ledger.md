# Program Ledger — `motor-unit-representation`

**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Freeze Epoch**: `1792809557`
**Owner Authorization**: User message t86u (2026-10-24) authorized launch from `HALTED` / `READY_NOT_STARTED` to `IN_PROGRESS`.

## Inherited Baseline Snapshot

| ID | Statement | Source |
|---|---|---|
| `X-BASE-001` | Deployed modules are proprioception-only: \(B_\omega(g_{13})\), \(\pi_\theta(x_{137}, z_{16})\); total `281,617` parameters. | `baseline/01`, `baseline/02` |
| `X-BASE-002` | Training-only dual forwards \(F_{\eta_1,\eta_2}\) read \(x_{137}+p_{5065}+a+z_{16}\) (`5,891,633` total online params). | `baseline/02` |
| `X-BASE-003` | Privileged context \(p_{5065}\) has 22 schema groups (`4,822` physical + `243` memory); Groups 18–21 carry Audit Issue #4 future-force leakage risk. | `baseline/02` §2.3, `baseline/03` Issue #4 |
| `X-BASE-004` | Short-run V3 smoke: `8,096` transitions, `101` updates, `coverage_ready=false`, zero-vel RMSE `5.89–13.88 rad/s`. | `baseline/03` |
| `X-BASE-005` | Nine open audit issues (#1–#9) block full-scale V3 training; Rank-16 vs 144-config Eckart-Young floor \(\approx 0.943\) if unconditioned. | `baseline/02` §6, `baseline/03` |

## Packet Decisions

### Packet `B01` Decisions & Claims
- `D-B01-001` (`packets/B01/decision.md`, `synthesis/B01-synthesis.md`): Selected Proposal A (`claude` Opus, mean `82.025/100`) over Proposal B (`codex` `gpt-6-astra`, mean `76.95/100`) by cross-family order-swapped adjudication (`agy` Order1 Tie-band with A primary `87.05` vs `82.90`; `claude` `sonnet` Order2 A win `77` vs `71`), with Mandatory Merges from Proposal B (manifest join, Group-18 layout, EXO-PREVIEW / `F_c` spike controls) and blind reviews (Theorem 2(a) sufficiency repair, composed G-1 ratio). Pre-registered spike `B01-SPIKE` passed on CPU (`leak_ratio≈12.97`, `causal_ratio≈0.012`, Bellman bias reduction `≈9.77×`).
- Claims `C-B01-A-01`..`A-03`, `C-B01-B-01`..`B-02`: Candidate with tighten-premises / stay as listed in `decision.md` §3.

### Packet `B02` Decisions & Claims
- `D-B02-001` (`packets/B02/decision.md`, `synthesis/B02-synthesis.md`): **Tie / Hybrid** — Proposal A mean `74.50/100`, Proposal B mean `79.00/100` (Δ`4.50` < tie margin `5.0`). Order1 `agy` exact tie `78/78` (A primary generative / B co-primary storage-gate); Order2 `sonnet` recommends B (`80` vs `71`). Mandatory merges: Philox `make_program` + A's interval tables; alternating load sign; delayed-κ rule law; joint 720-cell gate; dual BN + pre-activation hinge; canonical `g_hold` with negative/positive controls. Spike `B02-SPIKE` `PASS` (`coverage_ready=true`, hold RMSE ≪ 0.35).
- Claims `C-B02-A-01`..`A-02`, `C-B02-B-01`..`B-02`: Candidate Grade 1 with narrowed scope / revise-premise as in `decision.md` §3.

### Packet `B03` Decisions & Claims
- `D-B03-001` (`packets/B03/decision.md`, `synthesis/B03-synthesis.md`): Selected Proposal A (`claude` Opus, mean `79.625/100`) over Proposal B (`codex` `gpt-6-astra`, mean `73.875/100`) by mean margin `+5.750` (Order1 `agy` A win `83.25` vs `75.75`; Order2 `sonnet` Tie-band with A=`76` as Q vs B=`72` as P). Mandatory merges: conditional Ky Fan / config-matched reference lemma; rank-floor orth (not blind Σ→I); hierarchical IPW + target-law mixture; invertible `T_κ` + schema guards; repaired spike dictionary/gates. Spike `B03-SPIKE` `PASS` (CPU surrogate; H3 not yet locked).
- Claims `C-B03-A-01`..`A-03`, `C-B03-B-01`..`B-03`: Candidate with conditional / merge / hypothesis downgrade as in `decision.md` §3.

### Packet `B04` Decisions & Claims
- `D-B04-001` (`packets/B04/decision.md`, `synthesis/B04-synthesis.md`): **Tie / Hybrid** — Proposal A mean `68.5/100`, Proposal B mean `70.0/100` (Δ`1.5` < tie margin `5.0`). Order1 `agy` recommends A (`71` vs `65`, `LIMB2-v1` coupling / certificate primary); Order2 `sonnet` recommends B (`75` vs `66`, fairness / reproducibility lead). Mandatory merges: A plant + housing-transport / null-mode lemmas; B Schur reduction + numerical plant + masked `140k` params; blocking inverse-dynamics feasibility; controller-independent `IN`/`EDGE`/`OUT`; comparative `ΔS_ZS` transfer vs Baseline C on clean `3×3` grid; Grade-2 five-code diagnostics (not over-claimed necessity). Spike `B04-SPIKE` `PASS` (CPU analytic envelope + fair-ablation scaffold; H4 not locked).
- Claims `C-B04-A-01`..`A-03`, `C-B04-B-01`..`B-02`: Candidate with partial-accept / accept / downgrade-to-audit-gate as in `decision.md` §3.
