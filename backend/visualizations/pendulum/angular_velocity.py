"""Plot angular velocity (omega) vs time for both pendulum arms"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_angular_velocity(data: dict) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(DEFAULT_FIGSIZE[0], 8))

    ax1.plot(data['t'], data['omega1'], color='#EF4444', linewidth=1.5)
    ax1.set_ylabel('ω₁ (rad/s)', fontsize=11, fontweight='bold')
    ax1.set_title('First Pendulum Angular Velocity', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    ax2.plot(data['t'], data['omega2'], color='#3B82F6', linewidth=1.5)
    ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('ω₂ (rad/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Second Pendulum Angular Velocity', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    plt.tight_layout()
    return fig_to_base64(fig)
