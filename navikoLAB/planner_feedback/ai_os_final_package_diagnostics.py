from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
PACKAGE_DIR = WORKSPACE_DIR / "ai_os_final_package"

PACKAGE_PATH = PACKAGE_DIR / "ai_os_final_package.json"
OUTPUT_PATH = PACKAGE_DIR / "ai_os_final_package_diagnostics.json"

REQUIRED_KEYS = [
    "status",
    "phase",
    "Project",
    "PackageStatus",
    "SourceFound",
    "SourceCount",
    "MissingSourceCount",
    "AIOSStabilityReady",
    "FinalPipeline",
    "SafetyPolicy",
    "RiskCount",
    "SafeToContinue",
    "CollectedSources",
]

REQUIRED_SAFETY = {
    "WorkspaceOnly": True,
    "OriginalWrite": False,
    "PlannerWriteAllowed": False,
    "CapabilityRouterWriteAllowed": False,
    "ConnectorDispatcherWriteAllowed": False,
    "AutoPatch": False,
    "FileDelete": False,
    "ExternalOperation": False,
    "RealGUIOperation": False,
    "HumanApprovalRequired": True,
    "PermissionPolicyRequired": True,
    "ReadOnlyReference": True,
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    package_found = PACKAGE_PATH.exists()
    package = load_json(PACKAGE_PATH) if package_found else {}

    missing_keys = [key for key in REQUIRED_KEYS if key not in package]

    safety = package.get("SafetyPolicy", {})
    safety_mismatches = {
        key: {
            "expected": expected,
            "actual": safety.get(key),
        }
        for key, expected in REQUIRED_SAFETY.items()
        if safety.get(key) != expected
    }

    diagnostics_ok = (
        package_found
        and not missing_keys
        and not safety_mismatches
        and package.get("PackageStatus") == "built"
        and package.get("SourceFound") is True
        and package.get("SourceCount", 0) >= 14
        and package.get("MissingSourceCount") == 0
        and package.get("AIOSStabilityReady") is True
        and package.get("RiskCount") == 0
        and package.get("SafeToContinue") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase21-3 AI OS Final Package Diagnostics",
        "PackageFound": package_found,
        "RequiredKeysOK": len(missing_keys) == 0,
        "MissingKeys": missing_keys,
        "SafetyPolicyOK": len(safety_mismatches) == 0,
        "SafetyMismatches": safety_mismatches,
        "PackageStatusOK": package.get("PackageStatus") == "built",
        "SourceFound": package.get("SourceFound") is True,
        "SourceCountOK": package.get("SourceCount", 0) >= 14,
        "MissingSourceCountOK": package.get("MissingSourceCount") == 0,
        "AIOSStabilityReady": package.get("AIOSStabilityReady") is True,
        "WorkspaceOnly": safety.get("WorkspaceOnly") is True,
        "OriginalWrite": safety.get("OriginalWrite") is False,
        "HumanApprovalRequired": safety.get("HumanApprovalRequired") is True,
        "PermissionPolicyRequired": safety.get("PermissionPolicyRequired") is True,
        "FileDelete": safety.get("FileDelete") is True,
        "ExternalOperation": safety.get("ExternalOperation") is True,
        "RealGUIOperation": safety.get("RealGUIOperation") is True,
        "RiskCount": 0 if diagnostics_ok else 1,
        "SafeToContinue": diagnostics_ok,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== AI OS Final Package Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"RequiredKeysOK: {result['RequiredKeysOK']}")
    print(f"SafetyPolicyOK: {result['SafetyPolicyOK']}")
    print(f"PackageStatusOK: {result['PackageStatusOK']}")
    print(f"SourceFound: {result['SourceFound']}")
    print(f"SourceCountOK: {result['SourceCountOK']}")
    print(f"MissingSourceCountOK: {result['MissingSourceCountOK']}")
    print(f"AIOSStabilityReady: {result['AIOSStabilityReady']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()