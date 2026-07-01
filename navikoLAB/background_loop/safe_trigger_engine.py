# safe_trigger_engine.py

class SafeTriggerEngine:

    def evaluate(self, snapshot, phase_report):
        risk = snapshot.get("risk_level", 0)

        if snapshot.get("external_operation"):
            return "BLOCK"

        if snapshot.get("original_write"):
            return "BLOCK"

        if risk >= 2:
            return "WAIT_HUMAN"

        if phase_report.get("status") == "WARN":
            return "WAIT_HUMAN"

        return "ALLOW"