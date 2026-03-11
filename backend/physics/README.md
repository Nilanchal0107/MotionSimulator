# ⚙️ backend/physics/

This folder is the **math engine** of the simulator. It contains all the physics calculations that figure out *how objects move* over time.

No graphs are made here — this folder is purely about computing numbers (positions, velocities, angles) at each moment in time.

---

## 🗂️ What's Inside?

| Folder | What it simulates |
|---|---|
| `pendulum/` | The **double pendulum** — two swinging arms connected together. This is famous for its chaotic, unpredictable motion. |
| `projectile/` | **Projectile motion** — objects launched into the air, like a ball thrown or a cannonball fired. |

---

## 💡 What Does "Simulation" Mean Here?

Imagine you throw a ball at a certain speed and angle. Physics tells us exactly where that ball will be every fraction of a second. This folder does that math — step by tiny step — and returns a full list of positions and speeds over time.

These numbers are then handed off to the `visualizations/` folder to be turned into pretty graphs.

---

## 🔬 Technique Used

Both simulations use a method called **ODE solving** (Ordinary Differential Equations). This is a fancy way of saying: "given the laws of physics and a starting state, calculate what happens next, and the moment after that, and after that..."

Don't worry if this sounds complex — the code handles it all for you!
