class SystemHealth:

    def __init__(
        self,
        temp_status,
        humidity_status,
        co2_status,
        nh3_status,
        vibration_status,
        compliance_pct,
        mqtt_status,
        data_quality,
        uptime_days,
        active_critical,
        last_incident
    ):
        self.temp_status = temp_status
        self.humidity_status = humidity_status
        self.co2_status = co2_status
        self.nh3_status = nh3_status
        self.vibration_status = vibration_status
        self.compliance_pct = compliance_pct
        self.mqtt_status = mqtt_status
        self.data_quality = data_quality
        self.uptime_days = uptime_days
        self.active_critical = active_critical
        self.last_incident = last_incident