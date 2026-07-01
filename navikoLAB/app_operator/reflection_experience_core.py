from datetime import datetime

from navikoLAB.app_operator.app_operator_workspace_core import save_json_to_workspace


def build_reflection_record(mission_text, pipeline_result):
    pipeline_completed = pipeline_result.get("pipeline_completed", False)
    risk_count = pipeline_result.get("risk_count", 0)
    safe_to_continue = pipeline_result.get("safe_to_continue", True)

    return {
        "type": "reflection_record",
        "mission": mission_text,
        "pipeline_status": pipeline_result.get("status"),
        "pipeline_completed": pipeline_completed,
        "risk_count": risk_count,
        "safe_to_continue": safe_to_continue,
        "success_signal": pipeline_completed and risk_count == 0 and safe_to_continue,
        "failure_signal": not pipeline_completed or risk_count > 0 or not safe_to_continue,
        "reflection_summary": "Pipeline結果をReflectionとして評価しました。",
        "workspace_mode": True,
        "original_write": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def build_experience_record(mission_text, reflection_record):
    success_signal = reflection_record.get("success_signal", False)

    lesson = (
        "安全条件を満たしたPipeline実行はWorkspaceへ保存してよい。"
        if success_signal
        else "安全条件を満たさないPipeline実行は停止または追加承認が必要。"
    )

    return {
        "type": "experience_record",
        "mission": mission_text,
        "success_signal": success_signal,
        "failure_signal": reflection_record.get("failure_signal", False),
        "lesson": lesson,
        "planner_feedback": {
            "prefer_workspace_only": True,
            "require_human_approval": True,
            "require_permission_policy": True,
            "avoid_original_write": True,
        },
        "workspace_mode": True,
        "original_write": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_reflection_record(mission_text, pipeline_result):
    record = build_reflection_record(mission_text, pipeline_result)
    filename = f"reflection_record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    save_result = save_json_to_workspace(
        "reflection",
        filename,
        record,
    )

    return save_result, record


def save_experience_record(mission_text, reflection_record):
    record = build_experience_record(mission_text, reflection_record)
    filename = f"experience_record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    save_result = save_json_to_workspace(
        "experience",
        filename,
        record,
    )

    return save_result, record


def run_reflection_experience_cycle(mission_text, pipeline_result):
    reflection_save, reflection_record = save_reflection_record(
        mission_text,
        pipeline_result,
    )

    experience_save, experience_record = save_experience_record(
        mission_text,
        reflection_record,
    )

    return {
        "status": "completed",
        "phase": "Phase10-2 Reflection Experience Core",
        "reflection_saved": reflection_save["status"] == "saved",
        "experience_saved": experience_save["status"] == "saved",
        "success_signal": reflection_record["success_signal"],
        "failure_signal": reflection_record["failure_signal"],
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "reflection_save": reflection_save,
        "experience_save": experience_save,
        "reflection_record": reflection_record,
        "experience_record": experience_record,
    }


def run_reflection_experience_diagnostics():
    mission = "Phase10-2 Reflection Experience Core diagnostic mission"

    pipeline_result = {
        "status": "dry_run",
        "pipeline_completed": True,
        "safe_to_continue": True,
        "risk_count": 0,
        "dry_run": True,
        "read_only": True,
    }

    return run_reflection_experience_cycle(mission, pipeline_result)


if __name__ == "__main__":
    report = run_reflection_experience_diagnostics()

    print("=== Reflection Experience Core Diagnostics ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("SuccessSignal:", report["success_signal"])
    print("FailureSignal:", report["failure_signal"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("Reflection保存先:", report["reflection_save"]["path"])
    print("Experience保存先:", report["experience_save"]["path"])