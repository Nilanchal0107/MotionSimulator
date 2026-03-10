"""
Input Validation & Clamping Utilities
Sanitizes and bounds-checks all incoming API parameters.
"""


def _clamp(value, lo, hi, default):
    """Clamp a float to [lo, hi], returning default on parse error."""
    try:
        v = float(value)
        return max(lo, min(hi, v))
    except (TypeError, ValueError):
        return default


def parse_projectile_params(data: dict) -> dict:
    """Validate and clamp all projectile parameters."""
    return {
        'v0':         _clamp(data.get('v0',         10),  0.1,  500.0,  10.0),
        'angle':      _clamp(data.get('angle',       45),  1.0,   89.0,  45.0),
        'drag_coeff': _clamp(data.get('drag_coeff',   0),  0.0,   10.0,   0.0),
        't_max':      _clamp(data.get('t_max',        20),  0.5,   60.0,  20.0),
    }


def parse_pendulum_params(data: dict) -> dict:
    """Validate and clamp all double pendulum parameters."""
    return {
        'm1':      _clamp(data.get('m1',     1),   0.1,  50.0,  1.0),
        'm2':      _clamp(data.get('m2',     1),   0.1,  50.0,  1.0),
        'L1':      _clamp(data.get('L1',     1),   0.1,  10.0,  1.0),
        'L2':      _clamp(data.get('L2',     1),   0.1,  10.0,  1.0),
        'theta1':  _clamp(data.get('theta1', 90), -180.0, 180.0, 90.0),
        'theta2':  _clamp(data.get('theta2', 90), -180.0, 180.0, 90.0),
        'omega1':  _clamp(data.get('omega1',  0),  -50.0,  50.0,  0.0),
        'omega2':  _clamp(data.get('omega2',  0),  -50.0,  50.0,  0.0),
        't_max':   _clamp(data.get('t_max',  20),    1.0, 100.0, 20.0),
        'fps':     int(_clamp(data.get('fps', 100),  10,  200,  100)),
        'damping': _clamp(data.get('damping',  0),   0.0,   5.0,  0.0),
    }
