"""Double Pendulum API Routes"""

from flask import Blueprint, request, jsonify
from backend.utils.validation import parse_pendulum_params
from backend.utils.gravity import resolve_gravity
from backend.utils.caching import cached_pendulum_trajectory
from backend.physics.pendulum.engine import DoublePendulum
from backend.physics.pendulum.fft import calculate_fft
from backend.physics.pendulum.heatmap import calculate_position_heatmap
from backend.visualizations.pendulum.angles import plot_angle_vs_time
from backend.visualizations.pendulum.angular_velocity import plot_angular_velocity
from backend.visualizations.pendulum.phase_space import plot_phase_space
from backend.visualizations.pendulum.energy import plot_energy_conservation
from backend.visualizations.pendulum.frequency import plot_frequency_spectrum
from backend.visualizations.pendulum.heatmap import plot_position_heatmap

pendulum_bp = Blueprint('pendulum', __name__)


@pendulum_bp.route('/analyze', methods=['POST'])
def analyze():
    """Simulate and generate all pendulum analysis graphs in one call."""
    try:
        data = request.json or {}
        p = parse_pendulum_params(data)
        g = resolve_gravity(data)

        trajectory = cached_pendulum_trajectory(
            p['m1'], p['m2'], p['L1'], p['L2'],
            p['theta1'], p['theta2'],
            p['omega1'], p['omega2'],
            p['t_max'], p['fps'], p['damping'], g
        )

        engine = DoublePendulum(g=g)
        fft_data = calculate_fft(trajectory)
        heatmap_data = calculate_position_heatmap(trajectory)

        graphs = {
            'angles':           plot_angle_vs_time(trajectory),
            'angular_velocity': plot_angular_velocity(trajectory),
            'phase_space':      plot_phase_space(trajectory),
            'energy':           plot_energy_conservation(trajectory),
            'frequency':        plot_frequency_spectrum(fft_data),
            'heatmap':          plot_position_heatmap(heatmap_data),
        }

        return jsonify({'status': 'success', 'graphs': graphs, 'trajectory': trajectory})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
