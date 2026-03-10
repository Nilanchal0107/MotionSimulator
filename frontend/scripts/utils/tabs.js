/**
 * Analysis Tabs Setup
 * Wires up generic tab groups (data-analysis / .analysis-view patterns).
 */

/**
 * Initialise a set of analysis tabs and their corresponding content panels.
 * @param {string} tabSelector   - CSS selector for tab buttons
 * @param {string} viewSelector  - CSS selector for content panels
 */
function setupAnalysisTabs(tabSelector, viewSelector) {
    const tabs = document.querySelectorAll(tabSelector);
    const views = document.querySelectorAll(viewSelector);

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.analysis;

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            views.forEach(view => {
                view.classList.toggle('active', view.id.includes(target));
            });
        });
    });
}
