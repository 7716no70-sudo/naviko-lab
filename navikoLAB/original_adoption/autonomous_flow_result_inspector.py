from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "autonomous_flow_tests"


def run_inspection() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    mission = {
        "id": f"result_inspection_mission_{now}",
        "title": "TODOアプリを作りたい",
        "purpose": "TODOアプリを作りたい",
        "status": "active",
        "created_at": now,
        "source": "autonomous_flow_result_inspector",
    }

    flow = AutonomousCapabilityFlow(root_dir=ROOT)
    result = flow.run(mission)

    return {
        "inspection_id": f"autonomous_flow_result_inspection_{now}",
        "status": result.get("status", "unknown"),
        "result_keys": list(result.keys()),
        "result": result,
    }


def save_result(data: dict) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = LOG_DIR / f"{data['inspection_id']}.json"
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    data = run_inspection()
    output_path = save_result(data)

    print("=== AutonomousCapabilityFlow 戻り値構造確認 ===")
    print(f"状態: {data['status']}")
    print("戻り値キー:")
    for key in data["result_keys"]:
        value = data["result"].get(key)
        print(f"- {key}: {type(value).__name__}")
    print(f"保存先: {output_path}")


if __name__ == "__main__":
    main()