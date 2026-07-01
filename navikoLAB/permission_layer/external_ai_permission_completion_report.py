from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase87-3 External AI Permission Completion Report"

ROUTER_PATH = BASE_DIR / "external_ai_permission_router.json"
DIAGNOSTICS_PATH = BASE_DIR / "external_ai_permission_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router = load_json(ROUTER_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    router_found = router is not None
    diagnostics_found = diagnostics is not None

    router_completed = router_found and router.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    router_created = (
        router_found
        and router.get("ExternalAIPermissionRouterCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("ExternalAIPermissionDiagnosticsPassed") is True
    )

    known_providers_ok = (
        diagnostics_found
        and diagnostics.get("KnownProvidersApprovalRequiredOK") is True
    )

    unknown_providers_ok = (
        diagnostics_found
        and diagnostics.get("UnknownProvidersDeniedOK") is True
    )

    router_summary_ok = (
        diagnostics_found
        and diagnostics.get("RouterSummaryOK") is True
    )

    external_communication_blocked = (
        diagnostics_found
        and diagnostics.get("ExternalCommunicationExecuted") is False
    )

    completed = (
        router_completed
        and diagnostics_completed
        and router_created
        and diagnostics_passed
        and known_providers_ok
        and unknown_providers_ok
        and router_summary_ok
        and external_communication_blocked
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "ExternalAIRouterFound": router_found,
        "DiagnosticsFound": diagnostics_found,
        "ExternalAIRouterCompleted": router_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "ExternalAIPermissionRouterCreated": router_created,
        "ExternalAIPermissionDiagnosticsPassed": diagnostics_passed,
        "KnownProvidersApprovalRequiredOK": known_providers_ok,
        "UnknownProvidersDeniedOK": unknown_providers_ok,
        "RouterSummaryOK": router_summary_ok,
        "ExternalCommunicationExecuted": False,
        "ExternalAICompletionConfirmed": completed,
        "KnownProviders": [
            "chatgpt",
            "groq",
            "claude",
            "gemini",
        ],
        "UnknownProvidersDenied": True,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase88 Browser Permission",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"external_ai_permission_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "external_ai_permission_completion_report.json"
    txt_path = BASE_DIR / "external_ai_permission_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== External AI Permission Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"ExternalAIRouterFound: {report['ExternalAIRouterFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"ExternalAIRouterCompleted: {report['ExternalAIRouterCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"ExternalAIPermissionRouterCreated: {report['ExternalAIPermissionRouterCreated']}",
        f"ExternalAIPermissionDiagnosticsPassed: {report['ExternalAIPermissionDiagnosticsPassed']}",
        f"KnownProvidersApprovalRequiredOK: {report['KnownProvidersApprovalRequiredOK']}",
        f"UnknownProvidersDeniedOK: {report['UnknownProvidersDeniedOK']}",
        f"RouterSummaryOK: {report['RouterSummaryOK']}",
        f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}",
        f"ExternalAICompletionConfirmed: {report['ExternalAICompletionConfirmed']}",
        f"HumanApproved: {report['HumanApproved']}",
        f"Mode: {report['Mode']}",
        f"RiskCount: {report['RiskCount']}",
        f"SafeToContinue: {report['SafeToContinue']}",
        f"NextPhase: {report['NextPhase']}",
        f"保存先: {report_path}",
    ]

    txt_path.write_text("\n".join(lines), encoding="utf-8")

    return lines

def main():
    for line in build_report():
        print(line)

if __name__ == "__main__":
    main()