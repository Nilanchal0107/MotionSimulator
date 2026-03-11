# 🏀 backend/physics/projectile/

This folder simulates **projectile motion** — what happens when you launch an object into the air (like a ball, a cannonball, or a soccer kick).

It calculates the full flight path, including the effect of **air resistance** if enabled.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `engine.py` | The core class `ProjectileMotion`. It stores the gravity setting and provides the equations for how the object accelerates and moves through the air. |
| `solver.py` | Simulates the full flight from launch to landing, step-by-step, and records height, speed, and position at each moment in time. |
| `optimal_angle.py` | Tries many different launch angles (from 0° to 90°) and finds which one gives the **maximum range** for a given speed and drag. |
| `compare.py` | Runs **two simulations** side by side: one with air resistance and one without. This lets us see exactly how much drag affects the flight. |
| `__init__.py` | Tells Python this is a package. You don't need to edit this. |

---

## 💡 What Affects Projectile Motion?

Three main things:
1. **Launch speed (v₀)** — faster means it goes farther.
2. **Launch angle** — 45° gives the maximum range in a vacuum (no air).
3. **Air resistance (drag)** — slows the object down, especially at high speeds.

This simulator lets you play with all three!
