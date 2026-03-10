/**
 * Pendulum Simulator — Main Class
 * Orchestrates controls, API calls, canvas, trace, analysis, and export.
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
        this._setupControls();
        this._setupAnalysisTabs();
        this._loadPresets();
        this._drawInitialCanvas();
        this._drawInitialTrace();
    }

    _setupControls() {
        ['m1', 'm2', 'L1', 'L2', 'theta1', 'theta2', 'omega1', 'omega2', 'duration', 'damping'].forEach(name => {
            syncSliderInput(`${name}-slider`, `${name}-input`);
        });

        document.querySelectorAll('#pendulum-section .preset-btn[data-target="damping"]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('damping-slider').value = btn.dataset.value;
                document.getElementById('damping-input').value = btn.dataset.value;
            });
        });

        document.getElementById('simulate-pendulum').addEventListener('click', () => this.simulate());
        document.getElementById('reset-pendulum').addEventListener('click', () => this.reset());
        document.getElementById('play-pendulum').addEventListener('click', () => this.play());
        document.getElementById('pause-pendulum').addEventListener('click', () => this.pause());
        document.getElementById('restart-pendulum').addEventListener('click', () => this.restart());
        document.getElementById('clear-trace').addEventListener('click', () => this.clearTrace());

        document.getElementById('pendulum-speed').addEventListener('change', (e) => {
            this.playbackSpeed = parseFloat(e.target.value);
        });

        document.getElementById('pendulum-presets').addEventListener('change', (e) => {
            this._loadPresetScenario(e.target.value);
        });
    }

    _setupAnalysisTabs() {
        const tabs = document.querySelectorAll('.pendulum-tabs .analysis-tab');
        const views = document.querySelectorAll('#pendulum-section .analysis-view');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.analysis;
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                views.forEach(v => v.classList.toggle('active', v.id.includes(target)));
            });
        });
    }

    async _loadPresets() {
        try {
            const result = await apiRequest('/api/presets/pendulum');
            const select = document.getElementById('pendulum-presets');
            for (const [key, preset] of Object.entries(result.presets)) {
                const opt = document.createElement('option');
                opt.value = key; opt.textContent = preset.name; select.appendChild(opt);
            }
        } catch (e) { console.error('Failed to load presets:', e); }
    }

    _loadPresetScenario(presetKey) {
        if (!presetKey) return;
        apiRequest('/api/presets/pendulum').then(result => {
            const p = result.presets[presetKey];
            if (!p) return;
            const map = { m1: 'm1', m2: 'm2', L1: 'L1', L2: 'L2', theta1: 'theta1', theta2: 'theta2', omega1: 'omega1', omega2: 'omega2', t_max: 'duration', fps: 'fps', damping: 'damping' };
            Object.entries(map).forEach(([key, name]) => {
                const s = document.getElementById(`${name}-slider`);
                const i = document.getElementById(`${name}-input`);
                const sel = document.getElementById(`${name}-select`);
                if (s && i) { s.value = p[key]; i.value = p[key]; }
                else if (sel) sel.value = p[key];
            });
            showNotification(`Loaded: ${p.name}`, 'success');
        });
    }

    _getParameters() {
        const gravitySelect = document.getElementById('pend-gravity-select');
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
            fps: parseInt(document.getElementById('fps-select').value),
            damping: parseFloat(document.getElementById('damping-input').value || '0'),
            gravity_preset: gravitySelect ? gravitySelect.value : 'earth'
        };
    }

    async simulate() {
        showLoadingIndicator('pendulum-loading');
        try {
            const result = await apiRequest('/api/pendulum/analyze', 'POST', this._getParameters());
            if (result.status === 'success') {
                this.trajectoryData = result.trajectory;
                this._displayGraphs(result.graphs);
                this._displayStatistics(result.trajectory);
                this.currentFrame = 0; this.tracePoints = [];
                this.clearTrace(); this._drawPendulum();
                showNotification('Simulation completed!', 'success');
            }
        } catch (e) { console.error('Simulation failed:', e); }
        finally { hideLoadingIndicator('pendulum-loading'); }
    }

    _displayGraphs(graphs) {
        const map = {
            angles: 'pendulum-graph-angles', angular_velocity: 'pendulum-graph-velocity',
            phase_space: 'pendulum-graph-phase', energy: 'pendulum-graph-energy',
            frequency: 'pendulum-graph-frequency', heatmap: 'pendulum-graph-heatmap'
        };
        Object.entries(map).forEach(([key, id]) => {
            if (graphs[key]) document.getElementById(id).src = graphs[key];
        });
    }

    _displayStatistics(trajectory) {
        const stats = [
            { label: 'Max θ₁', value: `${formatNumber(trajectory.max_theta1_deg)}°` },
            { label: 'Max θ₂', value: `${formatNumber(trajectory.max_theta2_deg)}°` },
            { label: 'Max ω₁', value: `${formatNumber(trajectory.max_omega1)} rad/s` },
            { label: 'Max ω₂', value: `${formatNumber(trajectory.max_omega2)} rad/s` },
            { label: 'Rotations 1', value: trajectory.rotations1 },
            { label: 'Rotations 2', value: trajectory.rotations2 },
            { label: 'Energy Error', value: `${formatNumber(trajectory.energy_error_percent, 4)}%` },
        ];
        const div = document.getElementById('pendulum-stats');
        div.innerHTML = stats.map(s => `<div class="stat-item"><strong>${s.label}:</strong> ${s.value}</div>`).join('');
    }

    _drawInitialCanvas() {
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.beginPath(); this.ctx.arc(this.canvas.width / 2, 100, 6, 0, 2 * Math.PI); this.ctx.fill();
    }

    _drawInitialTrace() {
        this.traceCtx.fillStyle = '#FFFFFF';
        this.traceCtx.fillRect(0, 0, this.traceCanvas.width, this.traceCanvas.height);
    }

    _drawPendulum() {
        if (!this.trajectoryData) return;
        const data = this.trajectoryData;
        const frame = Math.floor(this.currentFrame);
        if (frame >= data.t.length) return;

        const cx = this.canvas.width / 2, cy = 100, scale = 150;
        this.ctx.fillStyle = '#000000'; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const x1 = cx + data.x1[frame] * scale, y1 = cy - data.y1[frame] * scale;
        const x2 = cx + data.x2[frame] * scale, y2 = cy - data.y2[frame] * scale;

        // Trail
        const start = Math.max(0, frame - this.trailLength);
        this.ctx.strokeStyle = 'rgba(255,215,0,0.3)'; this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        for (let i = start; i <= frame; i++) {
            const tx = cx + data.x2[i] * scale, ty = cy - data.y2[i] * scale;
            i === start ? this.ctx.moveTo(tx, ty) : this.ctx.lineTo(tx, ty);
        }
        this.ctx.stroke();

        // Arms
        this.ctx.strokeStyle = '#FFFFFF'; this.ctx.lineWidth = 3;
        this.ctx.beginPath(); this.ctx.moveTo(cx, cy); this.ctx.lineTo(x1, y1); this.ctx.stroke();
        this.ctx.beginPath(); this.ctx.moveTo(x1, y1); this.ctx.lineTo(x2, y2); this.ctx.stroke();

        // Bobs
        this.ctx.fillStyle = '#EF4444'; this.ctx.strokeStyle = '#FFFFFF'; this.ctx.lineWidth = 2;
        this.ctx.beginPath(); this.ctx.arc(x1, y1, 15, 0, 2 * Math.PI); this.ctx.fill(); this.ctx.stroke();
        this.ctx.fillStyle = '#3B82F6';
        this.ctx.beginPath(); this.ctx.arc(x2, y2, 12, 0, 2 * Math.PI); this.ctx.fill(); this.ctx.stroke();

        // Pivot
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.beginPath(); this.ctx.arc(cx, cy, 6, 0, 2 * Math.PI); this.ctx.fill();

        // Time display
        const td = document.getElementById('pendulum-time');
        if (td) td.textContent = `T: ${formatNumber(data.t[frame])}s`;

        this._updateTrace(x2, y2);
    }

    _updateTrace(x2, y2) {
        const traceScale = this.traceCanvas.width / this.canvas.width;
        const tcx = this.traceCanvas.width / 2, tcy = this.traceCanvas.height / 2;
        const tx = tcx + (x2 - this.canvas.width / 2) * traceScale;
        const ty = tcy + (y2 - 100) * traceScale;
        const hue = (this.currentFrame / this.trajectoryData.t.length) * 360;
        this.traceCtx.fillStyle = `hsl(${hue},80%,50%)`;
        this.traceCtx.beginPath(); this.traceCtx.arc(tx, ty, 2, 0, 2 * Math.PI); this.traceCtx.fill();
    }

    clearTrace() {
        this.traceCtx.fillStyle = '#FFFFFF';
        this.traceCtx.fillRect(0, 0, this.traceCanvas.width, this.traceCanvas.height);
        this.tracePoints = [];
    }

    play() { this.isPlaying = true; this._animate(); }
    pause() { this.isPlaying = false; cancelAnimationFrame(this.animationFrame); }
    restart() { this.currentFrame = 0; this.clearTrace(); this.isPlaying = true; this._animate(); }

    _animate() {
        if (!this.isPlaying || !this.trajectoryData) return;
        this.currentFrame += this.playbackSpeed;
        if (this.currentFrame >= this.trajectoryData.t.length) { this.currentFrame = this.trajectoryData.t.length - 1; this.isPlaying = false; }
        this._drawPendulum();
        if (this.isPlaying) this.animationFrame = requestAnimationFrame(() => this._animate());
    }

    reset() {
        this.pause(); this.currentFrame = 0; this.trajectoryData = null;
        this._drawInitialCanvas(); this.clearTrace();
        ['m1', 'm2', 'L1', 'L2'].forEach(n => { document.getElementById(`${n}-slider`).value = 1; document.getElementById(`${n}-input`).value = 1; });
        ['theta1', 'theta2'].forEach(n => { document.getElementById(`${n}-slider`).value = 90; document.getElementById(`${n}-input`).value = 90; });
        ['omega1', 'omega2'].forEach(n => { document.getElementById(`${n}-slider`).value = 0; document.getElementById(`${n}-input`).value = 0; });
        document.getElementById('duration-slider').value = 20; document.getElementById('duration-input').value = 20;
        document.getElementById('pendulum-stats').innerHTML = '';
        showNotification('Reset complete', 'info');
    }

}
