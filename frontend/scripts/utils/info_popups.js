/**
 * info_popups.js
 * Handles clickable "info-term" labels and the ℹ tab-info-icon buttons.
 * Clicking any element opens a small floating popup card with educational content.
 */

(function () {
    'use strict';

    // ── Content dictionary ────────────────────────────────────────────────────
    const INFO_CONTENT = {
        // ---- Projectile Motion ----
        parameters: {
            title: 'Parameters',
            body: 'Adjust these physical properties to define how the projectile is launched.',
            sections: [
                { heading: 'What you can control', items: ['Drag coefficient (air resistance)', 'Initial velocity (launch speed)', 'Launch angle', 'Maximum simulation time'] }
            ]
        },
        drag_coeff: {
            title: 'Drag Coefficient (B)',
            body: 'Controls how much air resistance acts on the projectile. B = 0 means a perfect vacuum — the trajectory is a pure parabola. Higher B means more drag and a shorter, lower trajectory.',
            sections: [
                { heading: 'Typical values', items: ['0 — Vacuum (no air)', '0.3 — Soccer / football', '1.0 — Golf ball', '2.5 — Shuttlecock'] }
            ]
        },
        init_velocity: {
            title: 'Initial Velocity (v₀)',
            body: 'The launch speed of the projectile in metres per second. Together with the angle, this determines the range and height of the trajectory.',
            sections: [
                { heading: 'Formula', items: ['vx = v₀ cos(θ)', 'vy = v₀ sin(θ)'] }
            ]
        },
        launch_angle: {
            title: 'Launch Angle (θ)',
            body: 'The angle above the horizontal at which the projectile is launched. In a vacuum, 45° gives the maximum horizontal range.',
            sections: [
                { heading: 'Key angles', items: ['45° — max range (vacuum)', '<45° — flatter, faster trajectory', '>45° — higher arc, shorter range'] }
            ]
        },
        sim_time: {
            title: 'Max Simulation Time',
            body: 'The maximum duration (in seconds) the simulation will run for. The projectile stops when it hits the ground or when this time is reached.',
        },
        gravity: {
            title: 'Gravity / Planet',
            body: 'Selects the gravitational acceleration used in the simulation. Different planets have very different surface gravity.',
            sections: [
                { heading: 'Values (m/s²)', items: ['🌍 Earth — 9.81', '🌕 Moon — 1.62', '🔴 Mars — 3.72', '🪐 Jupiter — 24.79'] }
            ]
        },
        presets: {
            title: 'Preset Scenarios',
            body: 'Quick-load a real-world scenario with realistic parameters for that type of projectile.',
            sections: [
                { heading: 'Available presets', items: ['Basketball', 'Golf ball', 'Soccer ball', 'Cannonball', 'Vacuum (no air)'] }
            ]
        },
        traj_viz: {
            title: 'Trajectory Visualization',
            body: 'Shows the full path of the projectile on a 2-D canvas. The red dot is the current position; the green arrow shows the velocity vector.',
            sections: [
                { heading: 'Controls', items: ['▶ Play — animate the flight', '⏸ Pause — freeze at current point', '↺ Restart — replay from start', 'Speed — change playback rate'] }
            ]
        },

        // ---- Analysis charts (Projectile) ----
        chart_velocity: {
            title: 'Velocity Components Chart',
            body: 'Shows how the horizontal (vx) and vertical (vy) velocity components change over time. Horizontal velocity stays constant in vacuum; drag reduces it. Vertical velocity falls due to gravity.',
        },
        chart_height: {
            title: 'Height vs Time Chart',
            body: 'Plots the projectile\'s height (y) against time. The curve peaks at maximum height and returns to zero at landing.',
        },
        chart_energy: {
            title: 'Energy Analysis Chart',
            body: 'Plots kinetic energy (KE = ½mv²), potential energy (PE = mgh), and total energy over time. With drag, total energy decreases — energy is lost to heat.',
        },
        chart_optimal: {
            title: 'Optimal Angle Chart',
            body: 'Shows the horizontal range achieved across all launch angles (0°–90°). The peak of this curve is the optimal angle. Without air resistance this is always 45°; drag shifts it slightly lower.',
        },
        chart_air: {
            title: 'Air Resistance Comparison',
            body: 'Overlays the trajectory with and without drag so you can see the impact of air resistance on range and height.',
        },

        // ---- Double Pendulum ----
        pend_params: {
            title: 'Pendulum Parameters',
            body: 'Controls the physical properties of both arms and bobs of the double pendulum system.',
        },
        mass1: {
            title: 'Mass of Bob 1 (m₁)',
            body: 'The mass of the first (upper) pendulum bob in kilograms. Heavier bobs carry more momentum and affect the coupled motion differently.',
        },
        length1: {
            title: 'Length of Arm 1 (L₁)',
            body: 'The length of the first pendulum arm in metres. Longer arms swing more slowly (period ∝ √L).',
        },
        theta1: {
            title: 'Initial Angle θ₁',
            body: 'Starting angle of the first arm from vertical, in degrees. 0° = hanging straight down. Larger angles lead to more energetic, chaotic motion.',
        },
        omega1: {
            title: 'Initial Angular Velocity ω₁',
            body: 'Starting rotational speed of the first arm in rad/s. Positive = counter-clockwise.',
        },
        mass2: {
            title: 'Mass of Bob 2 (m₂)',
            body: 'The mass of the second (lower) pendulum bob in kilograms.',
        },
        length2: {
            title: 'Length of Arm 2 (L₂)',
            body: 'The length of the second pendulum arm in metres.',
        },
        theta2: {
            title: 'Initial Angle θ₂',
            body: 'Starting angle of the second arm from vertical, in degrees.',
        },
        omega2: {
            title: 'Initial Angular Velocity ω₂',
            body: 'Starting rotational speed of the second arm in rad/s.',
        },
        p_duration: {
            title: 'Simulation Duration',
            body: 'How many seconds of physical time to simulate. Longer durations give more data for chaos analysis but take more computation time.',
        },
        fps: {
            title: 'Quality (FPS)',
            body: 'Frames per second used to record the simulation. Higher FPS gives smoother animation and better analysis graphs but increases computation time significantly.',
            sections: [
                { heading: 'Options', items: ['50 fps — fast compute, rougher graphs', '100 fps — balanced (default)', '200 fps — slow compute, smoothest graphs'] }
            ]
        },
        damping: {
            title: 'Damping Coefficient (b)',
            body: 'Models energy dissipation (friction / air drag) in the pendulum. b = 0 is a perfectly frictionless system; higher values damp the motion faster.',
            sections: [
                { heading: 'Typical values', items: ['0 — Frictionless (default)', '0.1 — Light damping', '0.5 — Medium', '1.5 — Heavy damping'] }
            ]
        },
        p_presets: {
            title: 'Preset Scenarios',
            body: 'Quick-load a physically interesting situation. Presets range from gentle periodic swings to highly chaotic motion.',
        },
        pend_anim: {
            title: 'Pendulum Animation',
            body: 'Live canvas showing the double pendulum in motion. The golden trail follows the lower bob. The path trace canvas below records the full trajectory.',
        },

        // ---- Pendulum analysis charts ----
        pchart_angles: {
            title: 'Angles vs Time',
            body: 'Shows how θ₁ and θ₂ evolve over time. Periodic motion gives smooth waves; chaotic motion gives irregular, never-repeating patterns.',
        },
        pchart_velocity: {
            title: 'Angular Velocity vs Time',
            body: 'Plots ω₁ and ω₂ (the rate of change of the angles) over time. Sharp spikes indicate fast "flip" events.',
        },
        pchart_phase: {
            title: 'Phase Space Diagram',
            body: 'Plots angle vs angular velocity (θ vs ω) for each arm. Periodic motion = closed loops; chaotic motion = space-filling, never-closed curves called "strange attractors".',
        },
        pchart_energy: {
            title: 'Energy Conservation',
            body: 'Plots total mechanical energy over time. For a frictionless system energy should be constant — any drift indicates numerical integration error. With damping, energy decays steadily.',
        },
        pchart_fft: {
            title: 'FFT Frequency Spectrum',
            body: 'Fast Fourier Transform of the angle signal. Periodic motion shows a few sharp peaks; chaotic motion shows a broad, noisy spectrum with no dominant frequency.',
        },
        pchart_heatmap: {
            title: 'Position Heatmap',
            body: 'Shows how often the second bob visits each region of space. Hot (bright) areas are visited most. Chaotic motion spreads the heat broadly; near-periodic motion concentrates it.',
        },
    };

    // ── Popup state ───────────────────────────────────────────────────────────
    let currentPopup = null;

    function closePopup() {
        if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
        }
    }

    function buildPopup(info) {
        const div = document.createElement('div');
        div.className = 'info-popup';

        // Header
        const header = document.createElement('div');
        header.className = 'info-popup-header';

        const title = document.createElement('span');
        title.className = 'info-popup-title';
        title.textContent = info.title;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'info-popup-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.addEventListener('click', (e) => { e.stopPropagation(); closePopup(); });

        header.appendChild(title);
        header.appendChild(closeBtn);

        // Body
        const body = document.createElement('div');
        body.className = 'info-popup-body';

        const bodyText = document.createElement('p');
        bodyText.textContent = info.body;
        body.appendChild(bodyText);

        if (info.sections) {
            info.sections.forEach(sec => {
                const section = document.createElement('div');
                section.className = 'info-popup-section';

                const heading = document.createElement('strong');
                heading.textContent = sec.heading;
                section.appendChild(heading);

                const ul = document.createElement('ul');
                sec.items.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item;
                    ul.appendChild(li);
                });
                section.appendChild(ul);
                body.appendChild(section);
            });
        }

        div.appendChild(header);
        div.appendChild(body);
        return div;
    }

    function positionPopup(popup, triggerEl) {
        // Append off-screen first so we can measure its size
        popup.style.visibility = 'hidden';
        popup.style.top = '0px';
        popup.style.left = '0px';
        document.body.appendChild(popup);

        const rect = triggerEl.getBoundingClientRect(); // viewport-relative
        const popW = popup.offsetWidth;
        const popH = popup.offsetHeight;
        const margin = 10;
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        // Default: open below the trigger, aligned to its left edge
        let top = rect.bottom + margin;
        let left = rect.left;

        // Flip right → left if overflows right viewport edge
        if (left + popW > vw - margin) {
            left = rect.right - popW;
        }

        // Flip below → above if overflows bottom viewport edge
        if (top + popH > vh - margin) {
            top = rect.top - popH - margin;
        }

        // Hard-clamp so it never goes outside the viewport
        top  = Math.min(Math.max(margin, top),  vh - popH - margin);
        left = Math.min(Math.max(margin, left), vw - popW - margin);

        popup.style.top  = top  + 'px';
        popup.style.left = left + 'px';
        popup.style.visibility = '';
    }

    function openPopup(key, triggerEl) {
        closePopup();

        const info = INFO_CONTENT[key];
        if (!info) return;

        const popup = buildPopup(info);
        positionPopup(popup, triggerEl);
        currentPopup = popup;
    }

    // ── Wire up elements ──────────────────────────────────────────────────────

    function attachListeners() {
        // .info-term spans — data-key attribute selects the content entry
        document.querySelectorAll('.info-term[data-key]').forEach(el => {
            el.addEventListener('click', (e) => {
                // Mark this event so the document handler knows it came from a trigger
                e._fromPopupTrigger = true;
                const key = el.dataset.key;
                if (currentPopup && el._popupOpen) {
                    // Second click on same term → toggle off
                    closePopup();
                    el._popupOpen = false;
                } else {
                    document.querySelectorAll('.info-term').forEach(t => t._popupOpen = false);
                    el._popupOpen = true;
                    openPopup(key, el);
                }
            });
        });

        // .tab-info-icon spans inside analysis tabs
        document.querySelectorAll('.tab-info-icon[data-key]').forEach(el => {
            el.addEventListener('click', (e) => {
                e._fromPopupTrigger = true;
                openPopup(el.dataset.key, el);
            });
        });

        // Document-level: close popup when clicking OUTSIDE it
        document.addEventListener('click', (e) => {
            if (!currentPopup) return;
            // Don't close if clicking inside the popup itself
            if (currentPopup.contains(e.target)) return;
            // Don't close if this click was the one that opened the popup
            if (e._fromPopupTrigger) return;
            closePopup();
            document.querySelectorAll('.info-term').forEach(t => t._popupOpen = false);
        });

        // Escape key always closes popup
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closePopup();
                document.querySelectorAll('.info-term').forEach(t => t._popupOpen = false);
            }
        });
    }

    // Run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', attachListeners);
    } else {
        attachListeners();
    }

})();
