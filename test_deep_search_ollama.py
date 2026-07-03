# -*- coding: utf-8 -*-
"""
DeepSearchEngine - Ollamaローカルテスト
完全オフライン環境でのディープサーチ実行
"""
import sys
from pathlib import Path

# navikoLABをインポート
sys.path.insert(0, str(Path(__file__).parent))

from navikoLAB.universal_llm_connector import UniversalLLMConnector
from navikoLAB.deep_search_engine import DeepSearchEngine

def main():
    print("🚀 DeepSearchEngine - Ollamaローカルテスト\n")
    print("="*60)
    print("💡 完全オフライン環境でディープサーチを実行します")
    print("="*60)
    
    # UniversalLLMConnector初期化（Ollamaモード）
    lab_dir = Path(__file__).parent / "navikoLAB"
    
    print(f"\n🔧 初期化中...")
    print(f"   LAB DIR: {lab_dir}")
    print(f"   Provider: local (Ollama)")
    print(f"   Model: codellama:7b")
    
    try:
        connector = UniversalLLMConnector(
            lab_dir=lab_dir,
            api_key=None,  # APIキー不要
            default_provider="local",  # ローカルOllama使用
            ollama_model="codellama:7b"  # 使用モデル
        )
        
        # 利用可能プロバイダー確認
        available = connector.get_available_providers()
        print(f"\n📊 利用可能プロバイダー: {', '.join(available) if available else 'なし'}")
        
        if "local" not in available:
            print("\n❌ Ollamaが利用できません")
            print("\n🔧 トラブルシューティング:")
            print("   1. Ollamaがインストールされているか確認: ollama --version")
            print("   2. Ollamaサーバーが起動しているか確認: ollama list")
            print("   3. モデルがダウンロード済みか確認: ollama list")
            print("   4. モデルをダウンロード: ollama pull codellama:7b")
            return
        
        print("✅ Ollama接続成功！")
        
        # DeepSearchEngine初期化
        engine = DeepSearchEngine(connector)
        
        print("\n" + "="*60)
        print("🔍 ディープサーチ実行（Ollama）")
        print("="*60)
        
        # テストクエリ
        query = input("\n質問を入力してください（または Enter でデフォルト）: ").strip()
        
        if not query:
            query = "Pythonのリスト内包表記について、基本から応用まで教えてください"
            print(f"デフォルトクエリ: {query}")
        
        depth_input = input("\n深さを入力してください（1-3、デフォルト: 2）: ").strip()
        depth = int(depth_input) if depth_input.isdigit() and 1 <= int(depth_input) <= 3 else 2
        
        print(f"\n⏳ 実行中...")
        print(f"   クエリ: {query}")
        print(f"   深さ: {depth}ラウンド")
        print(f"   プロバイダー: Ollama (codellama:7b)")
        print(f"   実行モード: 完全オフライン")
        print(f"\n⚠️ 注意: Ollamaは初回実行時に時間がかかる場合があります（数分）")
        print()
        
        # ディープサーチ実行
        result = engine.search(
            query=query,
            depth=depth,
            use_parallel=False  # Ollamaではシリアル実行推奨
        )
        
        # 結果表示
        print("\n" + "="*60)
        print("📊 ディープサーチ結果")
        print("="*60)
        print(engine.format_result(result))
        
        # 統計情報
        print("\n" + "="*60)
        print("📈 実行統計")
        print("="*60)
        print(f"   実行時間: {result.get('execution_time', 'N/A'):.2f}秒")
        print(f"   信頼度: {result.get('confidence_score', 'N/A'):.1f}%")
        print(f"   情報源: {result.get('sources', 'N/A')}")
        print(f"   プロバイダー: Ollama (完全ローカル)")
        
        print("\n" + "="*60)
        print("🎉 テスト完了！")
        print("\n💡 Naviko LAB v1.3.5 - 完全自律型AIシステム")
        print("   ✅ クラウドAPI不要")
        print("   ✅ 完全オフライン動作")
        print("   ✅ プライバシー完全保護")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 トラブルシューティング:")
        print("   1. Ollamaが起動しているか確認: ollama list")
        print("   2. モデルがインストールされているか確認: ollama list")
        print("   3. モデルをダウンロード: ollama pull codellama:7b")

if __name__ == "__main__":
    main()
