# 🖥️ frontend/

This folder contains everything the **user sees and interacts with** in their browser.

It is built using plain **HTML, CSS, and JavaScript** — no special framework needed. The frontend is the visual face of the application.

---

## 🗂️ What's Inside?

| File / Folder | What it does |
|---|---|
| `index.html` | The **main webpage**. This is the single HTML file that contains the entire user interface — both the projectile and pendulum simulator tabs. |
| `styles/` | Contains the **CSS file** (`main.css`) that makes the page look good — colors, layout, fonts, animations. |
| `scripts/` | Contains all the **JavaScript files** that make the page interactive — sending requests to the backend, showing graphs, handling user clicks, etc. |

---

## 💡 How the Frontend Works

1. The user opens `index.html` in their browser.
2. They enter values (e.g., launch angle, pendulum mass) and click "Simulate".
3. The JavaScript in `scripts/` sends those values to the backend server via an API call.
4. The backend calculates the physics and returns graphs.
5. The JavaScript displays those graphs on the page.

The frontend **never does any physics calculations itself** — it just sends requests and shows results.

---

## 🎨 Design

The page is designed to be clean, responsive, and easy to use. It works on both desktop and smaller screens.
