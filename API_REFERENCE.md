# Naviko LAB API Reference v1.4.0

**バージョン**: v1.4.0  
**最終更新**: 2026-07-06  
**ステータス**: Phase 7完了

---

## 目次

1. [InputAnalyzer](#inputanalyzer) - 入力解析モジュール
2. [GoalDecomposer](#goaldecomposer) - ゴール分解モジュール
3. [CapabilitySelector](#capabilityselector) - 能力選択モジュール
4. [ExecutionPlanner](#executionplanner) - 実行計画生成モジュール
5. [VoiceFeedback](#voicefeedback) - 音声フィードバックモジュール

---

## InputAnalyzer

**目的**: ユーザー入力を解析し、インテント、優先度、複雑度、エンティティを抽出します。

### クラス定義

```python
class InputAnalyzer:
    def __init__(self, user_input: str)
```

### メソッド

#### `analyze() -> Dict`

ユーザー入力を解析し、包括的な分析結果を返します。

**戻り値**:
```python
{
    "user_input": str,          # 元の入力
    "intent": str,              # インテント（create/analyze/modify/debug/help/unknown）
    "priority": str,            # 優先度（high/normal/low）
    "complexity": str,          # 複雑度（low/medium/high）
    "entities": {
        "技術スタック": List[str],  # 検出された技術（python, flask, sql等）
        "成果物": List[str],        # 要求される成果物（app, tool, api等）
        "キーワード": List[str]     # 抽出されたキーワード
    }
}
```

#### `get_summary() -> str`

解析結果のサマリーを文字列で返します。

**使用例**:

```python
from input_analyzer import InputAnalyzer

# 入力解析
analyzer = InputAnalyzer("PythonでWebスクレイピングツールを作成してください")
result = analyzer.analyze()

print(f"インテント: {result['intent']}")
print(f"複雑度: {result['complexity']}")
print(f"技術スタック: {result['entities']['技術スタック']}")
print(f"サマリー: {analyzer.get_summary()}")
```

---

## GoalDecomposer

**目的**: メインゴールをサブゴールに分解し、技術固有のサブゴールを追加し、依存関係を管理します。

### クラス定義

```python
class GoalDecomposer:
    def __init__(self, user_input: str, intent: str = "create")
```

### メソッド

#### `decompose() -> Dict`

メインゴールをサブゴールに分解します。

**戻り値**:
```python
{
    "main_goal": str,           # メインゴール
    "sub_goals": List[str],     # サブゴールのリスト
    "dependencies": Dict,       # サブゴール間の依存関係
    "total_steps": int,         # 総ステップ数
    "execution_order": List[str]  # 実行順序
}
```

#### `get_execution_order() -> List[str]`

サブゴールの実行順序を返します。

**使用例**:

```python
from goal_decomposer import GoalDecomposer

# ゴール分解
decomposer = GoalDecomposer(
    "Flaskを使ってWebアプリケーションを作成してください",
    intent="create"
)
result = decomposer.decompose()

print(f"メインゴール: {result['main_goal']}")
print(f"サブゴール数: {result['total_steps']}")
for i, sub_goal in enumerate(result['sub_goals'], 1):
    print(f"  {i}. {sub_goal}")
```

---

## CapabilitySelector

**目的**: タスクに必要な能力を選択し、推定時間を計算します。

### クラス定義

```python
class CapabilitySelector:
    def __init__(self)
```

### メソッド

#### `select_capabilities(task_analysis_result: Dict) -> Dict`

タスク分析結果から必要な能力を選択します。

**引数**:
```python
task_analysis_result = {
    "main_goal": str,
    "sub_tasks": List[Dict],    # [{"name": str, "estimated_time": str}, ...]
    "estimated_time": str,
    "complexity": str
}
```

**戻り値**:
```python
{
    "main_goal": str,
    "capabilities": List[Dict],   # 選択された能力のリスト
    "total_estimated_time": str,
    "selected_at": str            # ISO形式のタイムスタンプ
}
```

**使用例**:

```python
from capability_selector import CapabilitySelector

# 能力選択
selector = CapabilitySelector()
task_analysis = {
    "main_goal": "Webアプリケーション作成",
    "sub_tasks": [
        {"name": "要件定義", "estimated_time": "10分"},
        {"name": "設計", "estimated_time": "15分"}
    ],
    "estimated_time": "60分",
    "complexity": "medium"
}
result = selector.select_capabilities(task_analysis)

print(f"選択された能力数: {len(result['capabilities'])}")
print(f"総推定時間: {result['total_estimated_time']}")
```

---

## ExecutionPlanner

**目的**: 実行計画を生成し、並列実行可能なタスクをグループ化します。

### クラス定義

```python
class ExecutionPlanner:
    def __init__(self, max_parallel_tasks: int = 3)
```

### メソッド

#### `create_execution_plan(capability_selection_result: Dict) -> Dict`

実行計画を生成します。

**引数**:
```python
capability_selection_result = {
    "main_goal": str,
    "capabilities": List[Dict],
    "total_estimated_time": str
}
```

**戻り値**:
```python
{
    "main_goal": str,
    "execution_plan": {
        "levels": List[Dict],         # 実行レベルのリスト
        "critical_path": List[str],   # クリティカルパス
        "total_estimated_time": str,
        "sequential_time": str,
        "time_saved": str,
        "resource_requirements": Dict,
        "max_parallel_tasks": int,
        "error_handling": Dict
    },
    "warnings": List[str],
    "planned_at": str
}
```

**使用例**:

```python
from execution_planner import ExecutionPlanner

# 実行計画生成
planner = ExecutionPlanner(max_parallel_tasks=3)
capability_result = {
    "main_goal": "Webアプリケーション作成",
    "capabilities": [...],
    "total_estimated_time": "60分"
}
plan = planner.create_execution_plan(capability_result)

print(f"実行レベル数: {len(plan['execution_plan']['levels'])}")
print(f"総推定時間: {plan['execution_plan']['total_estimated_time']}")
print(f"並列実行による短縮時間: {plan['execution_plan']['time_saved']}")
```

---

## VoiceFeedback

**目的**: 音声フィードバック機能を提供し、タスクの進捗を音声で通知します。

### クラス定義

```python
class VoiceFeedback:
    def __init__(self, enabled: bool = True, volume: float = 0.8, rate: int = 150)
```

### メソッド

#### `notify_execution_start(main_goal: str, total_tasks: int = 0)`

実行開始を通知します。

#### `notify_level_start(level: int, task_names: List[str], parallel: bool = False)`

レベル開始を通知します。

#### `notify_task_start(task_name: str, estimated_time: str = "")`

タスク開始を通知します。

#### `notify_task_complete(task_name: str, success: bool = True, duration: str = "")`

タスク完了を通知します。

#### `notify_execution_complete(success: bool = True, total_time: str = "", warnings: List[str] = None)`

実行完了を通知します。

#### `notify_error(error_message: str, task_name: str = "", recovery_suggestion: str = "")`

エラーを通知します。

#### `get_notification_history() -> List[Dict]`

通知履歴を返します。

**使用例**:

```python
from voice_feedback import VoiceFeedback

# 音声フィードバック
voice = VoiceFeedback(enabled=True, volume=0.8, rate=150)

# 実行開始通知
voice.notify_execution_start("Webアプリケーション作成", total_tasks=5)

# タスク開始通知
voice.notify_task_start("要件定義", estimated_time="10分")

# タスク完了通知
voice.notify_task_complete("要件定義", success=True, duration="9分")

# 実行完了通知
voice.notify_execution_complete(success=True, total_time="45分")

# 通知履歴取得
history = voice.get_notification_history()
print(f"通知件数: {len(history)}")
```

---

## 完全な使用例：エンドツーエンド

5つのモジュールを連携させた完全な使用例です。

```python
from input_analyzer import InputAnalyzer
from goal_decomposer import GoalDecomposer
from capability_selector import CapabilitySelector
from execution_planner import ExecutionPlanner
from voice_feedback import VoiceFeedback

# ユーザー入力
user_input = "PythonでWebスクレイピングツールを作成してください"

# ステップ1: 入力解析
analyzer = InputAnalyzer(user_input)
analysis_result = analyzer.analyze()
print(f"インテント: {analysis_result['intent']}")

# ステップ2: ゴール分解
decomposer = GoalDecomposer(user_input, analysis_result['intent'])
goal_result = decomposer.decompose()
print(f"サブゴール数: {goal_result['total_steps']}")

# ステップ3: 能力選択
selector = CapabilitySelector()
task_analysis = {
    "main_goal": goal_result['main_goal'],
    "sub_tasks": [{"name": sg, "estimated_time": "10分"} for sg in goal_result['sub_goals']],
    "estimated_time": "60分",
    "complexity": analysis_result['complexity']
}
capability_result = selector.select_capabilities(task_analysis)
print(f"選択された能力数: {len(capability_result['capabilities'])}")

# ステップ4: 実行計画生成
planner = ExecutionPlanner(max_parallel_tasks=3)
plan_result = planner.create_execution_plan(capability_result)
print(f"実行レベル数: {len(plan_result['execution_plan']['levels'])}")

# ステップ5: 音声フィードバック
voice = VoiceFeedback(enabled=True)
voice.notify_execution_start(goal_result['main_goal'], total_tasks=len(goal_result['sub_goals']))
voice.notify_execution_complete(success=True, total_time="45分")
print(f"通知履歴: {len(voice.get_notification_history())}件")
```

---

## テスト

統合テストは `integration_test.py` で実行できます：

```bash
cd /Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB
python integration_test.py
```

**テストカバレッジ**: 11テスト（成功率100%）
- モジュールインポート確認
- 基本動作確認
- モジュール間連携テスト
- 実践シナリオテスト（3ケース）
- エラーハンドリングテスト
- パフォーマンス測定
- 高度なシナリオテスト（3ケース）
- エッジケーステスト（5ケース）
- ストレステスト（連続100回実行、33,138件/秒）

---

## パフォーマンス

- **処理速度**: 33,138件/秒（連続100回実行）
- **平均処理時間**: 0.03ms/件
- **メモリ使用量**: 最小限（軽量設計）
- **並列処理**: 最大3タスク同時実行可能

---

## サポート

- **バグ報告**: GitHub Issues
- **ドキュメント**: [README.md](README.md)
- **開発ガイド**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **アーキテクチャ**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Copyright © 2026 Naviko LAB. All rights reserved.**
