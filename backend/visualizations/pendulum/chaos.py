"""Plot chaos divergence (log separation and distance) between two trajectories"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_chaos_divergence(chaos_data: dict) -> str:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(DEFAULT_FIGSIZE[0], 8))

    ax1.plot(chaos_data['t'], chaos_data['distance'], color='#EF4444', linewidth=2)
    ax1.set_ylabel('Distance (m)', fontsize=11, fontweight='bold')
    ax1.set_title('Separation Between Second Bobs', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    ax2.plot(chaos_data['t'], chaos_data['log_separation'], color='#3B82F6', linewidth=2)
    ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('ln(distance/d₀)', fontsize=11, fontweight='bold')
    ax2.set_title(f'Exponential Divergence (λ ≈ {chaos_data["lyapunov_exponent"]:.3f})',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig_to_base64(fig)
