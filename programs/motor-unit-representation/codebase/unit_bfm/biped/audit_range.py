"""Compare this assembly with the actual saved V2 structure bank, read-only."""
import hashlib
import json

import mujoco
import numpy as np

from unit_bfm.biped.runtime import Biped, HERE
from unit_bfm.mechanics import Structure
from unit_bfm.schema import NOMINAL_FIELDS, NOMINAL_SCALES


def run():
    robot = Biped()
    bank = HERE.parent/'artifacts/rf_v2_full/models'
    records = json.loads((bank/'structures.json').read_text())
    sources, normalized = [], []
    for record in records:
        structure = Structure(**record)
        path = bank/(structure.key+'.xml')
        # Read the files used by the run; do not resample or regenerate the bank.
        model = mujoco.MjModel.from_xml_path(str(path))
        normalized.append(structure.nominal(model)[:14])
        sources.append(dict(key=structure.key, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    normalized = np.asarray(normalized)
    physical = normalized*np.asarray(NOMINAL_SCALES)
    low, high = physical.min(0), physical.max(0)
    rows = []
    for index, unit in enumerate(robot.units):
        values = robot.m[index, :14]*np.asarray(NOMINAL_SCALES)
        fields = {
            name: dict(value=float(value), bank_min=float(lo), bank_max=float(hi),
                       within_marginal_envelope=bool(lo-1e-7 <= value <= hi+1e-7))
            for name, value, lo, hi in zip(NOMINAL_FIELDS, values, low, high)
        }
        matches = [source['key'] for source, error in zip(sources, np.max(np.abs(normalized-robot.m[index, :14]), axis=1))
                   if error <= 1e-6]
        rows.append(dict(**unit, nominal_fields=fields, exact_m28_matches_in_saved_bank=matches,
                         geometry_family='uniform_0.04_m_square_rod',
                         P_COM_along_joint_axis_offset_m=-unit['xyz'][1]))
    report = dict(
        design_version=robot.config['version'],
        urdf_sha256=hashlib.sha256((HERE/'models/biped_4dof.urdf').read_bytes()).hexdigest(),
        reference_run=str(bank.parent.resolve()), reference_bank_size=len(records),
        reference='Saved V2 XMLs compiled with MuJoCo; scalar nominal envelopes only.',
        scalar_nominal_field_envelope_passed=all(f['within_marginal_envelope'] for r in rows for f in r['nominal_fields'].values()),
        joints=rows, saved_model_sources=sources,
        local_generator_verification='compatibility.json',
        full_training_distribution_match=False,
        remaining_composition_differences=[
            'Two hips share one rod torso; each thigh belongs to both a hip and a knee unit.',
            f"Hip joint origins are spaced by {2*robot.config['hip_half_spacing_m']:.2f} m along y. Planar mass/gravity equivalence is checked separately; collision sets are not identical.",
            'Ground contact and multiple neighboring learned controllers occur simultaneously, unlike the original separate R2/R3 roles.'
        ],
        simulator_settings_implemented_in=['models/biped_4dof.xml', 'runtime.py'],
        urdf_velocity_limit_note='12 rad/s is metadata only; the companion simulator does not enforce this extra speed limit.',
        note='Envelope inclusion is not exact finite-bank reuse or proof of policy capability. See compatibility.json for geometry, timing and integration checks.',
        walking_validated=False)
    (HERE/'range_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(bank_size=len(records), scalar_envelope_passed=report['scalar_nominal_field_envelope_passed'],
                         exact_matches={r['joint']: r['exact_m28_matches_in_saved_bank'] for r in rows}), indent=2))
    return report


if __name__ == '__main__':
    run()
