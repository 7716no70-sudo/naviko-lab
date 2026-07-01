from pathlib import Path

from capability_connector import CapabilityConnector
from capability_router import CapabilityRouter


def main():

    root_dir = Path(__file__).resolve().parent.parent

    connector = CapabilityConnector(root_dir)
    router = CapabilityRouter(root_dir)

    diagnosis = connector.diagnose()

    print("=== Capability 診断 ===")
    print("能力総数:", diagnosis["capability_count"])
    print("有効:", diagnosis["enabled_count"])
    print("無効:", diagnosis["disabled_count"])
    print("Type別:", diagnosis["type_count"])

    print("---------------")
    print("=== 有効能力 ===")

    for capability in connector.get_enabled_capabilities():
        print(
            "-",
            capability["id"],
            "/",
            capability["name"],
            "/",
            capability["type"],
            "/",
            capability["status"]
        )

    print("---------------")
    print("=== Router確認 ===")

    sample_goals = [
        "アプリを作りたい",
        "動画を作りたい",
        "画像を作りたい",
        "音声つき動画を作りたい",
        "検索して調査したい"
    ]

    for goal in sample_goals:
        result = router.route(goal)

        print("目的:", goal)
        print("必要:", result["required_ids"])
        print("選択:", [cap["id"] for cap in result["selected"]])
        print("不足:", result["missing"])
        print("---")

    print("保存先:", diagnosis["registry_file"])
    print("履歴:", diagnosis["history_file"])

    print("=== Capability 診断完了 ===")


if __name__ == "__main__":
    main()