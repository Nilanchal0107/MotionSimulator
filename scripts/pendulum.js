/**
 * Double Pendulum Simulator
 * Frontend logic for double pendulum simulation and chaotic motion visualization
 */

class PendulumSimulator {
    constructor() {
        this.canvas = document.getElementById('pendulum-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.traceCanvas = document.getElementById('trace-canvas');
        this.traceCtx = this.traceCanvas.getContext('2d');

        this.trajectoryData = null;
        this.animationFrame = null;
        this.isPlaying = false;
        this.currentFrame = 0;
        this.playbackSpeed = 1;
        this.trailLength = 100;
        this.tracePoints = [];

        this.init();
    }

    init() {
        this.setupControls();
        this.setupAnalysisTabs();
        this.loadPresets();
        this.drawInitialCanvas();
        this.drawInitialTrace();
    }

    setupControls() {
        // Sync all sliders with inputs
        syncSliderInput('m1-slider', 'm1-input');
        syncSliderInput('m2-slider', 'm2-input');
        syncSliderInput('L1-slider', 'L1-input');
        syncSliderInput('L2-slider', 'L2-input');
        syncSliderInput('theta1-slider', 'theta1-input');
        syncSliderInput('theta2-slider', 'theta2-input');
        syncSliderInput('omega1-slider', 'omega1-input');
        syncSliderInput('omega2-slider', 'omega2-input');
        syncSliderInput('duration-slider', 'duration-input');

        // Action buttons
        document.getElementById('simulate-pendulum').addEventListener('click', () => {
            this.simulate();
        });


        document.getElementById('reset-pendulum').addEventListener('click', () => {
            this.reset();
        });

        // Playback controls
        document.getElementById('play-pendulum').addEventListener('click', () => {
            this.play();
        });

        document.getElementById('pause-pendulum').addEventListener('click', () => {
            this.pause();
        });

        document.getElementById('restart-pendulum').addEventListener('click', () => {
            this.restart();
        });

        document.getElementById('pendulum-speed').addEventListener('change', (e) => {
            this.playbackSpeed = parseFloat(e.target.value);
        });

        // Clear trace
        document.getElementById('clear-trace').addEventListener('click', () => {
            this.clearTrace();
        });

        // Export
        document.getElementById('export-pendulum').addEventListener('click', () => {
            this.exportData();
        });

        // Preset scenarios
        document.getElementById('pendulum-presets').addEventListener('change', (e) => {
            this.loadPresetScenario(e.target.value);
        });
    }

    setupAnalysisTabs() {
        const tabs = document.querySelectorAll('.pendulum-tabs .analysis-tab');
        const views = document.querySelectorAll('#pendulum-section .analysis-view');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetAnalysis = tab.dataset.analysis;

                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                views.forEach(view => {
                    if (view.id.includes(targetAnalysis)) {
                        view.classList.add('active');
                    } else {
                        view.classList.remove('active');
                    }
                });
            });
        });

        // Tab info icons — stop propagation so tab switch still works
        document.querySelectorAll('#pendulum-section .tab-info-icon').forEach(icon => {
            icon.addEventListener('click', (e) => {
                e.stopPropagation();
                showInfoPopup(icon.dataset.key, e);
            });
        });
    }

    async loadPresets() {
        try {
            const result = await apiRequest('/api/presets/pendulum');
            const select = document.getElementById('pendulum-presets');

            for (const [key, preset] of Object.entries(result.presets)) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = preset.name;
                select.appendChild(option);
            }
        } catch (error) {
            console.error('Failed to load presets:', error);
        }
    }

    loadPresetScenario(presetKey) {
        if (!presetKey) return;

        apiRequest('/api/presets/pendulum')
            .then(result => {
                const preset = result.presets[presetKey];
                if (preset) {
                    document.getElementById('m1-slider').value = preset.m1;
                    document.getElementById('m1-input').value = preset.m1;
                    document.getElementById('m2-slider').value = preset.m2;
                    document.getElementById('m2-input').value = preset.m2;
                    document.getElementById('L1-slider').value = preset.L1;
                    document.getElementById('L1-input').value = preset.L1;
                    document.getElementById('L2-slider').value = preset.L2;
                    document.getElementById('L2-input').value = preset.L2;
                    document.getElementById('theta1-slider').value = preset.theta1;
                    document.getElementById('theta1-input').value = preset.theta1;
                    document.getElementById('theta2-slider').value = preset.theta2;
                    document.getElementById('theta2-input').value = preset.theta2;
                    document.getElementById('omega1-slider').value = preset.omega1;
                    document.getElementById('omega1-input').value = preset.omega1;
                    document.getElementById('omega2-slider').value = preset.omega2;
                    document.getElementById('omega2-input').value = preset.omega2;
                    document.getElementById('duration-slider').value = preset.t_max;
                    document.getElementById('duration-input').value = preset.t_max;
                    document.getElementById('fps-select').value = preset.fps;

                    showNotification(`Loaded preset: ${preset.name}`, 'success');
                }
            });
    }

    getParameters() {
        return {
            m1: parseFloat(document.getElementById('m1-input').value),
            m2: parseFloat(document.getElementById('m2-input').value),
            L1: parseFloat(document.getElementById('L1-input').value),
            L2: parseFloat(document.getElementById('L2-input').value),
            theta1: parseFloat(document.getElementById('theta1-input').value),
            theta2: parseFloat(document.getElementById('theta2-input').value),
            omega1: parseFloat(document.getElementById('omega1-input').value),
            omega2: parseFloat(document.getElementById('omega2-input').value),
            t_max: parseFloat(document.getElementById('duration-input').value),
            fps: parseInt(document.getElementById('fps-select').value)
        };
    }

    async simulate() {
        showLoadingIndicator('pendulum-loading');

        try {
            const params = this.getParameters();
            const result = await apiRequest('/api/pendulum/analyze', 'POST', params);

            if (result.status === 'success') {
                this.trajectoryData = result.trajectory;
                this.displayGraphs(result.graphs);
                this.displayStatistics(result.trajectory);

                this.currentFrame = 0;
                this.tracePoints = [];
                this.clearTrace();
                this.drawPendulum();
                showNotification('Simulation completed!', 'success');
            }
        } catch (error) {
            console.error('Simulation failed:', error);
        } finally {
            hideLoadingIndicator('pendulum-loading');
        }
    }

    displayGraphs(graphs) {
        if (graphs.angles) document.getElementById('pendulum-graph-angles').src = graphs.angles;
        if (graphs.angular_velocity) document.getElementById('pendulum-graph-velocity').src = graphs.angular_velocity;
        if (graphs.phase_space) document.getElementById('pendulum-graph-phase').src = graphs.phase_space;
        if (graphs.energy) document.getElementById('pendulum-graph-energy').src = graphs.energy;
        if (graphs.frequency) document.getElementById('pendulum-graph-frequency').src = graphs.frequency;
        if (graphs.heatmap) document.getElementById('pendulum-graph-heatmap').src = graphs.heatmap;
    }

    displayStatistics(trajectory) {
        const stats = [
            { key: 'pend_max_theta',   label: 'Max θ₁',       value: `${formatNumber(trajectory.max_theta1_deg)}°` },
            { key: 'pend_max_theta',   label: 'Max θ₂',       value: `${formatNumber(trajectory.max_theta2_deg)}°` },
            { key: 'pend_max_omega',   label: 'Max ω₁',       value: `${formatNumber(trajectory.max_omega1)} rad/s` },
            { key: 'pend_max_omega',   label: 'Max ω₂',       value: `${formatNumber(trajectory.max_omega2)} rad/s` },
            { key: 'pend_rotations',   label: 'Rotations 1', value: trajectory.rotations1 },
            { key: 'pend_rotations',   label: 'Rotations 2', value: trajectory.rotations2 },
            { key: 'pend_energy_error',label: 'Energy Error',value: `${formatNumber(trajectory.energy_error_percent, 4)}%` }
        ];

        const statsDiv = document.getElementById('pendulum-stats');
        statsDiv.innerHTML = '';

        for (const stat of stats) {
            const item = document.createElement('div');
            item.className = 'stat-item';
            item.innerHTML = `<strong><span class="info-term" data-key="${stat.key}">${stat.label}</span>:</strong> ${stat.value}`;
            statsDiv.appendChild(item);
        }

        // Bind newly created info-term elements
        initInfoTerms(statsDiv);
    }

    drawInitialCanvas() {
        // Black background
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw pivot point
        const centerX = this.canvas.width / 2;
        const centerY = 100;

        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 6, 0, 2 * Math.PI);
        this.ctx.fill();
    }

    drawInitialTrace() {
        this.traceCtx.fillStyle = '#FFFFFF';
        this.traceCtx.fillRect(0, 0, this.traceCanvas.width, this.traceCanvas.height);
    }

    drawPendulum() {
        if (!this.trajectoryData) return;

        const data = this.trajectoryData;
        const frame = Math.floor(this.currentFrame);

        if (frame >= data.t.length) return;

        // Clear canvas
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const centerX = this.canvas.width / 2;
        const centerY = 100;
        const scale = 150; // Scale for visualization

        // Get positions (subtract y to fix upside-down orientation)
        const x1 = centerX + data.x1[frame] * scale;
        const y1 = centerY - data.y1[frame] * scale;
        const x2 = centerX + data.x2[frame] * scale;
        const y2 = centerY - data.y2[frame] * scale;

        // Draw trail for second bob
        const trailStart = Math.max(0, frame - this.trailLength);
        this.ctx.strokeStyle = 'rgba(255, 215, 0, 0.3)';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        for (let i = trailStart; i <= frame; i++) {
            const tx = centerX + data.x2[i] * scale;
            const ty = centerY - data.y2[i] * scale;
            if (i === trailStart) {
                this.ctx.moveTo(tx, ty);
            } else {
                this.ctx.lineTo(tx, ty);
            }
        }
        this.ctx.stroke();

        // Draw arms
        this.ctx.strokeStyle = '#FFFFFF';
        this.ctx.lineWidth = 3;

        // First arm
        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY);
        this.ctx.lineTo(x1, y1);
        this.ctx.stroke();

        // Second arm
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();

        // Draw bobs
        // First bob (red)
        this.ctx.fillStyle = '#EF4444';
        this.ctx.strokeStyle = '#FFFFFF';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(x1, y1, 15, 0, 2 * Math.PI);
        this.ctx.fill();
        this.ctx.stroke();

        // Second bob (blue)
        this.ctx.fillStyle = '#3B82F6';
        this.ctx.beginPath();
        this.ctx.arc(x2, y2, 12, 0, 2 * Math.PI);
        this.ctx.fill();
        this.ctx.stroke();

        // Draw pivot
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 6, 0, 2 * Math.PI);
        this.ctx.fill();

        // Update time display
        const timeDisplay = document.getElementById('pendulum-time');
        if (timeDisplay) {
            timeDisplay.textContent = `T: ${formatNumber(data.t[frame])}s`;
        }

        // Update trace
        this.updateTrace(x2, y2);
    }

    updateTrace(x2, y2) {
        const traceScale = this.traceCanvas.width / this.canvas.width;
        const traceCenterX = this.traceCanvas.width / 2;
        const traceCenterY = this.traceCanvas.height / 2;

        const traceX = traceCenterX + (x2 - this.canvas.width / 2) * traceScale;
        const traceY = traceCenterY + (y2 - 100) * traceScale;

        // Draw point on trace canvas
        const hue = (this.currentFrame / (this.trajectoryData.t.length)) * 360;
        this.traceCtx.fillStyle = `hsl(${hue}, 80%, 50%)`;
        this.traceCtx.beginPath();
        this.traceCtx.arc(traceX, traceY, 2, 0, 2 * Math.PI);
        this.traceCtx.fill();
    }

    clearTrace() {
        this.traceCtx.fillStyle = '#FFFFFF';
        this.traceCtx.fillRect(0, 0, this.traceCanvas.width, this.traceCanvas.height);
        this.tracePoints = [];
    }

    play() {
        this.isPlaying = true;
        this.animate();
    }

    pause() {
        this.isPlaying = false;
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
    }

    restart() {
        this.currentFrame = 0;
        this.clearTrace();
        this.isPlaying = true;
        this.animate();
    }

    animate() {
        if (!this.isPlaying || !this.trajectoryData) return;

        this.currentFrame += this.playbackSpeed;

        if (this.currentFrame >= this.trajectoryData.t.length) {
            this.currentFrame = this.trajectoryData.t.length - 1;
            this.isPlaying = false;
        }

        this.drawPendulum();

        if (this.isPlaying) {
            this.animationFrame = requestAnimationFrame(() => this.animate());
        }
    }

    reset() {
        this.pause();
        this.currentFrame = 0;
        this.trajectoryData = null;
        this.drawInitialCanvas();
        this.clearTrace();

        // Reset controls to defaults
        document.getElementById('m1-slider').value = 1;
        document.getElementById('m1-input').value = 1;
        document.getElementById('m2-slider').value = 1;
        document.getElementById('m2-input').value = 1;
        document.getElementById('L1-slider').value = 1;
        document.getElementById('L1-input').value = 1;
        document.getElementById('L2-slider').value = 1;
        document.getElementById('L2-input').value = 1;
        document.getElementById('theta1-slider').value = 90;
        document.getElementById('theta1-input').value = 90;
        document.getElementById('theta2-slider').value = 90;
        document.getElementById('theta2-input').value = 90;
        document.getElementById('omega1-slider').value = 0;
        document.getElementById('omega1-input').value = 0;
        document.getElementById('omega2-slider').value = 0;
        document.getElementById('omega2-input').value = 0;
        document.getElementById('duration-slider').value = 20;
        document.getElementById('duration-input').value = 20;

        // Clear stats
        document.getElementById('pendulum-stats').innerHTML = '';

        showNotification('Reset complete', 'info');
    }

    exportData() {
        if (!this.trajectoryData) {
            showNotification('No simulation data to export', 'warning');
            return;
        }

        // Export as CSV
        let csv = 'Time,Theta1,Theta2,Omega1,Omega2,X1,Y1,X2,Y2,KE,PE,Total_Energy\n';
        const data = this.trajectoryData;

        for (let i = 0; i < data.t.length; i++) {
            csv += `${data.t[i]},${data.theta1[i]},${data.theta2[i]},${data.omega1[i]},${data.omega2[i]},`;
            csv += `${data.x1[i]},${data.y1[i]},${data.x2[i]},${data.y2[i]},`;
            csv += `${data.kinetic_energy[i]},${data.potential_energy[i]},${data.total_energy[i]}\n`;
        }

        downloadFile(csv, 'pendulum_data.csv', 'text/csv');
        showNotification('Data exported successfully', 'success');
    }
}
