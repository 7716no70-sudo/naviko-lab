from __future__ import annotations

import json
import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_NAVIKO = ROOT / "naviko.py"

ADOPTION_DIR = ROOT / "navikoLAB" / "original_adoption"
REQUEST_DIR = ADOPTION_DIR / "requests"
SIMULATION_DIR = ADOPTION_DIR / "simulations"
BACKUP_DIR = ADOPTION_DIR / "simulation_backups"


REQUIRED_FEATURES = [
    "MissionManager",
    "CapabilityRouter",
    "AgentManager",
    "AgentExecutor",
    "MultiAIOrchestrator",
    "MultiAIReflection",
    "MultiAIImprovementRequest",
    "AutonomousCapabilityFlow",
]


def find_latest_request() -> Path | None:
    if not REQUEST_DIR.exists():
        return None

    requests = sorted(
        REQUEST_DIR.glob("original_adoption_request_*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return requests[0] if requests else None


def load_request(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_original_naviko() -> dict:
    result = {
        "exists": ORIGINAL_NAVIKO.exists(),
        "syntax_ok": False,
        "error": None,
    }

    if not ORIGINAL_NAVIKO.exists():
        result["error"] = "naviko.py が存在しません。"
        return result

    try:
        py_compile.compile(str(ORIGINAL_NAVIKO), doraise=True)
        result["syntax_ok"] = True
    except Exception as error:
        result["error"] = str(error)

    return result


def create_simulation_backup() -> Path | None:
    if not ORIGINAL_NAVIKO.exists():
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"naviko_simulation_backup_{now}.py"
    shutil.copy2(ORIGINAL_NAVIKO, backup_path)
    return backup_path


def build_import_plan(request: dict) -> list[dict]:
    features = request.get("features", [])

    plan = []
    for feature in features:
        name = feature.get("name")
        if name not in REQUIRED_FEATURES:
            continue

        plan.append(
            {
                "feature": name,
                "risk": feature.get("risk", "unknown"),
                "integration_type": feature.get("integration_type", "import_call"),
                "target": feature.get("target", ""),
                "naviko_py_change": "import と GUI呼び出しのみ",
                "direct_code_merge": False,
                "simulation_status": "planned",
            }
        )

    return plan


def run_simulation() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    latest_request = find_latest_request()

    simulation = {
        "simulation_id": f"original_adoption_simulation_{now}",
        "status": "not_started",
        "created_at": now,
        "request_file": str(latest_request) if latest_request else None,
        "original_naviko_check": {},
        "backup_file": None,
        "import_plan": [],
        "diff_policy": {
            "naviko_py_direct_merge": False,
            "naviko_py_allowed_changes": [
                "import追加",
                "GUIボタン追加",
                "LAB呼び出し関数追加",
            ],
            "new_feature_location": "navikoLAB",
        },
        "rollback_ready": False,
        "allowed_to_next_step": False,
        "next_step": None,
        "errors": [],
    }

    if latest_request is None:
        simulation["status"] = "failed"
        simulation["errors"].append("original_adoption_request が見つかりません。")
        return simulation

    request = load_request(latest_request)

    naviko_check = check_original_naviko()
    simulation["original_naviko_check"] = naviko_check

    if not naviko_check["exists"]:
        simulation["status"] = "failed"
        simulation["errors"].append("naviko.py が存在しないため中止。")
        return simulation

    if not naviko_check["syntax_ok"]:
        simulation["status"] = "failed"
        simulation["errors"].append("naviko.py の構文チェックに失敗したため中止。")
        return simulation

    backup_path = create_simulation_backup()
    simulation["backup_file"] = str(backup_path) if backup_path else None
    simulation["rollback_ready"] = backup_path is not None and backup_path.exists()

    simulation["import_plan"] = build_import_plan(request)

    if not simulation["import_plan"]:
        simulation["status"] = "failed"
        simulation["errors"].append("import_plan を作成できませんでした。")
        return simulation

    if not simulation["rollback_ready"]:
        simulation["status"] = "failed"
        simulation["errors"].append("バックアップ作成に失敗したため中止。")
        return simulation

    simulation["status"] = "simulation_completed"
    simulation["allowed_to_next_step"] = True
    simulation["next_step"] = "第20工程-4 naviko.py へ import方式で安全接続"

    return simulation


def save_simulation_result(simulation: dict) -> Path:
    SIMULATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SIMULATION_DIR / f"{simulation['simulation_id']}.json"

    output_path.write_text(
        json.dumps(simulation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    simulation = run_simulation()
    output_path = save_simulation_result(simulation)

    print("=== オリジナル反映シミュレーション ===")
    print(f"状態: {simulation['status']}")
    print(f"保存先: {output_path}")
    print(f"申請ファイル: {simulation['request_file']}")
    print(f"naviko.py存在: {simulation['original_naviko_check'].get('exists')}")
    print(f"naviko.py構文OK: {simulation['original_naviko_check'].get('syntax_ok')}")
    print(f"バックアップ: {simulation['backup_file']}")
    print(f"ロールバック準備: {simulation['rollback_ready']}")
    print(f"次工程許可: {simulation['allowed_to_next_step']}")

    print("反映シミュレーション対象:")
    for item in simulation["import_plan"]:
        print(f"- {item['feature']} / {item['risk']} / {item['integration_type']}")

    if simulation["errors"]:
        print("エラー:")
        for error in simulation["errors"]:
            print(f"- {error}")

    print(f"次工程: {simulation['next_step']}")


if __name__ == "__main__":
    main()