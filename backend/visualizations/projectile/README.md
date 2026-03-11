# 📉 backend/visualizations/projectile/

This folder creates all the **graphs and charts** shown on the projectile motion tab of the webpage.

Each file draws one specific type of chart about the object's flight.

---

## 🗂️ Files in this Folder

| File | Chart it creates |
|---|---|
| `trajectory.py` | **Trajectory Arc** — the classic parabolic (curved) path of the object through the air. |
| `velocity.py` | **Velocity Components** — shows the horizontal speed (stays mostly constant) and vertical speed (changes due to gravity) over time. |
| `height.py` | **Height vs. Time** — how high the object is at each second of its flight. |
| `energy.py` | **Energy Analysis** — shows kinetic energy (speed energy) and potential energy (height energy) throughout the flight. Their total should stay roughly the same. |
| `optimal_angle.py` | **Optimal Angle Curve** — draws a curve showing how the range changes with different launch angles. Highlights the best angle to achieve maximum distance. |
| `air_resistance.py` | **Air Resistance Comparison** — draws two trajectories side by side: one with air drag, one without. Great for seeing how much air slows things down. |
| `__init__.py` | Tells Python this is a package. You don't need to edit this. |

---

## 💡 Real-World Connection

These are the same types of graphs that aerospace engineers and sports scientists use! For example, a golf coach might use an optimal angle chart to help players improve their drives.
