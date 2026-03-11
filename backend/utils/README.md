# 🛠️ backend/utils/

This folder contains small, reusable **helper tools** that are used across the entire backend.

Think of these as the **toolbox** — they don't do the main work themselves, but they support everything else.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `validation.py` | **Checks and cleans** the input sent by the user. For example, it makes sure the angle is a number, the mass is positive, and no required field is missing. If something is wrong, it raises an error with a helpful message. |
| `gravity.py` | Provides **gravity values** for different planets (Earth = 9.81, Moon = 1.62, Mars = 3.72, etc.). Also reads the user's choice of planet from their request. |
| `caching.py` | **Saves the result** of a simulation so if the user asks for the exact same settings again, the server doesn't have to recalculate everything — it just returns the saved result instantly. This makes the app faster. |
| `__init__.py` | Tells Python this is a package. You don't need to edit this. |

---

## 💡 Why Are These Separate?

Instead of copy-pasting the same validation or caching code into every file, we put it here once. Any part of the backend can import and use it. This keeps the code **clean, short, and easy to change**.

This principle is called **DRY** (Don't Repeat Yourself) — a core idea in good software development.
