"""
Projectile Motion Physics Engine
Simulates projectile motion with air resistance using numerical integration
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, List, Tuple


class ProjectileMotion:
    """Handles all projectile motion physics calculations"""
    
    def __init__(self, g: float = 9.81):
        """
        Initialize projectile motion calculator
        
        Args:
            g: Gravitational acceleration (default: 9.81 m/s²)
        """
        self.g = g
    
    def derivatives(self, t: float, state: np.ndarray, drag_coeff: float) -> np.ndarray:
        """
        Calculate derivatives for projectile motion with air resistance
        
        Args:
            t: Time
            state: [x, y, vx, vy] position and velocity
            drag_coeff: Drag coefficient (B)
            
        Returns:
            Derivatives [vx, vy, ax, ay]
        """
        x, y, vx, vy = state
        
        # Speed
        v = np.sqrt(vx**2 + vy**2)
        
        # Air resistance force components (F = -B*v*|v|)
        ax = -drag_coeff * vx * v
        ay = -self.g - drag_coeff * vy * v
        
        return np.array([vx, vy, ax, ay])
    
    def solve_trajectory(self, v0: float, angle_deg: float, drag_coeff: float, 
                        t_max: float = 20.0, num_points: int = 500) -> Dict:
        """
        Solve projectile motion trajectory
        
        Args:
            v0: Initial velocity (m/s)
            angle_deg: Launch angle (degrees)
            drag_coeff: Drag coefficient B
            t_max: Maximum simulation time
            num_points: Number of points to calculate
            
        Returns:
            Dictionary with trajectory data
        """
        angle_rad = np.radians(angle_deg)
        
        # Initial conditions
        vx0 = v0 * np.cos(angle_rad)
        vy0 = v0 * np.sin(angle_rad)
        state0 = [0, 0, vx0, vy0]
        
        # Event function to stop when hitting ground
        def hit_ground(t, state, drag_coeff):
            return state[1]  # y position
        hit_ground.terminal = True
        hit_ground.direction = -1
        
        # Solve ODE
        t_eval = np.linspace(0, t_max, num_points)
        solution = solve_ivp(
            self.derivatives,
            (0, t_max),
            state0,
            args=(drag_coeff,),
            t_eval=t_eval,
            events=hit_ground,
            method='RK45',
            dense_output=True
        )
        
        # Extract results
        t = solution.t
        x, y, vx, vy = solution.y
        
        # Filter out negative y values
        valid_idx = y >= 0
        t = t[valid_idx]
        x = x[valid_idx]
        y = y[valid_idx]
        vx = vx[valid_idx]
        vy = vy[valid_idx]
        
        # Calculate speed and energy
        speed = np.sqrt(vx**2 + vy**2)
        kinetic_energy = 0.5 * (vx**2 + vy**2)  # Per unit mass
        potential_energy = self.g * y
        total_energy = kinetic_energy + potential_energy
        
        # Find key metrics
        max_height_idx = np.argmax(y)
        max_height = y[max_height_idx]
        time_to_max_height = t[max_height_idx]
        total_flight_time = t[-1] if len(t) > 0 else 0
        horizontal_range = x[-1] if len(x) > 0 else 0
        
        # Impact velocity
        impact_speed = speed[-1] if len(speed) > 0 else 0
        impact_angle_rad = np.arctan2(vy[-1], vx[-1]) if len(vy) > 0 else 0
        impact_angle_deg = np.degrees(impact_angle_rad)
        
        # Energy loss
        initial_energy = 0.5 * v0**2
        final_energy = total_energy[-1] if len(total_energy) > 0 else 0
        energy_lost_percent = ((initial_energy - final_energy) / initial_energy * 100) if initial_energy > 0 else 0
        
        return {
            't': t.tolist(),
            'x': x.tolist(),
            'y': y.tolist(),
            'vx': vx.tolist(),
            'vy': vy.tolist(),
            'speed': speed.tolist(),
            'kinetic_energy': kinetic_energy.tolist(),
            'potential_energy': potential_energy.tolist(),
            'total_energy': total_energy.tolist(),
            'max_height': float(max_height),
            'time_to_max_height': float(time_to_max_height),
            'total_flight_time': float(total_flight_time),
            'horizontal_range': float(horizontal_range),
            'impact_speed': float(impact_speed),
            'impact_angle_deg': float(impact_angle_deg),
            'energy_lost_percent': float(energy_lost_percent)
        }
    
    def calculate_optimal_angle(self, v0: float, drag_coeff: float, 
                               angle_range: Tuple[int, int] = (20, 70),
                               step: int = 1) -> Tuple[float, float, List[float], List[float]]:
        """
        Find optimal launch angle for maximum range
        
        Args:
            v0: Initial velocity
            drag_coeff: Drag coefficient
            angle_range: Range of angles to test (min, max)
            step: Angle step size
            
        Returns:
            (optimal_angle, max_range, angles_list, ranges_list)
        """
        angles = list(range(angle_range[0], angle_range[1] + 1, step))
        ranges = []
        
        for angle in angles:
            result = self.solve_trajectory(v0, angle, drag_coeff, t_max=20, num_points=200)
            ranges.append(result['horizontal_range'])
        
        max_idx = np.argmax(ranges)
        optimal_angle = angles[max_idx]
        max_range = ranges[max_idx]
        
        return optimal_angle, max_range, angles, ranges
    
    def compare_trajectories(self, params_list: List[Dict]) -> List[Dict]:
        """
        Compare multiple trajectories with different parameters
        
        Args:
            params_list: List of parameter dictionaries
            
        Returns:
            List of trajectory results
        """
        results = []
        for params in params_list:
            result = self.solve_trajectory(
                v0=params.get('v0', 10),
                angle_deg=params.get('angle', 45),
                drag_coeff=params.get('drag_coeff', 0),
                t_max=params.get('t_max', 20)
            )
            result['label'] = params.get('label', 'Trajectory')
            result['color'] = params.get('color', '#3B82F6')
            results.append(result)
        
        return results
    
    def analyze_velocity_components(self, trajectory: Dict) -> Dict:
        """
        Analyze velocity components over time
        
        Args:
            trajectory: Trajectory data from solve_trajectory
            
        Returns:
            Dictionary with velocity analysis
        """
        t = np.array(trajectory['t'])
        vx = np.array(trajectory['vx'])
        vy = np.array(trajectory['vy'])
        speed = np.array(trajectory['speed'])
        
        return {
            't': t.tolist(),
            'vx': vx.tolist(),
            'vy': vy.tolist(),
            'speed': speed.tolist(),
            'vx_avg': float(np.mean(vx)),
            'vy_avg': float(np.mean(vy)),
            'speed_avg': float(np.mean(speed))
        }
    
    def compare_with_vacuum(self, v0: float, angle_deg: float, 
                           drag_coeff: float, t_max: float = 20) -> Dict:
        """
        Compare trajectory with air resistance vs vacuum
        
        Args:
            v0: Initial velocity
            angle_deg: Launch angle
            drag_coeff: Drag coefficient (for air resistance case)
            t_max: Maximum time
            
        Returns:
            Dictionary with both trajectories and comparison metrics
        """
        # With air resistance
        with_drag = self.solve_trajectory(v0, angle_deg, drag_coeff, t_max)
        
        # Vacuum (no air resistance)
        vacuum = self.solve_trajectory(v0, angle_deg, 0, t_max)
        
        # Calculate differences
        range_reduction = vacuum['horizontal_range'] - with_drag['horizontal_range']
        range_reduction_percent = (range_reduction / vacuum['horizontal_range'] * 100) if vacuum['horizontal_range'] > 0 else 0
        
        time_reduction = vacuum['total_flight_time'] - with_drag['total_flight_time']
        time_reduction_percent = (time_reduction / vacuum['total_flight_time'] * 100) if vacuum['total_flight_time'] > 0 else 0
        
        return {
            'with_drag': with_drag,
            'vacuum': vacuum,
            'range_reduction': float(range_reduction),
            'range_reduction_percent': float(range_reduction_percent),
            'time_reduction': float(time_reduction),
            'time_reduction_percent': float(time_reduction_percent)
        }
