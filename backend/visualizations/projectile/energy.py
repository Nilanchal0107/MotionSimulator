"""Plot kinetic, potential, and total energy over time for a projectile"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_energy_analysis(data: dict) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    ax.plot(data['t'], data['kinetic_energy'],   color='#EF4444', linewidth=2, label='Kinetic Energy',   alpha=0.9)
    ax.plot(data['t'], data['potential_energy'],  color='#3B82F6', linewidth=2, label='Potential Energy', alpha=0.9)
    ax.plot(data['t'], data['total_energy'],      color='#10B981', linewidth=2.5, label='Total Energy', linestyle='--', alpha=0.9)

    ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Energy per unit mass (J/kg)', fontsize=12, fontweight='bold')
    ax.set_title('Energy Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    return fig_to_base64(fig)
