/**
 * File Download Utilities
 * Functions to trigger browser file downloads.
 */

/**
 * Download plain text or CSV content as a file.
 * @param {string} content - File content string
 * @param {string} filename - Suggested filename
 * @param {string} [mimeType='text/plain'] - MIME type
 */
function downloadFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Download a base64-encoded PNG image.
 * @param {string} base64DataUri - Data URI string from server
 * @param {string} filename - Suggested filename
 */
function downloadBase64Image(base64DataUri, filename) {
    const a = document.createElement('a');
    a.href = base64DataUri;
    a.download = filename;
    a.click();
}
