# 🔄 backend/physics/pendulum/

This folder simulates the **double pendulum** — one of the most famous examples of **chaos** in physics. Even tiny changes in the starting position can lead to wildly different swinging paths.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `engine.py` | The core class `DoublePendulum`. It stores the physical properties (mass, length) and provides a function to compute the equations of motion. Think of it as the pendulum's "brain". |
| `solver.py` | Uses the engine's equations to **simulate time**. It runs the pendulum step-by-step and records the position and speed at each moment. |
| `fft.py` | Performs a **Frequency analysis** (FFT = Fast Fourier Transform). It figures out if the pendulum has any repeating patterns in its motion — like a hidden rhythm. |
| `heatmap.py` | Tracks *where* the pendulum tip spends the most time, creating data for a **position heatmap**. |
| `chaos.py` | Measures how **chaotic** the pendulum is by running two nearly identical simulations and seeing how fast they diverge (called the Lyapunov exponent). |
| `__init__.py` | Tells Python this is a package. You don't need to edit this. |

---

## 💡 What is a Double Pendulum?

Imagine a normal pendulum (like on a grandfather clock), but instead of a fixed weight at the end, there's **another pendulum attached**. This tiny change makes the motion extremely complex and unpredictable — a hallmark of **chaos theory**.
