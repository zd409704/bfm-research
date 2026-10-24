# V3 This round of development constraints and acceptance

2026-10-10, the main window is reordered based on the user's correction to the full archive. This article takes precedence over "All episodes are permanently saved", "Compressed full trajectory" and "Incomplete coverage must not be optimized" in this round of old tasks. Do not change the network skeleton/FB; do not change V2, do not delete the existing experimental records.

# Training Main Path Must be Implemented

The simulations continue to produce effective transfers with a boundary memory of Replay (rules and distributed capacity from online sources) Minibatch FB/Actor update regular checkpoint/evaluation. The cumulative W is not Replay capacity. The default does not permanently save the entire trajectory and does not rely on disk compression/archiving as training. The CPU memory retains the necessary training sheets and then sample the bats and move the GPU. The original trajectory is limited to quantitatively defined diagnostics, examples of failures and assessments.

g13/x137/z16, F=[x,p], standard loss/target/optimizer follows the verified core. F only reads additional real conditions; do not delete p with dynamic meaning in order to make Replay smaller. Repeated constants can be reviewed based on physical necessity, and the network skeleton cannot be changed without permission.

It is initially recommended to transfer capacity rule32768 and online65536. Calculate the upper bound based on the actual p_dim (including current/next). The machine currently has about 11GiB available, and the Replay upper limit is 4GiB. When it exceeds, a clear error report/download configuration will be started. Capacity is a configurable engineering quantity, and the capacity is not set at 20M. It does not reserve two complete episodes for each of the 144 groups for unlimited expansion. The decision will be made by the main window after being verified by the discussant. Each source/scene/configuration maintains a bounded index, updates the index upon elimination, does not scan the entire database every round, and does not decompress the disk when sampling. The fixed P0 sub-library also has a fixed capacity; the cumulative P0 collection budget can be greater than the retention amount, and the hierarchical retention coverage is not selected based on success.

To read the recent actor history and the necessary F memory, you only need to effectively transfer the correct pairing; training does not rely on a complete episode archive. Keep it during the online z call, the next call uses the current acquisition snapshot B; the learning goal is always recoded to the current B; there is no cross-version z target cache.

Project operation threshold = physical legality, correct input source/timing, limited gradient, and Replay can correctly sample. Coverage is the basis for continuous statistics/replenishment and final capacity acceptance. Legal transfer optimization cannot always be avoided because rare states are not covered. When source/scene/config is not populated, pre-populate the required groups for a short time or explicitly record the current distribution; do not pretend to be full rho, and do not use the hardcoded false switch to permanently block full.

The startup phase can start with online warmup after pre-filling the rules, maintaining the rules/online 50/50 baseline, current layered rho and updated budget; the large-scale P0 budget and 20M are formal experimental configurations and are not the minimum number of steps for all development checks. No new rewards/imitation/regression losses will be added.

The checkpoint retains the online /targets/optimizers/RNG/scheduler and current bounded Replay status. A full restore is explicitly different from a model-only warm start, and reliance on deprecated archives is prohibited. It can be saved at the rollout boundary, indicating whether it is restored accurately; the snapshot pool restores the physical state and history padding of the same model, and distinguishes checkpoint continuation training.

## File ownership and roles

- physics development: physics/mechanics/randomization/privileged/warp_backend/kernels/test_physics* and its own handoff. Only fix physical correctness, sampling conditions and runnable backend; do not edit training/network.
- Pipeline development: replay/collect/train/programs/coverage/queries/evaluate/interface/configs/test_pipeline* and its own handoff. Rebuild the above training main path without expanding the archive system.
- core discussion/audit: code read-only. Review training decisions first with capacity, rho, P0, history/state boundaries; then independently review implementation. Only write your own discussion audit documentation.
- Main window: determine the interface and scope, maintain the acceptance record of this document/README/, independent regression/integration/GPU test; do not compete with development agents.

GPU monopolized window; agents CPU. All angent high, follow the original play session. Three states are separated for start-up/submission/ acceptance. Developer must first prepare a short implementation list, anticipate RAM/need for API, and then complete the agreed scope; The probability of a network/loss/sampling need to be modified should be identified first to the main window programme and not adapted.

## This round of acceptance

1. The V2 benchmark hash/weight stat is unchanged, and no V2 training code is imported.
2. Physical regression: 100 random configuration initialization is legal, reset support parameters and ground distance F can be distinguished, failure isolation, same solve force/coordinate, mechanical P/D semantics, real parameter randomization and event loading release.
3. After Replay is written far beyond the capacity, RAM/active transfer is stable and there is no permanent episode growth; sampling rho can be explained, invalid does not enter the gradient, goal matches, and eliminated samples are not returned; minibatch sampling does not trigger disk decompression.
4. Real simulation collection, rules + online transfer are all used in FB, continuous updates, checkpoint recovery, Actor/B independent export and evaluation are all executable.
5. Real GPU/CPU pairing, batch acquisition and small-scale CUDA learning are run from the main window. Reports throughput and limitations, does not replace available acquisitions with "GPU class exists".
README may execute orders consistent with the actual realization. Short training certified the work and did not claim that the control skills or the complete 20M experiment had been completed.

## The precise definition of partial / strict in the main window

Training can be clearly recorded in the current effective distribution of training: when the config/bin is missing, the actual existence of the group is re-normalized, called partial; the "all expected configs are resident" is no longer a prerequisite for updating. The `strict=True` public contract should still reject the missing required group for independent integrity acceptance and cannot return formal = true and fallback = true but claim to be complete. The training entrance explicitly selects the partial and reports the revision/actual group weights; the query pool uses the same time point rho. Buffer capacity is not enough to keep each set of full episodes is not an error, just transfer hierarchical retention/bounded indexes one by one. History must be generated correctly at the time of acquisition and not preserved by episode disks.

## Main window ruling after discussion

Adopt the explicit current/next FP32 solution in v3-rl_design_review; start calculating RAM according to the real schema and retain the 4GiB hard budget. The rule capacity of 32768 is divided into 16384 fixed P0 anchor points + 16384 rolling rules, and 65536 are online. After P0 ends, the anchor point freezes; new rules enter the rolling area; sampling still treats the two as rule sources and stratifies them uniformly, without adding a third source or setting an internal 50/50 weight. The P0 large budget stage can be used to declare hierarchical reservations and not filter by success. Development of small configurations can be scaled down in the same proportion.

Before learning is started, ensure that both rules/policy sources are effectively transferred, and maintain the 50/50 source target; if the scene/config is not updated and reported according to the public partial distribution, single-source implicit learning will not be performed. Query pool adds Replay instance/content generation identity. You cannot just use group name and revision.

the checkpoint boundary is paused to avoid writing to the deepcopy library; the active array is saved, and the full-capacity empty slots are not saved; the direct takeover or release from library to library is resumed to avoid three buffers residing at the same time. By default, only the latest two complete checkpoints are scrolled, and the final output is saved as a small number of diagnostics; some historical experimental files are not cleaned up.
