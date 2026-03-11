# 📦 backend/

This is the **brain** of the Physics Motion Simulator.

It is written in **Python** using a framework called **Flask**, which lets us create a web server that the frontend (the webpage you see) can ask questions to — like "simulate a pendulum with these settings" — and get answers back.

---

## 🗂️ What's Inside?

| Folder / File | What it does |
|---|---|
| `app.py` | The **starting point** of the backend. It starts the web server and connects everything together. |
| `api/` | Contains the **API routes** — the URLs the frontend talks to (e.g. `/api/pendulum/analyze`). |
| `physics/` | Contains the actual **physics calculations** — the math that simulates how objects move. |
| `utils/` | Contains small **helper tools**, like checking if the user's input is valid. |
| `visualizations/` | Contains code that turns raw physics data into **charts and graphs**. |
| `requirements.txt` | A list of all the Python **libraries** this project needs to be installed. |
| `runtime.txt` | Tells the server which **Python version** to use. |

---

## 🚀 How to Run the Backend

1. Make sure you have Python installed.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open your browser and go to: `http://localhost:5000`

---

## 💡 Simple Analogy

Think of the backend like a **calculator hidden behind the scenes**. The user types in values on the webpage (frontend), the backend does all the math, and sends charts back to display.
