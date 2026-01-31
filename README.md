# Physics Motion Simulator

An interactive educational web application for simulating and analyzing projectile motion and double pendulum dynamics with comprehensive visualizations and real-time analysis.

## Features

### Projectile Motion Simulation
- **Comprehensive physics engine** with air resistance (drag coefficient B)
- **Real-time trajectory animation** with velocity vectors
- **Analysis panels** including:
  - Velocity components over time
  - Height vs time graphs
  - Energy analysis (kinetic, potential, total)
  - Optimal angle finder
  - Air resistance comparison
- **Preset scenarios**: Basketball, Golf, Soccer, Cannonball, Vacuum
- **Comparison mode**: Compare up to 3 trajectories simultaneously
- **Export functionality**: Download data as CSV

### Double Pendulum Simulation
- **Lagrangian mechanics** implementation with Runge-Kutta integration
- **Real-time pendulum animation** on black canvas with motion trails
- **Chaos demonstration**: Compare trajectories with tiny differences in initial conditions
- **Comprehensive analysis**:
  - Angle and angular velocity graphs
  - Phase space diagrams showing chaotic attractors
  - Energy conservation verification
  - FFT frequency analysis
  - Position heatmap
  - Lyapunov exponent calculation
- **Path trace visualization**: Full trajectory of second bob with time-gradient coloring
- **Preset scenarios**: Gentle Swing, Chaotic Motion, Near Flip, etc.

## Technology Stack

- **Backend**: Python with Flask
- **Physics**: SciPy (numerical integration), NumPy (computations)
- **Visualization**: Matplotlib (graphs converted to base64 images)
- **Frontend**: HTML5 Canvas, Vanilla JavaScript, Modern CSS
- **Design**: Educational theme with premium aesthetics

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Step 1: Install pip (if not installed)
```bash
sudo apt update
sudo apt install python3-pip
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install system packages (Ubuntu/Debian):
```bash
sudo apt install python3-flask python3-flask-cors python3-scipy python3-numpy python3-matplotlib python3-pil
```

### Step 3: Run the Application
```bash
python3 app.py
```

The server will start at `http://localhost:5000`

## Usage

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Choose a simulation** using the top tabs (Projectile Motion or Double Pendulum)
3. **Adjust parameters** using the left control panel
4. **Click "Simulate"** to run the physics calculations
5. **View results** in the main canvas and analysis panels
6. **Play/Pause/Restart** animations using playback controls
7. **Export data** as CSV files for further analysis

## Project Structure

```
Project/
├── app.py                      # Flask server with API endpoints
├── requirements.txt            # Python dependencies
├── physics/
│   ├── projectile.py          # Projectile motion physics engine
│   └── double_pendulum.py     # Double pendulum physics engine
├── visualizations/
│   └── graphs.py              # Matplotlib graph generation
├── index.html                  # Main HTML structure
├── styles/
│   └── main.css               # Design system and styles
└── scripts/
    ├── utils.js               # Utility functions
    ├── projectile.js          # Projectile frontend logic
    └── pendulum.js            # Pendulum frontend logic
```

## API Endpoints

### Projectile Motion
- `POST /api/projectile/simulate` - Calculate trajectory
- `POST /api/projectile/analyze` - Generate all analysis graphs
- `POST /api/projectile/optimal_angle` - Find optimal launch angle
- `POST /api/projectile/compare` - Compare multiple trajectories

### Double Pendulum
- `POST /api/pendulum/simulate` - Calculate pendulum motion
- `POST /api/pendulum/analyze` - Generate all analysis graphs
- `POST /api/pendulum/chaos` - Demonstrate chaos with similar initial conditions

### Presets
- `GET /api/presets/projectile` - Get projectile presets
- `GET /api/presets/pendulum` - Get pendulum presets

## Educational Content

The simulator includes built-in educational sections explaining:
- Physics principles and equations
- Real-world applications
- Lagrangian mechanics
- Chaotic dynamics and the butterfly effect
- Lyapunov exponents

## Performance Notes

- **Projectile calculations**: < 0.5 seconds
- **Pendulum calculations**: 2-5 seconds for high-quality simulations (200 fps, 100s)
- **Animations**: Target 60 fps for smooth playback
- **Energy conservation**: < 0.1% error for double pendulum

## Tips for Best Experience

1. Start with **preset scenarios** to understand the simulations
2. Use **comparison mode** for projectile motion to see effects of different parameters
3. Try the **chaos demonstration** for double pendulum to see exponential divergence
4. **Adjust playback speed** to slow down fast animations
5. **Export data** to analyze in spreadsheet software or plotting tools

## Troubleshooting

**If graphs don't appear:**
- Check browser console for errors
- Ensure backend server is running
- Wait for calculations to complete (loading indicator shown)

**If animations are choppy:**
- Reduce FPS quality for pendulum
- Lower playback speed
- Close other browser tabs

**If simulations take too long:**
- Reduce simulation duration
- Lower FPS for pendulum
- Use lower quality setting

## Future Enhancements

- Interactive graphs with Plotly.js (instead of static matplotlib images)
- 3D visualization for double pendulum
- More preset scenarios
- Comparison history to save previous runs
- Dark mode toggle
- Multi-language support

## License

Educational use - Feel free to use and modify for learning purposes.

## Credits

Built using:
- SciPy for numerical integration
- Matplotlib for graph generation
- Flask for web framework
- Modern web standards (HTML5, CSS3, ES6+)

---

**Enjoy exploring physics!** 🚀⚙️