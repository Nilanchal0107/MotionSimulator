"""
LRU Cache Wrappers
Caches expensive ODE solves so repeated identical requests are instant.
"""

from functools import lru_cache


@lru_cache(maxsize=64)
def cached_projectile_trajectory(v0, angle, drag_coeff, t_max, g):
    """Cached projectile ODE solve — keyed by all physics params."""
    from backend.physics.projectile.solver import solve_trajectory
    from backend.physics.projectile.engine import ProjectileMotion
    engine = ProjectileMotion(g=g)
    return solve_trajectory(engine, v0, angle, drag_coeff, t_max)


@lru_cache(maxsize=32)
def cached_pendulum_trajectory(m1, m2, L1, L2, theta1, theta2,
                                omega1, omega2, t_max, fps, damping, g):
    """Cached pendulum ODE solve — keyed by all physics params."""
    from backend.physics.pendulum.solver import solve_motion
    from backend.physics.pendulum.engine import DoublePendulum
    engine = DoublePendulum(g=g)
    return solve_motion(engine, m1, m2, L1, L2, theta1, theta2,
                        omega1, omega2, t_max, fps, damping)
