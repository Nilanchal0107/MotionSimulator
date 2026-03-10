"""Plot horizontal velocity, vertical velocity, and total speed over time"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_velocity_components(data: dict) -> str:
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(DEFAULT_FIGSIZE[0], 10))

    ax1.plot(data['t'], data['vx'], color='#3B82F6', linewidth=2)
    ax1.set_ylabel('Vx (m/s)', fontsize=11, fontweight='bold')
    ax1.set_title('Horizontal Velocity', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    ax2.plot(data['t'], data['vy'], color='#EF4444', linewidth=2)
    ax2.set_ylabel('Vy (m/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Vertical Velocity', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    ax3.plot(data['t'], data['speed'], color='#10B981', linewidth=2.5)
    ax3.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Speed (m/s)', fontsize=11, fontweight='bold')
    ax3.set_title('Total Speed', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig_to_base64(fig)
