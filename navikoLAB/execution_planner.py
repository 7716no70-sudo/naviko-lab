#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ExecutionPlanner - Naviko実行計画エンジン

CapabilitySelectorが選択した能力を受け取り、最適な実行計画を立てる。
依存関係の分析、並列実行戦略、リソース配分、エラーハンドリングを管理。

機能:
  - タスク依存グラフの構築（DAG）
  - 並列実行可能なタスクの検出
  - 実行レベルの割り当て（Level 1, 2, 3...）
  - リソース配分計画（メモリ、CPU）
  - エラーハンドリング戦略
  - 推定時間の再計算（並列実行考慮）
  - クリティカルパスの特定

例:
  入力: CapabilitySelectorの出力
  出力: {
      "execution_plan": {
          "levels": [  # 実行レベル（並列実行グループ）
              {
                  "level": 1,
                  "tasks": [...],
                  "estimated_time": "5分",
                  "parallel": True
              }
          ],
          "critical_path": [...],
          "total_estimated_time": "15分",
          "resource_requirements": {...}
      }
  }
"""

import os
import sys
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
from collections import defaultdict, deque


class ExecutionPlanner:
    """
    実行計画エンジン
    
    CapabilitySelectorの出力を受け取り、
    最適な実行計画（並列実行、リソース配分、エラーハンドリング）を立てる。
    """
    
    def __init__(self, max_parallel_tasks: int = 3, memory_limit_mb: int = 2048):
        """
        ExecutionPlannerの初期化
        
        Args:
            max_parallel_tasks: 最大並列実行タスク数（デフォルト: 3）
            memory_limit_mb: メモリ制限（MB、デフォルト: 2048MB = 2GB）
        """
        self.max_parallel_tasks = max_parallel_tasks
        self.memory_limit_mb = memory_limit_mb
        
        # リソース見積もり（能力ごとの推定リソース使用量）
        self.resource_estimates = {
            "DeepSearchEngine": {"memory_mb": 256, "cpu_cores": 1},
            "AppProjectBuilder": {"memory_mb": 512, "cpu_cores": 2},
            "ImprovementManager": {"memory_mb": 256, "cpu_cores": 1},
            "ConversationEngine": {"memory_mb": 128, "cpu_cores": 1},
            "DataProcessor": {"memory_mb": 512, "cpu_cores": 2},
            "DocumentGenerator": {"memory_mb": 256, "cpu_cores": 1}
        }
        
        # エラーハンドリング設定
        self.error_handling_config = {
            "max_retries": 3,
            "retry_delay_seconds": 5,
            "fallback_strategies": {
                "DeepSearchEngine": ["ConversationEngine"],
                "AppProjectBuilder": [],
                "ImprovementManager": [],
                "ConversationEngine": [],
                "DataProcessor": [],
                "DocumentGenerator": []
            }
        }
    
    def create_execution_plan(self, capability_selection_result: Dict) -> Dict:
        """
        実行計画を作成
        
        Args:
            capability_selection_result: CapabilitySelectorのselect_capabilities()の出力
            {
                "main_goal": str,
                "capabilities": List[Dict],
                "total_estimated_time": str,
                "execution_order": List[int],
                "warnings": List[str],
                "selected_at": str
            }
        
        Returns:
            実行計画の辞書:
            {
                "main_goal": str,
                "execution_plan": {
                    "levels": List[Dict],  # 実行レベル（並列グループ）
                    "critical_path": List[str],  # クリティカルパス
                    "total_estimated_time": str,  # 並列実行考慮後の時間
                    "sequential_time": str,  # 逐次実行時の時間
                    "time_saved": str,  # 並列化による時間短縮
                    "resource_requirements": Dict,  # リソース要件
                    "max_parallel_tasks": int,  # 実際の最大並列数
                    "error_handling": Dict  # エラーハンドリング計画
                },
                "warnings": List[str],
                "planned_at": str
            }
        """
        if not capability_selection_result or "capabilities" not in capability_selection_result:
            return self._empty_plan()
        
        main_goal = capability_selection_result.get("main_goal", "不明")
        capabilities = capability_selection_result.get("capabilities", [])
        warnings = capability_selection_result.get("warnings", []).copy()
        
        if not capabilities:
            warnings.append("実行可能な能力が選択されていません")
            return self._empty_plan(main_goal, warnings)
        
        # 1. タスク依存グラフを構築
        dependency_graph = self._build_dependency_graph(capabilities)
        
        # 2. 並列実行可能なタスクを検出
        parallel_groups = self._detect_parallel_tasks(capabilities, dependency_graph)
        
        # 3. 実行レベルを割り当て
        execution_levels = self._assign_execution_levels(capabilities, parallel_groups)
        
        # 4. リソース要件を計算
        resource_requirements = self._calculate_resource_requirements(execution_levels)
        
        # 5. エラーハンドリング計画を作成
        error_handling_plan = self._create_error_handling_plan(capabilities)
        
        # 6. 推定時間を再計算（並列実行考慮）
        time_info = self._recalculate_estimated_time(execution_levels)
        
        # 7. クリティカルパスを特定
        critical_path = self._find_critical_path(capabilities, dependency_graph)
        
        # 8. リソース制約チェック
        resource_warnings = self._check_resource_constraints(resource_requirements)
        warnings.extend(resource_warnings)
        
        # 実行計画を構築
        execution_plan = {
            "levels": execution_levels,
            "critical_path": critical_path,
            "total_estimated_time": time_info["total_time"],
            "sequential_time": time_info["sequential_time"],
            "time_saved": time_info["time_saved"],
            "resource_requirements": resource_requirements,
            "max_parallel_tasks": time_info["max_parallel"],
            "error_handling": error_handling_plan
        }
        
        return {
            "main_goal": main_goal,
            "execution_plan": execution_plan,
            "warnings": warnings,
            "planned_at": datetime.now().isoformat()
        }
    
    def _build_dependency_graph(self, capabilities: List[Dict]) -> Dict[str, List[str]]:
        """
        タスク依存グラフを構築（DAG: Directed Acyclic Graph）
        
        Args:
            capabilities: 能力のリスト
        
        Returns:
            依存グラフ: {task_id: [dependent_task_ids]}
        """
        graph = defaultdict(list)
        
        # 各能力にIDを割り当て
        for i, capability in enumerate(capabilities):
            capability["_id"] = f"task_{i}"
        
        # 依存関係を構築
        # 1. priority順（低い順に依存）
        # 2. タスクタイプ間の暗黙的依存
        #    - information_gathering → code_generation
        #    - code_generation → code_improvement
        
        sorted_caps = sorted(capabilities, key=lambda x: x.get("priority", 999))
        
        for i, cap in enumerate(sorted_caps):
            task_id = cap["_id"]
            task_type = cap["task"].get("type")
            
            # 前のタスクとの依存関係をチェック
            for prev_cap in sorted_caps[:i]:
                prev_id = prev_cap["_id"]
                prev_type = prev_cap["task"].get("type")
                
                # 暗黙的依存関係のルール
                if self._has_implicit_dependency(prev_type, task_type):
                    graph[prev_id].append(task_id)
        
        return dict(graph)
    
    def _has_implicit_dependency(self, prev_type: str, current_type: str) -> bool:
        """
        タスクタイプ間の暗黙的依存関係をチェック
        
        Args:
            prev_type: 前のタスクタイプ
            current_type: 現在のタスクタイプ
        
        Returns:
            依存関係がある場合True
        """
        dependencies = {
            "information_gathering": ["code_generation", "document_generation"],
            "code_generation": ["code_improvement"],
            "data_processing": ["document_generation"]
        }
        
        return current_type in dependencies.get(prev_type, [])
    
    def _detect_parallel_tasks(self, capabilities: List[Dict], dependency_graph: Dict[str, List[str]]) -> List[Set[str]]:
        """
        並列実行可能なタスクを検出
        
        Args:
            capabilities: 能力のリスト
            dependency_graph: 依存グラフ
        
        Returns:
            並列実行グループのリスト（各グループは並列実行可能なタスクIDのSet）
        """
        # 依存関係の逆グラフを作成（誰に依存されているか）
        reverse_graph = defaultdict(list)
        for task_id, dependents in dependency_graph.items():
            for dependent in dependents:
                reverse_graph[dependent].append(task_id)
        
        # 各タスクの入次数（依存数）を計算
        in_degree = {cap["_id"]: 0 for cap in capabilities}
        for task_id in reverse_graph:
            in_degree[task_id] = len(reverse_graph[task_id])
        
        # トポロジカルソート + グループ化
        parallel_groups = []
        visited = set()
        
        while len(visited) < len(capabilities):
            # 現在実行可能なタスク（入次数0）
            current_group = set()
            for cap in capabilities:
                task_id = cap["_id"]
                if task_id not in visited and in_degree[task_id] == 0:
                    current_group.add(task_id)
            
            if not current_group:
                # 循環依存またはエラー
                break
            
            parallel_groups.append(current_group)
            
            # 訪問済みマークと次数更新
            for task_id in current_group:
                visited.add(task_id)
                # このタスクに依存するタスクの入次数を減らす
                for dependent in dependency_graph.get(task_id, []):
                    in_degree[dependent] -= 1
        
        return parallel_groups
    
    def _assign_execution_levels(self, capabilities: List[Dict], parallel_groups: List[Set[str]]) -> List[Dict]:
        """
        実行レベルを割り当て
        
        Args:
            capabilities: 能力のリスト
            parallel_groups: 並列実行グループのリスト
        
        Returns:
            実行レベルのリスト（各レベルは並列実行グループ）
        """
        # タスクIDから能力を検索するマップ
        task_map = {cap["_id"]: cap for cap in capabilities}
        
        execution_levels = []
        for level_num, group in enumerate(parallel_groups, start=1):
            # グループ内のタスクを取得
            tasks = [task_map[task_id] for task_id in group]
            
            # 推定時間を計算（並列実行なので最大値）
            estimated_minutes = max(
                [task.get("estimated_minutes", 0) for task in tasks],
                default=0
            )
            
            # リソース制約による並列実行可否
            can_parallel = len(tasks) <= self.max_parallel_tasks
            
            level = {
                "level": level_num,
                "tasks": tasks,
                "task_count": len(tasks),
                "estimated_minutes": estimated_minutes,
                "estimated_time": self._format_time(estimated_minutes),
                "parallel": can_parallel and len(tasks) > 1,
                "actual_parallel_count": min(len(tasks), self.max_parallel_tasks)
            }
            execution_levels.append(level)
        
        return execution_levels
    
    def _calculate_resource_requirements(self, execution_levels: List[Dict]) -> Dict:
        """
        リソース要件を計算
        
        Args:
            execution_levels: 実行レベルのリスト
        
        Returns:
            リソース要件の辞書
        """
        max_memory_mb = 0
        max_cpu_cores = 0
        
        for level in execution_levels:
            level_memory = 0
            level_cpu = 0
            
            # 並列実行するタスクのリソースを合計
            parallel_count = min(level["task_count"], self.max_parallel_tasks)
            for i, task in enumerate(level["tasks"][:parallel_count]):
                capability_name = task["name"]
                resources = self.resource_estimates.get(
                    capability_name,
                    {"memory_mb": 256, "cpu_cores": 1}
                )
                level_memory += resources["memory_mb"]
                level_cpu += resources["cpu_cores"]
            
            max_memory_mb = max(max_memory_mb, level_memory)
            max_cpu_cores = max(max_cpu_cores, level_cpu)
        
        return {
            "max_memory_mb": max_memory_mb,
            "max_cpu_cores": max_cpu_cores,
            "memory_limit_mb": self.memory_limit_mb,
            "within_limits": max_memory_mb <= self.memory_limit_mb
        }
    
    def _create_error_handling_plan(self, capabilities: List[Dict]) -> Dict:
        """
        エラーハンドリング計画を作成
        
        Args:
            capabilities: 能力のリスト
        
        Returns:
            エラーハンドリング計画の辞書
        """
        plan = {
            "max_retries": self.error_handling_config["max_retries"],
            "retry_delay_seconds": self.error_handling_config["retry_delay_seconds"],
            "fallback_strategies": {}
        }
        
        for cap in capabilities:
            capability_name = cap["name"]
            fallbacks = self.error_handling_config["fallback_strategies"].get(
                capability_name,
                []
            )
            
            plan["fallback_strategies"][capability_name] = {
                "primary": capability_name,
                "fallbacks": fallbacks,
                "has_fallback": len(fallbacks) > 0
            }
        
        return plan
    
    def _recalculate_estimated_time(self, execution_levels: List[Dict]) -> Dict:
        """
        推定時間を再計算（並列実行考慮）
        
        Args:
            execution_levels: 実行レベルのリスト
        
        Returns:
            時間情報の辞書
        """
        # 並列実行時の総時間（各レベルの最大時間の合計）
        total_minutes = sum(
            level["estimated_minutes"] for level in execution_levels
        )
        
        # 逐次実行時の総時間（全タスクの合計）
        sequential_minutes = sum(
            sum(task.get("estimated_minutes", 0) for task in level["tasks"])
            for level in execution_levels
        )
        
        # 時間短縮
        time_saved_minutes = sequential_minutes - total_minutes
        
        # 実際の最大並列数
        max_parallel = max(
            level["actual_parallel_count"] for level in execution_levels
        ) if execution_levels else 1
        
        return {
            "total_time": self._format_time(total_minutes),
            "sequential_time": self._format_time(sequential_minutes),
            "time_saved": self._format_time(time_saved_minutes),
            "max_parallel": max_parallel
        }
    
    def _find_critical_path(self, capabilities: List[Dict], dependency_graph: Dict[str, List[str]]) -> List[str]:
        """
        クリティカルパスを特定（最長経路）
        
        Args:
            capabilities: 能力のリスト
            dependency_graph: 依存グラフ
        
        Returns:
            クリティカルパス（タスク名のリスト）
        """
        # タスクIDから能力を検索するマップ
        task_map = {cap["_id"]: cap for cap in capabilities}
        
        # 各タスクまでの最長時間を計算（動的計画法）
        max_time = {cap["_id"]: cap.get("estimated_minutes", 0) for cap in capabilities}
        
        # トポロジカル順にソート
        sorted_tasks = self._topological_sort(capabilities, dependency_graph)
        
        # 最長経路を計算
        for task_id in sorted_tasks:
            task_time = task_map[task_id].get("estimated_minutes", 0)
            
            # このタスクに依存するタスクの最長時間を更新
            for dependent_id in dependency_graph.get(task_id, []):
                max_time[dependent_id] = max(
                    max_time[dependent_id],
                    max_time[task_id] + task_map[dependent_id].get("estimated_minutes", 0)
                )
        
        # 最長時間のタスクから逆順に辿る
        if not max_time:
            return []
        
        # 終点（最長時間のタスク）を見つける
        end_task = max(max_time.items(), key=lambda x: x[1])[0]
        
        # 逆グラフを作成
        reverse_graph = defaultdict(list)
        for task_id, dependents in dependency_graph.items():
            for dependent in dependents:
                reverse_graph[dependent].append(task_id)
        
        # クリティカルパスを構築（逆順）
        critical_path = [end_task]
        current = end_task
        
        while reverse_graph.get(current):
            # 前のタスクで最長時間のものを選択
            prev_tasks = reverse_graph[current]
            if prev_tasks:
                prev = max(prev_tasks, key=lambda t: max_time[t])
                critical_path.append(prev)
                current = prev
            else:
                break
        
        # 順序を逆にしてタスク名に変換
        critical_path.reverse()
        return [task_map[task_id]["name"] for task_id in critical_path]
    
    def _topological_sort(self, capabilities: List[Dict], dependency_graph: Dict[str, List[str]]) -> List[str]:
        """
        トポロジカルソート
        
        Args:
            capabilities: 能力のリスト
            dependency_graph: 依存グラフ
        
        Returns:
            ソート済みタスクIDのリスト
        """
        # 入次数を計算
        in_degree = {cap["_id"]: 0 for cap in capabilities}
        for task_id, dependents in dependency_graph.items():
            for dependent in dependents:
                in_degree[dependent] += 1
        
        # 入次数0のタスクをキューに追加
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        sorted_tasks = []
        
        while queue:
            task_id = queue.popleft()
            sorted_tasks.append(task_id)
            
            # 依存タスクの入次数を減らす
            for dependent in dependency_graph.get(task_id, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        return sorted_tasks
    
    def _check_resource_constraints(self, resource_requirements: Dict) -> List[str]:
        """
        リソース制約をチェック
        
        Args:
            resource_requirements: リソース要件
        
        Returns:
            警告メッセージのリスト
        """
        warnings = []
        
        if not resource_requirements["within_limits"]:
            warnings.append(
                f"メモリ制限超過: 必要 {resource_requirements['max_memory_mb']}MB > "
                f"制限 {resource_requirements['memory_limit_mb']}MB"
            )
        
        return warnings
    
    def _format_time(self, minutes: int) -> str:
        """
        時間をフォーマット
        
        Args:
            minutes: 分数
        
        Returns:
            フォーマット済み文字列（例: "1時間30分", "45分", "2時間"）
        """
        if minutes == 0:
            return "0分"
        elif minutes < 60:
            return f"{minutes}分"
        else:
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"{hours}時間"
            else:
                return f"{hours}時間{mins}分"
    
    def _empty_plan(self, main_goal: str = "不明", warnings: Optional[List[str]] = None) -> Dict:
        """空の実行計画"""
        if warnings is None:
            warnings = ["実行計画を作成できません"]
        
        return {
            "main_goal": main_goal,
            "execution_plan": {
                "levels": [],
                "critical_path": [],
                "total_estimated_time": "0分",
                "sequential_time": "0分",
                "time_saved": "0分",
                "resource_requirements": {
                    "max_memory_mb": 0,
                    "max_cpu_cores": 0,
                    "memory_limit_mb": self.memory_limit_mb,
                    "within_limits": True
                },
                "max_parallel_tasks": 0,
                "error_handling": {
                    "max_retries": self.error_handling_config["max_retries"],
                    "retry_delay_seconds": self.error_handling_config["retry_delay_seconds"],
                    "fallback_strategies": {}
                }
            },
            "warnings": warnings,
            "planned_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # テストコード
    print("ExecutionPlanner - Naviko実行計画エンジン")
    print("==========================================")
    print()
    
    # サンプルのCapabilitySelector出力
    sample_input = {
        "main_goal": "Webアプリケーション作成",
        "capabilities": [
            {
                "name": "DeepSearchEngine",
                "module": "deep_search_engine",
                "description": "情報収集",
                "task": {"type": "information_gathering", "description": "リサーチ"},
                "priority": 1,
                "estimated_minutes": 5,
                "status": "ready",
                "dependencies": []
            },
            {
                "name": "AppProjectBuilder",
                "module": "app_project_builder",
                "description": "アプリ生成",
                "task": {"type": "code_generation", "description": "コード生成"},
                "priority": 2,
                "estimated_minutes": 10,
                "status": "ready",
                "dependencies": []
            },
            {
                "name": "ImprovementManager",
                "module": "improvement_manager",
                "description": "コード改善",
                "task": {"type": "code_improvement", "description": "改善"},
                "priority": 3,
                "estimated_minutes": 5,
                "status": "ready",
                "dependencies": []
            }
        ],
        "total_estimated_time": "20分",
        "execution_order": [1, 2, 3],
        "warnings": [],
        "selected_at": datetime.now().isoformat()
    }
    
    # ExecutionPlannerのインスタンス作成
    planner = ExecutionPlanner(max_parallel_tasks=2, memory_limit_mb=2048)
    
    # 実行計画を作成
    result = planner.create_execution_plan(sample_input)
    
    # 結果を表示
    print("【実行計画】")
    print(f"メインゴール: {result['main_goal']}")
    print()
    
    plan = result["execution_plan"]
    print(f"総推定時間（並列）: {plan['total_estimated_time']}")
    print(f"逐次実行時間: {plan['sequential_time']}")
    print(f"時間短縮: {plan['time_saved']}")
    print(f"最大並列数: {plan['max_parallel_tasks']}")
    print()
    
    print("【実行レベル】")
    for level in plan["levels"]:
        print(f"\nLevel {level['level']}: {level['estimated_time']}")
        print(f"  並列実行: {level['parallel']} (タスク数: {level['task_count']})")
        for task in level["tasks"]:
            print(f"    - {task['name']}: {task['description']}")
    
    print()
    print(f"【クリティカルパス】")
    print(" → ".join(plan["critical_path"]))
    
    print()
    print("【リソース要件】")
    res = plan["resource_requirements"]
    print(f"  最大メモリ: {res['max_memory_mb']}MB / {res['memory_limit_mb']}MB")
    print(f"  最大CPU: {res['max_cpu_cores']}コア")
    print(f"  制限内: {res['within_limits']}")
    
    if result["warnings"]:
        print()
        print("【警告】")
        for warning in result["warnings"]:
            print(f"  ⚠ {warning}")
