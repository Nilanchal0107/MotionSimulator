"""Plot range vs angle curve with optimal angle highlighted"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_optimal_angle_curve(angles, ranges, optimal_angle: float, max_range: float) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    ax.plot(angles, ranges, color='#3B82F6', linewidth=2.5, marker='o', markersize=4, label='Range vs Angle')
    ax.axvline(x=optimal_angle, color='#EF4444', linestyle='--', linewidth=2,
               label=f'Optimal: {optimal_angle:.1f}° → {max_range:.2f} m')
    ax.plot(optimal_angle, max_range, 'r*', markersize=20, zorder=5)

    ax.set_xlabel('Launch Angle (degrees)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Range (m)', fontsize=12, fontweight='bold')
    ax.set_title('Optimal Launch Angle Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc='upper right')
    return fig_to_base64(fig)
