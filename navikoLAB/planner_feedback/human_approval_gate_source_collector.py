from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"

ADOPTION_DIR = WORKSPACE_DIR / "human_approved_original_adoption"
GATE_DIR = WORKSPACE_DIR / "human_approval_gate"
GATE_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    ADOPTION_DIR / "human_approved_original_adoption_completion_report.json",
]

OUTPUT_PATH = GATE_DIR / "human_approval_gate_source.json"

def load_json_safe(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"load_error": str(e)}

def main():
    collected = {}
    missing = []

    for path in REQUIRED_FILES:
        data = load_json_safe(path)
        if data is None:
            missing.append(str(path))
        else:
            collected[path.name] = data

    adoption = collected.get(
        "human_approved_original_adoption_completion_report.json", {}
    )

    result = {
        "status": "completed",
        "phase": "Phase26-1 Human Approval Gate Source Collector",
        "SourceCount": len(collected),
        "MissingSourceCount": len(missing),
        "MissingSources": missing,
        "AdoptionReadyForHumanApproval": adoption.get("AdoptionReadyForHumanApproval") is True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "AutoPatch": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": 0 if len(missing) == 0 else 1,
        "SafeToContinue": (
            len(missing) == 0
            and adoption.get("AdoptionReadyForHumanApproval") is True
            and adoption.get("RiskCount") == 0
            and adoption.get("SafeToContinue") is True
            and adoption.get("OriginalWrite") is False
            and adoption.get("OriginalWriteBlocked") is True
        ),
        "CollectedSources": collected,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approval Gate Source Collector ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"AdoptionReadyForHumanApproval: {result['AdoptionReadyForHumanApproval']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"HumanApproved: {result['HumanApproved']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {result['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {result['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()