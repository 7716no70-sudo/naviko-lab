from navikoLAB.bridge.original_bridge_manager import OriginalBridgeManager
from navikoLAB.bridge.pipeline_bridge import PipelineBridge


def run_bridge_diagnostics():
    manager = OriginalBridgeManager()

    for name in manager.bridges:
        manager.register_bridge(name)

    pipeline = PipelineBridge()
    test_result = pipeline.transfer_pipeline({
        "mission": {"goal": "diagnostic mission"},
        "knowledge": {"summary": "diagnostic knowledge"},
        "reflection": {"result": "diagnostic reflection"},
        "improvement": {"proposal": "diagnostic improvement"},
    })

    status = manager.get_status()

    checks = {
        "MissionBridge": status["bridges"]["mission"],
        "KnowledgeBridge": status["bridges"]["knowledge"],
        "ReflectionBridge": status["bridges"]["reflection"],
        "ImprovementBridge": status["bridges"]["improvement"],
        "PipelineBridge": status["bridges"]["pipeline"],
        "Version": bool(status["version"]),
        "Safety_DirectWriteFalse": test_result["direct_write"] is False,
        "Safety_AutoApplyFalse": test_result["auto_apply"] is False,
        "Safety_HumanApprovalRequired": test_result["human_approval_required"] is True,
        "Connection": test_result["status"] == "pipeline_transferred",
    }

    passed = sum(1 for v in checks.values() if v)
    failed = len(checks) - passed

    return {
        "status": "passed" if failed == 0 else "failed",
        "check_count": len(checks),
        "passed": passed,
        "failed": failed,
        "checks": checks,
        "manager_status": status,
    }


if __name__ == "__main__":
    result = run_bridge_diagnostics()

    print("=== Bridge Diagnostics ===")
    print("状態:", result["status"])
    print("確認項目:", result["check_count"])
    print("通過:", result["passed"])
    print("失敗:", result["failed"])

    for name, ok in result["checks"].items():
        print(f"- {name}: {'OK' if ok else 'NG'}")