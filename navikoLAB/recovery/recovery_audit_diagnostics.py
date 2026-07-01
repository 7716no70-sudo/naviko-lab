# ============================================================
# Phase71-3 Recovery Audit Diagnostics
# 復旧監査ログ診断
# ============================================================

from pathlib import Path
import json


def main():
    log_dir = Path("navikoLAB/recovery/audit_logs")

    logs = sorted(
        log_dir.glob("recovery_audit_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    print("=== Recovery Audit Diagnostics ===")
    print("log_dir:", str(log_dir))
    print("log_count:", len(logs))

    if not logs:
        print("latest_status:", "empty")
        return

    latest = logs[0]

    with open(latest, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("latest_status:", "found")
    print("latest_file:", str(latest))
    print("timestamp:", data.get("timestamp"))
    print("status:", data.get("status"))

    policy = data.get("policy", {})
    print("policy_status:", policy.get("status"))
    print("policy_allowed:", policy.get("allowed"))
    print("policy_reasons:", policy.get("reasons"))

    recovery = data.get("recovery", {})
    print("recovery_status:", recovery.get("status"))


if __name__ == "__main__":
    main()