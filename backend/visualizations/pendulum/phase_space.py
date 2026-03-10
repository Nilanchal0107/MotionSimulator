"""Plot phase space (angle vs angular velocity) for both arms"""

import numpy as np
import matplotlib.pyplot as plt
from ..base import fig_to_base64


def plot_phase_space(data: dict) -> str:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    t = np.array(data['t'])
    theta1 = np.degrees(data['theta1'])
    theta2 = np.degrees(data['theta2'])

    sc1 = ax1.scatter(theta1, data['omega1'], c=t, cmap='plasma', s=1, alpha=0.6)
    ax1.set_xlabel('θ₁ (degrees)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('ω₁ (rad/s)', fontsize=11, fontweight='bold')
    ax1.set_title('Phase Space: Pendulum 1', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    sc2 = ax2.scatter(theta2, data['omega2'], c=t, cmap='plasma', s=1, alpha=0.6)
    ax2.set_xlabel('θ₂ (degrees)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('ω₂ (rad/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Phase Space: Pendulum 2', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(sc2, ax=ax2).set_label('Time (s)', fontsize=10)

    plt.tight_layout()
    return fig_to_base64(fig)
