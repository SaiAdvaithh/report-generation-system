from influxdb_client import InfluxDBClient
from app.models.telemetry import Telemetry

# Acts like a data access layer
#CLEAN ARCHITECTURE - Controller -> Service -> Repository -. Database

class InfluxRepository:

    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket

    def get_latest_telemetry(self, container_id):

        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r["_measurement"] == "container_telemetry")
        |> filter(fn: (r) => r["container_id"] == "{container_id}")
        |> last()
        '''
        # print("QUERY:", query)
        query_api = self.client.query_api()
        result = query_api.query(query)

        telemetry_data = {}

        for table in result:
            for record in table.records:
                telemetry_data[record.get_field()] = record.get_value()

        telemetry = Telemetry(
            temp=telemetry_data.get("temp"),
            humidity=telemetry_data.get("humidity"),
            co2=telemetry_data.get("co2"),
            nh3=telemetry_data.get("nh3"),
            vibration=telemetry_data.get("vibration"),
            battery=telemetry_data.get("battery"),
            lat=telemetry_data.get("lat"),
            lon=telemetry_data.get("lon")
        )

        return telemetry

    def get_telemetry_history(self, container_id):

        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "container_telemetry")
        |> filter(fn: (r) => r["container_id"] == "{container_id}")
        |> filter(fn: (r) => r["_field"] == "temp")
        '''

        tables = self.client.query_api().query(query)

        data = []

        for table in tables:
            for record in table.records:
                data.append((record.get_time(), record.get_value()))

        return data
    
    def get_telemetry_by_date_range(self, container_id, start_date, end_date):

        start_ts = start_date
        end_ts = end_date

        query = f"""
        from(bucket: "{self.bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r["_measurement"] == "container_telemetry")
        |> filter(fn: (r) => r["container_id"] == "{container_id}")
        """
        tables = self.client.query_api().query(query)

        data = {}

        for table in tables:
            for record in table.records:
                time = record.get_time()
                field = record.get_field()
                value = record.get_value()

                if time not in data:
                    data[time] = {}

                data[time][field] = value

        # Convert to structured list
        structured_data = []

        for time, values in data.items():
            structured_data.append({
                "time": time,
                "temp": values.get("temp"),
                "humidity": values.get("humidity"),
                "co2": values.get("co2"),
                "nh3": values.get("nh3"),
                "battery": values.get("battery"),
            })

        return structured_data
        



