"""Exported field order and units; no hidden state is part of this contract."""
OBSERVATION_FIELDS = [
    'q', 'dq', 'P_sin_pitch', 'P_cos_pitch', 'P_COM_vx', 'P_COM_vz', 'P_omega_y',
    'D_sin_pitch', 'D_cos_pitch', 'D_COM_vx', 'D_COM_vz', 'D_omega_y',
    'tau_motor_endpoint', 'previous_u_sent', 'P_contact_any', 'D_contact_any',
    'distance_to_lower_limit', 'distance_to_upper_limit',
    'P_env_Fx_mean', 'P_env_Fz_mean', 'P_env_My_COM_mean',
    'D_env_Fx_mean', 'D_env_Fz_mean', 'D_env_My_COM_mean',
]
OBSERVATION_SCALES = [1.2, 6., 1., 1., 2., 2., 6., 1., 1., 2., 2., 6.,
                      6., 1., 1., 1., 2.4, 2.4, 20., 20., 6., 20., 20., 6.]
NOMINAL_FIELDS = ['P_length', 'D_length', 'P_mass', 'D_mass', 'P_Iyy', 'D_Iyy',
                  'P_COM_from_joint_x', 'P_COM_from_joint_z', 'D_COM_from_joint_x',
                  'D_COM_from_joint_z', 'q_lower', 'q_upper', 'tau_nominal', 'T_nominal']
NOMINAL_SCALES = [.4, .4, 2., 1., .1, .1, .4, .4, .4, .4, 1.2, 1.2, 6., .02]


def contract():
    return dict(observation_fields=OBSERVATION_FIELDS, observation_divisors=OBSERVATION_SCALES,
                observation_sources=dict(
                    encoder_or_encoder_estimate=['q','dq'],
                    known_command=['previous_u_sent'],
                    known_geometry_plus_encoder=['distance_to_lower_limit','distance_to_upper_limit'],
                    simulation_truth_not_generic_motor_telemetry=[
                        f for i,f in enumerate(OBSERVATION_FIELDS)
                        if i in list(range(2,13))+[14,15]+list(range(18,24))]),
                hardware_boundary='Link pose/COM velocity, exact motor torque and contact/wrench require '
                    'additional sensors or estimators; this privileged model is not a motor-only deployment model.',
                nominal_fields=NOMINAL_FIELDS, nominal_divisors=NOMINAL_SCALES,
                nominal_validity='14 corresponding valid bits appended after 14 values',
                backward_fields=[f for f in OBSERVATION_FIELDS if f != 'previous_u_sent'],
                coordinates='world x-z, +rotation about y, linear velocities at body COM',
                wrench='environment contact plus explicit external force; exclude gravity and internal joint reactions',
                slow=dict(endpoint=list(range(12))+[16,17], mean=[12,13,18,19,20,21,22,23],
                          any=[14,15], padding=24, age=25, age_divisor_s=.2),
                fast_fields=['previous_u_sent','tau_motor_endpoint','padding'],
                first_valid_fast_ms=10,first_valid_slow_ms=20,
                feedback_fields=['o24','m28','B16','actor_context128','B_valid1'])
