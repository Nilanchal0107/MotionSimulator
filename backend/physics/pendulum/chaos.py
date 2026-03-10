"""
Chaos Analysis for Double Pendulum
Compares two nearby trajectories and estimates the Lyapunov exponent.
"""

import numpy as np
from .solver import solve_motion


def calculate_chaos_metrics(trajectory1: dict, trajectory2: dict) -> dict:
    """
    Estimate Lyapunov exponent and chaos rating from two diverging trajectories.

    Args:
        trajectory1, trajectory2: Trajectories with slightly different ICs

    Returns:
        Dict with distance array, log separation, lyapunov exponent, chaos rating
    """
    t = np.array(trajectory1['t'])
    x1 = np.array(trajectory1['x2'])
    y1 = np.array(trajectory1['y2'])
    x2 = np.array(trajectory2['x2'])
    y2 = np.array(trajectory2['y2'])

    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    d0 = distance[0] if distance[0] > 0 else 1e-10
    distance_safe = np.maximum(distance, 1e-10)
    log_separation = np.log(distance_safe / d0)

    lyapunov = 0.0
    half_idx = len(t) // 3
    if half_idx > 10:
        growth_start = next((i for i in range(1, half_idx) if distance[i] > 2 * d0), 0)
        if growth_start > 0 and half_idx > growth_start + 10:
            lyapunov = float(np.polyfit(t[growth_start:half_idx],
                                        log_separation[growth_start:half_idx], 1)[0])

    chaos_rating = "Low" if lyapunov < 0.1 else "Medium" if lyapunov < 0.5 else "High"

    L_total = trajectory1['params']['L1'] + trajectory1['params']['L2']
    threshold = 0.1 * L_total
    predictability_time = next((t[i] for i, d in enumerate(distance) if d > threshold), t[-1])

    return {
        't': t.tolist(),
        'distance': distance.tolist(),
        'log_separation': log_separation.tolist(),
        'lyapunov_exponent': lyapunov,
        'chaos_rating': chaos_rating,
        'predictability_time': float(predictability_time),
        'initial_separation': float(d0),
        'final_separation': float(distance[-1])
    }


def compare_chaos(engine, m1, m2, L1, L2, theta1_deg, theta2_deg,
                  omega1, omega2, difference=0.1,
                  t_max=20, fps=100, damping=0.0) -> dict:
    """
    Run two nearby simulations and return both trajectories with chaos metrics.

    Args:
        engine: DoublePendulum instance
        difference: Angular offset (degrees) for the second trajectory

    Returns:
        Dict with trajectory1, trajectory2, chaos_metrics and initial_difference_deg
    """
    traj1 = solve_motion(engine, m1, m2, L1, L2, theta1_deg, theta2_deg,
                         omega1, omega2, t_max, fps, damping)
    traj2 = solve_motion(engine, m1, m2, L1, L2, theta1_deg + difference, theta2_deg,
                         omega1, omega2, t_max, fps, damping)
    chaos_metrics = calculate_chaos_metrics(traj1, traj2)
    return {
        'trajectory1': traj1,
        'trajectory2': traj2,
        'chaos_metrics': chaos_metrics,
        'initial_difference_deg': difference
    }
