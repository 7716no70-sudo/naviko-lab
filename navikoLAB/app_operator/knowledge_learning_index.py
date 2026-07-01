from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = ROOT / "navikoLAB" / "workspace" / "knowledge"
INDEX_PATH = KNOWLEDGE_DIR / "knowledge_learning_index.json"

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_index():
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.json")):
        if path.name == INDEX_PATH.name:
            continue

        payload = load_json(path)
        if not isinstance(payload, dict):
            continue

        data = payload.get("data", payload)

        records.append({
            "file": path.name,
            "mission": data.get("mission"),
            "type": data.get("type"),
            "pipeline_status": data.get("pipeline_status"),
            "pipeline_completed": data.get("pipeline_completed"),
            "safe_to_continue": data.get("safe_to_continue"),
            "risk_count": data.get("risk_count"),
            "created_at": data.get("created_at") or payload.get("timestamp"),
        })

    index = {
        "status": "indexed",
        "record_count": len(records),
        "records": records,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index

def run_knowledge_learning_index_diagnostics():
    index = build_index()

    return {
        "status": "completed",
        "phase": "Phase9-3 Knowledge Learning Index",
        "index_created": INDEX_PATH.exists(),
        "record_count": index["record_count"],
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "index_path": str(INDEX_PATH),
    }

if __name__ == "__main__":
    report = run_knowledge_learning_index_diagnostics()

    print("=== Knowledge Learning Index Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("IndexCreated:", report["index_created"])
    print("RecordCount:", report["record_count"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", report["index_path"])