"""Preset Configurations API Routes"""

from flask import Blueprint, jsonify
from backend.utils.gravity import GRAVITY_PRESETS

presets_bp = Blueprint('presets', __name__)

PROJECTILE_PRESETS = {
    'basketball': {'name': 'Basketball Free Throw', 'v0': 7.5,  'angle': 52, 'drag_coeff': 0.15, 't_max': 3},
    'golf':       {'name': 'Golf Drive',            'v0': 70,   'angle': 12, 'drag_coeff': 0.25, 't_max': 8},
    'soccer':     {'name': 'Soccer Kick',           'v0': 25,   'angle': 30, 'drag_coeff': 0.30, 't_max': 5},
    'cannon':     {'name': 'Cannonball',            'v0': 100,  'angle': 45, 'drag_coeff': 0.05, 't_max': 15},
    'vacuum':     {'name': 'No Air Resistance',     'v0': 20,   'angle': 45, 'drag_coeff': 0,    't_max': 5},
}

PENDULUM_PRESETS = {
    'gentle':    {'name': 'Gentle Swing',            'm1': 1,   'm2': 1,   'L1': 1,   'L2': 1,   'theta1': 30,  'theta2': 30,  'omega1': 0, 'omega2': 0, 't_max': 20, 'fps': 100, 'damping': 0},
    'chaotic':   {'name': 'Chaotic Motion',          'm1': 1,   'm2': 1,   'L1': 1,   'L2': 1,   'theta1': 120, 'theta2': -30, 'omega1': 0, 'omega2': 0, 't_max': 30, 'fps': 100, 'damping': 0},
    'flip':      {'name': 'Near Flip',               'm1': 1,   'm2': 1,   'L1': 1,   'L2': 1,   'theta1': 175, 'theta2': 175, 'omega1': 0, 'omega2': 0, 't_max': 25, 'fps': 100, 'damping': 0},
    'equal':     {'name': 'Equal Lengths',           'm1': 2,   'm2': 2,   'L1': 1.5, 'L2': 1.5, 'theta1': 90,  'theta2': 90,  'omega1': 0, 'omega2': 0, 't_max': 20, 'fps': 100, 'damping': 0},
    'mass_diff': {'name': 'Extreme Mass Difference', 'm1': 0.5, 'm2': 5,   'L1': 1,   'L2': 1,   'theta1': 60,  'theta2': 60,  'omega1': 0, 'omega2': 0, 't_max': 20, 'fps': 100, 'damping': 0},
    'damped':    {'name': 'Damped Oscillation',      'm1': 1,   'm2': 1,   'L1': 1,   'L2': 1,   'theta1': 90,  'theta2': 90,  'omega1': 0, 'omega2': 0, 't_max': 30, 'fps': 100, 'damping': 0.5},
}


@presets_bp.route('/<simulation_type>')
def get_presets(simulation_type):
    """Return preset configurations for projectile or pendulum simulations."""
    if simulation_type == 'projectile':
        return jsonify({'status': 'success', 'presets': PROJECTILE_PRESETS})
    elif simulation_type == 'pendulum':
        return jsonify({'status': 'success', 'presets': PENDULUM_PRESETS})
    return jsonify({'status': 'error', 'message': 'Invalid simulation type'}), 400


@presets_bp.route('/gravity')
def get_gravity_presets():
    """Return available planetary gravity presets."""
    return jsonify({
        'status': 'success',
        'presets': {k: {'g': v, 'label': k.capitalize()} for k, v in GRAVITY_PRESETS.items()}
    })
