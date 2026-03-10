"""
Projectile Motion Engine
Core class holding gravitational constant and the ODE derivatives function.
"""

import numpy as np


class ProjectileMotion:
    """Base engine for projectile motion — holds gravity and derivatives."""

    def __init__(self, g: float = 9.81):
        """
        Args:
            g: Gravitational acceleration in m/s²
        """
        self.g = g

    def derivatives(self, t: float, state: np.ndarray, drag_coeff: float) -> np.ndarray:
        """
        Compute ODE derivatives for projectile motion with air resistance.

        Args:
            t: Current time (unused but required by solve_ivp)
            state: [x, y, vx, vy]
            drag_coeff: Air resistance coefficient B

        Returns:
            [dx/dt, dy/dt, dvx/dt, dvy/dt]
        """
        x, y, vx, vy = state
        v = np.sqrt(vx**2 + vy**2)
        ax = -drag_coeff * vx * v
        ay = -self.g - drag_coeff * vy * v
        return np.array([vx, vy, ax, ay])
