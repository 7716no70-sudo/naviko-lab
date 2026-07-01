class SelfRepairEngine:

    def __init__(self):

        self.repair_log = []

    # ■ メイン修復処理
    def repair(self, snapshot, memory, identity, conflict, execution):

        issues = self._detect_issues(
            snapshot,
            memory,
            identity,
            conflict,
            execution
        )

        if not issues:
            return {
                "status": "stable",
                "repairs": []
            }

        repaired_state = {
            "goals": snapshot.get("goals"),
            "memory_mode": "normal",
            "execution_mode": "normal",
            "identity_mode": identity,
            "conflict_status": conflict.get("status", "stable")
        }

        repairs = []

        for issue in issues:

            if issue["type"] == "MEMORY_CORRUPTION":
                repaired_state["memory_mode"] = "rebuild"
                repairs.append("memory_rebuild")

            if issue["type"] == "EXECUTION_LOOP_ERROR":
                repaired_state["execution_mode"] = "safe_mode"
                repairs.append("execution_safe_mode")

            if issue["type"] == "GOAL_INSTABILITY":
                repaired_state["goals"] = self._stabilize_goals(snapshot.get("goals", []))
                repairs.append("goal_stabilization")

            if issue["type"] == "IDENTITY_DRIFT":
                repaired_state["identity_mode"] = "recalibrate"
                repairs.append("identity_recalibration")

        result = {
            "status": "repaired",
            "issues": issues,
            "repairs": repairs,
            "state": repaired_state
        }

        self.repair_log.append(result)

        return result

    # ■ 問題検知
    def _detect_issues(self, snapshot, memory, identity, conflict, execution):

        issues = []

        # ■ memory破損検知
        if memory.latest() is None or len(str(memory.latest())) < 3:
            issues.append({
                "type": "MEMORY_CORRUPTION",
                "severity": "high"
            })

        # ■ execution異常
        if execution and execution.get("status") == "error":
            issues.append({
                "type": "EXECUTION_LOOP_ERROR",
                "severity": "high"
            })

        # ■ goal不安定
        goals = snapshot.get("goals", [])
        if isinstance(goals, list) and len(goals) == 0:
            issues.append({
                "type": "GOAL_INSTABILITY",
                "severity": "medium"
            })

        # ■ identity drift
        if identity["personality"]["stability"] < 0.3:
            issues.append({
                "type": "IDENTITY_DRIFT",
                "severity": "medium"
            })

        return issues

    # ■ goal修復
    def _stabilize_goals(self, goals):

        if not goals:
            return [
                "improve_stability",
                "maintain_execution",
                "restore_memory"
            ]

        return goals[:3]