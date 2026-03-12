/**
 * lightbox.js
 * Full-screen lightbox with pan & zoom.
 *
 * Supports:
 *  - <img class="graph-image">    → click any analysis graph to open
 *  - <canvas id="projectile-canvas"> + <canvas id="pendulum-canvas">
 *        → a small "⛶ Fullscreen" button appears on hover / tap
 *
 * Controls inside lightbox:
 *  - Mouse wheel / trackpad     → zoom in / out (towards cursor)
 *  - Click + drag               → pan
 *  - Double-click               → reset zoom & pan
 *  - Esc / click dark backdrop  → close
 */

(function () {
    'use strict';

    /* ─── State ──────────────────────────────────────────────────────────── */
    let lb      = null;   // overlay element
    let lbImg   = null;   // <img> inside lightbox
    let scale   = 1;
    let ox      = 0;      // pan offset X
    let oy      = 0;      // pan offset Y
    let dragging     = false;
    let lastX        = 0;
    let lastY        = 0;
    const MIN_SCALE  = 0.3;
    const MAX_SCALE  = 10;

    /* ─── Transform helpers ──────────────────────────────────────────────── */
    function applyTransform() {
        lbImg.style.transform = `translate(${ox}px, ${oy}px) scale(${scale})`;
    }

    function resetTransform() {
        scale = 1; ox = 0; oy = 0;
        if (lbImg) applyTransform();
    }

    /* ─── Close ──────────────────────────────────────────────────────────── */
    function closeLightbox() {
        if (!lb) return;
        // Remove global listeners added per-session
        document.removeEventListener('keydown', onKeyDown);
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup',  onMouseUp);
        lb.remove();
        lb = lbImg = null;
        dragging = false;
    }

    /* ─── Event handlers ─────────────────────────────────────────────────── */
    function onKeyDown(e) {
        if (e.key === 'Escape') closeLightbox();
    }

    function onWheel(e) {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
        const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale * factor));

        // Zoom toward the cursor position relative to lightbox centre
        const rect = lbImg.getBoundingClientRect();
        const cx = rect.left + rect.width  / 2;
        const cy = rect.top  + rect.height / 2;
        ox += (e.clientX - cx) * (1 - newScale / scale);
        oy += (e.clientY - cy) * (1 - newScale / scale);
        scale = newScale;
        applyTransform();
    }

    function onMouseDown(e) {
        if (e.button !== 0) return;
        if (e.target !== lbImg) return;
        e.preventDefault();
        dragging = true;
        lastX = e.clientX;
        lastY = e.clientY;
        lbImg.style.cursor = 'grabbing';
    }

    function onMouseMove(e) {
        if (!dragging) return;
        ox += e.clientX - lastX;
        oy += e.clientY - lastY;
        lastX = e.clientX;
        lastY = e.clientY;
        applyTransform();
    }

    function onMouseUp() {
        if (dragging) {
            dragging = false;
            if (lbImg) lbImg.style.cursor = 'grab';
        }
    }

    /* ─── Build & open lightbox ──────────────────────────────────────────── */
    function openLightbox(src, altText) {
        closeLightbox();
        resetTransform();

        /* Overlay */
        lb = document.createElement('div');
        lb.className = 'img-lightbox';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-modal', 'true');

        /* Close button */
        const closeBtn = document.createElement('button');
        closeBtn.className = 'img-lightbox-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.setAttribute('aria-label', 'Close lightbox');
        closeBtn.addEventListener('click', closeLightbox);

        /* Hint bar */
        const hint = document.createElement('div');
        hint.className = 'img-lightbox-hint';
        hint.textContent = 'Scroll to zoom · Drag to pan · Double-click to reset · Esc to close';

        /* Image */
        lbImg = document.createElement('img');
        lbImg.src = src;
        lbImg.alt = altText || 'Fullscreen view';
        lbImg.draggable = false;
        lbImg.style.cssText = 'cursor:grab;user-select:none;transform-origin:center center;transition:none;max-width:92vw;max-height:90vh;object-fit:contain;border-radius:8px';

        lb.appendChild(closeBtn);
        lb.appendChild(lbImg);
        lb.appendChild(hint);
        document.body.appendChild(lb);

        /* Click backdrop → close */
        lb.addEventListener('click', (e) => { if (e.target === lb) closeLightbox(); });

        /* Double-click image → reset */
        lb.addEventListener('dblclick', (e) => {
            if (e.target === lbImg) { e.stopPropagation(); resetTransform(); }
        });

        /* Zoom */
        lb.addEventListener('wheel', onWheel, { passive: false });

        /* Pan start */
        lb.addEventListener('mousedown', onMouseDown);

        /* Pan move & end — on document so we don't lose the drag */
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup',  onMouseUp);

        /* Keyboard */
        document.addEventListener('keydown', onKeyDown);

        /* ── Touch: pinch-zoom + drag ── */
        let lastDist  = null;
        let lastTX    = null;
        let lastTY    = null;

        lb.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                lastDist = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
            } else if (e.touches.length === 1) {
                lastTX = e.touches[0].clientX;
                lastTY = e.touches[0].clientY;
            }
        }, { passive: true });

        lb.addEventListener('touchmove', (e) => {
            e.preventDefault();
            if (e.touches.length === 2 && lastDist) {
                const d = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
                scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale * (d / lastDist)));
                lastDist = d;
                applyTransform();
            } else if (e.touches.length === 1 && lastTX !== null) {
                ox += e.touches[0].clientX - lastTX;
                oy += e.touches[0].clientY - lastTY;
                lastTX = e.touches[0].clientX;
                lastTY = e.touches[0].clientY;
                applyTransform();
            }
        }, { passive: false });

        lb.addEventListener('touchend', () => {
            lastDist = lastTX = lastTY = null;
        }, { passive: true });
    }

    /* ─── Helper: canvas → data URL ──────────────────────────────────────── */
    function canvasSnapshot(canvas) {
        try { return canvas.toDataURL('image/png'); }
        catch (e) { return null; }
    }

    /* ─── Attach to graph images ─────────────────────────────────────────── */
    function attachToImage(img) {
        if (img._lbAttached) return;
        img._lbAttached = true;
        img.style.cursor = 'zoom-in';
        img.title = 'Click to open fullscreen';
        img.addEventListener('click', () => {
            // Only open if the image actually has a real src
            if (img.src && !img.src.endsWith(location.href)) {
                openLightbox(img.src, img.alt);
            }
        });
    }

    function attachToAllImages() {
        document.querySelectorAll('img.graph-image').forEach(attachToImage);
    }

    /* ─── Attach fullscreen button to simulation canvases ───────────────── */
    function makeFullscreenBtn(canvas) {
        const btn = document.createElement('button');
        btn.textContent = '⛶ Fullscreen';
        btn.title = 'Open in fullscreen with pan & zoom';
        Object.assign(btn.style, {
            position:       'absolute',
            bottom:         '10px',
            right:          '10px',
            zIndex:         '50',
            padding:        '6px 12px',
            background:     'rgba(2,62,138,0.82)',
            color:          '#fff',
            border:         'none',
            borderRadius:   '8px',
            fontSize:       '0.82rem',
            fontWeight:     '600',
            cursor:         'pointer',
            backdropFilter: 'blur(4px)',
            transition:     'opacity 0.2s',
            opacity:        '0',
            pointerEvents:  'auto',
        });

        const container = canvas.closest('.canvas-container') || canvas.parentElement;
        if (!container) return;

        // Make sure parent is positioned
        if (getComputedStyle(container).position === 'static') {
            container.style.position = 'relative';
        }
        container.appendChild(btn);

        // Show / hide on hover
        container.addEventListener('mouseenter', () => { btn.style.opacity = '1'; });
        container.addEventListener('mouseleave', () => { btn.style.opacity = '0'; });

        btn.addEventListener('click', () => {
            const src = canvasSnapshot(canvas);
            if (src) openLightbox(src, `${canvas.id} snapshot`);
        });
    }

    /* ─── Observe DOM for dynamically-added / updated images ────────────── */
    const observer = new MutationObserver(() => attachToAllImages());

    /* ─── Init ───────────────────────────────────────────────────────────── */
    function init() {
        attachToAllImages();

        // Simulation canvases
        ['projectile-canvas', 'pendulum-canvas'].forEach(id => {
            const canvas = document.getElementById(id);
            if (canvas) makeFullscreenBtn(canvas);
        });

        observer.observe(document.body, {
            childList:       true,
            subtree:         true,
            attributes:      true,
            attributeFilter: ['src'],
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
