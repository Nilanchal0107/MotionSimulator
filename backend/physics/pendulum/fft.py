"""
FFT Frequency Analysis for Double Pendulum
Computes frequency spectrum of the second arm angle time series.
"""

import numpy as np
from scipy.fft import fft, fftfreq


def _find_peaks(data: np.ndarray, threshold: float = 0) -> np.ndarray:
    """Return indices of local maxima above threshold."""
    peaks = [
        i for i in range(1, len(data) - 1)
        if data[i] > data[i - 1] and data[i] > data[i + 1] and data[i] > threshold
    ]
    return np.array(peaks)


def calculate_fft(trajectory: dict) -> dict:
    """
    Compute the frequency power spectrum of theta2.

    Args:
        trajectory: Trajectory dictionary from solve_motion

    Returns:
        Dict with frequencies, power, dominant frequencies/powers
    """
    t = np.array(trajectory['t'])
    theta2 = np.array(trajectory['theta2'])

    dt = t[1] - t[0] if len(t) > 1 else 1
    N = len(theta2)
    yf = fft(theta2)
    xf = fftfreq(N, dt)[:N // 2]
    power = 2.0 / N * np.abs(yf[:N // 2])

    peaks_idx = _find_peaks(power, threshold=0.1 * np.max(power))
    return {
        'frequencies': xf.tolist(),
        'power': power.tolist(),
        'dominant_frequencies': xf[peaks_idx].tolist(),
        'dominant_powers': power[peaks_idx].tolist(),
        'sampling_rate': float(1 / dt)
    }
