"""Plot 2D position density heatmap for second pendulum bob"""

import numpy as np
import matplotlib.pyplot as plt
from ..base import fig_to_base64


def plot_position_heatmap(heatmap_data: dict) -> str:
    fig, ax = plt.subplots(figsize=(8, 8))

    heatmap = np.array(heatmap_data['heatmap'])
    x_centers = heatmap_data['x_centers']
    y_centers = heatmap_data['y_centers']

    im = ax.imshow(heatmap.T, origin='lower', cmap='hot', aspect='auto',
                   extent=[x_centers[0], x_centers[-1], y_centers[0], y_centers[-1]])
    ax.set_xlabel('X Position (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y Position (m)', fontsize=12, fontweight='bold')
    ax.set_title('Position Heatmap (Second Bob)', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax).set_label('Frequency (normalized)', fontsize=10)
    return fig_to_base64(fig)
