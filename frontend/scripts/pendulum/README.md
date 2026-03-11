# 🔄 frontend/scripts/pendulum/

This folder contains the **JavaScript code that powers the Pendulum simulation tab** on the webpage.

---

## 🗂️ Files in this Folder

| File | What it does |
|---|---|
| `simulator.js` | The **main pendulum simulator script**. It reads the user's input values (mass, length, angles, etc.), sends them to the backend API (`/api/pendulum/analyze`), and then displays the returned graphs on the page. It also handles preset loading and error messages. |

---

## 💡 What Happens When You Click "Simulate Pendulum"?

1. `simulator.js` reads all the values the user typed (e.g., mass = 1kg, angle = 120°).
2. It shows a loading spinner so the user knows something is happening.
3. It sends those values to the backend using a **fetch request** (a way for JavaScript to talk to a server).
4. The backend runs the physics simulation and sends back 6 graphs.
5. `simulator.js` takes those graphs and drops them onto the page for the user to see.
6. If something went wrong, it shows an error message.

It's like a messenger between the user and the physics engine.
