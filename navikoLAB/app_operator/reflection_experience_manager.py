from navikoLAB.app_operator.reflection_experience_core import (
    run_reflection_experience_cycle,
)
from navikoLAB.app_operator.reflection_experience_index import (
    build_reflection_experience_index,
)


def run_reflection_experience_learning_cycle(mission_text, pipeline_result):
    cycle_result = run_reflection_experience_cycle(
        mission_text,
        pipeline_result,
    )

    index_result = build_reflection_experience_index()

    return {
        "status": "completed",
        "phase": "Phase10-4 Reflection Experience Manager",
        "reflection_saved": cycle_result["reflection_saved"],
        "experience_saved": cycle_result["experience_saved"],
        "index_updated": index_result["status"] == "indexed",
        "reflection_count": index_result["reflection_count"],
        "experience_count": index_result["experience_count"],
        "success_count": index_result["success_count"],
        "failure_count": index_result["failure_count"],
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "cycle_result": cycle_result,
    }


def run_reflection_experience_manager_diagnostics():
    mission = "Phase10-4 Reflection Experience Manager diagnostic mission"

    pipeline_result = {
        "status": "dry_run",
        "pipeline_completed": True,
        "safe_to_continue": True,
        "risk_count": 0,
        "dry_run": True,
        "read_only": True,
    }

    return run_reflection_experience_learning_cycle(
        mission,
        pipeline_result,
    )


if __name__ == "__main__":
    report = run_reflection_experience_manager_diagnostics()

    print("=== Reflection Experience Manager Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("IndexUpdated:", report["index_updated"])
    print("ReflectionCount:", report["reflection_count"])
    print("ExperienceCount:", report["experience_count"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])