"""Plot projectile trajectory / trajectories"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_trajectory(trajectories: list, comparison_mode: bool = False) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    colors = ['#EF4444', '#3B82F6', '#10B981']

    for i, traj in enumerate(trajectories):
        x, y = traj['x'], traj['y']
        label = traj.get('label', f'Trajectory {i + 1}')
        color = traj.get('color', colors[i % len(colors)])
        ax.plot(x, y, color=color, linewidth=2.5, label=label, alpha=0.9)
        if x and y:
            ax.plot(x[0], y[0], 'o', color=color, markersize=8, zorder=5)
            ax.plot(x[-1], y[-1], 's', color=color, markersize=8, zorder=5)

    ax.set_xlabel('Horizontal Distance (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
    ax.set_title('Projectile Trajectory', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, alpha=0.7, label='Ground')
    if comparison_mode or len(trajectories) > 1:
        ax.legend(fontsize=10, loc='upper right')
    ax.set_ylim(bottom=0)
    return fig_to_base64(fig)
