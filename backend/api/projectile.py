"""Projectile Motion API Routes"""

from flask import Blueprint, request, jsonify
from backend.utils.validation import parse_projectile_params
from backend.utils.gravity import resolve_gravity
from backend.utils.caching import cached_projectile_trajectory
from backend.physics.projectile.engine import ProjectileMotion
from backend.physics.projectile.optimal_angle import calculate_optimal_angle
from backend.visualizations.projectile.trajectory import plot_trajectory
from backend.visualizations.projectile.velocity import plot_velocity_components
from backend.visualizations.projectile.height import plot_height_vs_time
from backend.visualizations.projectile.energy import plot_energy_analysis
from backend.visualizations.projectile.optimal_angle import plot_optimal_angle_curve
from backend.visualizations.projectile.air_resistance import plot_air_resistance_comparison

projectile_bp = Blueprint('projectile', __name__)


@projectile_bp.route('/analyze', methods=['POST'])
def analyze():
    """Simulate and generate all projectile analysis graphs in one call."""
    try:
        data = request.json or {}
        p = parse_projectile_params(data)
        g = resolve_gravity(data)

        trajectory = cached_projectile_trajectory(
            p['v0'], p['angle'], p['drag_coeff'], p['t_max'], g
        )

        graphs = {
            'trajectory':          plot_trajectory([trajectory]),
            'velocity_components': plot_velocity_components(trajectory),
            'height_vs_time':      plot_height_vs_time(trajectory),
            'energy':              plot_energy_analysis(trajectory),
        }

        comparison_stats = None
        if p['drag_coeff'] > 0:
            vacuum = cached_projectile_trajectory(p['v0'], p['angle'], 0.0, p['t_max'], g)
            graphs['air_resistance'] = plot_air_resistance_comparison(trajectory, vacuum)
            vr = vacuum['horizontal_range']
            tr = vacuum['total_flight_time']
            rr = vr - trajectory['horizontal_range']
            tr2 = tr - trajectory['total_flight_time']
            comparison_stats = {
                'range_reduction':         rr,
                'range_reduction_percent': rr / vr * 100 if vr > 0 else 0,
                'time_reduction':          tr2,
                'time_reduction_percent':  tr2 / tr * 100 if tr > 0 else 0,
            }
        else:
            graphs['air_resistance'] = None

        return jsonify({'status': 'success', 'graphs': graphs,
                        'trajectory': trajectory, 'comparison_stats': comparison_stats})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@projectile_bp.route('/optimal_angle', methods=['POST'])
def optimal_angle():
    """Find the optimal launch angle for maximum range."""
    try:
        data = request.json or {}
        p = parse_projectile_params(data)
        g = resolve_gravity(data)
        engine = ProjectileMotion(g=g)

        opt_angle, max_range, angles, ranges = calculate_optimal_angle(engine, p['v0'], p['drag_coeff'])
        graph = plot_optimal_angle_curve(angles, ranges, opt_angle, max_range)

        return jsonify({
            'status': 'success',
            'optimal_angle': opt_angle,
            'max_range': max_range,
            'graph': graph,
            'data': {'angles': angles, 'ranges': ranges}
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
