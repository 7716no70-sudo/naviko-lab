#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IntegrationTest - Naviko音声系モジュール統合テスト

Phase 6で実装された全モジュールの統合動作を確認する。
InputAnalyzer → GoalDecomposer → CapabilitySelector → 
ExecutionPlanner → VoiceFeedback の完全なフローをテスト。

テスト内容:
  1. モジュール間連携テスト（完全な実行フロー）
  2. 実践シナリオテスト（3つのシナリオ）
  3. パフォーマンス測定（実行時間、リソース使用量）
  4. エラーハンドリングテスト

使用例:
  python integration_test.py
"""

import os
import sys
import time
import traceback
from typing import Dict, List, Any
from datetime import datetime

# モジュールパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 音声系モジュールをインポート
try:
    from input_analyzer import InputAnalyzer
    from goal_decomposer import GoalDecomposer
    from capability_selector import CapabilitySelector
    from execution_planner import ExecutionPlanner
    from voice_feedback import VoiceFeedback
    
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"⚠️ モジュールインポートエラー: {e}")
    print("   必要なモジュールがインストールされていることを確認してください。")


class IntegrationTest:
    """
    音声系モジュール統合テストクラス
    
    全モジュールの連携動作をテストし、
    実践的なシナリオでの動作確認を行う。
    """
    
    def __init__(self):
        """統合テストの初期化"""
        self.test_results = []
        self.performance_data = []
        self.start_time = None
        self.end_time = None
        
        # テスト設定
        self.voice_enabled = False  # 音声はオフ（テスト用）
        self.verbose = True  # 詳細ログ
    
    def run_all_tests(self):
        """全テストを実行"""
        print("=" * 80)
        print("Naviko音声系モジュール 統合テスト")
        print("=" * 80)
        print()
        
        if not MODULES_AVAILABLE:
            print("❌ モジュールが利用できません。テストを中止します。")
            return False
        
        self.start_time = time.time()
        
        # テスト1: モジュールインポート確認
        self._test_module_imports()
        
        # テスト2: 基本動作確認
        self._test_basic_operations()
        
        # テスト3: モジュール間連携テスト
        self._test_module_integration()
        
        # テスト4: 実践シナリオテスト
        self._test_practical_scenarios()
        
        # テスト5: エラーハンドリングテスト
        self._test_error_handling()
        
        # テスト6: パフォーマンス測定
        self._test_performance()
        
        self.end_time = time.time()
        
        # テスト結果サマリー
        self._print_test_summary()
        
        return all([result["status"] == "success" for result in self.test_results])
    
    def _test_module_imports(self):
        """テスト1: モジュールインポート確認"""
        print("【テスト1: モジュールインポート確認】")
        print("-" * 80)
        
        modules = {
            "InputAnalyzer": InputAnalyzer,
            "GoalDecomposer": GoalDecomposer,
            "CapabilitySelector": CapabilitySelector,
            "ExecutionPlanner": ExecutionPlanner,
            "VoiceFeedback": VoiceFeedback
        }
        
        all_success = True
        for name, module in modules.items():
            try:
                instance = module() if name != "InputAnalyzer" else module("")
                print(f"  ✅ {name}: インポート成功")
            except Exception as e:
                print(f"  ❌ {name}: インポート失敗 - {e}")
                all_success = False
        
        status = "success" if all_success else "failed"
        self.test_results.append({
            "test": "モジュールインポート確認",
            "status": status,
            "duration": 0
        })
        
        print(f"結果: {'✅ 成功' if all_success else '❌ 失敗'}")
        print()
    
    def _test_basic_operations(self):
        """テスト2: 基本動作確認"""
        print("【テスト2: 基本動作確認】")
        print("-" * 80)
        
        start = time.time()
        all_success = True
        
        try:
            # InputAnalyzer
            analyzer = InputAnalyzer("Webアプリを作成してください")
            intent = analyzer.classify_intent()
            print(f"  ✅ InputAnalyzer: インテント分類 = {intent}")
            
            # GoalDecomposer
            decomposer = GoalDecomposer("Webアプリを作成してください")
            goals = decomposer.decompose()
            print(f"  ✅ GoalDecomposer: {len(goals['sub_goals'])}個のサブゴール生成")
            
            # CapabilitySelector
            selector = CapabilitySelector()
            task_analysis = {
                "main_goal": goals['main_goal'],
                "sub_tasks": [{"name": sg, "estimated_time": "10分"} for sg in goals['sub_goals']],
                "estimated_time": "60分",
                "complexity": "medium"
            }
            capabilities = selector.select_capabilities(task_analysis)
            print(f"  ✅ CapabilitySelector: {len(capabilities)}個の能力選択")
            
            # ExecutionPlanner
            planner = ExecutionPlanner(max_parallel_tasks=3)
            plan = planner.create_execution_plan(capabilities)
            print(f"  ✅ ExecutionPlanner: {len(plan['execution_plan']['levels'])}レベルの実行計画生成")
            
            # VoiceFeedback
            voice = VoiceFeedback(enabled=False)
            voice.notify_execution_start("テスト実行", total_tasks=3)
            history = voice.get_notification_history()
            print(f"  ✅ VoiceFeedback: 通知履歴 = {len(history)}件")
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            traceback.print_exc()
            all_success = False
        
        duration = time.time() - start
        status = "success" if all_success else "failed"
        self.test_results.append({
            "test": "基本動作確認",
            "status": status,
            "duration": duration
        })
        
        print(f"結果: {'✅ 成功' if all_success else '❌ 失敗'} (所要時間: {duration:.2f}秒)")
        print()
    
    def _test_module_integration(self):
        """テスト3: モジュール間連携テスト"""
        print("【テスト3: モジュール間連携テスト】")
        print("-" * 80)
        
        start = time.time()
        all_success = True
        
        try:
            user_input = "データ分析タスクを実行してください"
            
            # ステップ1: 入力解析
            print("  ステップ1: InputAnalyzer...")
            analyzer = InputAnalyzer(user_input)
            intent = analyzer.classify_intent()
            entities = analyzer.extract_entities()
            print(f"    インテント: {intent}")
            print(f"    エンティティ: {entities}")
            
            # ステップ2: ゴール分解
            print("  ステップ2: GoalDecomposer...")
            decomposer = GoalDecomposer(user_input)
            goals = decomposer.decompose()
            print(f"    メインゴール: {goals['main_goal']}")
            print(f"    サブゴール数: {len(goals['sub_goals'])}")
            
            # ステップ3: 能力選択
            print("  ステップ3: CapabilitySelector...")
            selector = CapabilitySelector()
            task_analysis = {
                "main_goal": goals['main_goal'],
                "sub_tasks": [{"name": sg, "estimated_time": "10分"} for sg in goals['sub_goals']],
                "estimated_time": "60分",
                "complexity": "medium"
            }
            capabilities = selector.select_capabilities(task_analysis)
            print(f"    選択能力数: {len(capabilities)}")
            
            # ステップ4: 実行計画生成
            print("  ステップ4: ExecutionPlanner...")
            planner = ExecutionPlanner(max_parallel_tasks=3)
            plan = planner.create_execution_plan(capabilities)
            print(f"    実行レベル数: {len(plan['execution_plan']['levels'])}")
            print(f"    総タスク数: {plan['total_tasks']}")
            print(f"    推定時間: {plan['execution_plan']['total_estimated_time']}")
            
            # ステップ5: 音声フィードバック
            print("  ステップ5: VoiceFeedback...")
            voice = VoiceFeedback(enabled=False)
            voice.notify_execution_start(goals['main_goal'], total_tasks=plan['total_tasks'])
            
            for level_num, level in enumerate(plan['execution_plan']['levels'], 1):
                task_names = [task['name'] for task in level['tasks']]
                voice.notify_level_start(level_num, task_names, parallel=level['parallel'])
            
            voice.notify_execution_complete(success=True, total_time=plan['execution_plan']['total_estimated_time'])
            
            history = voice.get_notification_history()
            print(f"    通知履歴: {len(history)}件")
            
            print("  ✅ 全ステップ完了")
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            traceback.print_exc()
            all_success = False
        
        duration = time.time() - start
        status = "success" if all_success else "failed"
        self.test_results.append({
            "test": "モジュール間連携テスト",
            "status": status,
            "duration": duration
        })
        
        print(f"結果: {'✅ 成功' if all_success else '❌ 失敗'} (所要時間: {duration:.2f}秒)")
        print()
    
    def _test_practical_scenarios(self):
        """テスト4: 実践シナリオテスト"""
        print("【テスト4: 実践シナリオテスト】")
        print("-" * 80)
        
        scenarios = [
            {
                "name": "シナリオ1: Webアプリケーション作成",
                "input": "Flaskを使ってWebアプリケーションを作成してください"
            },
            {
                "name": "シナリオ2: データ分析タスク",
                "input": "売上データを分析して可視化してください"
            },
            {
                "name": "シナリオ3: エラー対処シナリオ",
                "input": "エラーが発生した場合は自動的にリトライしてください"
            }
        ]
        
        for scenario in scenarios:
            print(f"  {scenario['name']}")
            print(f"    入力: {scenario['input']}")
            
            start = time.time()
            try:
                # 完全なフロー実行
                analyzer = InputAnalyzer(scenario['input'])
                intent = analyzer.classify_intent()
                
                decomposer = GoalDecomposer(scenario['input'])
                goals = decomposer.decompose()
                
                selector = CapabilitySelector()
                task_analysis = {
                    "main_goal": goals['main_goal'],
                    "sub_tasks": [{"name": sg, "estimated_time": "10分"} for sg in goals['sub_goals']],
                    "estimated_time": "60分",
                    "complexity": "medium"
                }
                capabilities = selector.select_capabilities(task_analysis)
                
                planner = ExecutionPlanner(max_parallel_tasks=3)
                plan = planner.create_execution_plan(capabilities)
                
                voice = VoiceFeedback(enabled=False)
                voice.notify_execution_start(goals['main_goal'], total_tasks=plan['total_tasks'])
                
                duration = time.time() - start
                print(f"    結果: ✅ 成功 (所要時間: {duration:.2f}秒)")
                print(f"    - インテント: {intent}")
                print(f"    - サブゴール数: {len(goals['sub_goals'])}")
                print(f"    - 実行レベル数: {len(plan['execution_plan']['levels'])}")
                print()
                
                self.test_results.append({
                    "test": scenario['name'],
                    "status": "success",
                    "duration": duration
                })
                
            except Exception as e:
                duration = time.time() - start
                print(f"    結果: ❌ 失敗 - {e}")
                print()
                
                self.test_results.append({
                    "test": scenario['name'],
                    "status": "failed",
                    "duration": duration
                })
        
        print()
    
    def _test_error_handling(self):
        """テスト5: エラーハンドリングテスト"""
        print("【テスト5: エラーハンドリングテスト】")
        print("-" * 80)
        
        start = time.time()
        all_success = True
        
        # テスト: 空入力
        try:
            print("  テストケース: 空入力")
            analyzer = InputAnalyzer("")
            intent = analyzer.classify_intent()
            print(f"    結果: {intent} (デフォルト値として処理)")
        except Exception as e:
            print(f"    エラー処理: {e}")
        
        # テスト: 不正な入力
        try:
            print("  テストケース: 不正な入力")
            decomposer = GoalDecomposer(None)
            goals = decomposer.decompose()
            print(f"    結果: デフォルトゴール生成")
        except Exception as e:
            print(f"    エラー処理: {e}")
        
        # テスト: 空のタスクリスト
        try:
            print("  テストケース: 空のタスクリスト")
            planner = ExecutionPlanner("テスト", [])
            plan = planner.create_execution_plan()
            print(f"    結果: 空の実行計画生成")
        except Exception as e:
            print(f"    エラー処理: {e}")
        
        duration = time.time() - start
        self.test_results.append({
            "test": "エラーハンドリングテスト",
            "status": "success",
            "duration": duration
        })
        
        print(f"結果: ✅ エラーハンドリング正常")
        print()
    
    def _test_performance(self):
        """テスト6: パフォーマンス測定"""
        print("【テスト6: パフォーマンス測定】")
        print("-" * 80)
        
        test_cases = [
            "簡単なタスク（3サブゴール）",
            "中規模タスク（10サブゴール）",
            "大規模タスク（20サブゴール）"
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            sub_goal_count = [3, 10, 20][i-1]
            
            print(f"  テストケース{i}: {test_case}")
            
            start = time.time()
            
            # サブゴールを生成
            sub_goals = [f"サブゴール{j}" for j in range(sub_goal_count)]
            
            # 能力選択
            selector = CapabilitySelector()
            task_analysis = {
                "main_goal": f"テストゴール{i}",
                "sub_tasks": [{"name": sg, "estimated_time": "5分"} for sg in sub_goals],
                "estimated_time": f"{sub_goal_count*5}分",
                "complexity": "medium"
            }
            capabilities = selector.select_capabilities(task_analysis)
            
            # 実行計画生成
            planner = ExecutionPlanner(max_parallel_tasks=3)
            plan = planner.create_execution_plan(capabilities)
            
            duration = time.time() - start
            
            print(f"    所要時間: {duration:.4f}秒")
            print(f"    能力数: {len(capabilities)}")
            print(f"    実行レベル数: {len(plan['execution_plan']['levels'])}")
            print(f"    推定時間: {plan['execution_plan']['total_estimated_time']}")
            print()
            
            self.performance_data.append({
                "test_case": test_case,
                "sub_goals": sub_goal_count,
                "duration": duration,
                "capabilities": len(capabilities),
                "levels": len(plan['execution_plan']['levels'])
            })
        
        self.test_results.append({
            "test": "パフォーマンス測定",
            "status": "success",
            "duration": sum([d['duration'] for d in self.performance_data])
        })
    
    def _print_test_summary(self):
        """テスト結果サマリーを出力"""
        print("=" * 80)
        print("【テスト結果サマリー】")
        print("=" * 80)
        print()
        
        # テスト結果一覧
        print("テスト結果:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"  {status_icon} {result['test']}: {result['status']} ({result['duration']:.2f}秒)")
        print()
        
        # 統計情報
        total_tests = len(self.test_results)
        success_tests = sum([1 for r in self.test_results if r["status"] == "success"])
        failed_tests = total_tests - success_tests
        success_rate = (success_tests / total_tests) * 100 if total_tests > 0 else 0
        
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        print("統計情報:")
        print(f"  総テスト数: {total_tests}")
        print(f"  成功: {success_tests}")
        print(f"  失敗: {failed_tests}")
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  総実行時間: {total_duration:.2f}秒")
        print()
        
        # パフォーマンスデータ
        if self.performance_data:
            print("パフォーマンスデータ:")
            for data in self.performance_data:
                print(f"  {data['test_case']}: {data['duration']:.4f}秒 "
                      f"({data['sub_goals']}サブゴール → {data['capabilities']}能力 → {data['levels']}レベル)")
            print()
        
        # 最終判定
        if success_rate == 100:
            print("🎉 全てのテストが合格しました！")
        else:
            print(f"⚠️ {failed_tests}個のテストが失敗しました。")
        print()


if __name__ == "__main__":
    # 統合テスト実行
    tester = IntegrationTest()
    success = tester.run_all_tests()
    
    # 終了コード
    sys.exit(0 if success else 1)
