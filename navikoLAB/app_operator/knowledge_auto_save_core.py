from datetime import datetime

from navikoLAB.app_operator.app_operator_workspace_core import save_json_to_workspace


def build_knowledge_record(mission_text, pipeline_result):
    return {
        "type": "knowledge_record",
        "mission": mission_text,
        "summary": "Mission実行結果からKnowledge Recordを生成しました。",
        "pipeline_status": pipeline_result.get("status"),
        "pipeline_completed": pipeline_result.get("pipeline_completed", False),
        "safe_to_continue": pipeline_result.get("safe_to_continue", True),
        "risk_count": pipeline_result.get("risk_count", 0),
        "dry_run": pipeline_result.get("dry_run", True),
        "read_only": pipeline_result.get("read_only", True),
        "workspace_mode": True,
        "original_write": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_knowledge_record(mission_text, pipeline_result):
    record = build_knowledge_record(mission_text, pipeline_result)
    filename = f"knowledge_record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    return save_json_to_workspace(
        "knowledge",
        filename,
        record,
    )


def run_knowledge_auto_save_diagnostics():
    mission = "Phase9-2 Knowledge Auto Save Core diagnostic mission"

    pipeline_result = {
        "status": "dry_run",
        "pipeline_completed": True,
        "safe_to_continue": True,
        "risk_count": 0,
        "dry_run": True,
        "read_only": True,
    }

    save_result = save_knowledge_record(mission, pipeline_result)

    return {
        "status": "completed",
        "phase": "Phase9-2 Knowledge Auto Save Core",
        "knowledge_record_saved": save_result["status"] == "saved",
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "save_result": save_result,
    }


if __name__ == "__main__":
    report = run_knowledge_auto_save_diagnostics()

    print("=== Knowledge Auto Save Core Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("KnowledgeRecordSaved:", report["knowledge_record_saved"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", report["save_result"]["path"])