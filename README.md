# Naviko LAB v1.4.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**自分で考えて成長するAI**

---

## 🎯 最終目的

> 「製作者がPC上で行える作業は、製作者が許可すればナビ子にもできる」

Naviko LABは単なるツールではありません。
**自律的に判断し、必要な能力を選択・実行する成長型AI**です。

### 理想の動作例
あなた: 「会議でプレゼンしたいから詳しく調べて資料を作成して」
  ↓
Naviko: （自分で判断）
  1. ディープサーチ（情報収集）
  2. データ整理
  3. プレゼン資料生成
  4. 完成

---

## 🌟 特徴

### 現在の能力（v1.4.0）
* ✅ **環境非依存** - ローカルLLM（Ollama）で完全オフライン動作
* ✅ **ディープサーチ** - ChatGPT風の深掘り調査エンジン
* ✅ **コード生成・改善** - 完全なアプリケーションを自動生成
* ✅ **自動フォールバック** - Local → Cloud → Template
* ✅ **高性能キャッシュ** - 98.77%圧縮、LRU削除

### 将来の能力（実装予定）
* ⏳ **能力選択** - 「何をしたいか」から自動で能力を選ぶ
* ⏳ **プレゼン資料作成** - 調査→分析→資料生成
* ⏳ **データ分析** - データ読み取り→分析→可視化

---

## 📦 インストール

### 必要環境
* Python 3.8以上
* Ollama（推奨）
* Groq APIキー（オプション）

### セットアップ
git clone https://github.com/7716no70-sudo/naviko-lab.git
cd naviko-lab
pip install -r requirements.txt

# Ollama（ローカルLLM）のセットアップ
ollama pull codellama:7b
ollama serve

---

## 🚀 クイックスタート

### アプリ生成
from pathlib import Path
from navikoLAB.app_project_builder import AppProjectBuilder

lab_dir = Path('/path/to/navikoLAB')
builder = AppProjectBuilder(lab_dir=lab_dir)

result = builder.build_basic_app_project(
    purpose='簡単な計算機アプリ',
    project_name='my_calculator'
)

### ディープサーチ
from navikoLAB.universal_llm_connector import UniversalLLMConnector
from navikoLAB.deep_search_engine import DeepSearchEngine

connector = UniversalLLMConnector(lab_dir=lab_dir, default_provider='local')
engine = DeepSearchEngine(llm_connector=connector)
result = engine.search('機械学習とは何ですか？')

---

## 📚 ドキュメント

* [API Reference](API_REFERENCE.md) - 完全なAPI仕様書
* [User Guide](USER_GUIDE.md) - ユーザー向けガイド
* [Developer Guide](DEVELOPER_GUIDE.md) - 開発者向けガイド
* [Architecture](ARCHITECTURE.md) - システムアーキテクチャ

---

## 🏗️ アーキテクチャ

### 現在（v1.4.0）
実行層（完成）
  ├─ UniversalLLMConnector（マルチプロバイダー）
  ├─ DeepSearchEngine（ディープサーチ）
  ├─ AppProjectBuilder（アプリ生成）
  └─ ImprovementManager（コード改善）

### 目標（Phase 6以降）
意思決定層
  ↓
能力選択層
  ↓
統合層
  ↓
実行層（完成）

---

## 📊 Phase 5完了状況

* ✅ Task 1: DeepSearchEngine実装
* ✅ Task 2: Ollama統合
* ✅ Task 3: UniversalLLMConnector拡張
* ✅ Task 4: パフォーマンス最適化
* ✅ Task 5: 統合テスト
* ✅ Task 6: ドキュメント完成
* ✅ Task 7: 本番環境準備

**Phase 5進捗: 100% (7/7タスク完了)**

---

## 🎯 ロードマップ

### Phase 6（次）
能力選択層の実装

### Phase 7（将来）
統合層の実装、プレゼン資料作成

### 最終形態
完全自律的AI、製作者の作業を全て代行

---

## 🤝 貢献

新しい能力の追加、バグ修正、ドキュメント改善など歓迎！
詳細は[Developer Guide](DEVELOPER_GUIDE.md)を参照。

---

## 📝 ライセンス
MIT License

---

**バージョン**: v1.4.0
**最終更新**: 2026-07-03
**設計思想**: 自分で考えて成長するAI
**ステータス**: Production Ready 🚀


---

## 📅 最新の更新（2026-07-03）

### ✅ naviko.py統合完了

**ErrorDiagnosticEngine + ExperienceMemory + ProcessRecorder 統合**

- **ErrorDiagnosticEngine** (510行): エラー自動診断、日本語解決策提案、7種類のエラーパターン対応
- **ExperienceMemory** (503行): エラー解決経験の蓄積、類似検索、最適解提案（SQLite連携）
- **ProcessRecorder** (549行): 作業プロセス記録、テンプレート化、テーマ変更再現
- **統合ガイド**: `navikoLAB/NAVIKO_GUI_INTEGRATION_GUIDE.md` (415行)

**統合結果**:
- naviko.py: 310,289 bytes (10,457行)
- 合計追加: 1,562行の自己改善機能
- 全モジュールテスト済み・正常動作確認済み

### ✅ Git同期問題解決

**3方向同期ライン確立**:
```
ローカルPC → GitHub → Databricks Workspace
```

- リポジトリ削除→再クローンによる完全同期
- 全ファイル確認済み（naviko.py + 統合モジュール）
- 今後の同期手順をドキュメント化

**コミット履歴**:
- `5ab6d6f`: navikoLAB統合モジュール追加
- `99ce3b4`: naviko.py統合コード追加
- `641137a`: 同期ライン確認テスト

---
