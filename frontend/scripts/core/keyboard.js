/**
 * Keyboard Shortcuts
 * Space = Play/Pause, R = Restart, 1 = Projectile tab, 2 = Pendulum tab.
 */

document.addEventListener('keydown', (e) => {
    // Ignore when focus is inside an input field
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    switch (e.key) {
        case ' ':
        case 'Spacebar':
            e.preventDefault();
            toggleActiveSimulator();
            break;
        case 'r':
        case 'R':
            restartActiveSimulator();
            break;
        case '1':
            switchTab('projectile');
            break;
        case '2':
            switchTab('pendulum');
            break;
    }
});

function toggleActiveSimulator() {
    const activeTab = document.querySelector('.tab-btn.active');
    if (!activeTab) return;
    const type = activeTab.dataset.tab;
    const playBtn = document.getElementById(`play-${type}`);
    const pauseBtn = document.getElementById(`pause-${type}`);
    if (playBtn && pauseBtn) {
        const isPlaying = pauseBtn.disabled === false;
        isPlaying ? pauseBtn.click() : playBtn.click();
    }
}

function restartActiveSimulator() {
    const activeTab = document.querySelector('.tab-btn.active');
    if (!activeTab) return;
    const restartBtn = document.getElementById(`restart-${activeTab.dataset.tab}`);
    if (restartBtn) restartBtn.click();
}

function switchTab(tabName) {
    const btn = document.querySelector(`.tab-btn[data-tab="${tabName}"]`);
    if (btn) btn.click();
}
