/**
 * Projectile Simulator — Main Class
 * Orchestrates controls, API calls, canvas, analysis, and export.
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
        this._setupControls();
        this._setupAnalysisTabs();
        this._loadPresets();
        this._drawInitialCanvas();
    }

    _setupControls() {
        syncSliderInput('drag-slider', 'drag-input', () => this._updateAngleDisplay());
        syncSliderInput('velocity-slider', 'velocity-input', debounce(() => this._updateAngleDisplay(), 300));
        syncSliderInput('angle-slider', 'angle-input', (val) => {
            this._updateAngleDisplay(val);
            debounce(() => this._updateAngleDisplay(), 300)();
        });
        syncSliderInput('time-slider', 'time-input');

        document.querySelectorAll('#projectile-section .preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.target || 'drag';
                if (target === 'drag') {
                    document.getElementById('drag-slider').value = btn.dataset.value;
                    document.getElementById('drag-input').value = btn.dataset.value;
                }
            });
        });

        document.getElementById('simulate-projectile').addEventListener('click', () => this.simulate());
        document.getElementById('find-optimal-angle').addEventListener('click', () => this.findOptimalAngle());
        document.getElementById('reset-projectile').addEventListener('click', () => this.reset());
        document.getElementById('play-projectile').addEventListener('click', () => this.play());
        document.getElementById('pause-projectile').addEventListener('click', () => this.pause());
        document.getElementById('restart-projectile').addEventListener('click', () => this.restart());

        document.getElementById('projectile-speed').addEventListener('change', (e) => {
            this.playbackSpeed = parseFloat(e.target.value);
        });

        document.getElementById('projectile-presets').addEventListener('change', (e) => {
            this._loadPresetScenario(e.target.value);
        });
    }

    _setupAnalysisTabs() {
        setupAnalysisTabs('.analysis-tab', '.analysis-view');
    }

    async _loadPresets() {
        try {
            const result = await apiRequest('/api/presets/projectile');
            const select = document.getElementById('projectile-presets');
            for (const [key, preset] of Object.entries(result.presets)) {
                const opt = document.createElement('option');
                opt.value = key;
                opt.textContent = preset.name;
                select.appendChild(opt);
            }
        } catch (e) { console.error('Failed to load presets:', e); }
    }

    _loadPresetScenario(presetKey) {
        if (!presetKey) return;
        apiRequest('/api/presets/projectile').then(result => {
            const preset = result.presets[presetKey];
            if (!preset) return;
            ['velocity', 'angle', 'drag', 'time'].forEach(name => {
                const key = name === 'drag' ? 'drag_coeff' : name === 'velocity' ? 'v0' : name === 'time' ? 't_max' : name;
                const sliderName = name === 'drag' ? 'drag' : name;
                document.getElementById(`${sliderName}-slider`).value = preset[key];
                document.getElementById(`${sliderName}-input`).value = preset[key];
            });
            this._updateAngleDisplay(preset.angle);
            showNotification(`Loaded: ${preset.name}`, 'success');
        });
    }

    _updateAngleDisplay(angleDeg) {
        const angle = angleDeg || parseFloat(document.getElementById('angle-input').value);
        const display = document.getElementById('angle-radians');
        if (display) display.textContent = `${(angle * Math.PI / 180).toFixed(3)} rad`;
    }

    _getParameters() {
        const gravitySelect = document.getElementById('proj-gravity-select');
        return {
            v0: parseFloat(document.getElementById('velocity-input').value),
            angle: parseFloat(document.getElementById('angle-input').value),
            drag_coeff: parseFloat(document.getElementById('drag-input').value),
            t_max: parseFloat(document.getElementById('time-input').value),
            gravity_preset: gravitySelect ? gravitySelect.value : 'earth'
        };
    }

    async simulate() {
        showLoadingIndicator('projectile-loading');
        try {
            const result = await apiRequest('/api/projectile/analyze', 'POST', this._getParameters());
            if (result.status === 'success') {
                this.trajectoryData = result.trajectory;
                this._displayGraphs(result.graphs);
                this._displayStatistics(result.trajectory);
                this.animationProgress = 0;
                this._drawTrajectory();
                showNotification('Simulation completed!', 'success');
            }
        } catch (e) { console.error('Simulation failed:', e); }
        finally { hideLoadingIndicator('projectile-loading'); }
    }

    async findOptimalAngle() {
        showLoadingIndicator('projectile-loading');
        try {
            const result = await apiRequest('/api/projectile/optimal_angle', 'POST', this._getParameters());
            if (result.status === 'success') {
                document.getElementById('graph-optimal').src = result.graph;
                document.querySelector('[data-analysis="optimal"]').click();
                showNotification(`Optimal: ${result.optimal_angle.toFixed(1)}° (${formatNumber(result.max_range)} m)`, 'success');
            }
        } catch (e) { console.error('Optimal angle failed:', e); }
        finally { hideLoadingIndicator('projectile-loading'); }
    }

    _displayGraphs(graphs) {
        if (graphs.velocity_components) document.getElementById('graph-velocity').src = graphs.velocity_components;
        if (graphs.height_vs_time) document.getElementById('graph-height').src = graphs.height_vs_time;
        if (graphs.energy) document.getElementById('graph-energy').src = graphs.energy;
        if (graphs.air_resistance) document.getElementById('graph-drag').src = graphs.air_resistance;
    }

    _displayStatistics(trajectory) {
        const stats = [
            { key: 'max_height', label: 'Max Height', value: formatPhysicsValue(trajectory.max_height, 'm') },
            { key: 'time_to_max', label: 'Time to Max', value: formatPhysicsValue(trajectory.time_to_max_height, 's') },
            { key: 'flight_time', label: 'Flight Time', value: formatPhysicsValue(trajectory.total_flight_time, 's') },
            { key: 'range', label: 'Range', value: formatPhysicsValue(trajectory.horizontal_range, 'm') },
            { key: 'impact_speed', label: 'Impact Speed', value: formatPhysicsValue(trajectory.impact_speed, 'm/s') },
            { key: 'impact_angle', label: 'Impact Angle', value: formatPhysicsValue(trajectory.impact_angle_deg, '°') },
            { key: 'energy_lost', label: 'Energy Lost', value: formatPhysicsValue(trajectory.energy_lost_percent, '%') },
        ];
        const container = document.getElementById('projectile-stats');
        container.innerHTML = stats.map(s => `
            <div class="stat-card">
                <div class="stat-label">${s.label}</div>
                <div class="stat-value">${s.value}</div>
            </div>`).join('');
    }

    _drawInitialCanvas() {
        this.ctx.fillStyle = '#f8fafc';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = '#8B4513'; this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.canvas.height - 50);
        this.ctx.lineTo(this.canvas.width, this.canvas.height - 50);
        this.ctx.stroke();
        this.ctx.strokeStyle = '#e2e8f0'; this.ctx.lineWidth = 1;
        for (let x = 0; x < this.canvas.width; x += 50) { this.ctx.beginPath(); this.ctx.moveTo(x, 0); this.ctx.lineTo(x, this.canvas.height); this.ctx.stroke(); }
        for (let y = 0; y < this.canvas.height; y += 50) { this.ctx.beginPath(); this.ctx.moveTo(0, y); this.ctx.lineTo(this.canvas.width, y); this.ctx.stroke(); }
    }

    _drawTrajectory() {
        if (!this.trajectoryData) return;
        this._drawInitialCanvas();
        const { x: xData, y: yData, vx, vy } = this.trajectoryData;
        const margin = 50;
        const scale = Math.min((this.canvas.width - 2 * margin) / Math.max(...xData), (this.canvas.height - 2 * margin) / Math.max(...yData));
        this.ctx.strokeStyle = '#3B82F6'; this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        xData.forEach((x, i) => {
            const cx = margin + x * scale, cy = this.canvas.height - margin - yData[i] * scale;
            i === 0 ? this.ctx.moveTo(cx, cy) : this.ctx.lineTo(cx, cy);
        });
        this.ctx.stroke();
        const idx = Math.floor(this.animationProgress);
        if (idx < xData.length) {
            const cx = margin + xData[idx] * scale, cy = this.canvas.height - margin - yData[idx] * scale;
            this.ctx.fillStyle = '#EF4444'; this.ctx.beginPath(); this.ctx.arc(cx, cy, 8, 0, 2 * Math.PI); this.ctx.fill();
            const angle = Math.atan2(-vy[idx], vx[idx]);
            this.ctx.strokeStyle = '#10B981'; this.ctx.lineWidth = 2;
            this.ctx.beginPath(); this.ctx.moveTo(cx, cy); this.ctx.lineTo(cx + vx[idx] * 5, cy - vy[idx] * 5); this.ctx.stroke();
        }
    }

    play() { this.isPlaying = true; this._animate(); }
    pause() { this.isPlaying = false; cancelAnimationFrame(this.animationFrame); }
    restart() { this.animationProgress = 0; this.isPlaying = true; this._animate(); }

    _animate() {
        if (!this.isPlaying || !this.trajectoryData) return;
        this.animationProgress += this.playbackSpeed;
        if (this.animationProgress >= this.trajectoryData.x.length) { this.animationProgress = this.trajectoryData.x.length - 1; this.isPlaying = false; }
        this._drawTrajectory();
        if (this.isPlaying) this.animationFrame = requestAnimationFrame(() => this._animate());
    }

    reset() {
        this.pause(); this.animationProgress = 0; this.trajectoryData = null; this._drawInitialCanvas();
        ['velocity-slider', 'velocity-input'].forEach(id => document.getElementById(id).value = 20);
        ['angle-slider', 'angle-input'].forEach(id => document.getElementById(id).value = 45);
        ['drag-slider', 'drag-input'].forEach(id => document.getElementById(id).value = 0.3);
        ['time-slider', 'time-input'].forEach(id => document.getElementById(id).value = 10);
        this._updateAngleDisplay(45);
        document.getElementById('projectile-stats').innerHTML = '';
        showNotification('Reset complete', 'info');
    }

}
