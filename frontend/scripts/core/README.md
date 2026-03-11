# 🧱 frontend/scripts/core/

This folder contains **core utilities** that are shared across both the pendulum and projectile simulators.

These are features that affect the whole app, not just one simulation type.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `keyboard.js` | Adds **keyboard shortcuts** to the app. For example, pressing a key might trigger a simulation or switch tabs — no need to always click with the mouse. |
| `url_state.js` | Saves the **current simulation settings into the URL** (the web address). This means you can copy and share the URL with someone, and they'll open the app with the exact same settings loaded automatically. |

---

## 💡 Why Are These "Core"?

These features work across the whole application regardless of whether you're on the projectile or pendulum tab. Instead of duplicating their code in both simulator scripts, they're placed here and shared.

- **Keyboard shortcuts** = power-user convenience
- **URL state** = easy sharing and bookmarking of simulations
