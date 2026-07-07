# voice_wakeword.py
"""
Vosk完全オフライン音声起動システム
ネットワーク不要・ローカルPC内で完結する音声認識
"""
import vosk
import pyaudio
import json
import threading
import queue
import time

class VoiceWakeWordDetector:
    """
    完全オフライン音声起動システム
    
    Features:
    - ネットワーク不要（Voskローカルモデル使用）
    - バックグラウンド音声認識
    - カスタマイズ可能なウェイクワード
    - 軽量・高速（小型モデル: CPU 5-10%）
    
    Usage:
        detector = VoiceWakeWordDetector(model_path)
        detector.start_listening(callback_function)
        # ... 音声起動待機 ...
        detector.stop_listening()
    """
    
    def __init__(self, model_path, wake_words=None):
        """
        初期化
        
        Args:
            model_path (str): Voskモデルのパス
                例: "vosk_models/vosk-model-small-ja-0.22"
            wake_words (list, optional): 起動キーワードのリスト
                デフォルト: ["ナビ子", "なびこ", "ナビコ"]
        """
        # Voskモデルの読み込み
        try:
            print(f"🔄 Voskモデルを読み込み中: {model_path}")
            self.model = vosk.Model(model_path)
            print(f"✅ Voskモデル読み込み完了")
        except Exception as e:
            raise RuntimeError(f"Voskモデルの読み込みに失敗: {e}")
        
        # ウェイクワード設定
        if wake_words is None:
            wake_words = ["ナビ子", "なびこ", "ナビコ"]
        self.wake_words = [w.lower() for w in wake_words]
        print(f"🎤 ウェイクワード設定: {self.wake_words}")
        
        # 内部状態
        self.is_listening = False
        self.callback = None
        self.recognition_thread = None
        
    def start_listening(self, callback):
        """
        バックグラウンド音声認識開始
        
        Args:
            callback (function): ウェイクワード検出時に呼ばれる関数
                シグネチャ: callback(detected_text: str)
        """
        if self.is_listening:
            print("⚠️ 既に音声認識中です")
            return
        
        self.callback = callback
        self.is_listening = True
        
        # 音声認識スレッド開始
        self.recognition_thread = threading.Thread(
            target=self._recognition_loop,
            daemon=True
        )
        self.recognition_thread.start()
        print("✅ バックグラウンド音声認識開始")
        
    def stop_listening(self):
        """音声認識停止"""
        if not self.is_listening:
            print("⚠️ 音声認識は既に停止しています")
            return
        
        self.is_listening = False
        if self.recognition_thread:
            self.recognition_thread.join(timeout=2.0)
        print("🔇 バックグラウンド音声認識停止")
        
    def _recognition_loop(self):
        """
        音声認識ループ（バックグラウンドスレッド）
        
        このメソッドは別スレッドで実行され、マイク入力を常時監視します。
        """
        # PyAudio初期化
        p = pyaudio.PyAudio()
        
        try:
            # マイクストリーム開始
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192
            )
            stream.start_stream()
            
            # Vosk認識器初期化
            rec = vosk.KaldiRecognizer(self.model, 16000)
            rec.SetWords(True)  # 単語単位で認識
            
            print("🎤 音声起動待機中...（'hey、ナビ子'と呼んでください）")
            
            # メインループ
            while self.is_listening:
                try:
                    # 音声データ取得
                    data = stream.read(4096, exception_on_overflow=False)
                    
                    # 音声認識
                    if rec.AcceptWaveform(data):
                        # 完全な文として認識された場合
                        result = json.loads(rec.Result())
                        text = result.get("text", "").lower()
                        
                        # ウェイクワード検出
                        if self._detect_wake_word(text):
                            print(f"✅ ウェイクワード検出: {text}")
                            if self.callback:
                                self.callback(text)
                    else:
                        # 部分的な認識結果もチェック
                        partial = json.loads(rec.PartialResult())
                        text = partial.get("partial", "").lower()
                        
                        # 部分一致でも検出（より敏感に反応）
                        if self._detect_wake_word(text):
                            print(f"✅ ウェイクワード検出（部分）: {text}")
                            if self.callback:
                                self.callback(text)
                
                except Exception as e:
                    # マイク入力エラーは無視して続行
                    if self.is_listening:
                        print(f"⚠️ 音声入力エラー（継続中）: {e}")
                    time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ 音声認識エラー: {e}")
        
        finally:
            # クリーンアップ
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
            p.terminate()
            print("🔇 音声認識スレッド終了")
        
    def _detect_wake_word(self, text):
        """
        ウェイクワード検出
        
        Args:
            text (str): 認識されたテキスト（小文字）
            
        Returns:
            bool: ウェイクワードが含まれているか
        """
        # 空文字チェック
        if not text or len(text.strip()) == 0:
            return False
        
        # 直接マッチ
        for wake_word in self.wake_words:
            if wake_word in text:
                return True
        
        # "hey"+"ナビ子"の組み合わせ
        greeting_words = ["hey", "ねぇ", "ねえ", "ね", "おい"]
        has_greeting = any(g in text for g in greeting_words)
        has_wake_word = any(w in text for w in self.wake_words)
        
        if has_greeting and has_wake_word:
            return True
        
        return False


# ============================================================
# テスト用コード（このファイルを直接実行した場合のみ動作）
# ============================================================

def test_wake_word_detection():
    """
    VoiceWakeWordDetectorの動作テスト
    
    Usage:
        python voice_wakeword.py
    """
    print("=" * 60)
    print("🔊 Vosk音声起動システム - 動作テスト")
    print("=" * 60)
    
    # モデルパス設定
    model_path = "vosk_models/vosk-model-small-ja-0.22"
    
    # コールバック関数
    def on_wake_word_detected(text):
        print(f"\n🎉 ウェイクワード検出成功！")
        print(f"   認識テキスト: {text}")
        print(f"\n   ナビ子が起動します...\n")
    
    try:
        # VoiceWakeWordDetector初期化
        detector = VoiceWakeWordDetector(model_path)
        
        # 音声認識開始
        detector.start_listening(on_wake_word_detected)
        
        print("\n📢 テスト手順:")
        print("   1. マイクに向かって「hey、ナビ子」と話してください")
        print("   2. または「ナビ子」単体でも反応します")
        print("   3. 30秒後に自動終了します")
        print("   4. Ctrl+Cで途中終了できます")
        print("\n待機中...\n")
        
        # 30秒待機
        time.sleep(30)
        
        # 音声認識停止
        detector.stop_listening()
        
        print("\n" + "=" * 60)
        print("✅ テスト完了")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ ユーザーによる中断")
        detector.stop_listening()
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_wake_word_detection()