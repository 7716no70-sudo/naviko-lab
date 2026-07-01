from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.diagnostics.app_operator_integrated_diagnostics import AppOperatorIntegratedDiagnostics
from navikoLAB.app_operator.reflection.app_operator_reflection_saver import AppOperatorReflectionSaver
from navikoLAB.app_operator.experience.app_operator_experience_saver import AppOperatorExperienceSaver

def main():
    diagnostics = AppOperatorIntegratedDiagnostics()
    diagnostic_result = diagnostics.run()

    reflection_saver = AppOperatorReflectionSaver()
    reflection, reflection_path = reflection_saver.save(diagnostic_result)

    experience_saver = AppOperatorExperienceSaver()
    experience, experience_path = experience_saver.save(reflection)

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-16 AppOperator Reflection / Experience save",
        "diagnostic_status": diagnostic_result["status"],
        "reflection_path": reflection_path,
        "experience_path": experience_path,
        "reflection_status": reflection["status"],
        "experience_status": experience["status"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-17 Original Bridge integration for AppOperator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_16_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-16 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("DiagnosticStatus:", report["diagnostic_status"])
    print("ReflectionStatus:", report["reflection_status"])
    print("ExperienceStatus:", report["experience_status"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Reflection保存先:", reflection_path)
    print("Experience保存先:", experience_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()