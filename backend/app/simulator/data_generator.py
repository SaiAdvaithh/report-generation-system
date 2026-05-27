import time
import random
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime, timezone

# 🔑 Your InfluxDB details
url = "http://localhost:8086"
token = "kk2Me_2dj96jsoF2Bow3JkEBfk0V_wqPkogiCmnjDq-T-liultgLF3i0tx4Z3hjY1cZS1fNjKuYFJKXn3wwSRw=="
org = "Epic Logic Solutions"
bucket = "hardware_data"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()

def generate_data():
    return {
        "temperature": round(random.uniform(10, 45), 2),   # cold storage
        "humidity": round(random.uniform(60, 90), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }

while True:
    data = generate_data()

    point = (
        Point("container_telemetry")
        .tag("container_id", random.choice(["C001", "C002", "C003"]))
        .field("temp", data["temperature"])
        .field("humidity", data["humidity"])
        .field("co2", random.uniform(300, 600))
        .field("nh3", random.uniform(5, 20))
        .field("vibration", random.uniform(0, 5))
        .field("battery", random.uniform(20, 100))
        .field("lat", 12.9716)
        .field("lon", 77.5946)
         #.time(datetime.now(timezone.utc), WritePrecision.NS)
    )

    write_api.write(bucket=bucket, org=org, record=point)

    print(f"Inserted: {data}")

    time.sleep(10)  # every 10 seconds