"""
Databricks Workspace用 Git操作ユーティリティ

Databricks Serverless環境の所有権エラーを回避するための
Git操作ラッパー関数を提供します。

使用例:
    from git_utils_workspace import run_git
    
    result = run_git(['status'])
    if result.returncode == 0:
        print(result.stdout)
"""

import subprocess
import os


def run_git(git_args, timeout=60, cwd=None):
    """
    Databricks Workspace環境でGit操作を実行するラッパー関数
    
    環境変数でsafe.directory設定を注入することで、
    セッションをまたいでもGit操作が可能になります。
    
    Args:
        git_args (list): Gitコマンドの引数リスト
            例: ['status'], ['add', 'naviko.py'], ['commit', '-m', 'message']
        timeout (int): タイムアウト秒数（デフォルト: 60）
        cwd (str): 作業ディレクトリ（デフォルト: カレントディレクトリ）
    
    Returns:
        subprocess.CompletedProcess: Gitコマンドの実行結果
            - returncode: 終了コード（0=成功）
            - stdout: 標準出力
            - stderr: 標準エラー出力
    
    使用例:
        # git status
        result = run_git(['status'])
        
        # git add
        result = run_git(['add', 'naviko.py'])
        
        # git commit
        result = run_git(['commit', '-m', 'feat: 新機能追加'])
        
        # git push
        result = run_git(['push', 'origin', 'main'])
        
        # git pull
        result = run_git(['pull', 'origin', 'main'])
    """
    # 環境変数を準備
    env = os.environ.copy()
    env['GIT_CONFIG_COUNT'] = '1'
    env['GIT_CONFIG_KEY_0'] = 'safe.directory'
    env['GIT_CONFIG_VALUE_0'] = '/Workspace/Users/7716no70@gmail.com/naviko-lab'
    
    # Gitコマンド実行
    result = subprocess.run(
        ['git'] + git_args,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        cwd=cwd if cwd else os.getcwd()
    )
    
    return result


def git_status():
    """git statusのショートカット"""
    return run_git(['status'])


def git_add(files):
    """
    git addのショートカット
    
    Args:
        files (str or list): ファイル名またはファイル名のリスト
    """
    if isinstance(files, str):
        files = [files]
    return run_git(['add'] + files)


def git_commit(message):
    """
    git commitのショートカット
    
    Args:
        message (str): コミットメッセージ
    """
    return run_git(['commit', '-m', message])


def git_push(remote='origin', branch='main'):
    """
    git pushのショートカット
    
    Args:
        remote (str): リモート名（デフォルト: origin）
        branch (str): ブランチ名（デフォルト: main）
    """
    return run_git(['push', remote, branch])


def git_pull(remote='origin', branch='main'):
    """
    git pullのショートカット
    
    Args:
        remote (str): リモート名（デフォルト: origin）
        branch (str): ブランチ名（デフォルト: main）
    """
    return run_git(['pull', remote, branch])


# テスト実行
if __name__ == '__main__':
    print("Git操作ユーティリティのテスト")
    print("-" * 60)
    
    # git status
    result = git_status()
    if result.returncode == 0:
        print("✅ git status 成功")
        print(result.stdout[:200])
    else:
        print(f"❌ git status 失敗: {result.stderr[:200]}")
