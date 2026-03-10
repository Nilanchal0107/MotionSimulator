"""Plot energy conservation (KE, PE, Total) for double pendulum"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_energy_conservation(data: dict) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    ax.plot(data['t'], data['kinetic_energy'],  color='#EF4444', linewidth=1.5, label='Kinetic',   alpha=0.8)
    ax.plot(data['t'], data['potential_energy'], color='#3B82F6', linewidth=1.5, label='Potential', alpha=0.8)
    ax.plot(data['t'], data['total_energy'],     color='#10B981', linewidth=2.5, label='Total',     linestyle='--', alpha=0.9)

    ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Energy (J)', fontsize=12, fontweight='bold')
    ax.set_title(f'Energy Conservation (Error: {data["energy_error_percent"]:.4f}%)',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    return fig_to_base64(fig)
