from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

# ------------------------------
# Database setup
# ------------------------------
conn = sqlite3.connect("sensors.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT,
    date TEXT,
    time TEXT,
    value REAL
)
""")
conn.commit()

# ------------------------------
# Receive data from sensors
# ------------------------------
@app.route("/data", methods=["POST"])
def receive_data():
    sensor_id = request.form.get("sensor_id")
    value = float(request.form.get("value"))

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_ = now.strftime("%H:%M:%S")

    cursor.execute(
        "INSERT INTO readings (sensor_id, date, time, value) VALUES (?, ?, ?, ?)",
        (sensor_id, date, time_, value)
    )
    conn.commit()

    return "OK", 200

# ------------------------------
# Dashboard
# ------------------------------
@app.route("/")
def homepage():
    cursor.execute("SELECT sensor_id, date, time, value FROM readings ORDER BY sensor_id, date, time")
    rows = cursor.fetchall()

    data_store = {}
    for sensor_id, date, time_, value in rows:
        key = (sensor_id, date)
        if key not in data_store:
            data_store[key] = []
        data_store[key].append((time_, value))

    return render_template("dash.html", data_store=data_store)

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
