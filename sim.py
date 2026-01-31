import numpy as np
import sympy as smp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
import sys

# Symbolic setup
t, g = smp.symbols('t g')
m1, m2 = smp.symbols('m1 m2')
L1, L2 = smp.symbols('L1, L2')

the1, the2 = smp.symbols(r'\theta_1, \theta_2', cls=smp.Function)
the1 = the1(t)
the2 = the2(t)
the1_d = smp.diff(the1, t)
the2_d = smp.diff(the2, t)
the1_dd = smp.diff(the1_d, t)
the2_dd = smp.diff(the2_d, t)

# Position coordinates
x1 = L1*smp.sin(the1)
y1 = -L1*smp.cos(the1)
x2 = L1*smp.sin(the1) + L2*smp.sin(the2)
y2 = -L1*smp.cos(the1) - L2*smp.cos(the2)

# Kinetic Energy
T1 = 1/2 * m1 * (smp.diff(x1, t)**2 + smp.diff(y1, t)**2)
T2 = 1/2 * m2 * (smp.diff(x2, t)**2 + smp.diff(y2, t)**2)
T = T1 + T2

# Potential Energy
V1 = m1 * g * y1
V2 = m2 * g * y2
V = V1 + V2

# Lagrangian
L = T - V

# Lagrange Equations
LE1 = smp.diff(L, the1) - smp.diff(smp.diff(L, the1_d), t).simplify()
LE2 = smp.diff(L, the2) - smp.diff(smp.diff(L, the2_d), t).simplify()

# Solve for accelerations
sols = smp.solve([LE1, LE2], (the1_dd, the2_dd), simplify=False, rational=False)

# Convert to numerical functions
dz1dt_f = smp.lambdify((t,g,m1,m2,L1,L2,the1,the2,the1_d,the2_d), sols[the1_dd])
dz2dt_f = smp.lambdify((t,g,m1,m2,L1,L2,the1,the2,the1_d,the2_d), sols[the2_dd])
dthe1dt_f = smp.lambdify(the1_d, the1_d)
dthe2dt_f = smp.lambdify(the2_d, the2_d)

def dSdt(S, t, g, m1, m2, L1, L2):
    """Differential equations for double pendulum."""
    the1, z1, the2, z2 = S
    return [
        dthe1dt_f(z1),
        dz1dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
        dthe2dt_f(z2),
        dz2dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
    ]

def get_user_input():
    """Get and validate all user inputs."""
    print("\n" + "="*60)
    print("   DOUBLE PENDULUM SIMULATION")
    print("="*60)
    print("\nThis simulation shows chaotic motion of a double pendulum.")
    print("Small changes in initial conditions lead to vastly different results!\n")
    
    # Mass 1
    while True:
        try:
            m1 = float(input("Mass of 1st bob (0.1-100 kg): "))
            if 0.1 <= m1 <= 100:
                break
            print("❌ Mass must be between 0.1 and 100 kg")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Mass 2
    while True:
        try:
            m2 = float(input("Mass of 2nd bob (0.1-100 kg): "))
            if 0.1 <= m2 <= 100:
                break
            print("❌ Mass must be between 0.1 and 100 kg")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Length 1
    print("\n⚠️  Recommended: L1 + L2 < 6 for best visualization")
    while True:
        try:
            L1 = float(input("Length of 1st string (0.1-5 m): "))
            if 0.1 <= L1 <= 5:
                break
            print("❌ Length must be between 0.1 and 5 meters")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Length 2
    while True:
        try:
            L2 = float(input("Length of 2nd string (0.1-5 m): "))
            if 0.1 <= L2 <= 5:
                break
            print("❌ Length must be between 0.1 and 5 meters")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Initial angle 1
    print("\n📐 Initial angles (in degrees):")
    print("   - 0° = hanging straight down")
    print("   - 90° = horizontal")
    print("   - 180° = pointing straight up")
    while True:
        try:
            theta1_deg = float(input("Initial angle of 1st pendulum (-180 to 180°): "))
            if -180 <= theta1_deg <= 180:
                theta1_rad = theta1_deg * np.pi / 180
                break
            print("❌ Angle must be between -180 and 180 degrees")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Initial angle 2
    while True:
        try:
            theta2_deg = float(input("Initial angle of 2nd pendulum (-180 to 180°): "))
            if -180 <= theta2_deg <= 180:
                theta2_rad = theta2_deg * np.pi / 180
                break
            print("❌ Angle must be between -180 and 180 degrees")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Initial angular velocities
    print("\n🔄 Initial angular velocities (rad/s):")
    print("   - 0 = starting from rest")
    print("   - ±5 = moderate initial push")
    print("   - ±10 = strong initial push")
    while True:
        try:
            omega1 = float(input("Initial angular velocity of 1st (-20 to 20 rad/s): "))
            if -20 <= omega1 <= 20:
                break
            print("❌ Angular velocity must be between -20 and 20 rad/s")
        except ValueError:
            print("❌ Please enter a valid number")
    
    while True:
        try:
            omega2 = float(input("Initial angular velocity of 2nd (-20 to 20 rad/s): "))
            if -20 <= omega2 <= 20:
                break
            print("❌ Angular velocity must be between -20 and 20 rad/s")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Simulation time
    print("\n⏱️  Simulation duration:")
    while True:
        try:
            sim_time = float(input("Simulation time (5-100 seconds): "))
            if 5 <= sim_time <= 100:
                break
            print("❌ Time must be between 5 and 100 seconds")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Animation quality
    print("\n🎬 Animation quality:")
    print("   1. Low (fast, 50 frames)")
    print("   2. Medium (balanced, 100 frames)")
    print("   3. High (slow, 200 frames)")
    while True:
        try:
            quality = int(input("Choose quality (1-3): "))
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
                print("❌ Please choose 1, 2, or 3")
        except ValueError:
            print("❌ Please enter a valid number")
    
    return m1, m2, L1, L2, theta1_rad, theta2_rad, omega1, omega2, sim_time, frames

def get_x1y1x2y2(t, the1, the2, L1, L2):
    """Calculate Cartesian coordinates from angles."""
    return (L1*np.sin(the1),
            -L1*np.cos(the1),
            L1*np.sin(the1) + L2*np.sin(the2),
            -L1*np.cos(the1) - L2*np.cos(the2))

def main():
    """Main simulation function."""
    # Get user inputs
    m1, m2, L1, L2, theta1_0, theta2_0, omega1_0, omega2_0, sim_time, frames = get_user_input()
    
    print("\n" + "="*60)
    print("⚙️  Running simulation...")
    print("="*60)
    
    # Setup
    g = 9.81  # gravity
    t = np.linspace(0, sim_time, 1001)
    
    # Initial conditions: [theta1, omega1, theta2, omega2]
    y0 = [theta1_0, omega1_0, theta2_0, omega2_0]
    
    # Solve differential equations
    print("📊 Solving equations of motion...")
    ans = odeint(dSdt, y0=y0, t=t, args=(g, m1, m2, L1, L2))
    
    the1 = ans.T[0]
    the2 = ans.T[2]
    
    # Plot angle vs time
    print("📈 Creating angle plot...")
    plt.figure(figsize=(10, 6))
    plt.plot(t, the1 * 180/np.pi, label='θ₁ (First pendulum)', linewidth=2)
    plt.plot(t, the2 * 180/np.pi, label='θ₂ (Second pendulum)', linewidth=2)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Angle (degrees)', fontsize=14)
    plt.title('Double Pendulum Angles vs Time', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('pendulum_angles.png', dpi=150, bbox_inches='tight')
    print("✅ Saved: pendulum_angles.png")
    plt.close()
    
    # Get positions
    x1, y1, x2, y2 = get_x1y1x2y2(t, ans.T[0], ans.T[2], L1, L2)
    
    # Create animation
    print(f"🎬 Creating animation with {frames} frames...")
    
    def animate(i):
        idx = int(i * len(x1) / frames)  # Map frame to data index
        ln1.set_data([0, x1[idx], x2[idx]], [0, y1[idx], y2[idx]])
        trace.set_data(x2[max(0, idx-50):idx], y2[max(0, idx-50):idx])  # Trail
        return ln1, trace
    
    # Setup figure
    max_length = L1 + L2
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_facecolor('black')
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    
    # Pendulum line
    ln1, = plt.plot([], [], 'ro-', lw=3, markersize=10, markerfacecolor='red', 
                    markeredgecolor='white', markeredgewidth=2)
    
    # Trace line (shows path of second bob)
    trace, = plt.plot([], [], 'y-', lw=1, alpha=0.5)
    
    ax.set_ylim(-max_length - 0.5, max_length + 0.5)
    ax.set_xlim(-max_length - 0.5, max_length + 0.5)
    ax.set_aspect('equal')
    
    # Add title
    ax.text(0, max_length + 0.3, 'Double Pendulum Simulation', 
            color='white', fontsize=16, ha='center', weight='bold')
    
    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=frames, 
                                  interval=int(sim_time * 1000 / frames), 
                                  blit=True)
    
    # Save animation
    print("💾 Saving animation (this may take a minute)...")
    ani.save('double_pendulum_simulation.gif', writer='pillow', fps=25)
    print("✅ Saved: double_pendulum_simulation.gif")
    
    plt.close()
    
    print("\n" + "="*60)
    print("✨ SIMULATION COMPLETE!")
    print("="*60)
    print("Generated files:")
    print("  1. pendulum_angles.png - Angle vs time plot")
    print("  2. double_pendulum_simulation.gif - Animation")
    print("\n💡 Try running again with slightly different initial conditions")
    print("   to see the chaotic nature of the double pendulum!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Simulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        sys.exit(1)