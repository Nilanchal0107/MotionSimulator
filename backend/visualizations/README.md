# 📊 backend/visualizations/

This folder turns **raw numbers into charts and graphs** that the user can see on the webpage.

After the physics engine calculates positions, velocities, and energies over time, this folder takes those numbers and draws them as visual plots using a Python library called **Matplotlib**.

---

## 🗂️ What's Inside?

| Folder | What it visualizes |
|---|---|
| `pendulum/` | Charts for the **double pendulum**: angles over time, energy, phase space, frequency, heatmap, etc. |
| `projectile/` | Charts for **projectile motion**: trajectory arc, velocity components, height over time, energy, air resistance comparison. |
| `base.py` | A shared helper that handles the common steps every graph needs — like setting the style, saving the image, and converting it to a format the browser can display. |

---

## 💡 How Does a Graph Get From Here to the Browser?

1. A physics value (e.g., list of angles over time) is passed into a function like `plot_angle_vs_time(trajectory)`.
2. Matplotlib draws the graph into memory.
3. The graph is converted into a **base64-encoded image string** (a way to send an image as text).
4. That string is sent back to the frontend, which displays it inside an `<img>` tag on the page.

No image files are saved on the server — everything is generated on the fly!
