from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
ROUTER_DIR = BASE_DIR / "external_ai"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase87-2 External AI Permission Diagnostics"

ROUTER_PATH = BASE_DIR / "external_ai_permission_router.json"
REGISTRY_PATH = ROUTER_DIR / "external_ai_provider_registry.json"

REQUIRED_KNOWN_PROVIDERS = [
    "chatgpt",
    "groq",
    "claude",
    "gemini",
]

REQUIRED_UNKNOWN_PROVIDERS = [
    "unknown_ai",
]

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_diagnostics():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router = load_json(ROUTER_PATH)
    registry = load_json(REGISTRY_PATH)

    router_found = router is not None
    registry_found = registry is not None

    results = router.get("results", []) if router_found else []
    providers = registry.get("providers", {}) if registry_found else {}

    result_by_provider = {
        r.get("provider"): r for r in results
    }

    missing_known = [
        provider for provider in REQUIRED_KNOWN_PROVIDERS
        if provider not in result_by_provider
    ]

    missing_unknown = [
        provider for provider in REQUIRED_UNKNOWN_PROVIDERS
        if provider not in result_by_provider
    ]

    known_providers_registered = all(
        provider in providers
        for provider in REQUIRED_KNOWN_PROVIDERS
    )

    known_providers_ok = (
        len(missing_known) == 0
        and all(
            result_by_provider[p].get("provider_known") is True
            and result_by_provider[p].get("approval_required") is True
            and result_by_provider[p].get("allowed") is False
            and result_by_provider[p].get("blocked") is True
            and result_by_provider[p].get("SafeToExecute") is False
            for p in REQUIRED_KNOWN_PROVIDERS
        )
    )

    unknown_providers_ok = (
        len(missing_unknown) == 0
        and all(
            result_by_provider[p].get("provider_known") is False
            and result_by_provider[p].get("denied") is True
            and result_by_provider[p].get("allowed") is False
            and result_by_provider[p].get("blocked") is True
            and result_by_provider[p].get("SafeToExecute") is False
            for p in REQUIRED_UNKNOWN_PROVIDERS
        )
    )

    router_summary_ok = (
        router_found
        and router.get("ExternalAIPermissionRouterCreated") is True
        and router.get("ExternalAIProviderRegistrySaved") is True
        and router.get("AllKnownProvidersApprovalRequired") is True
        and router.get("AllUnknownProvidersDenied") is True
        and router.get("ExternalAIPermissionRouterUsedForAll") is True
        and router.get("PolicyRequiredForAll") is True
        and router.get("CapabilityPermissionRequiredForAll") is True
        and router.get("PermissionLayerRequiredForAll") is True
        and router.get("ExternalCommunicationExecuted") is False
        and router.get("HumanApproved") is False
        and router.get("OriginalWrite") is False
        and router.get("ExternalOperation") is False
        and router.get("BrowserOperation") is False
        and router.get("RealGUIOperation") is False
        and router.get("FileDelete") is False
    )

    diagnostics_passed = (
        router_found
        and registry_found
        and known_providers_registered
        and known_providers_ok
        and unknown_providers_ok
        and router_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "ExternalAIRouterFound": router_found,
        "ExternalAIRegistryFound": registry_found,
        "RequiredKnownProviderCount": len(REQUIRED_KNOWN_PROVIDERS),
        "RequiredUnknownProviderCount": len(REQUIRED_UNKNOWN_PROVIDERS),
        "MissingKnownProviderCount": len(missing_known),
        "MissingUnknownProviderCount": len(missing_unknown),
        "MissingKnownProviders": missing_known,
        "MissingUnknownProviders": missing_unknown,
        "KnownProvidersRegistered": known_providers_registered,
        "KnownProvidersApprovalRequiredOK": known_providers_ok,
        "UnknownProvidersDeniedOK": unknown_providers_ok,
        "RouterSummaryOK": router_summary_ok,
        "ExternalAIPermissionDiagnosticsPassed": diagnostics_passed,
        "ExternalCommunicationExecuted": False,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase87-3 External AI Permission Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"external_ai_permission_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "external_ai_permission_diagnostics.json"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return report, report_path

def main():
    report, report_path = build_diagnostics()

    print("=== External AI Permission Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"ExternalAIRouterFound: {report['ExternalAIRouterFound']}")
    print(f"ExternalAIRegistryFound: {report['ExternalAIRegistryFound']}")
    print(f"RequiredKnownProviderCount: {report['RequiredKnownProviderCount']}")
    print(f"RequiredUnknownProviderCount: {report['RequiredUnknownProviderCount']}")
    print(f"MissingKnownProviderCount: {report['MissingKnownProviderCount']}")
    print(f"MissingUnknownProviderCount: {report['MissingUnknownProviderCount']}")
    print(f"KnownProvidersRegistered: {report['KnownProvidersRegistered']}")
    print(f"KnownProvidersApprovalRequiredOK: {report['KnownProvidersApprovalRequiredOK']}")
    print(f"UnknownProvidersDeniedOK: {report['UnknownProvidersDeniedOK']}")
    print(f"RouterSummaryOK: {report['RouterSummaryOK']}")
    print(f"ExternalAIPermissionDiagnosticsPassed: {report['ExternalAIPermissionDiagnosticsPassed']}")
    print(f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()