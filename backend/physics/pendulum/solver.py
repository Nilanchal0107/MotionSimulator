"""
Double Pendulum Motion Solver
Integrates the Lagrangian ODEs and returns a full trajectory dict.
"""

import numpy as np
from scipy.integrate import solve_ivp


def _count_rotations(theta: np.ndarray) -> int:
    """Count full 360° rotations via angle unwrapping."""
    theta_unwrapped = np.unwrap(theta)
    return int(abs(theta_unwrapped[-1] - theta_unwrapped[0]) / (2 * np.pi))


def solve_motion(engine, m1, m2, L1, L2,
                 theta1_deg, theta2_deg,
                 omega1=0.0, omega2=0.0,
                 t_max=20, fps=100,
                 damping=0.0, max_points=4000) -> dict:
    """
    Solve double pendulum motion using RK45.

    Args:
        engine: DoublePendulum instance
        m1, m2: Bob masses (kg)
        L1, L2: Arm lengths (m)
        theta1_deg, theta2_deg: Initial angles (degrees)
        omega1, omega2: Initial angular velocities (rad/s)
        t_max: Simulation duration (s)
        fps: Frames per second for evaluation density
        damping: Friction coefficient
        max_points: Cap on total output points

    Returns:
        Full trajectory dictionary with arrays and scalar summary stats
    """
    theta1_rad = np.radians(theta1_deg)
    theta2_rad = np.radians(theta2_deg)
    state0 = [theta1_rad, omega1, theta2_rad, omega2]

    raw_points = int(t_max * fps)
    num_points = min(raw_points, max_points)
    t_eval = np.linspace(0, t_max, num_points)

    solution = solve_ivp(
        engine.derivatives,
        (0, t_max),
        state0,
        args=(m1, m2, L1, L2, damping),
        t_eval=t_eval,
        method='RK45',
        rtol=1e-8,
        atol=1e-10,
        dense_output=True
    )

    t = solution.t
    theta1, omega1_t, theta2, omega2_t = solution.y

    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)

    v1_sq = (L1 * omega1_t) ** 2
    v2_sq = ((L1 * omega1_t) ** 2 + (L2 * omega2_t) ** 2
              + 2 * L1 * L2 * omega1_t * omega2_t * np.cos(theta1 - theta2))
    KE1 = 0.5 * m1 * v1_sq
    KE2 = 0.5 * m2 * v2_sq
    PE1 = m1 * engine.g * y1
    PE2 = m2 * engine.g * y2
    kinetic_energy = KE1 + KE2
    potential_energy = PE1 + PE2
    total_energy = kinetic_energy + potential_energy

    mean_e = np.abs(np.mean(total_energy))
    energy_error = float(np.std(total_energy) / mean_e * 100) if mean_e > 0 else 0

    return {
        't': t.tolist(),
        'theta1': theta1.tolist(), 'theta2': theta2.tolist(),
        'omega1': omega1_t.tolist(), 'omega2': omega2_t.tolist(),
        'x1': x1.tolist(), 'y1': y1.tolist(),
        'x2': x2.tolist(), 'y2': y2.tolist(),
        'kinetic_energy': kinetic_energy.tolist(),
        'potential_energy': potential_energy.tolist(),
        'total_energy': total_energy.tolist(),
        'KE1': KE1.tolist(), 'KE2': KE2.tolist(),
        'PE1': PE1.tolist(), 'PE2': PE2.tolist(),
        'energy_error_percent': energy_error,
        'max_theta1_rad': float(np.max(np.abs(theta1))),
        'max_theta2_rad': float(np.max(np.abs(theta2))),
        'max_theta1_deg': float(np.degrees(np.max(np.abs(theta1)))),
        'max_theta2_deg': float(np.degrees(np.max(np.abs(theta2)))),
        'max_omega1': float(np.max(np.abs(omega1_t))),
        'max_omega2': float(np.max(np.abs(omega2_t))),
        'rotations1': _count_rotations(theta1),
        'rotations2': _count_rotations(theta2),
        'params': {
            'm1': m1, 'm2': m2, 'L1': L1, 'L2': L2,
            'theta1_deg': theta1_deg, 'theta2_deg': theta2_deg,
            'omega1': omega1, 'omega2': omega2, 'damping': damping
        }
    }
