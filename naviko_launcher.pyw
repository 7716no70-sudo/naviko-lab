"""
Naviko スタートアップランチャー

このスクリプトはPC起動時にnavikoを自動起動するためのランチャーです。
.pyw拡張子によりコンソールウィンドウが表示されません。

使用方法:
1. このファイルのショートカットをWindowsスタートアップフォルダに配置
2. PC起動時に自動でnavikoがバックグラウンドモードで起動します

スタートアップフォルダの場所:
  Win+R → shell:startup → Enter
  または
  C:\Users\<ユーザー名>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
"""

import sys
import subprocess
import os
from pathlib import Path
import traceback

def main():
    """Navikoをバックグラウンドモードで起動"""
    
    # 現在のスクリプトのディレクトリを取得
    script_dir = Path(__file__).parent.absolute()
    naviko_path = script_dir / "naviko.py"
    
    # naviko.pyの存在確認
    if not naviko_path.exists():
        error_msg = f"エラー: naviko.pyが見つかりません\n場所: {naviko_path}"
        
        # エラーログファイルに記録
        log_path = script_dir / "naviko_launcher_error.log"
        with open(log_path, 'a', encoding='utf-8') as f:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {error_msg}\n")
        
        # メッセージボックスでエラー表示（オプション）
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # メインウィンドウを隠す
            messagebox.showerror("Naviko起動エラー", error_msg)
            root.destroy()
        except:
            pass  # tkinterが使えない場合はスキップ
        
        return
    
    # Python実行ファイルのパスを取得
    python_exe = sys.executable
    
    try:
        # navikoをバックグラウンドモード（--hidden）で起動
        # subprocess.Popen: 新しいプロセスとして起動し、このスクリプトは終了
        process = subprocess.Popen(
            [python_exe, str(naviko_path), "--hidden"],
            cwd=str(script_dir),
            stdout=subprocess.DEVNULL,  # 標準出力を抑制
            stderr=subprocess.DEVNULL,  # 標準エラーを抑制
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0  # Windowsでコンソール非表示
        )
        
        # 起動成功ログ
        log_path = script_dir / "naviko_launcher.log"
        with open(log_path, 'a', encoding='utf-8') as f:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] ✅ Naviko起動成功 (PID: {process.pid})\n")
    
    except Exception as e:
        # エラーログに記録
        error_msg = f"Naviko起動エラー: {e}\n{traceback.format_exc()}"
        log_path = script_dir / "naviko_launcher_error.log"
        with open(log_path, 'a', encoding='utf-8') as f:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {error_msg}\n")

if __name__ == "__main__":
    main()
