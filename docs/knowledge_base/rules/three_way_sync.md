# 3方向同期の正規手順

## 同期順序
```
Workspace → GitHub → ローカルPC
```

## 1. Workspace → GitHub

### runGitツール使用（推奨）
```python
# Step 1: 最新版取得
runGit({
  "operation": "pull",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab"
})

# Step 2: コミット＆プッシュ
runGit({
  "operation": "commit_and_push",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab",
  "commitMessage": "feat: [変更内容]",
  "files": ["naviko.py"]
})
```

## 2. GitHub → ローカルPC

### ローカルPC側で実行
```powershell
cd C:\Users\7716n\OneDrive\デスクトップ\naviko
git pull origin main
git log --oneline -3
```

## 3. GitHub → Workspace

### runGitツール使用
```python
runGit({
  "operation": "pull",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab"
})
```

### 環境変数設定版
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

## エラー対処

### branch is behind
まずpull → 競合解決 → commit_and_push

### コンフリクト発生
ユーザーに報告、手動解決を依頼
