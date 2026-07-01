# loop_guard.py


class LoopGuard:

    def check(self, snapshot):
        if snapshot.get("external_operation"):
            return "BLOCK"

        if snapshot.get("original_write"):
            return "BLOCK"

        if snapshot.get("risk_level", 0) >= 3:
            return "BLOCK"

        return "ALLOW"