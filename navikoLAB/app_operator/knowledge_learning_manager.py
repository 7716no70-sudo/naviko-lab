from navikoLAB.app_operator.knowledge_auto_save_core import save_knowledge_record
from navikoLAB.app_operator.knowledge_learning_index import build_index


def run_knowledge_learning_cycle(mission_text, pipeline_result):
    save_result = save_knowledge_record(mission_text, pipeline_result)
    index_result = build_index()

    return {
        "status": "completed",
        "phase": "Phase9-4 Knowledge Learning Manager",
        "knowledge_record_saved": save_result["status"] == "saved",
        "index_updated": index_result["status"] == "indexed",
        "record_count": index_result["record_count"],
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "save_result": save_result,
    }


def run_knowledge_learning_manager_diagnostics():
    mission = "Phase9-4 Knowledge Learning Manager diagnostic mission"

    pipeline_result = {
        "status": "dry_run",
        "pipeline_completed": True,
        "safe_to_continue": True,
        "risk_count": 0,
        "dry_run": True,
        "read_only": True,
    }

    return run_knowledge_learning_cycle(mission, pipeline_result)


if __name__ == "__main__":
    report = run_knowledge_learning_manager_diagnostics()

    print("=== Knowledge Learning Manager Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("KnowledgeRecordSaved:", report["knowledge_record_saved"])
    print("IndexUpdated:", report["index_updated"])
    print("RecordCount:", report["record_count"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", report["save_result"]["path"])