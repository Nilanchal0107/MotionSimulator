"""
Optimal Launch Angle Finder
Uses golden-section search to find the angle that maximises horizontal range.
"""

from scipy.optimize import minimize_scalar
from .solver import solve_trajectory


def calculate_optimal_angle(engine, v0: float, drag_coeff: float,
                             angle_range=(20, 70), step: int = 1):
    """
    Find the optimal launch angle for maximum range.

    Args:
        engine: ProjectileMotion instance
        v0: Initial velocity (m/s)
        drag_coeff: Air-resistance coefficient
        angle_range: (min_deg, max_deg) search bounds
        step: Step size for chart data points

    Returns:
        (optimal_angle, max_range, chart_angles, chart_ranges)
    """
    def neg_range(angle_deg):
        result = solve_trajectory(engine, v0, float(angle_deg), drag_coeff,
                                  t_max=20, num_points=200)
        return -result['horizontal_range']

    result = minimize_scalar(
        neg_range,
        bounds=(float(angle_range[0]), float(angle_range[1])),
        method='bounded',
        options={'xatol': 0.1}
    )
    optimal_angle = float(result.x)
    max_range = float(-result.fun)

    chart_angles = list(range(angle_range[0], angle_range[1] + 1, max(step * 5, 5)))
    if angle_range[1] not in chart_angles:
        chart_angles.append(angle_range[1])
    chart_ranges = [
        solve_trajectory(engine, v0, a, drag_coeff, t_max=20, num_points=200)['horizontal_range']
        for a in chart_angles
    ]

    return optimal_angle, max_range, chart_angles, chart_ranges
