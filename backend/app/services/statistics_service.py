class StatisticsService:
    
    #Compute statistics for telemetry data.
    def calculate_temperature_stats(self, history):
        if not history:
            return None

        temps = [d["temp"] for d in history if d.get("temp") is not None]

        return {
            "min_temp": min(temps),
            "max_temp": max(temps),
            "avg_temp": sum(temps) / len(temps)
        }