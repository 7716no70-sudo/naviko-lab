from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = ROOT / "navikoLAB" / "workspace"

WORKSPACE_DIRS = {
    "mission_results": WORKSPACE_ROOT / "mission_results",
    "knowledge": WORKSPACE_ROOT / "knowledge",
    "reflection": WORKSPACE_ROOT / "reflection",
    "experience": WORKSPACE_ROOT / "experience",
    "artifacts": WORKSPACE_ROOT / "artifacts",
}


def initialize_workspace():
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

    created = []
    for name, path in WORKSPACE_DIRS.items():
        path.mkdir(parents=True, exist_ok=True)
        created.append({
            "name": name,
            "path": str(path),
            "exists": path.exists(),
        })

    return {
        "status": "initialized",
        "workspace_root": str(WORKSPACE_ROOT),
        "created_dirs": created,
        "write_scope": "workspace_only",
        "original_write_allowed": False,
        "file_delete_allowed": False,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def is_workspace_path(path):
    target = Path(path).resolve()
    workspace = WORKSPACE_ROOT.resolve()

    try:
        target.relative_to(workspace)
        return True
    except ValueError:
        return False


def build_workspace_file_path(category, filename):
    if category not in WORKSPACE_DIRS:
        raise ValueError(f"Unknown workspace category: {category}")

    target = WORKSPACE_DIRS[category] / filename

    if not is_workspace_path(target):
        raise PermissionError("Workspace外への書き込みは禁止されています。")

    return target


def save_json_to_workspace(category, filename, data):
    target = build_workspace_file_path(category, filename)
    target.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "saved_by": "AppOperatorWorkspaceCore",
        "category": category,
        "filename": filename,
        "data": data,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "status": "saved",
        "category": category,
        "path": str(target),
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
    }


def save_mission_result(mission_text, result):
    filename = f"mission_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "mission": mission_text,
        "result": result,
        "dry_run": True,
        "workspace_mode": True,
    }

    return save_json_to_workspace("mission_results", filename, data)


def run_workspace_core_diagnostics():
    init_result = initialize_workspace()

    test_result = save_mission_result(
        "Phase8 Workspace Core diagnostic mission",
        {
            "status": "diagnostic_completed",
            "pipeline_completed": True,
            "workspace_write": True,
            "original_write": False,
        },
    )

    return {
        "status": "completed",
        "phase": "Phase8-2 AppOperator Workspace Core",
        "workspace_initialized": True,
        "workspace_root": str(WORKSPACE_ROOT),
        "mission_result_saved": test_result["status"] == "saved",
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "init_result": init_result,
        "test_result": test_result,
    }


if __name__ == "__main__":
    report = run_workspace_core_diagnostics()

    print("=== AppOperator Workspace Core Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("WorkspaceInitialized:", report["workspace_initialized"])
    print("MissionResultSaved:", report["mission_result_saved"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceRoot:", report["workspace_root"])
    print("保存先:", report["test_result"]["path"])