# Naviko 再構成プラン - クイックリファレンス
**作成**: 2026-07-05 05:34

## 📌 次回セッションで最初にすること

### 1. このファイルを開く（5秒）
```python
# Workspace上で実行
with open("/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB/reports/reconstruction_plan_20260705_053440.md", 'r', encoding='utf-8') as f:
    print(f.read())
```

### 2. Phase A実行（15分）
```python
# バックアップファイル削除
from pathlib import Path
lab_dir = Path("/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB")
backup_files = list(lab_dir.glob("**/*backup*.py")) + list(lab_dir.glob("**/*_v*.py"))

# 確認後に削除
for f in backup_files:
    print(f"削除: {f.relative_to(lab_dir)}")
    # f.unlink()  # コメント解除で実行
```

## 🛡️ 保護対象（絶対に削除しない）

**Phase 1-3コアモジュール（10個）**:
- meta_cognition_engine.py
- problem_pattern_learner.py
- core_orchestrator.py
- auto_recovery_engine.py
- databricks_safety_checker.py
- advanced_learning_analyzer.py
- self_evolution_engine.py
- knowledge_graph_builder.py
- problem_patterns.db
- run_integration_test.py

## 📂 詳細プラン参照

**Markdown**: `reconstruction_plan_20260705_053440.md`（完全版）
**JSON**: `reconstruction_plan_20260705_053440.json`（構造化データ）

---
**ステータス**: ✅ ユーザー承認済み
**次回アクション**: Phase A（クリーンアップ）実行
