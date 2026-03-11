# 🌐 backend/api/

This folder contains the **API routes** — think of these as the **doors** the frontend knocks on to request a simulation.

When the user clicks "Simulate" on the webpage, the frontend sends a message to one of these routes, which then runs the physics math and sends back the results.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `pendulum.py` | Handles requests for the **double pendulum** simulation. The frontend sends pendulum settings (mass, length, angle, etc.), and this file coordinates the physics and graph generation. |
| `projectile.py` | Handles requests for **projectile motion** (e.g. throwing a ball). It also has an endpoint to find the **best launch angle** for maximum range. |
| `presets.py` | Returns **pre-built example settings** (like "Golf Drive" or "Chaotic Pendulum") so users can explore quickly without typing everything manually. Also provides gravity settings for different planets. |
| `__init__.py` | A small file that tells Python "this folder is a package." You normally don't need to edit this. |

---

## 💡 How Does an API Route Work?

1. The **frontend** sends a request to a URL like `/api/pendulum/analyze` along with some data (e.g. the pendulum's mass and length).
2. The **route function** in this folder receives that data.
3. It calls the physics engine to simulate the motion.
4. It calls the visualization code to create graphs.
5. It sends everything back to the frontend as a response.

It's like ordering food at a restaurant — you (frontend) give the order to the waiter (API), who takes it to the kitchen (physics engine), and brings back the meal (charts).
