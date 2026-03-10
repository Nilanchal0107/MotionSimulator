"""
Projectile Trajectory Solver
Integrates the ODE and returns a full trajectory dictionary.
"""

import numpy as np
from scipy.integrate import solve_ivp


def solve_trajectory(engine, v0: float, angle_deg: float,
                     drag_coeff: float, t_max: float = 20.0,
                     num_points: int = 500) -> dict:
    """
    Solve projectile motion trajectory using RK45.

    Args:
        engine: ProjectileMotion instance (provides g & derivatives)
        v0: Initial speed (m/s)
        angle_deg: Launch angle (degrees)
        drag_coeff: Air-resistance coefficient B
        t_max: Max simulation time (s)
        num_points: Number of ODE evaluation points

    Returns:
        Dictionary with arrays and scalar summary metrics
    """
    angle_rad = np.radians(angle_deg)
    vx0 = v0 * np.cos(angle_rad)
    vy0 = v0 * np.sin(angle_rad)
    state0 = [0, 0, vx0, vy0]

    def hit_ground(t, state, drag_coeff):
        return state[1]
    hit_ground.terminal = True
    hit_ground.direction = -1

    t_eval = np.linspace(0, t_max, num_points)
    solution = solve_ivp(
        engine.derivatives,
        (0, t_max),
        state0,
        args=(drag_coeff,),
        t_eval=t_eval,
        events=hit_ground,
        method='RK45',
        rtol=1e-8,
        atol=1e-10,
        dense_output=True
    )

    t = solution.t
    x, y, vx, vy = solution.y

    valid_idx = y >= 0
    t, x, y, vx, vy = t[valid_idx], x[valid_idx], y[valid_idx], vx[valid_idx], vy[valid_idx]

    speed = np.sqrt(vx**2 + vy**2)
    kinetic_energy = 0.5 * (vx**2 + vy**2)
    potential_energy = engine.g * y
    total_energy = kinetic_energy + potential_energy

    max_height_idx = np.argmax(y)
    max_height = y[max_height_idx]
    time_to_max_height = t[max_height_idx]
    total_flight_time = t[-1] if len(t) > 0 else 0
    horizontal_range = x[-1] if len(x) > 0 else 0
    impact_speed = speed[-1] if len(speed) > 0 else 0
    impact_angle_deg = np.degrees(np.arctan2(vy[-1], vx[-1])) if len(vy) > 0 else 0

    initial_energy = 0.5 * v0**2
    final_energy = total_energy[-1] if len(total_energy) > 0 else 0
    energy_lost_percent = ((initial_energy - final_energy) / initial_energy * 100) if initial_energy > 0 else 0

    return {
        't': t.tolist(), 'x': x.tolist(), 'y': y.tolist(),
        'vx': vx.tolist(), 'vy': vy.tolist(), 'speed': speed.tolist(),
        'kinetic_energy': kinetic_energy.tolist(),
        'potential_energy': potential_energy.tolist(),
        'total_energy': total_energy.tolist(),
        'max_height': float(max_height),
        'time_to_max_height': float(time_to_max_height),
        'total_flight_time': float(total_flight_time),
        'horizontal_range': float(horizontal_range),
        'impact_speed': float(impact_speed),
        'impact_angle_deg': float(impact_angle_deg),
        'energy_lost_percent': float(energy_lost_percent)
    }
