from datetime import datetime
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
BRIDGE_DIR = ROOT / "navikoLAB" / "bridge"
REPORT_DIR = BRIDGE_DIR / "reports"


class OriginalBridgeManager:
    def __init__(self):
        self.version = "bridge_v1.0"
        self.status = "initialized"
        self.bridges = {
            "mission": False,
            "knowledge": False,
            "reflection": False,
            "improvement": False,
            "pipeline": False,
        }

    def register_bridge(self, name: str):
        if name in self.bridges:
            self.bridges[name] = True

    def get_status(self):
        connected = sum(1 for v in self.bridges.values() if v)
        return {
            "status": self.status,
            "version": self.version,
            "bridge_count": len(self.bridges),
            "connected": connected,
            "failed": len(self.bridges) - connected,
            "bridges": self.bridges,
            "original_direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
        }

    def save_status(self):
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        path = REPORT_DIR / f"original_bridge_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(self.get_status(), ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return path


if __name__ == "__main__":
    manager = OriginalBridgeManager()
    for name in manager.bridges:
        manager.register_bridge(name)

    path = manager.save_status()
    print("=== OriginalBridgeManager ===")
    print("状態:", manager.get_status()["status"])
    print("Version:", manager.get_status()["version"])
    print("保存先:", path)