/**
 * DOM Synchronisation Utilities
 * Keeps paired slider + number-input elements in sync.
 */

/**
 * Synchronise a range slider and a number input so changes to either
 * are reflected in the other.
 * @param {string} sliderId  - ID of the <input type="range">
 * @param {string} inputId   - ID of the <input type="number">
 * @param {Function} [onChange] - Optional callback fired with the new value
 */
function syncSliderInput(sliderId, inputId, onChange) {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);
    if (!slider || !input) return;

    slider.addEventListener('input', () => {
        input.value = slider.value;
        if (onChange) onChange(slider.value);
    });

    input.addEventListener('input', () => {
        slider.value = input.value;
        if (onChange) onChange(input.value);
    });
}

/**
 * Simple debounce wrapper.
 * @param {Function} fn - Function to debounce
 * @param {number} delay - Milliseconds to wait
 * @returns {Function} Debounced function
 */
function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}
