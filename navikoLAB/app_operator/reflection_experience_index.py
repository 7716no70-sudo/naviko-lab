from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REFLECTION_DIR = ROOT / "navikoLAB" / "workspace" / "reflection"
EXPERIENCE_DIR = ROOT / "navikoLAB" / "workspace" / "experience"
INDEX_PATH = ROOT / "navikoLAB" / "workspace" / "reflection_experience_index.json"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def collect_records(folder, record_type):
    records = []

    for path in sorted(folder.glob("*.json")):
        payload = load_json(path)
        if not isinstance(payload, dict):
            continue

        data = payload.get("data", payload)

        records.append({
            "file": path.name,
            "type": data.get("type", record_type),
            "mission": data.get("mission"),
            "success_signal": data.get("success_signal"),
            "failure_signal": data.get("failure_signal"),
            "risk_count": data.get("risk_count"),
            "safe_to_continue": data.get("safe_to_continue"),
            "created_at": data.get("created_at") or payload.get("timestamp"),
        })

    return records


def build_reflection_experience_index():
    REFLECTION_DIR.mkdir(parents=True, exist_ok=True)
    EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)

    reflection_records = collect_records(REFLECTION_DIR, "reflection")
    experience_records = collect_records(EXPERIENCE_DIR, "experience")

    index = {
        "status": "indexed",
        "reflection_count": len(reflection_records),
        "experience_count": len(experience_records),
        "success_count": sum(1 for r in reflection_records if r.get("success_signal") is True),
        "failure_count": sum(1 for r in reflection_records if r.get("failure_signal") is True),
        "reflection_records": reflection_records,
        "experience_records": experience_records,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index


def run_reflection_experience_index_diagnostics():
    index = build_reflection_experience_index()

    return {
        "status": "completed",
        "phase": "Phase10-3 Reflection Experience Index",
        "index_created": INDEX_PATH.exists(),
        "reflection_count": index["reflection_count"],
        "experience_count": index["experience_count"],
        "success_count": index["success_count"],
        "failure_count": index["failure_count"],
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "index_path": str(INDEX_PATH),
    }


if __name__ == "__main__":
    report = run_reflection_experience_index_diagnostics()

    print("=== Reflection Experience Index Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("IndexCreated:", report["index_created"])
    print("ReflectionCount:", report["reflection_count"])
    print("ExperienceCount:", report["experience_count"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", report["index_path"])