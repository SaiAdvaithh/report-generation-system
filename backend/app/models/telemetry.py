class Telemetry:

    def __init__(self, temp, humidity, co2, nh3, vibration, battery, lat, lon):
        self.temp = temp
        self.humidity = humidity
        self.co2 = co2
        self.nh3 = nh3
        self.vibration = vibration
        self.battery = battery
        self.lat = lat
        self.lon = lon