import requests
import random
import time

URL = "http://127.0.0.1:5000/data"  # or your deployed URL

sensors = ["SENSOR_1", "SENSOR_2", "SENSOR_3"]

while True:
    for sensor in sensors:
        value = round(random.uniform(20, 35), 1)

        try:
            response = requests.post(URL, data={
                "sensor_id": sensor,
                "value": value
            })
            print(sensor, "sent:", value)
        except Exception as e:
            print("Error sending data:", e)

    time.sleep(10)  # 10 sec for testing, change to 1800 for 30 min
