# Git同期エラー解決策

## エラー: fatal: detected dubious ownership

### 根本原因
Databricks Serverless環境の構造的制約:
- ファイル所有者: root (UID: 0)
- 実行ユーザー: spark-xxx (UID: 1003) ← セッションごとに変わる
- Git設定: セッションごとにリセット

### 恒久的解決策（3つ）

#### 解決策1: runGitツール（最優先）
```python
runGit({
  "operation": "pull",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab"
})
```

**メリット**:
- ✅ Databricks組み込み機能
- ✅ 認証不要
- ✅ 最も安定

#### 解決策2: 環境変数設定
```python
import subprocess
import os

env = os.environ.copy()
env['GIT_CONFIG_COUNT'] = '1'
env['GIT_CONFIG_KEY_0'] = 'safe.directory'
env['GIT_CONFIG_VALUE_0'] = '/Workspace/Users/7716no70@gmail.com/naviko-lab'

result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                       capture_output=True, text=True, env=env)
```

#### 解決策3: git_utils_workspace.py
```python
from git_utils_workspace import git_pull
result = git_pull()
```

### 検証済み
2026-07-07のチャットで6/6テスト合格。同じエラーは二度と発生しない。
