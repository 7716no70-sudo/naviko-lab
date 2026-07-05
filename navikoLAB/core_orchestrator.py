#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NavikoCoreOrchestrator - Navikoの中核統合管理システム

このモジュールはNavikoの「System 3」統合層として、以下を提供します：
- 全モジュールの統合管理
- System 1（直感的処理）/ System 2（論理的処理）/ System 3（メタ認知）の切り替え
- モジュール間の連携調整
- 最適な処理フローの選択

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum


class ThinkingMode(Enum):
    """
    思考モードの定義
    """
    SYSTEM_1 = "system_1"  # 直感的・高速・自動的
    SYSTEM_2 = "system_2"  # 論理的・熟考型・意識的
    SYSTEM_3 = "system_3"  # メタ認知・自己改善


class NavikoCoreOrchestrator:
    """
    Navikoコアオーケストレーター
    
    Navikoの全モジュールを統合管理し、System 1/2/3を切り替えながら
    最適な処理を実行する中核システム。
    """
    
    def __init__(self, lab_dir: str = None):
        """
        NavikoCoreOrchestratorの初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        # 基本パス設定
        if lab_dir is None:
            lab_dir = os.path.join(os.path.expanduser("~"), "navikoLAB")
            if not os.path.exists(lab_dir):
                lab_dir = "/Workspace/Users/7716no70@gmail.com/navikoLAB"
        
        self.lab_dir = Path(lab_dir)
        self.reports_dir = self.lab_dir / "reports" / "orchestrator"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 現在の思考モード
        self.current_mode = ThinkingMode.SYSTEM_2  # デフォルトは論理的モード
        
        # System 3モジュールの初期化（遅延読み込み）
        self.meta_cognition_engine = None
        self.problem_pattern_learner = None
        
        # モジュールレジストリ
        self.modules: Dict[str, Any] = {}
        
        # 処理履歴
        self.processing_history: List[Dict] = []
        
        # モード切り替えルール
        self.mode_switch_rules = self._initialize_mode_switch_rules()
        
    def _initialize_mode_switch_rules(self) -> Dict[str, Dict]:
        """
        モード切り替えルールの初期化
        
        Returns:
            ルール辞書
        """
        return {
            "simple_query": {
                "mode": ThinkingMode.SYSTEM_1,
                "conditions": ["単純なクエリ", "高速処理が必要"],
                "examples": ["ファイル検索", "簡単な計算"]
            },
            "complex_analysis": {
                "mode": ThinkingMode.SYSTEM_2,
                "conditions": ["複雑な分析", "論理的思考が必要"],
                "examples": ["コード生成", "問題解決"]
            },
            "self_improvement": {
                "mode": ThinkingMode.SYSTEM_3,
                "conditions": ["エラー発生", "パフォーマンス改善", "パターン分析"],
                "examples": ["エラー診断", "最適化"]
            }
        }
    
    def register_module(self, name: str, module: Any):
        """
        モジュールを登録
        
        Args:
            name: モジュール名
            module: モジュールインスタンス
        """
        self.modules[name] = module
    
    def _ensure_system3_modules(self):
        """
        System 3モジュールの遅延読み込み
        """
        if self.meta_cognition_engine is None:
            try:
                from meta_cognition_engine import MetaCognitionEngine
                self.meta_cognition_engine = MetaCognitionEngine(self.lab_dir)
            except ImportError:
                print("⚠️ MetaCognitionEngineが読み込めません")
        
        if self.problem_pattern_learner is None:
            try:
                from problem_pattern_learner import ProblemPatternLearner
                self.problem_pattern_learner = ProblemPatternLearner(self.lab_dir)
            except ImportError:
                print("⚠️ ProblemPatternLearnerが読み込めません")
    
    def switch_mode(self, mode: ThinkingMode, reason: str = None) -> bool:
        """
        思考モードを切り替え
        
        Args:
            mode: 新しい思考モード
            reason: 切り替え理由
        
        Returns:
            切り替え成功か
        """
        old_mode = self.current_mode
        self.current_mode = mode
        
        # 履歴記録
        self.processing_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "mode_switch",
            "from": old_mode.value,
            "to": mode.value,
            "reason": reason
        })
        
        # System 3に切り替える場合はモジュールを読み込み
        if mode == ThinkingMode.SYSTEM_3:
            self._ensure_system3_modules()
        
        return True
    
    def decide_mode(self, task_type: str, context: Dict[str, Any] = None) -> ThinkingMode:
        """
        タスクタイプとコンテキストから最適なモードを決定
        
        Args:
            task_type: タスクのタイプ
            context: 追加のコンテキスト情報
        
        Returns:
            推奨される思考モード
        """
        context = context or {}
        
        # エラー発生時はSystem 3
        if context.get("error_occurred"):
            return ThinkingMode.SYSTEM_3
        
        # タスクタイプによる判定
        if task_type in ["diagnose", "analyze_pattern", "improve"]:
            return ThinkingMode.SYSTEM_3
        elif task_type in ["generate_code", "complex_query", "deep_search"]:
            return ThinkingMode.SYSTEM_2
        else:
            return ThinkingMode.SYSTEM_1
    
    def process(self, task_type: str, task_data: Dict[str, Any], 
                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        タスクを処理
        
        Args:
            task_type: タスクのタイプ
            task_data: タスクデータ
            context: 追加コンテキスト
        
        Returns:
            処理結果
        """
        context = context or {}
        
        # 1. 最適なモードを決定
        optimal_mode = self.decide_mode(task_type, context)
        
        # 2. モード切り替え
        if optimal_mode != self.current_mode:
            self.switch_mode(optimal_mode, f"Task type: {task_type}")
        
        # 3. モードに応じた処理
        result = self._execute_task(task_type, task_data, context)
        
        # 4. 処理履歴に記録
        self.processing_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "process_task",
            "task_type": task_type,
            "mode": self.current_mode.value,
            "success": result.get("success", False)
        })
        
        return result
    
    def _execute_task(self, task_type: str, task_data: Dict[str, Any], 
                     context: Dict[str, Any]) -> Dict[str, Any]:
        """
        タスクを実行
        
        Args:
            task_type: タスクのタイプ
            task_data: タスクデータ
            context: コンテキスト
        
        Returns:
            実行結果
        """
        result = {
            "success": False,
            "mode": self.current_mode.value,
            "task_type": task_type,
            "data": {}
        }
        
        try:
            if self.current_mode == ThinkingMode.SYSTEM_1:
                # System 1: 直感的・高速処理
                result = self._execute_system1_task(task_type, task_data, context)
            
            elif self.current_mode == ThinkingMode.SYSTEM_2:
                # System 2: 論理的・熟考型処理
                result = self._execute_system2_task(task_type, task_data, context)
            
            elif self.current_mode == ThinkingMode.SYSTEM_3:
                # System 3: メタ認知・自己改善
                result = self._execute_system3_task(task_type, task_data, context)
            
            result["success"] = True
        
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            
            # エラー発生時はSystem 3に切り替えて診断
            if self.current_mode != ThinkingMode.SYSTEM_3:
                self.switch_mode(ThinkingMode.SYSTEM_3, f"Error occurred: {str(e)}")
                
                # エラーを記録
                if self.problem_pattern_learner:
                    self.problem_pattern_learner.record_problem(
                        f"{task_type}_error",
                        {"task_type": task_type, "error": str(e)},
                        None,
                        False
                    )
        
        return result
    
    def _execute_system1_task(self, task_type: str, task_data: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """
        System 1タスクを実行（直感的・高速処理）
        
        Args:
            task_type: タスクのタイプ
            task_data: タスクデータ
            context: コンテキスト
        
        Returns:
            実行結果
        """
        # シンプルなテンプレートベースの処理
        return {
            "success": True,
            "mode": "system_1",
            "task_type": task_type,
            "data": {
                "message": "System 1: 高速処理完了",
                "processing_time": "< 1s"
            }
        }
    
    def _execute_system2_task(self, task_type: str, task_data: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """
        System 2タスクを実行（論理的・熟考型処理）
        
        Args:
            task_type: タスクのタイプ
            task_data: タスクデータ
            context: コンテキスト
        
        Returns:
            実行結果
        """
        # 論理的処理（LLM連携等）
        return {
            "success": True,
            "mode": "system_2",
            "task_type": task_type,
            "data": {
                "message": "System 2: 論理的処理完了",
                "processing_time": "1-5s"
            }
        }
    
    def _execute_system3_task(self, task_type: str, task_data: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """
        System 3タスクを実行（メタ認知・自己改善）
        
        Args:
            task_type: タスクのタイプ
            task_data: タスクデータ
            context: コンテキスト
        
        Returns:
            実行結果
        """
        result = {
            "success": True,
            "mode": "system_3",
            "task_type": task_type,
            "data": {}
        }
        
        # System 3モジュールの読み込み確認
        self._ensure_system3_modules()
        
        # タスクタイプに応じた処理
        if task_type == "diagnose":
            # システム診断
            if self.meta_cognition_engine:
                diagnosis = self.meta_cognition_engine.diagnose_system_state()
                result["data"] = diagnosis
            else:
                result["data"]["message"] = "MetaCognitionEngineが利用不可"
        
        elif task_type == "analyze_pattern":
            # パターン分析
            if self.problem_pattern_learner:
                analysis = self.problem_pattern_learner.analyze_patterns()
                result["data"] = analysis
            else:
                result["data"]["message"] = "ProblemPatternLearnerが利用不可"
        
        elif task_type == "improve":
            # 自己改善
            if self.meta_cognition_engine:
                evaluation = self.meta_cognition_engine.self_evaluate()
                result["data"] = evaluation
            else:
                result["data"]["message"] = "MetaCognitionEngineが利用不可"
        
        else:
            result["data"]["message"] = f"System 3: {task_type}処理完了"
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """
        現在のステータスを取得
        
        Returns:
            ステータス情報
        """
        return {
            "current_mode": self.current_mode.value,
            "registered_modules": list(self.modules.keys()),
            "system3_ready": {
                "meta_cognition": self.meta_cognition_engine is not None,
                "pattern_learner": self.problem_pattern_learner is not None
            },
            "processing_history_count": len(self.processing_history)
        }
    
    def get_summary(self) -> str:
        """
        オーケストレーターのサマリーを取得
        
        Returns:
            人間が読みやすい形式のサマリー
        """
        status = self.get_status()
        
        lines = []
        lines.append("=" * 60)
        lines.append("Naviko Core Orchestrator ステータス")
        lines.append("=" * 60)
        lines.append(f"現在のモード: {status['current_mode']}")
        lines.append("")
        
        lines.append("【登録モジュール】")
        if status['registered_modules']:
            for module in status['registered_modules']:
                lines.append(f"  ✅ {module}")
        else:
            lines.append("  (なし)")
        lines.append("")
        
        lines.append("【System 3状態】")
        lines.append(f"  MetaCognitionEngine: {'[✅ 準備完了]' if status['system3_ready']['meta_cognition'] else '[❌ 未読み込み]'}")
        lines.append(f"  ProblemPatternLearner: {'[✅ 準備完了]' if status['system3_ready']['pattern_learner'] else '[❌ 未読み込み]'}")
        lines.append("")
        
        lines.append(f"処理履歴: {status['processing_history_count']}件")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """
    メインテスト関数
    """
    print("NavikoCoreOrchestrator テスト開始")
    print("=" * 60)
    
    # オーケストレーター初期化
    orchestrator = NavikoCoreOrchestrator()
    
    # ステータス表示
    print("\n1. 初期ステータス")
    print(orchestrator.get_summary())
    
    # System 1タスク
    print("\n2. System 1タスク実行")
    result1 = orchestrator.process("simple_query", {"query": "test"})
    print(f"  ✅ {result1['data']['message']}")
    
    # System 2タスク
    print("\n3. System 2タスク実行")
    result2 = orchestrator.process("complex_query", {"query": "complex test"})
    print(f"  ✅ {result2['data']['message']}")
    
    # System 3タスク
    print("\n4. System 3タスク実行")
    result3 = orchestrator.process("diagnose", {})
    print(f"  ✅ System 3タスク完了")
    
    # 最終ステータス
    print("\n5. 最終ステータス")
    print(orchestrator.get_summary())
    
    print("\n" + "=" * 60)
    print("✅ NavikoCoreOrchestrator テスト完了")


if __name__ == "__main__":
    main()
