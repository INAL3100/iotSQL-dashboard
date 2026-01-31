from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

# ------------------------------
# ZONE → SENSOR MAPPING
# ------------------------------
ZONES = {
    "Zone 1": ["SENSOR_1"],
    "Zone 2": ["SENSOR_2"],
    "Zone 3": ["SENSOR_3"]
}

# ------------------------------
# DATABASE SETUP
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
# RECEIVE SENSOR DATA
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
# DASHBOARD
# ------------------------------
@app.route("/")
def homepage():
    selected_sensor = request.args.get("sensor")
    selected_date = request.args.get("date")

    query = "SELECT sensor_id, date, time, value FROM readings WHERE 1=1"
    params = []

    if selected_sensor:
        query += " AND sensor_id = ?"
        params.append(selected_sensor)

    if selected_date:
        query += " AND date = ?"
        params.append(selected_date)

    query += " ORDER BY sensor_id, date, time"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    data_store = {}
    for sensor_id, date, time_, value in rows:
        key = (sensor_id, date)
        data_store.setdefault(key, []).append((time_, value))

    return render_template(
        "dashboard.html",
        data_store=data_store,
        zones=ZONES,
        selected_sensor=selected_sensor,
        selected_date=selected_date
    )

# ------------------------------
# RUN SERVER
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
