"""Read the URDF, verify its rigid-body tree/inertias/FK, export preview data."""
from pathlib import Path
import hashlib
import itertools
import json
import xml.etree.ElementTree as ET

import mujoco
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'models' / 'biped_4dof.urdf'


def vector(text, default='0 0 0'):
    return [float(x) for x in (text or default).split()]


def origin(element):
    item = element.find('origin')
    return dict(xyz=vector(item.get('xyz')) if item is not None else [0., 0., 0.],
                rpy=vector(item.get('rpy')) if item is not None else [0., 0., 0.])


def rotation(rpy):
    r, p, y = rpy
    cr, cp, cy = np.cos(rpy)
    sr, sp, sy = np.sin(rpy)
    return np.array([[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr],
                     [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr],
                     [-sp, cp*sr, cp*cr]])


def transform(o):
    t = np.eye(4)
    t[:3, :3] = rotation(o['rpy'])
    t[:3, 3] = o['xyz']
    return t


def forward(model, angles):
    poses = {model['root']: np.eye(4)}
    pending = list(model['joints'])
    while pending:
        ready = [j for j in pending if j['parent'] in poses]
        if not ready:
            raise ValueError('Cycle or disconnected joint tree')
        for j in ready:
            assert j['axis'] == [0., 1., 0.]
            r = transform(dict(xyz=[0, 0, 0], rpy=[0, angles[j['name']], 0]))
            poses[j['child']] = poses[j['parent']] @ transform(j['origin']) @ r
            pending.remove(j)
    return poses


def read_model():
    root = ET.parse(SOURCE).getroot()
    materials = {m.get('name'): vector(m.find('color').get('rgba')) for m in root.findall('material')}
    links = []
    for link in root.findall('link'):
        inertial = link.find('inertial')
        i = inertial.find('inertia').attrib
        matrix = [[float(i['ixx']), float(i['ixy']), float(i['ixz'])],
                  [float(i['ixy']), float(i['iyy']), float(i['iyz'])],
                  [float(i['ixz']), float(i['iyz']), float(i['izz'])]]
        record = dict(name=link.get('name'), mass=float(inertial.find('mass').get('value')),
                      inertial_origin=origin(inertial), inertia=matrix, visuals=[], collisions=[])
        for kind, key in [('visual', 'visuals'), ('collision', 'collisions')]:
            for element in link.findall(kind):
                shape = next(iter(element.find('geometry')))
                geometry = dict(type=shape.tag)
                if shape.tag == 'box':
                    geometry['size'] = vector(shape.get('size'))
                elif shape.tag == 'cylinder':
                    geometry.update(radius=float(shape.get('radius')), length=float(shape.get('length')))
                else:
                    raise ValueError(f'Unsupported preview geometry: {shape.tag}')
                entry = dict(name=element.get('name'), origin=origin(element), geometry=geometry)
                material = element.find('material')
                if material is not None:
                    entry['material'] = material.get('name')
                record[key].append(entry)
        links.append(record)
    joints = []
    for j in root.findall('joint'):
        assert j.get('type') == 'revolute'
        joints.append(dict(name=j.get('name'), type=j.get('type'),
                           parent=j.find('parent').get('link'), child=j.find('child').get('link'),
                           origin=origin(j), axis=vector(j.find('axis').get('xyz')),
                           limit={k: float(v) for k, v in j.find('limit').attrib.items()},
                           dynamics={k: float(v) for k, v in j.find('dynamics').attrib.items()}))
    names = {l['name'] for l in links}
    assert len(names) == len(links) == 5 and len(joints) == 4
    children = [j['child'] for j in joints]
    assert len(set(children)) == len(children)
    assert all(j['parent'] in names and j['child'] in names for j in joints)
    roots = names - set(children)
    assert roots == {'pelvis'}
    return dict(name=root.get('name'), root='pelvis', source=str(SOURCE),
                sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                links=links, joints=joints, materials=materials,
                total_mass=sum(l['mass'] for l in links),
                presets={'straight': [0., 0., 0., 0.],
                         'crouch': [-.25, .50, -.25, .50],
                         'left_clearance': [-.65, 1.1, 0., 0.],
                         'right_clearance': [0., 0., -.65, 1.1]})


def verify(model):
    for link in model['links']:
        assert link['mass'] > 0
        eig = np.linalg.eigvalsh(link['inertia'])
        assert (eig > 0).all() and eig[-1] <= eig[:2].sum() + 1e-12
        parts = zip([.9, .1] if link['name'] == 'pelvis' else [link['mass']], link['collisions'])
        center = np.asarray(link['inertial_origin']['xyz'])
        expected = np.zeros((3, 3))
        center_sum = np.zeros(3)
        for mass, geom in parts:
            a, b, c = geom['geometry']['size']
            pos = np.asarray(geom['origin']['xyz'])
            delta = pos - center
            expected += mass/12*np.diag([b*b+c*c, a*a+c*c, a*a+b*b])
            expected += mass*((delta @ delta)*np.eye(3)-np.outer(delta, delta))
            center_sum += mass*pos
        np.testing.assert_allclose(center_sum/link['mass'], center, atol=1e-12)
        np.testing.assert_allclose(expected, link['inertia'], atol=1e-12)
    assert abs(model['total_mass'] - 2.5) < 1e-12
    # Keep the root body for name-based FK comparison. This compiler option is
    # applied only to the validation import, not to the portable URDF file.
    root = ET.parse(SOURCE).getroot()
    compiler = ET.SubElement(ET.SubElement(root, 'mujoco'), 'compiler')
    compiler.set('fusestatic', 'false')
    mj = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding='unicode'))
    data = mujoco.MjData(mj)
    assert mj.njnt == mj.nq == 4
    assert abs(mj.body_mass.sum() - 2.5) < 1e-12
    rng = np.random.default_rng(20261001)
    cases = list(model['presets'].values()) + rng.uniform(-1.2, 1.2, (32, 4)).tolist()
    max_pos_error = max_rot_error = 0.
    for values in cases:
        angles = dict(zip([j['name'] for j in model['joints']], values))
        poses = forward(model, angles)
        for name, value in angles.items():
            data.qpos[int(mj.joint(name).qposadr[0])] = value
        mujoco.mj_forward(mj, data)
        for name, pose in poses.items():
            body = mj.body(name).id
            max_pos_error = max(max_pos_error, float(np.max(np.abs(data.xpos[body] - pose[:3, 3]))))
            max_rot_error = max(max_rot_error, float(np.max(np.abs(data.xmat[body].reshape(3, 3) - pose[:3, :3]))))
    assert max_pos_error < 1e-10 and max_rot_error < 1e-10
    poses = forward(model, dict.fromkeys([j['name'] for j in model['joints']], 0.))
    vertices = []
    for link in model['links']:
        for geom in link['collisions']:
            t = poses[link['name']] @ transform(geom['origin'])
            for signs in itertools.product([-1, 1], repeat=3):
                p = np.r_[np.asarray(signs)*np.asarray(geom['geometry']['size'])/2, 1.]
                vertices.append((t @ p)[:3])
    vertices = np.asarray(vertices)
    dimensions = vertices.max(0) - vertices.min(0)
    np.testing.assert_allclose(dimensions, [.04, .16, .85], atol=1e-12)
    return dict(source_sha256=model['sha256'], status='geometry_and_kinematics_verified',
                mujoco_version=mujoco.__version__, links=5, actuated_joints=4,
                mass_kg=model['total_mass'], straight_collision_extent_m=dimensions.tolist(),
                fk_pose_cases=len(cases), fk_max_position_error_m=max_pos_error,
                fk_max_rotation_error=max_rot_error,
                physics_stepped=False, walking_validated=False,
                note='URDF imported with fixed root for FK only; walking needs a planar floating root and V2 actuator implementation.')


if __name__ == '__main__':
    model = read_model()
    report = verify(model)
    (HERE/'model.json').write_text(json.dumps(model, ensure_ascii=False, indent=2)+'\n')
    (HERE/'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
