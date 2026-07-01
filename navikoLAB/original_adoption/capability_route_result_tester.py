from __future__ import annotations

import json
from pathlib import Path

from navikoLAB.capabilities.capability_router import CapabilityRouter


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    router = CapabilityRouter(ROOT / "navikoLAB")

    for purpose in [
        "TODOアプリを作りたい",
        "YouTube用の短い紹介動画を作りたい",
    ]:
        result = router.route(purpose)

        print("=== CapabilityRouter 戻り値確認 ===")
        print(f"目的: {purpose}")
        print("キー:")
        for key, value in result.items():
            print(f"- {key}: {type(value).__name__} = {value}")
        print("JSON:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("")


if __name__ == "__main__":
    main()