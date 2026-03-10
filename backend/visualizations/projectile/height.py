"""Plot height versus time for a projectile trajectory"""

import numpy as np
import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_height_vs_time(data: dict) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    t, y = data['t'], data['y']

    ax.plot(t, y, color='#8B5CF6', linewidth=2.5)
    ax.fill_between(t, y, alpha=0.3, color='#8B5CF6')

    if y:
        max_idx = int(np.argmax(y))
        ax.plot(t[max_idx], y[max_idx], 'ro', markersize=10,
                label=f'Max: {y[max_idx]:.2f} m at t={t[max_idx]:.2f}s')

    ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
    ax.set_title('Height vs Time', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_ylim(bottom=0)
    return fig_to_base64(fig)
