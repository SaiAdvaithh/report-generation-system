import matplotlib.pyplot as plt

class ChartGenerator:

    def generate_temperature_chart(self, data):

        # 🔥 SAFETY CHECK FIRST (IMPORTANT)
        if not data or len(data) < 2:
            return None

        # ✅ FIXED: Use dictionary keys
        times = [str(d["time"])[:19] for d in data]
        values = [d["temp"] for d in data]

        plt.figure()
        plt.plot(times, values, marker='o')

        plt.xticks(rotation=45)
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature Trend (Last 24h)")

        plt.tight_layout()

        file_path = "temp_chart.png"
        plt.savefig(file_path)
        plt.close()

        return file_path