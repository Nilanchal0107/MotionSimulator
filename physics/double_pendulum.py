"""
Double Pendulum Physics Engine
Simulates chaotic double pendulum motion using Lagrangian mechanics
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.fft import fft, fftfreq
from typing import Dict, List, Tuple


class DoublePendulum:
    """Handles all double pendulum physics calculations"""
    
    def __init__(self, g: float = 9.81):
        """
        Initialize double pendulum calculator
        
        Args:
            g: Gravitational acceleration (default: 9.81 m/s²)
        """
        self.g = g
    
    def derivatives(self, t: float, state: np.ndarray, m1: float, m2: float, 
                   L1: float, L2: float) -> np.ndarray:
        """
        Calculate derivatives using Lagrangian mechanics equations
        
        Args:
            t: Time
            state: [theta1, omega1, theta2, omega2]
            m1, m2: Masses of pendulum bobs
            L1, L2: Lengths of pendulum arms
            
        Returns:
            Derivatives [omega1, alpha1, omega2, alpha2]
        """
        theta1, omega1, theta2, omega2 = state
        
        # Delta theta
        delta = theta2 - theta1
        
        # Denominators for equations of motion
        den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) * np.cos(delta)
        den2 = (L2 / L1) * den1
        
        # Angular accelerations from Lagrangian equations
        alpha1 = (m2 * L1 * omega1 * omega1 * np.sin(delta) * np.cos(delta) +
                 m2 * self.g * np.sin(theta2) * np.cos(delta) +
                 m2 * L2 * omega2 * omega2 * np.sin(delta) -
                 (m1 + m2) * self.g * np.sin(theta1)) / den1
        
        alpha2 = (-m2 * L2 * omega2 * omega2 * np.sin(delta) * np.cos(delta) +
                 (m1 + m2) * self.g * np.sin(theta1) * np.cos(delta) -
                 (m1 + m2) * L1 * omega1 * omega1 * np.sin(delta) -
                 (m1 + m2) * self.g * np.sin(theta2)) / den2
        
        return np.array([omega1, alpha1, omega2, alpha2])
    
    def solve_motion(self, m1: float, m2: float, L1: float, L2: float,
                    theta1_deg: float, theta2_deg: float, 
                    omega1: float = 0, omega2: float = 0,
                    t_max: float = 20, fps: int = 100) -> Dict:
        """
        Solve double pendulum motion
        
        Args:
            m1, m2: Masses (kg)
            L1, L2: Lengths (m)
            theta1_deg, theta2_deg: Initial angles (degrees)
            omega1, omega2: Initial angular velocities (rad/s)
            t_max: Simulation duration (s)
            fps: Frames per second for animation
            
        Returns:
            Dictionary with motion data
        """
        # Convert angles to radians
        theta1_rad = np.radians(theta1_deg)
        theta2_rad = np.radians(theta2_deg)
        
        # Initial state
        state0 = [theta1_rad, omega1, theta2_rad, omega2]
        
        # Time points
        num_points = int(t_max * fps)
        t_eval = np.linspace(0, t_max, num_points)
        
        # Solve ODE
        solution = solve_ivp(
            self.derivatives,
            (0, t_max),
            state0,
            args=(m1, m2, L1, L2),
            t_eval=t_eval,
            method='RK45',
            dense_output=True
        )
        
        # Extract results
        t = solution.t
        theta1, omega1_t, theta2, omega2_t = solution.y
        
        # Convert to Cartesian coordinates for visualization
        x1 = L1 * np.sin(theta1)
        y1 = -L1 * np.cos(theta1)
        x2 = x1 + L2 * np.sin(theta2)
        y2 = y1 - L2 * np.cos(theta2)
        
        # Calculate energies
        # Kinetic energy
        v1_sq = (L1 * omega1_t)**2
        v2_sq = (L1 * omega1_t)**2 + (L2 * omega2_t)**2 + 2 * L1 * L2 * omega1_t * omega2_t * np.cos(theta1 - theta2)
        
        KE1 = 0.5 * m1 * v1_sq
        KE2 = 0.5 * m2 * v2_sq
        kinetic_energy = KE1 + KE2
        
        # Potential energy (using lowest point as reference)
        PE1 = m1 * self.g * y1
        PE2 = m2 * self.g * y2
        potential_energy = PE1 + PE2
        
        # Total energy
        total_energy = kinetic_energy + potential_energy
        
        # Energy error (should be constant)
        energy_error = np.std(total_energy) / np.abs(np.mean(total_energy)) * 100 if np.abs(np.mean(total_energy)) > 0 else 0
        
        # Count rotations
        rotations1 = self._count_rotations(theta1)
        rotations2 = self._count_rotations(theta2)
        
        # Calculate max values
        max_theta1 = float(np.max(np.abs(theta1)))
        max_theta2 = float(np.max(np.abs(theta2)))
        max_omega1 = float(np.max(np.abs(omega1_t)))
        max_omega2 = float(np.max(np.abs(omega2_t)))
        
        return {
            't': t.tolist(),
            'theta1': theta1.tolist(),
            'theta2': theta2.tolist(),
            'omega1': omega1_t.tolist(),
            'omega2': omega2_t.tolist(),
            'x1': x1.tolist(),
            'y1': y1.tolist(),
            'x2': x2.tolist(),
            'y2': y2.tolist(),
            'kinetic_energy': kinetic_energy.tolist(),
            'potential_energy': potential_energy.tolist(),
            'total_energy': total_energy.tolist(),
            'KE1': KE1.tolist(),
            'KE2': KE2.tolist(),
            'PE1': PE1.tolist(),
            'PE2': PE2.tolist(),
            'energy_error_percent': float(energy_error),
            'max_theta1_rad': float(max_theta1),
            'max_theta2_rad': float(max_theta2),
            'max_theta1_deg': float(np.degrees(max_theta1)),
            'max_theta2_deg': float(np.degrees(max_theta2)),
            'max_omega1': float(max_omega1),
            'max_omega2': float(max_omega2),
            'rotations1': int(rotations1),
            'rotations2': int(rotations2),
            'params': {
                'm1': m1, 'm2': m2, 'L1': L1, 'L2': L2,
                'theta1_deg': theta1_deg, 'theta2_deg': theta2_deg,
                'omega1': omega1, 'omega2': omega2
            }
        }
    
    def _count_rotations(self, theta: np.ndarray) -> int:
        """Count number of full rotations (crossings of ±π)"""
        # Unwrap angles to count continuous rotations
        theta_unwrapped = np.unwrap(theta)
        rotations = np.abs(theta_unwrapped[-1] - theta_unwrapped[0]) / (2 * np.pi)
        return int(rotations)
    
    def calculate_chaos_metrics(self, trajectory1: Dict, trajectory2: Dict) -> Dict:
        """
        Calculate chaos metrics by comparing two similar trajectories
        
        Args:
            trajectory1, trajectory2: Two trajectories with slightly different initial conditions
            
        Returns:
            Dictionary with chaos metrics including Lyapunov exponent estimate
        """
        t = np.array(trajectory1['t'])
        x1_1 = np.array(trajectory1['x2'])
        y1_1 = np.array(trajectory1['y2'])
        x2_1 = np.array(trajectory2['x2'])
        y2_1 = np.array(trajectory2['y2'])
        
        # Calculate distance between second bobs
        distance = np.sqrt((x1_1 - x2_1)**2 + (y1_1 - y2_1)**2)
        
        # Initial separation
        d0 = distance[0] if distance[0] > 0 else 1e-10
        
        # Avoid log(0) by replacing zeros with small values
        distance_safe = np.maximum(distance, 1e-10)
        
        # Log of separation ratio
        log_separation = np.log(distance_safe / d0)
        
        # Estimate Lyapunov exponent from linear fit (early exponential growth phase)
        # Use first half of data where exponential growth is clearest
        half_idx = len(t) // 3
        if half_idx > 10:
            # Find where distance starts growing significantly
            growth_start = 0
            for i in range(1, half_idx):
                if distance[i] > 2 * d0:
                    growth_start = i
                    break
            
            if growth_start > 0 and half_idx > growth_start + 10:
                t_fit = t[growth_start:half_idx]
                log_sep_fit = log_separation[growth_start:half_idx]
                
                # Linear regression: log(d/d0) = λ*t
                lyapunov = np.polyfit(t_fit, log_sep_fit, 1)[0]
            else:
                lyapunov = 0.0
        else:
            lyapunov = 0.0
        
        # Chaos rating based on Lyapunov exponent
        if lyapunov < 0.1:
            chaos_rating = "Low"
        elif lyapunov < 0.5:
            chaos_rating = "Medium"
        else:
            chaos_rating = "High"
        
        # Predictability time (when distance reaches certain threshold, e.g. 10% of pendulum length)
        L_total = trajectory1['params']['L1'] + trajectory1['params']['L2']
        threshold = 0.1 * L_total
        
        predictability_time = t[-1]  # Default to full simulation time
        for i, d in enumerate(distance):
            if d > threshold:
                predictability_time = t[i]
                break
        
        return {
            't': t.tolist(),
            'distance': distance.tolist(),
            'log_separation': log_separation.tolist(),
            'lyapunov_exponent': float(lyapunov),
            'chaos_rating': chaos_rating,
            'predictability_time': float(predictability_time),
            'initial_separation': float(d0),
            'final_separation': float(distance[-1])
        }
    
    def calculate_fft(self, trajectory: Dict) -> Dict:
        """
        Calculate frequency spectrum of pendulum motion
        
        Args:
            trajectory: Trajectory data
            
        Returns:
            Dictionary with FFT results
        """
        t = np.array(trajectory['t'])
        theta2 = np.array(trajectory['theta2'])
        
        # Sampling rate
        dt = t[1] - t[0] if len(t) > 1 else 1
        sampling_rate = 1 / dt
        
        # Perform FFT
        N = len(theta2)
        yf = fft(theta2)
        xf = fftfreq(N, dt)[:N//2]
        
        # Power spectrum (magnitude)
        power = 2.0/N * np.abs(yf[0:N//2])
        
        # Find dominant frequencies
        peaks_idx = self._find_peaks(power, threshold=0.1*np.max(power))
        dominant_frequencies = xf[peaks_idx].tolist()
        dominant_powers = power[peaks_idx].tolist()
        
        return {
            'frequencies': xf.tolist(),
            'power': power.tolist(),
            'dominant_frequencies': dominant_frequencies,
            'dominant_powers': dominant_powers,
            'sampling_rate': float(sampling_rate)
        }
    
    def _find_peaks(self, data: np.ndarray, threshold: float = 0) -> np.ndarray:
        """Find peaks in data above threshold"""
        peaks = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i-1] and data[i] > data[i+1] and data[i] > threshold:
                peaks.append(i)
        return np.array(peaks)
    
    def calculate_position_heatmap(self, trajectory: Dict, grid_size: int = 50) -> Dict:
        """
        Calculate 2D heatmap of where second bob spends time
        
        Args:
            trajectory: Trajectory data
            grid_size: Number of bins in each dimension
            
        Returns:
            Dictionary with heatmap data
        """
        x2 = np.array(trajectory['x2'])
        y2 = np.array(trajectory['y2'])
        
        # Create 2D histogram
        L_total = trajectory['params']['L1'] + trajectory['params']['L2']
        range_limit = L_total * 1.1
        
        heatmap, xedges, yedges = np.histogram2d(
            x2, y2,
            bins=grid_size,
            range=[[-range_limit, range_limit], [-range_limit, range_limit]]
        )
        
        # Normalize
        heatmap = heatmap / np.max(heatmap) if np.max(heatmap) > 0 else heatmap
        
        # Get bin centers
        x_centers = (xedges[:-1] + xedges[1:]) / 2
        y_centers = (yedges[:-1] + yedges[1:]) / 2
        
        return {
            'heatmap': heatmap.tolist(),
            'x_centers': x_centers.tolist(),
            'y_centers': y_centers.tolist(),
            'x_edges': xedges.tolist(),
            'y_edges': yedges.tolist()
        }
    
    def compare_chaos(self, m1: float, m2: float, L1: float, L2: float,
                     theta1_deg: float, theta2_deg: float,
                     omega1: float, omega2: float,
                     difference: float = 0.1, t_max: float = 20, 
                     fps: int = 100) -> Dict:
        """
        Demonstrate chaos by comparing two trajectories with tiny difference
        
        Args:
            Parameters for first trajectory
            difference: Tiny difference in theta1 for second trajectory (degrees)
            
        Returns:
            Dictionary with both trajectories and chaos analysis
        """
        # First trajectory
        traj1 = self.solve_motion(m1, m2, L1, L2, theta1_deg, theta2_deg, 
                                  omega1, omega2, t_max, fps)
        
        # Second trajectory with tiny difference
        traj2 = self.solve_motion(m1, m2, L1, L2, theta1_deg + difference, theta2_deg,
                                  omega1, omega2, t_max, fps)
        
        # Calculate chaos metrics
        chaos_metrics = self.calculate_chaos_metrics(traj1, traj2)
        
        return {
            'trajectory1': traj1,
            'trajectory2': traj2,
            'chaos_metrics': chaos_metrics,
            'initial_difference_deg': difference
        }
