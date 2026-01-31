import requests
import random
import time

# Replace with your server URL (local or Render)
URL = "http://localhost:5000/data"  # use your Render URL if online

sensors = ["SENSOR_1", "SENSOR_2", "SENSOR_3"]

while True:
    for sensor in sensors:
        value = round(random.uniform(20, 35), 1)  # simulate reading

        try:
            response = requests.post(URL, data={
                "sensor_id": sensor,
                "value": value
            })
            if response.status_code == 200:
                print(sensor, "sent:", value)
            else:
                print("Error sending", sensor, response.status_code)
        except Exception as e:
            print("Error connecting to server:", e)

    # Wait 10 seconds between readings (for testing, change to 1800 for 30 min)
    time.sleep(10)
