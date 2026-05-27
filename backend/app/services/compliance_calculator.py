class ComplianceCalculator:
    """
    Evaluate telemetry data and generate compliance score.
    """

    def evaluate_temperature(self, temp):
        if temp is None:
            return "UNKNOWN"

        if 2 <= temp <= 8:
            return "PASS"

        return "FAIL"

    def calculate_score(self, telemetry):

        checks = []

        # Temperature check
        checks.append(self.evaluate_temperature(telemetry.temp))

        # You can expand later (humidity, CO2, etc.)

        total = len(checks)
        passed = checks.count("PASS")

        score = (passed / total) * 100 if total else 0

        # Final status
        if score == 100:
            status = "EXCELLENT"
        elif score >= 70:
            status = "SATISFACTORY"
        else:
            status = "FAIL"

        return {
            "score": round(score, 2),
            "status": status
        }