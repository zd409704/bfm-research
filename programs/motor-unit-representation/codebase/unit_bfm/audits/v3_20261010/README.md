Independent review of # V3 protocol audit

These scripts only perform small-scale CPU verification and do not implement V3, start training, or modify the production network.

- `check_contracts.py`: Only replace the old network input layer and check the parameter amount; numerical difference checks the local endpoint formula; shows acceleration lag and compression history counterexamples; compares the FB scalar formula and row-by-row discount broadcast; calculates the rank bound of the invariant configuration coarse-grained occupancy matrix.
- `check_reaction.py`: CPU MuJoCo reaction force comparison with site sensor, torque reference point conversion, explicit postconstraint update.
- `check_weld.py`: Counterexample of world weld moment extraction for native MuJoCo 3.8.1, independently verified with angular momentum balance and Jacobian transpose multiplied by constraint force.
- `check_motor_coordinates.py`: True zero-angle attitude difference, cross-zero position/direction physical equivalence, non-zero ref, power/limit and third-speed capability limiter check.
- `check_collection.py`: Old PD's reload retention was insufficient with round-first-then-time sampling weights.
- `check_geometry.py`: An example of the old geometric filtration of parental collisions; This does not mean that V3 wide process geometry has been completed.

Run `unit_bfm/.venv/bin/python -B unit_bfm/audits/v3_20261010/check_contracts.py` in the workspace directory, and the rest of the scripts run the same way. The result is saved in the adjacent JSON. Model version MuJoCo 3.8.1; GPU or training validation not included.

The counterexample of compression history is an algebraic test of the feature operator, which does not pretend to be a complete kinetic trajectory; the rank bound is a restriction on the precise global FB density target, not a lower bound on the strategy control error or final return.
