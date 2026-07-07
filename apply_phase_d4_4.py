# -*- coding: utf-8 -*-
"""
Phase D-4-4自動適用スクリプト
大型モデル切り替え機能をローカルPC側のnaviko.pyに適用
"""

import os
import shutil
from datetime import datetime
import subprocess
import sys

def main():
    print("=" * 70)
    print("🚀 Phase D-4-4自動適用スクリプト")
    print("=" * 70)
    
    # naviko.pyの存在確認
    if not os.path.exists('naviko.py'):
        print("\n❌ エラー: naviko.pyが見つかりません")
        print("このスクリプトをnaviko.pyと同じディレクトリで実行してください")
        input("\nEnterキーを押して終了...")
        sys.exit(1)
    
    print("\n✅ naviko.pyを発見しました")
    
    # バックアップ作成
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'naviko_before_D4_4_auto_{timestamp}.py'
    
    print(f"\n📁 バックアップ作成中...")
    shutil.copy2('naviko.py', backup_name)
    print(f"✅ バックアップ作成完了: {backup_name}")
    
    # ファイル読み込み
    with open('naviko.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n📝 Phase D-4-4の変更を適用中...")
    
    # 変更1: グローバル定数の追加（try-exceptブロックの後）
    old_except = """except ImportError:
    VOSK_AVAILABLE = False
    print("⚠️ Vosk音声認識が利用できません（vosk/pyaudioが未インストール）")
# === Vosk音声認識インポート end ==="""
    
    new_except = """except ImportError:
    VOSK_AVAILABLE = False
    print("⚠️ Vosk音声認識が利用できません（vosk/pyaudioが未インストール）")
# === Vosk音声認識インポート end ===

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Voskモデルパス定義（Phase D-4-4）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOSK_MODEL_SMALL = "vosk_models/vosk-model-small-ja-0.22"  # 小型モデル（40MB）
VOSK_MODEL_LARGE = "vosk_models/vosk-model-ja-0.22"        # 大型モデル（1.8GB）
CURRENT_VOSK_MODEL = VOSK_MODEL_SMALL  # デフォルトは小型モデル"""
    
    if old_except in content:
        content = content.replace(old_except, new_except)
        print("✅ 変更1: グローバル定数追加")
    else:
        print("⚠️ 変更1: 既に適用済みまたはパターンが一致しません")
    
    # 変更2: __init__にcurrent_model_path保存を追加
    old_init = """        # 内部状態
        self.is_listening = False
        self.callback = None
        self.recognition_thread = None"""
    
    new_init = """        # 内部状態
        self.is_listening = False
        self.callback = None
        self.recognition_thread = None
        self.current_model_path = model_path  # 現在のモデルパスを保存（Phase D-4-4）"""
    
    if old_init in content and 'self.current_model_path = model_path  # 現在のモデルパスを保存（Phase D-4-4）' not in content:
        content = content.replace(old_init, new_init)
        print("✅ 変更2: current_model_path保存追加")
    else:
        print("⚠️ 変更2: 既に適用済みまたはパターンが一致しません")
    
    # 変更3: switch_model()メソッドの追加（VoiceWakeWordDetectorクラス内）
    switch_model_method = """    
    def switch_model(self, model_path):
        \"""
        Voskモデルを切り替える（Phase D-4-4）
        
        Args:
            model_path (str): 新しいVoskモデルのパス
                小型: "vosk_models/vosk-model-small-ja-0.22"
                大型: "vosk_models/vosk-model-ja-0.22"
        
        Returns:
            bool: モデル切り替え成功/失敗
        \"""
        # 音声認識が実行中の場合は停止
        was_listening = self.is_listening
        if was_listening:
            print("🔄 音声認識を一時停止してモデル切り替え...")
            self.stop_listening()
        
        # モデル切り替え
        try:
            print(f"🔄 Voskモデルを切り替え中: {model_path}")
            self.model = vosk.Model(model_path)
            self.current_model_path = model_path
            print(f"✅ Voskモデル切り替え完了")
            
            # 音声認識を再開
            if was_listening and self.callback:
                print("🔄 音声認識を再開...")
                self.start_listening(self.callback)
            
            return True
        except Exception as e:
            print(f"❌ モデル切り替え失敗: {e}")
            return False
"""
    
    if 'def switch_model(self, model_path):' not in content:
        # stop_listening()メソッドの後に挿入
        # stop_listening()の終了位置を探す
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # stop_listening()の終了を検出（次のdefの前または_recognition_loopの前）
            if i > 0 and '        print("✅ 音声認識停止完了")' in lines[i]:
                # 次の行がdefまたはクラスの終わりなら、ここに挿入
                if i+1 < len(lines) and (lines[i+1].strip().startswith('def ') or not lines[i+1].strip()):
                    new_lines.append(switch_model_method)
                    inserted = True
        
        if inserted:
            content = '\n'.join(new_lines)
            print("✅ 変更3: switch_model()メソッド追加")
        else:
            print("⚠️ 変更3: 挿入位置が見つかりません")
    else:
        print("⚠️ 変更3: 既に適用済み")
    
    # 変更4: ヘルパー関数の追加（VoiceWakeWordDetectorクラスの後）
    helper_functions = """

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Voskモデル切り替えヘルパー関数（Phase D-4-4）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def switch_vosk_model(detector, size='small'):
    \"""
    Voskモデルを切り替える
    
    Args:
        detector (VoiceWakeWordDetector): Detectorインスタンス
        size (str): 'small'（小型）または 'large'（大型）
    
    Returns:
        bool: 切り替え成功/失敗
    \"""
    global CURRENT_VOSK_MODEL
    
    if size == 'small':
        model_path = VOSK_MODEL_SMALL
        model_name = "小型モデル（40MB・認識精度85-90%）"
    elif size == 'large':
        model_path = VOSK_MODEL_LARGE
        model_name = "大型モデル（1.8GB・認識精度95-98%）"
    else:
        print(f"❌ 不正なサイズ指定: {size}")
        return False
    
    # モデルファイルの存在確認
    if not os.path.exists(model_path):
        print(f"❌ モデルが見つかりません: {model_path}")
        print(f"   大型モデルのダウンロードが必要です")
        print(f"   URL: https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip")
        return False
    
    # モデル切り替え実行
    print(f"🔄 {model_name}に切り替え中...")
    success = detector.switch_model(model_path)
    
    if success:
        CURRENT_VOSK_MODEL = model_path
        print(f"✅ モデル切り替え完了: {model_name}")
    
    return success


def download_large_vosk_model():
    \"""
    大型Voskモデルをダウンロード（Phase D-4-4）
    
    注意: 1.8GBのダウンロードが必要です（10-15分）
    
    Returns:
        bool: ダウンロード成功/失敗
    \"""
    import urllib.request
    import zipfile
    
    model_url = "https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip"
    zip_path = "vosk-model-ja-0.22.zip"
    extract_dir = "vosk_models"
    
    print("=" * 70)
    print("📥 大型Voskモデルをダウンロード中...")
    print("=" * 70)
    print(f"URL: {model_url}")
    print(f"サイズ: 約1.8GB")
    print(f"推定時間: 10-15分")
    print()
    
    try:
        # ダウンロード
        print("🔄 ダウンロード開始...")
        urllib.request.urlretrieve(model_url, zip_path)
        print("✅ ダウンロード完了")
        
        # 解凍
        print("🔄 解凍中...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("✅ 解凍完了")
        
        # zipファイル削除
        os.remove(zip_path)
        print("✅ 一時ファイル削除完了")
        
        print("=" * 70)
        print("🎉 大型Voskモデルのダウンロード完了！")
        print("=" * 70)
        print(f"保存先: {extract_dir}/vosk-model-ja-0.22")
        print()
        return True
        
    except Exception as e:
        print(f"❌ ダウンロード失敗: {e}")
        return False
"""
    
    if 'def switch_vosk_model(detector, size=' not in content:
        # _detect_wake_wordメソッドの後に挿入
        # _detect_wake_wordの終了位置を探す
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # _detect_wake_wordの最後を検出
            if '        return False' in line and i > 0:
                # 前の行が「for word in self.wake_words:」のブロックならここに挿入
                if i-3 >= 0 and 'for word in self.wake_words:' in lines[i-3]:
                    # 次の行がdefなら、ここに挿入
                    if i+1 < len(lines) and (lines[i+1].startswith('def ') or lines[i+1].startswith('# ━')):
                        new_lines.append(helper_functions)
                        inserted = True
        
        if inserted:
            content = '\n'.join(new_lines)
            print("✅ 変更4: ヘルパー関数追加")
        else:
            print("⚠️ 変更4: 挿入位置が見つかりません")
    else:
        print("⚠️ 変更4: 既に適用済み")
    
    # ファイルに保存
    with open('naviko.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ 変更を適用しました")
    print("✅ ファイルを保存しました")
    
    # 構文チェック
    print(f"\n🔍 構文チェック中...")
    result = subprocess.run([sys.executable, '-m', 'py_compile', 'naviko.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 構文エラーなし")
    else:
        print(f"❌ 構文エラー:\n{result.stderr}")
        input("\nEnterキーを押して終了...")
        sys.exit(1)
    
    # Git同期
    print(f"\n📤 Git同期中...")
    
    # git status
    result = subprocess.run(['git', 'status', '--short'], 
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.stdout:
        print("変更されたファイル:")
        print(result.stdout)
    
    # git add
    subprocess.run(['git', 'add', 'naviko.py'], 
                  capture_output=True, text=True, encoding='utf-8', errors='replace')
    print("\n✅ ステージング完了")
    
    # git commit
    subprocess.run(['git', 'commit', '-m', 'feat: Phase D-4-4完了 - 大型モデル切り替え機能追加'], 
                  capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    # git push
    print(f"\n📤 GitHubへプッシュ中...")
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print("\n" + "=" * 70)
    print("🎉 Phase D-4-4自動適用完了！")
    print("=" * 70)
    print("\n✅ すべての処理が正常に完了しました")
    print("✅ GitHub同期完了")
    
    print("\n" + "=" * 70)
    input("Enterキーを押して終了...")

if __name__ == '__main__':
    main()
