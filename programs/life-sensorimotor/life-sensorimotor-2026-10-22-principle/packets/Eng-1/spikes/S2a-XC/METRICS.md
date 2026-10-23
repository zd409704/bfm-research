# METRICS — S2a-XC spike (PLAN v2)

Verdict: **FAIL** (harness_pass=True; A02=False). Fired: A02, SUB_DOWN_NOT_MET. Harness validity only; no claim grade changes. `(q, r)` is PLACEHOLDER.

Units: `r_w = 0.001` per 100 ms window = registered 0.01 /s; `r_w = 0.005` = 0.05 /s. d_cert in bits. Coverage pointwise; Bonferroni fields in floor-cert/.

## Harness

- H1 determinism: True
- H2 null coverage: True
- H3 oracle: True
- H4 non-interference: True

## Calibration (thresholds/exceed counts)

- R1_CMD: drift=0.3538377195; r0.001: thr=5.6895556665 k*=3; r0.005: thr=4.97203795 k*=36
- R2_CMD: drift=0.3459968037; r0.001: thr=2.2163603376 k*=3; r0.005: thr=1.8549754702 k*=36
- R1_REAL_DOWN: drift=0.3279372505; r0.001: thr=3.6944030059 k*=3; r0.005: thr=2.9156912516 k*=36
- R1_REAL_UP: drift=0.0184277597; r0.001: thr=1.5579335262 k*=3; r0.005: thr=1.274089991 k*=36
- R2_REAL_DOWN: drift=0.3223428456; r0.001: thr=2.0757165611 k*=3; r0.005: thr=1.6865827348 k*=36
- R2_REAL_UP: drift=0.0517277854; r0.001: thr=1.6443245211 k*=3; r0.005: thr=1.3735460696 k*=36
- ORACLE_R1: drift=0.023556535; r0.001: thr=0.2766217117 k*=3; r0.005: thr=0.2350767926 k*=36

## TPR_hat / TPR_L / p95 latency by class at r_w=0.001 (0.01/s), pooled 3 seeds

| detector | d5M2 | d5M5 | d5M10 | d10M2 | d10M5 | d10M10 | d20M2 | d20M5 | d20M10 | d50M2 | d50M5 | d50M10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1_CMD TPR | 0.000 | 0.001 | 0.004 | 0.001 | 0.014 | 0.115 | 0.005 | 0.156 | 0.587 | 0.112 | 0.627 | 0.874 |
| R1_CMD d_cert bits | 0.00 | 0.00 | 0.01 | 0.00 | 0.04 | 0.76 | 0.01 | 1.11 | 5.72 | 0.73 | 6.21 | 9.52 |
| R1_CMD p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf |
| R2_CMD TPR | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.003 | 0.001 | 0.002 | 0.035 | 0.002 | 0.043 | 0.335 |
| R2_CMD d_cert bits | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.14 | 0.00 | 0.19 | 2.67 |
| R2_CMD p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf |
| R1_REAL_DOWN TPR | 0.000 | 0.000 | 0.007 | 0.001 | 0.033 | 0.275 | 0.016 | 0.320 | 0.734 | 0.247 | 0.752 | 0.936 |
| R1_REAL_DOWN d_cert bits | 0.00 | 0.00 | 0.01 | 0.00 | 0.13 | 2.09 | 0.05 | 2.52 | 7.15 | 1.83 | 7.38 | 9.93 |
| R1_REAL_DOWN p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf |
| R1_REAL_UP TPR | 0.001 | 0.019 | 0.510 | 0.034 | 0.682 | 0.928 | 0.610 | 0.943 | 1.000 | 0.904 | 1.000 | 1.000 |
| R1_REAL_UP d_cert bits | 0.00 | 0.05 | 4.33 | 0.12 | 6.25 | 9.45 | 5.42 | 9.69 | 10.68 | 9.11 | 10.68 | 10.68 |
| R1_REAL_UP p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | 23 | inf | 33 | 23 |
| R2_REAL_DOWN TPR | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.003 | 0.001 | 0.003 | 0.042 | 0.002 | 0.056 | 0.375 |
| R2_REAL_DOWN d_cert bits | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.17 | 0.00 | 0.25 | 2.93 |
| R2_REAL_DOWN p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf |
| R2_REAL_UP TPR | 0.000 | 0.000 | 0.001 | 0.000 | 0.001 | 0.008 | 0.001 | 0.007 | 0.201 | 0.004 | 0.248 | 0.700 |
| R2_REAL_UP d_cert bits | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.01 | 1.41 | 0.00 | 1.84 | 6.72 |
| R2_REAL_UP p95 ms | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf | inf |
| ORACLE_R1 TPR | 0.623 | 0.745 | 0.773 | 0.973 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| ORACLE_R1 d_cert bits | 6.16 | 7.73 | 8.11 | 11.10 | 11.65 | 11.65 | 11.65 | 11.65 | 11.65 | 11.65 | 11.65 | 11.65 |
| ORACLE_R1 p95 ms | inf | inf | inf | 9 | 5 | 5 | 9 | 5 | 5 | 9 | 5 | 5 |

FPR_U (r_w=0.001): R1_CMD=3.07e-04, R2_CMD=4.64e-04, R1_REAL_DOWN=4.64e-04, R1_REAL_UP=6.02e-04, R2_REAL_DOWN=6.02e-04, R2_REAL_UP=4.64e-04, ORACLE_R1=3.07e-04

## Meets (pointwise), q=0.90/0.95 at own r_w=0.001 — count of 12 classes

- R1_CMD: q0.90 0/12, q0.95 0/12; Bonferroni q0.90 0/12
- R2_CMD: q0.90 0/12, q0.95 0/12; Bonferroni q0.90 0/12
- R1_REAL_DOWN: q0.90 1/12, q0.95 0/12; Bonferroni q0.90 1/12
- R1_REAL_UP: q0.90 5/12, q0.95 3/12; Bonferroni q0.90 0/12
- R2_REAL_DOWN: q0.90 0/12, q0.95 0/12; Bonferroni q0.90 0/12
- R2_REAL_UP: q0.90 0/12, q0.95 0/12; Bonferroni q0.90 0/12
- ORACLE_R1: q0.90 9/12, q0.95 9/12; Bonferroni q0.90 9/12

## C-P1-012 contrasts (data only; no grade statement)

### Placement DOWN (primary)
- Factor-E counterexample (CMD_RECON@R1 matches REAL@R1 on all d>=10): **False** (3/9 classes match); identifiable-only: False
- Factor-R counterexample (REAL@R2 matches REAL@R1 on all d>=10): **False** (3/9 classes match); identifiable-only: False
- B.9.3 substitution (identifiable=['d20_M10', 'd50_M5', 'd50_M10']): met=False, min drop=0.0625, mean drop=0.1115

### Placement UP (outside C-P1-012 premise-5 scope)
- Factor-E counterexample (CMD_RECON@R1 matches REAL@R1 on all d>=10): **False** (1/9 classes match); identifiable-only: False
- Factor-R counterexample (REAL@R2 matches REAL@R1 on all d>=10): **False** (1/9 classes match); identifiable-only: False
- B.9.3 substitution (identifiable=['d5_M10', 'd10_M5', 'd10_M10', 'd20_M2', 'd20_M5', 'd20_M10', 'd50_M2', 'd50_M5', 'd50_M10']): met=True, min drop=0.1261666667, mean drop=0.5648333333

Caveats: rate contrast is confounded with observer bandwidth (gain.T fixed); sensitivity variants in sensitivity_fixedgain.json. CMD_RECON cells are shared baselines across placements. A small substitution drop is not proof that effort information is absent.
