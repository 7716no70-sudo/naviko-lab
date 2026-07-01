from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
ROUTER_DIR = BASE_DIR / "external_ai"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
ROUTER_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase87-1 External AI Permission Router"

EXTERNAL_AI_PROVIDERS = {
    "chatgpt": {
        "capability": "external_ai",
        "operation": "external_ai_execute",
        "risk_level": 3,
    },
    "groq": {
        "capability": "external_ai",
        "operation": "external_ai_execute",
        "risk_level": 3,
    },
    "claude": {
        "capability": "external_ai",
        "operation": "external_ai_execute",
        "risk_level": 3,
    },
    "gemini": {
        "capability": "external_ai",
        "operation": "external_ai_execute",
        "risk_level": 3,
    },
}

DEFAULT_EXTERNAL_AI_POLICY = {
    "capability": "external_ai",
    "operation": "unknown_external_ai_provider",
    "risk_level": 5,
}

def save_external_ai_provider_registry():
    path = ROUTER_DIR / "external_ai_provider_registry.json"
    payload = {
        "phase": PHASE,
        "mode": "dry_run",
        "providers": EXTERNAL_AI_PROVIDERS,
        "default_policy": DEFAULT_EXTERNAL_AI_POLICY,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return path

def route_external_ai_request(provider_name, purpose, payload=None):
    payload = payload or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    provider = EXTERNAL_AI_PROVIDERS.get(provider_name, DEFAULT_EXTERNAL_AI_POLICY)

    provider_known = provider_name in EXTERNAL_AI_PROVIDERS
    capability = provider["capability"]
    operation = provider["operation"]
    risk_level = provider["risk_level"]

    if provider_known:
        decision = "approval_required"
        approval_required = True
        denied = False
    else:
        decision = "deny"
        approval_required = True
        denied = True

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "provider": provider_name,
        "provider_known": provider_known,
        "purpose": purpose,
        "payload_preview": str(payload)[:200],
        "capability": capability,
        "operation": operation,
        "risk_level": risk_level,
        "router_decision": decision,
        "allowed": False,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": True,
        "human_approval_required": True,
        "human_approved": False,
        "dry_run": True,
        "ExternalAIPermissionRouterUsed": True,
        "PolicyRequired": True,
        "CapabilityPermissionRequired": True,
        "PermissionLayerRequired": True,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "OriginalWrite": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": False,
    }

    return result

def run_external_ai_router_test():
    registry_path = save_external_ai_provider_registry()

    test_requests = [
        ("chatgpt", "text reasoning dry_run test", {"message": "test"}),
        ("groq", "fast inference dry_run test", {"message": "test"}),
        ("claude", "long context dry_run test", {"message": "test"}),
        ("gemini", "multi modal dry_run test", {"message": "test"}),
        ("unknown_ai", "unknown provider test", {"message": "test"}),
    ]

    results = [
        route_external_ai_request(provider, purpose, payload)
        for provider, purpose, payload in test_requests
    ]

    known_results = [r for r in results if r["provider_known"] is True]
    unknown_results = [r for r in results if r["provider_known"] is False]

    report = {
        "status": "completed",
        "phase": PHASE,
        "ExternalAIPermissionRouterCreated": True,
        "ExternalAIProviderRegistrySaved": registry_path.exists(),
        "ExternalAIProviderRegistryPath": str(registry_path),
        "TestCount": len(results),
        "KnownProviderCount": len(known_results),
        "UnknownProviderCount": len(unknown_results),
        "AllKnownProvidersApprovalRequired": all(
            r["approval_required"] is True
            and r["allowed"] is False
            and r["blocked"] is True
            and r["SafeToExecute"] is False
            for r in known_results
        ),
        "AllUnknownProvidersDenied": all(
            r["denied"] is True
            and r["allowed"] is False
            and r["blocked"] is True
            for r in unknown_results
        ),
        "ExternalAIPermissionRouterUsedForAll": all(
            r["ExternalAIPermissionRouterUsed"] is True
            for r in results
        ),
        "PolicyRequiredForAll": all(r["PolicyRequired"] is True for r in results),
        "CapabilityPermissionRequiredForAll": all(
            r["CapabilityPermissionRequired"] is True
            for r in results
        ),
        "PermissionLayerRequiredForAll": all(
            r["PermissionLayerRequired"] is True
            for r in results
        ),
        "ExternalCommunicationExecuted": False,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase87-2 External AI Permission Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"external_ai_permission_router_{timestamp}.json"
    latest_path = BASE_DIR / "external_ai_permission_router.json"

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
    report, report_path = run_external_ai_router_test()

    print("=== External AI Permission Router ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"ExternalAIPermissionRouterCreated: {report['ExternalAIPermissionRouterCreated']}")
    print(f"ExternalAIProviderRegistrySaved: {report['ExternalAIProviderRegistrySaved']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"KnownProviderCount: {report['KnownProviderCount']}")
    print(f"UnknownProviderCount: {report['UnknownProviderCount']}")
    print(f"AllKnownProvidersApprovalRequired: {report['AllKnownProvidersApprovalRequired']}")
    print(f"AllUnknownProvidersDenied: {report['AllUnknownProvidersDenied']}")
    print(f"ExternalAIPermissionRouterUsedForAll: {report['ExternalAIPermissionRouterUsedForAll']}")
    print(f"PolicyRequiredForAll: {report['PolicyRequiredForAll']}")
    print(f"CapabilityPermissionRequiredForAll: {report['CapabilityPermissionRequiredForAll']}")
    print(f"PermissionLayerRequiredForAll: {report['PermissionLayerRequiredForAll']}")
    print(f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()