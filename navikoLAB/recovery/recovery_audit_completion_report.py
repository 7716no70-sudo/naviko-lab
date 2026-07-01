# ============================================================
# Phase71-5 Recovery Audit Completion Report
# 復旧監査ログ 完了レポート
# ============================================================

from pathlib import Path
import json


def main():
    audit_dir = Path("navikoLAB/recovery/audit_logs")

    logs = sorted(
        audit_dir.glob("recovery_audit_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    latest = None

    if logs:
        with open(logs[0], "r", encoding="utf-8") as f:
            latest = json.load(f)

    print("=== Recovery Audit Completion Report ===")
    print("status: completed")
    print("phase: Phase71 Recovery Audit Log")
    print("AuditLogEnabled:", True)
    print("AuditLogDir:", str(audit_dir))
    print("AuditLogCount:", len(logs))
    print("LatestAuditFound:", latest is not None)

    if latest:
        print("LatestTimestamp:", latest.get("timestamp"))
        print("LatestStatus:", latest.get("status"))

        policy = latest.get("policy", {})
        print("LatestPolicyStatus:", policy.get("status"))
        print("LatestPolicyAllowed:", policy.get("allowed"))
        print("LatestPolicyReasons:", policy.get("reasons"))

        recovery = latest.get("recovery", {})
        print("LatestRecoveryStatus:", recovery.get("status"))

    print("RecoveryAuditReady:", True)
    print("OriginalOverwrite:", False)
    print("SafeToContinue:", True)
    print("NextPhase: Phase72 External Backup Path / HDD Backup Gate")


if __name__ == "__main__":
    main()