# Research Queue: FB Reinforcement Learning Beyond Imitation Data and Model-Based Acceleration

**Program**: `fb-beyond-imitation-acceleration`
**Portfolio Order**: #1 (Primary Queue Target)
**Execution State**: `COMPLETED` (All 5 Packets `B01`–`B05` completed through Step 6 Synthesis & Ledger, including Google Colab NVIDIA L4 GPU verification in `gpu_experiments/colab_gpu_results_cuda.json`).

| Order | Packet ID | Brief Path | Title | Winning Track / Disposition | Mean Score (B vs A) | Spike & L4 GPU Verdict | Status |
|---:|---|---|---|---|---|---|---|
| 1 | `B01` | `briefs/B01-fb-density-gram-geometry-and-intrinsic-reward-identifiability.md` | FB Density Factorization, Gram Matrix Conditioning, and Intrinsic Reward Identifiability | Proposal B (`codex` `gpt-6-astra`) + Merges (`D-B01-001`) | `85.5` vs `74.5` (`+11.0` B) | `PASS` (`18.56x`/`12.26x` L4 GPU MSE reduction) | `DONE` |
| 2 | `B02` | `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md` | Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment in Joint FB + Task-Q + Planner Training | Tie / Hybrid Co-Design (`Proposal B` lead base, `D-B02-001`) | `80.75` vs `79.25` (`+1.50` B) | `PASS` (`0.0` BN/relabel drift, `0.0` L4 burn-in err) | `DONE` |
| 3 | `B03` | `briefs/B03-motion-only-backward-map-under-contact-and-terrain-aliasing.md` | Motion-Only Backward Map Aliasing and Privileged/Perceptive Compensation in Contact-Rich Tasks | Tie / Hybrid Co-Design (`Proposal A` lead base, `D-B03-001`) | `72.5` vs `75.0` (`+2.50` A) | `PASS` (`6.80e-4` perceptive MSE vs `0.9105` floor) | `DONE` |
| 4 | `B04` | `briefs/B04-pathwise-world-model-gradients-vs-fb-successor-derivatives-ablation.md` | Pathwise World-Model Gradients vs First-Action FB Successor Derivatives: Controlled 4-Arm Ablation and Hybrid Horizon Design | Tie / Hybrid Co-Design (`Proposal A` lead base, `D-B04-001`) | `77.0` vs `77.5` (`+0.50` A) | `PASS` (`414,771 steps/s` L4; `H=8..16` sweet spot) | `DONE` |
| 5 | `B05` | `briefs/B05-obstacle-traversal-r2-terminal-boundary-and-curriculum-verification.md` | Autonomous 3D Obstacle Traversal R2.1 Terminal Boundary (`severe_penetration` vs `invalid`) and Multi-Height Curriculum Verification | Proposal B (`codex` `gpt-6-astra`) + Merges (`D-B05-001`) | `83.0` vs `63.0` (`+20.0` B) | `PASS` (`invalid > severe_penetration`, `4096` quotas) | `DONE` |
