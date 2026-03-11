# ⚡ frontend/scripts/

This folder contains all the **JavaScript files** that make the webpage interactive and dynamic.

JavaScript runs inside the user's browser and handles everything that happens after the page loads — like responding to button clicks, calling the backend, and displaying graphs.

---

## 🗂️ What's Inside?

| Folder | What it does |
|---|---|
| `core/` | **Core utilities** used by both simulators — keyboard shortcut handling and URL state management. |
| `pendulum/` | JavaScript that powers the **pendulum simulator** tab — collects input, calls the API, and shows the results. |
| `projectile/` | JavaScript that powers the **projectile simulator** tab — same idea but for projectile motion. |
| `utils/` | Small **helper functions** used throughout the frontend — showing loading spinners, displaying notifications, formatting numbers, etc. |

---

## 💡 How It All Fits Together

Think of the scripts folder like the **nervous system** of the webpage:
- `utils/` = the basic reflexes (small, reusable helpers)
- `pendulum/` and `projectile/` = the main actions (run simulation, show results)
- `core/` = the system-wide controls (keyboard shortcuts, shareable URL state)

When the user clicks "Simulate", the appropriate `simulator.js` file takes over, gathers the form values, calls the backend, and updates the page with the graphs it receives.
