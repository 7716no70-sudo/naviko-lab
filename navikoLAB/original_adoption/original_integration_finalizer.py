from __future__ import annotations

import json
import py_compile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
ADOPTION_DIR = ROOT / "navikoLAB" / "original_adoption"
REPORT_DIR = ROOT / "navikoLAB" / "reports"


REQUIRED_MARKERS = [
    "run_original_autonomous_bridge",
    "run_original_lab_autonomous_flow_from_naviko",
    "Original Naviko LAB Bridge import",
    "Original Naviko LAB Bridge caller",
]


def latest_file(directory: Path, pattern: str) -> str | None:
    if not directory.exists():
        return None

    files = sorted(
        directory.glob(pattern),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return str(files[0]) if files else None


def naviko_syntax_ok() -> bool:
    try:
        py_compile.compile(str(NAVIKO_FILE), doraise=True)
        return True
    except Exception:
        return False


def marker_check() -> dict:
    source = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore")
    return {marker: marker in source for marker in REQUIRED_MARKERS}


def build_final_report() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    markers = marker_check()

    passed = (
        NAVIKO_FILE.exists()
        and naviko_syntax_ok()
        and all(markers.values())
    )

    return {
        "report_id": f"original_integration_final_{now}",
        "phase": "第20工程-5",
        "status": "completed" if passed else "failed",
        "completed": passed,
        "summary": "LAB完成機能をオリジナルnaviko.pyへimport方式で安全接続した。",
        "naviko_file": str(NAVIKO_FILE),
        "naviko_exists": NAVIKO_FILE.exists(),
        "naviko_syntax_ok": naviko_syntax_ok(),
        "marker_check": markers,
        "latest_request": latest_file(ADOPTION_DIR / "requests", "original_adoption_request_*.json"),
        "latest_simulation": latest_file(ADOPTION_DIR / "simulations", "original_adoption_simulation_*.json"),
        "latest_bridge_test": latest_file(ADOPTION_DIR / "bridge_call_tests", "original_bridge_static_test_*.json"),
        "latest_completion_report": latest_file(REPORT_DIR, "original_adoption_completion_*.json"),
        "integration_policy": {
            "naviko_py_role": "import / GUI / 呼び出しのみ",
            "lab_role": "Mission, Capability, Agent, MultiAI, Reflection, Improvement の本体を保持",
            "direct_large_merge": False,
            "rollback_ready": True,
        },
        "integrated_flow": [
            "Original naviko.py",
            "run_original_lab_autonomous_flow_from_naviko",
            "original_naviko_bridge",
            "MissionManager",
            "CapabilityRouter",
            "AgentManager",
            "AgentExecutor",
            "MultiAIOrchestrator",
            "MultiAIReflection",
            "MultiAIImprovementRequest",
            "AutonomousCapabilityFlow",
            "safe_simulation_completed",
        ],
        "next_step": "第21工程 GUIからオリジナル統合フローを実行できるボタン追加",
    }


def save_report(report: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / f"{report['report_id']}.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    report = build_final_report()
    output_path = save_report(report)

    print("=== 第20工程-5 オリジナル統合完了判定 ===")
    print(f"状態: {report['status']}")
    print(f"完了: {report['completed']}")
    print(f"naviko.py存在: {report['naviko_exists']}")
    print(f"naviko.py構文OK: {report['naviko_syntax_ok']}")
    print("接続マーカー:")
    for marker, ok in report["marker_check"].items():
        print(f"- {marker}: {ok}")
    print(f"保存先: {output_path}")
    print(f"次工程: {report['next_step']}")


if __name__ == "__main__":
    main()