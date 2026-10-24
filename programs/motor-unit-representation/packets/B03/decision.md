# Packet B03 Decision — Rank-16 Bilinear Bottleneck Across 144 Morphology-Stroke Regimes and Orthonormalization Regularization

- **Decision ID**: `D-B03-001`
- **Packet ID**: `B03`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (Order 1: `P=A, Q=B`): `packets/B03/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B03/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B03/spikes/B03-SPIKE/VERDICT.json` (`PASS`, CPU; reused after Step-1 freeze)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `83.25 / 100.0` | `76.0 / 100.0` (as Q) | **79.625 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `75.75 / 100.0` | `72.0 / 100.0` (as P) | **73.875 / 100.0** |

- **Winning Track**: **Proposal A (`claude` Opus)** by mean margin **+5.750** (≥ tie margin `5.0`).
- **Order notes**: Order 1 recommends P(=A) by `+7.50` (clears win). Order 2 recommends Tie with Q(=A) leading by `+4.0` inside the margin; carrier preference Q(=A). Cross-order mean clears the win threshold for A.
- **Disposition**: **`Recommend: Proposal A` with Mandatory Merges from Proposal B and Blind Reviews**.

---

## 2. Key Adjudication Findings & Mandatory Merges

1. **Core math (base = Proposal A)**:
   - Adopt A's Ky Fan floor (Theorem 1), Corollary 1a (F-conditioning cannot lower the right-span floor), and Corollary 1b / `C-B03-A-01` as a **conditional** lemma under explicit regularity assumptions (pooled HS reference; distinct lever-arm shells). Do **not** lock the numeric `0.745` figure or the absolute claim “H3 unreachable as V3 is specified” until a premise audit on the calibrated V3 reference is filed.
   - Adopt Theorem 2: configuration-matched FB reference measure removes the cross-shell orthogonality floor and turns per-configuration isotropy / rank into an identification requirement.
   - Merge B's exact length-congruence / shared-right-span spectral-tail statements into the same conditional rank-floor claim family.

2. **Orthonormalization / Audit Issue #7**:
   - Replace unhinged exact-isotropy `(Û_k − 16)` with a **rank-floor hinge** (e.g. `(Û_k − 256/13)_+` or isotropy only on the 15-D subspace orthogonal to any linear λ-anchor). Resolves Σ→I vs tip-scale decode conflict flagged by both adjudicators.
   - Adopt B's hierarchical IPW with 10% direct target-law mixture (weights bounded ≤10 without biased clipping), `INSUFFICIENT_SUPPORT` instead of silent stratum drop, and two-batch cross estimator; keep A's within-block stratified U-statistic as an allowed alternate plug-in.
   - Synchronize FB negative sampling with configuration-matched `ν_k`.

3. **Nondimensionalization `T_κ` + tip preservation**:
   - Adopt A's parameter-free invertible `T_κ` (divide tip block by `ρ̂`, allometric time factor, write `λ = log(ρ̂/ρ_ref)` into the dead `v_tip,z` slot) with training-only λ-anchor (or subspace-orthogonal orth if anchor retained).
   - Merge B's `SCHEMA_INCOMPATIBLE` guards, centered effective-rank checks, and length-relative tip decoding thresholds.
   - Ablation hygiene: isolate `T_κ` from normalizer fitting and from the λ-anchor (`A3` vs `A4-λ`).

4. **Spike protocol repairs (mandatory before locking H3)**:
   - Common physical outcome dictionary across strokes (no manufactured 144×N disjoint cells by config ID; no coarse pooled dictionary that is blind to length or floor-bound). Report pooled-reference and configuration-matched errors separately.
   - Fix G3 to test pooled-reference algebraic consistency; remove invalid `ε_cm ≥ 0.70` requirements and “W must fail” gating.
   - Hold out geometry seeds completely from FB / orth / anchor / κ / normalizer; cycle only over training seeds.
   - Existing CPU `B03-SPIKE` VERDICT (`PASS`: worst nondim erank ≥12, tip decode retains lever arm) is retained as **Candidate-level** mechanism verification. Full H3 lock requires re-run after B02 collector integration + the repaired protocol above.

5. **Hard constraints preserved**: `d_z=16`; deployed budget `281,617`; `B_ω`/`π_θ` proprioception-only; zero new deployed parameters from `T_κ` / IPW / hinges.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B03-A-01` / `C-B03-P-01` (Order1) / `C-B03-Q-01` (Order2)**: `Candidate` Grade 1 — ACCEPT AS CONDITIONAL LEMMA (tighten premises; do not lock 0.745 / “H3 impossible”).
- **`C-B03-A-02`**: `Candidate` Grade 1 — ACCEPT WITH TIGHTNESS CORRECTION; merge with B's pooled-isotropy-cannot-certify-conditional-resolution claim.
- **`C-B03-A-03`**: Downgrade from “obligatory” to **testable hypothesis** until sphere-projected feature model is repaired or A3 vs A4 spike decides.
- **`C-B03-B-01`**: `Candidate` Grade 1 — ACCEPT WITH overlap-boundary amendment; merge into conditional per-group measurement claim.
- **`C-B03-B-02`**: `Candidate` Grade 1 — ACCEPT / MERGE into shared rank-floor statement.
- **`C-B03-B-03`**: `Candidate` Grade 1 — ACCEPT ON NARROW PREPROCESSING SCOPE.

---

## 4. Empirical Verification Summary (`B03-SPIKE`)

Reused `packets/B03/spikes/B03-SPIKE/VERDICT.json` (`PASS`, device `cpu`, `elapsed_sec≈0.93`):

- G1 worst nondim erank ≥ 12: `PASS` (`worst≈13.58`)
- G2 global raw collapse check: `PASS` (`worst_raw≈10.29`)
- G3 tip decode retains lever arm: `PASS` (`tip_rmse≈0.223` vs ang-only `≈0.954`)
- Summary: `mean_erank_raw≈11.62`, `mean_erank_nd≈13.78`

Status: Candidate-level surrogate evidence supporting nondimensionalization + stratified capacity diagnostics. Not yet a lock of Charter H3 under the repaired protocol.
