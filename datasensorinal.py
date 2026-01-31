import requests
import random
import time

URL = "https://iotsql-dashboard.onrender.com/data"
sensors = ["SENSOR_1", "SENSOR_2", "SENSOR_3"]

while True:
    for sensor in sensors:
        value = round(random.uniform(20, 35), 1)
        requests.post(URL, data={"sensor_id": sensor, "value": value})
        print(sensor, value)

    time.sleep(30)
