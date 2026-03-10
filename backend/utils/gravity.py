"""
Gravity Presets & Resolver
Provides gravity constants for different celestial bodies.
"""

GRAVITY_PRESETS = {
    'earth':   9.81,
    'moon':    1.62,
    'mars':    3.72,
    'jupiter': 24.79,
}


def resolve_gravity(data: dict) -> float:
    """Return gravity value from 'gravity_preset' key or custom 'g' key."""
    preset = data.get('gravity_preset', 'earth')
    if preset in GRAVITY_PRESETS:
        return GRAVITY_PRESETS[preset]
    try:
        g = float(data.get('g', 9.81))
        return max(0.1, min(100.0, g))
    except (TypeError, ValueError):
        return 9.81
