from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.original_adoption_dry_run_package_builder import OriginalAdoptionDryRunPackageBuilder

def main():
    builder = OriginalAdoptionDryRunPackageBuilder()
    package, package_path = builder.build_package()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-28 Original Adoption DryRun Package Builder",
        "package_status": package["status"],
        "package_type": package["package_type"],
        "included_module_count": len(package["included_modules"]),
        "package_path": package_path,
        "adoption_allowed": package["adoption_allowed"],
        "reason": package["reason"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_auto_write": False,
        "original_write_executed": False,
        "next_phase": "Phase2-29 Original Adoption DryRun Package Validator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_path = Path(__file__).resolve().parent / f"app_operator_phase2_28_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-28 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("PackageStatus:", report["package_status"])
    print("IncludedModuleCount:", report["included_module_count"])
    print("AdoptionAllowed:", report["adoption_allowed"])
    print("Reason:", report["reason"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("Package保存先:", package_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()