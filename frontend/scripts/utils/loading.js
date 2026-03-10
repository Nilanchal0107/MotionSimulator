/**
 * Loading Indicator Helpers
 * Show/hide spinner overlays by element ID.
 */

/**
 * Show a loading indicator element.
 * @param {string} elementId - ID of the loading container
 */
function showLoadingIndicator(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = 'flex';
}

/**
 * Hide a loading indicator element.
 * @param {string} elementId - ID of the loading container
 */
function hideLoadingIndicator(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = 'none';
}
