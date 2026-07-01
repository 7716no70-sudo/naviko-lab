from pathlib import Path

from navikoLAB.capabilities.capability_gui_bridge import CapabilityGUIBridge


def main():
    root_dir = Path(__file__).resolve().parents[1]

    bridge = CapabilityGUIBridge(
        root_dir
    )

    print(bridge.format_capability_summary())
    print("")
    print(
        bridge.diagnose_route(
            "YouTube用の短い紹介動画を作りたい"
        )
    )


if __name__ == "__main__":
    main()