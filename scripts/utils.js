/**
 * Utility Functions
 * Shared helper functions for the physics simulator
 */

// Debounce function to limit API calls
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Format numbers with specified decimals
function formatNumber(value, decimals = 2) {
    return parseFloat(value).toFixed(decimals);
}

// Format physics values with units
function formatPhysicsValue(value, unit) {
    return `${formatNumber(value)} ${unit}`;
}

// Show loading indicator
function showLoadingIndicator(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'flex';
    }
}

// Hide loading indicator
function hideLoadingIndicator(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.textContent = message;
    notification.className = 'notification';
    notification.classList.add('show', type);

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Download file
function downloadFile(data, filename, type) {
    const blob = new Blob([data], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Download base64 image
function downloadBase64Image(base64Data, filename) {
    const link = document.createElement('a');
    link.href = base64Data;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Sync slider and input
function syncSliderInput(sliderId, inputId, callback) {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);

    if (!slider || !input) return;

    slider.addEventListener('input', () => {
        input.value = slider.value;
        if (callback) callback(parseFloat(slider.value));
    });

    input.addEventListener('input', () => {
        slider.value = input.value;
        if (callback) callback(parseFloat(input.value));
    });
}

// API request helper
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'API request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// Create statistics display
function createStatsDisplay(stats) {
    const statsGrid = document.createElement('div');
    statsGrid.className = 'stats-grid';

    for (const [key, value] of Object.entries(stats)) {
        const statCard = document.createElement('div');
        statCard.className = 'stat-card';

        const label = document.createElement('div');
        label.className = 'stat-label';
        label.textContent = key;

        const valueEl = document.createElement('div');
        valueEl.className = 'stat-value';
        valueEl.textContent = value;

        statCard.appendChild(label);
        statCard.appendChild(valueEl);
        statsGrid.appendChild(statCard);
    }

    return statsGrid;
}

// Setup analysis tabs
function setupAnalysisTabs(tabsSelector, viewsSelector) {
    const tabs = document.querySelectorAll(tabsSelector);
    const views = document.querySelectorAll(viewsSelector);

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetAnalysis = tab.dataset.analysis;

            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active view
            views.forEach(view => {
                if (view.id.includes(targetAnalysis)) {
                    view.classList.add('active');
                } else {
                    view.classList.remove('active');
                }
            });
        });
    });
}

// ==================== INFO POPUP SYSTEM ====================

const TERM_DEFINITIONS = {

    // ---- Pendulum terms ----
    pend_params: {
        title: '📐 Pendulum Parameters',
        bullets: [
            'Parameters define the physical properties of the double pendulum system.',
            'The system has two linked arms, each with its own mass, length, angle, and angular velocity.',
            'Tiny changes in any parameter can cause dramatically different long-term behaviour — this is the hallmark of a chaotic system.',
            'All parameters feed into the Lagrangian equations of motion, which are solved numerically.'
        ],
        applications: [
            '🔬 Physics research: studying chaotic dynamics and sensitivity to initial conditions.',
            '🤖 Robotics: double-pendulum models underlie the control of multi-joint robotic arms.',
            '🎡 Mechanical engineering: suspension bridges and cranes exhibit similar coupled oscillations.'
        ]
    },
    mass1: {
        title: '⚖️ Mass 1 (m₁)',
        bullets: [
            'The mass of the <strong>first (upper) bob</strong>, in kilograms.',
            'Heavier m₁ increases the inertia of the upper arm, slowing its angular accelerations.',
            'The ratio m₁/m₂ significantly affects how energy is transferred between the two arms.',
            'Equal masses (m₁ = m₂) produce a symmetric system that still exhibits chaos.'
        ],
        applications: [
            '🤖 Robotics: upper arm mass in bipedal walking robots affects gait stability.',
            '🌉 Civil engineering: modelling the mass distribution in suspension cable systems.',
            '🎠 Amusement parks: coupled pendulum rides are tuned by adjusting bob masses.'
        ]
    },
    length1: {
        title: '📏 Length 1 (L₁)',
        bullets: [
            'The length of the <strong>first arm</strong>, measured from the fixed pivot to the first bob, in metres.',
            'Natural frequency of the upper pendulum scales as <em>ω ∝ √(g/L₁)</em>.',
            'Longer arms swing more slowly; shorter arms swing faster for the same initial angle.',
            'L₁ and L₂ together determine the spatial reach of the full system.'
        ],
        applications: [
            '🏗️ Crane dynamics: the boom length corresponds to L₁ in pendulum models.',
            '🕰️ Clock design: pendulum clock regulators tune L to achieve precise 1-second periods.',
            '🎡 Theme park rides: arm length determines the height and speed of swing rides.'
        ]
    },
    theta1: {
        title: '📐 Initial Angle (θ₁)',
        bullets: [
            'The starting angle of the <strong>first arm</strong> from the vertical, in degrees.',
            'θ₁ = 0° means the arm hangs straight down (stable equilibrium).',
            'θ₁ = 180° means the arm points straight up (unstable equilibrium — highly chaotic).',
            'Even a 0.01° difference in θ₁ can lead to completely different long-term trajectories due to chaos sensitivity.'
        ],
        applications: [
            '🔬 Chaos theory: sensitivity to initial conditions (butterfly effect) is studied using tiny θ changes.',
            '🎢 Roller coasters: initial drop angle determines the speed and energy of the ride.',
            '🌊 Tidal modelling: ocean pendulum analogues use initial tilt to model tidal forcing.'
        ]
    },
    omega1: {
        title: '🔄 Angular Velocity (ω₁)',
        bullets: [
            'The initial rotational speed of the <strong>first arm</strong>, in radians per second.',
            'Positive ω₁ means the arm is spinning counter-clockwise at the start; negative means clockwise.',
            'A non-zero ω₁ adds kinetic energy to the system at t = 0.',
            'Combined with θ₁, it fully defines the initial state of the upper arm.'
        ],
        applications: [
            '🤸 Gymnastics: angular velocity of a gymnast\'s arm during a routine follows similar equations.',
            '🌀 Gyroscopes: angular velocity is the key operating parameter.',
            '🪁 Throwing sports: initial angular velocity of a discus or hammer determines trajectory.'
        ]
    },
    mass2: {
        title: '⚖️ Mass 2 (m₂)',
        bullets: [
            'The mass of the <strong>second (lower) bob</strong>, in kilograms.',
            'A heavier m₂ increases the effective load on the first arm, affecting the full system dynamics.',
            'When m₂ >> m₁, the second arm barely moves relative to the first.',
            'When m₂ << m₁, the second arm flails wildly — maximum chaotic behaviour.'
        ],
        applications: [
            '🤖 Prosthetics: the mass at the end of a prosthetic limb is tuned for natural swinging.',
            '🎣 Fishing rods: the lure at the end acts as m₂ in a two-segment rod model.',
            '🏋️ Weight training: barbells on the end of arms model double-pendulum dynamics in lifts.'
        ]
    },
    length2: {
        title: '📏 Length 2 (L₂)',
        bullets: [
            'The length of the <strong>second arm</strong>, from the first bob to the second bob, in metres.',
            'A longer L₂ creates a wider swing arc and richer chaotic patterns.',
            'When L₂ >> L₁, the system becomes more like a whip with a small handle.',
            'The ratio L₁/L₂ strongly influences whether the second arm can complete full rotations.'
        ],
        applications: [
            '🤸 Acrobatics: the lower leg in a human swing corresponds to L₂ in a pendulum.',
            '🌉 Bridge cables: secondary cable lengths in suspension bridges model L₂.',
            '🎸 Guitar strings: vibrating string segments are modelled as linked pendulums.'
        ]
    },
    theta2: {
        title: '📐 Initial Angle (θ₂)',
        bullets: [
            'The starting angle of the <strong>second arm</strong> from the vertical, in degrees.',
            'Setting θ₂ ≠ θ₁ introduces asymmetry that quickly amplifies into chaotic divergence.',
            'θ₂ = θ₁ is the symmetric start — the system is still chaotic but takes longer to diverge.',
            'Extreme angles (± 180°) near the inverted position produce the most dramatic motion.'
        ],
        applications: [
            '🔬 Chaos experiments: physicists test θ₂ sensitivity in lab pendulum apparatus.',
            '🤸 Ballet: the angle of a dancer\'s lower leg during a pirouette follows θ₂ dynamics.',
            '🚂 Train bogies: wheel angle in a coupled bogie system mirrors θ₂ in a pendulum.'
        ]
    },
    omega2: {
        title: '🔄 Angular Velocity (ω₂)',
        bullets: [
            'The initial rotational speed of the <strong>second arm</strong>, in radians per second.',
            'A large ω₂ at t = 0 gives the lower arm enough energy to complete full revolutions.',
            'ω₂ is the primary driver of whether the second bob will spin or oscillate.',
            'Together with θ₂, it fully defines the initial state of the lower arm.'
        ],
        applications: [
            '🌀 Centrifuges: high angular velocity is the working principle of lab centrifuges.',
            '🤸 Gymnastics: release angular velocity in bar routines determines aerial somersaults.',
            '🛸 Satellite attitude control: angular velocities of coupled rigid bodies are modelled this way.'
        ]
    },
    p_duration: {
        title: '⏱️ Simulation Duration',
        bullets: [
            'The total time span for which the double pendulum motion is computed, in seconds.',
            'Longer durations produce more complex trace patterns but require more computation.',
            'At around 20–30s, chaotic behaviour becomes visible even for regular-looking initial conditions.',
            'For near-unstable initial conditions (θ close to 180°), 5–10s may already show full chaos.'
        ],
        applications: [
            '🔬 Research: multi-hour simulations of coupled oscillators are used in climate modelling.',
            '🎮 Games: physics engines run short-duration pendulum simulations each frame (~16ms).',
            '🚀 Space missions: trajectory simulations span hours or days for orbit calculations.'
        ]
    },
    fps: {
        title: '🎬 Quality (FPS)',
        bullets: [
            'Sets the number of frames per second computed for the animation.',
            'Higher FPS = smoother animation but slower computation on the server.',
            '<strong>50 FPS:</strong> good for quick exploration. <strong>100 FPS:</strong> balanced. <strong>200 FPS:</strong> silky-smooth for export.',
            'FPS does not affect the physical accuracy of the simulation — only the visual resolution of the animation.'
        ],
        applications: [
            '🎬 Cinema: 24 FPS for film, 60 FPS for sports broadcasts, 120+ FPS for VR.',
            '🎮 Video games: physics engines target 60–120 FPS for smooth gameplay feel.',
            '🔬 High-speed cameras: up to 1,000,000 FPS used to study explosions and impacts.'
        ]
    },
    p_presets: {
        title: '🎮 Preset Scenarios',
        bullets: [
            'Presets are pre-configured double pendulum setups that fill all parameters at once.',
            'Each preset is designed to demonstrate a specific physical behaviour.',
            'Examples: Equal Arms (balanced chaos), Heavy Bottom (slow lower arm), Near Unstable (maximum chaos).',
            'Use presets as starting points and then adjust individual parameters to explore variations.'
        ],
        applications: [
            '⚖️ Equal masses: symmetric chaos useful for textbook demonstrations.',
            '🌪️ Near-inverted: θ₁ ≈ 179° triggers rapid onset of chaos — used to study Lyapunov exponents.',
            '🏋️ Heavy bottom: large m₂ models a wrecking ball hanging from a crane arm.'
        ]
    },
    pend_anim: {
        title: '🎥 Pendulum Animation',
        bullets: [
            'The animation canvas shows the live motion of both pendulum arms and bobs.',
            'The gold trail is the path traced by the second (lower) bob over recent frames.',
            'The white lines are the two rigid arms; the red and blue circles are the bobs.',
            'The pivot point at the top is the fixed point from which the whole system hangs.',
            'All motion is governed by Lagrangian mechanics solved numerically with scipy.'
        ],
        applications: [
            '🎓 Education: visually demonstrates sensitivity to initial conditions (chaos).',
            '🤖 Robotics: visualising multi-joint arm trajectories for path planning.',
            '🎨 Art: the chaotic trace pattern is used as a generative art tool.'
        ]
    },
    // ---- Pendulum stat terms ----
    pend_max_theta: {
        title: '📐 Max θ (Angle)',
        bullets: [
            'The maximum angular displacement reached by each arm during the simulation.',
            'Max θ₁ and Max θ₂ indicate how far each arm swings from its equilibrium (vertical) position.',
            'Values near ±180° mean the arm nearly or fully inverted — indicating high-energy, chaotic motion.',
            'In a simple (non-chaotic) pendulum, max θ stays near the initial angle.'
        ],
        applications: [
            '🤸 Athletics: max joint angle in a gymnast\'s swing determines vault height.',
            '🕰️ Grandfather clocks: max θ is precisely controlled to maintain accurate timekeeping.',
            '🔬 Pendulum experiments: max θ is used to calculate the initial potential energy.'
        ]
    },
    pend_max_omega: {
        title: '🔄 Max ω (Angular Velocity)',
        bullets: [
            'The maximum angular speed reached by each arm, in radians per second.',
            'Peak ω occurs at the lowest point of the swing (for simple pendulums), or unpredictably for chaotic ones.',
            'Max ω₁ and Max ω₂ quantify how violently the arms are rotating at their fastest.',
            'High max ω often indicates the arm completed full rotations around the pivot.'
        ],
        applications: [
            '🌀 Centrifuges: maximum angular velocity determines the separation force.',
            '🤸 Gymnastics: peak angular velocity in a release move determines flight height.',
            '⚡ Generators: rotational speed (ω) directly determines electrical power output.'
        ]
    },
    pend_rotations: {
        title: '🔁 Rotations',
        bullets: [
            'The number of complete 360° revolutions made by each arm during the simulation.',
            'Rotation 1 and Rotation 2 count full spins of the first and second arms respectively.',
            'Rotations ≥ 1 indicate the arm had enough energy to continuously spin — a highly chaotic state.',
            'A simple pendulum that just oscillates will have Rotations = 0.'
        ],
        applications: [
            '🌀 Electric motors: rotations per second (RPS) defines operating speed.',
            '🎡 Mechanical devices: gear rotation counts are computed similarly.',
            '🔬 Chaos experiments: counting rotations is a quick indicator of chaotic vs. regular motion.'
        ]
    },
    pend_energy_error: {
        title: '⚡ Energy Error (%)',
        bullets: [
            'The percentage drift in total mechanical energy over the course of the simulation.',
            'In an ideal frictionless double pendulum, total energy (KE + PE) should be perfectly conserved.',
            'A small energy error (< 0.1%) means the numerical solver is accurate.',
            'A large energy error indicates the simulation step size is too coarse — try increasing FPS.',
            'This is a built-in quality check for numerical integration accuracy.'
        ],
        applications: [
            '💻 Scientific computing: energy conservation is the primary validation metric for ODE solvers.',
            '🚀 Orbital mechanics: energy drift in simulations leads to incorrect orbit predictions.',
            '⚙️ Engineering: energy error budgets are used to validate FEA (finite element analysis) models.'
        ]
    },
    // ---- Pendulum chart terms ----
    pchart_angles: {
        title: '📊 Angles vs Time Chart',
        bullets: [
            'Plots <strong>θ₁ (upper arm angle)</strong> and <strong>θ₂ (lower arm angle)</strong> over time.',
            'In regular oscillation, both curves are smooth, periodic sinusoids.',
            'In chaotic motion, the curves become irregular and unpredictable after a short time.',
            'The divergence between the two curves shows how independently each arm moves.'
        ],
        applications: [
            '🔬 Chaos research: angle-time plots are used to identify the onset of chaotic motion.',
            '🤖 Robotics: joint angle profiles are tracked for robot arm control feedback.',
            '🎓 Physics education: comparing θ₁ vs θ₂ curves illustrates coupled oscillation.'
        ]
    },
    pchart_velocity: {
        title: '📊 Angular Velocity Chart',
        bullets: [
            'Shows <strong>ω₁</strong> and <strong>ω₂</strong> (angular velocities) for both arms over time.',
            'Smooth oscillating curves indicate regular (non-chaotic) motion.',
            'Spiky, irregular curves indicate highly chaotic behaviour with sudden direction reversals.',
            'The moments where ω = 0 correspond to the extremes of each arm\'s swing.'
        ],
        applications: [
            '⚙️ Machinery: angular velocity monitoring detects vibrations and bearing faults.',
            '🤸 Sports science: angular velocity profiles of limbs are analysed for technique optimisation.',
            '🌀 Turbine control: ω is the key control variable in power generation systems.'
        ]
    },
    pchart_phase: {
        title: '🌀 Phase Space Chart',
        bullets: [
            'Plots <strong>angle (θ) vs angular velocity (ω)</strong> for each arm — instead of vs. time.',
            'For a simple pendulum, this produces a smooth ellipse (regular orbit).',
            'For a chaotic pendulum, the phase space fills up with tangled, non-repeating curves.',
            'This is the most powerful tool for diagnosing chaos vs. regularity in the system.',
            'A closed loop = periodic motion; a filled region = chaotic motion.'
        ],
        applications: [
            '🔬 Nonlinear dynamics: phase space is the standard tool for studying chaos and attractors.',
            '📡 Signal processing: phase plots diagnose noise and stability in oscillating systems.',
            '🧬 Biology: heartbeat rhythms are analysed in phase space to detect arrhythmias.'
        ]
    },
    pchart_energy: {
        title: '⚡ Energy Chart',
        bullets: [
            'Shows <strong>kinetic energy (KE)</strong>, <strong>potential energy (PE)</strong>, and <strong>total energy</strong> over time.',
            'In a perfect frictionless system, KE + PE = constant (total energy is conserved).',
            'Any drift in the total energy line indicates numerical integration error.',
            'Rapid energy exchanges between KE and PE coincide with the chaotic swinging motions.'
        ],
        applications: [
            '⚙️ Mechanical systems: energy exchange analysis informs damping and spring design.',
            '🔋 Energy harvesting: coupling pendulums to generators extracts energy from their oscillation.',
            '🎓 Physics: demonstrates the equivalence of kinetic and potential energy in real time.'
        ]
    },
    pchart_fft: {
        title: '📡 FFT / Frequency Spectrum',
        bullets: [
            'Shows the <strong>frequency content</strong> of the pendulum motion using Fast Fourier Transform.',
            'For a regular pendulum, a sharp peak appears at the natural frequency.',
            'For a chaotic pendulum, the spectrum is broad and continuous — no single dominant frequency.',
            'The natural frequency of the first arm ≈ <em>√(g/L₁) / (2π)</em> Hz.',
            'Identifying frequency peaks helps distinguish regular from chaotic regimes.'
        ],
        applications: [
            '🎵 Audio engineering: FFT is the foundation of equalizers and audio spectrum analysers.',
            '📡 Telecommunications: frequency spectrum analysis underlies all wireless communication.',
            '🔬 Medical imaging: MRI machines use Fourier transforms to reconstruct images from signals.'
        ]
    },
    pchart_heatmap: {
        title: '🌡️ Position Heatmap',
        bullets: [
            'Shows the <strong>density of positions</strong> visited by the second bob over the full simulation.',
            'Hot colours (red/yellow) indicate regions the bob spends the most time in.',
            'Cool colours (blue) show regions rarely visited.',
            'For regular motion, the heatmap shows clean arcs. For chaotic motion, it fills a broad, complex region.',
            'The heatmap reveals the long-term "attractor" geometry of the chaotic system.'
        ],
        applications: [
            '🗺️ Urban planning: pedestrian heatmaps use the same density-visualisation principle.',
            '🎮 Game analytics: player position heatmaps guide level design decisions.',
            '🔬 Particle physics: hit-density heatmaps are used to analyse detector data in accelerators.'
        ]
    },

    // ---- Projectile terms ----
    parameters: {
        title: '📐 Parameters',

        bullets: [
            'A <strong>parameter</strong> is any adjustable input that controls how the simulation behaves.',
            'Changing parameters lets you model different real-world scenarios without rewriting equations.',
            'This simulator has four key parameters: drag coefficient, initial velocity, launch angle, and simulation time.',
            'Small changes in parameters can lead to dramatically different trajectories — especially when air resistance is involved.'
        ],
        applications: [
            '🏀 Sports science: tuning parameters to model basketball or soccer ball flights.',
            '🎯 Military ballistics: calculating optimal shell parameters for maximum range.',
            '🚀 Space engineering: setting rocket launch parameters for orbital insertion.'
        ]
    },
    drag_coeff: {
        title: '💨 Drag Coefficient (B)',
        bullets: [
            'The drag coefficient <strong>B</strong> measures how strongly air resistance opposes the motion of the projectile.',
            'Drag force is calculated as: <em>F_drag = −B × v × |v|</em>, where v is velocity.',
            'A value of <strong>0</strong> means no air resistance (perfect vacuum) — the projectile follows an ideal parabola.',
            'Higher B values (e.g. 2.5 for a shuttlecock) cause significant trajectory shortening.',
            'The optimal launch angle shifts below 45° as B increases.'
        ],
        applications: [
            '⚽ Soccer balls have B ≈ 0.3; golf balls ≈ 1.0 due to dimples reducing effective drag.',
            '🪂 Parachute design relies on high drag coefficients to slow descent safely.',
            '🌬️ Atmospheric particles behave according to their individual drag coefficients.'
        ]
    },
    init_velocity: {
        title: '🚀 Initial Velocity (v₀)',
        bullets: [
            'The <strong>initial velocity</strong> is the launch speed of the projectile, measured in m/s.',
            'It determines the total energy available to the projectile at launch.',
            'Higher v₀ increases both the maximum height and horizontal range.',
            'Components: <em>v₀ₓ = v₀ cos(θ)</em> (horizontal) and <em>v₀ᵧ = v₀ sin(θ)</em> (vertical).',
            'With drag, increasing v₀ also increases air resistance forces proportionally.'
        ],
        applications: [
            '🏹 Archery: arrow velocity directly determines how far and flat it flies.',
            '🏌️ Golf: a driver launches a ball at ~70 m/s, giving 200–250 m of carry.',
            '🚀 Minimum orbital velocity for Earth is ~7,900 m/s (Mach 23).'
        ]
    },
    launch_angle: {
        title: '📐 Launch Angle (θ)',
        bullets: [
            'The angle above the horizontal at which the projectile is fired, in degrees.',
            'In a vacuum, <strong>45°</strong> gives the maximum range for any given initial velocity.',
            'With air resistance, the optimal angle decreases — typically to 30°–40°.',
            'At 90°, the projectile goes straight up — zero range, maximum height.',
            'At very low angles (< 15°), the projectile skims with short flight time.'
        ],
        applications: [
            '⚾ Baseball: pitchers and batters intuitively adjust angle for different plays.',
            '💣 Artillery: historical cannons used 45° for maximum field range.',
            '🎆 Fireworks: shells launched at precise angles to burst at correct altitudes.'
        ]
    },
    sim_time: {
        title: '⏱️ Max Simulation Time',
        bullets: [
            'Sets the <strong>maximum duration</strong> (seconds) over which the simulation is computed.',
            'If the projectile lands before this time, the simulation ends at impact.',
            'Increase this for high-velocity or low-drag scenarios to capture the full path.',
            'Too high wastes computation; too low cuts off the trajectory prematurely.',
            'Internally solved using numerical integration (scipy solve_ivp) over this span.'
        ],
        applications: [
            '🎾 Tennis serve: crosses the net in < 1 second — short sim time needed.',
            '💫 Long-range artillery: shells airborne for 60–90 seconds — high sim time needed.',
            '🌋 Volcanic lava bombs can travel for hundreds of seconds depending on eruption speed.'
        ]
    },
    presets: {
        title: '🎮 Preset Scenarios',
        bullets: [
            '<strong>Presets</strong> are pre-configured real-world examples that auto-fill all parameters.',
            'Each preset models a specific object with realistic drag, velocity, angle, and time.',
            'Available: Basketball Free Throw, Golf Drive, Soccer Kick, Cannonball, Vacuum.',
            'Load a preset then fine-tune individual parameters to explore variations.'
        ],
        applications: [
            '🏀 Basketball: v₀=7.5 m/s, angle=52°, B=0.15 — models a free throw arc.',
            '⛳ Golf: v₀=70 m/s, angle=12°, B=0.25 — models a driver shot.',
            '⚽ Soccer: v₀=25 m/s, angle=30°, B=0.30 — models a powerful kick.'
        ]
    },
    traj_viz: {
        title: '📺 Trajectory Visualization',
        bullets: [
            'The animated canvas showing the projectile\'s complete path in real time.',
            'The blue arc shows the full trajectory from launch to landing.',
            'The red dot is the projectile, animated along the path at configurable speed.',
            'The green arrow shows the current velocity vector — direction and magnitude update each frame.',
            'A grid and ground line provide spatial reference for scale.'
        ],
        applications: [
            '🎓 Education: visually see the effect of changing launch angle or drag.',
            '🏋️ Biomechanics: coaches analyse athlete throwing patterns using trajectory visuals.',
            '🛸 Mission control: spacecraft trajectory visualisation is used during critical manoeuvres.'
        ]
    },
    max_height: {
        title: '⬆️ Max Height',
        bullets: [
            'The peak vertical position reached by the projectile, in metres.',
            'Occurs when the vertical velocity component (vᵧ) equals zero.',
            'Vacuum formula: <em>H = (v₀ sin θ)² / (2g)</em>.',
            'With drag, the peak is lower and reached earlier than the vacuum prediction.',
            'Depends primarily on the vertical component of initial velocity (v₀ sin θ).'
        ],
        applications: [
            '🏈 Coaches track punt apex height to optimise hang time.',
            '🎆 Fireworks burst altitude is controlled by initial velocity and mortar angle.',
            '🛩️ Projectile max height calculations define safe airspace exclusion zones.'
        ]
    },
    time_to_max: {
        title: '⏳ Time to Max Height',
        bullets: [
            'The duration from launch until the projectile reaches its highest point.',
            'In a vacuum, this equals exactly half the total flight time (symmetric parabola).',
            'With air resistance, ascent takes longer relative to the descent — symmetry is broken.',
            'Vacuum formula: <em>t_peak = v₀ sin(θ) / g</em>.',
            'Helps understand the shape and asymmetry introduced by drag.'
        ],
        applications: [
            '🏀 Basketball: knowing hang time helps defenders time their jumps.',
            '🎯 Skeet shooting: shooters predict where the clay pigeon peaks.',
            '🚀 Missile defence: time-to-apex is critical for interception timing.'
        ]
    },
    flight_time: {
        title: '✈️ Total Flight Time',
        bullets: [
            'The complete duration the projectile spends in the air, from launch to landing.',
            'Ends when the projectile returns to ground level (y = 0).',
            'In a vacuum, it is exactly twice the time to max height.',
            'Air resistance shortens total flight time by reducing range and height.',
            'Longer flight times give wind and drag more opportunity to deflect the projectile.'
        ],
        applications: [
            '🏈 Punters maximise hang time so the coverage team can reach the returner.',
            '🧨 Shell flight time determines how early to fire to intercept a moving target.',
            '🌂 Skydiving freefall time calculations use air resistance models like this one.'
        ]
    },
    range: {
        title: '📏 Horizontal Range',
        bullets: [
            'The total horizontal distance the projectile travels before landing, in metres.',
            'Vacuum formula: <em>R = v₀² sin(2θ) / g</em> — maximised at exactly 45°.',
            'With air resistance, maximum range occurs at a launch angle below 45°.',
            'Increasing v₀ increases range quadratically in a vacuum.',
            'Use "Find Optimal Angle" to calculate the exact range-maximising angle.'
        ],
        applications: [
            '🏌️ Golf: driving distance is the primary metric professionals optimise.',
            '🪖 Artillery range tables list horizontal distance for each shell type and charge.',
            '🚜 Irrigation sprinklers use range calculations to design field coverage patterns.'
        ]
    },
    impact_speed: {
        title: '💥 Impact Speed',
        bullets: [
            'The total speed of the projectile at the moment it hits the ground, in m/s.',
            'Computed as: <em>|v| = √(vₓ² + vᵧ²)</em> at the landing point.',
            'In a vacuum, impact speed equals the launch speed (energy conservation).',
            'With drag, impact speed is always less than the initial velocity.',
            'Determines the kinetic energy carried to the target on impact.'
        ],
        applications: [
            '🪖 Bullet impact speed determines armour penetration capability.',
            '🏐 Volleyball spike speed affects how hard the ball is to receive.',
            '🚗 Vehicle impact speed is the primary factor in accident reconstruction.'
        ]
    },
    impact_angle: {
        title: '📉 Impact Angle',
        bullets: [
            'The angle below the horizontal at which the projectile strikes the ground.',
            'In a vacuum, the impact angle equals the launch angle (perfect symmetry).',
            'With drag, the impact angle becomes steeper — the projectile falls more vertically.',
            'A steeper impact angle concentrates more energy downward on landing.',
            'Critical for understanding penetration depth and damage patterns.'
        ],
        applications: [
            '🏹 Arrow impact angle affects how deeply it penetrates the target.',
            '🪖 Shells designed to penetrate fortifications need near-vertical impact angles.',
            '⚽ Goal-bound shots with steep angles are harder for goalkeepers to save.'
        ]
    },
    energy_lost: {
        title: '⚡ Energy Lost (%)',
        bullets: [
            'The percentage of initial kinetic energy dissipated by air resistance during flight.',
            'Formula: <em>(KE_initial − KE_impact) / KE_initial × 100%</em>.',
            'With B = 0 (vacuum), energy lost is 0% — kinetic energy is fully conserved.',
            'Higher drag and longer paths result in more energy being lost.',
            'Lost energy is converted to heat through fluid friction in the surrounding air.'
        ],
        applications: [
            '🚀 Re-entry vehicles lose enormous energy to drag — managed as heat shields.',
            '🏸 Shuttlecocks lose ~80% of energy in flight due to their extreme drag.',
            '🌬️ Wind turbine blade design studies energy loss to optimise efficiency.'
        ]
    },
    chart_velocity: {
        title: '📊 Velocity Components Chart',
        bullets: [
            'Plots <strong>horizontal velocity (vₓ)</strong> and <strong>vertical velocity (vᵧ)</strong> over time.',
            'In a vacuum: vₓ stays constant; vᵧ decreases linearly due to gravity.',
            'With drag: vₓ also decreases as air resistance opposes horizontal motion.',
            'The crossover point (vᵧ = 0) is the moment of maximum height.',
            'vᵧ becomes negative after the peak — the projectile is descending.'
        ],
        applications: [
            '🏋️ Biomechanics: analysing how a javelin\'s velocity components change in flight.',
            '🎮 Game physics: velocity graphs used to tune projectile behaviour in video games.',
            '✈️ Aviation: velocity decomposition is fundamental to aircraft trajectory planning.',
            '🚀 Rocketry: staging decisions are based on velocity component thresholds.'
        ]
    },
    chart_height: {
        title: '📈 Height vs Time Chart',
        bullets: [
            'Shows the projectile\'s <strong>altitude (y)</strong> as a function of <strong>time (t)</strong>.',
            'In a vacuum, the shape is a perfect downward parabola.',
            'With drag, the descent is steeper and asymmetric compared to the ascent.',
            'The curve peak shows the maximum height and when it is reached.',
            'The curve ends when y = 0 — the point of ground impact.'
        ],
        applications: [
            '🏗️ Demolition engineers use height vs time calculations for safety clearances.',
            '🌋 Volcanologists use height-time profiles of ballistic ejecta to predict impact zones.',
            '🏔️ Helicopter supply-drop calculations rely on height vs time models.',
            '🛸 Satellite re-entry: descent profile modelling for spacecraft returning from orbit.'
        ]
    },
    chart_energy: {
        title: '⚡ Energy Analysis Chart',
        bullets: [
            'Shows <strong>kinetic energy (KE)</strong>, <strong>potential energy (PE)</strong>, and <strong>total energy</strong> over time.',
            'In a vacuum: KE + PE = constant — total energy perfectly conserved.',
            'With drag: total energy decreases as it is lost to air resistance.',
            'KE is highest at launch and at impact; PE is zero at ground level.',
            'The shrinking total energy directly shows the work done by drag over time.'
        ],
        applications: [
            '⚙️ Engineers use energy audits to design more efficient launchers.',
            '🌱 Energy dissipation models help study particle deposition in the atmosphere.',
            '🏭 Spray systems (paint, water, concrete) use energy analysis to optimise nozzle design.',
            '🎓 Demonstrates the work-energy theorem and conservation laws visually.'
        ]
    },
    chart_optimal: {
        title: '🎯 Optimal Angle Chart',
        bullets: [
            'Plots <strong>horizontal range</strong> as a function of <strong>launch angle θ</strong> (20° to 70°).',
            'The peak of the curve shows the <strong>optimal angle</strong> for maximum range.',
            'In a vacuum, the peak is always at 45°. With drag, the peak shifts left.',
            'The shape becomes increasingly asymmetric as drag increases.',
            'Use this to find the best launch angle for any v₀ and B combination.'
        ],
        applications: [
            '🏈 Field goal kickers determine optimal kick angle for maximum distance.',
            '🎖️ Military computes optimal firing angle tables for every artillery piece.',
            '🚿 Sprinkler heads set to the optimal angle for maximum irrigation coverage.',
            '🏌️ Golf club face angles engineered to achieve optimal launch for each shot type.'
        ]
    },
    chart_air: {
        title: '🌬️ Air Resistance Comparison',
        bullets: [
            'Compares the real trajectory <strong>with drag</strong> vs the ideal <strong>vacuum trajectory</strong>.',
            'Shows how much shorter, lower, and steeper the real path is vs the ideal.',
            'Displays reduction in range, peak height, and flight time caused by air resistance.',
            'Only visible when drag coefficient B > 0.',
            'The gap between the two curves grows as B or v₀ increases.'
        ],
        applications: [
            '🏸 The huge gap for a shuttlecock shows why badminton is so different from tennis.',
            '🛸 Re-entry vehicles must account for drag to avoid overshooting landing zones.',
            '🌬️ Engineers compare drag profiles using similar before/after trajectory analysis.',
            '🎯 Long-range bullet drop tables built by comparing vacuum vs drag trajectories.'
        ]
    }
};

// Active popup element
let _activePopup = null;

/**
 * Show an info popup near the cursor position
 */
function showInfoPopup(key, event) {
    event.stopPropagation();
    hideInfoPopup();

    const def = TERM_DEFINITIONS[key];
    if (!def) return;

    const popup = document.createElement('div');
    popup.className = 'info-popup';
    popup.id = 'info-popup-active';

    const bulletsHtml = def.bullets.map(b => `<li>${b}</li>`).join('');
    const appsHtml = def.applications
        ? `<div class="info-popup-section"><strong>🌍 Real-World Applications</strong><ul>${def.applications.map(a => `<li>${a}</li>`).join('')}</ul></div>`
        : '';

    popup.innerHTML = `
        <div class="info-popup-header">
            <span class="info-popup-title">${def.title}</span>
            <button class="info-popup-close" title="Close">×</button>
        </div>
        <div class="info-popup-body">
            <ul>${bulletsHtml}</ul>
            ${appsHtml}
        </div>
    `;

    document.body.appendChild(popup);
    _activePopup = popup;

    // Position near cursor, keeping within viewport
    requestAnimationFrame(() => {
        const margin = 12;
        const rect = popup.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        let left = event.clientX + margin;
        let top = event.clientY + margin;

        if (left + rect.width > vw - margin) left = event.clientX - rect.width - margin;
        if (top + rect.height > vh - margin) top = event.clientY - rect.height - margin;
        if (top < margin) top = margin;
        if (left < margin) left = margin;

        popup.style.left = `${left}px`;
        popup.style.top = `${top}px`;
    });

    // Close button
    popup.querySelector('.info-popup-close').addEventListener('click', (e) => {
        e.stopPropagation();
        hideInfoPopup();
    });

    // Close on outside click
    setTimeout(() => {
        document.addEventListener('click', _outsideClickHandler);
    }, 10);
}

function _outsideClickHandler(e) {
    if (_activePopup && !_activePopup.contains(e.target)) {
        hideInfoPopup();
    }
}

function hideInfoPopup() {
    if (_activePopup) {
        _activePopup.remove();
        _activePopup = null;
    }
    document.removeEventListener('click', _outsideClickHandler);
}

/**
 * Bind hover colour + click popup to all .info-term[data-key] elements
 */
function initInfoTerms(container) {
    const root = container || document;
    root.querySelectorAll('.info-term[data-key]').forEach(el => {
        if (el.dataset.infoBound) return;
        el.dataset.infoBound = 'true';
        el.addEventListener('click', (e) => showInfoPopup(el.dataset.key, e));
    });
}

// Bind on page load
document.addEventListener('DOMContentLoaded', () => initInfoTerms());

// ==================== IMAGE LIGHTBOX ====================

let _lightbox = null;

function openLightbox(src) {
    if (_lightbox) closeLightbox();

    // State
    let scale = 1;
    let panX = 0, panY = 0;
    let isDragging = false;
    let startX = 0, startY = 0;
    let lastPanX = 0, lastPanY = 0;
    const MIN_SCALE = 0.5, MAX_SCALE = 8;

    const overlay = document.createElement('div');
    overlay.className = 'img-lightbox';

    const img = document.createElement('img');
    img.src = src;
    img.alt = 'Enlarged view';
    img.style.userSelect = 'none';
    img.style.cursor = 'grab';
    img.style.willChange = 'transform';

    const closeBtn = document.createElement('button');
    closeBtn.className = 'img-lightbox-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.title = 'Close (Esc)';

    const hint = document.createElement('div');
    hint.className = 'img-lightbox-hint';
    hint.textContent = 'Scroll to zoom · Drag to pan · Double-click to reset · Esc to close';

    overlay.appendChild(img);
    overlay.appendChild(closeBtn);
    overlay.appendChild(hint);
    document.body.appendChild(overlay);
    _lightbox = overlay;

    function applyTransform() {
        img.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    }

    // ---- Scroll to zoom (centred on cursor) ----
    overlay.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomFactor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
        const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale * zoomFactor));

        // Adjust pan so zoom is centred on the cursor position
        const rect = img.getBoundingClientRect();
        const offsetX = e.clientX - (rect.left + rect.width / 2);
        const offsetY = e.clientY - (rect.top + rect.height / 2);
        panX -= offsetX * (newScale / scale - 1);
        panY -= offsetY * (newScale / scale - 1);

        scale = newScale;
        applyTransform();
    }, { passive: false });

    // ---- Drag to pan ----
    img.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        isDragging = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
        lastPanX = panX;
        lastPanY = panY;
        img.style.cursor = 'grabbing';
        e.preventDefault();
    });

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);

    function onMouseMove(e) {
        if (!isDragging) return;
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        applyTransform();
    }

    function onMouseUp() {
        if (!isDragging) return;
        isDragging = false;
        img.style.cursor = 'grab';
    }

    // ---- Double-click image to reset ----
    img.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        scale = 1; panX = 0; panY = 0;
        applyTransform();
    });

    // ---- Close on overlay background click ----
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeLightbox();
    });

    closeBtn.addEventListener('click', closeLightbox);
    document.addEventListener('keydown', _lightboxKeyHandler);

    // Clean up mouse listeners on close
    const _origClose = closeLightbox;
    _lightbox._cleanup = () => {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    };
}


function _lightboxKeyHandler(e) {
    if (e.key === 'Escape') closeLightbox();
}

function closeLightbox() {
    if (_lightbox) {
        if (typeof _lightbox._cleanup === 'function') _lightbox._cleanup();
        _lightbox.remove();
        _lightbox = null;
    }
    document.removeEventListener('keydown', _lightboxKeyHandler);
}

/**
 * Bind double-click zoom to:
 *  - Any <canvas> element (converts to data URL)
 *  - Any .graph-image <img> element (uses its src)
 * Uses event delegation so dynamically added images are handled automatically.
 */
function initImageZoom() {
    // Canvas — convert to data URL on dblclick
    document.querySelectorAll('canvas').forEach(canvas => {
        if (canvas.dataset.zoomBound) return;
        canvas.dataset.zoomBound = 'true';
        canvas.title = 'Double-click to enlarge';
        canvas.style.cursor = 'zoom-in';
        canvas.addEventListener('dblclick', () => {
            const dataUrl = canvas.toDataURL('image/png');
            openLightbox(dataUrl);
        });
    });

    // Graph images — use event delegation on the document for dynamic images
    if (!document._zoomDelegated) {
        document._zoomDelegated = true;
        document.addEventListener('dblclick', (e) => {
            const img = e.target.closest('.graph-image');
            if (img && img.src && !img.src.endsWith('#')) {
                openLightbox(img.src);
            }
        });
    }
}

// Bind on page load
document.addEventListener('DOMContentLoaded', () => initImageZoom());
