# phase_watcher.py

class PhaseWatcher:

    def check(self, snapshot):
        phase = snapshot.get("phase")
        risk = snapshot.get("risk_level", 0)

        issues = []

        # Phase異常
        if phase == "unknown":
            issues.append("PHASE_UNKNOWN")

        # リスク過多
        if risk >= 3:
            issues.append("HIGH_RISK")

        # 停滞チェック（簡易）
        if snapshot.get("pending_adoption", 0) > 10:
            issues.append("QUEUE_OVERFLOW")

        return {
            "status": "OK" if not issues else "WARN",
            "issues": issues
        }