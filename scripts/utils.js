/**
 * Utility Functions
 * Shared helper functions for the physics simulator
 */

// Debounce function to limit API calls
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Format numbers with specified decimals
function formatNumber(value, decimals = 2) {
    return parseFloat(value).toFixed(decimals);
}

// Format physics values with units
function formatPhysicsValue(value, unit) {
    return `${formatNumber(value)} ${unit}`;
}

// Show loading indicator
function showLoadingIndicator(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'flex';
    }
}

// Hide loading indicator
function hideLoadingIndicator(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.textContent = message;
    notification.className = 'notification';
    notification.classList.add('show', type);

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Download file
function downloadFile(data, filename, type) {
    const blob = new Blob([data], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Download base64 image
function downloadBase64Image(base64Data, filename) {
    const link = document.createElement('a');
    link.href = base64Data;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Sync slider and input
function syncSliderInput(sliderId, inputId, callback) {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);

    if (!slider || !input) return;

    slider.addEventListener('input', () => {
        input.value = slider.value;
        if (callback) callback(parseFloat(slider.value));
    });

    input.addEventListener('input', () => {
        slider.value = input.value;
        if (callback) callback(parseFloat(input.value));
    });
}

// API request helper
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'API request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// Create statistics display
function createStatsDisplay(stats) {
    const statsGrid = document.createElement('div');
    statsGrid.className = 'stats-grid';

    for (const [key, value] of Object.entries(stats)) {
        const statCard = document.createElement('div');
        statCard.className = 'stat-card';

        const label = document.createElement('div');
        label.className = 'stat-label';
        label.textContent = key;

        const valueEl = document.createElement('div');
        valueEl.className = 'stat-value';
        valueEl.textContent = value;

        statCard.appendChild(label);
        statCard.appendChild(valueEl);
        statsGrid.appendChild(statCard);
    }

    return statsGrid;
}

// Setup analysis tabs
function setupAnalysisTabs(tabsSelector, viewsSelector) {
    const tabs = document.querySelectorAll(tabsSelector);
    const views = document.querySelectorAll(viewsSelector);

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetAnalysis = tab.dataset.analysis;

            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active view
            views.forEach(view => {
                if (view.id.includes(targetAnalysis)) {
                    view.classList.add('active');
                } else {
                    view.classList.remove('active');
                }
            });
        });
    });
}
