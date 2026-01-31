import numpy as np
import sympy as smp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
import sys

# Symbolic variables
t, m, g = smp.symbols('t m g')
the = smp.symbols(r'\theta', cls=smp.Function)
the = the(t)
the_d = smp.diff(the, t)
the_dd = smp.diff(the_d, t)

x, y = smp.symbols('x y', cls=smp.Function)
x = x(the)
y = y(the)

def get_user_input():
    """Get and validate user input for simulation parameters."""
    print("\n" + "="*70)
    print(" "*15 + "BEAD ON A WIRE SIMULATION")
    print("="*70)
    print("\nThis simulation shows a bead sliding down a curved wire")
    print("under the influence of gravity (no friction).\n")
    
    # Choose path type
    print("🛤️  Available Wire Paths:\n")
    print("  [1] Tautochrone - Cycloid curve")
    print("      └─ Special property: Equal time for all starting positions!")
    print("      └─ Shape: Curved, like a skateboard ramp")
    print()
    print("  [2] Parabolic - Simple parabola")
    print("      └─ Classic U-shaped curve")
    print("      └─ Different times for different starting positions")
    print()
    
    while True:
        try:
            path_choice = int(input("Choose wire path (1 or 2): "))
            if path_choice in [1, 2]:
                path = 'taut' if path_choice == 1 else 'parab'
                break
            print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get starting angles for two beads
    print("\n📐 Starting Positions (Angle θ):")
    if path == 'taut':
        print("   - Valid range: 0° to 90° (0 to π/2 radians)")
        print("   - 0° = top of the curve")
        print("   - 90° = halfway down")
        max_angle = np.pi/2
    else:
        print("   - Valid range: 0° to 60° (0 to π/3 radians)")
        print("   - 0° = top of the parabola")
        print("   - 45° = partway down")
        max_angle = np.pi/3
    
    print("\n🔴 First Bead:")
    while True:
        try:
            angle1_deg = float(input(f"  Starting angle (0-{int(max_angle*180/np.pi)}°): "))
            angle1_rad = angle1_deg * np.pi / 180
            if 0.01 <= angle1_rad <= max_angle:
                break
            print(f"❌ Angle must be between 0 and {int(max_angle*180/np.pi)} degrees")
        except ValueError:
            print("❌ Please enter a valid number")
    
    print("\n🔵 Second Bead:")
    while True:
        try:
            angle2_deg = float(input(f"  Starting angle (0-{int(max_angle*180/np.pi)}°): "))
            angle2_rad = angle2_deg * np.pi / 180
            if 0.01 <= angle2_rad <= max_angle:
                if abs(angle1_rad - angle2_rad) < 0.01:
                    print("⚠️  Warning: Angles are too similar, beads will overlap!")
                    confirm = input("  Continue anyway? (y/n): ")
                    if confirm.lower() == 'y':
                        break
                else:
                    break
            print(f"❌ Angle must be between 0 and {int(max_angle*180/np.pi)} degrees")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get initial velocities
    print("\n🏃 Initial Velocities:")
    print("   - 0 rad/s = starting from rest (most common)")
    print("   - Positive = pushed forward")
    print("   - Negative = pushed backward")
    
    print("\n🔴 First Bead:")
    while True:
        try:
            vel1 = float(input("  Initial velocity (-5 to 5 rad/s): "))
            if -5 <= vel1 <= 5:
                break
            print("❌ Velocity must be between -5 and 5 rad/s")
        except ValueError:
            print("❌ Please enter a valid number")
    
    print("\n🔵 Second Bead:")
    while True:
        try:
            vel2 = float(input("  Initial velocity (-5 to 5 rad/s): "))
            if -5 <= vel2 <= 5:
                break
            print("❌ Velocity must be between -5 and 5 rad/s")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Simulation time
    print("\n⏱️  Simulation Settings:")
    while True:
        try:
            sim_time = float(input("  Simulation duration (5-60 seconds): "))
            if 5 <= sim_time <= 60:
                break
            print("❌ Time must be between 5 and 60 seconds")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Animation quality
    print("\n🎬 Animation Quality:")
    print("   [1] Low (50 frames) - Fast")
    print("   [2] Medium (100 frames) - Balanced")
    print("   [3] High (200 frames) - Smooth")
    while True:
        try:
            quality = int(input("  Choose quality (1-3): "))
            if quality == 1:
                frames = 50
                break
            elif quality == 2:
                frames = 100
                break
            elif quality == 3:
                frames = 200
                break
            else:
                print("❌ Please enter 1, 2, or 3")
        except ValueError:
            print("❌ Please enter a valid number")
    
    return path, angle1_rad, angle2_rad, vel1, vel2, sim_time, frames

def setup_path(path):
    """Setup the wire path equations."""
    global x, y, x_f, y_f, the
    
    if path == 'taut':
        # Tautochrone (cycloid) path
        x = smp.sin(2*the) + 2*the
        y = 1 - smp.cos(2*the)
        x_f = smp.lambdify(the, x)
        y_f = smp.lambdify(the, y)
        path_name = "Tautochrone (Cycloid)"
    else:
        # Parabolic path
        x = the
        y = the**2
        x_f = smp.lambdify(the, x)
        y_f = smp.lambdify(the, y)
        path_name = "Parabolic"
    
    return x, y, x_f, y_f, path_name

def derive_equations(x, y):
    """Derive equations of motion using Lagrangian mechanics."""
    # Kinetic energy
    T = 1/2 * m * (smp.diff(x, t)**2 + smp.diff(y, t)**2)
    
    # Potential energy
    V = m * g * y
    
    # Lagrangian
    L = T - V
    
    # Lagrange equation
    LE = smp.diff(L, the) - smp.diff(smp.diff(L, the_d), t)
    LE = LE.simplify()
    
    # Solve for acceleration
    deriv_2 = smp.solve(LE, the_dd)[0]
    deriv_1 = the_d
    
    # Convert to numerical functions
    deriv2_f = smp.lambdify((g, the, the_d), deriv_2)
    deriv1_f = smp.lambdify(the_d, the_d)
    
    return deriv1_f, deriv2_f

def dSdt_factory(deriv1_f, deriv2_f, g_val):
    """Create the differential equation function."""
    def dSdt(S, t):
        return [
            deriv1_f(S[1]),           # dθ/dt
            deriv2_f(g_val, S[0], S[1])  # dω/dt
        ]
    return dSdt

def simulate_motion(dSdt, y0_1, y0_2, t_array):
    """Simulate the motion of two beads."""
    ans1 = odeint(dSdt, y0=y0_1, t=t_array)
    ans2 = odeint(dSdt, y0=y0_2, t=t_array)
    return ans1, ans2

def plot_angles(t_array, ans1, ans2, angle1_deg, angle2_deg):
    """Plot angle vs time for both beads."""
    plt.figure(figsize=(12, 6))
    plt.plot(t_array, ans1.T[0] * 180/np.pi, 'r-', linewidth=2, 
             label=f'Bead 1 (start: {angle1_deg:.1f}°)')
    plt.plot(t_array, ans2.T[0] * 180/np.pi, 'b-', linewidth=2, 
             label=f'Bead 2 (start: {angle2_deg:.1f}°)')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Angle θ (degrees)', fontsize=14)
    plt.title('Bead Position vs Time', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('bead_angles.png', dpi=150, bbox_inches='tight')
    print("✅ Saved: bead_angles.png")
    plt.close()

def create_animation(x1, y1, x2, y2, x_f, y_f, theta_range, frames, path_name):
    """Create and save the animation."""
    def animate(i):
        idx = int(i * len(x1) / frames)
        ln1.set_data([x1[idx]], [y1[idx]])
        ln2.set_data([x2[idx]], [y2[idx]])
        # Update trails
        trail_len = 30
        start_idx = max(0, idx - trail_len)
        trail1.set_data(x1[start_idx:idx], y1[start_idx:idx])
        trail2.set_data(x2[start_idx:idx], y2[start_idx:idx])
        return ln1, ln2, trail1, trail2
    
    # Setup figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.grid(True, alpha=0.3)
    
    # Plot the wire path
    theta_path = np.linspace(theta_range[0], theta_range[1], 500)
    x_path = x_f(theta_path)
    y_path = y_f(theta_path)
    ax.plot(x_path, y_path, 'k-', linewidth=3, label='Wire path', alpha=0.7)
    
    # Bead markers
    ln1, = plt.plot([], [], 'ro', markersize=12, label='Bead 1', 
                    markeredgecolor='darkred', markeredgewidth=2)
    ln2, = plt.plot([], [], 'bo', markersize=12, label='Bead 2', 
                    markeredgecolor='darkblue', markeredgewidth=2)
    
    # Trails
    trail1, = plt.plot([], [], 'r-', linewidth=1, alpha=0.5)
    trail2, = plt.plot([], [], 'b-', linewidth=1, alpha=0.5)
    
    # Set limits with padding
    x_min, x_max = min(x_path), max(x_path)
    y_min, y_max = min(y_path), max(y_path)
    x_padding = (x_max - x_min) * 0.1
    y_padding = (y_max - y_min) * 0.1
    
    ax.set_xlim(x_min - x_padding, x_max + x_padding)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)
    ax.set_aspect('equal')
    
    ax.set_xlabel('x position', fontsize=14)
    ax.set_ylabel('y position', fontsize=14)
    ax.set_title(f'Bead on Wire: {path_name}', fontsize=16, weight='bold')
    ax.legend(fontsize=11, loc='upper right')
    
    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=frames, 
                                  interval=50, blit=True)
    
    return ani, fig

def main():
    """Main simulation function."""
    # Get user inputs
    path, angle1, angle2, vel1, vel2, sim_time, frames = get_user_input()
    
    print("\n" + "="*70)
    print("⚙️  Setting up simulation...")
    print("="*70)
    
    # Setup path
    print("📐 Deriving equations of motion...")
    x_eq, y_eq, x_f, y_f, path_name = setup_path(path)
    
    # Derive equations
    deriv1_f, deriv2_f = derive_equations(x_eq, y_eq)
    
    # Setup simulation
    g_val = 9.81
    t_array = np.linspace(0, sim_time, 1000)
    dSdt = dSdt_factory(deriv1_f, deriv2_f, g_val)
    
    # Initial conditions: [angle, angular_velocity]
    y0_1 = [angle1, vel1]
    y0_2 = [angle2, vel2]
    
    # Run simulation
    print("🔬 Solving differential equations...")
    ans1, ans2 = simulate_motion(dSdt, y0_1, y0_2, t_array)
    
    # Plot angles
    print("📊 Creating angle plot...")
    plot_angles(t_array, ans1, ans2, angle1*180/np.pi, angle2*180/np.pi)
    
    # Get positions
    def get_xy(theta):
        return x_f(theta), y_f(theta)
    
    x1, y1 = get_xy(ans1.T[0])
    x2, y2 = get_xy(ans2.T[0])
    
    # Create animation
    print(f"🎬 Creating animation with {frames} frames...")
    
    theta_range = [0, max(angle1, angle2) * 1.5]
    ani, fig = create_animation(x1, y1, x2, y2, x_f, y_f, theta_range, 
                                frames, path_name)
    
    # Save animation
    print("💾 Saving animation (this may take a minute)...")
    ani.save('bead_on_wire.gif', writer='pillow', fps=25)
    print("✅ Saved: bead_on_wire.gif")
    plt.close()
    
    # Summary
    print("\n" + "="*70)
    print("✨ SIMULATION COMPLETE!")
    print("="*70)
    print(f"Path: {path_name}")
    print(f"Bead 1: Started at {angle1*180/np.pi:.1f}° with {vel1:.2f} rad/s")
    print(f"Bead 2: Started at {angle2*180/np.pi:.1f}° with {vel2:.2f} rad/s")
    print(f"\nGenerated files:")
    print("  1. bead_angles.png - Angle vs time plot")
    print("  2. bead_on_wire.gif - Animation")
    
    if path == 'taut':
        print("\n💡 Fun Fact about Tautochrone:")
        print("   Both beads should reach the bottom at approximately")
        print("   the same time, regardless of starting position!")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Simulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)