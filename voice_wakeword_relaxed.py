# voice_wakeword_relaxed.py
"""
Vosk音声認識 緩和版
ウェイクワード検出条件を緩和（「ナビ」単体で検出）
"""
import vosk
import pyaudio
import json
import threading
import time

class VoiceWakeWordDetectorRelaxed:
    """
    緩和版：「ナビ」を含む発話で検出
    """
    
    def __init__(self, model_path, wake_words=None):
        """初期化"""
        try:
            print(f"🔄 Voskモデルを読み込み中: {model_path}")
            self.model = vosk.Model(model_path)
            print(f"✅ Voskモデル読み込み完了")
        except Exception as e:
            raise RuntimeError(f"Voskモデルの読み込みに失敗: {e}")
        
        # 緩和版ウェイクワード（「ナビ」単体で検出）
        if wake_words is None:
            wake_words = [
                "ナビ", "なび", "ナビコ",  # 基本
                "日 木", "なぁ 日",  # 誤認識パターン
            ]
        self.wake_words = [w.lower() for w in wake_words]
        print(f"🎤 ウェイクワード設定（緩和版）: {self.wake_words}")
        
        self.is_listening = False
        self.callback = None
        self.recognition_thread = None
        
    def start_listening(self, callback):
        """バックグラウンド音声認識開始"""
        if self.is_listening:
            print("⚠️ 既に音声認識中です")
            return
        
        self.callback = callback
        self.is_listening = True
        
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
        """音声認識ループ（緩和版）"""
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192
            )
            stream.start_stream()
            
            rec = vosk.KaldiRecognizer(self.model, 16000)
            rec.SetWords(True)
            
            print("🎤 音声認識開始...（緩和版 - 「ナビ」を含む発話で検出）")
            print("=" * 60)
            
            while self.is_listening:
                try:
                    data = stream.read(4096, exception_on_overflow=False)
                    
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "")
                        
                        if text:
                            print(f"✅ 認識（完全）: {text}")
                            
                            # ウェイクワード検出チェック（緩和版）
                            text_lower = text.lower()
                            if self._detect_wake_word(text_lower):
                                print(f"🎉 ウェイクワード検出！")
                                if self.callback:
                                    self.callback(text)
                    else:
                        partial = json.loads(rec.PartialResult())
                        text = partial.get("partial", "")
                        
                        if text:
                            # 部分認識の表示を少なく（最後の部分のみ）
                            # print(f"⏳ 認識（部分）: {text}")
                            pass
                            
                            # 部分一致でも検出チェック（緩和版）
                            text_lower = text.lower()
                            if self._detect_wake_word(text_lower):
                                print(f"⏳ 認識（部分）: {text}")
                                print(f"🎉 ウェイクワード検出（部分）！")
                                if self.callback:
                                    self.callback(text)
                
                except Exception as e:
                    if self.is_listening:
                        print(f"⚠️ 音声入力エラー: {e}")
                    time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ 音声認識エラー: {e}")
        
        finally:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
            p.terminate()
            print("🔇 音声認識スレッド終了")
        
    def _detect_wake_word(self, text):
        """ウェイクワード検出（緩和版）"""
        if not text or len(text.strip()) == 0:
            return False
        
        # 緩和版：「ナビ」を含む or 誤認識パターンを含む
        for wake_word in self.wake_words:
            if wake_word in text:
                print(f"  → マッチ検出: '{wake_word}' in '{text}'")
                return True
        
        return False


def test_wake_word_detection_relaxed():
    """緩和版テスト"""
    print("=" * 60)
    print("🔊 Vosk音声起動システム - 緩和版テスト")
    print("=" * 60)
    
    model_path = "vosk_models/vosk-model-small-ja-0.22"
    
    def on_wake_word_detected(text):
        print(f"\n🎉 ウェイクワード検出成功！")
        print(f"   認識テキスト: {text}")
        print(f"\n   ナビ子が起動します...\n")
    
    try:
        detector = VoiceWakeWordDetectorRelaxed(model_path)
        detector.start_listening(on_wake_word_detected)
        
        print("\n📢 緩和版テスト手順:")
        print("   1. マイクに向かって「ナビ子」と話してください")
        print("   2. 「ナビ」を含む発話で検出されます")
        print("   3. 60秒後に自動終了します")
        print("   4. Ctrl+Cで途中終了できます")
        print("\n話してください...\n")
        
        time.sleep(60)
        
        detector.stop_listening()
        
        print("\n" + "=" * 60)
        print("✅ 緩和版テスト完了")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ ユーザーによる中断")
        detector.stop_listening()
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_wake_word_detection_relaxed()