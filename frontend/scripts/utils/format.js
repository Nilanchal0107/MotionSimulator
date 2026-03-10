/**
 * Number Formatting Utilities
 * Human-readable formatting for physics values.
 */

/**
 * Format a number to a fixed number of decimal places.
 * @param {number} value
 * @param {number} [decimals=2]
 * @returns {string}
 */
function formatNumber(value, decimals = 2) {
    if (value === null || value === undefined || isNaN(value)) return '—';
    return parseFloat(value).toFixed(decimals);
}

/**
 * Format a physics measurement with a unit suffix.
 * @param {number} value
 * @param {string} unit - e.g. 'm', 'm/s', '°'
 * @param {number} [decimals=2]
 * @returns {string}
 */
function formatPhysicsValue(value, unit, decimals = 2) {
    return `${formatNumber(value, decimals)} ${unit}`;
}
