/**
 * Projectile Motion Simulator
 * Frontend logic for projectile motion simulation and visualization
 */

class ProjectileSimulator {
    constructor() {
        this.canvas = document.getElementById('projectile-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.trajectoryData = null;
        this.animationFrame = null;
        this.isPlaying = false;
        this.animationProgress = 0;
        this.playbackSpeed = 1;

        this.init();
    }

    init() {
        this.setupControls();
        this.setupAnalysisTabs();
        this.loadPresets();
        this.drawInitialCanvas();
    }

    setupControls() {
        // Sync sliders with inputs
        syncSliderInput('drag-slider', 'drag-input', () => this.updateAngleDisplay());
        syncSliderInput('velocity-slider', 'velocity-input');
        syncSliderInput('angle-slider', 'angle-input', (val) => this.updateAngleDisplay(val));
        syncSliderInput('time-slider', 'time-input');

        // Preset drag coefficient buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const value = btn.dataset.value;
                document.getElementById('drag-slider').value = value;
                document.getElementById('drag-input').value = value;
            });
        });

        // Action buttons
        document.getElementById('simulate-projectile').addEventListener('click', () => {
            this.simulate();
        });

        document.getElementById('find-optimal-angle').addEventListener('click', () => {
            this.findOptimalAngle();
        });

        document.getElementById('reset-projectile').addEventListener('click', () => {
            this.reset();
        });

        // Playback controls
        document.getElementById('play-projectile').addEventListener('click', () => {
            this.play();
        });

        document.getElementById('pause-projectile').addEventListener('click', () => {
            this.pause();
        });

        document.getElementById('restart-projectile').addEventListener('click', () => {
            this.restart();
        });

        document.getElementById('projectile-speed').addEventListener('change', (e) => {
            this.playbackSpeed = parseFloat(e.target.value);
        });



        // Export
        document.getElementById('export-projectile').addEventListener('click', () => {
            this.exportData();
        });

        // Tab info icons — stop propagation so tab switch still works; open popup on icon click
        document.querySelectorAll('#projectile-section .tab-info-icon').forEach(icon => {
            icon.addEventListener('click', (e) => {
                e.stopPropagation();
                showInfoPopup(icon.dataset.key, e);
            });
        });

        // Preset scenarios
        document.getElementById('projectile-presets').addEventListener('change', (e) => {
            this.loadPresetScenario(e.target.value);
        });
    }

    setupAnalysisTabs() {
        setupAnalysisTabs('.analysis-tab', '.analysis-view');
    }

    async loadPresets() {
        try {
            const result = await apiRequest('/api/presets/projectile');
            const select = document.getElementById('projectile-presets');

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

        apiRequest('/api/presets/projectile')
            .then(result => {
                const preset = result.presets[presetKey];
                if (preset) {
                    document.getElementById('velocity-slider').value = preset.v0;
                    document.getElementById('velocity-input').value = preset.v0;
                    document.getElementById('angle-slider').value = preset.angle;
                    document.getElementById('angle-input').value = preset.angle;
                    document.getElementById('drag-slider').value = preset.drag_coeff;
                    document.getElementById('drag-input').value = preset.drag_coeff;
                    document.getElementById('time-slider').value = preset.t_max;
                    document.getElementById('time-input').value = preset.t_max;

                    this.updateAngleDisplay(preset.angle);
                    showNotification(`Loaded preset: ${preset.name}`, 'success');
                }
            });
    }

    updateAngleDisplay(angleDeg) {
        const angle = angleDeg || parseFloat(document.getElementById('angle-input').value);
        const radians = (angle * Math.PI / 180).toFixed(3);
        const display = document.getElementById('angle-radians');
        if (display) {
            display.textContent = `${radians} rad`;
        }
    }

    getParameters() {
        return {
            v0: parseFloat(document.getElementById('velocity-input').value),
            angle: parseFloat(document.getElementById('angle-input').value),
            drag_coeff: parseFloat(document.getElementById('drag-input').value),
            t_max: parseFloat(document.getElementById('time-input').value)
        };
    }

    async simulate() {
        showLoadingIndicator('projectile-loading');

        try {
            const params = this.getParameters();
            const result = await apiRequest('/api/projectile/analyze', 'POST', params);

            if (result.status === 'success') {
                this.trajectoryData = result.trajectory;
                this.displayGraphs(result.graphs);
                this.displayStatistics(result.trajectory);

                this.animationProgress = 0;
                this.drawTrajectory();
                showNotification('Simulation completed!', 'success');
            }
        } catch (error) {
            console.error('Simulation failed:', error);
        } finally {
            hideLoadingIndicator('projectile-loading');
        }
    }

    async findOptimalAngle() {
        showLoadingIndicator('projectile-loading');

        try {
            const params = this.getParameters();
            const result = await apiRequest('/api/projectile/optimal_angle', 'POST', params);

            if (result.status === 'success') {
                // Display optimal angle graph
                document.getElementById('graph-optimal').src = result.graph;

                // Switch to optimal angle tab
                document.querySelector('[data-analysis="optimal"]').click();

                showNotification(
                    `Optimal angle: ${result.optimal_angle}° (Range: ${formatNumber(result.max_range)}m)`,
                    'success'
                );
            }
        } catch (error) {
            console.error('Optimal angle calculation failed:', error);
        } finally {
            hideLoadingIndicator('projectile-loading');
        }
    }

    displayGraphs(graphs) {
        if (graphs.trajectory) {
            document.getElementById('graph-velocity').src = graphs.velocity_components;
        }
        if (graphs.height_vs_time) {
            document.getElementById('graph-height').src = graphs.height_vs_time;
        }
        if (graphs.energy) {
            document.getElementById('graph-energy').src = graphs.energy;
        }
        if (graphs.air_resistance) {
            document.getElementById('graph-drag').src = graphs.air_resistance;
        }
    }

    displayStatistics(trajectory) {
        const stats = [
            { key: 'max_height',    label: 'Max Height',    value: formatPhysicsValue(trajectory.max_height, 'm') },
            { key: 'time_to_max',   label: 'Time to Max',   value: formatPhysicsValue(trajectory.time_to_max_height, 's') },
            { key: 'flight_time',   label: 'Flight Time',   value: formatPhysicsValue(trajectory.total_flight_time, 's') },
            { key: 'range',         label: 'Range',         value: formatPhysicsValue(trajectory.horizontal_range, 'm') },
            { key: 'impact_speed',  label: 'Impact Speed',  value: formatPhysicsValue(trajectory.impact_speed, 'm/s') },
            { key: 'impact_angle',  label: 'Impact Angle',  value: formatPhysicsValue(trajectory.impact_angle_deg, '°') },
            { key: 'energy_lost',   label: 'Energy Lost',   value: formatPhysicsValue(trajectory.energy_lost_percent, '%') }
        ];

        const statsContainer = document.getElementById('projectile-stats');
        statsContainer.innerHTML = '';

        for (const stat of stats) {
            const statCard = document.createElement('div');
            statCard.className = 'stat-card';
            statCard.innerHTML = `
                <div class="stat-label">
                    <span class="info-term" data-key="${stat.key}">${stat.label}</span>
                </div>
                <div class="stat-value">${stat.value}</div>
            `;
            statsContainer.appendChild(statCard);
        }

        // Bind the newly created info-term elements
        initInfoTerms(statsContainer);
    }

    drawInitialCanvas() {
        this.ctx.fillStyle = '#f8fafc';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw ground
        this.ctx.strokeStyle = '#8B4513';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.canvas.height - 50);
        this.ctx.lineTo(this.canvas.width, this.canvas.height - 50);
        this.ctx.stroke();

        // Draw grid
        this.ctx.strokeStyle = '#e2e8f0';
        this.ctx.lineWidth = 1;
        for (let x = 0; x < this.canvas.width; x += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        for (let y = 0; y < this.canvas.height; y += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }

    drawTrajectory() {
        if (!this.trajectoryData) return;

        this.drawInitialCanvas();

        const data = this.trajectoryData;
        const xData = data.x;
        const yData = data.y;

        // Scale to canvas
        const maxX = Math.max(...xData);
        const maxY = Math.max(...yData);
        const margin = 50;
        const scaleX = (this.canvas.width - 2 * margin) / maxX;
        const scaleY = (this.canvas.height - 2 * margin) / maxY;
        const scale = Math.min(scaleX, scaleY);

        // Draw trajectory path
        this.ctx.strokeStyle = '#3B82F6';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        for (let i = 0; i < xData.length; i++) {
            const x = margin + xData[i] * scale;
            const y = this.canvas.height - margin - yData[i] * scale;

            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }
        this.ctx.stroke();

        // Draw projectile at current position
        if (this.animationProgress < xData.length) {
            const idx = Math.floor(this.animationProgress);
            const x = margin + xData[idx] * scale;
            const y = this.canvas.height - margin - yData[idx] * scale;

            this.ctx.fillStyle = '#EF4444';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 8, 0, 2 * Math.PI);
            this.ctx.fill();

            // Draw velocity vector
            const vx = data.vx[idx];
            const vy = data.vy[idx];
            const vectorScale = 5;

            this.ctx.strokeStyle = '#10B981';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(x + vx * vectorScale, y - vy * vectorScale);
            this.ctx.stroke();

            // Arrowhead
            const angle = Math.atan2(-vy, vx);
            const arrowLength = 8;
            this.ctx.beginPath();
            this.ctx.moveTo(x + vx * vectorScale, y - vy * vectorScale);
            this.ctx.lineTo(
                x + vx * vectorScale - arrowLength * Math.cos(angle - Math.PI / 6),
                y - vy * vectorScale + arrowLength * Math.sin(angle - Math.PI / 6)
            );
            this.ctx.moveTo(x + vx * vectorScale, y - vy * vectorScale);
            this.ctx.lineTo(
                x + vx * vectorScale - arrowLength * Math.cos(angle + Math.PI / 6),
                y - vy * vectorScale + arrowLength * Math.sin(angle + Math.PI / 6)
            );
            this.ctx.stroke();
        }
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
        this.animationProgress = 0;
        this.isPlaying = true;
        this.animate();
    }

    animate() {
        if (!this.isPlaying || !this.trajectoryData) return;

        this.animationProgress += this.playbackSpeed;

        if (this.animationProgress >= this.trajectoryData.x.length) {
            this.animationProgress = this.trajectoryData.x.length - 1;
            this.isPlaying = false;
        }

        this.drawTrajectory();

        if (this.isPlaying) {
            this.animationFrame = requestAnimationFrame(() => this.animate());
        }
    }

    reset() {
        this.pause();
        this.animationProgress = 0;
        this.trajectoryData = null;
        this.drawInitialCanvas();

        // Reset controls to defaults
        document.getElementById('velocity-slider').value = 20;
        document.getElementById('velocity-input').value = 20;
        document.getElementById('angle-slider').value = 45;
        document.getElementById('angle-input').value = 45;
        document.getElementById('drag-slider').value = 0.3;
        document.getElementById('drag-input').value = 0.3;
        document.getElementById('time-slider').value = 10;
        document.getElementById('time-input').value = 10;

        this.updateAngleDisplay(45);

        // Clear stats
        document.getElementById('projectile-stats').innerHTML = '';

        showNotification('Reset complete', 'info');
    }

    exportData() {
        if (!this.trajectoryData) {
            showNotification('No simulation data to export', 'warning');
            return;
        }

        // Export as CSV
        let csv = 'Time,X,Y,Vx,Vy,Speed,KE,PE,Total Energy\n';
        const data = this.trajectoryData;

        for (let i = 0; i < data.t.length; i++) {
            csv += `${data.t[i]},${data.x[i]},${data.y[i]},${data.vx[i]},${data.vy[i]},`;
            csv += `${data.speed[i]},${data.kinetic_energy[i]},${data.potential_energy[i]},${data.total_energy[i]}\n`;
        }

        downloadFile(csv, 'projectile_data.csv', 'text/csv');
        showNotification('Data exported successfully', 'success');
    }
}
