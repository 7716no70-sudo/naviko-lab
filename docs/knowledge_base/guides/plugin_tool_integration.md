# プラグイン→ツール自動登録機能 実装記録

**実装日**: 2026-07-08  
**所要時間**: 約1時間  
**状態**: ✅ 完了

---

## 📋 実装概要

**目的**: プラグインが提供するメソッドを、ToolRegistryに自動的に登録する仕組みを構築

**実装内容**:
1. BasePluginに `provide_tools()` メソッド追加
2. サンプルプラグインにツール提供機能実装
3. naviko.pyにプラグイン→ToolRegistry自動登録ブリッジコード追加
4. 統合テスト完全成功

---

## 🔧 実装詳細

### 1. BasePlugin修正

**ファイル**: `navikoLAB/plugin_system/base_plugin.py`

**追加メソッド**:
```python
def provide_tools(self) -> List[Dict[str, Any]]:
    """
    プラグインが提供するツールの定義
    
    Returns:
        List[Dict[str, Any]]: ツール定義のリスト
            各ツール定義: {'metadata': ToolMetadata, 'function': Callable}
    
    Note:
        デフォルト実装では空リストを返す。
        ツールを提供するプラグインはこのメソッドをオーバーライド。
    """
    return []
```

---

### 2. SimpleVoicePlugin修正

**ファイル**: `navikoLAB/plugins/examples/simple_voice_plugin.py`

**提供ツール**:
* `voice_synthesize` - テキストから音声を合成

**実装例**:
```python
def provide_tools(self):
    from navikoLAB.tool_system import ToolMetadata, ToolCategory, ToolComplexity
    
    def synthesize_voice(text: str, speed: float = 1.0) -> str:
        return self.execute(text=text, speed=speed)
    
    metadata = ToolMetadata(
        name="voice_synthesize",
        version="1.0.0",
        category=ToolCategory.VOICE_PROCESSING,
        description="テキストから音声を合成するツール",
        complexity=ToolComplexity.SIMPLE,
        required_params=["text"],
        optional_params=["speed"],
        return_type="str",
        tags=["voice", "tts", "synthesize"],
        author="Naviko Team",
        priority=10
    )
    
    return [{'metadata': metadata, 'function': synthesize_voice}]
```

---

### 3. SimpleDataProcessorPlugin修正

**ファイル**: `navikoLAB/plugins/examples/simple_data_processor_plugin.py`

**提供ツール**:
* `data_filter` - データをフィルタリング（正の数のみ抽出）
* `data_map` - データを変換（各要素を2倍）
* `data_reduce` - データを集約（合計計算）

**実装パターン**:
```python
def provide_tools(self):
    from navikoLAB.tool_system import ToolMetadata, ToolCategory, ToolComplexity
    
    def data_filter(data: List[Any]) -> List[Any]:
        return self.execute(data=data, operation='filter')
    
    filter_metadata = ToolMetadata(
        name="data_filter",
        version="1.0.0",
        category=ToolCategory.DATA_PROCESSING,
        description="データをフィルタリング（正の数のみ抽出）",
        complexity=ToolComplexity.SIMPLE,
        required_params=["data"],
        return_type="List[Any]",
        tags=["data", "filter"]
    )
    
    return [
        {'metadata': filter_metadata, 'function': data_filter},
        # ... 他のツール
    ]
```

---

### 4. naviko.py修正

**ファイル**: `naviko.py`（10954行目付近）

**ブリッジコード**:
```python
# プラグインシステムからツールを自動登録
if PLUGIN_SYSTEM_AVAILABLE:
    try:
        plugin_registry = UniversalPluginRegistry.get_instance()
        all_plugins = plugin_registry.get_all_plugins()
        
        tools_registered = 0
        for plugin_instance in all_plugins:
            # プラグインが提供するツールを取得
            tools = plugin_instance.provide_tools()
            
            # 各ツールをToolRegistryに登録
            for tool_info in tools:
                metadata = tool_info['metadata']
                function = tool_info['function']
                success = tool_registry.register_tool(metadata, function)
                if success:
                    tools_registered += 1
        
        if tools_registered > 0:
            print(f"✅ ToolRegistry 連携完了（{tools_registered}個のツールを登録）")
        else:
            print("✅ ToolRegistry 連携完了（ツール提供なし）")
    except Exception as e:
        print(f"⚠️ プラグインツール連携エラー: {e}")
```

---

## ✅ テスト結果

### 統合テスト

**実行内容**:
1. プラグインシステム初期化
2. ToolRegistry初期化
3. プラグインからツール自動登録
4. 登録されたツールの実行テスト

**結果**:
* ✅ 4個のツールを自動登録成功
  - SimpleDataProcessorPlugin: 3ツール
  - SimpleVoicePlugin: 1ツール
* ✅ すべてのツール実行テスト成功
  - voice_synthesize: 成功
  - data_filter: 成功
  - data_map: 成功
  - data_reduce: 成功

**ToolRegistry統計**:
* 総ツール数: 6個（既存2個 + 新規4個）
* カテゴリ:
  - data_processing: 5個
  - voice_processing: 1個

---

## 🎯 実装の意義

### 従来の問題
* プラグインの機能をツールとして登録するには手動コーディングが必要
* プラグイン追加時にToolRegistryへの登録を忘れる可能性
* プラグインとツールの連携が不透明

### 解決策
* プラグインが自動的にツールを提供
* PluginLoaderがロード時に自動登録
* プラグイン追加 = ツール追加が自動化

### メリット
1. **拡張性**: 新しいプラグインを追加するだけでツールが増える
2. **保守性**: プラグイン内でツール定義が完結
3. **透明性**: プラグイン→ツールのマッピングが明確
4. **再利用性**: プラグインの機能がツールAPIで統一的に利用可能

---

## 🔄 今後の拡張

### 1. 実用プラグインの追加
* VoiceVox音声合成プラグイン
* Webスクレイピングプラグイン
* データベース接続プラグイン

### 2. ツールメタデータの拡張
* 実行時間の記録
* エラー率の統計
* ユーザー評価

### 3. 動的ツール管理
* ツールの有効化/無効化
* バージョン管理
* 依存関係の自動解決

---

## 📚 関連ドキュメント

* `docs/knowledge_base/guides/session_20260708_part3.md` - プラグインシステム実装
* `navikoLAB/tool_system/README.md` - ToolRegistry仕様
* `navikoLAB/plugin_system/README.md` - プラグインシステム仕様

---

**記録者**: Genie Code  
**最終更新**: 2026-07-08
