"""
Position Heatmap Calculator
Bins the second bob's Cartesian positions into a 2D density grid.
"""

import numpy as np


def calculate_position_heatmap(trajectory: dict, grid_size: int = 50) -> dict:
    """
    Build a 2D histogram of where the second bob spends its time.

    Args:
        trajectory: Trajectory dict from solve_motion
        grid_size: Number of histogram bins per axis

    Returns:
        Dict with normalised heatmap and axis tick arrays
    """
    x2 = np.array(trajectory['x2'])
    y2 = np.array(trajectory['y2'])

    L_total = trajectory['params']['L1'] + trajectory['params']['L2']
    lim = L_total * 1.1

    heatmap, xedges, yedges = np.histogram2d(
        x2, y2,
        bins=grid_size,
        range=[[-lim, lim], [-lim, lim]]
    )
    heatmap = heatmap / np.max(heatmap) if np.max(heatmap) > 0 else heatmap

    x_centers = (xedges[:-1] + xedges[1:]) / 2
    y_centers = (yedges[:-1] + yedges[1:]) / 2

    return {
        'heatmap': heatmap.tolist(),
        'x_centers': x_centers.tolist(),
        'y_centers': y_centers.tolist(),
        'x_edges': xedges.tolist(),
        'y_edges': yedges.tolist()
    }
