"""
Double Pendulum Engine
Core class holding gravitational constant and Lagrangian ODE derivatives.
"""

import numpy as np


class DoublePendulum:
    """Base engine for double pendulum — holds gravity and Lagrangian derivatives."""

    def __init__(self, g: float = 9.81):
        """
        Args:
            g: Gravitational acceleration in m/s²
        """
        self.g = g

    def derivatives(self, t: float, state: np.ndarray,
                    m1: float, m2: float, L1: float, L2: float,
                    damping: float = 0.0) -> np.ndarray:
        """
        Lagrangian equations of motion with optional damping.

        Args:
            t: Time (unused but required by solve_ivp)
            state: [theta1, omega1, theta2, omega2]
            m1, m2: Bob masses (kg)
            L1, L2: Arm lengths (m)
            damping: Energy dissipation coefficient

        Returns:
            [dtheta1/dt, dalpha1/dt, dtheta2/dt, dalpha2/dt]
        """
        theta1, omega1, theta2, omega2 = state
        delta = theta2 - theta1

        den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
        den2 = (L2 / L1) * den1

        alpha1 = (m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta)
                  + m2 * self.g * np.sin(theta2) * np.cos(delta)
                  + m2 * L2 * omega2**2 * np.sin(delta)
                  - (m1 + m2) * self.g * np.sin(theta1)) / den1

        alpha2 = (-m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta)
                  + (m1 + m2) * self.g * np.sin(theta1) * np.cos(delta)
                  - (m1 + m2) * L1 * omega1**2 * np.sin(delta)
                  - (m1 + m2) * self.g * np.sin(theta2)) / den2

        alpha1 -= damping * omega1
        alpha2 -= damping * omega2

        return np.array([omega1, alpha1, omega2, alpha2])
