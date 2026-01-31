"""
Graph Generation Module
Creates all matplotlib visualizations and converts them to base64 images
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from typing import Dict, List


class GraphGenerator:
    """Generates all physics visualization graphs"""
    
    def __init__(self, dpi: int = 100, figsize: tuple = (8, 6)):
        """
        Initialize graph generator
        
        Args:
            dpi: Resolution for images
            figsize: Default figure size in inches
        """
        self.dpi = dpi
        self.figsize = figsize
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
    
    # ==================== PROJECTILE MOTION GRAPHS ====================
    
    def plot_trajectory(self, trajectories: List[Dict], comparison_mode: bool = False) -> str:
        """Plot projectile trajectory/trajectories"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        colors = ['#EF4444', '#3B82F6', '#10B981']
        
        for i, traj in enumerate(trajectories):
            x = traj['x']
            y = traj['y']
            label = traj.get('label', f'Trajectory {i+1}')
            color = traj.get('color', colors[i % len(colors)])
            
            ax.plot(x, y, color=color, linewidth=2.5, label=label, alpha=0.9)
            
            # Mark start and end
            if x and y:
                ax.plot(x[0], y[0], 'o', color=color, markersize=8, zorder=5)
                ax.plot(x[-1], y[-1], 's', color=color, markersize=8, zorder=5)
        
        ax.set_xlabel('Horizontal Distance (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
        ax.set_title('Projectile Trajectory', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, alpha=0.7, label='Ground')
        
        if comparison_mode or len(trajectories) > 1:
            ax.legend(fontsize=10, loc='upper right')
        
        ax.set_ylim(bottom=0)
        
        return self._fig_to_base64(fig)
    
    def plot_velocity_components(self, data: Dict) -> str:
        """Plot velocity components over time"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(self.figsize[0], 10))
        
        t = data['t']
        vx = data['vx']
        vy = data['vy']
        speed = data['speed']
        
        # Horizontal velocity
        ax1.plot(t, vx, color='#3B82F6', linewidth=2, label='Vx')
        ax1.set_ylabel('Vx (m/s)', fontsize=11, fontweight='bold')
        ax1.set_title('Horizontal Velocity', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Vertical velocity
        ax2.plot(t, vy, color='#EF4444', linewidth=2, label='Vy')
        ax2.set_ylabel('Vy (m/s)', fontsize=11, fontweight='bold')
        ax2.set_title('Vertical Velocity', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Speed
        ax3.plot(t, speed, color='#10B981', linewidth=2.5, label='Speed')
        ax3.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Speed (m/s)', fontsize=11, fontweight='bold')
        ax3.set_title('Total Speed', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_height_vs_time(self, data: Dict) -> str:
        """Plot height versus time"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        t = data['t']
        y = data['y']
        
        ax.plot(t, y, color='#8B5CF6', linewidth=2.5)
        ax.fill_between(t, y, alpha=0.3, color='#8B5CF6')
        
        # Mark maximum height
        if y:
            max_idx = np.argmax(y)
            ax.plot(t[max_idx], y[max_idx], 'ro', markersize=10, 
                   label=f'Max: {y[max_idx]:.2f} m at t={t[max_idx]:.2f} s')
        
        ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
        ax.set_title('Height vs Time', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_ylim(bottom=0)
        
        return self._fig_to_base64(fig)
    
    def plot_range_analysis(self, trajectories: List[Dict]) -> str:
        """Plot range comparison"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        labels = [traj.get('label', f'Traj {i+1}') for i, traj in enumerate(trajectories)]
        ranges = [traj['horizontal_range'] for traj in trajectories]
        colors = [traj.get('color', '#3B82F6') for traj in trajectories]
        
        bars = ax.bar(labels, ranges, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, range_val in zip(bars, ranges):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{range_val:.2f} m',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Range (m)', fontsize=12, fontweight='bold')
        ax.set_title('Horizontal Range Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        return self._fig_to_base64(fig)
    
    def plot_optimal_angle_curve(self, angles: List[float], ranges: List[float], 
                                 optimal_angle: float, max_range: float) -> str:
        """Plot angle vs range curve showing optimal angle"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(angles, ranges, color='#3B82F6', linewidth=2.5, marker='o', 
               markersize=4, label='Range vs Angle')
        
        # Highlight optimal angle
        ax.axvline(x=optimal_angle, color='#EF4444', linestyle='--', linewidth=2,
                  label=f'Optimal: {optimal_angle}° → {max_range:.2f} m')
        ax.plot(optimal_angle, max_range, 'r*', markersize=20, zorder=5)
        
        ax.set_xlabel('Launch Angle (degrees)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Range (m)', fontsize=12, fontweight='bold')
        ax.set_title('Optimal Launch Angle Analysis', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10, loc='upper right')
        
        return self._fig_to_base64(fig)
    
    def plot_energy_analysis(self, data: Dict) -> str:
        """Plot energy components over time"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        t = data['t']
        ke = data['kinetic_energy']
        pe = data['potential_energy']
        te = data['total_energy']
        
        ax.plot(t, ke, color='#EF4444', linewidth=2, label='Kinetic Energy', alpha=0.9)
        ax.plot(t, pe, color='#3B82F6', linewidth=2, label='Potential Energy', alpha=0.9)
        ax.plot(t, te, color='#10B981', linewidth=2.5, label='Total Energy', 
               linestyle='--', alpha=0.9)
        
        ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Energy per unit mass (J/kg)', fontsize=12, fontweight='bold')
        ax.set_title('Energy Analysis', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        return self._fig_to_base64(fig)
    
    def plot_air_resistance_comparison(self, with_drag: Dict, vacuum: Dict) -> str:
        """Compare trajectories with and without air resistance"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(with_drag['x'], with_drag['y'], color='#EF4444', linewidth=2.5,
               label='With Air Resistance', alpha=0.9)
        ax.plot(vacuum['x'], vacuum['y'], color='#3B82F6', linewidth=2.5,
               label='Vacuum (No Drag)', linestyle='--', alpha=0.9)
        
        ax.set_xlabel('Horizontal Distance (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Height (m)', fontsize=12, fontweight='bold')
        ax.set_title('Air Resistance Impact', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11, loc='upper right')
        ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, alpha=0.7)
        ax.set_ylim(bottom=0)
        
        return self._fig_to_base64(fig)
    
    # ==================== DOUBLE PENDULUM GRAPHS ====================
    
    def plot_angle_vs_time(self, data: Dict) -> str:
        """Plot angles over time for both pendulums"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], 8))
        
        t = data['t']
        theta1 = np.degrees(data['theta1'])
        theta2 = np.degrees(data['theta2'])
        
        ax1.plot(t, theta1, color='#EF4444', linewidth=1.5, label='θ₁')
        ax1.set_ylabel('Angle θ₁ (degrees)', fontsize=11, fontweight='bold')
        ax1.set_title('First Pendulum Angle', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        ax2.plot(t, theta2, color='#3B82F6', linewidth=1.5, label='θ₂')
        ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Angle θ₂ (degrees)', fontsize=11, fontweight='bold')
        ax2.set_title('Second Pendulum Angle', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_angular_velocity(self, data: Dict) -> str:
        """Plot angular velocities over time"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], 8))
        
        t = data['t']
        omega1 = data['omega1']
        omega2 = data['omega2']
        
        ax1.plot(t, omega1, color='#EF4444', linewidth=1.5)
        ax1.set_ylabel('ω₁ (rad/s)', fontsize=11, fontweight='bold')
        ax1.set_title('First Pendulum Angular Velocity', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        ax2.plot(t, omega2, color='#3B82F6', linewidth=1.5)
        ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('ω₂ (rad/s)', fontsize=11, fontweight='bold')
        ax2.set_title('Second Pendulum Angular Velocity', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_phase_space(self, data: Dict) -> str:
        """Plot phase space diagrams"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        theta1 = np.degrees(data['theta1'])
        theta2 = np.degrees(data['theta2'])
        omega1 = data['omega1']
        omega2 = data['omega2']
        
        # Create time-based colormap
        t = np.array(data['t'])
        colors1 = t
        colors2 = t
        
        # Phase space 1
        scatter1 = ax1.scatter(theta1, omega1, c=colors1, cmap='plasma', 
                              s=1, alpha=0.6)
        ax1.set_xlabel('θ₁ (degrees)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('ω₁ (rad/s)', fontsize=11, fontweight='bold')
        ax1.set_title('Phase Space: Pendulum 1', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Phase space 2
        scatter2 = ax2.scatter(theta2, omega2, c=colors2, cmap='plasma',
                              s=1, alpha=0.6)
        ax2.set_xlabel('θ₂ (degrees)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('ω₂ (rad/s)', fontsize=11, fontweight='bold')
        ax2.set_title('Phase Space: Pendulum 2', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter2, ax=ax2)
        cbar.set_label('Time (s)', fontsize=10)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_energy_conservation(self, data: Dict) -> str:
        """Plot energy conservation for double pendulum"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        t = data['t']
        ke = data['kinetic_energy']
        pe = data['potential_energy']
        te = data['total_energy']
        
        ax.plot(t, ke, color='#EF4444', linewidth=1.5, label='Kinetic', alpha=0.8)
        ax.plot(t, pe, color='#3B82F6', linewidth=1.5, label='Potential', alpha=0.8)
        ax.plot(t, te, color='#10B981', linewidth=2.5, label='Total', 
               linestyle='--', alpha=0.9)
        
        ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Energy (J)', fontsize=12, fontweight='bold')
        ax.set_title(f'Energy Conservation (Error: {data["energy_error_percent"]:.4f}%)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        return self._fig_to_base64(fig)
    
    def plot_chaos_divergence(self, chaos_data: Dict) -> str:
        """Plot exponential divergence showing chaos"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], 8))
        
        t = chaos_data['t']
        distance = chaos_data['distance']
        log_sep = chaos_data['log_separation']
        
        # Linear plot of distance
        ax1.plot(t, distance, color='#EF4444', linewidth=2)
        ax1.set_ylabel('Distance (m)', fontsize=11, fontweight='bold')
        ax1.set_title('Separation Between Second Bobs', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # Log plot showing exponential growth
        ax2.plot(t, log_sep, color='#3B82F6', linewidth=2)
        ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('ln(distance/d₀)', fontsize=11, fontweight='bold')
        ax2.set_title(f'Exponential Divergence (λ ≈ {chaos_data["lyapunov_exponent"]:.3f})', 
                     fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_position_heatmap(self, heatmap_data: Dict) -> str:
        """Plot 2D heatmap of bob positions"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        heatmap = np.array(heatmap_data['heatmap'])
        x_centers = heatmap_data['x_centers']
        y_centers = heatmap_data['y_centers']
        
        im = ax.imshow(heatmap.T, origin='lower', cmap='hot', aspect='auto',
                      extent=[x_centers[0], x_centers[-1], y_centers[0], y_centers[-1]])
        
        ax.set_xlabel('X Position (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y Position (m)', fontsize=12, fontweight='bold')
        ax.set_title('Position Heatmap (Second Bob)', fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Frequency (normalized)', fontsize=10)
        
        # Add circle showing pendulum reach
        return self._fig_to_base64(fig)
    
    def plot_frequency_spectrum(self, fft_data: Dict) -> str:
        """Plot frequency spectrum from FFT"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        frequencies = fft_data['frequencies']
        power = fft_data['power']
        
        ax.plot(frequencies, power, color='#8B5CF6', linewidth=2)
        
        # Mark dominant frequencies
        if fft_data['dominant_frequencies']:
            dom_freq = fft_data['dominant_frequencies']
            dom_pow = fft_data['dominant_powers']
            ax.plot(dom_freq, dom_pow, 'ro', markersize=8, 
                   label=f'Dominant: {dom_freq[0]:.2f} Hz' if dom_freq else '')
        
        ax.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Power', fontsize=12, fontweight='bold')
        ax.set_title('Frequency Spectrum (FFT)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        if fft_data['dominant_frequencies']:
            ax.legend(fontsize=10)
        ax.set_xlim(left=0, right=10)  # Focus on lower frequencies
        
        return self._fig_to_base64(fig)
