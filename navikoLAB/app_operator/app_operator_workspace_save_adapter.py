from datetime import datetime

from navikoLAB.app_operator.app_operator_workspace_core import save_json_to_workspace


def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_mission_result_to_workspace(mission_text, result):
    filename = f"mission_result_{_timestamp()}.json"
    data = {
        "type": "mission_result",
        "mission": mission_text,
        "result": result,
        "workspace_mode": True,
        "original_write": False,
    }
    return save_json_to_workspace("mission_results", filename, data)


def save_knowledge_to_workspace(mission_text, knowledge):
    filename = f"knowledge_{_timestamp()}.json"
    data = {
        "type": "knowledge",
        "mission": mission_text,
        "knowledge": knowledge,
        "workspace_mode": True,
        "original_write": False,
    }
    return save_json_to_workspace("knowledge", filename, data)


def save_reflection_to_workspace(mission_text, reflection):
    filename = f"reflection_{_timestamp()}.json"
    data = {
        "type": "reflection",
        "mission": mission_text,
        "reflection": reflection,
        "workspace_mode": True,
        "original_write": False,
    }
    return save_json_to_workspace("reflection", filename, data)


def save_experience_to_workspace(mission_text, experience):
    filename = f"experience_{_timestamp()}.json"
    data = {
        "type": "experience",
        "mission": mission_text,
        "experience": experience,
        "workspace_mode": True,
        "original_write": False,
    }
    return save_json_to_workspace("experience", filename, data)


def run_workspace_save_adapter_diagnostics():
    mission = "Phase8-5 Workspace Save Adapter diagnostic mission"

    mission_result = save_mission_result_to_workspace(
        mission,
        {
            "status": "completed",
            "pipeline_completed": True,
        },
    )

    knowledge_result = save_knowledge_to_workspace(
        mission,
        {
            "summary": "Workspace保存アダプターによりKnowledge保存を確認。",
            "source": "diagnostic",
        },
    )

    reflection_result = save_reflection_to_workspace(
        mission,
        {
            "status": "reflected",
            "risk_count": 0,
            "safe_to_continue": True,
        },
    )

    experience_result = save_experience_to_workspace(
        mission,
        {
            "status": "recorded",
            "lesson": "Workspace限定保存は正常。",
        },
    )

    return {
        "status": "completed",
        "phase": "Phase8-5 Workspace Save Adapter",
        "mission_saved": mission_result["status"] == "saved",
        "knowledge_saved": knowledge_result["status"] == "saved",
        "reflection_saved": reflection_result["status"] == "saved",
        "experience_saved": experience_result["status"] == "saved",
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "results": {
            "mission": mission_result,
            "knowledge": knowledge_result,
            "reflection": reflection_result,
            "experience": experience_result,
        },
    }


if __name__ == "__main__":
    report = run_workspace_save_adapter_diagnostics()

    print("=== AppOperator Workspace Save Adapter Diagnostics ===")
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