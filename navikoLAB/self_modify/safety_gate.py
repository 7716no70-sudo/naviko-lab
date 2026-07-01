# safety_gate.py


class SafetyGate:

    def validate(self, behavior):

        # ■ 絶対禁止条件
        if behavior.get("risk_threshold", 0) < 0:
            return False

        if behavior.get("loop_speed", 1) < 0.1:
            return False

        return True