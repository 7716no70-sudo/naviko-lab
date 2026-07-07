# Workspace → GitHub同期

## 制約
Databricks環境のセキュリティポリシーで外部への直接`git push`不可

## 解決策: runGitツール

### Step 1: 最新版取得（必要な場合）
```python
runGit({
  "operation": "pull",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab"
})
```

### Step 2: コミット＆プッシュ
```python
runGit({
  "operation": "commit_and_push",
  "repoPath": "/Workspace/Users/7716no70@gmail.com/naviko-lab",
  "commitMessage": "feat: [変更内容を簡潔に記述]",
  "files": ["naviko.py"]  # オプション
})
```

## エラー対処

### branch is behind
```python
# まずpull
runGit({"operation": "pull", "repoPath": "..."})
# その後commit_and_push
runGit({"operation": "commit_and_push", ...})
```

## 成功例
- Phase D-4-4（2026-07-08）: runGitで同期成功
- コミット: `6ec6d41 feat: Phase D-4-4完了 - 大型モデル切り替え機能追加`
