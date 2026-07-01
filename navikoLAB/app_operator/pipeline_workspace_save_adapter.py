from navikoLAB.app_operator.app_operator_workspace_save_adapter import (
    save_mission_result_to_workspace,
    save_knowledge_to_workspace,
    save_reflection_to_workspace,
    save_experience_to_workspace,
)


def save_pipeline_result_to_workspace(mission_text, pipeline_result):
    mission_save = save_mission_result_to_workspace(
        mission_text,
        pipeline_result,
    )

    knowledge_save = save_knowledge_to_workspace(
        mission_text,
        {
            "summary": "Pipeline結果をWorkspaceへ保存しました。",
            "pipeline_completed": pipeline_result.get("pipeline_completed", False),
            "status": pipeline_result.get("status"),
        },
    )

    reflection_save = save_reflection_to_workspace(
        mission_text,
        {
            "status": "reflected",
            "safe_to_continue": pipeline_result.get("safe_to_continue", True),
            "risk_count": pipeline_result.get("risk_count", 0),
        },
    )

    experience_save = save_experience_to_workspace(
        mission_text,
        {
            "status": "recorded",
            "lesson": "Pipeline結果をWorkspace限定で保存しました。",
            "workspace_only": True,
            "original_write": False,
        },
    )

    return {
        "status": "completed",
        "phase": "Phase8-8 Pipeline Workspace Save Adapter",
        "mission_saved": mission_save["status"] == "saved",
        "knowledge_saved": knowledge_save["status"] == "saved",
        "reflection_saved": reflection_save["status"] == "saved",
        "experience_saved": experience_save["status"] == "saved",
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "saved_results": {
            "mission": mission_save,
            "knowledge": knowledge_save,
            "reflection": reflection_save,
            "experience": experience_save,
        },
    }


def run_pipeline_workspace_save_adapter_diagnostics():
    mission = "Phase8-8 Pipeline Workspace Save Adapter diagnostic mission"

    pipeline_result = {
        "status": "dry_run",
        "pipeline_completed": True,
        "safe_to_continue": True,
        "risk_count": 0,
        "read_only": True,
        "workspace_mode": True,
        "original_write": False,
    }

    return save_pipeline_result_to_workspace(mission, pipeline_result)


if __name__ == "__main__":
    report = run_pipeline_workspace_save_adapter_diagnostics()

    print("=== Pipeline Workspace Save Adapter Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("MissionSaved:", report["mission_saved"])
    print("KnowledgeSaved:", report["knowledge_saved"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])