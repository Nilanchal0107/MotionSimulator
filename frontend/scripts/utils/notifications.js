/**
 * Notification System
 * Shows transient toast messages in the bottom-right corner.
 */

/**
 * Display a notification toast.
 * @param {string} message - Text to display
 * @param {'success'|'error'|'warning'|'info'} [type='info']
 * @param {number} [duration=4000] - Auto-dismiss delay in ms
 */
function showNotification(message, type = 'info', duration = 4000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    const icons = { success: '✓', error: '✗', warning: '⚠', info: 'ℹ' };
    notification.textContent = `${icons[type] || ''} ${message}`;

    document.body.appendChild(notification);

    requestAnimationFrame(() => notification.classList.add('show'));

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}
