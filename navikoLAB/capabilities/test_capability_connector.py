from pathlib import Path

from capability_connector import CapabilityConnector


def main():

    root_dir = Path(__file__).resolve().parent.parent

    connector = CapabilityConnector(root_dir)

    print("=== CapabilityConnector 単体テスト ===")

    capabilities = connector.list_capabilities()

    print("登録能力数:", len(capabilities))

    for capability in capabilities:
        print(
            "-",
            capability["id"],
            "/",
            capability["name"],
            "/",
            capability["type"],
            "/ enabled:",
            capability["enabled"],
            "/ status:",
            capability["status"]
        )

    connector.enable_capability("image_ai")
    connector.enable_capability("video_ai")

    print("---------------")
    print("有効化テスト:")
    print("image_ai:", connector.find_by_id("image_ai")["enabled"])
    print("video_ai:", connector.find_by_id("video_ai")["enabled"])

    diagnosis = connector.diagnose()

    print("---------------")
    print("=== 診断 ===")

    for key, value in diagnosis.items():
        print(key + ":", value)

    print("=== CapabilityConnector 単体テスト完了 ===")


if __name__ == "__main__":
    main()


