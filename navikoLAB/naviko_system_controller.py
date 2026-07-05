#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NavikoSystemController - Naviko統合管理システム
Phase 3-A: Phase 1・2モジュールの統一管理とセッション制御

このモジュールはNavikoシステム全体を統括し、以下の責務を担う：
1. Phase 1・2モジュールの統一初期化・管理
2. セッション開始時の自動初期化
3. エラー検出時の自動System 3起動
4. システム全体の健全性監視
5. 処理履歴の統合管理

APIキー管理：
- 環境変数参照のみ（os.environ.get('GROQ_API_KEY')）
- ハードコード厳禁（セキュリティリスク）
"""

import os
import sys
import json
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Phase 1・2モジュールのインポート
try:
    from meta_cognition_engine import MetaCognitionEngine
    from problem_pattern_learner import ProblemPatternLearner
    from core_orchestrator import NavikoCoreOrchestrator
    from auto_recovery_engine import AutoRecoveryEngine
    from databricks_safety_checker import DatabricksSafetyChecker
except ImportError as e:
    print(f"⚠️ モジュールインポートエラー: {e}")
    print("注意: navikoLABディレクトリ内で実行してください")


class NavikoSystemController:
    """
    Naviko統合管理システム
    
    Phase 1・2の全モジュールを統合管理し、システム全体の
    健全性とエラーハンドリングを担当する。
    """
    
    def __init__(self, lab_dir: str = "/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB"):
        """
        コントローラー初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        self.lab_dir = Path(lab_dir)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_start_time = datetime.now()
        
        # 環境変数からAPIキーを取得（ハードコード厳禁）
        self.api_key = os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            print("⚠️ 警告: GROQ_API_KEYが設定されていません")
            print("環境変数を設定してください: os.environ['GROQ_API_KEY'] = 'your_key'")
        
        # Phase 1・2モジュールのインスタンス
        self.meta_engine: Optional[MetaCognitionEngine] = None
        self.pattern_learner: Optional[ProblemPatternLearner] = None
        self.core_orchestrator: Optional[NavikoCoreOrchestrator] = None
        self.recovery_engine: Optional[AutoRecoveryEngine] = None
        self.safety_checker: Optional[DatabricksSafetyChecker] = None
        
        # システム状態
        self.system_status = {
            "initialized": False,
            "modules_loaded": [],
            "modules_failed": [],
            "last_error": None,
            "error_count": 0,
            "auto_recovery_count": 0
        }
        
        # 処理履歴
        self.execution_history = []
        self.history_file = self.lab_dir / "system_controller_history.json"
        
        print(f"✅ NavikoSystemController初期化完了")
        print(f"   セッションID: {self.session_id}")
        print(f"   LABディレクトリ: {self.lab_dir}")
    
    
    def initialize_system(self) -> Dict[str, Any]:
        """
        システム全体の初期化
        
        Phase 1・2の全モジュールを初期化し、統合管理を開始する。
        
        Returns:
            初期化結果
        """
        print("\n🚀 Navikoシステム初期化開始...")
        
        initialization_result = {
            "success": True,
            "session_id": self.session_id,
            "modules": {},
            "errors": []
        }
        
        # Phase 1: メタ認知基盤
        print("\n📊 Phase 1モジュール初期化...")
        
        # 1-A: MetaCognitionEngine
        try:
            self.meta_engine = MetaCognitionEngine(str(self.lab_dir))
            self.system_status["modules_loaded"].append("MetaCognitionEngine")
            initialization_result["modules"]["MetaCognitionEngine"] = "✅ 成功"
            print("  ✅ MetaCognitionEngine: OK")
        except Exception as e:
            self.system_status["modules_failed"].append("MetaCognitionEngine")
            initialization_result["modules"]["MetaCognitionEngine"] = f"❌ 失敗: {str(e)}"
            initialization_result["errors"].append(str(e))
            print(f"  ❌ MetaCognitionEngine: {e}")
        
        # 1-B: ProblemPatternLearner
        try:
            self.pattern_learner = ProblemPatternLearner(str(self.lab_dir))
            self.system_status["modules_loaded"].append("ProblemPatternLearner")
            initialization_result["modules"]["ProblemPatternLearner"] = "✅ 成功"
            print("  ✅ ProblemPatternLearner: OK")
        except Exception as e:
            self.system_status["modules_failed"].append("ProblemPatternLearner")
            initialization_result["modules"]["ProblemPatternLearner"] = f"❌ 失敗: {str(e)}"
            initialization_result["errors"].append(str(e))
            print(f"  ❌ ProblemPatternLearner: {e}")
        
        # 1-C: NavikoCoreOrchestrator
        try:
            self.core_orchestrator = NavikoCoreOrchestrator(str(self.lab_dir))
            self.system_status["modules_loaded"].append("NavikoCoreOrchestrator")
            initialization_result["modules"]["NavikoCoreOrchestrator"] = "✅ 成功"
            print("  ✅ NavikoCoreOrchestrator: OK")
        except Exception as e:
            self.system_status["modules_failed"].append("NavikoCoreOrchestrator")
            initialization_result["modules"]["NavikoCoreOrchestrator"] = f"❌ 失敗: {str(e)}"
            initialization_result["errors"].append(str(e))
            print(f"  ❌ NavikoCoreOrchestrator: {e}")
        
        # Phase 2: 自動対処層
        print("\n🔧 Phase 2モジュール初期化...")
        
        # 2-A: AutoRecoveryEngine
        try:
            self.recovery_engine = AutoRecoveryEngine(str(self.lab_dir))
            self.system_status["modules_loaded"].append("AutoRecoveryEngine")
            initialization_result["modules"]["AutoRecoveryEngine"] = "✅ 成功"
            print("  ✅ AutoRecoveryEngine: OK")
        except Exception as e:
            self.system_status["modules_failed"].append("AutoRecoveryEngine")
            initialization_result["modules"]["AutoRecoveryEngine"] = f"❌ 失敗: {str(e)}"
            initialization_result["errors"].append(str(e))
            print(f"  ❌ AutoRecoveryEngine: {e}")
        
        # 2-B: DatabricksSafetyChecker
        try:
            self.safety_checker = DatabricksSafetyChecker(str(self.lab_dir))
            self.system_status["modules_loaded"].append("DatabricksSafetyChecker")
            initialization_result["modules"]["DatabricksSafetyChecker"] = "✅ 成功"
            print("  ✅ DatabricksSafetyChecker: OK")
        except Exception as e:
            self.system_status["modules_failed"].append("DatabricksSafetyChecker")
            initialization_result["modules"]["DatabricksSafetyChecker"] = f"❌ 失敗: {str(e)}"
            initialization_result["errors"].append(str(e))
            print(f"  ❌ DatabricksSafetyChecker: {e}")
        
        # 初期化完了判定
        if len(self.system_status["modules_failed"]) == 0:
            self.system_status["initialized"] = True
            print(f"\n✅ システム初期化完了！ 全{len(self.system_status['modules_loaded'])}モジュール正常")
        else:
            initialization_result["success"] = False
            print(f"\n⚠️ システム初期化完了（一部失敗）")
            print(f"   成功: {len(self.system_status['modules_loaded'])}モジュール")
            print(f"   失敗: {len(self.system_status['modules_failed'])}モジュール")
        
        # 履歴に記録
        self._record_execution("system_initialization", initialization_result)
        
        return initialization_result
    
    
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        エラー発生時の統合処理
        
        1. メタ認知エンジンで診断
        2. 自動リカバリーエンジンで対処
        3. パターン学習器で学習
        
        Args:
            error: 発生したエラー
            context: エラー発生時のコンテキスト
        
        Returns:
            処理結果
        """
        self.system_status["error_count"] += 1
        self.system_status["last_error"] = str(error)
        
        print(f"\n⚠️ エラー検出: {error}")
        print(f"   コンテキスト: {context}")
        
        result = {
            "error": str(error),
            "context": context,
            "diagnosis": None,
            "recovery_attempt": None,
            "pattern_learned": False,
            "success": False
        }
        
        # Step 1: メタ認知エンジンで診断
        if self.meta_engine:
            try:
                print("\n🔍 Phase 1: メタ認知診断...")
                diagnosis = self.meta_engine.diagnose_system()
                result["diagnosis"] = diagnosis
                print(f"  診断結果: {diagnosis.get('overall_status', 'N/A')}")
            except Exception as e:
                print(f"  ❌ 診断失敗: {e}")
        
        # Step 2: 自動リカバリー試行
        if self.recovery_engine:
            try:
                print("\n🔧 Phase 2: 自動リカバリー試行...")
                recovery_result = self.recovery_engine.attempt_recovery(
                    error_type=type(error).__name__,
                    error_message=str(error),
                    context=context
                )
                result["recovery_attempt"] = recovery_result
                
                if recovery_result.get("success"):
                    self.system_status["auto_recovery_count"] += 1
                    result["success"] = True
                    print(f"  ✅ リカバリー成功: {recovery_result.get('action_taken')}")
                else:
                    print(f"  ❌ リカバリー失敗: {recovery_result.get('message')}")
            except Exception as e:
                print(f"  ❌ リカバリー試行中にエラー: {e}")
        
        # Step 3: パターン学習
        if self.pattern_learner:
            try:
                print("\n📚 Phase 3: パターン学習...")
                self.pattern_learner.learn_from_problem(
                    problem_type=type(error).__name__,
                    description=str(error),
                    context=context,
                    solution=result.get("recovery_attempt", {}).get("action_taken", ""),
                    success=result["success"]
                )
                result["pattern_learned"] = True
                print("  ✅ パターン学習完了")
            except Exception as e:
                print(f"  ❌ パターン学習失敗: {e}")
        
        # 履歴に記録
        self._record_execution("error_handling", result)
        
        return result
    
    
    def run_safety_check(self) -> Dict[str, Any]:
        """
        作業前の安全性チェック
        
        DatabricksSafetyCheckerを使用して、作業開始前の
        環境チェックを実行する。
        
        Returns:
            チェック結果
        """
        if not self.safety_checker:
            return {
                "success": False,
                "message": "DatabricksSafetyCheckerが初期化されていません"
            }
        
        print("\n🔒 作業前安全性チェック...")
        
        try:
            check_result = self.safety_checker.run_pre_work_check()
            
            if check_result.get("safe_to_proceed"):
                print("  ✅ 安全性チェック: 問題なし")
            else:
                print("  ⚠️ 安全性チェック: 問題検出")
                for issue in check_result.get("issues", []):
                    print(f"     - {issue}")
            
            self._record_execution("safety_check", check_result)
            return check_result
            
        except Exception as e:
            print(f"  ❌ チェック失敗: {e}")
            return {
                "success": False,
                "safe_to_proceed": False,
                "message": str(e)
            }
    
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        システム状態の取得
        
        Returns:
            システム状態情報
        """
        uptime = (datetime.now() - self.session_start_time).total_seconds()
        
        return {
            "session_id": self.session_id,
            "uptime_seconds": uptime,
            "uptime_human": f"{int(uptime // 60)}分{int(uptime % 60)}秒",
            "status": self.system_status.copy(),
            "modules": {
                "meta_engine": self.meta_engine is not None,
                "pattern_learner": self.pattern_learner is not None,
                "core_orchestrator": self.core_orchestrator is not None,
                "recovery_engine": self.recovery_engine is not None,
                "safety_checker": self.safety_checker is not None
            },
            "api_key_configured": bool(self.api_key)
        }
    
    
    def _record_execution(self, operation: str, result: Any):
        """
        実行履歴を記録
        
        Args:
            operation: 操作名
            result: 実行結果
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "operation": operation,
            "result": result
        }
        
        self.execution_history.append(record)
        
        # ファイルに保存（最新100件のみ）
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(record)
            history = history[-100:]  # 最新100件のみ保持
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 履歴保存失敗: {e}")
    
    
    def shutdown(self):
        """システムシャットダウン"""
        print(f"\n🛑 NavikoSystemController シャットダウン...")
        print(f"   セッション時間: {(datetime.now() - self.session_start_time).total_seconds():.1f}秒")
        print(f"   処理回数: {len(self.execution_history)}")
        print(f"   エラー回数: {self.system_status['error_count']}")
        print(f"   自動リカバリー成功: {self.system_status['auto_recovery_count']}")
        print(f"✅ シャットダウン完了")


# テスト用コード
if __name__ == "__main__":
    # コントローラー初期化
    controller = NavikoSystemController()
    
    # システム初期化
    init_result = controller.initialize_system()
    print(f"\n初期化結果: {json.dumps(init_result, ensure_ascii=False, indent=2)}")
    
    # システム状態確認
    status = controller.get_system_status()
    print(f"\nシステム状態: {json.dumps(status, ensure_ascii=False, indent=2)}")
    
    # 安全性チェック
    safety_result = controller.run_safety_check()
    print(f"\n安全性チェック: {json.dumps(safety_result, ensure_ascii=False, indent=2)}")
