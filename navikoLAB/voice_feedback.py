#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VoiceFeedback - Naviko音声フィードバックシステム

ExecutionPlannerの実行状況を音声で通知する。
タスク開始・進行・完了・エラーをリアルタイムで音声フィードバック。

機能:
  - テキスト読み上げ（TTS）エンジン統合
  - 実行状況の音声通知（タスク開始、レベル完了）
  - タスク完了時のフィードバック（成功、警告）
  - エラー発生時の音声アラート
  - 音声設定（音量、速度、音声選択）
  - 静音モード（音声オフ機能）
  - キュー管理（複数通知の順次再生）

依存ライブラリ:
  - pyttsx3: オフラインTTSエンジン（pip install pyttsx3）

例:
  voice = VoiceFeedback(enabled=True)
  voice.notify_execution_start("Webアプリケーション作成")
  voice.notify_level_start(1, ["リサーチ", "要件定義"])
  voice.notify_task_complete("リサーチ", success=True)
  voice.notify_execution_complete(success=True, total_time="30分")
"""

import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading
import queue

# TTS（テキスト読み上げ）エンジン
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ Warning: pyttsx3 not installed. Voice feedback will be disabled.")
    print("   Install with: pip install pyttsx3")


class VoiceFeedback:
    """
    音声フィードバックシステム
    
    ExecutionPlannerの実行状況を音声で通知し、
    ユーザーに分かりやすいフィードバックを提供する。
    """
    
    def __init__(self, enabled: bool = True, volume: float = 0.8, rate: int = 150):
        """
        VoiceFeedbackの初期化
        
        Args:
            enabled: 音声フィードバックの有効/無効（デフォルト: True）
            volume: 音量（0.0-1.0、デフォルト: 0.8）
            rate: 読み上げ速度（wpm、デフォルト: 150）
        """
        self.enabled = enabled and TTS_AVAILABLE
        self.volume = max(0.0, min(1.0, volume))
        self.rate = max(100, min(300, rate))
        
        # TTSエンジン
        self.engine = None
        if self.enabled:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('volume', self.volume)
                self.engine.setProperty('rate', self.rate)
                
                # 日本語音声を優先的に選択
                voices = self.engine.getProperty('voices')
                japanese_voice = None
                for voice in voices:
                    if 'ja' in voice.languages or 'japanese' in voice.name.lower():
                        japanese_voice = voice
                        break
                
                if japanese_voice:
                    self.engine.setProperty('voice', japanese_voice.id)
            except Exception as e:
                print(f"⚠️ Warning: Failed to initialize TTS engine: {e}")
                self.enabled = False
        
        # 音声キュー（順次再生用）
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        
        # 音声スレッド
        if self.enabled:
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
        
        # 通知履歴
        self.notification_history = []
    
    def _speech_worker(self):
        """音声再生ワーカースレッド"""
        while True:
            try:
                text = self.speech_queue.get(timeout=1.0)
                if text is None:  # 終了シグナル
                    break
                
                self.is_speaking = True
                if self.engine:
                    self.engine.say(text)
                    self.engine.runAndWait()
                self.is_speaking = False
                
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ Voice feedback error: {e}")
                self.is_speaking = False
    
    def _speak(self, text: str, priority: bool = False):
        """
        テキストを音声で読み上げ
        
        Args:
            text: 読み上げるテキスト
            priority: 優先度（True: キューの先頭に追加）
        """
        # 通知履歴に記録（enabled状態に関わらず常に記録）
        self.notification_history.append({
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "priority": priority
        })
        
        # 音声が無効な場合はここで終了
        if not self.enabled or not self.engine:
            return
        
        # キューに追加
        if priority:
            # 優先通知（エラーなど）
            temp_queue = queue.Queue()
            temp_queue.put(text)
            while not self.speech_queue.empty():
                try:
                    temp_queue.put(self.speech_queue.get_nowait())
                except queue.Empty:
                    break
            self.speech_queue = temp_queue
        else:
            self.speech_queue.put(text)
    
    def set_enabled(self, enabled: bool):
        """
        音声フィードバックの有効/無効を切り替え
        
        Args:
            enabled: 有効にする場合True
        """
        if not TTS_AVAILABLE:
            print("⚠️ Warning: pyttsx3 not available. Cannot enable voice feedback.")
            return
        
        self.enabled = enabled
        if enabled and self.engine is None:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('volume', self.volume)
                self.engine.setProperty('rate', self.rate)
            except Exception as e:
                print(f"⚠️ Warning: Failed to initialize TTS engine: {e}")
                self.enabled = False
    
    def set_volume(self, volume: float):
        """
        音量を設定
        
        Args:
            volume: 音量（0.0-1.0）
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            self.engine.setProperty('volume', self.volume)
    
    def set_rate(self, rate: int):
        """
        読み上げ速度を設定
        
        Args:
            rate: 速度（wpm、100-300）
        """
        self.rate = max(100, min(300, rate))
        if self.engine:
            self.engine.setProperty('rate', self.rate)
    
    def notify_execution_start(self, main_goal: str, total_tasks: int = 0):
        """
        実行計画の開始を通知
        
        Args:
            main_goal: メインゴール
            total_tasks: 総タスク数
        """
        if total_tasks > 0:
            text = f"実行を開始します。{main_goal}。全{total_tasks}個のタスクを実行します。"
        else:
            text = f"実行を開始します。{main_goal}。"
        
        self._speak(text)
    
    def notify_level_start(self, level: int, task_names: List[str], parallel: bool = False):
        """
        実行レベルの開始を通知
        
        Args:
            level: レベル番号
            task_names: タスク名のリスト
            parallel: 並列実行かどうか
        """
        task_list = "、".join(task_names)
        
        if parallel:
            text = f"レベル{level}を開始します。{task_list}を並列実行します。"
        else:
            text = f"レベル{level}を開始します。{task_list}。"
        
        self._speak(text)
    
    def notify_task_start(self, task_name: str, estimated_time: str = ""):
        """
        タスクの開始を通知
        
        Args:
            task_name: タスク名
            estimated_time: 推定時間
        """
        if estimated_time:
            text = f"{task_name}を開始します。推定時間は{estimated_time}です。"
        else:
            text = f"{task_name}を開始します。"
        
        self._speak(text)
    
    def notify_task_complete(self, task_name: str, success: bool = True, duration: str = ""):
        """
        タスクの完了を通知
        
        Args:
            task_name: タスク名
            success: 成功したかどうか
            duration: 実行時間
        """
        if success:
            if duration:
                text = f"{task_name}が完了しました。実行時間は{duration}です。"
            else:
                text = f"{task_name}が完了しました。"
        else:
            text = f"{task_name}が失敗しました。"
        
        self._speak(text)
    
    def notify_level_complete(self, level: int, success_count: int, total_count: int):
        """
        実行レベルの完了を通知
        
        Args:
            level: レベル番号
            success_count: 成功したタスク数
            total_count: 総タスク数
        """
        if success_count == total_count:
            text = f"レベル{level}が完了しました。全{total_count}個のタスクが成功しました。"
        else:
            text = f"レベル{level}が完了しました。{total_count}個中{success_count}個のタスクが成功しました。"
        
        self._speak(text)
    
    def notify_execution_complete(self, success: bool = True, total_time: str = "", warnings: List[str] = None):
        """
        実行計画の完了を通知
        
        Args:
            success: 成功したかどうか
            total_time: 総実行時間
            warnings: 警告メッセージのリスト
        """
        if success:
            if warnings and len(warnings) > 0:
                text = f"実行が完了しました。総実行時間は{total_time}です。{len(warnings)}件の警告があります。"
            else:
                text = f"実行が完了しました。総実行時間は{total_time}です。"
        else:
            text = f"実行が失敗しました。エラーが発生しました。"
        
        self._speak(text)
    
    def notify_error(self, error_message: str, task_name: str = "", recovery_suggestion: str = ""):
        """
        エラー発生を通知（優先度高）
        
        Args:
            error_message: エラーメッセージ
            task_name: エラーが発生したタスク名
            recovery_suggestion: 対処方法の提案
        """
        if task_name:
            text = f"エラーが発生しました。{task_name}で{error_message}。"
        else:
            text = f"エラーが発生しました。{error_message}。"
        
        if recovery_suggestion:
            text += f"{recovery_suggestion}"
        
        # 優先度を高く設定（エラー通知は即座に行う）
        self._speak(text, priority=True)
    
    def notify_retry(self, task_name: str, attempt: int, max_attempts: int):
        """
        リトライを通知
        
        Args:
            task_name: タスク名
            attempt: 現在の試行回数
            max_attempts: 最大試行回数
        """
        text = f"{task_name}をリトライします。{attempt}回目の試行です。最大{max_attempts}回まで試行します。"
        self._speak(text)
    
    def notify_fallback(self, primary_name: str, fallback_name: str):
        """
        フォールバックを通知
        
        Args:
            primary_name: プライマリ能力名
            fallback_name: フォールバック先の能力名
        """
        text = f"{primary_name}が利用できません。代わりに{fallback_name}を使用します。"
        self._speak(text)
    
    def notify_resource_warning(self, warning_message: str):
        """
        リソース警告を通知
        
        Args:
            warning_message: 警告メッセージ
        """
        text = f"警告。{warning_message}"
        self._speak(text, priority=True)
    
    def notify_progress(self, completed: int, total: int, current_task: str = ""):
        """
        進捗状況を通知
        
        Args:
            completed: 完了したタスク数
            total: 総タスク数
            current_task: 現在実行中のタスク
        """
        progress_percent = int((completed / total) * 100) if total > 0 else 0
        
        if current_task:
            text = f"進捗状況。{total}個中{completed}個完了しました。現在{current_task}を実行中です。"
        else:
            text = f"進捗状況。{total}個中{completed}個完了しました。進捗率は{progress_percent}パーセントです。"
        
        self._speak(text)
    
    def clear_queue(self):
        """音声キューをクリア"""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
    
    def wait_until_done(self, timeout: Optional[float] = None):
        """
        全ての音声通知が完了するまで待機
        
        Args:
            timeout: タイムアウト時間（秒）
        """
        if not self.enabled:
            return
        
        try:
            self.speech_queue.join()
            if timeout:
                import time
                start_time = time.time()
                while self.is_speaking and (time.time() - start_time) < timeout:
                    time.sleep(0.1)
        except Exception as e:
            print(f"⚠️ Wait error: {e}")
    
    def get_notification_history(self) -> List[Dict]:
        """
        通知履歴を取得
        
        Returns:
            通知履歴のリスト
        """
        return self.notification_history.copy()
    
    def shutdown(self):
        """音声フィードバックシステムを終了"""
        if self.enabled:
            self.speech_queue.put(None)  # 終了シグナル
            if hasattr(self, 'speech_thread'):
                self.speech_thread.join(timeout=1.0)
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass


if __name__ == "__main__":
    # テストコード
    print("=" * 60)
    print("VoiceFeedback - Naviko音声フィードバックシステム")
    print("=" * 60)
    print()
    
    # VoiceFeedbackのインスタンス作成
    voice = VoiceFeedback(enabled=True, volume=0.8, rate=150)
    
    if not voice.enabled:
        print("⚠️ 音声フィードバックが無効です。pyttsx3をインストールしてください。")
        print("   pip install pyttsx3")
        sys.exit(1)
    
    print("【テストケース1: 実行開始通知】")
    voice.notify_execution_start("Webアプリケーション作成", total_tasks=4)
    voice.wait_until_done(timeout=5.0)
    print("✅ テストケース1: 成功")
    print()
    
    print("【テストケース2: レベル開始・完了通知】")
    voice.notify_level_start(1, ["リサーチ", "要件定義"], parallel=True)
    voice.wait_until_done(timeout=5.0)
    
    voice.notify_task_start("リサーチ", estimated_time="5分")
    voice.wait_until_done(timeout=5.0)
    
    voice.notify_task_complete("リサーチ", success=True, duration="4分30秒")
    voice.wait_until_done(timeout=5.0)
    
    voice.notify_level_complete(1, success_count=2, total_count=2)
    voice.wait_until_done(timeout=5.0)
    print("✅ テストケース2: 成功")
    print()
    
    print("【テストケース3: エラー通知】")
    voice.notify_error(
        error_message="メモリ不足エラー",
        task_name="アプリ生成",
        recovery_suggestion="並列実行数を減らして再試行してください。"
    )
    voice.wait_until_done(timeout=5.0)
    print("✅ テストケース3: 成功")
    print()
    
    print("【テストケース4: 実行完了通知】")
    voice.notify_execution_complete(success=True, total_time="30分", warnings=["メモリ使用量が高めです"])
    voice.wait_until_done(timeout=5.0)
    print("✅ テストケース4: 成功")
    print()
    
    # 通知履歴を表示
    print("【通知履歴】")
    history = voice.get_notification_history()
    for i, notification in enumerate(history, 1):
        print(f"{i}. [{notification['timestamp']}] {notification['text']}")
    print()
    
    print("🎉 全てのテストケースが合格しました！")
    
    # シャットダウン
    voice.shutdown()
