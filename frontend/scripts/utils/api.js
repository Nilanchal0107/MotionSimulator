/**
 * API Request Utility
 * Single function for all fetch calls to the Flask backend.
 */

/**
 * Make a JSON API request.
 * @param {string} url - Endpoint path (e.g. '/api/projectile/analyze')
 * @param {string} method - HTTP method, default 'GET'
 * @param {object|null} body - JSON body for POST requests
 * @returns {Promise<object>} Parsed JSON response
 */
async function apiRequest(url, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(url, options);
    if (!response.ok) {
        const err = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(err.message || 'API request failed');
    }
    return response.json();
}
