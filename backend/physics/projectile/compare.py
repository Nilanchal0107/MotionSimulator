"""
Trajectory Comparison Utilities
Functions for comparing multiple projectile trajectories.
"""

from .solver import solve_trajectory


def compare_trajectories(engine, params_list: list) -> list:
    """
    Simulate and return multiple trajectories for comparison overlays.

    Args:
        engine: ProjectileMotion instance
        params_list: List of dicts with keys v0, angle, drag_coeff, t_max, label, color

    Returns:
        List of trajectory result dicts (each with 'label' and 'color' keys)
    """
    results = []
    for params in params_list:
        result = solve_trajectory(
            engine,
            v0=params.get('v0', 10),
            angle_deg=params.get('angle', 45),
            drag_coeff=params.get('drag_coeff', 0),
            t_max=params.get('t_max', 20)
        )
        result['label'] = params.get('label', 'Trajectory')
        result['color'] = params.get('color', '#3B82F6')
        results.append(result)
    return results


def compare_with_vacuum(engine, v0: float, angle_deg: float,
                        drag_coeff: float, t_max: float = 20) -> dict:
    """
    Compare a drag trajectory against the theoretical vacuum trajectory.

    Returns:
        Dict with both trajectories and reduction metrics
    """
    with_drag = solve_trajectory(engine, v0, angle_deg, drag_coeff, t_max)
    vacuum = solve_trajectory(engine, v0, angle_deg, 0.0, t_max)

    range_reduction = vacuum['horizontal_range'] - with_drag['horizontal_range']
    time_reduction = vacuum['total_flight_time'] - with_drag['total_flight_time']

    return {
        'with_drag': with_drag,
        'vacuum': vacuum,
        'range_reduction': float(range_reduction),
        'range_reduction_percent': float(range_reduction / vacuum['horizontal_range'] * 100)
                                   if vacuum['horizontal_range'] > 0 else 0,
        'time_reduction': float(time_reduction),
        'time_reduction_percent': float(time_reduction / vacuum['total_flight_time'] * 100)
                                  if vacuum['total_flight_time'] > 0 else 0,
    }
