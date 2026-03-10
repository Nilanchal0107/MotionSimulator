/**
 * URL State Persistence
 * Saves simulation parameters to the URL hash so users can share or bookmark runs.
 */

/** Gather current state from both simulators' controls into a flat object. */
function collectState() {
    const ids = [
        'velocity-input', 'angle-input', 'drag-input', 'time-input',
        'm1-input', 'm2-input', 'L1-input', 'L2-input',
        'theta1-input', 'theta2-input', 'omega1-input', 'omega2-input',
        'duration-input', 'damping-input'
    ];
    const state = {};
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el) state[id] = el.value;
    });
    return state;
}

/** Write current state to the URL hash (without triggering a navigation). */
function persistState() {
    const state = collectState();
    const hash = encodeURIComponent(JSON.stringify(state));
    history.replaceState(null, '', `#${hash}`);
}

/** Read state from URL hash and restore control values. */
function restoreState() {
    if (!location.hash) return;
    try {
        const state = JSON.parse(decodeURIComponent(location.hash.slice(1)));
        Object.entries(state).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) {
                el.value = value;
                // Also sync paired slider
                const sliderId = id.replace('-input', '-slider');
                const slider = document.getElementById(sliderId);
                if (slider) slider.value = value;
            }
        });
    } catch (_) { /* Malformed hash — ignore */ }
}

// Auto-persist on input changes
document.addEventListener('input', debounce(persistState, 500));

// Restore on page load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(restoreState, 50);
});

// Expose globally for other scripts
window.persistSimState = persistState;
