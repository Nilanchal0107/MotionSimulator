# 🔧 frontend/scripts/utils/

This folder contains small, reusable **helper functions** used throughout the frontend JavaScript code.

These are not tied to any specific simulator — they handle common tasks like calling the API, showing loading icons, or formatting numbers.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `api.js` | A helper for making **API calls** to the backend. Instead of writing the same fetch() request code in every file, this provides a clean, reusable function. |
| `dom.js` | Helpers for **interacting with the HTML page** — like finding elements, updating text, or toggling visibility. DOM stands for "Document Object Model" — it's how JavaScript refers to the elements on the webpage. |
| `loading.js` | Shows and hides the **loading spinner** that appears while the simulation is running. |
| `notifications.js` | Displays **toast notifications** — small pop-up messages that appear briefly to tell the user something (e.g., "Simulation complete!" or "Error: invalid input"). |
| `format.js` | Formats **numbers for display** — for example, showing "9.81" instead of "9.810000000001" (rounding to a reasonable number of decimal places). |
| `download.js` | Lets the user **download graphs** as image files (e.g., PNG). |
| `tabs.js` | Handles switching between the **Projectile** and **Pendulum** tabs on the page. |

---

## 💡 Why Put These in a Separate Folder?

Each of these helpers is simple on its own, but they're used in many places across the app. Keeping them in `utils/` means:
- You only write the code once
- It's easy to find and fix if something breaks
- Each simulator script stays short and focused on its main job
