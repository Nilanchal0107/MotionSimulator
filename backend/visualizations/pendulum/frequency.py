"""Plot FFT frequency power spectrum for pendulum theta2"""

import matplotlib.pyplot as plt
from ..base import fig_to_base64, DEFAULT_FIGSIZE


def plot_frequency_spectrum(fft_data: dict) -> str:
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    ax.plot(fft_data['frequencies'], fft_data['power'], color='#8B5CF6', linewidth=2)

    if fft_data['dominant_frequencies']:
        ax.plot(fft_data['dominant_frequencies'], fft_data['dominant_powers'],
                'ro', markersize=8,
                label=f'Dominant: {fft_data["dominant_frequencies"][0]:.2f} Hz')
        ax.legend(fontsize=10)

    ax.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Power', fontsize=12, fontweight='bold')
    ax.set_title('Frequency Spectrum (FFT)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0, right=10)
    return fig_to_base64(fig)
