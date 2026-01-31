import subprocess
import sys
import os
from datetime import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print fancy banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║              🎓 PHYSICS SIMULATION SUITE 🎓                      ║
    ║                                                                  ║
    ║                   Advanced Physics Simulations                   ║
    ║                        Version 1.0                              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_simulation_details(sim_type):
    """Print detailed information about each simulation."""
    if sim_type == 1:
        print("\n" + "="*70)
        print("📊 PROJECTILE MOTION SIMULATOR")
        print("="*70)
        print("\n📖 Description:")
        print("   This simulation models the trajectory of projectiles under")
        print("   the influence of gravity and air resistance (drag).")
        print("\n✨ Features:")
        print("   • Simulate single or multiple trajectories")
        print("   • Compare different launch angles")
        print("   • Find optimal angle for maximum distance")
        print("   • Adjust drag coefficient (B) and initial velocity (V)")
        print("   • Real-world examples (golf ball, soccer ball)")
        print("\n🎯 Applications:")
        print("   • Sports physics (golf, soccer, basketball)")
        print("   • Ballistics and artillery")
        print("   • Understanding air resistance effects")
        print("\n⏱️  Estimated time: 2-5 minutes")
        print("="*70)
    
    elif sim_type == 2:
        print("\n" + "="*70)
        print("🔄 DOUBLE PENDULUM SIMULATOR")
        print("="*70)
        print("\n📖 Description:")
        print("   This simulation demonstrates the chaotic motion of a double")
        print("   pendulum system using Lagrangian mechanics.")
        print("\n✨ Features:")
        print("   • Visualize chaotic dynamics")
        print("   • Create animated GIF of pendulum motion")
        print("   • Customize masses, lengths, and initial conditions")
        print("   • See angle vs time plots")
        print("   • Observe sensitivity to initial conditions")
        print("\n🎯 Applications:")
        print("   • Chaos theory demonstration")
        print("   • Classical mechanics visualization")
        print("   • Understanding deterministic chaos")
        print("\n⏱️  Estimated time: 3-10 minutes (depending on animation length)")
        print("="*70)

def show_history():
    """Show simulation history (if log file exists)."""
    if os.path.exists('simulation_history.txt'):
        print("\n" + "="*70)
        print("📜 RECENT SIMULATION HISTORY")
        print("="*70)
        with open('simulation_history.txt', 'r') as f:
            lines = f.readlines()
            for line in lines[-5:]:  # Show last 5 entries
                print(f"   {line.strip()}")
        print("="*70)
    else:
        print("\n   No simulation history found.")

def log_simulation(sim_name):
    """Log simulation run to history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('simulation_history.txt', 'a') as f:
        f.write(f"{timestamp} - {sim_name}\n")

def print_menu():
    """Display the main menu."""
    clear_screen()
    print_banner()
    print("\n📚 Available Simulations:\n")
    print("  [1] 🚀 Projectile Motion Simulator")
    print("      └─ Air resistance, optimal angles, trajectory analysis")
    print()
    print("  [2] 🔄 Double Pendulum Simulator")
    print("      └─ Chaotic motion, Lagrangian mechanics, animation")
    print()
    print("  [3] ℹ️  View Simulation Details")
    print("      └─ Learn more about each simulation")
    print()
    print("  [4] 📜 View Simulation History")
    print("      └─ See your recent simulations")
    print()
    print("  [5] 🚪 Exit")
    print("\n" + "="*70)

def run_script(script_name, sim_name):
    """Run a Python script using subprocess."""
    clear_screen()
    
    # Check if file exists
    if not os.path.exists(script_name):
        print(f"\n❌ ERROR: {script_name} not found!")
        print(f"   Make sure {script_name} is in the same directory as main.py")
        input("\n Press Enter to return to main menu...")
        return
    
    print(f"\n🚀 Launching {sim_name}...\n")
    print("="*70 + "\n")
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_name], check=True)
        
        if result.returncode == 0:
            print("\n" + "="*70)
            print(f"✅ {sim_name} completed successfully!")
            print("="*70)
            log_simulation(sim_name)
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*70)
        print(f"❌ ERROR: Simulation failed with exit code {e.returncode}")
        print("="*70)
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    input("\nPress Enter to return to main menu...")

def view_details():
    """Show details menu."""
    while True:
        clear_screen()
        print("\n" + "="*70)
        print("ℹ️  SIMULATION DETAILS")
        print("="*70)
        print("\n[1] Projectile Motion Simulator")
        print("[2] Double Pendulum Simulator")
        print("[3] Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            print_simulation_details(1)
            input("\nPress Enter to continue...")
        elif choice == '2':
            print_simulation_details(2)
            input("\nPress Enter to continue...")
        elif choice == '3':
            break
        else:
            print("\n❌ Invalid choice!")
            input("Press Enter to continue...")

def main():
    """Main menu loop."""
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            run_script('pro.py', 'Projectile Motion Simulator')
        
        elif choice == '2':
            run_script('sim.py', 'Double Pendulum Simulator')
        
        elif choice == '3':
            view_details()
        
        elif choice == '4':
            show_history()
            input("\nPress Enter to return to main menu...")
        
        elif choice == '5':
            clear_screen()
            print("\n" + "="*70)
            print("\n   👋 Thank you for using Physics Simulation Suite!")
            print("   📧 Feedback: physics@simulator.com")
            print("   🌐 Visit: www.physicssimulator.com")
            print("\n   Goodbye!\n")
            print("="*70 + "\n")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please enter 1-5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n⚠️  Program interrupted by user")
        print("   Goodbye!\n")
        sys.exit(0)