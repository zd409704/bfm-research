# Stage-2 runner

Scaled full-physics smoke for H1–H4, plus the Colab notebook `colab_stage2_runner.ipynb`.

The merge norms are implemented in `../codebase/unit_bfm/v3/stage2_norms.py`. This directory re-exports them and runs the gate plant.

```bash
python3 run_stage2.py --output stage2_results.json
```

`scientific_lock` in the JSON stays false. Read `../STAGE2_STATUS.md` before treating a PASS as a charter result.
