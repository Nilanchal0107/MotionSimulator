import numpy as np
import scipy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def dSdt(t, S, B):
    """Differential equation for projectile motion with drag."""
    x, vx, y, vy = S
    return [vx,
    -B*np.sqrt(vx**2 + vy**2)*vx,
    vy,
    -1-B*np.sqrt(vx**2 + vy**2)*vy]

def get_user_input():
    """Get and validate user input for simulation parameters."""
    print("\n=== PROJECTILE MOTION SIMULATOR ===\n")
    
    while True:
        try:
            # Get drag coefficient
            print("Drag Coefficient (B):")
            print("  - 0 = No air resistance (vacuum)")
            print("  - 0.1-0.5 = Light drag (soccer ball, basketball)")
            print("  - 0.5-2.0 = Moderate drag (golf ball, baseball)")
            print("  - 2.0+ = Heavy drag (badminton shuttlecock)")
            B = float(input("Enter B (0-5): "))
            if not (0 <= B <= 5):
                print("ERROR: B must be between 0 and 5")
                continue
            
            # Get initial velocity
            print("\nInitial Velocity (V):")
            print("  - Units: velocity/gravity (dimensionless)")
            print("  - 1 = moderate speed")
            print("  - 2-3 = fast throw")
            print("  - 5+ = very fast (professional)")
            V = float(input("Enter V (0.1-10): "))
            if not (0.1 <= V <= 10):
                print("ERROR: V must be between 0.1 and 10")
                continue
            
            # Get launch angle
            print("\nLaunch Angle:")
            print("  - 45° = traditional optimal (no air resistance)")
            print("  - 30-40° = typical with air resistance")
            angle = float(input("Enter angle in degrees (5-85): "))
            if not (5 <= angle <= 85):
                print("ERROR: Angle must be between 5 and 85 degrees")
                continue
            
            # Get simulation time
            print("\nSimulation Time:")
            print("  - Adjust based on velocity")
            print("  - Higher V needs more time")
            t_max = float(input("Enter max time (1-20): "))
            if not (1 <= t_max <= 20):
                print("ERROR: Time must be between 1 and 20")
                continue
            
            return B, V, angle, t_max
            
        except ValueError:
            print("\nERROR: Please enter valid numbers\n")

def simulate_trajectory(B, V, angle, t_max):
    """Simulate single trajectory."""
    angle_rad = angle * np.pi / 180
    sol = solve_ivp(dSdt, [0, t_max], 
                    y0=[0, V*np.cos(angle_rad), 0, V*np.sin(angle_rad)], 
                    t_eval=np.linspace(0, t_max, 1000), 
                    args=(B,))
    return sol

def get_distance(angle, B, V=1, t=2):
    """Calculate distance traveled before hitting ground."""
    v0x = V*np.cos(angle*np.pi/180)
    v0y = V*np.sin(angle*np.pi/180)
    sol = solve_ivp(dSdt, [0, t], 
                    y0=[0, v0x, 0, v0y], 
                    t_eval=np.linspace(0, t, 5000),  # Reduced from 10000
                    args=(B,), 
                    atol=1e-7, 
                    rtol=1e-4)
    
    # Find where projectile hits ground (y=0)
    crossings = np.where(np.diff(np.sign(sol.y[2])) < 0)[0]
    if len(crossings) == 0:
        return 0  # Didn't hit ground
    
    just_above_idx = crossings[0]
    just_below_idx = just_above_idx + 1
    x_loc = (sol.y[0][just_above_idx] + sol.y[0][just_below_idx]) / 2
    return x_loc

def plot_trajectory(sol, angle, B, V):
    """Plot single trajectory."""
    plt.figure(figsize=(10, 6))
    plt.plot(sol.y[0], sol.y[2], 'b-', linewidth=2)
    plt.ylim(bottom=0)
    plt.xlabel('Horizontal Distance (x/g)', fontsize=14)
    plt.ylabel('Height (y/g)', fontsize=14)
    plt.title(f'Trajectory: θ={angle}°, B={B}, V={V}', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.show()

def find_optimal_angle(B, V, t_max):
    """Find angle that gives maximum distance."""
    print("\nFinding optimal angle...")
    angles = np.linspace(20, 70, 100)  # Reduced from 200
    distances = np.vectorize(get_distance)(angles, B=B, V=V, t=t_max)
    
    optimal_idx = np.argmax(distances)
    optimal_angle = angles[optimal_idx]
    max_distance = distances[optimal_idx]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(angles, distances, 'b-', linewidth=2)
    plt.axvline(optimal_angle, ls='--', color='r', linewidth=2, 
                label=f'Optimal: {optimal_angle:.1f}°')
    plt.xlabel('Launch Angle (degrees)', fontsize=14)
    plt.ylabel('Maximum Distance (x/g)', fontsize=14)
    plt.title(f'Distance vs Angle (B={B}, V={V})', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return optimal_angle, max_distance

def main():
    """Main program with menu."""
    while True:
        print("\n" + "="*50)
        print("MENU:")
        print("1. Simulate single trajectory")
        print("2. Compare multiple angles")
        print("3. Find optimal angle")
        print("4. Quick demo (B=1, V=1, 45°)")
        print("5. Exit")
        print("="*50)
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '1':
            B, V, angle, t_max = get_user_input()
            sol = simulate_trajectory(B, V, angle, t_max)
            plot_trajectory(sol, angle, B, V)
            distance = get_distance(angle, B, V, t_max)
            print(f"\nDistance traveled: {distance:.3f} units")
        
        elif choice == '2':
            B, V, _, t_max = get_user_input()
            angles_str = input("Enter 3 angles separated by commas (e.g., 40,45,50): ")
            angles = [float(a.strip()) for a in angles_str.split(',')]
            
            plt.figure(figsize=(10, 6))
            for angle in angles:
                sol = simulate_trajectory(B, V, angle, t_max)
                plt.plot(sol.y[0], sol.y[2], linewidth=2, 
                        label=f'θ={angle}°')
            
            plt.ylim(bottom=0)
            plt.xlabel('Horizontal Distance (x/g)', fontsize=14)
            plt.ylabel('Height (y/g)', fontsize=14)
            plt.title(f'Trajectory Comparison (B={B}, V={V})', fontsize=16)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()
        
        elif choice == '3':
            B, V, _, t_max = get_user_input()
            optimal_angle, max_distance = find_optimal_angle(B, V, t_max)
            print(f"\nOptimal angle: {optimal_angle:.2f}°")
            print(f"Maximum distance: {max_distance:.3f} units")
        
        elif choice == '4':
            print("\nRunning demo with B=1, V=1, angle=45°...")
            sol = simulate_trajectory(1, 1, 45, 2)
            plot_trajectory(sol, 45, 1, 1)
        
        elif choice == '5':
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()