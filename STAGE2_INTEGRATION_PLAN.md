
=== Stage 2統合テスト：naviko.pyプラグイン統合計画 ===

【現状分析】
✅ プラグイン基盤ファイル: 全て存在
  - base.py (5,757 bytes)
  - registry.py (8,693 bytes)
  - config_manager.py (7,128 bytes)
  - default_sprite.py (8,645 bytes)
  - conversational.py (7,074 bytes)
  - gui_config.json (999 bytes)

✅ naviko.py構造:
  - 総行数: 10,410行
  - ファイルサイズ: 305,283 bytes
  - 主要なGUI初期化: 8100-8300行台
  - チャットウィンドウ: 9300-9700行台

【修正箇所の特定】

1. Import追加（推定: 10-100行台）
   - 現在: tkinter, PIL, その他基本ライブラリ
   - 追加必要:
     ```python
     from navikoLAB.gui_plugins.config_manager import ConfigManager
     from navikoLAB.gui_plugins.registry import PluginRegistry
     from navikoLAB.gui_plugins.renderers.default_sprite import DefaultSpriteRenderer
     from navikoLAB.gui_plugins.chat_displays.conversational import ConversationalChat
     ```

2. プラグイン初期化（8100-8134行: GUI起動チェック後）
   - 現在: Phase 3モジュール初期化（8119-8133行）
   - 追加:
     ```python
     # プラグインシステム初期化
     config_manager = ConfigManager(str(ROOT / "gui_config.json"))
     plugin_registry = PluginRegistry()
     
     # プラグイン登録
     plugin_registry.register_renderer("DefaultSprite", DefaultSpriteRenderer)
     plugin_registry.register_chat_display("Conversational", ConversationalChat)
     
     # 設定読み込み
     gui_config = config_manager.load_config()
     
     # プラグイン取得
     renderer_class = plugin_registry.get_renderer(gui_config["character_renderer"]["type"])
     chat_display_class = plugin_registry.get_chat_display(gui_config["chat_display"]["type"])
     ```

3. キャラクター表示のプラグイン化（8135-8300行台）
   - 現在: 直接スプライトシート読み込み + tkinter Label
   - 修正後: DefaultSpriteRendererプラグイン使用
   - 具体的修正:
     a. Line 8148-8157: スプライトシート読み込み → プラグイン初期化に置き換え
     b. Line 8159-8172: resize_pet_images → プラグインメソッド使用
     c. Line 8176: pet_label → プラグインのget_widget()
     d. Line 8184-8257: run_animation_loop → プラグインのupdate_emotion()

4. チャット表示のプラグイン化（9344-9700行台）
   - 現在: 直接ScrolledText作成
   - 修正後: ConversationalChatプラグイン使用
   - 具体的修正:
     a. Line 9391-9404: ScrolledText作成 → プラグイン初期化 + get_widget()
     b. append_chat_bubble関数 → プラグインのdisplay_user_message / display_ai_message

【段階的実装戦略】

Phase 1: Import追加（5分）
  - リスク: 低
  - 影響範囲: 小
  - 確認方法: 構文チェック

Phase 2: プラグイン初期化コード追加（10分）
  - リスク: 低
  - 影響範囲: 中
  - 確認方法: プラグイン読み込み成功確認

Phase 3: キャラクター表示統合（15-20分）
  - リスク: 中
  - 影響範囲: 大
  - 確認方法: キャラクター表示動作確認

Phase 4: チャット表示統合（15-20分）
  - リスク: 中
  - 影響範囲: 大
  - 確認方法: チャット送受信動作確認

Phase 5: 統合テスト + Git同期（10分）
  - 全機能動作確認
  - 3方向同期

合計所要時間: 55-70分

【リスク軽減策】

1. バックアップ作成
   - 修正前にnaviko.pyをバックアップ
   - Git commitで履歴保持

2. 段階的実装
   - 一度に全てを変更しない
   - 各Phaseごとに動作確認

3. ロールバック計画
   - 問題発生時は即座にGit revert
   - バックアップから復元

【次のアクション】

Option A: 今すぐ統合開始（推奨）
  - Import追加から順次実装
  - 約1時間で完了予定

Option B: 統合計画の確認
  - ユーザーに計画を確認
  - 承認後に実装開始

Option C: より詳細な分析
  - 影響範囲をさらに調査
  - テストケース作成
