# 📈 backend/visualizations/pendulum/

This folder creates all the **graphs and charts** shown on the pendulum simulation tab of the webpage.

Each file here is responsible for drawing one specific type of chart.

---

## 🗂️ Files in this Folder

| File | Chart it creates |
|---|---|
| `angles.py` | **Angle vs. Time** — shows how the angle of each pendulum arm changes over time. You can see if the motion is regular or chaotic. |
| `angular_velocity.py` | **Angular Velocity vs. Time** — shows how fast each arm is spinning at each moment. |
| `phase_space.py` | **Phase Space Plot** — draws angle vs. angular velocity. A regular pendulum makes a neat loop; a chaotic one makes a tangled mess. |
| `energy.py` | **Energy Conservation** — shows the kinetic energy, potential energy, and total energy over time. In a perfect simulation, total energy should stay constant. |
| `frequency.py` | **Frequency Spectrum** — shows which frequencies (oscillation speeds) appear in the pendulum's motion. |
| `heatmap.py` | **Position Heatmap** — a color map showing where the pendulum tip spends the most time. Bright areas = visited often. |
| `chaos.py` | **Chaos / Divergence Plot** — shows how two nearly identical pendulums drift apart over time, demonstrating chaos. |
| `__init__.py` | Tells Python this is a package. You don't need to edit this. |

---

## 💡 Which Chart Is Most Interesting?

The **Phase Space Plot** and **Position Heatmap** are the most visually striking. When the pendulum is chaotic, these charts look like beautiful, tangled art!
