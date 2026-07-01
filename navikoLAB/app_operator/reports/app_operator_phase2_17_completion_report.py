from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.diagnostics.app_operator_integrated_diagnostics import AppOperatorIntegratedDiagnostics
from navikoLAB.app_operator.reflection.app_operator_reflection_saver import AppOperatorReflectionSaver
from navikoLAB.app_operator.experience.app_operator_experience_saver import AppOperatorExperienceSaver
from navikoLAB.app_operator.bridge.app_operator_original_bridge import AppOperatorOriginalBridge

def main():
    diagnostics = AppOperatorIntegratedDiagnostics()
    diagnostic_result = diagnostics.run()

    reflection_saver = AppOperatorReflectionSaver()
    reflection, reflection_path = reflection_saver.save(diagnostic_result)

    experience_saver = AppOperatorExperienceSaver()
    experience, experience_path = experience_saver.save(reflection)

    bridge = AppOperatorOriginalBridge()
    payload, payload_path = bridge.create_payload(
        diagnostic_result=diagnostic_result,
        reflection_path=reflection_path,
        experience_path=experience_path,
    )

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-17 Original Bridge integration for AppOperator",
        "bridge_status": payload["status"],
        "payload_path": payload_path,
        "requires_human_approval": payload["requires_human_approval"],
        "original_auto_write": payload["original_auto_write"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-18 AppOperator Original Adoption Request",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_17_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-17 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("BridgeStatus:", report["bridge_status"])
    print("HumanApproval:", report["requires_human_approval"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Payload保存先:", payload_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()