"""Plot angle vs time for both pendulum arms"""

import numpy as np
import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_angle_vs_time(data: dict) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(DEFAULT_FIGSIZE[0], 8))

    t = data['t']
    theta1 = np.degrees(data['theta1'])
    theta2 = np.degrees(data['theta2'])

    ax1.plot(t, theta1, color='#EF4444', linewidth=1.5)
    ax1.set_ylabel('Angle θ₁ (degrees)', fontsize=11, fontweight='bold')
    ax1.set_title('First Pendulum Angle', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    ax2.plot(t, theta2, color='#3B82F6', linewidth=1.5)
    ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Angle θ₂ (degrees)', fontsize=11, fontweight='bold')
    ax2.set_title('Second Pendulum Angle', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    plt.tight_layout()
    return fig_to_base64(fig)
