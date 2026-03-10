"""
Physics Motion Simulator - Flask Backend
API server for projectile motion and double pendulum simulations
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

from physics.projectile import ProjectileMotion
from physics.double_pendulum import DoublePendulum
from visualizations.graphs import GraphGenerator

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize physics engines and graph generator
projectile_engine = ProjectileMotion()
pendulum_engine = DoublePendulum()
graph_gen = GraphGenerator()


# ==================== SERVE STATIC FILES ====================

@app.route('/')
def index():
    """Serve main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)


# ==================== PROJECTILE MOTION ENDPOINTS ====================

@app.route('/api/projectile/simulate', methods=['POST'])
def projectile_simulate():
    """Simulate projectile motion"""
    try:
        data = request.json
        
        v0 = float(data.get('v0', 10))
        angle = float(data.get('angle', 45))
        drag_coeff = float(data.get('drag_coeff', 0))
        t_max = float(data.get('t_max', 20))
        
        result = projectile_engine.solve_trajectory(v0, angle, drag_coeff, t_max)
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/projectile/analyze', methods=['POST'])
def projectile_analyze():
    """Generate all analysis graphs for projectile motion"""
    try:
        data = request.json
        
        v0 = float(data.get('v0', 10))
        angle = float(data.get('angle', 45))
        drag_coeff = float(data.get('drag_coeff', 0))
        t_max = float(data.get('t_max', 20))
        
        # Get trajectory data
        trajectory = projectile_engine.solve_trajectory(v0, angle, drag_coeff, t_max)
        
        # Generate graphs
        graphs = {}
        
        # Main trajectory
        graphs['trajectory'] = graph_gen.plot_trajectory([trajectory])
        
        # Velocity components
        graphs['velocity_components'] = graph_gen.plot_velocity_components(trajectory)
        
        # Height vs time
        graphs['height_vs_time'] = graph_gen.plot_height_vs_time(trajectory)
        
        # Energy analysis
        graphs['energy'] = graph_gen.plot_energy_analysis(trajectory)
        
        # Air resistance comparison (if drag > 0)
        if drag_coeff > 0:
            comparison = projectile_engine.compare_with_vacuum(v0, angle, drag_coeff, t_max)
            graphs['air_resistance'] = graph_gen.plot_air_resistance_comparison(
                comparison['with_drag'], comparison['vacuum']
            )
            comparison_stats = {
                'range_reduction': comparison['range_reduction'],
                'range_reduction_percent': comparison['range_reduction_percent'],
                'time_reduction': comparison['time_reduction'],
                'time_reduction_percent': comparison['time_reduction_percent']
            }
        else:
            graphs['air_resistance'] = None
            comparison_stats = None
        
        return jsonify({
            'status': 'success',
            'graphs': graphs,
            'trajectory': trajectory,
            'comparison_stats': comparison_stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/projectile/optimal_angle', methods=['POST'])
def projectile_optimal_angle():
    """Find optimal launch angle"""
    try:
        data = request.json
        
        v0 = float(data.get('v0', 10))
        drag_coeff = float(data.get('drag_coeff', 0))
        
        optimal_angle, max_range, angles, ranges = projectile_engine.calculate_optimal_angle(
            v0, drag_coeff
        )
        
        # Generate graph
        graph = graph_gen.plot_optimal_angle_curve(angles, ranges, optimal_angle, max_range)
        
        return jsonify({
            'status': 'success',
            'optimal_angle': optimal_angle,
            'max_range': max_range,
            'graph': graph,
            'data': {
                'angles': angles,
                'ranges': ranges
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


# ==================== DOUBLE PENDULUM ENDPOINTS ====================

@app.route('/api/pendulum/simulate', methods=['POST'])
def pendulum_simulate():
    """Simulate double pendulum motion"""
    try:
        data = request.json
        
        m1 = float(data.get('m1', 1))
        m2 = float(data.get('m2', 1))
        L1 = float(data.get('L1', 1))
        L2 = float(data.get('L2', 1))
        theta1 = float(data.get('theta1', 90))
        theta2 = float(data.get('theta2', 90))
        omega1 = float(data.get('omega1', 0))
        omega2 = float(data.get('omega2', 0))
        t_max = float(data.get('t_max', 20))
        fps = int(data.get('fps', 100))
        
        result = pendulum_engine.solve_motion(
            m1, m2, L1, L2, theta1, theta2, omega1, omega2, t_max, fps
        )
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/pendulum/analyze', methods=['POST'])
def pendulum_analyze():
    """Generate all analysis graphs for double pendulum"""
    try:
        data = request.json
        
        m1 = float(data.get('m1', 1))
        m2 = float(data.get('m2', 1))
        L1 = float(data.get('L1', 1))
        L2 = float(data.get('L2', 1))
        theta1 = float(data.get('theta1', 90))
        theta2 = float(data.get('theta2', 90))
        omega1 = float(data.get('omega1', 0))
        omega2 = float(data.get('omega2', 0))
        t_max = float(data.get('t_max', 20))
        fps = int(data.get('fps', 100))
        
        # Get trajectory
        trajectory = pendulum_engine.solve_motion(
            m1, m2, L1, L2, theta1, theta2, omega1, omega2, t_max, fps
        )
        
        # Generate graphs
        graphs = {}
        
        graphs['angles'] = graph_gen.plot_angle_vs_time(trajectory)
        graphs['angular_velocity'] = graph_gen.plot_angular_velocity(trajectory)
        graphs['phase_space'] = graph_gen.plot_phase_space(trajectory)
        graphs['energy'] = graph_gen.plot_energy_conservation(trajectory)
        
        # FFT analysis
        fft_data = pendulum_engine.calculate_fft(trajectory)
        graphs['frequency'] = graph_gen.plot_frequency_spectrum(fft_data)
        
        # Position heatmap
        heatmap_data = pendulum_engine.calculate_position_heatmap(trajectory)
        graphs['heatmap'] = graph_gen.plot_position_heatmap(heatmap_data)
        
        return jsonify({
            'status': 'success',
            'graphs': graphs,
            'trajectory': trajectory
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


# ==================== PRESET CONFIGURATIONS ====================

@app.route('/api/presets/<simulation_type>', methods=['GET'])
def get_presets(simulation_type):
    """Get preset configurations"""
    
    if simulation_type == 'projectile':
        presets = {
            'basketball': {
                'name': 'Basketball Free Throw',
                'v0': 7.5,
                'angle': 52,
                'drag_coeff': 0.15,
                't_max': 3
            },
            'golf': {
                'name': 'Golf Drive',
                'v0': 70,
                'angle': 12,
                'drag_coeff': 0.25,
                't_max': 8
            },
            'soccer': {
                'name': 'Soccer Kick',
                'v0': 25,
                'angle': 30,
                'drag_coeff': 0.3,
                't_max': 5
            },
            'cannon': {
                'name': 'Cannonball',
                'v0': 100,
                'angle': 45,
                'drag_coeff': 0.05,
                't_max': 15
            },
            'vacuum': {
                'name': 'No Air Resistance (Theoretical)',
                'v0': 20,
                'angle': 45,
                'drag_coeff': 0,
                't_max': 5
            }
        }
    elif simulation_type == 'pendulum':
        presets = {
            'gentle': {
                'name': 'Gentle Swing',
                'm1': 1, 'm2': 1, 'L1': 1, 'L2': 1,
                'theta1': 30, 'theta2': 30,
                'omega1': 0, 'omega2': 0,
                't_max': 20, 'fps': 100
            },
            'chaotic': {
                'name': 'Chaotic Motion',
                'm1': 1, 'm2': 1, 'L1': 1, 'L2': 1,
                'theta1': 120, 'theta2': -30,
                'omega1': 0, 'omega2': 0,
                't_max': 30, 'fps': 100
            },
            'flip': {
                'name': 'Near Flip',
                'm1': 1, 'm2': 1, 'L1': 1, 'L2': 1,
                'theta1': 175, 'theta2': 175,
                'omega1': 0, 'omega2': 0,
                't_max': 25, 'fps': 100
            },
            'equal': {
                'name': 'Equal Lengths',
                'm1': 2, 'm2': 2, 'L1': 1.5, 'L2': 1.5,
                'theta1': 90, 'theta2': 90,
                'omega1': 0, 'omega2': 0,
                't_max': 20, 'fps': 100
            },
            'mass_diff': {
                'name': 'Extreme Mass Difference',
                'm1': 0.5, 'm2': 5, 'L1': 1, 'L2': 1,
                'theta1': 60, 'theta2': 60,
                'omega1': 0, 'omega2': 0,
                't_max': 20, 'fps': 100
            }
        }
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid simulation type'
        }), 400
    
    return jsonify({
        'status': 'success',
        'presets': presets
    })


# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("=" * 60)
    print("Physics Motion Simulator - Server Starting")
    print("=" * 60)
    print("Projectile Motion & Double Pendulum Simulations")
    print("\nServer running at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
