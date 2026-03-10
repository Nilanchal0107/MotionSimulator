"""Compare drag trajectory against vacuum (no air resistance) trajectory"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_air_resistance_comparison(with_drag: dict, vacuum: dict) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    ax.plot(with_drag['x'], with_drag['y'], color='#EF4444', linewidth=2.5,
            label='With Air Resistance', alpha=0.9)
    ax.plot(vacuum['x'], vacuum['y'], color='#3B82F6', linewidth=2.5,
            label='Vacuum (No Drag)', linestyle='--', alpha=0.9)

    ax.set_xlabel('Horizontal Distance (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
    ax.set_title('Air Resistance Impact', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper right')
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, alpha=0.7)
    ax.set_ylim(bottom=0)
    return fig_to_base64(fig)
