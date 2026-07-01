from pathlib import Path

try:
    from .capability_router import CapabilityRouter
except ImportError:
    from capability_router import CapabilityRouter


def test_route(router, purpose):
    result = router.route(purpose)

    print("---------------")
    print("目的:", purpose)
    print("必要能力:", result.get("required_ids", []))
    print("選択済み:", [cap.get("id") for cap in result.get("selected", [])])
    print("不足:", result.get("missing", []))


def main():
    root_dir = Path(__file__).resolve().parent.parent
    router = CapabilityRouter(root_dir)

    print("=== CapabilityRouter テスト ===")

    test_route(router, "TODOアプリを作りたい")
    test_route(router, "YouTube用の短い紹介動画を作りたい")
    test_route(router, "画像生成ツールを作りたい")
    test_route(router, "音声ナレーション付き動画を作りたい")
    test_route(router, "AIエージェント管理ツールを作りたい")
    test_route(router, "最新情報を検索して調査したい")

    print("===============")
    print("=== Router診断 ===")

    diagnosis = router.diagnose()

    for key, value in diagnosis.items():
        print(f"{key}: {value}")

    print("=== CapabilityRouter テスト完了 ===")


if __name__ == "__main__":
    main()