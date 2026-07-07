# Naviko システム再構成プラン
**作成日時**: 2026年07月05日 05:34:40
**ステータス**: ✅ ユーザー承認済み
**次回セッション**: このプランに従って実行

---

## 📊 現状分析結果

### コアモジュール（保護対象）
**Phase 1-3で実装済み、削除・変更不可**

| モジュール | サイズ | 説明 |
|-----------|--------|------|
| meta_cognition_engine.py | 25,377 bytes | メタ認知エンジン - 自己診断・予測 |
| problem_pattern_learner.py | 23,168 bytes | 問題学習システム - パターン化・予防策 |
| core_orchestrator.py | 15,725 bytes | 統合管理 - System 1/2/3制御 |
| auto_recovery_engine.py | 21,134 bytes | 自動リカバリー - エラー対処 |
| databricks_safety_checker.py | 13,625 bytes | 事前安全チェック |
| advanced_learning_analyzer.py | 33,518 bytes | 高度学習 - 予測・相関分析 |
| self_evolution_engine.py | 31,370 bytes | 自己進化 - コード改善提案 |
| knowledge_graph_builder.py | 17,255 bytes | 知識グラフ - 推論エンジン |
| problem_patterns.db | 0 bytes | 学習データベース |
| run_integration_test.py | 7,819 bytes | 統合テストスクリプト |

**合計**: 10モジュール、約189 KB

---

## 🗑️ 削除対象ファイル

### バックアップファイル（51件）
**理由**: Phase 1-3完了、Git同期完了済みで不要

主な対象:
- naviko_core_v1_*_backup.py（8ファイル）
- naviko_chat_main_v1_0_backup.py
- その他バックアップファイル（43ファイル）

**削減容量**: 約76 KB

### 大容量ファイル（2件）
**合計サイズ**: 58.2 MB

1. `python-manager-26.3.msix`（47.0 MB）
   - Pythonインストーラー、開発環境では不要

2. `docs/auto_documentation_20260626_211640.md`（11.2 MB）
   - 古い自動生成ドキュメント、最新版に置き換え済み

**削減容量**: 約58 MB

### テストファイル（29件）
**状態**: 内容確認後に判断
**最終更新**: 0日前（実行中の可能性）

主な対象:
- test_autonomous_core_capability_connection.py
- core/test_mission_*.py（複数）

**アクション**: 次回セッションで内容確認

---

## 🎯 実行プラン

### Phase A: クリーンアップ（推奨実施）

#### A-1. バックアップファイル削除（5-10分）
**優先度**: 🥇 最優先
**リスク**: 低
**効果**: ディスク容量削減、構造明確化

**実行コマンド**:
```python
# バックアップファイルを安全に削除
import shutil
from pathlib import Path

lab_dir = Path("/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB")

# バックアップファイル検出
backup_files = list(lab_dir.glob("**/*backup*.py")) + \
               list(lab_dir.glob("**/*_v*.py"))

# 削除前確認
print(f"削除対象: {len(backup_files)}件")
for f in backup_files[:5]:
    print(f"  - {f.relative_to(lab_dir)}")

# 実行確認後に削除
# for f in backup_files:
#     f.unlink()
```

#### A-2. 大容量ファイル削除（5分）
**優先度**: 🥇 最優先
**リスク**: 低
**効果**: 58MB削減

**対象**:
- `python-manager-26.3.msix`
- `docs/auto_documentation_20260626_211640.md`

---

### Phase B: コア機能保護メカニズム（新規実装）

#### B-1. モジュール保護システム実装（1-2時間）
**優先度**: 🥈 高優先（1-2日以内）
**リスク**: 中
**効果**: 将来の破壊的変更を防止

**実装内容**:
1. **コアモジュール完全性チェック**
   - ファイルハッシュ検証
   - 必須関数の存在確認
   - データベース整合性チェック

2. **依存関係マップ**
   - 各モジュールの依存関係自動検出
   - 破壊的変更の事前検出
   - 安全な更新順序の提案

3. **バージョン管理**
   - セマンティックバージョニング
   - 変更履歴の自動記録
   - ロールバック機能

**新規ファイル**:
- `protection/core_protection.py`
- `protection/integrity_checker.py`
- `protection/dependency_mapper.py`

#### B-2. ディレクトリ再編成（30-60分）
**優先度**: 🥈 高優先（1-2日以内）
**リスク**: 中
**効果**: core/plugins分離、拡張性向上

**新ディレクトリ構造**:
```
navikoLAB/
├── core/              # コアモジュール（保護対象）
│   ├── meta_cognition_engine.py
│   ├── problem_pattern_learner.py
│   ├── core_orchestrator.py
│   ├── auto_recovery_engine.py
│   ├── databricks_safety_checker.py
│   ├── advanced_learning_analyzer.py
│   ├── self_evolution_engine.py
│   └── knowledge_graph_builder.py
├── plugins/           # 拡張機能（追加・削除自由）
│   ├── voice_chat/
│   ├── 3d_character/
│   └── custom_analyzers/
├── protection/        # 保護メカニズム
│   ├── core_protection.py
│   ├── integrity_checker.py
│   └── dependency_mapper.py
└── tests/            # テストスイート
    ├── unit/
    ├── integration/
    └── regression/
```

---

### Phase C: 拡張可能アーキテクチャ

#### C-1. テストフレームワーク強化（2-3時間）
**優先度**: 🥉 中優先（1週間以内）
**リスク**: 低
**効果**: 継続的品質保証

**実装内容**:
- 単体テスト（各モジュール）
- 統合テスト（モジュール間連携）
- 回帰テスト（既存機能保護）

#### C-2. プラグインシステム設計（4-6時間）
**優先度**: 🥉 中優先（1週間以内）
**リスク**: 高
**効果**: 将来の機能追加が安全に

**設計指針**:
- 標準化されたAPI（入力・出力フォーマット）
- エラーハンドリングの統一
- ロギング形式の統一

---

## 📋 次回セッション実行チェックリスト

### ステップ1: 環境確認（5分）
- [ ] APIキー設定確認
- [ ] Git同期状態確認
- [ ] コアモジュール存在確認

### ステップ2: Phase A実行（15-20分）
- [ ] A-1: バックアップファイル削除
- [ ] A-2: 大容量ファイル削除
- [ ] Git commit & push
- [ ] ローカルPC同期確認

### ステップ3: Phase B準備（30分）
- [ ] 保護ディレクトリ作成
- [ ] コアモジュールリスト定義
- [ ] 依存関係初期分析

---

## 🔗 関連ファイル

**このプラン**:
- Markdown: `reports/reconstruction_plan_{timestamp}.md`
- JSON: `reports/reconstruction_plan_{timestamp}.json`

**実行ログ**:
- 次回セッションで `reports/reconstruction_execution_{timestamp}.log` に記録

**Git同期**:
- Workspace → GitHub → ローカルPC
- コミットメッセージ: "docs: Naviko再構成プラン策定"

---

## ⚠️ 重要な注意事項

1. **コアモジュールは絶対に削除・変更しない**
   - Phase 1-3で実装済み
   - 実運用テスト済み（成功率100%）
   - Git同期完了済み

2. **削除前に必ず確認**
   - バックアップファイルリストを目視確認
   - 大容量ファイルの用途確認
   - テストファイルの実行状況確認

3. **Git同期は必須**
   - 削除作業後は必ずcommit & push
   - ローカルPCへの同期確認
   - 3方向同期ライン維持

4. **テスト実行**
   - Phase A完了後に統合テスト実行
   - コアモジュールの動作確認
   - エラー発生時はロールバック

---

**作成者**: Genie Code (Databricks Assistant)
**承認**: ユーザー承認済み（2026-07-05）
**有効期限**: なし（永続保存）
