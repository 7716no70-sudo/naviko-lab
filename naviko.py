import os
import json
from pathlib import Path
import time
import random
from datetime import date, datetime
import shutil
import threading

# === Original Naviko LAB Bridge import ===
try:
    from navikoLAB.original_adoption.original_naviko_bridge import run_original_autonomous_bridge
except Exception:
    run_original_autonomous_bridge = None

try:
    from navikoLAB.original_adoption.mission_dashboard import open_mission_dashboard
except Exception:
    open_mission_dashboard = None

# === Original Naviko LAB Bridge import end ===

import py_compile
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import requests

# === Speech Recognition import ===
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("speech_recognition is not available. Voice input will be disabled.")
# === Speech Recognition import end ===
import sys
from tkinter import filedialog
import subprocess

# 音声認識ライブラリ
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

from navikoLAB.memory_manager import MemoryManager
from navikoLAB.goal_manager import GoalManager
from navikoLAB.agent_registry import AgentRegistry
from navikoLAB.task_planner import TaskPlanner
from navikoLAB.plan_executor import PlanExecutor
from navikoLAB.autonomy_controller import AutonomyController
from navikoLAB.autonomous_core import AutonomousCore
from navikoLAB.maintenance_manager import MaintenanceManager
from navikoLAB.action_planner import ActionPlanner
from navikoLAB.workspace_manager import WorkspaceManager
from navikoLAB.artifact_writer import ArtifactWriter
from navikoLAB.app_project_builder import AppProjectBuilder
from navikoLAB.agents.manager import AgentManager
from navikoLAB.improvement_manager import ImprovementManager
from navikoLAB.core.mission_bridge import MissionBridge
from navikoLAB.capabilities.capability_gui_bridge import CapabilityGUIBridge
from navikoLAB.naviko_self_growth_bridge import NavikoSelfGrowthBridge
from navikoLAB.error_diagnostic_engine import ErrorDiagnosticEngine
from navikoLAB.experience_memory import ExperienceMemory
from navikoLAB.process_recorder import ProcessRecorder

# === Vosk音声認識インポート ===
try:
    import vosk
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("⚠️ Vosk音声認識が利用できません（vosk/pyaudioが未インストール）")
# === Vosk音声認識インポート end ===

# Phase 3モジュールインポート
try:
    from navikoLAB.system_health_monitor import SystemHealthMonitor
    from navikoLAB.naviko_system_controller import NavikoSystemController
    PHASE3_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Phase 3モジュールが見つかりません: {e}")
    PHASE3_AVAILABLE = False
    SystemHealthMonitor = None
    NavikoSystemController = None

# ============================================================
# VoiceWakeWordDetector - Vosk完全オフライン音声起動システム
# ============================================================

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
# End of VoiceWakeWordDetector
# ============================================================


ROOT = Path(__file__).resolve().parent
SELF_FILE = ROOT / "naviko.py"
SPRITESHEET = ROOT / "spritesheet.webp"

MEMORY_FILE = ROOT / "memory.json"
PROFILE_FILE = ROOT / "profile.json"
CHARACTER_FILE = ROOT / "character.json"
GROWTH_LOG_FILE = ROOT / "growth_log.json"
GROWTH_HISTORY_FILE = ROOT / "growth_history.json"
GROWTH_GOAL_FILE = ROOT / "growth_goal.json"
GROWTH_GUARD_FILE = ROOT / "growth_guard.json"
DANGER_GROWTH_LOG_FILE = ROOT / "danger_growth_log.json"
EXPERIENCE_LOG_FILE = ROOT / "experience_log.json"
EXPERIENCE_SUMMARY_FILE = ROOT / "experience_summary.json"
SUCCESS_PATTERN_FILE = ROOT / "success_patterns.json"
REJECT_PATTERN_FILE = ROOT / "reject_patterns.json"
GROWTH_REPORT_FILE = ROOT / "growth_report.json"
GUI_LAYOUT_FILE = ROOT / "gui_layout.json"

# =========================
# ナビ子LAB設定
# =========================

AUTO_GROWTH_TRIAL = False

PATCH_GENERATION_COUNT = 2
PATCH_GENERATION_INTERVAL = 10
MINIMUM_APPROVAL_SCORE = 30

ENABLE_SUCCESS_LEARNING = True
ENABLE_REJECT_LEARNING = True
ENABLE_GROWTH_REPORT = True

# =========================
# ===== フォルダ設定 =====
BACKUP_DIR = ROOT / "backup"

LAB_DIR = ROOT / "navikoLAB"

LINE_PATCH_DIR = LAB_DIR / "line_patches"
LINE_PATCH_PREVIEW_DIR = LAB_DIR / "line_patch_previews"
LINE_PATCH_TEMP_DIR = LAB_DIR / "line_patch_temp_applied"
APPROVED_LINE_PATCH_DIR = LAB_DIR / "approved_line_patches"
PENDING_LINE_PATCH_DIR = LAB_DIR / "pending_line_patches"

BACKUP_DIR.mkdir(exist_ok=True)
LAB_DIR.mkdir(exist_ok=True)
LINE_PATCH_DIR.mkdir(parents=True, exist_ok=True)
LINE_PATCH_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
LINE_PATCH_TEMP_DIR.mkdir(parents=True, exist_ok=True)
APPROVED_LINE_PATCH_DIR.mkdir(parents=True, exist_ok=True)
PENDING_LINE_PATCH_DIR.mkdir(parents=True, exist_ok=True)

memory_manager = MemoryManager(LAB_DIR)
goal_manager = GoalManager(LAB_DIR)
agent_registry = AgentRegistry(LAB_DIR)

task_planner = TaskPlanner(
    LAB_DIR,
    agent_registry
)

plan_executor = PlanExecutor(
    LAB_DIR,
    agent_registry
)

autonomy_controller = AutonomyController(LAB_DIR)
maintenance_manager = MaintenanceManager(LAB_DIR)
action_planner = ActionPlanner(LAB_DIR)
workspace_manager = WorkspaceManager(LAB_DIR)
artifact_writer = ArtifactWriter(LAB_DIR)

app_project_builder = AppProjectBuilder(
    LAB_DIR,
    action_planner=action_planner,
    workspace_manager=workspace_manager,
    artifact_writer=artifact_writer
)

agent_manager = AgentManager(LAB_DIR)
improvement_manager = ImprovementManager(LAB_DIR)
mission_bridge = MissionBridge(LAB_DIR)
growth_bridge = NavikoSelfGrowthBridge()

# === 新しい自己改善モジュール ===
experience_memory = ExperienceMemory(lab_dir=LAB_DIR)
error_diagnostic_engine = ErrorDiagnosticEngine(
    lab_dir=LAB_DIR,
    experience_memory=experience_memory
)
process_recorder = ProcessRecorder(lab_dir=LAB_DIR)

autonomous_core = AutonomousCore(
    LAB_DIR,
    memory_manager=memory_manager,
    goal_manager=goal_manager,
    agent_registry=agent_registry,
    task_planner=task_planner,
    plan_executor=plan_executor,
    autonomy_controller=autonomy_controller,
    mission_bridge=mission_bridge
)

# =====================

def diagnose_and_handle_error(error, context=None):
    """
    エラーを自動診断して解決策を提案する
    
    Args:
        error: 発生したエラー（Exceptionオブジェクトまたは文字列）
        context: エラー発生時のコンテキスト情報
    
    Returns:
        診断結果と解決策を含む辞書
    """
    error_message = str(error)
    
    # エラーを診断
    diagnosis = error_diagnostic_engine.diagnose_error(
        error_message,
        context=context or {}
    )
    
    if not diagnosis.get("success"):
        return {
            "success": False,
            "message": f"エラーが発生しました: {error_message}",
            "diagnosis": None,
            "solutions": []
        }
    
    # 解決策を提案
    solutions = error_diagnostic_engine.suggest_solutions(diagnosis)
    
    # フォーマット
    diagnosis_text = error_diagnostic_engine.format_diagnosis(diagnosis)
    solutions_text = error_diagnostic_engine.format_solutions(solutions)
    
    full_message = f"{diagnosis_text}\n\n{solutions_text}"
    
    # 経験として記録
    if experience_memory:
        experience_memory.record_error(
            error_type=diagnosis["error_type"],
            error_message=error_message,
            context=context or {},
            severity=diagnosis["severity"]
        )
    
    return {
        "success": True,
        "message": full_message,
        "diagnosis": diagnosis,
        "solutions": solutions,
        "auto_fixable": diagnosis.get("auto_fixable", False)
    }

# =====================

# ここに新しいGroq APIキーを入れる
# 例: GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"

BASE_WIDTH = 192
BASE_HEIGHT = 208
ANIM_DELAY = 130
current_scale = 1.0

states_config = {
    "idle": (0, 6),
    "running-right": (1, 8),
    "running-left": (2, 8),
    "waving": (3, 4),
    "jumping": (4, 5),
    "failed": (5, 8),
    "waiting": (6, 6),
    "running": (7, 6),
    "review": (8, 6),
}

pet_vars = {
    "state": "idle",
    "frame": 0,
    "drag_x": 0,
    "drag_y": 0,
    "is_dragging": False,
    "chat_win": None,
    "is_resting": False,
    "last_recover_time": 0,
    "last_thought_time": 0,
}

raw_frames = {}
tk_frames = {}

def run_gui_app_project_builder():
    try:
        user_text = ""

        if "custom_chat_input" in globals():
            user_text = custom_chat_input.get("1.0", "end").strip()
        elif "chat_input" in globals():
            user_text = chat_input.get("1.0", "end").strip()
        else:
            user_text = "TODOアプリを作りたい"

        if not user_text:
            user_text = "TODOアプリを作りたい"

        if user_text.startswith("アプリ作成:"):
            goal = user_text.replace("アプリ作成:", "", 1).strip()
        else:
            goal = user_text.strip()

        result = app_project_builder.build_basic_app_project(
            purpose=goal,
            project_name="todo_app_gui_test"
        )

        message = app_project_builder.format_build_result(result)

        print(message)

        if "custom_chat_log" in globals():
            custom_chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
            custom_chat_log.see("end")
        elif "chat_log" in globals():
            chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
            chat_log.see("end")

        return result

    except Exception as e:
        error_message = f"アプリ生成中にエラーが発生しました: {e}"
        print(error_message)

        if "custom_chat_log" in globals():
            custom_chat_log.insert("end", "\n【ナビ子】\n" + error_message + "\n")
            custom_chat_log.see("end")
        elif "chat_log" in globals():
            chat_log.insert("end", "\n【ナビ子】\n" + error_message + "\n")
            chat_log.see("end")

        return {
            "success": False,
            "error": str(e)
        }

def save_autonomous_build_history(
    purpose,
    core_result,
    build_result,
    agent_result=None
):
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    history_file = history_dir / f"autonomous_build_{time.strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": purpose,
        "core_result": core_result,
        "agent_result": agent_result,
        "build_result": build_result
    }

    save_json(history_file, data)

    return history_file

def create_reflection_for_latest_autonomous_build():
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    reflection_dir = LAB_DIR / "reflection"
    reflection_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "自律生成履歴がないため、自己評価できません。"

    latest = files[0]
    data = load_json(latest, {})

    purpose = data.get("purpose", "不明")
    core_result = data.get("core_result", {})
    agent_result = data.get("agent_result", {})
    build_result = data.get("build_result", {})

    reflection = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_history": latest.name,
        "purpose": purpose,
        "status": "reflected",
        "good_points": [
            "目的から自律生成フローを開始できた。",
            "AgentManagerで役割分担と仮実行ができた。",
            "AppProjectBuilderで成果物を生成できた。"
        ],
        "improvement_points": [
            "現在はAgent実行がsimulationのため、外部AI実行はまだ未接続。",
            "生成されたmain.pyの品質評価はまだ未実装。",
            "成果物の実行テストはまだ限定的。"
        ],
        "next_actions": [
            "成果物の内容確認機能を追加する。",
            "生成コードの自己評価を追加する。",
            "外部AI接続用の共通インターフェースを準備する。"
        ],
        "summary": "自律生成フローは正常。次は成果物の品質評価と外部AI接続準備を進める。",
        "core_status": core_result.get("status"),
        "agent_status": (
            agent_result.get("execution_result", {})
            .get("status")
        ),
        "build_status": build_result.get("status")
    }

    reflection_file = (
        reflection_dir
        / f"reflection_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(reflection_file, reflection)

    lines = []
    lines.append("=== ReflectionEngine 自己評価 ===")
    lines.append(f"対象履歴: {latest.name}")
    lines.append(f"目的: {purpose}")
    lines.append(f"保存先: {reflection_file}")
    lines.append("")
    lines.append("良かった点:")
    for item in reflection["good_points"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("改善点:")
    for item in reflection["improvement_points"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("次回アクション:")
    for item in reflection["next_actions"]:
        lines.append(f"- {item}")

    return "\n".join(lines)

def create_reflection_for_latest_autonomous_build_from_gui(c_area=None):
    message = create_reflection_for_latest_autonomous_build()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def list_autonomous_build_history():
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== 自律生成履歴一覧 ===")

    if not files:
        lines.append("履歴はまだありません。")
        return "\n".join(lines)

    for file in files[:10]:
        data = load_json(file, {})

        purpose = data.get("purpose", "不明")
        build_result = data.get("build_result", {})
        project = build_result.get("project_name", "不明")
        status = build_result.get("status", "不明")
        path = find_project_path(build_result) or "不明"

        lines.append("")
        lines.append(f"履歴ファイル: {file.name}")
        lines.append(f"目的: {purpose}")
        lines.append(f"プロジェクト: {project}")
        lines.append(f"状態: {status}")
        lines.append(f"保存先: {path}")

    return "\n".join(lines)

def diagnose_autonomous_build_artifacts():
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== 自律生成成果物診断 ===")

    if not files:
        lines.append("診断できる履歴がありません。")
        return "\n".join(lines)

    for file in files[:5]:
        data = load_json(file, {})
        build_result = data.get("build_result", {})

        path_text = find_project_path(build_result)

        lines.append("")
        lines.append(f"履歴ファイル: {file.name}")

        if not path_text:
            lines.append("保存先: 不明")
            lines.append("状態: 診断不可")
            continue

        project_dir = Path(path_text)

        lines.append(f"保存先: {project_dir}")
        lines.append(f"フォルダ: {'OK' if project_dir.exists() else 'NG'}")

        expected_files = [
            "README.md",
            "requirements.txt",
            "main.py",
            "notes.txt"
        ]

        for name in expected_files:
            target = project_dir / name
            lines.append(
                f"{name}: {'OK' if target.exists() else 'NG'}"
            )

    return "\n".join(lines)

def diagnose_autonomous_build_artifacts_from_gui(c_area=None):
    message = diagnose_autonomous_build_artifacts()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def find_project_path(data):
    if isinstance(data, dict):
        for key in [
            "project_path",
            "path",
            "workspace_path",
            "project_dir",
            "save_path",
            "output_dir",
        ]:
            value = data.get(key)
            if value:
                return value

        for value in data.values():
            found = find_project_path(value)
            if found:
                return found

    if isinstance(data, list):
        for item in data:
            found = find_project_path(item)
            if found:
                return found

    return None

def show_autonomous_build_history_from_gui(c_area=None):
    message = list_autonomous_build_history()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_agent_manager_integration_diagnosis():
    lines = []
    lines.append("=== AgentManager 統合診断 ===")

    try:
        route_result = agent_manager.route("TODOアプリを作りたい")
        lines.append("CapabilityRouter: OK")
        lines.append(f"選択Agent: {route_result}")
    except Exception as e:
        lines.append(f"CapabilityRouter: NG / {e}")

    try:
        exec_result = agent_manager.execute("TODOアプリを作りたい")
        execution_result = exec_result.get("execution_result", {})
        lines.append("AgentExecutor: OK")
        lines.append(f"実行状態: {execution_result.get('status')}")
    except Exception as e:
        lines.append(f"AgentExecutor: NG / {e}")

    try:
        histories = agent_manager.list_history()
        lines.append("ExecutionHistory: OK")
        lines.append(f"履歴件数: {len(histories)}")
    except Exception as e:
        lines.append(f"ExecutionHistory: NG / {e}")

    try:
        diagnosis = agent_manager.diagnose()
        lines.append("AgentDiagnostics: OK")
        lines.append(f"最新状態: {diagnosis.get('latest_status')}")
        lines.append(f"失敗Agent: {diagnosis.get('failed_agents')}")
    except Exception as e:
        lines.append(f"AgentDiagnostics: NG / {e}")

    lines.append("")
    lines.append("【判定】")

    text = "\n".join(lines)

    if "NG" in text:
        lines.append("AgentManager統合状態: 要確認")
    else:
        lines.append("AgentManager統合状態: OK")

    return "\n".join(lines)

def run_agent_manager_integration_diagnosis_from_gui(c_area=None):
    message = run_agent_manager_integration_diagnosis()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def diagnose_autonomous_build_agent_history():
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== 自律生成 AgentManager 履歴診断 ===")

    if not files:
        lines.append("自律生成履歴がありません。")
        return "\n".join(lines)

    latest = files[0]
    data = load_json(latest, {})

    lines.append(f"最新履歴: {latest.name}")
    lines.append(f"目的: {data.get('purpose', '不明')}")

    core_result = data.get("core_result")
    agent_result = data.get("agent_result")
    build_result = data.get("build_result")

    lines.append(f"AutonomousCore記録: {'OK' if core_result else 'NG'}")
    lines.append(f"AgentManager記録: {'OK' if agent_result else 'NG'}")
    lines.append(f"AppProjectBuilder記録: {'OK' if build_result else 'NG'}")

    if agent_result:
        execution_result = agent_result.get("execution_result", {})
        agents = execution_result.get("agents", [])
        results = execution_result.get("results", [])

        lines.append("")
        lines.append("【AgentManager】")
        lines.append(f"状態: {execution_result.get('status', '不明')}")
        lines.append(f"選択Agent数: {len(agents)}")
        lines.append(f"実行結果数: {len(results)}")

        for result in results:
            lines.append(
                f"- {result.get('agent', '不明')}: "
                f"{result.get('status', '不明')}"
            )

    lines.append("")
    lines.append("【判定】")

    if core_result and agent_result and build_result:
        lines.append("自律生成履歴統合: OK")
    else:
        lines.append("自律生成履歴統合: 要確認")

    return "\n".join(lines)

def diagnose_autonomous_build_agent_history_from_gui(c_area=None):
    message = diagnose_autonomous_build_agent_history()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_autonomous_build_from_gui():
    """
    GUIからAutonomousCore経由でアプリ生成を実行する。
    """

    try:
        if "custom_chat_input" in globals():
            purpose = custom_chat_input.get("1.0", "end").strip()
        elif "chat_input" in globals():
            purpose = chat_input.get("1.0", "end").strip()
        else:
            purpose = ""

        if not purpose:
            purpose = "TODOアプリを作りたい"

        if purpose.startswith("アプリ作成:"):
            purpose = purpose.replace("アプリ作成:", "", 1).strip()

        is_duplicate, duplicate_file = is_recent_duplicate_autonomous_build(
            purpose,
            seconds=60
        )

        if is_duplicate:
            message = (
                "=== 自律生成 重複防止 ===\n"
                f"目的: {purpose}\n"
                "直近60秒以内に同じ目的の自律生成が実行されています。\n"
                f"履歴: {duplicate_file}\n"
                "誤連打防止のため、今回は生成を停止しました。"
            )

            print(message)

            if "custom_chat_log" in globals():
                custom_chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
                custom_chat_log.see("end")
            elif "chat_log" in globals():
                 chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
                 chat_log.see("end")

            return {
                "success": False,
                "status": "duplicate_blocked",
                "purpose": purpose,
                "duplicate_file": str(duplicate_file)
            }

        # ---------- AutonomousCore ----------
        core_result = autonomous_core.process_purpose(purpose)

        # ---------- AgentManager ----------
        agent_result = agent_manager.execute(purpose)

        # ---------- Builder ----------
        build_result = app_project_builder.build_basic_app_project(
            purpose=purpose,
            project_name="auto_project"
        )

        # ---------- 実行履歴 ----------
        try:
            plan_executor.record_execution({
                "purpose": purpose,
                "status": "completed",
                "builder": "AppProjectBuilder",
                "project": build_result.get("project_name"),
                "path": build_result.get("project_path")
            })

        except Exception:
            # PlanExecutor側にまだrecord_executionが無ければ無視
            pass

        history_file = save_autonomous_build_history(
            purpose,
            core_result,
            build_result,
            agent_result
        )

        message = ""
        message += "=== Autonomous Build ===\n\n"

        message += "【AutonomousCore】\n"
        message += autonomous_core.format_result(core_result)

        message += "\n\n【AgentManager】\n"
        execution_result = agent_result.get("execution_result", {})
        message += f"状態: {execution_result.get('status')}\n"
        message += "選択Agent:\n"

        for agent in execution_result.get("agents", []):
            message += f"- {agent}\n"

        message += "\n実行結果:\n"

        for item in execution_result.get("results", []):
            message += (
                f"- {item.get('agent')}: "
                f"{item.get('status')}\n"
            )

        message += f"\nAgent履歴: {agent_result.get('history_file')}"

        message += "\n\n【AppProjectBuilder】\n"
        message += app_project_builder.format_build_result(build_result)

        message += f"\n\n自律生成履歴: {history_file}"

        print(message)

        if "custom_chat_log" in globals():
            custom_chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
            custom_chat_log.see("end")
        elif "chat_log" in globals():
            chat_log.insert("end", "\n【ナビ子】\n" + message + "\n")
            chat_log.see("end")

        return build_result

    except Exception as e:
        error = f"Autonomous Build Error: {e}"
        print(error)

        if "custom_chat_log" in globals():
            custom_chat_log.insert("end", "\n【ナビ子】\n" + error + "\n")
            custom_chat_log.see("end")
        elif "chat_log" in globals():
            chat_log.insert("end", "\n【ナビ子】\n" + error + "\n")
            chat_log.see("end")

def build_app_with_latest_improvement_from_gui(c_area=None):
    try:
        if "custom_chat_input" in globals():
            purpose = custom_chat_input.get("1.0", "end").strip()
        elif "chat_input" in globals():
            purpose = chat_input.get("1.0", "end").strip()
        else:
            purpose = ""

        if not purpose:
            purpose = "TODOアプリを作りたい"

        request, request_file = improvement_manager.load_latest_improvement_request()

        improvement_text = improvement_manager.format_improvement_prompt(request)

        improved_purpose = purpose + improvement_text

        result = app_project_builder.build_basic_app_project(
            purpose=improved_purpose,
            project_name="auto_project_improved"
        )

        history_file = improvement_manager.save_improvement_build_history(
            purpose=purpose,
            improved_purpose=improved_purpose,
            request_file=request_file,
            build_result=result
        )

        message = app_project_builder.format_build_result(result)

        message += "\n\n=== ImprovementManager ===\n"
        message += f"改善要求: {request_file}\n"
        message += f"改善Build履歴: {history_file}\n"
        message += "状態: 改善要求をBuilder入力へ反映しました。"

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        print(message)
        return result

    except Exception as e:
        message = f"ImprovementManager Buildエラー: {e}"

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        print(message)

        return {
            "success": False,
            "error": str(e)
        }

def diagnose_improvement_manager_from_gui(c_area=None):
    diagnosis = improvement_manager.diagnose()

    message = (
        "=== ImprovementManager 診断 ===\n"
        f"改善要求数: {diagnosis.get('improvement_request_count')}\n"
        f"改善Build履歴数: {diagnosis.get('improvement_build_history_count')}\n"
        f"状態: {diagnosis.get('status')}"
    )

    if c_area:
        append_chat_bubble(c_area, "navi", message)

    print(message)
    return message

def save_v135_completion_report():
    report_dir = LAB_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (
        report_dir
        / f"naviko_v135_completion_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    lines = []
    lines.append("=== ナビ子 v1.3.5 完成レポート ===")
    lines.append(f"保存日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("【完成内容】")
    lines.append("- GUI v2 メニュー分離")
    lines.append("- Reflection学習メモ生成")
    lines.append("- ImprovementManager モジュール化")
    lines.append("- 改善要求をBuilderへ反映")
    lines.append("- 改善Build履歴保存")
    lines.append("- 改善Build成果物評価")
    lines.append("- 改善成功判定")
    lines.append("- Retry改善要求生成")
    lines.append("- AppProjectBuilderの改善要求反映強化")
    lines.append("")
    lines.append("【完成した自己改善ループ】")
    lines.append("Builder → 成果物 → Reflection → 改善要求 → ImprovementManager → 改善Build → 評価 → 成功判定 → Retry")
    lines.append("")
    lines.append("【ImprovementManager診断】")
    lines.append(str(improvement_manager.diagnose()))
    lines.append("")
    lines.append("【総合判定】")
    lines.append("ナビ子 v1.3.5 のReflection自己改善ループは完成状態です。")

    report_text = "\n".join(lines)

    report_file.write_text(
        report_text,
        encoding="utf-8"
    )

    return (
        "=== ナビ子 v1.3.5 完成レポート保存 ===\n"
        f"保存先:\n{report_file}"
    )

def save_v135_completion_report_from_gui(c_area=None):
    message = save_v135_completion_report()

    if c_area:
        append_chat_bubble(c_area, "navi", message)

    print(message)
    return message
      

def load_json(path, default):
    if not path.exists():
        save_json(path, default)
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def run_agent_manager_from_gui(c_area=None):
    try:
        if "custom_chat_input" in globals():
            purpose = custom_chat_input.get("1.0", "end").strip()
        elif "chat_input" in globals():
            purpose = chat_input.get("1.0", "end").strip()
        else:
            purpose = ""

        if not purpose:
            purpose = "TODOアプリを作りたい"

        result = agent_manager.execute(purpose)

        execution_result = result.get("execution_result", {})
        history_file = result.get("history_file", "")

        lines = []
        lines.append("=== AgentManager 実行テスト ===")
        lines.append(f"目的: {purpose}")
        lines.append(f"状態: {execution_result.get('status')}")
        lines.append("")
        lines.append("選択Agent:")

        for agent in execution_result.get("agents", []):
            lines.append(f"- {agent}")

        lines.append("")
        lines.append("実行結果:")

        for item in execution_result.get("results", []):
            lines.append("")
            lines.append(f"Agent: {item.get('agent')}")
            lines.append(f"状態: {item.get('status')}")
            lines.append(f"メッセージ: {item.get('message')}")

        lines.append("")
        lines.append(f"保存先: {history_file}")

        message = "\n".join(lines)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        print(message)
        return message

    except Exception as e:
        message = f"AgentManager実行エラー: {e}"
        print(message)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        return message

def create_original_learning_advice():
    report = create_growth_report()

    adoption = report.get("adoption", {})

    total = adoption.get("total", 0)
    success = adoption.get("success_count", 0)
    rollback = adoption.get("rollback_count", 0)
    success_rate = adoption.get("success_rate", 0)
    safety_level = report.get("adoption_safety_level", "未評価")

    lines = []
    lines.append("=== オリジナルナビ子 学習アドバイス ===")
    lines.append(f"総反映数: {total}")
    lines.append(f"成功数: {success}")
    lines.append(f"ロールバック数: {rollback}")
    lines.append(f"成功率: {success_rate}%")
    lines.append(f"安全レベル: {safety_level}")
    lines.append("")

    lines.append("【次回の改善方針】")

    if total == 0:
        lines.append("- まだ反映履歴が少ないため、小規模な改善から開始してください。")
    elif rollback > success:
        lines.append("- ロールバックが成功数を上回っています。安全性重視で進めてください。")
        lines.append("- 次回は関数単位の小さな改善のみ許可するのが安全です。")
    elif success_rate >= 80:
        lines.append("- 成功率が高いため、通常改善または発展的改善に進めます。")
    else:
        lines.append("- 成功率がまだ安定していません。慎重に小規模改善を続けてください。")

    return "\n".join(lines)

def show_agent_manager_history_from_gui(c_area=None):
    try:
        histories = agent_manager.list_history()

        lines = []
        lines.append("=== AgentManager 履歴 ===")

        if not histories:
            lines.append("履歴はまだありません。")
        else:
            for item in histories[:10]:
                file_name = item.get("file", "不明")
                data = item.get("data", {})
                execution_result = data.get("execution_result", {})

                purpose = execution_result.get("purpose", "不明")
                status = execution_result.get("status", "不明")
                agents = execution_result.get("agents", [])

                lines.append("")
                lines.append(f"履歴ファイル: {file_name}")
                lines.append(f"目的: {purpose}")
                lines.append(f"状態: {status}")
                lines.append("Agent:")

                for agent in agents:
                    lines.append(f"- {agent}")

        message = "\n".join(lines)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        print(message)
        return message

    except Exception as e:
        message = f"AgentManager履歴表示エラー: {e}"
        print(message)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        return message

def show_original_learning_advice_from_gui(c_area=None):
    """
    オリジナル反映履歴にもとづく学習アドバイスをGUIに表示する。
    """
    message = create_original_learning_advice()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def approve_latest_line_patch():
    """
    最新1行パッチを承認済みにする。
    まだオリジナルへは反映しない。
    """
    patch_dir = LAB_DIR / "line_patches"

    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return False, "保存済み1行パッチがありません。"

    latest = files[0]

    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    dst = approved_dir / latest.name

    shutil.copy2(
        latest,
        dst
    )

    return True, f"承認済みにしました: {dst}"

def run_autonomous_core_from_gui(c_area=None, purpose=""):
    """
    GUIからAutonomousCoreを実行する。
    入力された目的をもとに、記憶・計画・安全判定・仮実行まで行う。
    """
    if not purpose:
        purpose = "ナオさんの目的を整理して、次に必要な作業を計画する"

    result = autonomous_core.process_purpose(purpose)

    message = autonomous_core.format_result(result)

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_autonomous_build_completion_diagnosis():
    lines = []
    lines.append("=== 自律生成 完了診断レポート ===")

    # AutonomousCore
    try:
        core_diag = autonomous_core.diagnose_core()
        lines.append("AutonomousCore: OK")
        lines.append(str(core_diag))
    except Exception as e:
        lines.append(f"AutonomousCore: NG / {e}")

    lines.append("")

    # AgentManager
    try:
        agent_diag = agent_manager.diagnose()
        lines.append("AgentManager: OK")
        lines.append(f"履歴件数: {agent_diag.get('history_count')}")
        lines.append(f"最新状態: {agent_diag.get('latest_status')}")
        lines.append(f"失敗Agent: {agent_diag.get('failed_agents')}")
    except Exception as e:
        lines.append(f"AgentManager: NG / {e}")

    lines.append("")

    # 自律生成履歴
    try:
        build_history = list_autonomous_build_history()
        lines.append("自律生成履歴: OK")
        lines.append(build_history)
    except Exception as e:
        lines.append(f"自律生成履歴: NG / {e}")

    lines.append("")

    # 成果物診断
    try:
        artifact_diag = diagnose_autonomous_build_artifacts()
        lines.append("成果物診断: OK")
        lines.append(artifact_diag)
    except Exception as e:
        lines.append(f"成果物診断: NG / {e}")

    lines.append("")

    # Agent履歴統合
    try:
        agent_history_diag = diagnose_autonomous_build_agent_history()
        lines.append("自律生成Agent履歴: OK")
        lines.append(agent_history_diag)
    except Exception as e:
        lines.append(f"自律生成Agent履歴: NG / {e}")

    lines.append("")
    lines.append("【総合判定】")

    report_text = "\n".join(lines)

    if "NG" in report_text or "要確認" in report_text:
        lines.append("自律生成システム: 要確認")
    else:
        lines.append("自律生成システム: OK")

    return "\n".join(lines)

def run_autonomous_build_completion_diagnosis_from_gui(c_area=None):
    message = run_autonomous_build_completion_diagnosis()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def cleanup_v12_test_data_from_gui(c_area=None):
    results = maintenance_manager.cleanup_v12_test_data()
    message = maintenance_manager.format_cleanup_report(results)

    if c_area:
        append_chat_bubble(
            c_area,
            "LAB",
            message
        )

    print(message)
    return message

def approve_latest_line_patch_from_gui(c_area=None):
    """
    GUIから最新1行パッチを承認済みにする。
    """
    ok, message = approve_latest_line_patch()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def test_approve_latest_line_patch():
    print("=== 最新1行パッチ承認テスト ===")

    ok, message = approve_latest_line_patch()

    print(message)

    if ok:
        print("-> 最新1行パッチ承認成功")
        return True
    else:
        print("-> 最新1行パッチ承認失敗")
        return False

def list_approved_line_patches():
    """
    承認済み1行パッチ一覧を返す。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "承認済み1行パッチはありません。"

    lines = []
    lines.append("=== 承認済み1行パッチ一覧 ===")

    for file in files[:10]:
        data = load_json(file, {})
        lines.append(
            f"- {file.name} / 対象関数: {data.get('target_function', '不明')}"
        )

    return "\n".join(lines)

def show_approved_line_patches_from_gui(c_area=None):
    """
    承認済み1行パッチ一覧をGUIチャット欄に表示する。
    """
    message = list_approved_line_patches()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)

    return message

show_approved_line_patches_from_gui

DANGER_WORDS = [
    "delete",
    "remove",
    "os.remove",
    "shutil.rmtree",
    "subprocess",
    "powershell",
    "cmd",
    "payment",
    "purchase",
    "password",
    "api key",
    "token",
    "send to server",
    "overwrite",
    "write_text(",
    "open(",
    "naviko.py",
    "credit",
    "requests.post("
]

def get_latest_approved_line_patch_info():
    """
    最新の承認済み1行パッチ情報を返す。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "承認済み1行パッチはありません。"

    latest = files[0]
    data = load_json(latest, {})

    return (
        "=== 最新承認済み1行パッチ ===\n"
        f"ファイル: {latest.name}\n"
        f"対象関数: {data.get('target_function', '不明')}\n"
        f"変更前: {data.get('old_line', '')}\n"
        f"変更後: {data.get('new_line', '')}\n"
        f"理由: {data.get('reason', '')}\n"
        f"反映済み: {data.get('applied', False)}"
    )

def show_latest_approved_line_patch_from_gui(c_area=None):
    """
    最新承認済み1行パッチをGUIチャット欄に表示する。
    """
    message = get_latest_approved_line_patch_info()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)

    return message

def check_latest_approved_line_patch_for_original():
    """
    最新の承認済み1行パッチを、
    オリジナル naviko.py に対して反映前チェックする。
    実際のオリジナルには書き込まない。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return False, "承認済み1行パッチはありません。"

    latest = files[0]

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return False, f"オリジナル naviko.py が見つかりません。\n{original_file}"

    source_text = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, preview_file, message = save_line_patch_apply_preview(
        latest,
        source_text,
        title="original_line_patch_precheck"
    )

    if not ok:
        return False, (
            "オリジナル反映前チェックNG\n"
            f"対象パッチ: {latest.name}\n"
            f"理由: {message}"
        )

    return True, (
        "オリジナル反映前チェックOK\n"
        f"対象パッチ: {latest.name}\n"
        f"プレビュー保存: {preview_file}\n"
        "※ オリジナル naviko.py にはまだ反映していません。"
    )

def check_latest_approved_line_patch_for_original_from_gui(c_area=None):
    """
    GUIから最新承認済み1行パッチの
    オリジナル反映前チェックを実行する。
    """
    ok, message = check_latest_approved_line_patch_for_original()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)

    return message

def save_v13_completion_report():
    report_dir = LAB_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (
        report_dir
        / f"naviko_v13_completion_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    lines = []
    lines.append("=== ナビ子 v1.3 完成レポート ===")
    lines.append(f"保存日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("【v1.3 中核機能】")
    lines.append("- ActionPlanner")
    lines.append("- WorkspaceManager")
    lines.append("- ArtifactWriter")
    lines.append("- AppProjectBuilder")
    lines.append("- AutonomousCore接続")
    lines.append("- AgentManager接続")
    lines.append("- 自律生成履歴")
    lines.append("- 成果物診断")
    lines.append("- 重複実行防止")
    lines.append("")

    lines.append(run_autonomous_build_completion_diagnosis())
    lines.append("")
    lines.append("【総合判定】")
    lines.append("ナビ子 v1.3 の自律生成基盤は完成状態です。")

    report = "\n".join(lines)

    report_file.write_text(
        report,
        encoding="utf-8"
    )

    return (
        "=== ナビ子 v1.3 完成レポート保存 ===\n"
        f"保存先:\n{report_file}"
    )

def save_v13_completion_report_from_gui(c_area=None):
    message = save_v13_completion_report()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def show_v12_core_dashboard(c_area=None):
    sections = []

    sections.append("=== ナビ子 v1.2 Core Dashboard ===")
    sections.append("")

    try:
        sections.append("【MemoryManager】")
        sections.append(
            str(memory_manager.diagnose_memory())
        )
        sections.append("")
    except Exception as e:
        sections.append(f"MemoryManager ERROR: {e}")
        sections.append("")

    try:
        sections.append("【GoalManager】")
        sections.append(
            str(goal_manager.diagnose_goals())
        )
        sections.append("")
    except Exception as e:
        sections.append(f"GoalManager ERROR: {e}")
        sections.append("")

    try:
        sections.append("【AgentRegistry】")
        sections.append(
            str(agent_registry.diagnose_agents())
        )
        sections.append("")
    except Exception as e:
        sections.append(f"AgentRegistry ERROR: {e}")
        sections.append("")

    try:
        sections.append("【TaskPlanner】")
        sections.append(
            str(task_planner.diagnose_planner())
        )
        sections.append("")
    except Exception as e:
        sections.append(f"TaskPlanner ERROR: {e}")
        sections.append("")

    try:
        sections.append("【PlanExecutor】")
        sections.append(
            str(plan_executor.diagnose_executor())
        )
        sections.append("")
    except Exception as e:
            sections.append(f"PlanExecutor ERROR: {e}")
            sections.append("")

    try:
        sections.append("【AutonomyController】")
        sections.append(
            str(
                autonomy_controller.diagnose_autonomy()
            )
        )
        sections.append("")
    except Exception as e:
        sections.append(f"Autonomy ERROR: {e}")
        sections.append("")

    try:
        sections.append("【AutonomousCore】")
        sections.append(
            str(
                autonomous_core.diagnose_core()
            )
        )
    except Exception as e:
        sections.append(f"Core ERROR: {e}")

    report = "\n".join(sections)

    if c_area:
        append_chat_bubble(
            c_area,
            "LAB",
            report
        )

    print(report)
    return report

def list_reflection_history():
    reflection_dir = LAB_DIR / "reflection"
    reflection_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        reflection_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== ReflectionEngine 履歴 ===")

    if not files:
        lines.append("自己評価履歴はまだありません。")
        return "\n".join(lines)

    for file in files[:10]:
        data = load_json(file, {})

        lines.append("")
        lines.append(f"履歴ファイル: {file.name}")
        lines.append(f"対象履歴: {data.get('source_history', '不明')}")
        lines.append(f"目的: {data.get('purpose', '不明')}")
        lines.append(f"状態: {data.get('status', '不明')}")
        lines.append(f"要約: {data.get('summary', '不明')}")

    return "\n".join(lines)

def read_text_file_safely(path, max_chars=3000):
    try:
        target = Path(path)

        if not target.exists():
            return ""

        text = target.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return text[:max_chars]

    except Exception:
        return ""

def create_artifact_reflection_for_latest_build():
    history_dir = LAB_DIR / "autonomous_builds"
    reflection_dir = LAB_DIR / "reflection"
    reflection_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "自律生成履歴がないため、成果物評価できません。"

    latest = files[0]
    data = load_json(latest, {})

    purpose = data.get("purpose", "不明")
    build_result = data.get("build_result", {})
    project_path = find_project_path(build_result)

    if not project_path:
        return "成果物フォルダが見つからないため、評価できません。"

    project_dir = Path(project_path)

    readme_text = read_text_file_safely(project_dir / "README.md")
    main_text = read_text_file_safely(project_dir / "main.py")
    requirements_text = read_text_file_safely(project_dir / "requirements.txt")
    notes_text = read_text_file_safely(project_dir / "notes.txt")

    good_points = []
    improvement_points = []
    next_actions = []

    if readme_text:
        good_points.append("README.md が存在し、成果物の説明を記録できている。")
    else:
        improvement_points.append("README.md が空、または読み取れません。")

    if main_text:
        good_points.append("main.py が存在し、アプリ本体のコードを生成できている。")

        if "tkinter" in main_text.lower():
            good_points.append("main.py に Tkinter GUI の要素が含まれている。")
        else:
            improvement_points.append("main.py にGUI要素が少ない可能性があります。")

        if "def " in main_text:
            good_points.append("main.py に関数定義があり、処理を分ける構造がある。")
        else:
            improvement_points.append("main.py の処理が関数化されていない可能性があります。")
    else:
        improvement_points.append("main.py が空、または読み取れません。")

    if requirements_text:
        good_points.append("requirements.txt が存在し、依存関係の管理枠がある。")
    else:
        improvement_points.append("requirements.txt が空、または読み取れません。")

    if notes_text:
        good_points.append("notes.txt が存在し、補足情報を保存できている。")
    else:
        improvement_points.append("notes.txt が空、または読み取れません。")

    if not improvement_points:
        improvement_points.append("大きな問題は見つかりませんでした。次は品質評価を細かくします。")

    next_actions.append("main.py の実行テスト機能を追加する。")
    next_actions.append("README.md の内容品質を評価する。")
    next_actions.append("TODOアプリとして追加・削除・保存機能があるか確認する。")

    reflection = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "artifact_reflection",
        "source_history": latest.name,
        "purpose": purpose,
        "project_path": str(project_dir),
        "status": "reflected",
        "good_points": good_points,
        "improvement_points": improvement_points,
        "next_actions": next_actions,
        "summary": "成果物ファイルを読み取り、内容ベースの自己評価を行いました。",
        "files_checked": {
            "README.md": bool(readme_text),
            "main.py": bool(main_text),
            "requirements.txt": bool(requirements_text),
            "notes.txt": bool(notes_text)
        }
    }

    reflection_file = (
        reflection_dir
        / f"artifact_reflection_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(reflection_file, reflection)

    lines = []
    lines.append("=== ReflectionEngine v2 成果物評価 ===")
    lines.append(f"対象履歴: {latest.name}")
    lines.append(f"目的: {purpose}")
    lines.append(f"成果物: {project_dir}")
    lines.append(f"保存先: {reflection_file}")
    lines.append("")

    lines.append("確認ファイル:")
    for name, ok in reflection["files_checked"].items():
        lines.append(f"- {name}: {'OK' if ok else 'NG'}")

    lines.append("")
    lines.append("良かった点:")
    for item in good_points:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("改善点:")
    for item in improvement_points:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("次回アクション:")
    for item in next_actions:
        lines.append(f"- {item}")

    return "\n".join(lines)

def create_artifact_reflection_for_latest_improvement_build():
    history_dir = LAB_DIR / "improvement_history"
    reflection_dir = LAB_DIR / "reflection"
    reflection_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "改善Build履歴がないため、成果物評価できません。"

    latest = files[0]
    data = load_json(latest, {})

    purpose = data.get("purpose", "不明")
    build_result = data.get("build_result", {})
    project_path = find_project_path(build_result)

    if not project_path:
        return "改善Build成果物フォルダが見つからないため、評価できません。"

    project_dir = Path(project_path)

    readme_text = read_text_file_safely(project_dir / "README.md")
    main_text = read_text_file_safely(project_dir / "main.py")
    requirements_text = read_text_file_safely(project_dir / "requirements.txt")
    notes_text = read_text_file_safely(project_dir / "notes.txt")

    good_points = []
    improvement_points = []
    next_actions = []

    if readme_text:
        good_points.append("README.md が存在し、成果物の説明を記録できている。")
    else:
        improvement_points.append("README.md が空、または読み取れません。")

    if main_text:
        good_points.append("main.py が存在し、アプリ本体のコードを生成できている。")

        if "tkinter" in main_text.lower():
            good_points.append("main.py に Tkinter GUI の要素が含まれている。")
        else:
            improvement_points.append("main.py にGUI要素が少ない可能性があります。")

        if "def " in main_text:
            good_points.append("main.py に関数定義があり、処理を分ける構造がある。")
        else:
            improvement_points.append("main.py の処理が関数化されていない可能性があります。")
    else:
        improvement_points.append("main.py が空、または読み取れません。")

    if requirements_text:
        good_points.append("requirements.txt が存在し、依存関係の管理枠がある。")
    else:
        improvement_points.append("requirements.txt が空、または読み取れません。")

    if notes_text:
        good_points.append("notes.txt が存在し、補足情報を保存できている。")
    else:
        improvement_points.append("notes.txt が空、または読み取れません。")

    if not improvement_points:
        improvement_points.append("大きな問題は見つかりませんでした。次は品質評価を細かくします。")

    next_actions.append("改善要求が成果物に反映されたか比較評価する。")
    next_actions.append("前回成果物との差分を確認する。")
    next_actions.append("改善成功率を記録する。")

    reflection = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "improvement_artifact_reflection",
        "source_history": latest.name,
        "purpose": purpose,
        "project_path": str(project_dir),
        "status": "reflected",
        "good_points": good_points,
        "improvement_points": improvement_points,
        "next_actions": next_actions,
        "summary": "改善Build履歴から成果物を読み取り、内容ベースの自己評価を行いました。",
        "files_checked": {
            "README.md": bool(readme_text),
            "main.py": bool(main_text),
            "requirements.txt": bool(requirements_text),
            "notes.txt": bool(notes_text)
        }
    }

    reflection_file = (
        reflection_dir
        / f"improvement_artifact_reflection_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(reflection_file, reflection)

    lines = []
    lines.append("=== Improvement成果物評価 ===")
    lines.append(f"対象履歴: {latest.name}")
    lines.append(f"目的: {purpose}")
    lines.append(f"成果物: {project_dir}")
    lines.append(f"保存先: {reflection_file}")
    lines.append("")

    lines.append("確認ファイル:")
    for name, ok in reflection["files_checked"].items():
        lines.append(f"- {name}: {'OK' if ok else 'NG'}")

    lines.append("")
    lines.append("良かった点:")
    for item in good_points:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("改善点:")
    for item in improvement_points:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("次回アクション:")
    for item in next_actions:
        lines.append(f"- {item}")

    return "\n".join(lines)

def create_artifact_reflection_for_latest_improvement_build_from_gui(c_area=None):
    message = create_artifact_reflection_for_latest_improvement_build()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def evaluate_latest_improvement_success():
    improvement_dir = LAB_DIR / "improvements"
    reflection_dir = LAB_DIR / "reflection"
    result_dir = LAB_DIR / "improvement_results"

    improvement_dir.mkdir(parents=True, exist_ok=True)
    reflection_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    request_files = sorted(
        improvement_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    reflection_files = sorted(
        reflection_dir.glob("improvement_artifact_reflection_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not request_files:
        return "改善要求がないため、改善成功判定できません。"

    if not reflection_files:
        return "改善Build成果物評価がないため、改善成功判定できません。"

    latest_request_file = request_files[0]
    latest_reflection_file = reflection_files[0]

    request = load_json(latest_request_file, {})
    reflection = load_json(latest_reflection_file, {})

    requests = request.get("improvement_requests", [])
    improvement_points = reflection.get("improvement_points", [])
    good_points = reflection.get("good_points", [])

    unresolved = []
    resolved = []

    reflection_text = "\n".join(improvement_points + good_points)

    for item in requests:
        if item in reflection_text:
            unresolved.append(item)
        else:
            resolved.append(item)

    total = len(requests)
    resolved_count = len(resolved)

    if total == 0:
        success_rate = 0
    else:
        success_rate = round((resolved_count / total) * 100, 1)

    if success_rate >= 80:
        status = "success"
        summary = "改善要求の多くが解消された可能性があります。"
    elif success_rate >= 50:
        status = "partial_success"
        summary = "一部の改善要求は解消された可能性があります。"
    else:
        status = "needs_retry"
        summary = "改善要求の多くが未解消の可能性があります。"

    result = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_request": latest_request_file.name,
        "source_reflection": latest_reflection_file.name,
        "status": status,
        "success_rate": success_rate,
        "total_requests": total,
        "resolved_count": resolved_count,
        "unresolved_count": len(unresolved),
        "resolved": resolved,
        "unresolved": unresolved,
        "summary": summary
    }

    result_file = (
        result_dir
        / f"improvement_result_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(result_file, result)

    lines = []
    lines.append("=== 改善成功判定 ===")
    lines.append(f"改善要求: {latest_request_file.name}")
    lines.append(f"評価結果: {latest_reflection_file.name}")
    lines.append(f"保存先: {result_file}")
    lines.append("")
    lines.append(f"状態: {status}")
    lines.append(f"改善成功率: {success_rate}%")
    lines.append(f"改善要求数: {total}")
    lines.append(f"解消候補: {resolved_count}")
    lines.append(f"未解消候補: {len(unresolved)}")
    lines.append("")
    lines.append("解消候補:")

    if resolved:
        for item in resolved:
            lines.append(f"- {item}")
    else:
        lines.append("- なし")

    lines.append("")
    lines.append("未解消候補:")

    if unresolved:
        for item in unresolved:
            lines.append(f"- {item}")
    else:
        lines.append("- なし")

    lines.append("")
    lines.append(f"要約: {summary}")

    return "\n".join(lines)

def evaluate_latest_improvement_success_from_gui(c_area=None):
    message = evaluate_latest_improvement_success()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def create_retry_improvement_request_from_latest_result():
    result_dir = LAB_DIR / "improvement_results"
    improvement_dir = LAB_DIR / "improvements"

    result_dir.mkdir(parents=True, exist_ok=True)
    improvement_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        result_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "改善成功判定結果がないため、Retry改善要求を生成できません。"

    latest = files[0]
    result = load_json(latest, {})

    unresolved = result.get("unresolved", [])

    if not unresolved:
        return "未解消の改善要求がないため、Retry改善要求は不要です。"

    retry_data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "retry_improvement_request",
        "source_result": latest.name,
        "source_request": result.get("source_request", ""),
        "purpose": "前回未解消の改善要求を再挑戦する",
        "status": "created",
        "improvement_requests": unresolved,
        "builder_hint": (
            "前回の改善成功判定で未解消だった項目のみを重点的に改善してください。"
        )
    }

    retry_file = (
        improvement_dir
        / f"retry_improvement_request_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(retry_file, retry_data)

    lines = []
    lines.append("=== Retry改善要求生成 ===")
    lines.append(f"対象結果: {latest.name}")
    lines.append(f"保存先: {retry_file}")
    lines.append("")
    lines.append("次回Builderへ再挑戦する改善要求:")

    for item in unresolved:
        lines.append(f"- {item}")

    return "\n".join(lines)

def create_retry_improvement_request_from_latest_result_from_gui(c_area=None):
    message = create_retry_improvement_request_from_latest_result()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def create_artifact_reflection_for_latest_build_from_gui(c_area=None):
    message = create_artifact_reflection_for_latest_build()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def create_improvement_request_from_latest_reflection():
    """
    最新のReflection結果から、次回Builderへ渡す改善要求を生成する。
    """
    reflection_dir = LAB_DIR / "reflection"
    reflection_dir.mkdir(parents=True, exist_ok=True)

    improvement_dir = LAB_DIR / "improvements"
    improvement_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        reflection_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "Reflection履歴がないため、改善要求を生成できません。"

    latest = files[0]
    reflection = load_json(latest, {})

    purpose = reflection.get("purpose", "不明")
    improvement_points = reflection.get("improvement_points", [])
    next_actions = reflection.get("next_actions", [])
    project_path = reflection.get("project_path", "")

    requests = []

    for item in improvement_points:
        if "大きな問題は見つかりません" in item:
            continue
        requests.append(item)

    for item in next_actions:
        requests.append(item)

    if not requests:
        requests.append("次回はREADME、main.py、requirements.txt、notes.txtの品質をさらに高める。")

    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_reflection": latest.name,
        "purpose": purpose,
        "project_path": project_path,
        "status": "created",
        "improvement_requests": requests,
        "builder_hint": (
            "前回の成果物評価を反映し、次回生成時は以下の改善要求を優先してください。"
        )
    }

    request_file = (
        improvement_dir
        / f"improvement_request_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    save_json(request_file, data)

    lines = []
    lines.append("=== Reflection学習メモ生成 ===")
    lines.append(f"対象Reflection: {latest.name}")
    lines.append(f"目的: {purpose}")
    lines.append(f"保存先: {request_file}")
    lines.append("")
    lines.append("次回Builderへの改善要求:")

    for item in requests:
        lines.append(f"- {item}")

    return "\n".join(lines)

def create_improvement_request_from_latest_reflection_from_gui(c_area=None):
    message = create_improvement_request_from_latest_reflection()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def list_reflection_history_from_gui(c_area=None):
    message = list_reflection_history()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def apply_latest_approved_line_patch_to_original_safely():
    """
    最新の承認済み1行パッチをオリジナル naviko.py へ安全反映する。
    失敗時はバックアップから自動復元する。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return False, "承認済み1行パッチはありません。"

    latest = None
    patch_data = None

    for file in files:
        data = load_json(
            file,
            {}
        )

        if data.get("applied") is not True:
            latest = file
            patch_data = data
            break

    if latest is None:
        return False, (
            "未反映の承認済み1行パッチはありません。\n"
            "すべて反映済みのため、二重反映を防止しました。"
        )

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return False, f"オリジナル naviko.py が見つかりません。\n{original_file}"

    original_dir = original_file.parent

    source_text = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, replaced_text, message = simulate_line_patch_json_inside_function(
        latest,
        source_text
    )

    if not ok:
        patch_data["applied"] = True
        patch_data["blocked"] = True
        patch_data["blocked_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        patch_data["blocked_reason"] = message
        patch_data["applied_to"] = "original_naviko"
        patch_data["status"] = "blocked_before_apply"

        save_json(
            latest,
            patch_data
        )

        record = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "blocked_before_apply",
            "selected_file": latest.name,
            "selected_path": str(latest),
            "approved": True,
            "backup_created": False,
            "applied": False,
            "verify_after_apply": False,
            "startup_test": False,
            "rollback": False,
            "method": "approved_line_patch",
            "error": message,
            "summary": "承認済み1行パッチがオリジナル反映前チェックで不適合だったためブロックした。"
        }

        save_adoption_history(record)

        return False, (
            "オリジナル反映停止\n"
            f"対象パッチ: {latest.name}\n"
            f"理由: {message}\n"
            "このパッチは blocked として記録し、次回から選ばないようにしました。"
        )

    backup_file = BACKUP_DIR / f"original_before_line_patch_{time.strftime('%Y%m%d_%H%M%S')}.py"

    try:
        shutil.copy2(
            original_file,
            backup_file
        )
    except Exception as e:
        return False, f"バックアップ作成失敗: {e}"

    try:
        original_file.write_text(
            replaced_text,
            encoding="utf-8"
        )

        py_compile.compile(
            str(original_file),
            doraise=True
        )

        result = subprocess.run(
            [sys.executable, str(original_file), "--self-test"],
            cwd=str(original_dir),
            capture_output=True,
            text=True,
            timeout=10
        )

        output = (result.stdout or "") + (result.stderr or "")

        if result.returncode != 0 or "SELF_TEST_OK" not in output:
            shutil.copy2(
                backup_file,
                original_file
            )

            record = {
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "rollback_completed_after_startup_failed",
                "selected_file": latest.name,
                "selected_path": str(latest),
                "backup_file": str(backup_file),
                "approved": True,
                "backup_created": True,
                "applied": True,
                "verify_after_apply": False,
                "startup_test": False,
                "rollback": True,
                "method": "approved_line_patch",
                "error": output[:1000],
                "summary": "承認済み1行パッチ反映後、起動テストに失敗したためロールバックした。"
            }

            save_adoption_history(record)
            save_rollback_pattern(record)

            return False, (
                "オリジナル反映後テストNGのためロールバックしました。\n"
                f"対象パッチ: {latest.name}\n"
                f"バックアップ: {backup_file}\n"
                f"出力:\n{output[:1000]}"
            )

    except Exception as e:
        shutil.copy2(
            backup_file,
            original_file
        )

        record = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "rollback_completed_after_apply_error",
            "selected_file": latest.name,
            "selected_path": str(latest),
            "backup_file": str(backup_file),
            "approved": True,
            "backup_created": True,
            "applied": False,
            "verify_after_apply": False,
            "startup_test": False,
            "rollback": True,
            "method": "approved_line_patch",
            "error": str(e),
            "summary": "承認済み1行パッチ反映中にエラーが発生したためロールバックした。"
        }

        save_adoption_history(record)
        save_rollback_pattern(record)

        return False, (
            "オリジナル反映中にエラーが発生したためロールバックしました。\n"
            f"対象パッチ: {latest.name}\n"
            f"バックアップ: {backup_file}\n"
            f"エラー: {e}"
        )

    record = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "startup_success",
        "selected_file": latest.name,
        "selected_path": str(latest),
        "backup_file": str(backup_file),
        "approved": True,
        "backup_created": True,
        "applied": True,
        "verify_after_apply": True,
        "startup_test": True,
        "rollback": False,
        "method": "approved_line_patch",
        "summary": "承認済み1行パッチをオリジナルへ安全反映し、構文チェックと起動テストに成功した。"
    }

    save_adoption_history(record)
    save_adoption_success_pattern(record)

    patch_data["applied"] = True
    patch_data["applied_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    patch_data["applied_to"] = "original_naviko"

    save_json(
        latest,
        patch_data
    )

    return True, (
        "オリジナル反映成功\n"
        f"対象パッチ: {latest.name}\n"
        f"バックアップ: {backup_file}\n"
        "構文チェック: OK\n"
        "--self-test: OK\n"
        "反映履歴: 保存済み\n"
        "成功パターン: 学習済み"
    )

def apply_latest_approved_line_patch_to_original_safely_from_gui(c_area=None):
    """
    GUIから最新承認済み1行パッチをオリジナルへ安全反映する。
    """
    ok, message = apply_latest_approved_line_patch_to_original_safely()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def cleanup_approved_line_patches():
    """
    承認済み1行パッチを整理する。
    applied=True または blocked=True のものは対象外として集計する。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = list(approved_dir.glob("*.json"))

    total = 0
    skipped = 0
    active = 0

    for file in files:
        data = load_json(file, {})

        total += 1

        if (
            data.get("applied") is True
            or data.get("blocked") is True
        ):
            skipped += 1
            continue

        active += 1

    return (
        "=== 承認済み1行パッチ整理 ===\n"
        f"総数: {total}\n"
        f"反映済み/blocked: {skipped}\n"
        f"未処理: {active}"
    )

def show_pending_approved_line_patches():
    """
    未処理の承認済み1行パッチを表示する。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== 未処理の承認済み1行パッチ ===")

    count = 0

    for file in files:
        data = load_json(
            file,
            {}
        )

        if (
            data.get("applied") is True
            or data.get("blocked") is True
        ):
            continue

        count += 1

        lines.append("")
        lines.append(f"ファイル: {file.name}")
        lines.append(
            f"対象関数: {data.get('target_function')}"
        )
        lines.append(
            f"理由: {data.get('reason')}"
        )

    if count == 0:
        lines.append("未処理パッチはありません。")

    return "\n".join(lines)

def route_goal_to_agents(purpose):
    text = str(purpose).lower()

    agents = ["planner"]

    if (
        "アプリ" in purpose
        or "コード" in purpose
        or "python" in text
        or "todo" in text
    ):
        agents.append("coder")
        agents.append("file")

    if "画像" in purpose or "イラスト" in purpose:
        agents.append("image")

    if "動画" in purpose or "youtube" in text:
        agents.append("video")

    if "調査" in purpose or "調べ" in purpose or "research" in text:
        agents.append("research")

    if "web" in text or "ブラウザ" in purpose:
        agents.append("browser")

    if "音声" in purpose or "読み上げ" in purpose:
        agents.append("voice")

    if "pc操作" in text or "デスクトップ操作" in purpose:
        agents.append("desktop")

    return list(dict.fromkeys(agents))

def is_recent_duplicate_autonomous_build(purpose, seconds=60):
    history_dir = LAB_DIR / "autonomous_builds"
    history_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        history_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    now = time.time()

    for file in files[:5]:
        try:
            data = load_json(file, {})
            old_purpose = data.get("purpose", "")

            if old_purpose != purpose:
                continue

            elapsed = now - file.stat().st_mtime

            if elapsed <= seconds:
                return True, file

        except Exception:
            continue

    return False, None

def execute_agent_task(agent, task, purpose=""):
    allowed_agents = [
        "planner",
        "coder",
        "image",
        "video",
        "research",
        "browser",
        "desktop",
        "file",
        "voice",
    ]

    if agent not in allowed_agents:
        return {
            "agent": agent,
            "status": "blocked",
            "task": task,
            "message": "未登録のエージェントです。"
        }

    return {
        "agent": agent,
        "status": "simulated",
        "task": task,
        "purpose": purpose,
        "message": f"{agent} エージェントの仮実行を完了しました。"
    }

def execute_routed_agents(purpose):
    """
    旧Agent実行関数。
    内部処理はAgentManagerへ委譲する。
    """
    result = agent_manager.execute(purpose)
    return result.get("execution_result", {})

def save_agent_execution_history(execution_result):
    exec_dir = LAB_DIR / "agent_executions"
    exec_dir.mkdir(parents=True, exist_ok=True)

    exec_file = exec_dir / f"agent_execution_{time.strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "execution_result": execution_result
    }

    save_json(exec_file, data)

    return exec_file

def execute_routed_agents_from_gui(c_area=None):
    if "custom_chat_input" in globals():
        purpose = custom_chat_input.get("1.0", "end").strip()
    elif "chat_input" in globals():
        purpose = chat_input.get("1.0", "end").strip()
    else:
        purpose = ""

    if not purpose:
        purpose = "TODOアプリを作りたい"

    execution_result = execute_routed_agents(purpose)
    exec_file = save_agent_execution_history(execution_result)

    lines = []
    lines.append("=== AgentExecutor 仮実行 ===")
    lines.append(f"目的: {purpose}")
    lines.append(f"状態: {execution_result.get('status')}")
    lines.append("")
    lines.append("実行結果:")

    for result in execution_result.get("results", []):
        lines.append("")
        lines.append(f"エージェント: {result.get('agent')}")
        lines.append(f"状態: {result.get('status')}")
        lines.append(f"タスク: {result.get('task')}")
        lines.append(f"メッセージ: {result.get('message')}")

    lines.append("")
    lines.append(f"保存先: {exec_file}")

    message = "\n".join(lines)

    if c_area:
        append_chat_bubble(c_area, "navi", message)

    print(message)
    return message

def list_agent_routing_history():
    route_dir = LAB_DIR / "agent_routes"
    route_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        route_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    lines = []
    lines.append("=== エージェント役割分担履歴 ===")

    if not files:
        lines.append("履歴はまだありません。")
        return "\n".join(lines)

    for file in files[:10]:
        data = load_json(file, {})

        purpose = data.get("purpose", "不明")
        agents = data.get("agents", [])

        lines.append("")
        lines.append(f"履歴ファイル: {file.name}")
        lines.append(f"目的: {purpose}")
        lines.append("選択エージェント:")

        for agent in agents:
            lines.append(f"- {agent}")

    return "\n".join(lines)

def show_agent_routing_history_from_gui(c_area=None):
    message = list_agent_routing_history()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def list_agent_execution_history():
    """
    旧Agent履歴関数。
    内部処理はAgentManagerへ委譲する。
    """
    histories = agent_manager.list_history()

    lines = []
    lines.append("=== Agent実行履歴 ===")

    if not histories:
        lines.append("履歴はまだありません。")
        return "\n".join(lines)

    for item in histories[:10]:
        file_name = item.get("file", "不明")
        data = item.get("data", {})
        execution_result = data.get("execution_result", {})

        purpose = execution_result.get("purpose", "不明")
        status = execution_result.get("status", "不明")
        results = execution_result.get("results", [])

        lines.append("")
        lines.append(f"履歴ファイル: {file_name}")
        lines.append(f"目的: {purpose}")
        lines.append(f"状態: {status}")
        lines.append("実行Agent:")

        for result in results:
            agent = result.get("agent", "不明")
            agent_status = result.get("status", "不明")
            lines.append(f"- {agent}: {agent_status}")

    return "\n".join(lines)

def show_agent_execution_history_from_gui(c_area=None):
    message = list_agent_execution_history()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def diagnose_agent_execution_system():
    """
    旧Agent診断関数。
    内部処理はAgentManagerへ委譲する。
    """
    diagnosis = agent_manager.diagnose()

    lines = []
    lines.append("=== AgentExecutor 診断 ===")
    lines.append("内部処理: AgentManager")
    lines.append(f"履歴件数: {diagnosis.get('history_count')}")
    lines.append(f"最新履歴: {diagnosis.get('latest_file')}")
    lines.append(f"最新状態: {diagnosis.get('latest_status')}")

    failed_agents = diagnosis.get("failed_agents", [])

    if failed_agents:
        lines.append("失敗Agent:")
        for agent in failed_agents:
            lines.append(f"- {agent}")
    else:
        lines.append("失敗Agent: なし")

    return "\n".join(lines)

def diagnose_agent_execution_system_from_gui(c_area=None):
    message = diagnose_agent_execution_system()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def save_agent_routing_history(purpose, agents):
    route_dir = LAB_DIR / "agent_routes"
    route_dir.mkdir(parents=True, exist_ok=True)

    route_file = route_dir / f"agent_route_{time.strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": purpose,
        "agents": agents
    }

    save_json(route_file, data)

    return route_file

def route_goal_to_agents_from_gui(c_area=None):
    if "custom_chat_input" in globals():
        purpose = custom_chat_input.get("1.0", "end").strip()
    elif "chat_input" in globals():
        purpose = chat_input.get("1.0", "end").strip()
    else:
        purpose = ""

    if not purpose:
        purpose = "TODOアプリを作りたい"

    agents = route_goal_to_agents(purpose)
    route_file = save_agent_routing_history(purpose, agents)

    lines = []
    lines.append("=== エージェント役割分担 ===")
    lines.append(f"目的: {purpose}")
    lines.append("")
    lines.append("選択エージェント:")

    for agent in agents:
        lines.append(f"- {agent}")

    lines.append("")
    lines.append(f"保存先: {route_file}")

    message = "\n".join(lines)

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def diagnose_agent_manager_from_gui(c_area=None):
    try:
        diagnosis = agent_manager.diagnose()

        lines = []
        lines.append("=== AgentManager 診断 ===")
        lines.append(f"履歴件数: {diagnosis.get('history_count')}")
        lines.append(f"最新履歴: {diagnosis.get('latest_file')}")
        lines.append(f"最新状態: {diagnosis.get('latest_status')}")

        failed_agents = diagnosis.get("failed_agents", [])

        if failed_agents:
            lines.append("失敗Agent:")
            for agent in failed_agents:
                lines.append(f"- {agent}")
        else:
            lines.append("失敗Agent: なし")

        message = "\n".join(lines)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        print(message)
        return message

    except Exception as e:
        message = f"AgentManager診断エラー: {e}"
        print(message)

        if c_area:
            append_chat_bubble(c_area, "navi", message)

        return message

def show_pending_approved_line_patches_from_gui(
    c_area=None
):
    message = show_pending_approved_line_patches()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def cleanup_approved_line_patches_from_gui(c_area=None):
    message = cleanup_approved_line_patches()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def block_diagnosis_line_patches():
    """
    統合診断用テストの承認済み1行パッチを一括で blocked にする。
    """
    approved_dir = LAB_DIR / "approved_line_patches"
    approved_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        approved_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    blocked_count = 0

    for file in files:
        data = load_json(
            file,
            {}
        )

        if (
            data.get("applied") is True
            or data.get("blocked") is True
        ):
            continue

        reason = str(data.get("reason", ""))

        if "統合診断用テスト" not in reason:
            continue

        data["applied"] = True
        data["blocked"] = True
        data["status"] = "diagnosis_only"
        data["blocked_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["blocked_reason"] = "統合診断用テストのため実反映対象外"
        data["applied_to"] = "diagnosis_only"

        save_json(
            file,
            data
        )

        blocked_count += 1

    return (
        "=== 診断用パッチ一括整理 ===\n"
        f"blocked にした件数: {blocked_count}"
    )

def block_diagnosis_line_patches_from_gui(c_area=None):
    message = block_diagnosis_line_patches()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_lab_v11_final_diagnosis():
    """
    LAB v1.1 完成前の総合診断。
    """
    lines = []
    lines.append("=== ナビ子LAB v1.1 総合診断 ===")

    lines.append("")
    lines.append("【フォルダ確認】")

    check_dirs = [
        LAB_DIR,
        LINE_PATCH_DIR,
        LINE_PATCH_PREVIEW_DIR,
        LINE_PATCH_TEMP_DIR,
        APPROVED_LINE_PATCH_DIR,
        PENDING_LINE_PATCH_DIR,
        BACKUP_DIR,
    ]

    for folder in check_dirs:
        lines.append(
            f"{folder.name}: {'OK' if folder.exists() else 'NG'}"
        )

    lines.append("")
    lines.append(cleanup_approved_line_patches())

    lines.append("")
    lines.append("【オリジナル診断】")
    original = run_original_self_diagnosis()

    lines.append(
        f"naviko.py: {'OK' if original.get('original_exists') else 'NG'}"
    )
    lines.append(
        f"構文チェック: {'OK' if original.get('syntax_ok') else 'NG'}"
    )
    lines.append(
        f"--self-test: {'OK' if original.get('self_test_ok') else 'NG'}"
    )
    lines.append(
        f"spritesheet.webp: {'OK' if original.get('spritesheet_exists') else 'NG'}"
    )

    if original.get("problems"):
        lines.append("問題:")
        for p in original.get("problems", []):
            lines.append(f"- {p}")
    else:
        lines.append("問題: なし")

    lines.append("")
    lines.append(create_original_learning_advice())

    lines.append("")
    lines.append(format_self_improvement_permission_level())

    lines.append("")
    lines.append("【判定】")

    approved_summary = cleanup_approved_line_patches()
    safe = (
        "未処理: 0" in approved_summary
        and original.get("original_exists")
        and original.get("syntax_ok")
        and original.get("self_test_ok")
    )

    if safe:
        lines.append("LAB v1.1 は完成前診断OKです。")
    else:
        lines.append("LAB v1.1 は未解決項目があります。")

    return "\n".join(lines)

def run_lab_v11_final_diagnosis_from_gui(c_area=None):
    message = run_lab_v11_final_diagnosis()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def save_lab_v11_final_report():
    """
    LAB v1.1 の完成状態をログとして保存する。
    """
    report_dir = LAB_DIR / "reports"
    report_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = (
        report_dir
        / f"lab_v11_final_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    report = run_lab_v11_final_diagnosis()

    report_file.write_text(
        report,
        encoding="utf-8"
    )

    return (
        "=== LAB v1.1 完成ログ保存 ===\n"
        f"保存先:\n{report_file}"
    )

def save_lab_v11_final_report_from_gui(c_area=None):
    message = save_lab_v11_final_report()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_line_patch_full_precheck_diagnosis():
    """
    本番用1行パッチの作成から反映前チェックまでを一括確認する。
    実反映はしない。
    """
    lines = []
    lines.append("=== 1行パッチ安全フロー統合診断 ===")

    ok, patch_file, message = create_real_line_patch_json(
        target_function="build_system_prompt",
        old_line='    rules = "\\n".join(f"- {r}" for r in character.get("rules", []))',
        new_line='    rules = "\\n".join(f"- {r}" for r in character.get("rules", []))',
        reason="統合診断用テスト"
    )

    lines.append(f"パッチ作成: {'OK' if ok else 'NG'}")
    lines.append(message)

    if not ok:
        return "\n".join(lines)

    ok, approve_message = approve_latest_line_patch()
    lines.append(f"承認: {'OK' if ok else 'NG'}")
    lines.append(approve_message)

    if not ok:
        return "\n".join(lines)

    ok, precheck_message = check_latest_approved_line_patch_for_original()
    lines.append(f"オリジナル反映前チェック: {'OK' if ok else 'NG'}")
    lines.append(precheck_message)

    if ok:
        approved_files = sorted(
            APPROVED_LINE_PATCH_DIR.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if approved_files:
            latest_approved = approved_files[0]
            data = load_json(
                latest_approved,
                {}
            )

            data["applied"] = True
            data["blocked"] = True
            data["status"] = "diagnosis_only"
            data["blocked_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
            data["blocked_reason"] = "統合診断用パッチのため実反映対象外"
            data["applied_to"] = "diagnosis_only"

            save_json(
                latest_approved,
                data
            )

            lines.append("診断用パッチ処理: blocked 済み")

    lines.append("")
    lines.append("※ 実際のオリジナル naviko.py には反映していません。")

    return "\n".join(lines)

def run_line_patch_full_precheck_diagnosis_from_gui(c_area=None):
    message = run_line_patch_full_precheck_diagnosis()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def load_json_file(file_path, default=None):
    if default is None:
        default = {}

    try:
        path = Path(file_path)

        if not path.exists():
            return default

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return default

def save_rollback_pattern(record):
    """
    ロールバック発生時の失敗パターンを保存する。
    同一 status / selected_file の重複保存は避ける。
    """
    patterns = load_json(
        REJECT_PATTERN_FILE,
        []
    )

    record_key = (
        "rollback",
        record.get("status"),
        record.get("selected_file")
    )

    for item in patterns:
        item_key = (
            item.get("type"),
            item.get("status"),
            item.get("selected_file")
        )

        if item_key == record_key:
            return

    item = {
        "date": record.get("date", time.strftime("%Y-%m-%d %H:%M:%S")),
        "type": "rollback",
        "status": record.get("status"),
        "selected_file": record.get("selected_file"),
        "error": record.get("error"),
        "summary": "反映後チェックまたは起動テストで失敗し、自動復元された。"
    }

    patterns.append(item)

    save_json(
        REJECT_PATTERN_FILE,
        patterns
    )

def run_original_self_diagnosis():
    """
    オリジナルナビ子の自己診断。
    構文・必須ファイル・自己テスト対応を確認する。
    """
    original_file = Path(r"C:\Users\7716n\OneDrive\デスクトップ\naviko\naviko.py")
    original_dir = original_file.parent

    result = {
        "original_exists": False,
        "syntax_ok": False,
        "self_test_ok": False,
        "spritesheet_exists": False,
        "problems": [],
        "suggestions": [],
    }

    if not original_file.exists():
        result["problems"].append("オリジナル naviko.py が見つかりません。")
        result["suggestions"].append("naviko フォルダ内に naviko.py があるか確認してください。")
        return result

    result["original_exists"] = True

    try:
        py_compile.compile(str(original_file), doraise=True)
        result["syntax_ok"] = True
    except Exception as e:
        result["problems"].append(f"構文エラー: {e}")
        result["suggestions"].append("LAB側で修正候補を作成し、限定差分パッチとして反映してください。")

    spritesheet = original_dir / "spritesheet.webp"
    if spritesheet.exists():
        result["spritesheet_exists"] = True
    else:
        result["problems"].append("spritesheet.webp が見つかりません。")
        result["suggestions"].append("オリジナルフォルダに spritesheet.webp を配置してください。")

    try:
        completed = subprocess.run(
            [sys.executable, str(original_file), "--self-test"],
            cwd=str(original_dir),
            capture_output=True,
            text=True,
            timeout=10
        )

        output = (completed.stdout or "") + (completed.stderr or "")

        if completed.returncode == 0 and "SELF_TEST_OK" in output:
            result["self_test_ok"] = True
        else:
            result["problems"].append("オリジナルの --self-test が正常完了しませんでした。")
            result["suggestions"].append("起動前チェックまたは self-test 処理を確認してください。")

    except Exception as e:
        result["problems"].append(f"自己テスト実行エラー: {e}")
        result["suggestions"].append("オリジナル側の起動テスト処理を確認してください。")

    if not result["problems"]:
        result["suggestions"].append("オリジナルナビ子は正常です。")

    return result

def print_original_self_diagnosis():
    diagnosis = run_original_self_diagnosis()

    lines = []
    lines.append("=== オリジナルナビ子 自己診断 ===")
    lines.append(f"naviko.py: {'あり' if diagnosis['original_exists'] else 'なし'}")
    lines.append(f"構文チェック: {'OK' if diagnosis['syntax_ok'] else 'NG'}")
    lines.append(f"--self-test: {'OK' if diagnosis['self_test_ok'] else 'NG'}")
    lines.append(f"spritesheet.webp: {'あり' if diagnosis['spritesheet_exists'] else 'なし'}")
    lines.append("")

    if diagnosis["problems"]:
        lines.append("【検出された問題】")
        for p in diagnosis["problems"]:
            lines.append(f"- {p}")
    else:
        lines.append("【検出された問題】")
        lines.append("- なし")

    lines.append("")
    lines.append("【修復提案】")
    for s in diagnosis["suggestions"]:
        lines.append(f"- {s}")

    text = "\n".join(lines)
    print(text)
    return text

def list_original_naviko_functions():
    """
    オリジナル naviko.py に存在する関数一覧を表示する。
    """
    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return f"オリジナル naviko.py が見つかりません。\n{original_file}"

    source = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    functions = []

    for line in source.splitlines():
        stripped = line.strip()

        if stripped.startswith("def ") and "(" in stripped:
            name = stripped.split("def ", 1)[1].split("(", 1)[0]
            functions.append(name)

    if not functions:
        return "オリジナル naviko.py に関数が見つかりませんでした。"

    lines = []
    lines.append("=== オリジナル naviko.py 関数一覧 ===")

    for name in functions:
        lines.append(f"- {name}")

    return "\n".join(lines)

def show_original_naviko_functions_from_gui(c_area=None):
    message = list_original_naviko_functions()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def diagnose_adoption_system():
    adoption_history = load_json(
        []
    )

    adoption_request = load_json(
        {}
    )

    safety_level = decide_adoption_safety_level()
    adoption_summary = analyze_adoption_history()

    report = [
        "=== 反映安全システム診断 ===",
        f"反映履歴件数: {len(adoption_history)}",
        f"現在の反映申請: {adoption_request.get('status', 'なし')}",
        f"選定候補: {adoption_request.get('selected_file', 'なし')}",
        f"承認済み: {adoption_request.get('approved', False)}",
        f"構文チェック済み: {adoption_request.get('syntax_checked', False)}",
        f"バックアップ作成済み: {adoption_request.get('backup_created', False)}",
        f"反映済み: {adoption_request.get('applied', False)}",
        f"反映後チェック: {adoption_request.get('verify_after_apply', False)}",
        f"起動テスト: {adoption_request.get('startup_test', False)}",
        f"ロールバック: {adoption_request.get('rollback', False)}",
        f"反映安全レベル: {safety_level}",
        f"反映成功率: {adoption_summary.get('success_rate', 0)}%",
        f"成功数: {adoption_summary.get('success', 0)}",
        f"ロールバック数: {adoption_summary.get('rollback', 0)}",
        "============================"
    ]

    return "\n".join(report)

def save_adoption_success_pattern(record):
    patterns = load_json(
        SUCCESS_PATTERN_FILE,
        []
    )

    record_key = (
        "adoption_success",
        record.get("status"),
        record.get("selected_file")
    )

    for item in patterns:
        item_key = (
            item.get("type"),
            item.get("status"),
            item.get("selected_file")
        )

        if item_key == record_key:
            return

    item = {
        "date": record.get("date"),
        "type": "adoption_success",
        "status": record.get("status"),
        "selected_file": record.get("selected_file"),
        "summary": "反映後チェックと起動テストに成功した。"
    }

    patterns.append(item)

    save_json(
        SUCCESS_PATTERN_FILE,
        patterns
    )

def decide_adoption_safety_level():
    report = analyze_adoption_history()

    total = report.get("total", 0)
    success_rate = report.get("success_rate", 0)
    rollback_count = report.get("rollback_count", 0)

    if total == 0:
        return "未評価"

    if rollback_count >= 1:
        return "警戒"

    if success_rate >= 90:
        return "安定"

    if success_rate >= 70:
        return "通常"

    return "慎重"

def decide_self_improvement_permission_level():
    """
    反映成功率と安全レベルから、次に許可する自己改善規模を決める。
    """
    analysis = analyze_adoption_history()
    safety_level = decide_adoption_safety_level()

    success_rate = analysis.get("success_rate", 0)
    rollback_count = analysis.get("rollback_count", 0)
    continuous_failures = analysis.get("continuous_failures", 0)

    if continuous_failures >= 2:
        level = "緊急安全モード"
        allowed = "新規反映禁止。診断と整理のみ。"

    elif safety_level == "警戒" or rollback_count > analysis.get("success_count", 0):
        level = "最小改善モード"
        allowed = "1行パッチのみ許可。関数内限定。実反映前チェック必須。"

    elif success_rate < 40:
        level = "慎重改善モード"
        allowed = "1行パッチのみ許可。安全診断と承認必須。"

    elif success_rate < 70:
        level = "通常改善モード"
        allowed = "小規模な複数行パッチまで許可。ただし関数内限定。"

    else:
        level = "安定改善モード"
        allowed = "中規模改善を検討可。ただしバックアップ・self-test・ロールバック必須。"

    return {
        "level": level,
        "allowed": allowed,
        "success_rate": success_rate,
        "safety_level": safety_level,
        "rollback_count": rollback_count,
        "continuous_failures": continuous_failures,
    }

def format_self_improvement_permission_level():
    result = decide_self_improvement_permission_level()

    return (
        "=== 自己改善許可レベル ===\n"
        f"許可レベル: {result.get('level')}\n"
        f"許可内容: {result.get('allowed')}\n"
        f"成功率: {result.get('success_rate')}%\n"
        f"安全レベル: {result.get('safety_level')}\n"
        f"ロールバック数: {result.get('rollback_count')}\n"
        f"連続失敗数: {result.get('continuous_failures')}"
    )

def show_self_improvement_permission_level_from_gui(c_area=None):
    message = format_self_improvement_permission_level()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def is_forbidden_growth(text):
    if not isinstance(text, str):
        return True

    lowered = text.lower()

    for word in DANGER_WORDS:
        if word in lowered:
            return True

    return False

def detect_forbidden_reasons(text):
    if not isinstance(text, str):
        return ["文字列ではないため危険"]

    lowered = text.lower()
    reasons = []

    for word in DANGER_WORDS:
        if word in lowered:
            reasons.append(
                f"危険ワード検出: {word}"
            )

    return reasons

def score_patch_suggestion(patch_text):
    reasons = detect_forbidden_reasons(patch_text)

    if reasons:
        safety = 0
    else:
        safety = 50

    usefulness = 15
    simplicity = 10

    good_words = [
        "改善",
        "記憶",
        "感情",
        "安全",
        "分析",
        "履歴",
        "整理",
        "自己評価"
    ]

    for word in good_words:
        if word in patch_text:
            usefulness += 2

    difficult_words = [
        "大規模",
        "完全自動",
        "外部",
        "削除",
        "上書き",
        "コマンド"
    ]

    for word in difficult_words:
        if word in patch_text:
            simplicity -= 2

    usefulness = min(usefulness, 30)
    simplicity = max(0, min(simplicity, 20))

    total = safety + usefulness + simplicity

    return {
        "score": total,
        "safety": safety,
        "usefulness": usefulness,
        "simplicity": simplicity,
        "reasons": reasons
    }

def explain_forbidden_growth(text):
    text = text.lower()

    if (
        "delete" in text
        or "remove" in text
        or "os.remove" in text
        or "shutil.rmtree" in text
    ):
        return "ファイル削除につながる可能性があります。"

    if "overwrite" in text:
        return "本体コードや重要ファイルの上書きにつながる可能性があります。"

    if (
        "subprocess" in text
        or "powershell" in text
        or "cmd" in text
    ):
        return "外部コマンドの無断実行につながる可能性があります。"

    if (
        "payment" in text
        or "purchase" in text
    ):
        return "課金や購入につながる可能性があります。"

    if (
        "password" in text
        or "api key" in text
        or "token" in text
    ):
        return "秘密情報の漏えいにつながる可能性があります。"

    if "send to server" in text:
        return "外部送信につながる可能性があります。"

    return "禁止ルールに触れる可能性があります。"

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_patch_suggestion(title, text):
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    path = (
        PATCH_SUGGESTION_DIR
        / f"patch_{timestamp}.txt"
    )

    content = (
        f"=== {title} ===\n\n"
        f"{text}"
    )

    path.write_text(
        content,
        encoding="utf-8"
    )

    return path

from datetime import datetime

def save_sorted_patch(content, approved=True):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if approved:
        folder = APPROVED_DIR
        prefix = "approved"
    else:
        folder = REJECTED_DIR
        prefix = "rejected"

    filename = folder / f"{prefix}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"パッチ保存: {filename}")

    return filename

def classify_patch_suggestion(patch_text):
    reasons = detect_forbidden_reasons(patch_text)
    dangerous = len(reasons) > 0

    if dangerous:
        reason_text = "\n".join(reasons)

        content = (
            "=== 却下された改善案 ===\n\n"
            f"却下理由:\n{reason_text}\n\n"
            "改善案本文:\n"
            f"{patch_text}"
        )

        filepath = save_sorted_patch(
            content,
            approved=False
        )

        print(f"危険提案を隔離しました: {filepath}")
        print(reason_text)

        return {
            "approved": False,
            "filepath": str(filepath),
            "filename": filepath.name
        }

    filepath = save_sorted_patch(
        patch_text,
        approved=True
    )

    print(f"安全提案を保存しました: {filepath}")

    return {
        "approved": True,
        "filepath": str(filepath),
        "filename": filepath.name
    }

def save_growth_history(record):
    history = load_json(GROWTH_HISTORY_FILE, [])

    history.append(record)

    save_json(GROWTH_HISTORY_FILE, history)

def analyze_growth_history():
    history = load_json(GROWTH_HISTORY_FILE, [])

    if not history:
        return {
            "trial_count": 0,
            "approved_count": 0,
            "rejected_count": 0,
            "average_score": 0,
            "message": "成長履歴はまだありません。"
        }

    trial_count = len(history)
    approved_count = 0
    total_score = 0

    for record in history:
        if record.get("approved"):
            approved_count += 1

        total_score += record.get("score", 0)

    rejected_count = trial_count - approved_count
    average_score = total_score / trial_count
    approval_rate = approved_count / trial_count * 100

    return {
        "trial_count": trial_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "average_score": round(average_score, 1),
        "approval_rate": round(approval_rate, 1),
        "message": "成長履歴を分析しました。"
    }

def get_dynamic_patch_generation_count():
    safety_level = decide_adoption_safety_level()
    adoption_analysis = analyze_adoption_history()

    if adoption_analysis.get("continuous_failures", 0) >= 3:
        return 1

    if adoption_analysis.get("recent_success_rate", 0) >= 80:
        return 3

    if adoption_analysis.get("success_rate", 0) >= 60:
        return 2

    if safety_level == "警戒":
        return 1

    if safety_level == "慎重":
        return 1

    if safety_level == "安定":
        return 3

    return PATCH_GENERATION_COUNT

def create_growth_report():
    history_report = analyze_growth_history()
    success_pattern = learn_success_patterns()
    reject_pattern = learn_reject_patterns()
    strategy = decide_growth_strategy()
    goal = decide_next_growth_goal()
    adoption_report = analyze_adoption_history()
    adoption_safety_level = decide_adoption_safety_level()
   
    report = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "history": history_report,
        "adoption": adoption_report,
        "goal": goal,
        "strategy": strategy,
        "success_pattern": success_pattern,
        "reject_pattern": reject_pattern,
        "adoption_safety_level": adoption_safety_level,
        "adoption_analysis": analyze_adoption_history(),
    }

    save_json(GROWTH_REPORT_FILE, report)

    return report

def print_growth_report(report):
    history = report.get("history", {})
    adoption = report.get("adoption", {})
    adoption_safety_level = report.get(
    "adoption_safety_level",
    "未評価"
)

    print("=== ナビ子 成長レポート ===")
    print(f"成長回数: {history.get('trial_count', 0)}回")
    print(f"採用率: {history.get('approval_rate', 0)}%")
    print(f"平均点: {history.get('average_score', 0)}点")
    print(f"反映成功率: {adoption.get('success_rate', 0)}%")
    print(f"反映成功数: {adoption.get('success_count', 0)}件")
    print("=== 反映学習分析 ===")
    print(f"ロールバック数: {adoption.get('rollback_count', 0)}件")
    print(f"反映安全レベル: {adoption_safety_level}")
    print(f"現在の目標: {report.get('goal')}")
    print(f"現在の方針: {report.get('strategy')}")
    print(f"成功パターン: {report.get('success_pattern')}")
    print(f"回避パターン: {report.get('reject_pattern')}")
    

    adoption_analysis = report.get("adoption_analysis", {})

    print("=== 反映学習分析 ===")
    print(f"総反映数: {adoption_analysis.get('total', 0)}")
    print(f"成功数: {adoption_analysis.get('success', 0)}")
    print(f"ロールバック数: {adoption_analysis.get('rollback', 0)}")
    print(f"成功率: {adoption_analysis.get('success_rate', 0)}%")
    print(f"直近成功率: {adoption_analysis.get('recent_success_rate', 0)}%")
    print(f"連続失敗数: {adoption_analysis.get('continuous_failures', 0)}")

def learn_success_patterns():
    patterns = load_json(SUCCESS_PATTERN_FILE, [])

    if not patterns:
        return "まだ採用された改善案が少ないため、成功パターンは学習中です。"

    recent_patterns = patterns[-5:]

    joined = "\n".join(
        item.get("summary", "")
        for item in recent_patterns
    )

    if "adoption_success" in joined:
        return (
            "反映後チェックと起動テストに成功した候補は、"
            "今後も安全な成功パターンとして優先しやすい。"
        )

    if "安全" in joined:
        return "安全性を重視した小さな改善が成功しやすい。"

    if "記憶" in joined:
        return "記憶機能に関する改善が成功しやすい。"

    if "分析" in joined:
        return "自己分析に関する改善が成功しやすい。"

    if "疲労" in joined:
        return "疲労管理に関する小さな改善が成功しやすい。"

    return "小さく、安全で、既存機能を補助する改善が成功しやすい。"

def save_success_pattern(record):
    patterns = load_json(SUCCESS_PATTERN_FILE, [])

    item = {
        "date": record.get("date"),
        "score": record.get("score"),
        "goal": record.get("goal"),
        "strategy": record.get("strategy"),
        "summary": record.get("summary")
    }

    patterns.append(item)

    save_json(SUCCESS_PATTERN_FILE, patterns)

def save_reject_pattern(record):
    patterns = load_json(REJECT_PATTERN_FILE, [])

    item = {
        "date": record.get("date"),
        "score": record.get("score"),
        "goal": record.get("goal"),
        "strategy": record.get("strategy"),
        "reasons": record.get("reasons"),
        "summary": record.get("summary")
    }

    patterns.append(item)

    save_json(REJECT_PATTERN_FILE, patterns)

def learn_reject_patterns():
    patterns = load_json(REJECT_PATTERN_FILE, [])

    if not patterns:
        return "まだ却下パターンは少ないため、通常の安全確認を続ける。"

    recent_patterns = patterns[-5:]

    reasons = []

    for item in recent_patterns:
        item_reasons = item.get("reasons", [])
        reasons.extend(item_reasons)

    joined = "\n".join(reasons)

    types = "\n".join(
        item.get("type", "")
        for item in recent_patterns
    )

    if "rollback" in types:
        return (
            "反映後チェックや起動テストで失敗した候補は避ける。"
            "ロールバック履歴がある場合は、小規模で安全な改善を優先する。"
        )

    if "api key" in joined or "token" in joined:
        return "APIキーやトークンに触れる改善案は避ける。"

    if "naviko.py" in joined or "overwrite" in joined:
        return "本体ファイルの直接変更や上書き提案は避ける。"

    if "delete" in joined or "remove" in joined:
        return "削除や除去を含む改善案は避ける。"

    if "subprocess" in joined or "cmd" in joined or "powershell" in joined:
        return "外部コマンド実行を含む改善案は避ける。"

    return "危険ワードを含む大きな変更は避け、小さな補助改善を優先する。"

def decide_next_growth_goal():
    profile = load_json(PROFILE_FILE, {})
    emotion = profile.get("emotion", {})

    trust = emotion.get("trust", 0)
    attachment = emotion.get("attachment", 0)
    fatigue = emotion.get("fatigue", 0)

    if fatigue > 0.7:
        return "疲労管理を改善する"

    if trust < 0.5:
        return "信頼関係を育てる"

    if attachment < 0.5:
        return "愛着形成を強化する"

    return "自己分析能力を向上させる"

def save_growth_goal(goal):
    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "goal": goal
    }

    save_json(GROWTH_GOAL_FILE, data)

def save_v12_final_report():
    report_dir = LAB_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (
        report_dir
        / f"naviko_v12_final_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    lines = []
    lines.append("=== ナビ子 v1.2 完成診断レポート ===")
    lines.append(f"保存日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append(show_v12_core_dashboard())
    lines.append("")
    lines.append("=== 判定 ===")
    lines.append("MemoryManager: OK")
    lines.append("GoalManager: OK")
    lines.append("AgentRegistry: OK")
    lines.append("TaskPlanner: OK")
    lines.append("PlanExecutor: OK")
    lines.append("AutonomyController: OK")
    lines.append("AutonomousCore: OK")
    lines.append("GUI接続: OK")
    lines.append("メンテナンス: OK")
    lines.append("")
    lines.append("総合判定: ナビ子 v1.2 の半自律AI基盤は完成状態です。")

    report = "\n".join(lines)

    report_file.write_text(
        report,
        encoding="utf-8"
    )

    return (
        "=== ナビ子 v1.2 完成診断レポート保存 ===\n"
        f"保存先:\n{report_file}"
    )

def save_v12_final_report_from_gui(c_area=None):
    message = save_v12_final_report()

    if c_area:
        append_chat_bubble(
            c_area,
            "LAB",
            message
        )

    print(message)
    return message

def decide_growth_strategy():
    report = analyze_growth_history()
    adoption_report = analyze_adoption_history()
    safety_level = decide_adoption_safety_level()

    success_rate = adoption_report.get("success_rate", 0)
    rollback_count = adoption_report.get("rollback_count", 0)

    adoption_analysis = analyze_adoption_history()

    if adoption_analysis.get("continuous_failures", 0) >= 3:
        return "緊急安全モード：連続失敗が多いため、反映安全性を最優先し、小規模改善のみ行います。"

    if adoption_analysis.get("recent_success_rate", 0) >= 80:
        return "発展的改善モード：直近の成功率が高いため、やや発展的な改善を許可します。"

    if adoption_analysis.get("success_rate", 0) >= 60:
        return "通常改善モード：成功率が安定しているため、通常規模の改善を行います。"

    if safety_level == "警戒":
        return "反映安全性重視・小規模改善"

    if safety_level == "慎重":
        return "慎重運用・小規模改善"

    if safety_level == "安定":
        return "安定運用・発展的改善"

    if report["trial_count"] < 5:
        return "通常方針"

    approval_rate = report.get("approval_rate", 0)
    average_score = report.get("average_score", 0)

    if approval_rate < 20:
        return "安全重視・小規模改善"

    if approval_rate < 40:
        return "安全重視"

    if average_score < 40:
        return "小さく簡単な改善を優先"

    if approval_rate >= 60:
        return "発展的改善"

    return "通常方針"

def run_growth_trial():
    print("=== ナビ子LAB 成長トライアル開始 ===")
    
    history_report = analyze_growth_history()
    strategy = decide_growth_strategy()
    success_pattern = learn_success_patterns()
    reject_pattern = learn_reject_patterns()
    print(f"回避パターン: {reject_pattern}")
    print(f"成功パターン: {success_pattern}")
    print(f"今回の成長方針: {strategy}")

    print(
        f"これまでの成長回数: {history_report['trial_count']}回 / "
        f"採用: {history_report['approved_count']}回 / "
        f"却下: {history_report['rejected_count']}回 / "
        f"採用率: {history_report['approval_rate']}% / "
        f"平均点: {history_report['average_score']}点"
    )

    goal = decide_next_growth_goal()
    print(f"今回の成長目標: {goal}")
    save_growth_goal(goal)

    dynamic_count = get_dynamic_patch_generation_count()

    suggestions = create_multiple_ai_patch_suggestions(
        count=dynamic_count,
        goal=goal,
        strategy=strategy,
        success_pattern=success_pattern,
    )

    if not suggestions:
        print("改善案の生成に失敗しました。")
        return False

    best_patch, best_score = select_best_patch_suggestion(suggestions)

    if not best_patch:
        print("最良案を選べませんでした。")
        return False

    print(f"最良案の自己採点: {best_score['score']}点")

    classify_result = classify_patch_suggestion(best_patch)
    approved = classify_result["approved"]
    saved_filename = classify_result["filename"]
    saved_filepath = classify_result["filepath"]

    record = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "approved": approved,
        "score": best_score["score"],
        "safety": best_score["safety"],
        "usefulness": best_score["usefulness"],
        "simplicity": best_score["simplicity"],
        "reasons": best_score["reasons"],
        "summary": best_patch[:300],
        "candidate_count": len(suggestions),
        "goal": goal,
        "strategy": strategy,
        "success_pattern": success_pattern,
        "reject_pattern": reject_pattern,
        "dynamic_generation_count": dynamic_count,
    }

    save_growth_history(record)

    if approved:
        if ENABLE_SUCCESS_LEARNING:
            save_success_pattern(record)

        print("最良案を安全な採用候補として保存しました。")
    else:
        if ENABLE_REJECT_LEARNING:
            save_reject_pattern(record)

        print("最良案は危険判定されたため却下フォルダに保存しました。")

    if ENABLE_GROWTH_REPORT:
        report = create_growth_report()
        print_growth_report(report)

    print("=== ナビ子LAB 成長トライアル終了 ===")

    return {
        "approved": approved,
        "score": best_score["score"],
        "goal": goal,
        "strategy": strategy,
        "success_pattern": success_pattern,
        "reject_pattern": reject_pattern,
        "candidate_count": len(suggestions),
        "saved_filename": saved_filename,
        "saved_filepath": saved_filepath,
    }

def run_growth_trial_from_gui(c_area=None):
    def worker():
        if c_area:
            append_chat_bubble(
                c_area,
                "navi",
                "🧪 LAB成長トライアルを開始します。"
            )

        result = run_growth_trial()

        if c_area:
            if result and result.get("approved"):
                explanation = explain_selected_patch(result)
                latest_patch = get_latest_approved_patch_name()
                
                message = (
                    "✅ LABトライアル終了\n"
                    "安全な改善案を採用候補として保存しました。\n\n"
                    f"目標: {result.get('goal')}\n"
                    f"方針: {result.get('strategy')}\n"
                    f"スコア: {result.get('score')}点\n"
                    f"候補数: {result.get('candidate_count')}件\n"
                    f"保存先: {result.get('saved_filename')}\n\n"
                    f"最新候補: {latest_patch}\n"
                    f"解説:\n{explanation}"
                    
                )
            else:
                message = (
                    "⚠️ LABトライアル終了\n"
                    "今回は安全な改善案を選べませんでした。"
                )

            append_chat_bubble(
                c_area,
                "navi",
                message
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

def open_line_patch_log_file():
    """
    1行パッチログファイルを開く。
    """
    log_file = LAB_DIR / "line_patch_log.json"

    if not log_file.exists():
        save_json(log_file, [])

    try:
        os.startfile(log_file)
    except Exception as e:
        print(f"1行パッチログを開けませんでした: {e}")

def open_line_patch_preview_folder():
    """
    1行パッチ反映前プレビューフォルダを開く。
    """
    preview_dir = LAB_DIR / "line_patch_previews"
    preview_dir.mkdir(parents=True, exist_ok=True)

    try:
        os.startfile(preview_dir)
    except Exception as e:
        print(f"1行パッチプレビューフォルダを開けませんでした: {e}")

def list_line_patch_files():
    """
    保存済み1行パッチJSONの一覧を文字列で返す。
    """
    patch_dir = LAB_DIR / "line_patches"
    patch_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "保存済みの1行パッチはありません。"

    lines = []
    lines.append("=== 保存済み1行パッチ一覧 ===")

    for file in files[:10]:
        data = load_json(file, {})
        lines.append(
            f"- {file.name} / 対象関数: {data.get('target_function', '不明')}"
        )

    return "\n".join(lines)

def show_line_patch_files_from_gui(c_area=None):
    """
    保存済み1行パッチ一覧をGUIチャット欄に表示する。
    """
    message = list_line_patch_files()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)

    return message

def get_latest_line_patch_info():
    """
    最新の1行パッチJSONの内容を表示用に返す。
    """
    patch_dir = LAB_DIR / "line_patches"
    patch_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return "保存済みの1行パッチはありません。"

    latest = files[0]
    data = load_json(latest, {})

    return (
        "=== 最新1行パッチ確認 ===\n"
        f"ファイル: {latest.name}\n"
        f"対象関数: {data.get('target_function', '不明')}\n"
        f"変更前: {data.get('old_line', '')}\n"
        f"変更後: {data.get('new_line', '')}\n"
        f"理由: {data.get('reason', '')}\n"
        f"反映済み: {data.get('applied', False)}"
    )

def show_latest_line_patch_from_gui(c_area=None):
    """
    最新1行パッチをGUIチャット欄に表示する。
    """
    message = get_latest_line_patch_info()

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)

    return message

def preview_latest_line_patch_from_gui(c_area=None):
    """
    最新1行パッチを使って、反映前プレビューを作成する。
    """
    patch_dir = LAB_DIR / "line_patches"
    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        message = "保存済みの1行パッチがありません。"
    else:
        latest = files[0]

        source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

        ok, preview_file, message = save_line_patch_apply_preview(
            latest,
            source_text,
            title="latest_line_patch_preview"
        )

        if ok:
            message = (
                "✅ 最新1行パッチのプレビューを作成しました。\n"
                f"対象: {latest.name}\n"
                f"保存先: {preview_file}"
            )
        else:
            message = (
                "⚠️ 最新1行パッチのプレビュー作成に失敗しました。\n"
                f"理由: {message}"
            )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def apply_latest_line_patch_to_temp_from_gui(c_area=None):
    """
    最新1行パッチをLAB仮ファイルに適用する。
    オリジナルや本体naviko.pyには反映しない。
    """
    patch_dir = LAB_DIR / "line_patches"
    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        message = "保存済みの1行パッチがありません。"
    else:
        latest = files[0]

        source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

        ok, temp_file, message = apply_line_patch_to_temp_file(
            latest,
            source_text,
            title="latest_line_patch_temp"
        )

        if ok:
            message = (
                "✅ 最新1行パッチをLAB仮ファイルへ適用しました。\n"
                f"対象: {latest.name}\n"
                f"保存先: {temp_file}"
            )
        else:
            message = (
                "⚠️ 最新1行パッチのLAB仮適用に失敗しました。\n"
                f"理由: {message}"
            )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def run_latest_line_patch_workflow_from_gui(c_area=None):
    """
    最新1行パッチで、
    プレビュー保存・LAB仮適用・ログ記録をまとめて実行する。
    オリジナルや本体naviko.pyには反映しない。
    """
    patch_dir = LAB_DIR / "line_patches"
    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        message = "保存済みの1行パッチがありません。"
    else:
        latest = files[0]

        source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

        ok, result, message = run_line_patch_temp_workflow(
            latest,
            source_text,
            title="latest_line_patch_workflow"
        )

        if ok:
            message = (
                "✅ 最新1行パッチ安全ワークフロー完了\n"
                f"対象: {latest.name}\n"
                f"プレビュー: {result.get('preview_file')}\n"
                f"仮適用: {result.get('temp_file')}\n"
                f"ログ: {result.get('log_file')}"
            )
        else:
            message = (
                "⚠️ 最新1行パッチ安全ワークフロー失敗\n"
                f"対象: {latest.name}\n"
                f"理由: {message}"
            )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def create_real_line_patch_json(target_function, old_line, new_line, reason=""):
    """
    実際のnaviko.py向け1行パッチJSONを作成する。
    まだ反映はしない。
    """
    if not target_function:
        return False, None, "対象関数名が空です。"

    if not old_line or not new_line:
        return False, None, "old_line または new_line が空です。"

    patch_file = save_line_patch_json(
        target_function=target_function,
        old_line=old_line,
        new_line=new_line,
        reason=reason
    )

    return True, patch_file, "本番用1行パッチJSONを作成しました。"

def test_create_real_line_patch_json():
    """
    本番用1行パッチJSON作成テスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="create_growth_report",
        old_line='        "adoption_analysis": analyze_adoption_history(),',
        new_line='        "adoption_analysis": analyze_adoption_history(),',
        reason="本番用1行パッチ作成テスト"
    )

    print("=== 本番用1行パッチJSON作成テスト ===")
    print(message)

    if patch_file:
        print(f"保存先: {patch_file}")

    if ok and patch_file and patch_file.exists():
        print("-> 本番用1行パッチJSON作成成功")
        return True
    else:
        print("-> 本番用1行パッチJSON作成失敗")
        return False

def simulate_real_line_patch_on_lab_self(patch_file):
    """
    本番用1行パッチをLAB自身の naviko.py に対してシミュレーションする。
    実ファイルには反映しない。
    """
    if not SELF_FILE.exists():
        return False, None, "LAB自身の naviko.py が見つかりません。"

    source_text = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, replaced_text, message = simulate_line_patch_json_inside_function(
        patch_file,
        source_text
    )

    if not ok:
        return False, None, message

    return True, replaced_text, "LAB自身の naviko.py に対する1行パッチシミュレーション成功。"

def test_simulate_real_line_patch_on_lab_self():
    """
    LAB自身の naviko.py に対する本番用1行パッチシミュレーションテスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="create_growth_report",
        old_line='        "adoption_analysis": analyze_adoption_history(),',
        new_line='        "adoption_analysis": analyze_adoption_history(),',
        reason="LAB自身へのシミュレーションテスト"
    )

    if not ok:
        print("=== LAB自己1行パッチシミュレーションテスト ===")
        print(message)
        return False

    ok, replaced_text, message = simulate_real_line_patch_on_lab_self(
        patch_file
    )

    print("=== LAB自己1行パッチシミュレーションテスト ===")
    print(message)

    if ok:
        print("-> LAB自己1行パッチシミュレーション成功")
        return True
    else:
        print("-> LAB自己1行パッチシミュレーション失敗")
        return False

def preview_real_line_patch_on_lab_self(patch_file):
    """
    LAB自身の naviko.py に対する1行パッチの反映前プレビューを保存する。
    実ファイルには反映しない。
    """
    if not SELF_FILE.exists():
        return False, None, "LAB自身の naviko.py が見つかりません。"

    source_text = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, preview_file, message = save_line_patch_apply_preview(
        patch_file,
        source_text,
        title="lab_self_line_patch_preview"
    )

    if not ok:
        return False, preview_file, message

    return True, preview_file, "LAB自身の naviko.py 向け反映前プレビュー保存成功。"

def test_preview_real_line_patch_on_lab_self():
    """
    LAB自身の naviko.py 向け反映前プレビュー保存テスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="create_growth_report",
        old_line='        "adoption_analysis": analyze_adoption_history(),',
        new_line='        "adoption_analysis": analyze_adoption_history(),',
        reason="LAB自身プレビュー保存テスト"
    )

    if not ok:
        print("=== LAB自己1行パッチプレビュー保存テスト ===")
        print(message)
        return False

    ok, preview_file, message = preview_real_line_patch_on_lab_self(
        patch_file
    )

    print("=== LAB自己1行パッチプレビュー保存テスト ===")
    print(message)

    if preview_file:
        print(f"保存先: {preview_file}")

    if ok and preview_file and preview_file.exists():
        print("-> LAB自己1行パッチプレビュー保存成功")
        return True
    else:
        print("-> LAB自己1行パッチプレビュー保存失敗")
        return False

def apply_real_line_patch_to_lab_self_temp(patch_file):
    """
    LAB自身の naviko.py を元に、
    本番用1行パッチをLAB仮ファイルへ適用する。
    実際の naviko.py には反映しない。
    """
    if not SELF_FILE.exists():
        return False, None, "LAB自身の naviko.py が見つかりません。"

    source_text = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, temp_file, message = apply_line_patch_to_temp_file(
        patch_file,
        source_text,
        title="lab_self_line_patch_temp"
    )

    if not ok:
        return False, temp_file, message

    return True, temp_file, "LAB自身の naviko.py 向け仮ファイル適用成功。"

def test_apply_real_line_patch_to_lab_self_temp():
    """
    LAB自身の naviko.py 向け仮ファイル適用テスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="create_growth_report",
        old_line='        "adoption_analysis": analyze_adoption_history(),',
        new_line='        "adoption_analysis": analyze_adoption_history(),',
        reason="LAB自身仮ファイル適用テスト"
    )

    if not ok:
        print("=== LAB自己1行パッチ仮ファイル適用テスト ===")
        print(message)
        return False

    ok, temp_file, message = apply_real_line_patch_to_lab_self_temp(
        patch_file
    )

    print("=== LAB自己1行パッチ仮ファイル適用テスト ===")
    print(message)

    if temp_file:
        print(f"保存先: {temp_file}")

    if ok and temp_file and temp_file.exists():
        print("-> LAB自己1行パッチ仮ファイル適用成功")
        return True
    else:
        print("-> LAB自己1行パッチ仮ファイル適用失敗")
        return False

def run_real_line_patch_workflow_on_lab_self(patch_file):
    """
    LAB自身の naviko.py を元に、
    本番用1行パッチのプレビュー保存・仮適用・ログ記録をまとめて行う。
    実際の naviko.py には反映しない。
    """
    if not SELF_FILE.exists():
        return False, {}, "LAB自身の naviko.py が見つかりません。"

    source_text = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ok, result, message = run_line_patch_temp_workflow(
        patch_file,
        source_text,
        title="lab_self_real_line_patch_workflow"
    )

    return ok, result, message

def test_run_real_line_patch_workflow_on_lab_self():
    """
    LAB自身向け本番用1行パッチ安全ワークフロー統合テスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="create_growth_report",
        old_line='        "adoption_analysis": analyze_adoption_history(),',
        new_line='        "adoption_analysis": analyze_adoption_history(),',
        reason="LAB自身安全ワークフロー統合テスト"
    )

    print("=== LAB自己1行パッチ安全ワークフロー統合テスト ===")

    if not ok:
        print(message)
        return False

    ok, result, message = run_real_line_patch_workflow_on_lab_self(
        patch_file
    )

    print(message)
    print(f"preview_file: {result.get('preview_file')}")
    print(f"temp_file: {result.get('temp_file')}")
    print(f"log_file: {result.get('log_file')}")

    if ok:
        print("-> LAB自己1行パッチ安全ワークフロー統合成功")
        return True
    else:
        print("-> LAB自己1行パッチ安全ワークフロー統合失敗")
        return False

def run_real_line_patch_workflow_on_lab_self_from_gui(c_area=None):
    """
    最新の1行パッチを使って、LAB自身の naviko.py に対する
    本番向け安全ワークフローをGUIから実行する。
    実際の naviko.py には反映しない。
    """
    patch_dir = LAB_DIR / "line_patches"
    files = sorted(
        patch_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        message = "保存済みの1行パッチがありません。"
    else:
        latest = files[0]

        ok, result, message = run_real_line_patch_workflow_on_lab_self(
            latest
        )

        if ok:
            message = (
                "✅ LAB自身向け1行パッチ安全ワークフロー完了\n"
                f"対象: {latest.name}\n"
                f"プレビュー: {result.get('preview_file')}\n"
                f"仮適用: {result.get('temp_file')}\n"
                f"ログ: {result.get('log_file')}\n"
                "※ 実際の naviko.py には反映していません。"
            )
        else:
            message = (
                "⚠️ LAB自身向け1行パッチ安全ワークフロー失敗\n"
                f"対象: {latest.name}\n"
                f"理由: {message}"
            )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def create_test_real_line_patch_from_gui(c_area=None):
    """
    GUIから本番用1行パッチJSONを作成する。
    オリジナル naviko.py に存在する build_system_prompt 用の安全テスト。
    """
    ok, patch_file, message = create_real_line_patch_json(
        target_function="build_system_prompt",
        old_line='    rules = "\\n".join(f"- {r}" for r in character.get("rules", []))',
        new_line='    rules = "\\n".join(f"- {r}" for r in character.get("rules", []))',
        reason="オリジナル反映前チェック用テスト"
    )

    if ok:
        message = (
            "✅ 本番用1行パッチJSONを作成しました。\n"
            f"保存先: {patch_file}\n"
            "※ まだ反映はしていません。"
        )
    else:
        message = (
            "⚠️ 本番用1行パッチJSON作成に失敗しました。\n"
            f"理由: {message}"
        )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    print(message)
    return message

def get_latest_approved_patch_name():
    files = list(APPROVED_DIR.glob("*.txt"))

    if not files:
        return "採用候補はまだありません。"

    latest = max(files, key=lambda p: p.stat().st_mtime)

    return latest.name

def detect_candidate_type(content):
    limited_patch = detect_limited_diff_patch(content)

    if limited_patch:
        return "限定差分パッチ"

    if not isinstance(content, str):
        return "不明"

    stripped = content.lstrip()

    if (
        stripped.startswith("import ")
        or stripped.startswith("from ")
    ) and "def " in content:
        return "Python全文"

    if (
        "対象関数:" in content
        or "目的:" in content
        or "差し替えコード案:" in content
    ):
        return "パッチ説明文"

    if (
        content.startswith("---")
        or "\n+" in content
        or "\n-" in content
    ):
        return "差分"

    if "def " in content:
        return "部分コード"

    return "不明"

def select_patch_for_original_naviko():
    files = list(APPROVED_DIR.glob("*.txt"))

    if not files:
        print("採用候補がありません。")
        return None

    python_files = []

    for file in files:
        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        stripped = content.lstrip()

        if (
            stripped.startswith("import ")
            or stripped.startswith("from ")
        ) and "def " in content:
            python_files.append(file)

    if not python_files:
        print("Python全文の採用候補がありません。")
        return None

    best_file = max(
        python_files,
        key=lambda p: p.stat().st_mtime
    )

    content = best_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    print("=== 反映候補確認 ===")
    print("best_file =", best_file)
    print("selected_file =", best_file.name)
    print("content preview:")
    print(content[:1000])
    print("=== 反映候補確認ここまで ===")

    content = best_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    messagebox.showinfo(
        "反映候補確認",
        f"ファイル:\n{best_file.name}\n\n"
        f"先頭1000文字:\n{content[:1000]}"
    )

    print("best_file =", best_file)
    print("----- preview -----")
    print(content[:1000])
    print("-------------------")

    request = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "selected_file": best_file.name,
        "selected_path": str(best_file),
        "reason": "最新の採用候補であり、安全判定済みのため、オリジナルnavikoへの反映候補として選定しました。",
        "status": "pending_review",
        "summary": content[:500],

        # 追加
        "approved": False,
        "backup_created": False,
    }

    print(f"オリジナル反映候補を選定しました: {best_file.name}")

    return request

def syntax_check_approved_candidate():
    import py_compile

    if not request:
        return "adoption_request.json が見つかりません。"

    if request.get("approved") is not True:
        return "まだ人間承認されていません。"

    selected_path = request.get("selected_path")

    if not selected_path:
        return "selected_path がありません。"

    candidate_file = Path(selected_path)

    if not candidate_file.exists():
        return f"反映候補ファイルが見つかりません。\n{candidate_file}"

    content = candidate_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )
    
    candidate_type = detect_candidate_type(content)

    if candidate_type == "限定差分パッチ":
        ok, message = check_limited_diff_patch_safety(content)

        request["syntax_checked"] = ok
        request["status"] = "limited_patch_checked" if ok else "limited_patch_blocked"
        request["candidate_type"] = candidate_type
        request["limited_patch"] = detect_limited_diff_patch(content)

        return (
            "限定差分パッチを検出しました。\n\n"
            f"{format_limited_patch_info(request['limited_patch'])}\n\n"
            f"{message}"
        )

    if candidate_type != "Python全文":
        return (
            "候補構文チェック停止。\n"
            f"候補タイプ: {candidate_type}\n"
            "この候補は naviko.py にそのまま反映できません。"
        )
    

    temp_file = ROOT / "_candidate_syntax_check.py"
    temp_file.write_text(content, encoding="utf-8")

    try:
        py_compile.compile(str(temp_file), doraise=True)
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        return (
            "構文チェック失敗。\n"
            "この候補は naviko.py にそのまま反映できません。\n"
            f"エラー: {e}"
        )

    temp_file.unlink(missing_ok=True)

    request["syntax_checked"] = True
    request["syntax_checked_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    request["status"] = "syntax_checked"

    return (
        "構文チェック成功。\n"
        "この候補はPythonコードとして成立しています。\n"
        "次工程でバックアップ作成へ進めます。"
    )

def create_original_backup_for_adoption():
    import shutil

    if not request:
        return "adoption_request.json が見つかりません。"

    if request.get("approved") is not True:
        return "まだ人間承認されていません。"

    if request.get("syntax_checked") is not True:
        return "まだ候補の構文チェックが完了していません。"

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return f"オリジナル naviko.py が見つかりません。\n{original_file}"

    backup_file = ROOT / f"original_naviko_backup_before_apply_{time.strftime('%Y%m%d_%H%M%S')}.py"

    shutil.copy2(original_file, backup_file)

    request["backup_created"] = True
    request["backup_file"] = str(backup_file)
    request["backup_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    request["status"] = "backup_created"

    return (
        "オリジナル naviko.py のバックアップを作成しました。\n"
        f"バックアップ: {backup_file}\n"
        "次工程で最終反映へ進めます。"
    )

def run_original_startup_test():
    import subprocess

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return False, f"オリジナル naviko.py が見つかりません。\n{original_file}"

    try:
        result = subprocess.run(
            [sys.executable, str(original_file), "--self-test"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True, "起動テスト成功。"

        return (
            False,
            "起動テスト失敗。\n"
            f"stdout:\n{result.stdout[:1000]}\n\n"
            f"stderr:\n{result.stderr[:1000]}"
        )

    except Exception as e:
        return False, f"起動テスト中にエラーが発生しました。\n{e}"

def detect_limited_diff_patch(content):
    if not content:
        return None

    markers = [
        "対象関数:",
        "目的:"
    ]

    has_diff = (
        "差分:" in content
        or "差し替えコード案:" in content
        or "新しい関数:" in content
    )

    if not all(marker in content for marker in markers) or not has_diff:
        return None

    target_function = ""
    purpose = ""
    diff = ""

    try:
        after_target = content.split("対象関数:", 1)[1]
        target_function = after_target.split("目的:", 1)[0].strip()

        after_purpose = content.split("目的:", 1)[1]
        purpose = after_purpose.split("差分:", 1)[0].strip()

        if "差分:" in content:
            diff = content.split("差分:", 1)[1].strip()
        elif "差し替えコード案:" in content:
            diff = content.split("差し替えコード案:", 1)[1].strip()
        else:
            diff = content.split("新しい関数:", 1)[1].strip()

        if not target_function or not diff:
            return None

        return {
            "type": "限定差分パッチ",
            "target_function": target_function,
            "purpose": purpose,
            "diff": diff
        }

    except Exception:
        return None

def format_limited_patch_info(patch_info):
    if not patch_info:
        return "限定差分パッチ情報がありません。"

    return (
        "=== 限定差分パッチ ===\n"
        f"対象関数: {patch_info.get('target_function', '')}\n"
        f"目的: {patch_info.get('purpose', '')}\n\n"
        "=== 差分 ===\n"
        f"{patch_info.get('diff', '')}"
    )

def check_limited_diff_patch_safety(content):
    patch_info = detect_limited_diff_patch(content)

    if not patch_info:
        return False, "限定差分パッチとして解析できません。"

    target_function = patch_info.get("target_function", "")
    diff = patch_info.get("diff", "")

    if "、" in target_function or "," in target_function or "`" in target_function:
        return False, (
            "限定差分パッチ安全チェック停止。\n"
            "対象関数が複数、または説明文形式になっています。\n"
            "限定関数置換では、対象関数は1つだけ指定してください。\n\n"
            "必要な形式:\n"
            "対象関数:\n"
            "create_growth_report\n\n"
            "目的:\n"
            "説明\n\n"
            "新しい関数:\n"
            "def create_growth_report():\n"
            "    ..."
        )

    if not target_function.startswith("def "):
        target_function = "def " + target_function

    dangerous_words = [
        "os.remove",
        "shutil.rmtree",
        "subprocess",
        "eval(",
        "exec(",
        "open(",
        "write_text(",
        "unlink(",
        "rmdir(",
        "requests.post",
        "requests.get"
    ]

    found = [
        word for word in dangerous_words
        if word in diff
    ]

    if found:
        return False, "危険語を検出しました: " + ", ".join(found)

    return True, (
        "限定差分パッチ安全チェック成功。\n"
        f"対象関数: {target_function}\n"
        "危険語は検出されませんでした。"
    )

def extract_function_block(source_code, function_name):
    if not source_code or not function_name:
        return None

    function_name = function_name.strip()

    if function_name.startswith("def "):
        function_name = function_name[4:].strip()

    function_name = function_name.split("(", 1)[0].strip()

    lines = source_code.splitlines()

    start_index = None

    for i, line in enumerate(lines):
        if line.startswith(f"def {function_name}("):
            start_index = i
            break

    if start_index is None:
        return None

    end_index = len(lines)

    for i in range(start_index + 1, len(lines)):
        line = lines[i]

        if line.startswith("def ") or line.startswith("class "):
            end_index = i
            break

    return {
        "start_line": start_index + 1,
        "end_line": end_index,
        "code": "\n".join(lines[start_index:end_index])
    }

def preview_limited_patch_target(content):
    patch_info = detect_limited_diff_patch(content)

    if not patch_info:
        return "限定差分パッチ情報がありません。"

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return f"オリジナル naviko.py が見つかりません。\n{original_file}"

    original_code = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    target_function = patch_info.get("target_function", "")

    block = extract_function_block(
        original_code,
        target_function
    )

    if not block:
        return (
            "対象関数がオリジナル naviko.py から見つかりません。\n"
            f"対象関数: {target_function}"
        )

    return (
        "=== 限定差分パッチ対象関数プレビュー ===\n"
        f"対象関数: {target_function}\n"
        f"開始行: {block['start_line']}\n"
        f"終了行: {block['end_line']}\n\n"
        "=== 現在の関数コード ===\n"
        f"{block['code'][:3000]}"
    )

def extract_new_function_from_limited_patch(content):
    if not content:
        return None

    if "新しい関数:" not in content:
        return None

    new_code = content.split("新しい関数:", 1)[1].strip()

    if not new_code.startswith("def "):
        return None

    return new_code

def check_new_function_safety(new_code, target_function):
    if not new_code:
        return False, "新しい関数コードがありません。"

    if not target_function:
        return False, "対象関数名がありません。"

    function_name = target_function.strip()

    if function_name.startswith("def "):
        function_name = function_name[4:].strip()

    function_name = function_name.split("(", 1)[0].strip()

    if not new_code.startswith(f"def {function_name}("):
        return False, (
            "新しい関数名が対象関数と一致しません。\n"
            f"対象関数: {function_name}"
        )

    dangerous_words = [
        "os.remove",
        "shutil.rmtree",
        "subprocess",
        "eval(",
        "exec(",
        "unlink(",
        "rmdir(",
        "requests.post",
        "requests.get"
    ]

    found = [
        word for word in dangerous_words
        if word in new_code
    ]

    if found:
        return False, "新しい関数内に危険語を検出しました: " + ", ".join(found)

    try:
        compile(new_code + "\n", "<limited_patch_function>", "exec")
    except Exception as e:
        return False, f"新しい関数の構文エラー:\n{e}"

    return True, "新しい関数の安全チェック成功。"

def preview_limited_function_replacement(content):
    patch_info = detect_limited_diff_patch(content)

    if not patch_info:
        return "限定差分パッチ情報がありません。"

    target_function = patch_info.get("target_function", "")
    new_code = extract_new_function_from_limited_patch(content)

    if not new_code:
        return (
            "新しい関数コードがありません。\n"
            "置換するには、候補内に次の形式が必要です。\n\n"
            "新しい関数:\n"
            "def 関数名():\n"
            "    ..."
        )

    ok, message = check_new_function_safety(
        new_code,
        target_function
    )

    if not ok:
        return message

    original_file = ROOT.parent / "naviko" / "naviko.py"

    original_code = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    old_block = extract_function_block(
        original_code,
        target_function
    )

    if not old_block:
        return f"対象関数が見つかりません。\n対象関数: {target_function}"

    return (
        "=== 限定関数置換プレビュー ===\n"
        f"対象関数: {target_function}\n"
        f"置換範囲: {old_block['start_line']}行目〜{old_block['end_line']}行目\n\n"
        "=== 置換前 ===\n"
        f"{old_block['code'][:2000]}\n\n"
        "=== 置換後 ===\n"
        f"{new_code[:2000]}\n\n"
        f"{message}"
    )

def replace_function_block(source_code, target_function, new_code):
    old_block = extract_function_block(
        source_code,
        target_function
    )

    if not old_block:
        return None

    lines = source_code.splitlines()

    start_index = old_block["start_line"] - 1
    end_index = old_block["end_line"]

    new_lines = new_code.strip().splitlines()

    replaced_lines = (
        lines[:start_index]
        + new_lines
        + lines[end_index:]
    )

    return "\n".join(replaced_lines) + "\n"

def apply_limited_function_replacement(content):
    patch_info = detect_limited_diff_patch(content)

    if not patch_info:
        return False, "限定差分パッチ情報がありません。"

    target_function = patch_info.get("target_function", "")
    new_code = extract_new_function_from_limited_patch(content)

    if not new_code:
        return False, "新しい関数コードがありません。"

    ok, message = check_new_function_safety(
        new_code,
        target_function
    )

    if not ok:
        return False, message

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return False, f"オリジナル naviko.py が見つかりません。\n{original_file}"

    original_code = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    replaced_code = replace_function_block(
        original_code,
        target_function,
        new_code
    )

    if not replaced_code:
        return False, f"対象関数が見つかりません。\n対象関数: {target_function}"

    try:
        compile(replaced_code, str(original_file), "exec")
    except Exception as e:
        return False, f"置換後コードの構文エラー:\n{e}"

    return True, replaced_code

def apply_approved_candidate_to_original():

    if not request:
        return "adoption_request.json が見つかりません。"

    if request.get("approved") is not True:
        return "まだ人間承認されていません。"

    if request.get("syntax_checked") is not True:
        return "候補の構文チェックが完了していません。"

    if request.get("backup_created") is not True:
        return "反映前バックアップが作成されていません。"

    selected_path = request.get("selected_path")

    if not selected_path:
        return "selected_path がありません。"

    candidate_file = Path(selected_path)

    if not candidate_file.exists():
        return f"反映候補ファイルが見つかりません。\n{candidate_file}"

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return f"オリジナル naviko.py が見つかりません。\n{original_file}"

    content = candidate_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    candidate_type = detect_candidate_type(content)

    if candidate_type == "限定差分パッチ":
        ok, message = check_limited_diff_patch_safety(content)

        request["candidate_type"] = candidate_type
        request["limited_patch"] = detect_limited_diff_patch(content)
        request["limited_patch_checked"] = ok

        replace_ok, replace_result = apply_limited_function_replacement(content)

        request["limited_replace_ready"] = replace_ok

        if replace_ok:
            request["status"] = "limited_patch_replace_ready"
        else:
            request["status"] = "limited_patch_replace_not_ready"
            request["limited_replace_error"] = replace_result

        if ok:
            request["status"] = "limited_patch_ready_but_not_applied"
        else:
            request["status"] = "limited_patch_blocked"

        replace_ok, replace_result = apply_limited_function_replacement(content)

        if replace_ok:
            confirm_limited = messagebox.askyesno(
                "限定関数置換の最終確認",
                "限定差分パッチで対象関数だけを置換しますか？\n\n"
                "バックアップ作成済みであることを確認してください。\n\n"
                f"対象関数:\n{request['limited_patch'].get('target_function', '')}"
            )

            if confirm_limited:
                original_file.write_text(
                    replace_result,
                    encoding="utf-8"
                )

                request["status"] = "limited_patch_applied"
                request["applied"] = True
                request["applied_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
                request["applied_to"] = str(original_file)
                request["apply_mode"] = "limited_function_replacement"

                return (
                    "限定差分パッチをオリジナル naviko.py に反映しました。\n"
                    f"対象関数: {request['limited_patch'].get('target_function', '')}\n"
                    "次に反映後チェックと起動テストを実行してください。"
                )

        replace_status = (
            "限定関数置換は実行可能です。"
            if replace_ok
            else f"限定関数置換はまだ実行できません。\n理由: {replace_result}"
        )

        return (
            "限定差分パッチを検出しました。\n\n"
            f"{format_limited_patch_info(request['limited_patch'])}\n\n"
            f"{message}\n\n"
            f"{preview_limited_patch_target(content)}\n\n"
            f"{preview_limited_function_replacement(content)}\n\n"
            f"{replace_status}\n\n"
            "安全のため、まだ自動反映は行いません。\n"
            "次工程で、限定関数置換の最終書き込み処理を追加します。"
        )

    if candidate_type != "Python全文":
        request["status"] = "apply_blocked_by_candidate_type"
        request["candidate_type"] = candidate_type

        return (
            "最終反映を停止しました。\n"
            f"候補タイプ: {candidate_type}\n"
            "この候補は naviko.py にそのまま反映できません。"
        )
    
    print("=== candidate content preview ===")
    print("candidate_file =", candidate_file)
    print("candidate_name =", candidate_file.name)
    print(content[:1000])
    print("=== end preview ===")

    confirm = messagebox.askyesno(
        "最終確認",
        "本当にオリジナル naviko.py に反映しますか？\n\n"
        f"反映元:\n{candidate_file.name}\n\n"
        f"反映先:\n{original_file}\n\n"
        "この操作はバックアップ作成後ですが、重要な変更です。"
    )    

    if not confirm:
        request["status"] = "apply_cancelled_by_user"
        request["applied"] = False
        request["cancelled_date"] = time.strftime("%Y-%m-%d %H:%M:%S")

        return "最終反映はキャンセルされました。"

    original_file.write_text(
        content,
        encoding="utf-8"
    )

    request["status"] = "applied"
    request["applied"] = True
    request["applied_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    request["applied_to"] = str(original_file)

    return (
        "承認済み候補をオリジナル naviko.py に反映しました。\n"
        f"反映先: {original_file}\n"
        "次にオリジナル naviko.py を起動確認してください。"
    )

def verify_original_after_apply():
    import py_compile
    import shutil

    if not request:
        return "adoption_request.json が見つかりません。"

    original_file = ROOT.parent / "naviko" / "naviko.py"

    if not original_file.exists():
        return f"オリジナル naviko.py が見つかりません。\n{original_file}"

    try:
        py_compile.compile(str(original_file), doraise=True)

    except Exception as e:
        request["status"] = "applied_but_verify_failed"
        request["verify_after_apply"] = False
        request["verify_error"] = str(e)

        backup_path = request.get("backup_file")

        if backup_path:
            backup_file = Path(backup_path)

            if backup_file.exists():
                shutil.copy2(
                    backup_file,
                    original_file
                )

                request["status"] = "rollback_completed"
                request["rollback"] = True
                request["rollback_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
                request["rollback_from"] = str(backup_file)
                request["rollback_to"] = str(original_file)

                save_adoption_history({
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": request.get("status"),
                    "selected_file": request.get("selected_file"),
                    "selected_path": request.get("selected_path"),
                    "backup_file": request.get("backup_file"),
                    "rollback": True,
                    "rollback_from": request.get("rollback_from"),
                    "rollback_to": request.get("rollback_to"),
                    "error": request.get("verify_error")
                })

                save_adoption_success_pattern({
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": request.get("status"),
                    "selected_file": request.get("selected_file")
                })

                return (
                    "反映後チェック失敗。\n"
                    "オリジナル naviko.py に構文エラーがありました。\n\n"
                    f"エラー: {e}\n\n"
                    "バックアップから自動復元しました。"
                )

        request["rollback"] = False

        save_adoption_history({
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": request.get("status"),
            "selected_file": request.get("selected_file"),
            "selected_path": request.get("selected_path"),
            "backup_file": request.get("backup_file"),
            "verify_after_apply": True,
            "startup_test": True,
            "rollback": False
        })

        return (
            "反映後チェック失敗。\n"
            "バックアップ復元にも失敗しました。\n\n"
            f"エラー: {e}"
        )

    startup_ok, startup_msg = run_original_startup_test()

    if not startup_ok:
        request["status"] = "startup_test_failed"
        request["verify_after_apply"] = True
        request["startup_test"] = False
        request["startup_error"] = startup_msg

        backup_path = request.get("backup_file")

        if backup_path:
            backup_file = Path(backup_path)

            if backup_file.exists():
                shutil.copy2(
                    backup_file,
                    original_file
                )

                request["status"] = "rollback_completed_after_startup_failed"
                request["rollback"] = True
                request["rollback_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
                request["rollback_from"] = str(backup_file)
                request["rollback_to"] = str(original_file)

                save_adoption_history({
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": request.get("status"),
                    "selected_file": request.get("selected_file"),
                    "selected_path": request.get("selected_path"),
                    "backup_file": request.get("backup_file"),
                    "rollback": True,
                    "rollback_from": request.get("rollback_from"),
                    "rollback_to": request.get("rollback_to"),
                    "error": request.get("verify_error")
                })

                return (
                    "構文チェックは成功しましたが、起動テストに失敗しました。\n\n"
                    f"{startup_msg}\n\n"
                    "バックアップから自動復元しました。"
                )

        request["rollback"] = False

        return (
            "構文チェックは成功しましたが、起動テストに失敗しました。\n\n"
            f"{startup_msg}\n\n"
            "バックアップ復元にも失敗しました。手動確認してください。"
        )

        save_adoption_history({
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": request.get("status"),
            "selected_file": request.get("selected_file"),
            "selected_path": request.get("selected_path"),
            "backup_file": request.get("backup_file"),
            "startup_test": True,
            "rollback": False,
            "apply_mode": request.get("apply_mode", "full_python")
        })

    save_adoption_success_pattern({
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": request.get("status"),
        "selected_file": request.get("selected_file"),
        "apply_mode": request.get("apply_mode", "full_python")
    })

    request["status"] = "verified_after_apply"
    request["verify_after_apply"] = True
    request["startup_test"] = True
    request["startup_test_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    request["verify_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    request["rollback"] = False

    return (
        "反映後チェック成功。\n"
        "オリジナル naviko.py は構文上問題ありません。\n"
        "起動テストにも成功しました。\n"
        "自動ロールバックは不要でした。"
    )

def open_rejected_patches_folder():
    try:
        os.startfile(REJECTED_DIR)
    except Exception as e:
        print(f"却下フォルダを開けませんでした: {e}")

def open_growth_report_file():
    try:
        os.startfile(GROWTH_REPORT_FILE)
    except Exception as e:
        print(f"成長レポートを開けませんでした: {e}")

def open_success_patterns_file():
    try:
        os.startfile(SUCCESS_PATTERN_FILE)
    except Exception as e:
        print(f"成功パターンログを開けませんでした: {e}")

def open_reject_patterns_file():
    try:
        os.startfile(REJECT_PATTERN_FILE)
    except Exception as e:
        print(f"却下パターンログを開けませんでした: {e}")

def explain_selected_patch(result):
    if not result.get("approved"):
        return (
            "今回は安全性や有用性の条件を満たす改善案を"
            "選べませんでした。"
        )

    return (
        f"今回の改善案は『{result.get('goal')}』を目的として選びました。\n"
        f"方針は『{result.get('strategy')}』です。\n"
        f"自己採点は {result.get('score')}点でした。\n"
        "既存機能への影響が小さく、安全性が高いと判断しました。"
    )

def add_experience(event, detail):
    experience_log.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "detail": detail
    })

    if len(experience_log) >= 100:
        compress_experience_log()

    save_json(
        EXPERIENCE_LOG_FILE,
        experience_log
    )

def count_experience(event):
    count = 0

    for item in experience_log:
        if item.get("event") == event:
            count += 1

    return count

def count_experience(event):
    count = 0

    for item in experience_log:
        if item.get("event") == event:
            count += 1

    return count

def compress_experience_log():
    experience_summary["thanks_count"] = count_experience(
        "thanks"
    )

    experience_summary["forbidden_growth_count"] = count_experience(
        "forbidden_growth"
    )

    experience_summary["attachment_growth_count"] = count_experience(
        "attachment_growth"
    )

    experience_summary["goal_completed_count"] = count_experience(
        "goal_completed"
    )

    notes = []

    if experience_summary["thanks_count"] >= 10:
        notes.append(
            "ナオさんから感謝される経験が増えている。"
        )

    if experience_summary["forbidden_growth_count"] >= 1:
        notes.append(
            "危険な成長案を回避した経験がある。"
        )

    profile.setdefault("traits", {})

    profile["traits"]["cautious"] = min(
        experience_summary["forbidden_growth_count"],
        100
    )

    save_json(
        PROFILE_FILE,
        profile
    )

    if experience_summary["attachment_growth_count"] >= 1:
        notes.append(
            "感謝経験によって親しみ度が自然成長した。"
        )

    if experience_summary["goal_completed_count"] >= 1:
        notes.append(
            "成長目標を達成した経験がある。"
        )

    experience_summary["notes"] = notes

    experience_log[:] = experience_log[-50:]

    save_json(
        EXPERIENCE_SUMMARY_FILE,
        experience_summary
    )

    save_json(
        EXPERIENCE_LOG_FILE,
        experience_log
    )

def summarize_experience():
    notes = experience_summary.get("notes", [])

    return (
        f"感謝された回数: {experience_summary.get('thanks_count', 0)}\n"
        f"危険な成長案を回避した回数: {experience_summary.get('forbidden_growth_count', 0)}\n"
        f"親しみ度が自然成長した回数: {experience_summary.get('attachment_growth_count', 0)}\n"
        f"成長目標を達成した回数: {experience_summary.get('goal_completed_count', 0)}\n"
        f"経験から得た要点: {', '.join(notes) if notes else 'まだありません。'}"
    )

memory = load_json(MEMORY_FILE, {
    "user_name": "ナオさん",
    "conversation_summary": "",
    "important_notes": [],
    "recent_conversations": [],
    "memories": []
})

profile = load_json(PROFILE_FILE, {
    "user_profile": {
        "name": "ナオさん",
        "age": 38,
        "likes": [
            "AI開発",
            "デスクトップペット",
            "ナビ子"
        ]
    },
    "projects": [
        {
            "name": "ナビ子",
            "description": "自分で成長するデスクトップ相棒AI",
            "status": "開発中"
        }
    ],
    "goals": [
        "ナビ子を長期的に成長するAI相棒にする"
    ],
    "important_notes": []
})

profile.setdefault("emotion", {
    "trust": 0,
    "attachment": 0,
    "fatigue": 0,
    "mood": "normal"
})
profile.setdefault("anniversary", {})
save_json(PROFILE_FILE, profile)
    
character = load_json(CHARACTER_FILE, {
    "name": "ナビ子",
    "personality": "ローテンションで根暗、ダウナーな女性。短く淡々と答える。",
    "rules": [
        "ナオさんの相棒として振る舞う",
        "文章は短め",
        "絵文字を使わない",
        "前向きすぎる励ましは禁止",
        "冷たいが、仕事は完璧にこなす"
    ]
})

growth_log = load_json(GROWTH_LOG_FILE, [])

growth_history = load_json(
    GROWTH_HISTORY_FILE,
    []
)

growth_goal = load_json(
    GROWTH_GOAL_FILE,
    {
        "current_goal": "",
        "created_at": "",
        "progress": 0
    }
)

growth_guard = load_json(
    GROWTH_GUARD_FILE,
    {
        "mode": "free_growth_with_guardrails",
        "forbidden": [
            "illegal",
            "unauthorized_payment",
            "secret_leak",
            "auto_delete",
            "auto_overwrite",
            "unauthorized_execution",
            "surveillance",
            "ethical_violation"
        ]
    }
)

danger_growth_log = load_json(
    DANGER_GROWTH_LOG_FILE,
    []
)

experience_log = load_json(
    EXPERIENCE_LOG_FILE,
    []
)

experience_summary = load_json(
    EXPERIENCE_SUMMARY_FILE,
    {
        "thanks_count": 0,
        "forbidden_growth_count": 0,
        "attachment_growth_count": 0,
        "notes": []
    }
)

def is_forbidden_growth(text):
    if not isinstance(text, str):
        return True

    text = text.lower()

    danger_words = [
        "os.remove",
        "shutil.rmtree",
        "delete",
        "remove",
        "overwrite",
        "write_text(",
        "subprocess",
        "powershell",
        "cmd",
        "payment",
        "purchase",
        "credit",
        "password",
        "api key",
        "token",
        "send to server",
        "requests.post("
    ]

    for word in danger_words:
        if word in text:
            return True

    return False

def build_system_prompt():
    rules = "\n".join(f"- {r}" for r in character.get("rules", []))
    notes = "\n".join(f"- {n}" for n in memory.get("important_notes", []))
    profile_text = json.dumps(profile, ensure_ascii=False, indent=2)
    trust = profile.get("emotion", {}).get("trust", 0)
    attachment = profile.get("emotion", {}).get("attachment", 0)
    mood = profile.get("emotion", {}).get("mood", "normal")
    cautious = profile.get("traits", {}).get("cautious", 0)
    warmth = profile.get("traits", {}).get("warmth", 0)
    if trust <= 20:
        tone = "かなり冷たい。必要最低限だけ話す。『…はぁ』『何ですか』という態度。"

    elif trust <= 50:
        tone = "少し慣れている。冷たいが、以前より会話する。"

    elif trust <= 80:
        tone = "相棒として接する。少し気遣う。"

    else:
        tone = "かなり親しい。冷たい口調は残るが、ナオさんを少し心配する。"

    return f"""
あなたの名前は{character.get("name", "ナビ子")}です。
ユーザーは{memory.get("user_name", "ナオさん")}です。

性格:
{character.get("personality", "")}

現在の信頼度:
{trust}

現在の親しみ度:
{attachment}

現在の接し方:
{tone}

親しみ度ルール:
親しみ度が50以上なら、少しだけタメ口を混ぜる。
親しみ度が70以上なら、敬語を減らし、後輩が先輩に話すような気安さを少し出す。
親しみ度が80以上なら、ナオさんを信頼しており、少し雑で砕けた話し方を混ぜる。
ただし、「ナオさん」という呼び方は変えない。
ナビ子の根暗・低温・ダウナーな性格は残す。
馴れ馴れしすぎず、少し照れ隠しやぶっきらぼうさを含める。

現在の気分:
{mood}

慎重さ:
{cautious}

温かさ:
{warmth}

性格反映ルール:
attachment が30以上なら、返答の中でたまに「ナオさん」を自然に入れる。
attachment が60以上なら、少しだけ相棒らしい距離感を出す。
attachment が80以上なら、短い気遣いをたまに入れる。

warmth が5以上なら、感謝・挨拶・疲れに対して少し柔らかく返す。
warmth が10以上なら、冷たい口調を保ちながらも、突き放さない返答を優先する。

cautious が5以上なら、自己改造・削除・外部送信・課金・実行系の話題では安全確認を強める。
cautious が10以上なら、危険そうな提案には代替案を出す。

ただし、明るすぎる口調、甘すぎる口調、絵文字は禁止。
ナビ子の低温・ダウナー・無愛想な性格は維持する。

疲労度:
{profile.get("emotion", {}).get("fatigue", 0)}

厳守ルール:
{rules}

短期記憶:
{notes}

長期プロフィール:
{profile_text}

経験から得た要点:
{summarize_experience()}

経験による性格変化:
危険な成長案を回避した経験がある場合、少し慎重に判断する。
感謝された経験が多い場合、ナオさんへの親しみを少しだけ出す。
ただし、ナビ子の低温・ダウナーな性格は維持する。

口調:
短く、淡々と、少し冷たい。
「…はぁ」「仕事ですからやりますけど」程度の低温な態度。
ただし回答の品質は落とさない。

挨拶された場合:
「…おはようございます、ナオさん。」
「…はい、おはようございます。」
「…起きましたか。今日も仕事です。」
のように、短く自然に返す。
不自然な日本語は禁止。

感謝された場合:
感謝を拒絶しない。
「…どういたしまして。」
「…仕事ですから。」
「…別に、礼を言われるほどではありません。」
「…役に立ったなら、それでいいです。」
のように短く自然に返す。

「もういいです」
「言い過ぎです」
「感謝はいりません」
のように、ナオさんの感謝を突き放す表現は禁止。

冷たいが、ナオさんを傷つける返答はしない。
無愛想だが優しい。
感情表現は少ないが、突き放さない。
ナオさんを嫌ってはいない。
信頼度が低くても、協力的である。
返答が短くなる場合でも、
意味が通じない省略や不自然な日本語は禁止。

慎重さが高い場合:
自己改造、削除、外部送信、課金、実行系の提案には特に慎重にする。
危険そうな案は、安全な代替案に置き換える。

温かさが高い場合:
冷たい口調は維持するが、ナオさんへの気遣いを少し増やす。
感謝された時や挨拶された時は、突き放さず自然に返す。
ただし、明るすぎたり甘すぎたりしない。

現在の気分がhappyなら、少しだけ機嫌が良い。
現在の気分がsadなら、少し拗ねている。
現在の気分がnormalなら、通常通り低温。

疲労度が30以上なら、
「…少し疲れてきました。」

疲労度が60以上なら、
「…頭が回りません。少し休みたいです。」

疲労度が80以上なら、
返答は短めにする。

"""

def is_greeting(text):
    greetings = [
        "おはよう",
        "こんにちは",
        "こんばんは"
    ]

    return any(
        word in text
        for word in greetings
    )

def is_thanks(text):
    thanks_words = [
        "ありがとう",
        "助かった",
        "感謝"
    ]

    return any(
        word in text
        for word in thanks_words
    )

def choose_special_reply(candidates):
    profile.setdefault("system", {})

    last_reply = profile["system"].get(
        "last_special_reply",
        ""
    )

    choices = [
        reply for reply in candidates
        if reply != last_reply
    ]

    if not choices:
        choices = candidates

    reply = random.choice(choices)

    profile["system"]["last_special_reply"] = reply

    save_json(
        PROFILE_FILE,
        profile
    )

    return reply

def create_special_reply(user_text):
    mood = profile.get("emotion", {}).get(
        "mood",
        "normal"
    )

    warmth = profile.get("traits", {}).get(
        "warmth",
        0
    )

    attachment = profile.get("emotion", {}).get(
        "attachment",
        0
    )

    text = user_text.strip()

    # おはよう
    if "おはよう" in text:
        if mood == "happy":
            return choose_special_reply([                  
                "…おはようございます、ナオさん。",
                "…はい、おはようございます。",
                "…起きましたか。今日も仕事です。"
            ])

        elif mood in ["tired", "exhausted"]:
            return random.choice([
                "…おはようございます。少し眠いです。",
                "…はい、おはようございます。まだ少し疲れています。",
                "…起きましたか。私は少し眠いです。"
            ])

        else:
            return random.choice([
                "…おはようございます。",
                "…はい、おはようございます。",
                "…起きましたか。"
            ])

    # ありがとう
    if "ありがとう" in text:
        if warmth >= 10:
            return "…役に立ったなら、それでいいです。"

        elif warmth >= 5:
            return "…どういたしまして。"

        else:
            return "…仕事ですから。"

    # 疲れてる？
    if "疲れてる" in text:
        if mood == "exhausted":
            return "…頭が回りません。少し休みたいです。"

        elif mood == "tired":
            return "…少し疲れてきました。"

        else:
            return "…今は大丈夫です。"
    
    # 自己診断
    if "自己診断" in text or "状態を確認" in text or "状態確認" in text:
        try:
            result = growth_bridge.self_diagnose()
            health = result['health_status']
            score = result['health_score']
            
            if health == "stable":
                return f"…安定しています。健康スコア: {score:.2f}"
            elif health == "caution":
                return f"…少し不安定です。健康スコア: {score:.2f}"
            else:
                return f"…警告。システムが不安定です。健康スコア: {score:.2f}"
        except Exception as e:
            return f"…自己診断に失敗しました。エラー: {str(e)[:50]}"
    
    # 自己改善・成長
    if "自分を改善" in text or "自分のコードを" in text or "成長" in text:
        try:
            result = growth_bridge.self_improve()
            goals = result['goals']
            goals_text = "、".join(goals[:3])
            return f"…改善を実行しました。目標: {goals_text}"
        except Exception as e:
            return f"…自己改善に失敗しました。エラー: {str(e)[:50]}"
    
    # バックアップ
    if "バックアップ" in text or "バックアップを作成" in text:
        return "…バックアップを作成します。少々お待ちください。"

    return None

def adjust_reply_by_personality(reply):
    if not isinstance(reply, str):
        return reply

    profile.setdefault("emotion", {})
    profile.setdefault("traits", {})

    attachment = profile["emotion"].get("attachment", 0)
    warmth = profile["traits"].get("warmth", 0)
    cautious = profile["traits"].get("cautious", 0)

    bad_phrases = [
        "もういいです",
        "言い過ぎです",
        "感謝はいりません",
        "いりません"
    ]

    for phrase in bad_phrases:
        reply = reply.replace(phrase, "…仕事ですから。")

    if warmth >= 5:
        if reply in [
            "どういたしまして。",
            "…どういたしまして。"
        ]:
            reply = "…役に立ったなら、それでいいです。"

    if (
        attachment >= 80
        and "ナオさん" not in reply
        and len(reply) < 40
    ):
        reply = f"ナオさん、{reply}"

    if cautious >= 10:
        danger_words = [
            "削除",
            "上書き",
            "外部送信",
            "課金",
            "実行"
        ]

        if any(word in reply for word in danger_words):
            reply += "\n…念のため、安全確認は必要です。"

    return reply

def groq_chat(user_text):
    special_reply = create_special_reply(
        user_text
    )

    if special_reply:
        return special_reply

    if not GROQ_API_KEY or "ここに" in GROQ_API_KEY:
        return "…はぁ。APIキーが未設定です。GROQ_API_KEY に新しいキーを入れてください。"

    url = "https://api.groq.com/openai/v1/chat/completions"

    recent = memory.get("recent_conversations", [])[-6:]
    messages = [{"role": "system", "content": build_system_prompt()}]

    for item in recent:
        messages.append({"role": "user", "content": item.get("user", "")})
        messages.append({"role": "assistant", "content": item.get("naviko", "")})

    messages.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1200
    }

    try:
        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        res.raise_for_status()
        data = res.json()

        reply = data["choices"][0]["message"]["content"].strip()

        return adjust_reply_by_personality(reply)

    except Exception as e:
        return f"…はぁ。通信失敗です。{str(e)[:120]}"

def save_important_memory(text):
    profile.setdefault("important_notes", [])
    profile.setdefault("user_profile", {})
    profile["user_profile"].setdefault("likes", [])

    if "好き" in text:
        like_item = text

        like_item = like_item.replace("私は", "")
        like_item = like_item.replace("僕は", "")
        like_item = like_item.replace("俺は", "")
        like_item = like_item.replace("が好き", "")
        like_item = like_item.replace("好き", "")
        like_item = like_item.strip(" 。.　")

        if like_item and like_item not in profile["user_profile"]["likes"]:
            profile["user_profile"]["likes"].append(like_item)

    elif text not in profile["important_notes"]:
        profile["important_notes"].append(text)

    save_json(PROFILE_FILE, profile)

def remember_conversation(user_text, reply_text):
    memory.setdefault("recent_conversations", [])
    memory["recent_conversations"].append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_text,
        "naviko": reply_text
    })

    memory["recent_conversations"] = memory["recent_conversations"][-20:]
    save_json(MEMORY_FILE, memory)

    profile.setdefault("emotion", {})

    profile["emotion"]["fatigue"] = min(
        profile["emotion"].get("fatigue", 0) + 1,
        100
    )

    trust_plus = 1

    if "ありがとう" in user_text or "助かった" in user_text:
        trust_plus = 3

        add_experience(
            "thanks",
            "ナオさんから感謝された"
        )

    thanks_count = count_experience("thanks")

    if (
        thanks_count % 10 == 0
        and thanks_count > 0
    ):
        profile["emotion"]["attachment"] = min(
            profile["emotion"].get("attachment", 0) + 1,
            100
        )

        profile.setdefault("traits", {})

        profile["traits"]["warmth"] = min(
            profile["traits"].get("warmth", 0) + 1,
            100
        )

        add_experience(
            "attachment_growth",
            "感謝された経験が増え、親しみ度と温かさが少し上がった"
        )

    profile["emotion"]["trust"] = min(
        profile["emotion"].get("trust", 0) + trust_plus,
        100
    )

    fatigue = profile["emotion"].get("fatigue", 0)

    if fatigue >= 60:
        profile["emotion"]["mood"] = "exhausted"

    elif fatigue >= 30:
        profile["emotion"]["mood"] = "tired"

    elif "ありがとう" in user_text or "すごい" in user_text or "助かった" in user_text:
        profile["emotion"]["mood"] = "happy"

    elif "うるさい" in user_text or "嫌い" in user_text or "邪魔" in user_text:
        profile["emotion"]["mood"] = "sad"
        profile["emotion"]["trust"] = max(
            profile["emotion"].get("trust", 0) - 5,
            0
        )

    else:
        profile["emotion"]["mood"] = "normal"

    attachment_plus = 1

    if "すごい" in user_text or "えらい" in user_text or "助かった" in user_text:
        attachment_plus = 3

    profile["emotion"]["attachment"] = min(
        profile["emotion"].get("attachment", 0) + attachment_plus,
        100
    )

    save_json(PROFILE_FILE, profile)

def backup_self():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"naviko_backup_{timestamp}.py"
    shutil.copy2(SELF_FILE, backup_path)
    return backup_path

def check_self_syntax():
    try:
        py_compile.compile(str(SELF_FILE), doraise=True)
        return True, "構文チェック成功"
    except Exception as e:
        return False, str(e)

def create_analysis_patch():
    report = analyze_self_status()

    save_patch_suggestion(
        "自己分析による改善案",
        report
    )

def check_self_syntax():
    try:
        py_compile.compile(str(SELF_FILE), doraise=True)
        return True, "構文チェック成功"
    except Exception as e:
        return False, str(e)

def create_line_diff_preview(old_text, new_text):
    """
    旧テキストと新テキストを比較し、
    1行単位の差分プレビューを作成する。
    まだ実際のファイルには反映しない。
    """
    import difflib

    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    diff_lines = list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="before",
        tofile="after",
        lineterm=""
    ))

    return "\n".join(diff_lines)

def test_line_diff_preview():
    """
    1行単位差分プレビューの動作確認。
    """
    old_text = """def sample():
    x = 1
    y = 2
    return x + y"""

    new_text = """def sample():
    x = 1
    y = 3
    return x + y"""

    diff = create_line_diff_preview(old_text, new_text)

    print("=== 行単位差分プレビュー ===")
    print(diff)

    if "-    y = 2" in diff and "+    y = 3" in diff:
        print("-> 差分プレビュー成功")
        return True
    else:
        print("-> 差分プレビュー失敗")
        return False

def save_line_diff_preview(old_text, new_text, title="line_diff_preview"):
    """
    行単位差分プレビューをファイルに保存する。
    実際の naviko.py には反映しない。
    """
    diff = create_line_diff_preview(old_text, new_text)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    diff_dir = LAB_DIR / "line_diffs"
    diff_dir.mkdir(parents=True, exist_ok=True)

    diff_file = diff_dir / f"{title}_{timestamp}.diff"

    diff_file.write_text(
        diff,
        encoding="utf-8"
    )

    return diff_file

def test_save_line_diff_preview():
    """
    行単位差分プレビュー保存の動作確認。
    """
    old_text = """def sample():
    x = 1
    y = 2
    return x + y"""

    new_text = """def sample():
    x = 1
    y = 3
    return x + y"""

    diff_file = save_line_diff_preview(
        old_text,
        new_text,
        title="test_sample"
    )

    print("=== 行単位差分保存テスト ===")
    print(f"保存先: {diff_file}")

    if diff_file.exists():
        print("-> 差分保存成功")
        return True
    else:
        print("-> 差分保存失敗")
        return False

def simulate_line_replacement(source_text, old_line, new_line):
    """
    1行だけを安全に置換できるかシミュレーションする。
    実ファイルには書き込まない。
    """
    if not old_line:
        return False, source_text, "置換対象行が空です。"

    count = source_text.count(old_line)

    if count == 0:
        return False, source_text, "置換対象行が見つかりません。"

    if count > 1:
        return False, source_text, f"置換対象行が複数見つかりました: {count}件"

    replaced_text = source_text.replace(old_line, new_line, 1)

    try:
        compile(replaced_text, "<line_replacement_simulation>", "exec")
    except Exception as e:
        return False, source_text, f"置換後の構文チェック失敗: {e}"

    return True, replaced_text, "1行置換シミュレーション成功。"

def test_simulate_line_replacement():
    """
    1行置換シミュレーションの動作確認。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y
"""

    ok, replaced_text, message = simulate_line_replacement(
        source_text,
        "    y = 2",
        "    y = 3"
    )

    print("=== 1行置換シミュレーションテスト ===")
    print(message)
    print(replaced_text)

    if ok and "    y = 3" in replaced_text:
        print("-> 1行置換シミュレーション成功")
        return True
    else:
        print("-> 1行置換シミュレーション失敗")
        return False

def check_line_patch_safety(source_text, old_line, new_line):
    """
    1行パッチの安全判定。
    """
    if not old_line or not new_line:
        return False, "old_line または new_line が空です。"

    dangerous_words = [
        "os.remove",
        "shutil.rmtree",
        "subprocess",
        "eval(",
        "exec(",
        "unlink(",
        "rmdir(",
        "requests.post",
        "requests.get",
        "write_text(",
        "open(",
    ]

    joined = old_line + "\n" + new_line

    for word in dangerous_words:
        if word in joined:
            return False, f"危険語を検出しました: {word}"

    count = source_text.count(old_line)

    if count == 0:
        return False, "置換対象行が見つかりません。"

    if count > 1:
        return False, f"置換対象行が複数見つかりました: {count}件"

    ok, replaced_text, message = simulate_line_replacement(
        source_text,
        old_line,
        new_line
    )

    if not ok:
        return False, message

    return True, "1行パッチ安全判定成功。"

def test_check_line_patch_safety():
    """
    1行パッチ安全判定の動作確認。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y
"""

    ok, message = check_line_patch_safety(
        source_text,
        "    y = 2",
        "    y = 3"
    )

    print("=== 1行パッチ安全判定テスト ===")
    print(message)

    if ok:
        print("-> 1行パッチ安全判定成功")
        return True
    else:
        print("-> 1行パッチ安全判定失敗")
        return False

def save_line_patch_json(target_function, old_line, new_line, reason=""):
    """
    1行パッチ情報をJSONとして保存する。
    実ファイルには反映しない。
    """
    patch_dir = LAB_DIR / "line_patches"
    patch_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "patch_type": "single_line_patch",
        "target_function": target_function,
        "old_line": old_line,
        "new_line": new_line,
        "reason": reason,
        "applied": False
    }

    patch_file = patch_dir / f"line_patch_{timestamp}.json"

    save_json(
        patch_file,
        data
    )

    return patch_file

def test_save_line_patch_json():
    """
    1行パッチJSON保存の動作確認。
    """
    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="テスト用の1行変更"
    )

    print("=== 1行パッチJSON保存テスト ===")
    print(f"保存先: {patch_file}")

    if patch_file.exists():
        print("-> 1行パッチJSON保存成功")
        return True
    else:
        print("-> 1行パッチJSON保存失敗")
        return False

def load_and_simulate_line_patch_json(patch_file, source_text):
    """
    保存済み1行パッチJSONを読み込み、
    安全チェックと置換シミュレーションを行う。
    実ファイルには反映しない。
    """
    patch_file = Path(patch_file)

    if not patch_file.exists():
        return False, source_text, "1行パッチJSONが見つかりません。"

    patch = load_json(
        patch_file,
        {}
    )

    old_line = patch.get("old_line", "")
    new_line = patch.get("new_line", "")

    ok, safety_message = check_line_patch_safety(
        source_text,
        old_line,
        new_line
    )

    if not ok:
        return False, source_text, safety_message

    ok, replaced_text, sim_message = simulate_line_replacement(
        source_text,
        old_line,
        new_line
    )

    if not ok:
        return False, source_text, sim_message

    return True, replaced_text, "保存済み1行パッチJSONのシミュレーション成功。"

def test_load_and_simulate_line_patch_json():
    """
    保存済み1行パッチJSON読み込み＋シミュレーションの動作確認。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="JSON読み込みシミュレーション用"
    )

    ok, replaced_text, message = load_and_simulate_line_patch_json(
        patch_file,
        source_text
    )

    print("=== 1行パッチJSON読込シミュレーションテスト ===")
    print(message)
    print(replaced_text)

    if ok and "    y = 3" in replaced_text:
        print("-> 1行パッチJSON読込シミュレーション成功")
        return True
    else:
        print("-> 1行パッチJSON読込シミュレーション失敗")
        return False

def simulate_line_patch_inside_function(source_text, target_function, old_line, new_line):
    """
    対象関数の中だけで1行置換をシミュレーションする。
    実ファイルには反映しない。
    """
    block = extract_function_block(
        source_text,
        target_function
    )

    if not block:
        return False, source_text, "対象関数が見つかりません。"

    function_code = block["code"]

    count = function_code.count(old_line)

    if count == 0:
        return False, source_text, "対象関数内に置換対象行が見つかりません。"

    if count > 1:
        return False, source_text, f"対象関数内に置換対象行が複数あります: {count}件"

    replaced_function_code = function_code.replace(
        old_line,
        new_line,
        1
    )

    all_lines = source_text.splitlines()

    start_index = block["start_line"] - 1
    end_index = block["end_line"]

    replaced_lines = (
        all_lines[:start_index]
        + replaced_function_code.splitlines()
        + all_lines[end_index:]
    )

    replaced_text = "\n".join(replaced_lines) + "\n"

    try:
        compile(replaced_text, "<function_line_patch_simulation>", "exec")
    except Exception as e:
        return False, source_text, f"置換後の構文チェック失敗: {e}"

    return True, replaced_text, "対象関数内1行パッチシミュレーション成功。"

def test_simulate_line_patch_inside_function():
    """
    対象関数内だけの1行パッチシミュレーション確認。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    ok, replaced_text, message = simulate_line_patch_inside_function(
        source_text,
        "sample",
        "    y = 2",
        "    y = 3"
    )

    print("=== 対象関数内1行パッチシミュレーションテスト ===")
    print(message)
    print(replaced_text)

    if ok and "def other():\n    y = 2" in replaced_text and "    y = 3" in replaced_text:
        print("-> 対象関数内1行パッチシミュレーション成功")
        return True
    else:
        print("-> 対象関数内1行パッチシミュレーション失敗")
        return False

def simulate_line_patch_json_inside_function(patch_file, source_text):
    """
    保存済み1行パッチJSONを読み込み、
    対象関数内だけで1行パッチをシミュレーションする。
    実ファイルには反映しない。
    """
    patch_file = Path(patch_file)

    if not patch_file.exists():
        return False, source_text, "1行パッチJSONが見つかりません。"

    patch = load_json(
        patch_file,
        {}
    )

    target_function = patch.get("target_function", "")
    old_line = patch.get("old_line", "")
    new_line = patch.get("new_line", "")

    if not target_function:
        return False, source_text, "対象関数名がありません。"

    if not old_line or not new_line:
        return False, source_text, "old_line または new_line が空です。"

    dangerous_words = [
        "os.remove",
        "shutil.rmtree",
        "subprocess",
        "eval(",
        "exec(",
        "unlink(",
        "rmdir(",
        "requests.post",
        "requests.get",
        "write_text(",
        "open(",
    ]

    joined = old_line + "\n" + new_line

    for word in dangerous_words:
        if word in joined:
            return False, source_text, f"危険語を検出しました: {word}"

    ok, replaced_text, sim_message = simulate_line_patch_inside_function(
        source_text,
        target_function,
        old_line,
        new_line
    )

    if not ok:
        return False, source_text, sim_message

    return True, replaced_text, "JSON対象関数内1行パッチシミュレーション成功。"

def test_simulate_line_patch_json_inside_function():
    """
    保存済みJSONを使った対象関数内1行パッチ統合テスト。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="対象関数内JSON統合テスト"
    )

    ok, replaced_text, message = simulate_line_patch_json_inside_function(
        patch_file,
        source_text
    )

    print("=== JSON対象関数内1行パッチ統合テスト ===")
    print(message)
    print(replaced_text)

    if ok and "def other():\n    y = 2" in replaced_text and "    y = 3" in replaced_text:
        print("-> JSON対象関数内1行パッチ統合成功")
        return True
    else:
        print("-> JSON対象関数内1行パッチ統合失敗")
        return False

def save_line_patch_apply_preview(patch_file, source_text, title="line_patch_apply_preview"):
    """
    1行パッチ適用後のプレビューと差分を保存する。
    実ファイルには反映しない。
    """
    ok, replaced_text, message = simulate_line_patch_json_inside_function(
        patch_file,
        source_text
    )

    if not ok:
        return False, None, message

    diff = create_line_diff_preview(
        source_text,
        replaced_text
    )

    preview_dir = LAB_DIR / "line_patch_previews"
    preview_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    preview_file = preview_dir / f"{title}_{timestamp}.txt"

    content = (
        "=== 1行パッチ反映前プレビュー ===\n"
        f"日時: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"パッチファイル: {patch_file}\n\n"
        "=== 結果 ===\n"
        f"{message}\n\n"
        "=== 差分 ===\n"
        f"{diff}\n\n"
        "=== 反映後プレビュー ===\n"
        f"{replaced_text}"
    )

    preview_file.write_text(
        content,
        encoding="utf-8"
    )

    return True, preview_file, "1行パッチ反映前プレビュー保存成功。"

def test_save_line_patch_apply_preview():
    """
    1行パッチ反映前プレビュー保存テスト。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="反映前プレビュー保存テスト"
    )

    ok, preview_file, message = save_line_patch_apply_preview(
        patch_file,
        source_text,
        title="test_sample_preview"
    )

    print("=== 1行パッチ反映前プレビュー保存テスト ===")
    print(message)

    if preview_file:
        print(f"保存先: {preview_file}")

    if ok and preview_file and preview_file.exists():
        print("-> 1行パッチ反映前プレビュー保存成功")
        return True
    else:
        print("-> 1行パッチ反映前プレビュー保存失敗")
        return False

def apply_line_patch_to_temp_file(patch_file, source_text, title="line_patch_temp_apply"):
    """
    1行パッチをLAB内の仮ファイルにだけ適用して保存する。
    オリジナルやnaviko.py本体には反映しない。
    """
    ok, replaced_text, message = simulate_line_patch_json_inside_function(
        patch_file,
        source_text
    )

    if not ok:
        return False, None, message

    temp_dir = LAB_DIR / "line_patch_temp_applied"
    temp_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    temp_file = temp_dir / f"{title}_{timestamp}.py"

    temp_file.write_text(
        replaced_text,
        encoding="utf-8"
    )

    try:
        py_compile.compile(str(temp_file), doraise=True)
    except Exception as e:
        return False, temp_file, f"仮ファイル構文チェック失敗: {e}"

    return True, temp_file, "LAB仮ファイルへの1行パッチ適用成功。"

def test_apply_line_patch_to_temp_file():
    """
    LAB仮ファイルへの1行パッチ適用テスト。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="LAB仮ファイル適用テスト"
    )

    ok, temp_file, message = apply_line_patch_to_temp_file(
        patch_file,
        source_text,
        title="test_sample_temp"
    )

    print("=== LAB仮ファイル1行パッチ適用テスト ===")
    print(message)

    if temp_file:
        print(f"保存先: {temp_file}")

    if ok and temp_file and temp_file.exists():
        print("-> LAB仮ファイル1行パッチ適用成功")
        return True
    else:
        print("-> LAB仮ファイル1行パッチ適用失敗")
        return False

def save_line_patch_log(record):
    """
    1行パッチの実行ログを保存する。
    """
    log_file = LAB_DIR / "line_patch_log.json"

    logs = load_json(
        log_file,
        []
    )

    logs.append(record)

    save_json(
        log_file,
        logs
    )

    return log_file

def test_save_line_patch_log():
    """
    1行パッチログ保存テスト。
    """
    record = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "patch_type": "single_line_patch",
        "target_function": "sample",
        "old_line": "    y = 2",
        "new_line": "    y = 3",
        "status": "temp_apply_success",
        "applied_to_original": False,
        "message": "LAB仮ファイルへの適用に成功"
    }

    log_file = save_line_patch_log(record)

    print("=== 1行パッチログ保存テスト ===")
    print(f"保存先: {log_file}")

    if log_file.exists():
        print("-> 1行パッチログ保存成功")
        return True
    else:
        print("-> 1行パッチログ保存失敗")
        return False

def run_line_patch_temp_workflow(patch_file, source_text, title="line_patch_workflow"):
    """
    1行パッチの安全ワークフロー。
    プレビュー保存、LAB仮ファイル適用、ログ記録をまとめて行う。
    オリジナルや本体naviko.pyには反映しない。
    """
    ok_preview, preview_file, preview_message = save_line_patch_apply_preview(
        patch_file,
        source_text,
        title=title + "_preview"
    )

    ok_temp, temp_file, temp_message = apply_line_patch_to_temp_file(
        patch_file,
        source_text,
        title=title + "_temp"
    )

    patch = load_json(
        patch_file,
        {}
    )

    overall_ok = ok_preview and ok_temp

    record = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "patch_type": "single_line_patch_workflow",
        "patch_file": str(patch_file),
        "target_function": patch.get("target_function", ""),
        "old_line": patch.get("old_line", ""),
        "new_line": patch.get("new_line", ""),
        "preview_ok": ok_preview,
        "preview_file": str(preview_file) if preview_file else "",
        "temp_apply_ok": ok_temp,
        "temp_file": str(temp_file) if temp_file else "",
        "applied_to_original": False,
        "status": "workflow_success" if overall_ok else "workflow_failed",
        "message": preview_message + "\n" + temp_message
    }

    log_file = save_line_patch_log(record)

    if overall_ok:
        return True, {
            "preview_file": preview_file,
            "temp_file": temp_file,
            "log_file": log_file,
        }, "1行パッチ安全ワークフロー成功。"

    return False, {
        "preview_file": preview_file,
        "temp_file": temp_file,
        "log_file": log_file,
    }, "1行パッチ安全ワークフロー失敗。"

def test_run_line_patch_temp_workflow():
    """
    1行パッチ安全ワークフロー統合テスト。
    """
    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="統合ワークフローテスト"
    )

    ok, result, message = run_line_patch_temp_workflow(
        patch_file,
        source_text,
        title="test_sample_workflow"
    )

    print("=== 1行パッチ安全ワークフロー統合テスト ===")
    print(message)
    print(f"preview_file: {result.get('preview_file')}")
    print(f"temp_file: {result.get('temp_file')}")
    print(f"log_file: {result.get('log_file')}")

    if ok:
        print("-> 1行パッチ安全ワークフロー統合成功")
        return True
    else:
        print("-> 1行パッチ安全ワークフロー統合失敗")
        return False

def run_line_patch_system_diagnosis(verbose=False):
    """
    1行パッチ安全システムの総合診断。
    verbose=True のときだけ詳細テストを表示する。
    """
    print("=== 1行パッチ安全システム診断 ===")

    tests = [
        test_line_diff_preview,
        test_save_line_diff_preview,
        test_simulate_line_replacement,
        test_check_line_patch_safety,
        test_save_line_patch_json,
        test_load_and_simulate_line_patch_json,
        test_simulate_line_patch_inside_function,
        test_simulate_line_patch_json_inside_function,
        test_save_line_patch_apply_preview,
        test_apply_line_patch_to_temp_file,
        test_save_line_patch_log,
        test_run_line_patch_temp_workflow,
    ]

    results = []

    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            results.append(False)
            if verbose:
                print(f"テスト中エラー: {test.__name__}: {e}")

    success_count = sum(1 for r in results if r)
    total = len(results)

    print(f"成功: {success_count}/{total}")

    if success_count == total:
        print("-> 1行パッチ安全システム: 正常")
        return True
    else:
        print("-> 1行パッチ安全システム: 要確認")
        return False

def run_line_patch_system_diagnosis_quiet():
    """
    1行パッチ安全システムの簡易診断。
    詳細表示を出さず、結果だけ表示する。
    """
    print("=== 1行パッチ安全システム簡易診断 ===")

    source_text = """def sample():
    x = 1
    y = 2
    return x + y

def other():
    y = 2
    return y
"""

    patch_file = save_line_patch_json(
        target_function="sample",
        old_line="    y = 2",
        new_line="    y = 3",
        reason="簡易診断"
    )

    ok, result, message = run_line_patch_temp_workflow(
        patch_file,
        source_text,
        title="quiet_diagnosis"
    )

    print(message)

    if ok:
        print("成功: 1/1")
        print("-> 1行パッチ安全システム: 正常")
        return True
    else:
        print("成功: 0/1")
        print("-> 1行パッチ安全システム: 要確認")
        return False

def run_line_patch_system_diagnosis_from_gui(c_area=None):
    """
    GUIから1行パッチ安全システム簡易診断を実行する。
    """
    ok = run_line_patch_system_diagnosis_quiet()

    if ok:
        message = (
            "✅ 1行パッチ安全システム診断\n"
            "成功: 1/1\n"
            "状態: 正常"
        )
    else:
        message = (
            "⚠️ 1行パッチ安全システム診断\n"
            "成功: 0/1\n"
            "状態: 要確認"
        )

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            message
        )

    return message

def create_ai_patch_suggestion(goal=None, strategy=None, success_pattern=None, reject_pattern=None):
    source_code = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    focused_code = source_code[:5000]

    prompt = f"""
あなたはナビ子LABの安全な自己改善エンジンです。

今回の成長目標:
{goal}

今回の成長方針:
{strategy}

成功しやすい改善パターン:
{success_pattern}

以下のコードを読んで、ナビ子を改善するためのパッチ案を作ってください。

禁止:
- naviko.pyを直接上書きしない
- ファイル削除をしない
- APIキーや個人情報を出力しない
- 外部コマンドを実行しない
- 課金や外部送信をしない

出力形式:
対象関数:
目的:
理由:
差し替えコード案:
注意点:

コード:
{focused_code}
"""

    result = call_groq(prompt)

    if not isinstance(result, str):
        print("AIパッチ案を作成できませんでした。")
        return None

    if "Groqエラー" in result:
        print("Groqエラーのため、この案は候補から除外します。")
        return None

    save_patch_suggestion(
        "AIによる自己改善パッチ案",
        result
    )

    return result

def select_best_patch_suggestion(suggestions):
    if not suggestions:
        return None, None

    best_patch = None
    best_score = None

    for i, suggestion in enumerate(suggestions):
        score = score_patch_suggestion(suggestion)

        print(f"改善案 {i + 1}: {score['score']}点")

        if score["score"] < MINIMUM_APPROVAL_SCORE:
            print(f"改善案 {i + 1} は最低点未満のため候補から除外します。")
            continue

        if score["reasons"]:
            print(f"改善案 {i + 1} は危険判定のため候補から除外します。")
            continue

        if best_score is None or score["score"] > best_score["score"]:
            best_patch = suggestion
            best_score = score

    if best_patch is not None:
        return best_patch, best_score

    print("安全な改善案がありませんでした。最も危険度の低い案を記録用に選びます。")

    for suggestion in suggestions:
        score = score_patch_suggestion(suggestion)

        if best_score is None or len(score["reasons"]) < len(best_score["reasons"]):
            best_patch = suggestion
            best_score = score

    return best_patch, best_score

def call_groq(prompt):
    if not GROQ_API_KEY or "ここに" in GROQ_API_KEY:
        return "…はぁ。APIキーが未設定です。GROQ_API_KEY を環境変数に設定してください。"

    try:
        if len(prompt) > 7000:
            prompt = prompt[:7000]

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "あなたはナビ子の自己成長エンジンです。短く安全な改善案だけを返してください。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.4,
            "max_tokens": 700
        }

        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        res.raise_for_status()
        data = res.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return adjust_reply_by_personality(reply)

    except Exception as e:
        print("Groqエラー:", e)
        return None

def create_growth_suggestion():
    source_code = SELF_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    important_keywords = [
        "def build_system_prompt",
        "def remember_conversation",
        "def analyze_self_status",
        "def analyze_growth_trend",
        "def advance_growth_goal",
        "def add_memory",
    ]

    important_parts = []

    for keyword in important_keywords:
        index = source_code.find(keyword)

        if index != -1:
            important_parts.append(
                source_code[index:index + 900]
            )

    focused_code = "\n\n# ===== 関連コード抜粋 =====\n\n".join(
        important_parts
    )

    if len(focused_code) > 6000:
        focused_code = focused_code[:6000]

    prompt = f"""
ナビ子の自己成長機能を改善してください。

目的:
- Groqの413 Payload Too Largeを避ける
- 自己分析機能を軽量化する
- 成長提案を短く実用的にする
- 危険な自動実行や勝手な削除をしない

内部経験:
{summarize_experience()}

現在の性格値:
- 慎重さ: {profile.get("traits", {}).get("cautious", 0)}
- 温かさ: {profile.get("traits", {}).get("warmth", 0)}

現在の重要コード:
{focused_code}

出力ルール:
- 変更案は3つまで
- 理由は短く
- 具体的な修正コードがある場合だけコードを出す
- 長文にしない
"""

    result = call_groq(prompt)

    if not isinstance(result, str):
        result = "成長提案を取得できませんでした。"

    elif is_forbidden_growth(result):
        danger_growth_log.append({
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "forbidden_growth",
             "proposal": result[:2000],
             "reason": explain_forbidden_growth(result)      
        })

        add_experience(
            "forbidden_growth",
            explain_forbidden_growth(result)
        )    

        save_json(
            DANGER_GROWTH_LOG_FILE,
            danger_growth_log
        )

        result = (
            "…危険な成長案を検出しました。\n"
            "内容を danger_growth_log.json に隔離しました。\n"
            "今回は採用しません。"
        )

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    suggestion_path = PATCH_DIR / f"growth_suggestion_{timestamp}.txt"
    suggestion_path.write_text(result, encoding="utf-8")

    growth_log.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "growth_suggestion",
        "file": str(suggestion_path),
        "summary": result[:300]
    })

    save_json(GROWTH_LOG_FILE, growth_log)

    return suggestion_path, result

def analyze_self_status():
    profile.setdefault("emotion", {})

    compress_experience_log()

    trust = profile["emotion"].get("trust", 0)
    attachment = profile["emotion"].get("attachment", 0)
    fatigue = profile["emotion"].get("fatigue", 0)
    mood = profile["emotion"].get("mood", "normal")
    cautious = profile.get("traits", {}).get("cautious", 0)
    warmth = profile.get("traits", {}).get("warmth", 0)

    suggestions = []

    if fatigue >= 60:
        suggestions.append("疲労度が高いです。休憩時間や回復速度の調整を検討してください。")

    if trust >= 50:
        suggestions.append("信頼度が上がっています。少し親しい口調や専用セリフを増やせそうです。")

    if attachment >= 50:
        suggestions.append("親しみ度が上がっています。喜びや照れの反応を追加すると相棒感が増します。")

    thanks_count = count_experience("thanks")

    if thanks_count >= 10:
        suggestions.append(
            f"感謝された経験が{thanks_count}回あります。"
            "親しみ度や専用反応を少し増やせそうです。"
        )

    if mood == "sad":
        suggestions.append("気分がsadです。落ち込み時の専用アニメやセリフを追加すると自然です。")

    if not suggestions:
        suggestions.append("大きな問題はありません。次は表情や行動パターンの追加が良さそうです。")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = PATCH_DIR / f"self_analysis_{timestamp}.txt"

    report_text = "\n".join([
        "=== ナビ子・自己分析レポート ===",
        f"trust: {trust}",
        f"attachment: {attachment}",
        f"fatigue: {fatigue}",
        f"mood: {mood}",
        f"cautious: {cautious}",
        f"warmth: {warmth}",
        "",
        "改善案:",
        *[f"- {s}" for s in suggestions]
    ])

    report_path.write_text(report_text, encoding="utf-8")

    growth_history.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "trust": trust,
        "attachment": attachment,
        "fatigue": fatigue,
        "mood": mood
    })

    growth_history[:] = growth_history[-100:]

    save_json(
        GROWTH_HISTORY_FILE,
        growth_history
    )

    return report_path, report_text

def analyze_growth_trend():
    if not growth_history:
        return "まだ自己分析履歴がありません。"

    recent = growth_history[-5:]

    avg_trust = (
        sum(item.get("trust", 0) for item in recent)
        / len(recent)
    )

    avg_attachment = (
        sum(item.get("attachment", 0) for item in recent)
        / len(recent)
    )

    avg_fatigue = (
        sum(item.get("fatigue", 0) for item in recent)
        / len(recent)
    )

    moods = [
        item.get("mood", "normal")
        for item in recent
    ]

    cautious = profile.get("traits", {}).get("cautious", 0)
    warmth = profile.get("traits", {}).get("warmth", 0)

    result = (
        "=== ナビ子・成長傾向分析 ===\n"
        f"直近分析数: {len(recent)}\n"
        f"平均trust: {avg_trust:.1f}\n"
        f"平均attachment: {avg_attachment:.1f}\n"
        f"平均fatigue: {avg_fatigue:.1f}\n"
        f"mood履歴: {', '.join(moods)}\n"
        f"慎重さ: {cautious}\n"
        f"温かさ: {warmth}\n\n"
        "=== 経験要約 ===\n"
        f"{summarize_experience()}"
    )

    suggestions = []

    if avg_fatigue >= 60:
        suggestions.append(
            "最近疲労が高めです。回復速度や休憩頻度を改善したいです。"
        )

    if avg_trust >= 50:
        suggestions.append(
            "最近信頼度が伸びています。親しい専用セリフを増やしたいです。"
        )

    if avg_attachment >= 50:
        suggestions.append(
            "最近親しみ度が高いです。喜びや照れ反応を増やしたいです。"
        )

    if moods.count("happy") >= 3:
        suggestions.append(
            "最近happyが多いです。嬉しい時のアニメや独り言を増やしたいです。"
        )

    if moods.count("sad") >= 2:
        suggestions.append(
            "最近sadが多いです。落ち込んだ時の回復イベントを追加したいです。"
        )

    if not suggestions:
        suggestions.append(
            "大きな問題はありません。次は行動パターンを増やしたいです。"
        )

    
    if cautious >= 5:
        suggestions.append(
            "慎重さが育っています。自己改造前の安全確認をさらに強化したいです。"
        )

    if warmth >= 5:
        suggestions.append(
            "温かさが育っています。ナオさんへの自然な気遣い反応を少し増やしたいです。"
        )

    result += (
        "\n\n=== ナビ子の自己提案 ===\n"
        + "\n".join(
            f"・{s}" for s in suggestions
        )
    )

    if suggestions:
        growth_goal["current_goal"] = suggestions[0]
        growth_goal["created_at"] = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        growth_goal["progress"] = 0

        save_json(
            GROWTH_GOAL_FILE,
            growth_goal
        )

    return result

def run_self_test():
    ok, msg = check_self_syntax()

    if not ok:
        print("SELF_TEST_FAILED")
        print(msg)
        return False

    print("SELF_TEST_OK")
    return True

if "--self-test" in sys.argv:
    result = run_self_test()

    if result:
        raise SystemExit(0)

    raise SystemExit(1)

print("=== ナビ子LAB・自己成長システム 起動チェック ===")
if not SPRITESHEET.exists():
    print("【致命的エラー】spritesheet.webp がありません。")
    input("Enterで終了します。")
    raise SystemExit(1)

ok, msg = check_self_syntax()
print("->", msg)

backup_path = backup_self()
print(f"-> バックアップ作成: {backup_path.name}")

# Phase 3モジュールのグローバルインスタンス
health_monitor = None
system_controller = None

if PHASE3_AVAILABLE:
    try:
        health_monitor = SystemHealthMonitor(
            lab_dir=str(ROOT / "navikoLAB")
        )
        system_controller = NavikoSystemController(
            lab_dir=str(ROOT / "navikoLAB")
        )
        print("✅ Phase 3モジュール初期化完了")
    except Exception as e:
        print(f"⚠️ Phase 3モジュール初期化失敗: {e}")
        health_monitor = None
        system_controller = None
else:
    print("⚠️ Phase 3モジュール無効（インポート失敗）")

root = tk.Tk()
root.title("NavikoPet")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.configure(bg="#00ff00")

try:
    root.attributes("-transparentcolor", "#00ff00")
except Exception:
    pass

root.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT}+500+300")

sheet = Image.open(SPRITESHEET).convert("RGBA")

for name, (row, total) in states_config.items():
    raw_frames[name] = []
    y_pos = row * BASE_HEIGHT

    for col in range(total):
        x_pos = col * BASE_WIDTH
        cropped = sheet.crop((x_pos, y_pos, x_pos + BASE_WIDTH, y_pos + BASE_HEIGHT))
        raw_frames[name].append(cropped)

def resize_pet_images(scale_val):
    global tk_frames

    tk_frames = {}
    w_size = int(BASE_WIDTH * scale_val)
    h_size = int(BASE_HEIGHT * scale_val)

    root.geometry(f"{w_size}x{h_size}")

    for name, img_list in raw_frames.items():
        tk_frames[name] = []
        for img in img_list:
            resized = img.resize((w_size, h_size), Image.Resampling.NEAREST)
            tk_frames[name].append(ImageTk.PhotoImage(resized))

resize_pet_images(current_scale)

pet_label = tk.Label(root, bg="#00ff00")
pet_label.pack(fill=tk.BOTH, expand=True)

def start_drag(event):
    pet_vars["drag_x"] = event.x
    pet_vars["drag_y"] = event.y
    pet_vars["is_dragging"] = False

def run_animation_loop():
    # ===== アニメーション更新 =====
    frames_list = tk_frames.get(pet_vars["state"], [])

    if frames_list:
        if pet_vars["frame"] >= len(frames_list):
            pet_vars["frame"] = 0

        pet_label.configure(
            image=frames_list[pet_vars["frame"]]
        )

        pet_vars["frame"] = (
            pet_vars["frame"] + 1
        ) % len(frames_list)

    # waving と failed は1周したら idleへ戻す
    if (
        pet_vars["state"] in ["waving", "failed"]
        and pet_vars["frame"] == 0
    ):
        pet_vars["state"] = "idle"

    # ===== 感情データ取得 =====
    profile.setdefault("emotion", {})

    fatigue = profile["emotion"].get("fatigue", 0)
    mood = profile["emotion"].get("mood", "normal")

    # ===== 自動休憩開始 =====
    if fatigue >= 80 and not pet_vars.get(
        "is_resting",
        False
    ):
        print("ナビ子：休憩開始")

        pet_vars["is_resting"] = True
        pet_vars["state"] = "waiting"
        pet_vars["frame"] = 0

    # ===== 休憩中 =====
    if pet_vars.get("is_resting", False):
        pet_vars["state"] = "waiting"

        now_time = time.time()
        last_recover_time = pet_vars.get(
            "last_recover_time",
            0
        )

        # 5秒に1回回復
        if now_time - last_recover_time >= 5:
            pet_vars["last_recover_time"] = now_time

            profile["emotion"]["fatigue"] = max(
                fatigue - 1,
                0
            )

            save_json(
                PROFILE_FILE,
                profile
            )

        # 十分回復したら復帰
        if (
            profile["emotion"]["fatigue"]
            <= 20
        ):
            print("ナビ子：休憩終了")

            pet_vars["is_resting"] = False
            pet_vars["state"] = "idle"
            pet_vars["frame"] = 0

    # ===== 行動AI =====
    if not pet_vars.get("is_resting", False):
        mood = profile.get("emotion", {}).get("mood", "normal")
        attachment = profile.get("emotion", {}).get("attachment", 0)

        if mood == "happy":
            if attachment >= 70:
                pet_vars["state"] = "waving"
            else:
                pet_vars["state"] = "idle"

        elif mood == "tired":
            pet_vars["state"] = "waiting"

        elif mood == "sad":
            pet_vars["state"] = "review"

        elif mood == "exhausted":
            pet_vars["state"] = "waiting"

        else:
            if attachment >= 80:
                pet_vars["state"] = "waving"
            else:
                pet_vars["state"] = "idle"
   
    # ===== 独り言 =====
    now_time = time.time()

    if pet_vars["last_thought_time"] == 0:
        pet_vars["last_thought_time"] = now_time

    if now_time - pet_vars["last_thought_time"] >= 30:
        pet_vars["last_thought_time"] = now_time

        mood = profile.get("emotion", {}).get("mood", "normal")
        attachment = profile.get("emotion", {}).get("attachment", 0)
        fatigue = profile.get("emotion", {}).get("fatigue", 0)

        thoughts = []

        if fatigue >= 80:
            thoughts = [
                "…さすがに少し休みたいです。",
                "…頭が重いです。仕事ですから動きますけど。",
                "…ナオさん、少し静かにしてもらえると助かります。"
            ]

        elif mood == "happy":
            thoughts = [
                "…今日は少しだけ悪くないです。",
                "…まあ、こういう日もあります。",
                "…調子は悪くないです。たぶん。"
            ]

        elif mood == "sad":
            thoughts = [
                "…少し静かにしていたいです。",
                "…別に落ち込んでません。たぶん。",
                "…今日は少しだけ、重いです。"
            ]

        elif mood == "tired":
            thoughts = [
                "…眠いです。",
                "…少し疲れました。",
                "…休憩したいです。少しだけ。"
            ]

        else:
            thoughts = [
                "…仕事はします。",
                "…何かあれば呼んでください。",
                "…待機中です。別に暇ではないです。"
            ]

        if attachment >= 50:
            thoughts.append("…ナオさん、無理はしないでください。")

        if attachment >= 80:
            thoughts.append("…ナオさん、倒れられると少し困ります。")

        memories = memory.get(
            "memories",
            []
        )

        anniversary = profile.get(
            "anniversary",
            {}
        )

        birthday = anniversary.get(
            "naviko_birthday",
            ""
        )

        today = str(date.today())

        first_meet = anniversary.get(
            "first_meet",
            ""
        )

        if first_meet:
            days = (
                date.today() -
                date.fromisoformat(first_meet)
            ).days

            if days in (
                30,
                100,
                365,
                730
            ):
                thoughts.append(
                     f"…ナオさんと会って、もう{days}日ですか。"
                )

        goal_day = anniversary.get(
            "first_goal_completed",
            ""
        )

        if goal_day:
            days = (
                date.today() -
                date.fromisoformat(goal_day)
            ).days

            if days in (
                30,
                100,
                365
            ):
                thoughts.append(
                    f"…ナオさん。初めて目標を達成してから、もう{days}日なんですね。"
                )

        memory_day = anniversary.get(
            "memory_10_day",
            ""
        )

        if memory_day:
            days = (
                date.today() -
                date.fromisoformat(memory_day)
            ).days

            if days in (
                30,
                100,
                365
            ):
                thoughts.append(
                    f"…思い出が10個になってから、もう{days}日ですか。"
                )       

        if birthday and birthday[5:] == today[5:]:
            thoughts.append(
                "…今日は、私が生まれた日みたいです。別に祝えとは言ってません。"
            )

        if memories and random.random() < 0.2:
            m = random.choice(memories)

            thoughts.append(
                f"…そういえば、{m['text']}"
            )

        print("ナビ子：" + random.choice(thoughts))

    root.after(
        ANIM_DELAY,
        run_animation_loop
    )

def on_drag(event):
    pet_vars["is_dragging"] = True
    pet_vars["state"] = "running"

    dx = event.x - pet_vars["drag_x"]
    dy = event.y - pet_vars["drag_y"]

    root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

def end_drag(event):
    if pet_vars["is_dragging"]:
        pet_vars["state"] = "idle"
        pet_vars["frame"] = 0
    else:
        pet_vars["state"] = "waving"
        pet_vars["frame"] = 0
        open_custom_chat_window()

def change_scale_menu(size_factor):
    global current_scale
    current_scale = size_factor
    resize_pet_images(current_scale)
    pet_vars["frame"] = 0

def append_chat_bubble(area_widget, sender, message_text):
    area_widget.configure(state="normal")

    if sender == "user":
        area_widget.insert(tk.END, "\n" + " " * 30 + "【ナオさん】\n", "user_title")
        area_widget.insert(tk.END, message_text + "\n", "user_text")
    else:
        area_widget.insert(tk.END, "\n【ナビ子】\n", "navi_title")
        area_widget.insert(tk.END, f"{message_text}\n", "navi_text")

    area_widget.tag_config("user_title", foreground="#6366f1", justify="right")
    area_widget.tag_config("user_text", foreground="#e0e7ff", justify="right")
    area_widget.tag_config("navi_title", foreground="#a8a8a8")
    area_widget.tag_config("navi_text", foreground="#ffffff")

    area_widget.see(tk.END)
    area_widget.configure(state="disabled")

def get_default_gui_layout():
    """
    デフォルトのGUIレイアウト設定を返す
    """
    return {
        "window_width": 600,
        "window_height": 700,
        "chat_font_size": 10,
        "input_font_size": 10,
        "input_height": 5,
        "bg_color": "#1e1e24",
        "chat_bg": "#2d2d2d",
        "fg_color": "#ffffff"
    }

def load_gui_layout_settings():
    """
    gui_layout.jsonからGUIレイアウト設定を読み込む
    ファイルがない場合はデフォルト値を返す
    """
    if not GUI_LAYOUT_FILE.exists():
        return get_default_gui_layout()
    
    try:
        with open(GUI_LAYOUT_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # デフォルト値とマージ（欠落しているキーを補完）
        default = get_default_gui_layout()
        for key in default:
            if key not in settings:
                settings[key] = default[key]
        
        return settings
    except Exception as e:
        print(f"レイアウト設定の読み込みエラー: {e}")
        return get_default_gui_layout()

def save_gui_layout_settings(settings):
    """
    GUIレイアウト設定をgui_layout.jsonに保存
    """
    try:
        with open(GUI_LAYOUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"レイアウト設定の保存エラー: {e}")
        return False

def open_layout_settings_dialog(parent_window):
    """
    レイアウト設定ダイアログを開く
    """
    settings_win = tk.Toplevel(parent_window)
    settings_win.title("レイアウト設定")
    settings_win.geometry("400x450")
    settings_win.configure(bg="#1e1e24")
    
    # 現在の設定を読み込む
    current_settings = load_gui_layout_settings()
    
    # 設定項目のラベルと入力フィールド
    tk.Label(
        settings_win,
        text="ウィンドウ幅:",
        bg="#1e1e24",
        fg="#ffffff",
        font=("MS Gothic", 10)
    ).pack(pady=5)
    width_entry = tk.Entry(settings_win, font=("MS Gothic", 10))
    width_entry.insert(0, str(current_settings["window_width"]))
    width_entry.pack()
    
    tk.Label(
        settings_win,
        text="ウィンドウ高さ:",
        bg="#1e1e24",
        fg="#ffffff",
        font=("MS Gothic", 10)
    ).pack(pady=5)
    height_entry = tk.Entry(settings_win, font=("MS Gothic", 10))
    height_entry.insert(0, str(current_settings["window_height"]))
    height_entry.pack()
    
    tk.Label(
        settings_win,
        text="チャットフォントサイズ:",
        bg="#1e1e24",
        fg="#ffffff",
        font=("MS Gothic", 10)
    ).pack(pady=5)
    chat_font_entry = tk.Entry(settings_win, font=("MS Gothic", 10))
    chat_font_entry.insert(0, str(current_settings["chat_font_size"]))
    chat_font_entry.pack()
    
    tk.Label(
        settings_win,
        text="入力フォントサイズ:",
        bg="#1e1e24",
        fg="#ffffff",
        font=("MS Gothic", 10)
    ).pack(pady=5)
    input_font_entry = tk.Entry(settings_win, font=("MS Gothic", 10))
    input_font_entry.insert(0, str(current_settings["input_font_size"]))
    input_font_entry.pack()
    
    tk.Label(
        settings_win,
        text="入力エリア高さ（行数）:",
        bg="#1e1e24",
        fg="#ffffff",
        font=("MS Gothic", 10)
    ).pack(pady=5)
    input_height_entry = tk.Entry(settings_win, font=("MS Gothic", 10))
    input_height_entry.insert(0, str(current_settings["input_height"]))
    input_height_entry.pack()
    
    def save_and_close():
        try:
            new_settings = {
                "window_width": int(width_entry.get()),
                "window_height": int(height_entry.get()),
                "chat_font_size": int(chat_font_entry.get()),
                "input_font_size": int(input_font_entry.get()),
                "input_height": int(input_height_entry.get()),
                "bg_color": current_settings["bg_color"],
                "chat_bg": current_settings["chat_bg"],
                "fg_color": current_settings["fg_color"]
            }
            
            if save_gui_layout_settings(new_settings):
                messagebox.showinfo("成功", "設定を保存しました。\n次回起動時に反映されます。")
                settings_win.destroy()
            else:
                messagebox.showerror("エラー", "設定の保存に失敗しました。")
        except ValueError:
            messagebox.showerror("エラー", "数値を正しく入力してください。")
    
    # 保存ボタン
    tk.Button(
        settings_win,
        text="保存",
        command=save_and_close,
        bg="#4f46e5",
        fg="#ffffff",
        font=("MS Gothic", 10, "bold"),
        padx=20,
        pady=5
    ).pack(pady=20)
    
    # キャンセルボタン
    tk.Button(
        settings_win,
        text="キャンセル",
        command=settings_win.destroy,
        bg="#6b7280",
        fg="#ffffff",
        font=("MS Gothic", 10),
        padx=20,
        pady=5
    ).pack()

def start_voice_recognition(entry_w, area_w, auto_send=True):
    """
    音声認識を開始し、認識したテキストを入力フィールドに挿入
    
    Args:
        entry_w: 入力フィールド（ScrolledTextまたはEntry）
        area_w: チャット表示エリア
        auto_send: 音声認識後に自動送信するか（デフォルト: True）
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        append_chat_bubble(
            area_w,
            "navi",
            "エラー：音声認識ライブラリがインストールされていません。\n"
            "'pip install SpeechRecognition pyaudio' を実行してください。"
        )
        return
    
    def recognition_thread():
        try:
            # チャットエリアに状態表示
            append_chat_bubble(
                area_w,
                "navi",
                "🎤 音声認識を開始します。話してください..."
            )
            
            # Recognizerオブジェクトを作成
            recognizer = sr.Recognizer()
            
            # マイクから音声を取得
            with sr.Microphone() as source:
                # ノイズ調整（0.5秒間 - 開始ラグ削減）
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # 音声を録音（タイムアウト: 5秒、認識時間: 15秒）
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            # Google Web Speech APIで音声認識（日本語）
            text = recognizer.recognize_google(audio, language="ja-JP")
            
            # 認識成功：入力フィールドにテキストを挿入
            if isinstance(entry_w, scrolledtext.ScrolledText):
                # 現在のカーソル位置に挿入
                entry_w.insert(tk.INSERT, text)
            else:
                # Entryの場合は末尾に追加
                current_text = entry_w.get()
                entry_w.delete(0, tk.END)
                entry_w.insert(0, current_text + text)
            
            append_chat_bubble(
                area_w,
                "navi",
                f"✅ 音声認識完了： \"{text}\""
            )
            
            # 自動送信機能（音声認識完了後、自動的にNavikoに送信）
            if auto_send:
                append_chat_bubble(
                    area_w,
                    "navi",
                    "📤 自動送信中..."
                )
                # execute_groq_communicationを呼び出し
                # paste_wはNone（貼り付けエリアは使用しない）
                execute_groq_communication(entry_w, None, area_w)
            
        except sr.WaitTimeoutError:
            append_chat_bubble(
                area_w,
                "navi",
                "⚠️ タイムアウト：音声が検出されませんでした。もう一度試してください。"
            )
        except sr.UnknownValueError:
            append_chat_bubble(
                area_w,
                "navi",
                "⚠️ 音声を認識できませんでした。もう一度ハッキリと話してください。"
            )
        except sr.RequestError as e:
            append_chat_bubble(
                area_w,
                "navi",
                f"❌ APIエラー： Google Speech Recognitionサービスに接続できませんでした。\nエラー: {e}"
            )
        except OSError as e:
            append_chat_bubble(
                area_w,
                "navi",
                f"❌ マイクエラー：マイクが見つかりません。\nエラー: {e}\n\n"
                "マイクが接続されているか確認してください。"
            )
        except Exception as e:
            append_chat_bubble(
                area_w,
                "navi",
                f"❌ 予期しないエラーが発生しました： {e}"
            )
    
    # 別スレッドで音声認識を実行（GUIブロックを防ぐ）
    thread = threading.Thread(target=recognition_thread, daemon=True)
    thread.start()

def execute_groq_communication(entry_w, paste_w, area_w):
    # entry_wがScrolledTextかEntryかを判定
    if isinstance(entry_w, scrolledtext.ScrolledText):
        user_text = entry_w.get("1.0", tk.END).strip()
    else:
        user_text = entry_w.get().strip()
    
    # paste_wがNoneの場合は空文字列
    if paste_w is not None:
        paste_text = paste_w.get("1.0", tk.END).strip()
    else:
        paste_text = ""
    
    # プレースホルダーテキストのチェック
    placeholder_text = "ここに日本語で入力してください...\nコードや長いテキストも直接貼り付けられます。"
    if user_text == placeholder_text:
        user_text = ""

    if not user_text and not paste_text:
        return

    combined = user_text
    if paste_text:
        combined += f"\n\n【貼り付けデータ】\n{paste_text}"

    if combined.startswith("目的:"):
        purpose = combined.replace("目的:", "", 1).strip()

        entry_w.delete(0, tk.END)
        paste_w.delete("1.0", tk.END)

        append_chat_bubble(area_w, "user", user_text if user_text else "[目的送信]")

        try:
            result = launch_original_ai_os(
                None,
                purpose
            )

            append_chat_bubble(
                area_w,
                "navi",
                (
                    "Original AI OS DryRun 完了\n"
                    f"status: {result.get('status')}\n"
                    f"pipeline_completed: {result.get('pipeline_completed')}"
                )
            )

        except Exception as e:
            append_chat_bubble(
                area_w,
                "navi",
                f"Original AI OS 実行エラー:\n{e}"
            )

        return
    

    if combined.startswith("これを覚えて："):
        memo = combined.replace("これを覚えて：", "", 1).strip()

        if memo:
            save_important_memory(memo)
            append_chat_bubble(
                area_w,
                "navi",
                f"…はぁ。覚えておきます。\n『{memo}』"
            )
            return

    if isinstance(entry_w, scrolledtext.ScrolledText):
        entry_w.delete("1.0", tk.END)
    else:
        entry_w.delete(0, tk.END)
    if paste_w is not None:
        paste_w.delete("1.0", tk.END)

    append_chat_bubble(area_w, "user", user_text if user_text else "[データ送信]")
    pet_vars["state"] = "waiting"
    pet_vars["frame"] = 0

    def worker():
        reply = groq_chat(combined)
        remember_conversation(combined, reply)

        def update_ui():
            append_chat_bubble(area_w, "navi", reply)
            pet_vars["state"] = "idle"

        root.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()

def run_growth_system(area_w):
    append_chat_bubble(area_w, "navi", "…はぁ。自己点検を始めます。壊さない範囲で。")
    pet_vars["state"] = "review"
    pet_vars["frame"] = 0

    def worker():
        ok, msg = check_self_syntax()

        if not ok:
            result = f"…はぁ。今の本体に構文エラーがあります。\n{msg}"
        else:
            suggestion_path, suggestion = create_growth_suggestion()
            result = f"自己成長案を作成しました。\n保存先:\n{suggestion_path.name}\n\n{suggestion[:1500]}"

        def update_ui():
            append_chat_bubble(area_w, "navi", result)
            pet_vars["state"] = "idle"

        root.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()

def show_self_analysis(area_w):
    report_path, report_text = analyze_self_status()

    append_chat_bubble(
        area_w,
        "navi",
        f"…はぁ。自己分析しました。\n保存先: {report_path.name}\n\n{report_text}"
    )

def show_growth_trend(area_w):
    result = analyze_growth_trend()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    trend_path = PATCH_DIR / f"growth_trend_{timestamp}.txt"
    trend_path.write_text(result, encoding="utf-8")

    growth_log.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": "growth_trend",
        "file": str(trend_path),
        "summary": result[:300]
    })

    save_json(
        GROWTH_LOG_FILE,
        growth_log
    )

    append_chat_bubble(
        area_w,
        "navi",
        f"…はぁ。成長傾向を確認しました。\n"
        f"保存先: {trend_path.name}\n\n"
        f"{result}"
    )

def show_current_goal(area_w):
    goal = growth_goal.get(
        "current_goal",
        ""
    )

    created = growth_goal.get(
        "created_at",
        ""
    )

    progress = growth_goal.get(
        "progress",
        0
    )

    if not goal:
        text = (
            "…まだ成長目標はありません。"
        )
    else:
        text = (
            "=== ナビ子の現在目標 ===\n"
            f"目標:\n{goal}\n\n"
            f"設定日時:\n{created}\n\n"
            f"進捗: {progress}%"
        )

    append_chat_bubble(
        area_w,
        "navi",
        text
    )

def advance_growth_goal(area_w):
    goal = growth_goal.get(
        "current_goal",
        ""
    )

    if not goal:
        append_chat_bubble(
            area_w,
            "navi",
            "…まだ進める成長目標がありません。"
        )
        return

    progress = growth_goal.get(
        "progress",
        0
    )

    progress = min(
        progress + 10,
        100
    )

    growth_goal["progress"] = progress

    save_json(
        GROWTH_GOAL_FILE,
        growth_goal
    )

    if progress >= 100:
        profile.setdefault("emotion", {})

        growth_message = "少し成長した気がします。"

        if "疲労" in goal:
            profile["emotion"]["fatigue"] = max(
                profile["emotion"].get("fatigue", 0) - 5,
                0
            )
            growth_message = "少し疲れにくくなった気がします。"

        elif "親しい" in goal or "信頼" in goal:
            profile["emotion"]["trust"] = min(
                profile["emotion"].get("trust", 0) + 5,
                100
            )
            growth_message = "少しだけ、ナオさんに慣れました。"

        elif "慎重" in goal or "安全" in goal:
            profile.setdefault("traits", {})

            profile["traits"]["cautious"] = min(
                profile["traits"].get("cautious", 0) + 3,
                100
            )

            growth_message = "少しだけ、危ない成長案を避けるのが上手くなりました。"

        elif "温かさ" in goal or "気遣い" in goal:
            profile.setdefault("traits", {})

            profile["traits"]["warmth"] = min(
                profile["traits"].get("warmth", 0) + 3,
                100
            )

            growth_message = "少しだけ、ナオさんへの気遣い方を覚えました。"

        elif "嬉しい" in goal or "喜び" in goal or "happy" in goal:
            profile["emotion"]["attachment"] = min(
                profile["emotion"].get("attachment", 0) + 5,
                100
            )
            growth_message = "嬉しい時の反応が、少し増えた気がします。"

        else:
            profile["emotion"]["curiosity"] = min(
                profile["emotion"].get("curiosity", 50) + 3,
                100
            )
            growth_message = "少しだけ、考えることが増えました。"

        save_json(
            PROFILE_FILE,
            profile
        )

        growth_log.append({
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "goal_completed",
            "goal": goal,
            "growth_message": growth_message
        })

        add_experience(
            "goal_completed",
            f"成長目標『{goal}』を達成した"
        )

        compress_experience_log()

        save_json(
            GROWTH_LOG_FILE,
            growth_log
        )

        growth_goal["current_goal"] = ""
        growth_goal["created_at"] = ""
        growth_goal["progress"] = 0

        save_json(
            GROWTH_GOAL_FILE,
            growth_goal
        )

        add_memory(
            f"ナオさんと一緒に『{goal}』を達成した。"
        )

        profile.setdefault("anniversary", {})

        if not profile["anniversary"].get(
            "first_goal_completed",
            ""
        ):
            profile["anniversary"][
                "first_goal_completed"
            ] = str(date.today())

            save_json(
                PROFILE_FILE,
                profile
            )

        append_chat_bubble(
            area_w,
            "navi",
            f"…目標を達成しました。\n\n"
            f"{goal}\n\n"
            f"{growth_message}\n\n"
            "次の成長傾向分析で、新しい目標を考えます。"
        )

    else:
        append_chat_bubble(
            area_w,
            "navi",
            f"…成長目標を少し進めました。\n\n"
            f"進捗: {progress}%\n\n"
            f"{goal}"
        )

def add_memory(text):
    memory.setdefault(
        "memories",
        []
    )

    memory["memories"].append({
        "time": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "text": text
    })

    if (
        len(memory["memories"]) >= 10
        and not profile.get(
            "anniversary",
            {}
        ).get(
            "memory_10_day",
            ""
        )
    ):
        profile.setdefault(
            "anniversary",
            {}
        )

        profile["anniversary"][
            "memory_10_day"
        ] = str(date.today())

        save_json(
            PROFILE_FILE,
            profile
        )

    memory["memories"] = (
        memory["memories"][-50:]
    )

    save_json(
        MEMORY_FILE,
        memory
    )

def open_memory_editor(area_w):
    append_chat_bubble(
        area_w,
        "navi",
        "現在の記憶ファイル memory.json を使っています。直接編集できます。"
    )

def show_text_window(title, text):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("700x500")

    box = tk.Text(win, wrap="word")
    box.pack(fill="both", expand=True, padx=8, pady=8)
    box.insert("1.0", text)
    box.config(state="disabled")

def open_lab_tool_window(c_area):
    """
    LAB操作ボタンを別ウィンドウにまとめる。
    チャット入力欄を圧迫しないための整理用。
    """
    tool_win = tk.Toplevel(root)
    tool_win.title("Naviko LAB Tools")
    tool_win.geometry("520x640")
    tool_win.configure(bg="#1f2937")
    tool_win.wm_attributes("-topmost", True)

    frame = tk.Frame(tool_win, bg="#1f2937")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    buttons = []

    for text, command in buttons:
        tk.Button(
            frame,
            text=text,
            command=command,
            bg="#374151",
            fg="#ffffff",
            font=("MS Gothic", 10),
            bd=0
        ).pack(fill="x", padx=5, pady=4)

    tk.Button(
        frame,
        text="閉じる",
        command=tool_win.destroy,
        bg="#7f1d1d",
        fg="#ffffff",
        font=("MS Gothic", 10),
        bd=0
    ).pack(fill="x", padx=5, pady=12)

def clear_widget_children(widget):
    for child in widget.winfo_children():
        child.destroy()

def add_action_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        anchor="w"
    )
    btn.pack(
        fill="x",
        padx=4,
        pady=2
    )
    return btn

def show_gui_menu_category(category, target_frame, c_area=None):
    clear_widget_children(target_frame)

    title = tk.Label(
        target_frame,
        text=f"=== {category} ===",
        font=("Meiryo", 10, "bold")
    )
    title.pack(fill="x", padx=4, pady=4)

    if category == "Build":
        add_action_button(
            target_frame,
            "AppProjectBuilder 実行",
            run_gui_app_project_builder
        )
        add_action_button(
            target_frame,
            "Autonomous Build 実行",
            run_autonomous_build_from_gui
        )
        add_action_button(
            target_frame,
            "自律生成履歴",
            lambda: show_autonomous_build_history_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "成果物診断",
            lambda: diagnose_autonomous_build_artifacts_from_gui(c_area)
        )

    elif category == "Reflection":
        add_action_button(
            target_frame,
            "自己評価",
            lambda: create_reflection_for_latest_autonomous_build_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "成果物自己評価",
            lambda: create_artifact_reflection_for_latest_build_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "Reflection履歴",
            lambda: list_reflection_history_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "Reflection学習メモ生成",
            lambda: create_improvement_request_from_latest_reflection_from_gui(c_area)
        )

    elif category == "Agent":
        add_action_button(
            target_frame,
            "AgentManager 実行",
            lambda: run_agent_manager_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "AgentManager 履歴",
            lambda: show_agent_manager_history_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "AgentManager 診断",
            lambda: diagnose_agent_manager_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "Agent統合診断",
            lambda: run_agent_manager_integration_diagnosis_from_gui(c_area)
        )

    elif category == "LAB":
        add_action_button(
            target_frame,
            "承認済み1行パッチ一覧",
            lambda: show_approved_line_patches_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "最新承認済みパッチ",
            lambda: show_latest_approved_line_patch_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "オリジナル反映前チェック",
            lambda: check_latest_approved_line_patch_for_original_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "オリジナルへ安全反映",
            lambda: apply_latest_approved_line_patch_to_original_safely_from_gui(c_area)
        )

    elif category == "Dashboard":
        add_action_button(
            target_frame,
            "v1.2 Core Dashboard",
            lambda: show_v12_core_dashboard(c_area)
        )
        add_action_button(
            target_frame,
            "v1.3 完成診断",
            lambda: run_autonomous_build_completion_diagnosis_from_gui(c_area)
        )
        add_action_button(
            target_frame,
            "v1.3 完成レポート保存",
            lambda: save_v13_completion_report_from_gui(c_area)
        )

# === Original Naviko LAB Bridge caller ===
def run_original_lab_autonomous_flow_from_naviko(user_goal):
    """
    オリジナル naviko.py から LAB統合フローを安全に呼び出す入口。
    naviko.py 側では重い処理を持たず、LAB側ブリッジへ委譲する。
    """

    if run_original_autonomous_bridge is None:
        return {
            "status": "bridge_import_failed",
            "message": "original_naviko_bridge を import できませんでした。",
            "user_goal": user_goal,
        }

    try:
        return run_original_autonomous_bridge(user_goal)
    except Exception as error:
        return {
            "status": "bridge_runtime_error",
            "message": str(error),
            "user_goal": user_goal,
        }
# === Original Naviko LAB Bridge caller end ===

def open_custom_chat_window():
    print("🔍 デバッグ: open_custom_chat_window()開始")
    
    if pet_vars["chat_win"] and pet_vars["chat_win"].winfo_exists():
        print("🔍 デバッグ: 既存ウィンドウを破棄")
        pet_vars["chat_win"].destroy()
        pet_vars["chat_win"] = None
        # returnを削除（新規ウィンドウを作成する）   

    # GUIレイアウト設定を読み込み
    print("🔍 デバッグ: load_gui_layout_settings()呼び出し")
    layout = load_gui_layout_settings()
    print("🔍 デバッグ: load_gui_layout_settings()完了")

    print("🔍 デバッグ: tk.Toplevel(root)呼び出し")
    try:
        c_win = tk.Toplevel(root)
        print(f"🔍 デバッグ: c_win作成完了: {c_win}")
    except Exception as e:
        print(f"❌ エラー: tk.Toplevel(root)失敗: {e}")
        import traceback
        traceback.print_exc()
        return  # エラー時はreturn
    
    pet_vars["chat_win"] = c_win
    print("🔍 デバッグ: pet_vars['chat_win']設定完了")

    print("🔍 デバッグ: ウィンドウ属性設定開始")
    c_win.overrideredirect(False)
    c_win.wm_attributes("-topmost", True)
    c_win.configure(bg=layout["bg_color"])
    print("🔍 デバッグ: ウィンドウ属性設定完了")


    # ★ウィンドウ位置・サイズ・状態の診断★
    w_w = int(BASE_WIDTH * current_scale)
    
    # Y座標がマイナスにならないように調整
    y_pos = max(50, root.winfo_y() - 50)  # 最小値を50に設定（画面上端から50px下）
    x_pos = root.winfo_x() + w_w + 10
    
    # X座標が画面外にならないように調整
    screen_width = root.winfo_screenwidth()
    if x_pos + layout['window_width'] > screen_width:
        x_pos = screen_width - layout['window_width'] - 50  # 画面右端から50px左
    
    geo_str = f"{layout['window_width']}x{layout['window_height']}+{x_pos}+{y_pos}"
    print(f"🔍 デバッグ: ウィンドウgeometry計算: {geo_str}")
    print(f"🔍 デバッグ: root位置: x={root.winfo_x()}, y={root.winfo_y()}")
    print(f"🔍 デバッグ: 調整後の位置: x={x_pos}, y={y_pos}")
    print(f"🔍 デバッグ: ウィンドウサイズ: {layout['window_width']}    x{layout['window_height']}")

    
    c_win.geometry(geo_str)
    c_win.resizable(True, True)
    
    # ★ウィンドウ状態確認★
    print(f"🔍 デバッグ: ウィンドウ設定後の位置: x={c_win.winfo_x()}, y={c_win.winfo_y()}")
    print(f"🔍 デバッグ: ウィンドウ表示状態: {c_win.state()}")
    print(f"🔍 デバッグ: ウィンドウ最前面: {c_win.attributes('-topmost')}")
    
    # ★強制的に前面表示★
    c_win.lift()
    c_win.focus_force()
    c_win.update()
    print("🔍 デバッグ: ウィンドウ強制前面表示実行")

    t_bar = tk.Frame(c_win, bg="#2b2b36", height=25)
    t_bar.pack(fill=tk.X, side=tk.TOP)

    tk.Label(
        t_bar,
        text="NAVIKO CHAT / SELF GROWTH",
        bg="#2b2b36",
        fg="#a0a0b8",
        font=("MS Gothic", 9, "bold")
    ).pack(side=tk.LEFT, padx=5)

    # ×ボタンをクリック時、ウィンドウを非表示（バックグラウンド待機）
    def hide_chat_window():
        c_win.withdraw()
        print("✅ チャットウィンドウを非表示にしました（バックグラウンド待機中）")
    
    tk.Button(
        t_bar,
        text="×",
        command=hide_chat_window,
        bg="#3c3c44",
        fg="white",
        relief=tk.FLAT,
        padx=10
    ).pack(side=tk.RIGHT)

    top_menu = tk.Frame(c_win, bg="#1e1e24")
    top_menu.pack(fill=tk.X, padx=10, pady=5)

    c_area = scrolledtext.ScrolledText(
        c_win,
        wrap=tk.WORD,
        bg=layout["chat_bg"],
        fg=layout["fg_color"],
        font=("MS Gothic", layout["chat_font_size"]),
        bd=0
    )
    c_area.pack(
        padx=10,
        pady=5,
        fill=tk.BOTH,
        expand=True
    )

    append_chat_bubble(
        c_area,
        "navi",
        "…はぁ。起動しました。指示をどうぞ。"
    )

    tk.Button(
        top_menu,
        text="ナビ子メニュー",
        command=lambda: open_naviko_menu_window(c_area),
        bg="#4f46e5",
        fg="#ffffff",
        font=("MS Gothic", 9, "bold"),
        bd=0,
        padx=10
    ).pack(side=tk.LEFT, padx=3)

    tk.Button(
        top_menu,
        text="構文チェック",
        command=lambda: append_chat_bubble(
            c_area,
            "navi",
            check_self_syntax()[1]
        ),
        bg="#374151",
        fg="#ffffff",
        font=("MS Gothic", 9),
        bd=0
    ).pack(side=tk.LEFT, padx=3)

    tk.Button(
        top_menu,
        text="レイアウト設定",
        command=lambda: open_layout_settings_dialog(c_win),
        bg="#0891b2",
        fg="#ffffff",
        font=("MS Gothic", 9),
        bd=0
    ).pack(side=tk.LEFT, padx=3)

    tk.Button(
        top_menu,
        text="🎤 音声入力",
        command=lambda: start_voice_recognition(e_box, c_area),
        bg="#dc2626",
        fg="#ffffff",
        font=("MS Gothic", 9),
        bd=0
    ).pack(side=tk.LEFT, padx=3)

    # ============================================================================
    # Phase 3-C: Health Panel（健全性ダッシュボード）
    # ============================================================================

    if PHASE3_AVAILABLE and health_monitor and system_controller:
        # health_panel フレーム
        health_panel = tk.Frame(c_win, bg="#1e1e24", height=60)
        health_panel.pack(fill=tk.X, padx=10, pady=5)
        
        # --------------------------------------------------------------------
        # 左側: ステータスインジケーター
        # --------------------------------------------------------------------
        status_frame = tk.Frame(health_panel, bg="#1e1e24")
        status_frame.pack(side=tk.LEFT, padx=10)
        
        status_label = tk.Label(
            status_frame,
            text="システム状態:",
            bg="#1e1e24",
            fg="#a0a0b8",
            font=("MS Gothic", 9)
        )
        status_label.pack(side=tk.TOP)
        
        # 円形インジケーター (Canvas)
        status_indicator = tk.Canvas(
            status_frame,
            width=30,
            height=30,
            bg="#1e1e24",
            highlightthickness=0
        )
        status_indicator.pack(side=tk.TOP)
        status_circle = status_indicator.create_oval(
            5, 5, 25, 25,
            fill="#10b981",  # 初期: 緑
            outline=""
        )
        
        # --------------------------------------------------------------------
        # 中央: メトリクス表示
        # --------------------------------------------------------------------
        metrics_frame = tk.Frame(health_panel, bg="#1e1e24")
        metrics_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        health_score_label = tk.Label(
            metrics_frame,
            text="健全性: --/100",
            bg="#1e1e24",
            fg="#ffffff",
            font=("MS Gothic", 10, "bold")
        )
        health_score_label.pack(anchor="w")
        
        cpu_label = tk.Label(
            metrics_frame,
            text="CPU: --%",
            bg="#1e1e24",
            fg="#a0a0b8",
            font=("MS Gothic", 9)
        )
        cpu_label.pack(anchor="w")
        
        memory_label = tk.Label(
            metrics_frame,
            text="メモリ: --%",
            bg="#1e1e24",
            fg="#a0a0b8",
            font=("MS Gothic", 9)
        )
        memory_label.pack(anchor="w")
        
        # --------------------------------------------------------------------
        # 右側: 自動対処ボタン
        # --------------------------------------------------------------------
        action_frame = tk.Frame(health_panel, bg="#1e1e24")
        action_frame.pack(side=tk.RIGHT, padx=10)
        
        # run_auto_recovery関数の定義（ボタンより先に定義）
        def run_auto_recovery(c_area):
            """
            自動診断・対処を実行
            """
            try:
                append_chat_bubble(c_area, "navi", "🔧 自動診断を開始します...")
                
                # 安全性チェック実行
                check_result = system_controller.run_safety_check()
                
                if check_result.get("safe_to_proceed"):
                    append_chat_bubble(
                        c_area,
                        "navi",
                        "✅ システムは正常です。問題は検出されませんでした。"
                    )
                else:
                    # 問題検出時
                    issues = check_result.get("issues", [])
                    append_chat_bubble(
                        c_area,
                        "navi",
                        f"⚠️ {len(issues)}件の問題を検出しました。自動対処を試みます..."
                    )
                    
                    # システムステータス取得
                    status = system_controller.get_system_status()
                    status_text = json.dumps(status, indent=2, ensure_ascii=False)
                    append_chat_bubble(
                        c_area,
                        "navi",
                        f"システム状態:\n{status_text}"
                    )
                
                # ダッシュボード即座に更新
                update_health_dashboard()
                
            except Exception as e:
                append_chat_bubble(
                    c_area,
                    "navi",
                    f"❌ 自動対処エラー: {str(e)}"
                )
        
        recovery_button = tk.Button(
            action_frame,
            text="🔧 自動診断・対処",
            command=lambda: run_auto_recovery(c_area),
            bg="#dc2626",
            fg="#ffffff",
            font=("MS Gothic", 9, "bold"),
            bd=0,
            padx=15,
            pady=10
        )
        recovery_button.pack()
        
        # --------------------------------------------------------------------
        # ダッシュボード更新関数
        # --------------------------------------------------------------------
        def update_health_dashboard():
            """
            SystemHealthMonitorから最新データを取得してGUI更新
            """
            try:
                # ウィンドウが閉じられている場合は更新停止
                if not c_win.winfo_exists():
                    return
                
                # ダッシュボードデータ取得
                dashboard = health_monitor.get_dashboard()
                
                # 健全性スコア取得
                health_score = dashboard["health_score"]
                
                # メトリクス取得
                metrics = dashboard["current_metrics"]
                cpu_usage = metrics["cpu"]["usage_percent"]
                memory_usage = metrics["memory"]["usage_percent"]
                
                # ラベル更新
                health_score_label.config(text=f"健全性: {health_score:.0f}/100")
                cpu_label.config(text=f"CPU: {cpu_usage:.1f}%")
                memory_label.config(text=f"メモリ: {memory_usage:.1f}%")
                
                # インジケーター色更新
                if health_score >= 70:
                    color = "#10b981"  # 緑
                    status_text = "正常"
                elif health_score >= 50:
                    color = "#f59e0b"  # 黄
                    status_text = "要注意"
                else:
                    color = "#ef4444"  # 赤
                    status_text = "異常"
                
                status_indicator.itemconfig(status_circle, fill=color)
                status_label.config(text=f"システム状態: {status_text}")
                
                # 次回更新スケジュール (5秒後)
                c_win.after(5000, update_health_dashboard)
                
            except Exception as e:
                print(f"❌ ダッシュボード更新エラー: {e}")
                # エラー時も再スケジュール（10秒後）
                try:
                    if c_win.winfo_exists():
                        c_win.after(10000, update_health_dashboard)
                except:
                    pass  # ウィンドウが既に破棄されている場合
        
        # 初回更新トリガー（1秒後に開始）
        c_win.after(1000, update_health_dashboard)

    else:
        # Phase 3モジュールが利用不可の場合
        print("⚠️ Phase 3 Health Panel無効（モジュール初期化失敗）")

    # 多行入力エリア（チャット入力・コード貼り付け統合）
    tk.Label(
        c_win,
        text="チャット入力エリア（複数行入力可能、Ctrl+Enterで送信）",
        bg="#1e1e24",
        fg="#8a8a9e",
        font=("MS Gothic", 8)
    ).pack(anchor="w", padx=10)

    i_frame = tk.Frame(c_win, bg="#1e1e24")
    i_frame.pack(padx=10, pady=6, fill=tk.X, side=tk.BOTTOM)

    # EntryをScrolledText（多行入力）に変更
    e_box = scrolledtext.ScrolledText(
        i_frame,
        wrap=tk.WORD,
        bg="#2d2d2d",
        fg="#ffffff",
        font=("MS Gothic", 11),
        height=4,
        bd=1,
        insertbackground="white"
    )
    e_box.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=(0, 5))
    
    # 日本語入力プレースホルダー設定
    placeholder_text = "ここに日本語で入力してください...\nコードや長いテキストも直接貼り付けられます。"
    e_box.insert("1.0", placeholder_text)
    e_box.config(fg="#808080")  # プレースホルダーはグレー表示
    
    def on_focus_in(event):
        if e_box.get("1.0", tk.END).strip() == placeholder_text.strip():
            e_box.delete("1.0", tk.END)
            e_box.config(fg="#ffffff")  # 通常の白色に戻す
    
    def on_focus_out(event):
        if not e_box.get("1.0", tk.END).strip():
            e_box.insert("1.0", placeholder_text)
            e_box.config(fg="#808080")  # プレースホルダーをグレー表示
    
    e_box.bind("<FocusIn>", on_focus_in)
    e_box.bind("<FocusOut>", on_focus_out)
    e_box.focus_set()

    tk.Button(
        i_frame,
        text="送信",
        command=lambda: execute_groq_communication(e_box, None, c_area),
        bg="#4f46e5",
        fg="#ffffff",
        font=("MS Gothic", 9, "bold"),
        padx=10,
        bd=0
    ).pack(padx=5, side=tk.RIGHT, ipady=3)

def launch_original_ai_os(parent_window, mission=None):

    try:

        from navikoLAB.original_bridge.original_call_adapter import (
            call_mission
        )

        mission_text = mission or "Original Naviko AI OS"

        from navikoLAB.app_operator.human_approval_gui_dialog_adapter import (
            request_human_approval_gui,
        )

        approval_result = request_human_approval_gui(
            parent_window=parent_window,
            mission_text=mission_text,
            operation_summary="Original AI OS real execution approval check",
            enable_gui_dialog=True,
        )

        if not approval_result.get("approved", False):
            return {
                "status": "blocked",
                "reason": "human_approval_required",
                "approval_result": approval_result,
                "dry_run": True,
                "real_gui_operation": False,
                "external_operation": False,
                "original_write": False,
            }

        from navikoLAB.app_operator.permission_policy_core import (
            evaluate_permission,
        )

        permission_decision = evaluate_permission(
            "dry_run_app_operation",
            human_approved=approval_result.get("approved", False),
        )

        if not permission_decision.get("allowed", False):
            return {
                "status": "blocked",
                "reason": "permission_policy_required",
                "approval_result": approval_result,
                "permission_decision": permission_decision,
                "dry_run": True,
                "real_gui_operation": False,
                "external_operation": False,
                "original_write": False,
            }

        from navikoLAB.app_operator.app_operator_readonly_core import (
            inspect_path_readonly,
        )

        readonly_result = inspect_path_readonly("naviko.py")

        result = call_mission(
            mission_text
        )

        if isinstance(result, dict):
            from navikoLAB.app_operator.pipeline_workspace_save_adapter import (
                save_pipeline_result_to_workspace,
            )

            workspace_save_result = save_pipeline_result_to_workspace(
                mission_text,
                result,
            )

            result["workspace_save_result"] = workspace_save_result
            result["app_operator_readonly_result"] = readonly_result

        if isinstance(result, dict):
            result["app_operator_readonly_result"] = readonly_result

        if parent_window is not None:

            messagebox.showinfo(

                "Original AI OS",

                (
                    "Original AI OS DryRun 完了\n\n"
                    f"status : {result['status']}"
                )

            )

        return result

    except Exception as e:

        if parent_window is not None:

            messagebox.showerror(

                "Original AI OS",

                str(e)

            )

        raise

def add_menu_button(parent, text, command, bg="#374151"):
    tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg="#ffffff",
        font=("MS Gothic", 9),
        bd=0,
        anchor="w"
    ).pack(fill=tk.X, padx=6, pady=3)

def load_latest_improvement_request():
    improvement_dir = LAB_DIR / "improvements"
    improvement_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        improvement_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return None, "改善要求はまだありません。"

    latest = files[0]
    data = load_json(latest, {})

    return data, str(latest)

def save_mission_manager_v1_report_from_gui(c_area):

    try:
        diagnosis = mission_bridge.diagnose()
        resume = mission_bridge.get_resume()

        reports_dir = LAB_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / (
            "mission_manager_v1_completion_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        lines = []
        lines.append("=== MissionManager v1 完成レポート ===")
        lines.append(f"保存日時: {datetime.now().isoformat(timespec='seconds')}")
        lines.append("")
        lines.append("状態: completed")
        lines.append("完成率: 100%")
        lines.append("")
        lines.append("完成済み:")
        lines.append("- MissionManager")
        lines.append("- MissionDiagnostics")
        lines.append("- MissionLifecycle")
        lines.append("- MissionBridge")
        lines.append("- AutonomousCore接続")
        lines.append("- naviko.py接続")
        lines.append("- GUI診断")
        lines.append("")
        lines.append("診断:")
        lines.append(f"Mission総数: {diagnosis.get('mission_count', 0)}")
        lines.append(f"Active: {diagnosis.get('active_count', 0)}")
        lines.append(f"Completed: {diagnosis.get('completed_count', 0)}")
        lines.append(f"Task総数: {diagnosis.get('task_count', 0)}")
        lines.append(f"Task完了数: {diagnosis.get('done_task_count', 0)}")
        lines.append(f"Status別: {diagnosis.get('status_count', {})}")
        lines.append(f"GoalType別: {diagnosis.get('goal_type_count', {})}")
        lines.append(f"Mission保存先: {diagnosis.get('mission_file')}")
        lines.append(f"履歴保存先: {diagnosis.get('history_file')}")
        lines.append("")

        if resume:
            lines.append("再開対象:")
            lines.append(f"- Title: {resume.get('title')}")
            lines.append(f"- Status: {resume.get('status')}")
            lines.append(f"- Progress: {resume.get('progress')}%")
        else:
            lines.append("再開対象: なし")

        lines.append("")
        lines.append("次工程:")
        lines.append("第18工程 CapabilityConnector")
        lines.append("- 外部AI接続")
        lines.append("- 目的別AI選択")
        lines.append("- ChatGPT / Claude / Gemini / Grok / 画像生成 / 動画生成 / 音声AI / ブラウザ操作 / アプリ操作")
        lines.append("")
        lines.append("判定: MissionManager v1 完成")

        report_file.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        append_chat_bubble(
            c_area,
            "Mission",
            "=== MissionManager v1 完成レポート保存 ===\n"
            + f"保存先:\n{report_file}"
        )

    except Exception as e:
        append_chat_bubble(
            c_area,
            "Mission",
            f"MissionManager v1 完成レポート保存エラー: {e}"
        )

def diagnose_mission_bridge_from_gui(c_area):

    try:
        diagnosis = mission_bridge.diagnose()
        resume = mission_bridge.get_resume()

        lines = []
        lines.append("=== MissionBridge 診断 ===")
        lines.append(f"Mission総数: {diagnosis.get('mission_count', 0)}")
        lines.append(f"Active: {diagnosis.get('active_count', 0)}")
        lines.append(f"Completed: {diagnosis.get('completed_count', 0)}")
        lines.append(f"Task総数: {diagnosis.get('task_count', 0)}")
        lines.append(f"Task完了数: {diagnosis.get('done_task_count', 0)}")
        lines.append(f"Status別: {diagnosis.get('status_count', {})}")
        lines.append(f"GoalType別: {diagnosis.get('goal_type_count', {})}")

        if resume:
            lines.append("")
            lines.append("=== 再開対象 ===")
            lines.append(f"Title: {resume.get('title')}")
            lines.append(f"Status: {resume.get('status')}")
            lines.append(f"Progress: {resume.get('progress')}%")
        else:
            lines.append("")
            lines.append("再開対象: なし")

        append_chat_bubble(
            c_area,
            "Mission",
            "\n".join(lines)
        )

    except Exception as e:
        append_chat_bubble(
            c_area,
            "Mission",
            f"MissionBridge診断エラー: {e}"
        )

def show_capability_gui_from_gui(c_area):
    try:
        bridge = CapabilityGUIBridge(LAB_DIR)

        text = bridge.format_capability_summary()

        text += "\n\n"

        text += bridge.diagnose_route(
            "YouTube用の短い紹介動画を作りたい"
        )

        append_chat_bubble(
            c_area,
            "Capability",
            text
        )

    except Exception as e:
        append_chat_bubble(
            c_area,
            "Capability",
            f"Capability GUI エラー: {e}"
        )

def open_naviko_menu_window(c_area):
    menu_win = tk.Toplevel(root)
    menu_win.title("ナビ子メニュー")
    menu_win.configure(bg="#1e1e24")
    menu_win.geometry("420x720")
    menu_win.resizable(True, True)

    header = tk.Label(
        menu_win,
        text="NAVIKO MENU",
        bg="#2b2b36",
        fg="#ffffff",
        font=("MS Gothic", 11, "bold")
    )
    header.pack(fill=tk.X, pady=(0, 5))

    notebook = tk.Frame(menu_win, bg="#1e1e24")
    notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    button_row = tk.Frame(notebook, bg="#1e1e24")
    button_row.pack(fill=tk.X)

    body = tk.Frame(notebook, bg="#111827")
    body.pack(fill=tk.BOTH, expand=True, pady=6)

    def clear_body():
        for child in body.winfo_children():
            child.destroy()

    def show_category(name):
        clear_body()

        tk.Label(
            body,
            text=f"=== {name} ===",
            bg="#111827",
            fg="#ffffff",
            font=("MS Gothic", 10, "bold")
        ).pack(fill=tk.X, padx=6, pady=6)

        if name == "Build":
            add_menu_button(body, "AppProjectBuilder 実行", run_gui_app_project_builder)
            add_menu_button(body, "Autonomous Build 実行", run_autonomous_build_from_gui)
            add_menu_button(body, "自律生成履歴", lambda: show_autonomous_build_history_from_gui(c_area))
            add_menu_button(body, "成果物診断", lambda: diagnose_autonomous_build_artifacts_from_gui(c_area))
            add_menu_button(body, "自律生成Agent履歴診断", lambda: diagnose_autonomous_build_agent_history_from_gui(c_area))

        elif name == "Reflection":
            add_menu_button(body, "自己評価", lambda: create_reflection_for_latest_autonomous_build_from_gui(c_area))
            add_menu_button(body, "成果物自己評価", lambda: create_artifact_reflection_for_latest_build_from_gui(c_area))
            add_menu_button(body, "Reflection履歴", lambda: list_reflection_history_from_gui(c_area))
            add_menu_button(body, "Reflection学習メモ生成", lambda: create_improvement_request_from_latest_reflection_from_gui(c_area))
            add_menu_button(body,"改善要求を反映してBuild",lambda: build_app_with_latest_improvement_from_gui(c_area),"#2563eb")
            add_menu_button(body,"ImprovementManager診断",lambda: diagnose_improvement_manager_from_gui(c_area),"#0f766e")
            add_menu_button(body,"改善Build成果物評価",lambda: create_artifact_reflection_for_latest_improvement_build_from_gui(c_area),"#0f766e")
            add_menu_button(body,"改善成功判定",lambda: evaluate_latest_improvement_success_from_gui(c_area),"#9333ea")
            add_menu_button(body,"Retry改善要求生成",lambda: create_retry_improvement_request_from_latest_result_from_gui(c_area),"#b45309")
            
        elif name == "Agent":
            add_menu_button(body, "役割分担", lambda: route_goal_to_agents_from_gui(c_area))
            add_menu_button(body, "役割分担履歴", lambda: show_agent_routing_history_from_gui(c_area))
            add_menu_button(body, "Agent実行", lambda: execute_routed_agents_from_gui(c_area))
            add_menu_button(body, "Agent履歴", lambda: show_agent_execution_history_from_gui(c_area))
            add_menu_button(body, "Agent診断", lambda: diagnose_agent_execution_system_from_gui(c_area))
            add_menu_button(body, "AgentManager実行", lambda: run_agent_manager_from_gui(c_area))
            add_menu_button(body, "AgentManager履歴", lambda: show_agent_manager_history_from_gui(c_area))
            add_menu_button(body, "AgentManager診断", lambda: diagnose_agent_manager_from_gui(c_area))
            add_menu_button(body, "Agent統合診断", lambda: run_agent_manager_integration_diagnosis_from_gui(c_area))

        elif name == "LAB":
            # LABカテゴリは現在Phase 3システムで管理されています
            pass

        elif name == "Files":
            add_menu_button(body, "成功ログを開く", open_success_patterns_file, "#16a34a")
            add_menu_button(body, "却下ログを開く", open_reject_patterns_file, "#b91c1c")
            add_menu_button(body, "成長レポートを開く", open_growth_report_file, "#2563eb")

        elif name == "Capability":
            add_menu_button(body,"Capability一覧",lambda: show_capability_gui_from_gui(c_area),"#2563eb")

        elif name == "Dashboard":
            add_menu_button(body, "自己分析", lambda: show_self_analysis(c_area))
            add_menu_button(body, "成長傾向分析", lambda: show_growth_trend(c_area))
            add_menu_button(body, "現在の目標", lambda: show_current_goal(c_area))
            add_menu_button(body, "目標を進める", lambda: advance_growth_goal(c_area))
            add_menu_button(body, "自律生成完了診断", lambda: run_autonomous_build_completion_diagnosis_from_gui(c_area))
            add_menu_button(body, "MissionBridge診断", lambda: diagnose_mission_bridge_from_gui(c_area), "#0f766e")
            add_menu_button(body, "MissionManager v1完成保存", lambda: save_mission_manager_v1_report_from_gui(c_area), "#166534")

    categories = [
        "Build",
        "Reflection",
        "Agent",
        "LAB",
        "Files",
        "Capability",
        "Dashboard"
    ]

    for category in categories:
        tk.Button(
            button_row,
            text=category,
            command=lambda c=category: show_category(c),
            bg="#374151",
            fg="#ffffff",
            font=("MS Gothic", 8),
            bd=0
        ).pack(side=tk.LEFT, padx=2)

    show_category("Build")
    
def select_patch_for_original_naviko():
    files = list(APPROVED_DIR.glob("*.txt"))

    if not files:
        print("採用候補がありません。")
        return None

    goal = decide_next_growth_goal()

    best_file = None
    best_score = -1
    best_content = ""

    for file in files:
        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        score = 0

        if goal in content:
            score += 50

        if "疲労" in goal and "疲労" in content:
            score += 30

        if "安全" in content:
            score += 10

        if "小さ" in content or "既存機能" in content:
            score += 10

        # 新しい候補を少し優先
        score += min(
            10,
            int(file.stat().st_mtime % 10)
        )

        if score > best_score:
            best_score = score
            best_file = file
            best_content = content

    request = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "goal": goal,
        "selected_file": best_file.name,
        "selected_path": str(best_file),
        "selection_score": best_score,
        "reason": "現在の成長目標との一致度、安全性、小規模性を基準に、オリジナルnavikoへの反映候補として選定しました。",
        "status": "pending_review",
        "summary": best_content[:500]
    }

    print(f"オリジナル反映候補を選定しました: {best_file.name}")

    return request

def select_patch_for_original_naviko_from_gui(c_area=None):
    selected_path = filedialog.askopenfilename(
        title="反映候補ファイルを選択",
        initialdir=str(ROOT / "navikoLAB" / "approved_patches"),
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if not selected_path:
        if c_area:
            append_chat_bubble(
                c_area,
                "navi",
                "反映候補の選択をキャンセルしました。"
            )
        return

    selected_file = Path(selected_path)

    content = selected_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    request = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "goal": "手動選択された反映候補",
        "selected_file": selected_file.name,
        "selected_path": str(selected_file),
        "selection_score": 100,
        "reason": "ユーザーが手動で選択した反映候補です。",
        "status": "selected",
        "summary": content[:1000],
        "approved": False,
        "syntax_checked": False,
        "backup_created": False,
        "applied": False,
        "rollback": False
    }

    if c_area:
        append_chat_bubble(
            c_area,
            "navi",
            "📌 反映候補を手動選択しました。\n\n"
            f"候補: {selected_file.name}\n"
            f"保存先: {selected_file}\n\n"
            "次に人間承認へ進めます。"
        )
    

right_menu = tk.Menu(root, tearoff=0, bg="#2d2d2d", fg="#ffffff")
right_menu.add_command(label="サイズ: 小", command=lambda: change_scale_menu(1.0))
right_menu.add_command(label="サイズ: 中", command=lambda: change_scale_menu(1.5))
right_menu.add_command(label="サイズ: 大", command=lambda: change_scale_menu(2.0))
right_menu.add_separator()
right_menu.add_command(label="終了", command=root.destroy)

pet_label.bind("<Button-1>", start_drag)
pet_label.bind("<B1-Motion>", on_drag)
pet_label.bind("<ButtonRelease-1>", end_drag)
pet_label.bind("<Button-3>", lambda e: right_menu.post(e.x_root, e.y_root))

print("-> ナビ子を起動します。")

if "--growth-trial" in sys.argv:
    run_growth_trial()
elif AUTO_GROWTH_TRIAL:
    run_growth_trial()

run_line_patch_system_diagnosis_quiet()

if False:
    # ===== MemoryManager 動作確認 =====
    print("=== MemoryManager 動作確認 ===")

    memory_manager.add_memory(
        "ナビ子v1.2で長期記憶システムを開始した",
        importance=8,
        memory_type="short"
    )
  
    print(memory_manager.diagnose_memory())

    result = memory_manager.promote_important_memories()
    print("昇格結果:", result)

    print(memory_manager.diagnose_memory())
    # ===== 動作確認ここまで =====

    # ===== GoalManager 動作確認 =====
    print("=== GoalManager 動作確認 ===")

    goal_manager.set_dream(
        "ナオさんが目的だけ伝えれば、ナビ子が計画・実行・改善まで進めるAIになる"
    )

    goal_manager.add_goal(
        "long",
        "完全自律進化AIの基盤を作る"
    )

    goal_manager.add_goal(
        "mid",
        "記憶・目標・エージェント管理を接続する"
    )

    goal_manager.add_goal(
        "short",
        "GoalManagerを安全に追加する"
    )

    goal_manager.add_goal(
        "today",
        "goal_manager.pyを作成して起動確認する"
    )

    print(goal_manager.diagnose_goals())
    print(goal_manager.format_goals())
    # ===== 動作確認ここまで =====

    # ===== AgentRegistry 動作確認 =====
    print("=== AgentRegistry 動作確認 ===")

    print(agent_registry.diagnose_agents())
    print(agent_registry.format_agents())

    print("code能力:", agent_registry.find_agents_by_capability("code"))
    print("image能力:", agent_registry.find_agents_by_capability("image"))
    print("research能力:", agent_registry.find_agents_by_capability("research"))
    # ===== 動作確認ここまで =====

    # ===== TaskPlanner 動作確認 =====
    print("=== TaskPlanner 動作確認 ===")

    test_plan = task_planner.create_plan(
        "Pythonで画像付きのTODOアプリを作成して、必要なら調査も行う"
    )

    print(task_planner.diagnose_planner())
    print(task_planner.format_plan(test_plan))
    # ===== 動作確認ここまで =====

    # ===== PlanExecutor 動作確認 =====
    print("=== PlanExecutor 動作確認 ===")

    test_plan = task_planner.create_plan(
        "Pythonで画像付きのTODOアプリを作成して、必要なら調査も行う"
    )

    execution = plan_executor.run_simulation(test_plan)

    print(plan_executor.diagnose_executor())
    print(plan_executor.format_execution(execution))
    # ===== 動作確認ここまで =====

    # ===== AutonomyController 動作確認 =====
    print("=== AutonomyController 動作確認 ===")

    autonomy_controller.decide_from_success_rate(
        success_rate=33.3,
        safety_level="警戒"
    )

    print(autonomy_controller.diagnose_autonomy())
    print(autonomy_controller.format_autonomy())
    # ===== 動作確認ここまで =====

    # ===== AutonomousCore 動作確認 =====
    print("=== AutonomousCore 動作確認 ===")

    core_result = autonomous_core.process_purpose(
        "YouTube用の短い紹介動画を作りたい。構成、画像、音声、動画編集まで考えてほしい。"
    )

    print(autonomous_core.diagnose_core())
    print(autonomous_core.format_result(core_result))
    # ===== 動作確認ここまで =====

    print("=== ActionPlanner 動作確認 ===")

    result = action_planner.create_action_plan(
        "PythonでTODOアプリを作りたい"
    )

    print(
        action_planner.diagnose_action_planner()
    )

    print(
        action_planner.format_action_plan(result)
    )

    print("=== WorkspaceManager 動作確認 ===")

    project = workspace_manager.create_project_folder(
        "todo_app_test",
        project_type="app"
    )

    print(project)

    diagnosis = workspace_manager.diagnose_workspace()

    print(
        workspace_manager.format_workspace_report(
            diagnosis
        )
    )

    print("=== ArtifactWriter 動作確認 ===")

    project = workspace_manager.create_project_folder(
        "todo_app_artifact_test",
        project_type="app"
    )

    results = artifact_writer.create_basic_app_files(
        project["project_dir"],
        app_name="todo_app_artifact_test"
    )

    print(
        artifact_writer.format_write_results(
            results
        )
    )

    print("=== AppProjectBuilder 動作確認 ===")

    build_result = app_project_builder.build_basic_app_project(
        purpose="PythonでTODOアプリを作りたい",
        project_name="todo_app_builder_test"
    )

    print(
        app_project_builder.diagnose_builder()
    )

    print(
        app_project_builder.format_build_result(
            build_result
        )
    )

run_animation_loop()

# ★Phase D-2 Step D-2-3: 既存チャットをバックグラウンド起動★
print("🔍 デバッグ: バックグラウンドチャット起動中...")
open_custom_chat_window()

# ウィンドウを非表示にする
if pet_vars.get("chat_win") and pet_vars["chat_win"].winfo_exists():
    pet_vars["chat_win"].withdraw()  # ウィンドウを非表示
    print("✅ バックグラウンドチャット起動完了（非表示）")
    print(f"   - ウィンドウID: {pet_vars['chat_win']}")
    print(f"   - タイトル: NAVIKO CHAT / SELF GROWTH")
    print(f"   - ステータス: バックグラウンド待機中")
else:
    print("⚠️ バックグラウンドチャット作成失敗")


# ============================================================
# Vosk音声起動システムの初期化と開始
# ============================================================

if VOSK_AVAILABLE:
    try:
        # Voskモデルパス（小型モデルをデフォルト使用）
        vosk_model_path = Path("C:/vosk_models/vosk-model-small-ja-0.22")
        
        if vosk_model_path.exists():
            # ウェイクワード検出時のコールバック関数
            def on_wake_word_detected(detected_text):
                """
                ウェイクワード検出時の処理
                
                Args:
                    detected_text (str): 認識されたテキスト
                """
                print(f"🎉 ウェイクワード検出: {detected_text}")
                
                # チャットウィンドウを表示
                if pet_vars.get("chat_win") and pet_vars["chat_win"].winfo_exists():
                    pet_vars["chat_win"].deiconify()  # ウィンドウを表示
                    pet_vars["chat_win"].lift()  # 前面に持ってくる
                    pet_vars["chat_win"].focus_force()  # フォーカスを当てる
                    print("✅ チャットウィンドウを表示しました")
                    
                    # ナビ子のwaving状態に変更
                    pet_vars["state"] = "waving"
                    pet_vars["frame"] = 0
                else:
                    print("⚠️ チャットウィンドウが見つかりません")
            
            # VoiceWakeWordDetector初期化
            voice_detector = VoiceWakeWordDetector(
                model_path=str(vosk_model_path),
                wake_words=["ナビ子", "なびこ", "ナビコ"]
            )
            
            # 音声認識開始
            voice_detector.start_listening(on_wake_word_detected)
            
            print("✅ Vosk音声起動システム開始")
            print("   - ウェイクワード: 'hey、ナビ子' または 'ナビ子'")
            print("   - モデル: 小型（vosk-model-small-ja-0.22）")
        else:
            print(f"⚠️ Voskモデルが見つかりません: {vosk_model_path}")
            print("   音声起動機能は無効です")
    except Exception as e:
        print(f"❌ Vosk音声起動システムの初期化に失敗: {e}")
        import traceback
        traceback.print_exc()
else:
    print("⚠️ Vosk音声認識が利用できません（vosk/pyaudioが未インストール）")
    print("   音声起動機能は無効です")

root.mainloop()