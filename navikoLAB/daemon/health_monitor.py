# health_monitor.py


class HealthMonitor:

    def analyze(self, snapshot):
        health = "OK"

        if snapshot.get("phase") == "unknown":
            health = "DEGRADED"

        if snapshot.get("pending_adoption", 0) > 10:
            health = "DEGRADED"

        if snapshot.get("risk_level", 0) >= 3:
            health = "CRITICAL"

        return health