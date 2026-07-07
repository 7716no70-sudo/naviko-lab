#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase D-2-5自動適用スクリプト

このスクリプトは以下を自動実行します：
1. naviko.pyのバックアップ作成
2. Phase D-2-5の変更を自動適用
3. 構文チェック
4. Git同期（コミット・プッシュ）

使い方：
  cd C:\Users\7716n\OneDrive\デスクトップ\naviko
  python apply_phase_d2_5.py
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

def main():
    print("=" * 70)
    print("🚀 Phase D-2-5自動適用スクリプト")
    print("=" * 70)
    
    # 1. ディレクトリ確認
    if not os.path.exists('naviko.py'):
        print("❌ エラー: naviko.pyが見つかりません")
        print("   正しいディレクトリで実行してください")
        input("Enterキーを押して終了...")
        sys.exit(1)
    
    print("\n✅ naviko.pyを発見しました")
    
    # 2. バックアップ作成
    print("\n📁 バックアップ作成中...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'naviko_before_D2_5_auto_{timestamp}.py'
    shutil.copy2('naviko.py', backup_name)
    print(f"✅ バックアップ作成完了: {backup_name}")
    
    # 3. 変更適用
    print("\n📝 Phase D-2-5の変更を適用中...")
    
    with open('naviko.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 検索する文字列
    old_text = """    top_menu = tk.Frame(c_win, bg="#1e1e24")
    top_menu.pack(fill=tk.X, padx=10, pady=5)

    c_area = scrolledtext.ScrolledText("""
    
    # 置換後の文字列
    new_text = """    top_menu = tk.Frame(c_win, bg="#1e1e24")
    top_menu.pack(fill=tk.X, padx=10, pady=5)
    
    # 設定ボタン（左側）
    def open_settings():
        print("⚙️ 設定画面（Phase D-3で実装予定）")
        # TODO: Phase D-3で設定画面を実装
    
    settings_btn = tk.Button(
        top_menu,
        text="⚙️ 設定",
        command=open_settings,
        bg="#3c3c44",
        fg="white",
        relief=tk.FLAT,
        padx=10,
        pady=5
    )
    settings_btn.pack(side=tk.LEFT, padx=5)
    
    # クイックプリセットボタン群（右側）
    preset_frame = tk.Frame(top_menu, bg="#1e1e24")
    preset_frame.pack(side=tk.RIGHT, padx=5)
    
    def apply_preset(preset_name):
        print(f"🎭 プリセット切り替え: {preset_name}（Phase D-3で実装予定）")
        # TODO: Phase D-3でプリセット切り替え機能を実装
    
    # デフォルトプリセットボタン
    default_btn = tk.Button(
        preset_frame,
        text="デフォルト",
        command=lambda: apply_preset("デフォルト"),
        bg="#4a9eff",
        fg="white",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    default_btn.pack(side=tk.LEFT, padx=2)
    
    # ノベル風プリセットボタン
    novel_btn = tk.Button(
        preset_frame,
        text="ノベル風",
        command=lambda: apply_preset("ノベル風"),
        bg="#3c3c44",
        fg="#888888",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    novel_btn.pack(side=tk.LEFT, padx=2)
    
    # RPG風プリセットボタン
    rpg_btn = tk.Button(
        preset_frame,
        text="RPG風",
        command=lambda: apply_preset("RPG風"),
        bg="#3c3c44",
        fg="#888888",
        relief=tk.FLAT,
        padx=8,
        pady=3
    )
    rpg_btn.pack(side=tk.LEFT, padx=2)

    c_area = scrolledtext.ScrolledText("""
    
    # 置換実行
    if old_text in content:
        content = content.replace(old_text, new_text)
        print("✅ 変更を適用しました")
        
        # ファイルに書き込み
        with open('naviko.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ファイルを保存しました")
    else:
        print("⚠️  変更対象が見つかりません（既に適用済みの可能性）")
        print("   スクリプトを終了します")
        input("Enterキーを押して終了...")
        sys.exit(0)
    
    # 4. 構文チェック
    print("\n🔍 構文チェック中...")
    import py_compile
    import tempfile
    try:
        temp_pyc = tempfile.mktemp(suffix='.pyc')
        py_compile.compile('naviko.py', cfile=temp_pyc, doraise=True)
        print("✅ 構文エラーなし")
        if os.path.exists(temp_pyc):
            os.remove(temp_pyc)
    except py_compile.PyCompileError as e:
        print(f"❌ 構文エラー: {e}")
        print(f"   バックアップから復元してください: {backup_name}")
        input("Enterキーを押して終了...")
        sys.exit(1)
    
    # 5. Git同期
    print("\n📤 Git同期中...")
    
    # git status
    result = subprocess.run(['git', 'status', '--short'], 
                           capture_output=True, text=True)
    print("変更されたファイル:")
    print(result.stdout)
    
    # git add
    subprocess.run(['git', 'add', 'naviko.py'], check=True)
    print("✅ ステージング完了")
    
    # git commit
    commit_msg = "feat: Phase D-2-5完了 - 設定ボタン+プリセットボタン追加"
    result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                           capture_output=True, text=True)
    print(result.stdout)
    
    # git push
    print("\n📤 GitHubへプッシュ中...")
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                           capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("🎉 Phase D-2-5自動適用完了！")
        print("=" * 70)
        print("\n✅ すべての処理が正常に完了しました")
        print("✅ GitHub同期完了")
        print("\n次のステップ:")
        print("1. Databricks Workspaceで最新版を確認")
        print("2. Phase D-2-6（動作確認）に進む")
    else:
        print("\n⚠️  Push失敗（ネットワーク・認証エラーの可能性）")
        print("   手動でpushしてください: git push origin main")
    
    print("\n" + "=" * 70)
    input("Enterキーを押して終了...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  処理を中断しました")
        input("Enterキーを押して終了...")
    except Exception as e:
        print(f"\n\n❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
        input("Enterキーを押して終了...")
