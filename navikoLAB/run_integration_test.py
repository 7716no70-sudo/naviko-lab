#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naviko System 実運用テスト統合スクリプト

Phase 1-3の全モジュールを統合テストします。
"""

import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB")

# テスト結果記録
test_results = []

def log_test(test_name, status, details=""):
    """テスト結果を記録"""
    result = {
        "test_name": test_name,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    test_results.append(result)
    
    status_icon = "✅" if status == "passed" else "❌" if status == "failed" else "⚠️"
    print(f"{status_icon} {test_name}: {status}")
    if details:
        print(f"   詳細: {details}")

def run_phase1_tests():
    """Phase 1: System 3コア基盤のテスト"""
    print("\n" + "="*70)
    print("  Phase 1: System 3コア基盤テスト")
    print("="*70)
    
    # MetaCognitionEngine テスト
    try:
        from meta_cognition_engine import MetaCognitionEngine
        engine = MetaCognitionEngine()
        diagnosis = engine.diagnose_system()
        
        if diagnosis:
            log_test("MetaCognitionEngine 自己診断", "passed", 
                    f"システム状態: {len(diagnosis.get('issues', []))}個の問題検出")
        else:
            log_test("MetaCognitionEngine 自己診断", "warning", "診断結果が空")
    except Exception as e:
        log_test("MetaCognitionEngine 自己診断", "failed", str(e))
    
    # ProblemPatternLearner テスト
    try:
        from problem_pattern_learner import ProblemPatternLearner
        learner = ProblemPatternLearner()
        
        # ダミー問題を記録
        test_problem = {
            "problem_type": "test_api_error",
            "context": {"test": "実運用テスト"},
            "solution": {"action": "テスト対処"}
        }
        pattern_id = learner.record_problem(**test_problem)
        
        if pattern_id:
            log_test("ProblemPatternLearner 問題記録", "passed", 
                    f"パターンID: {pattern_id}")
        else:
            log_test("ProblemPatternLearner 問題記録", "failed", "記録失敗")
    except Exception as e:
        log_test("ProblemPatternLearner 問題記録", "failed", str(e))
    
    # NavikoCoreOrchestrator テスト
    try:
        from core_orchestrator import NavikoCoreOrchestrator
        orchestrator = NavikoCoreOrchestrator()
        
        # 簡単なタスク実行
        result = orchestrator.process_task({
            "task_type": "simple",
            "description": "テストタスク"
        })
        
        if result:
            log_test("NavikoCoreOrchestrator タスク処理", "passed",
                    f"実行モード: {result.get('execution_mode', 'unknown')}")
        else:
            log_test("NavikoCoreOrchestrator タスク処理", "warning", "結果なし")
    except Exception as e:
        log_test("NavikoCoreOrchestrator タスク処理", "failed", str(e))

def run_phase2_tests():
    """Phase 2: 自動対処層のテスト"""
    print("\n" + "="*70)
    print("  Phase 2: 自動対処層テスト")
    print("="*70)
    
    # AutoRecoveryEngine テスト
    try:
        from auto_recovery_engine import AutoRecoveryEngine
        recovery = AutoRecoveryEngine()
        
        # ダミーエラーで対処機能テスト
        error_info = {
            "error_type": "test_error",
            "error_message": "テスト用エラー",
            "context": {}
        }
        recovery_plan = recovery.detect_and_recover(error_info)
        
        if recovery_plan:
            log_test("AutoRecoveryEngine エラー検出", "passed",
                    f"対処プラン: {recovery_plan.get('recovery_type', 'unknown')}")
        else:
            log_test("AutoRecoveryEngine エラー検出", "warning", "対処プランなし")
    except Exception as e:
        log_test("AutoRecoveryEngine エラー検出", "failed", str(e))
    
    # DatabricksSafetyChecker テスト
    try:
        from databricks_safety_checker import DatabricksSafetyChecker
        checker = DatabricksSafetyChecker()
        
        # 安全性チェック実行
        safety_result = checker.check_safety_before_operation("test_operation")
        
        if safety_result:
            log_test("DatabricksSafetyChecker 安全性チェック", "passed",
                    f"安全性: {safety_result.get('is_safe', False)}")
        else:
            log_test("DatabricksSafetyChecker 安全性チェック", "warning", "チェック結果なし")
    except Exception as e:
        log_test("DatabricksSafetyChecker 安全性チェック", "failed", str(e))

def run_phase3_tests():
    """Phase 3: 高度な学習機能のテスト"""
    print("\n" + "="*70)
    print("  Phase 3: 高度な学習機能テスト")
    print("="*70)
    
    # AdvancedLearningAnalyzer テスト
    try:
        from advanced_learning_analyzer import AdvancedLearningAnalyzer
        analyzer = AdvancedLearningAnalyzer()
        
        diagnosis = analyzer.diagnose_learning_system()
        log_test("AdvancedLearningAnalyzer システム診断", "passed",
                f"ヘルススコア: {diagnosis['health_score']:.2f}")
    except Exception as e:
        log_test("AdvancedLearningAnalyzer システム診断", "failed", str(e))
    
    # SelfEvolutionEngine テスト
    try:
        from self_evolution_engine import SelfEvolutionEngine
        engine = SelfEvolutionEngine()
        
        diagnosis = engine.diagnose_evolution_system()
        log_test("SelfEvolutionEngine 進化診断", "passed",
                f"ステータス: {diagnosis['status']}")
    except Exception as e:
        log_test("SelfEvolutionEngine 進化診断", "failed", str(e))
    
    # KnowledgeGraphBuilder テスト
    try:
        from knowledge_graph_builder import KnowledgeGraphBuilder
        builder = KnowledgeGraphBuilder()
        
        result = builder.build_knowledge_graph()
        log_test("KnowledgeGraphBuilder グラフ構築", "passed",
                f"ノード数: {result['node_count']}")
    except Exception as e:
        log_test("KnowledgeGraphBuilder グラフ構築", "failed", str(e))

def print_summary():
    """テスト結果サマリー"""
    print("\n" + "="*70)
    print("  テスト結果サマリー")
    print("="*70)
    
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    warning = sum(1 for r in test_results if r['status'] == 'warning')
    total = len(test_results)
    
    print(f"\n総テスト数: {total}")
    print(f"✅ 成功: {passed}")
    print(f"❌ 失敗: {failed}")
    print(f"⚠️ 警告: {warning}")
    
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"\n成功率: {success_rate:.1f}%")
    
    return success_rate if total > 0 else 0

if __name__ == "__main__":
    print("="*70)
    print("  Naviko System 実運用テスト")
    print("  実行日時:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)
    
    run_phase1_tests()
    run_phase2_tests()
    run_phase3_tests()
    
    success_rate = print_summary()
    
    print("\n" + "="*70)
    if success_rate >= 80:
        print("  🎉 テスト完了: システムは実運用準備が整っています")
    elif success_rate >= 60:
        print("  ⚠️ テスト完了: 一部問題がありますが基本動作は可能です")
    else:
        print("  ❌ テスト完了: 重要な問題が検出されました")
    print("="*70)
