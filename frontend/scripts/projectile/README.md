# 🎯 frontend/scripts/projectile/

This folder contains the **JavaScript code that powers the Projectile Motion simulation tab** on the webpage.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `simulator.js` | The **main projectile simulator script**. It reads the user's input (launch speed, angle, air drag, etc.), sends them to the backend API (`/api/projectile/analyze`), and displays the returned graphs. It also handles the "Find Optimal Angle" button and preset loading. |

---

## 💡 What Happens When You Click "Launch Projectile"?

1. `simulator.js` collects the values the user entered (e.g., speed = 25 m/s, angle = 45°).
2. It shows a loading indicator.
3. It sends a **fetch request** to the backend with those values.
4. The backend runs the physics and sends back graphs (trajectory, velocity, height, energy, etc.).
5. `simulator.js` displays those graphs on the page.
6. If the user enabled air resistance, an additional **air resistance comparison** chart is shown.

The "Find Optimal Angle" feature sends a separate request to `/api/projectile/optimal_angle` and shows which angle achieves the greatest range.
