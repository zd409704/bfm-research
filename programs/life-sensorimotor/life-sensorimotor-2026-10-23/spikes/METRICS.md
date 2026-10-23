# S0a METRICS

Run: attempt 2 of max 3 (attempt 1 was FAIL; see runs.log and deviations.md).

Verbatim JSON verdict line (also the last line of runs.log):

```json
{"metric": "discriminating_latency_sweep", "threshold": "tau<=5ms peak<=0.01 AND tau>=15ms peak>0.01", "fixture_A_peaks": {"2": {"0": 0.005517037668933026, "1": 0.005523117807014134, "2": 0.005546855115887719}, "5": {"0": 0.0075200071960854955, "1": 0.0075353043790616055, "2": 0.007550524893934129}, "8": {"0": 0.010795542423835859, "1": 0.01080983207273388, "2": 0.010817335814347944}, "9.5": {"0": 0.022093849997547002, "1": 0.022081250416703998, "2": 0.022173481426451737}, "10": {"0": 0.025055232944359594, "1": 0.025023758839973223, "2": 0.025031578880800667}, "12": {"0": 0.038590125319057755, "1": 0.038507957746963785, "2": 0.0384543796170672}, "15": {"0": 0.0574001905881876, "1": 0.05741194385130749, "2": 0.05742254070411094}, "20": {"0": 0.08282377777659555, "1": 0.08278861991193864, "2": 0.0828264334321471}}, "open_loop_peaks_min": 1.071517289228084, "L_star_ms": 9.531, "L_star_lip_ms": 9.838, "a_lip": 3.302, "lip_formula": "L*=ln(1+a*b/D)/a, b=0.01, D=1", "flag": "NONE", "verdict": "PASS"}
```

Verdict: PASS. This validates only the amended scalar discrimination harness. The packet decision stays Provisional regarding hardware transfer.
Fixture B is observation only: L*_LIP = 9.838 ms, so no POLICY_50HZ_MAY_SUFFICE flag (it is not above 20 ms).
