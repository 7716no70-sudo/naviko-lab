#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CapabilitySelector - Naviko能力選択エンジン

TaskAnalyzerが分解したタスクを受け取り、対応する能力（Capability）を選択・マッピングする。
既存モジュール（DeepSearchEngine, AppProjectBuilder等）との統合を管理。

例:
  入力: TaskAnalyzerの出力（sub_tasksリスト）
  出力: {
      "capabilities": [
          {
              "name": "DeepSearchEngine",
              "task": {...},
              "priority": 1,
              "estimated_time": "5分",
              "status": "ready"
          }
      ]
  }
"""

import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime


class CapabilitySelector:
    """
    能力選択エンジン
    
    TaskAnalyzerのタスク分解結果を受け取り、
    対応する能力（Capability）をマッピングする。
    """
    
    def __init__(self, naviko_lab_path: Optional[str] = None):
        """
        CapabilitySelectorの初期化
        
        Args:
            naviko_lab_path: navikoLABディレクトリのパス（オプション）
        """
        # navikoLABのパスを設定
        if naviko_lab_path is None:
            # デフォルト: 現在のファイルがあるディレクトリ
            naviko_lab_path = os.path.dirname(os.path.abspath(__file__))
        
        self.naviko_lab_path = naviko_lab_path
        
        # 能力マッピングの定義
        self.capability_mappings = {
            "information_gathering": {
                "module": "deep_search_engine",
                "class": "DeepSearchEngine",
                "description": "ディープサーチエンジン（情報収集）",
                "available": True,
                "dependencies": ["universal_llm_connector"]
            },
            "code_generation": {
                "module": "app_project_builder",
                "class": "AppProjectBuilder",
                "description": "アプリケーションビルダー（コード生成）",
                "available": True,
                "dependencies": ["llm_connector"]
            },
            "code_improvement": {
                "module": "improvement_manager",
                "class": "ImprovementManager",
                "description": "改善マネージャー（コード改善）",
                "available": True,
                "dependencies": ["llm_connector"]
            },
            "data_processing": {
                "module": "data_processor",
                "class": "DataProcessor",
                "description": "データプロセッサー（データ処理）",
                "available": False,  # 未実装
                "dependencies": []
            },
            "document_generation": {
                "module": "document_generator",
                "class": "DocumentGenerator",
                "description": "ドキュメント生成（資料作成）",
                "available": False,  # 未実装
                "dependencies": []
            },
            "conversation": {
                "module": "conversation_engine",
                "class": "ConversationEngine",
                "description": "会話エンジン（質問応答）",
                "available": True,
                "dependencies": ["llm_connector"]
            }
        }
    
    def select_capabilities(self, task_analysis_result: Dict) -> Dict:
        """
        TaskAnalyzerの出力から能力を選択
        
        Args:
            task_analysis_result: TaskAnalyzerのanalyze()メソッドの出力
            {
                "main_goal": str,
                "sub_tasks": List[Dict],
                "estimated_time": str,
                "complexity": str,
                "requires_confirmation": bool,
                "analyzed_at": str
            }
        
        Returns:
            選択結果の辞書:
            {
                "main_goal": str,
                "capabilities": List[Dict],  # 選択された能力のリスト
                "total_estimated_time": str,
                "execution_order": List[int],  # 実行順序（priorityのリスト）
                "warnings": List[str],  # 警告メッセージ（利用不可な能力等）
                "selected_at": str
            }
        """
        if not task_analysis_result or "sub_tasks" not in task_analysis_result:
            return self._empty_result()
        
        main_goal = task_analysis_result.get("main_goal", "不明")
        sub_tasks = task_analysis_result.get("sub_tasks", [])
        
        # 各タスクに対応する能力を選択
        capabilities = []
        warnings = []
        total_minutes = 0
        
        for task in sub_tasks:
            task_type = task.get("type")
            if task_type not in self.capability_mappings:
                warnings.append(f"タスクタイプ '{task_type}' に対応する能力が見つかりません")
                continue
            
            mapping = self.capability_mappings[task_type]
            
            # 能力が利用可能かチェック
            if not mapping["available"]:
                warnings.append(
                    f"{mapping['description']} は現在利用できません（未実装）"
                )
                continue
            
            # 依存関係チェック
            missing_deps = self._check_dependencies(mapping["dependencies"])
            if missing_deps:
                warnings.append(
                    f"{mapping['description']} の依存関係が不足: {', '.join(missing_deps)}"
                )
                continue
            
            # 能力を追加
            capability = {
                "name": mapping["class"],
                "module": mapping["module"],
                "description": mapping["description"],
                "task": task,
                "priority": task.get("priority", 999),
                "estimated_minutes": task.get("estimated_minutes", 0),
                "status": "ready",
                "dependencies": mapping["dependencies"]
            }
            capabilities.append(capability)
            total_minutes += task.get("estimated_minutes", 0)
        
        # 実行順序を生成（priorityでソート）
        execution_order = [cap["priority"] for cap in sorted(capabilities, key=lambda x: x["priority"])]
        
        # 総推定時間を計算
        total_estimated_time = self._format_time(total_minutes)
        
        return {
            "main_goal": main_goal,
            "capabilities": capabilities,
            "total_estimated_time": total_estimated_time,
            "execution_order": execution_order,
            "warnings": warnings,
            "selected_at": datetime.now().isoformat()
        }
    
    def _empty_result(self) -> Dict:
        """空の結果"""
        return {
            "main_goal": "不明",
            "capabilities": [],
            "total_estimated_time": "0分",
            "execution_order": [],
            "warnings": ["タスク分析結果が不正です"],
            "selected_at": datetime.now().isoformat()
        }
    
    def _check_dependencies(self, dependencies: List[str]) -> List[str]:
        """
        依存関係をチェック
        
        Args:
            dependencies: 依存モジュール名のリスト
        
        Returns:
            不足している依存関係のリスト（空なら全て満たされている）
        """
        missing = []
        for dep in dependencies:
            dep_path = os.path.join(self.naviko_lab_path, f"{dep}.py")
            if not os.path.exists(dep_path):
                missing.append(dep)
        return missing
    
    def _format_time(self, total_minutes: int) -> str:
        """
        推定時間をフォーマット
        
        Args:
            total_minutes: 総分数
        
        Returns:
            フォーマット済みの時間文字列
        """
        if total_minutes < 60:
            return f"{total_minutes}分"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes == 0:
                return f"{hours}時間"
            else:
                return f"{hours}時間{minutes}分"
    
    def get_capability_info(self, capability_name: str) -> Optional[Dict]:
        """
        指定された能力の情報を取得
        
        Args:
            capability_name: 能力のクラス名
        
        Returns:
            能力情報の辞書（見つからない場合はNone）
        """
        for task_type, mapping in self.capability_mappings.items():
            if mapping["class"] == capability_name:
                return {
                    "task_type": task_type,
                    "module": mapping["module"],
                    "class": mapping["class"],
                    "description": mapping["description"],
                    "available": mapping["available"],
                    "dependencies": mapping["dependencies"]
                }
        return None
    
    def list_available_capabilities(self) -> List[Dict]:
        """
        利用可能な能力の一覧を取得
        
        Returns:
            利用可能な能力のリスト
        """
        available = []
        for task_type, mapping in self.capability_mappings.items():
            if mapping["available"]:
                missing_deps = self._check_dependencies(mapping["dependencies"])
                available.append({
                    "task_type": task_type,
                    "class": mapping["class"],
                    "description": mapping["description"],
                    "dependencies": mapping["dependencies"],
                    "dependencies_met": len(missing_deps) == 0,
                    "missing_dependencies": missing_deps
                })
        return available
    
    def validate_execution_plan(self, capabilities: List[Dict]) -> Dict:
        """
        実行計画を検証
        
        Args:
            capabilities: 選択された能力のリスト
        
        Returns:
            検証結果:
            {
                "valid": bool,
                "errors": List[str],
                "warnings": List[str]
            }
        """
        errors = []
        warnings = []
        
        # 1. 能力が空でないかチェック
        if not capabilities:
            errors.append("実行する能力が選択されていません")
        
        # 2. 各能力の依存関係チェック
        for cap in capabilities:
            missing_deps = self._check_dependencies(cap.get("dependencies", []))
            if missing_deps:
                errors.append(
                    f"{cap['name']} の依存関係が不足: {', '.join(missing_deps)}"
                )
        
        # 3. 優先度の重複チェック
        priorities = [cap.get("priority") for cap in capabilities]
        if len(priorities) != len(set(priorities)):
            warnings.append("優先度に重複があります")
        
        # 4. ステータスチェック
        for cap in capabilities:
            if cap.get("status") != "ready":
                warnings.append(
                    f"{cap['name']} のステータスが 'ready' ではありません: {cap.get('status')}"
                )
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


# テスト用のmain関数
if __name__ == "__main__":
    # TaskAnalyzerをインポート
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from task_analyzer import TaskAnalyzer
    
    # テストケース
    analyzer = TaskAnalyzer()
    selector = CapabilitySelector()
    
    test_cases = [
        "プレゼン資料作成して",
        "アプリ作成して",
        "データ分析して"
    ]
    
    print("=== CapabilitySelector テスト ===\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"【テスト {i}/3】")
        print(f"入力: {test}")
        
        # タスク分析
        task_result = analyzer.analyze(test)
        print(f"  タスク分析:")
        print(f"    メインゴール: {task_result['main_goal']}")
        print(f"    サブタスク数: {len(task_result['sub_tasks'])}")
        
        # 能力選択
        capability_result = selector.select_capabilities(task_result)
        print(f"  能力選択:")
        print(f"    選択された能力数: {len(capability_result['capabilities'])}")
        print(f"    総推定時間: {capability_result['total_estimated_time']}")
        print(f"    実行順序: {capability_result['execution_order']}")
        
        if capability_result['warnings']:
            print(f"    警告:")
            for warning in capability_result['warnings']:
                print(f"      ⚠️ {warning}")
        
        print(f"  選択された能力:")
        for cap in capability_result['capabilities']:
            print(f"    {cap['priority']}. {cap['description']} ({cap['name']})")
        
        print()
    
    # 利用可能な能力の一覧
    print("\n=== 利用可能な能力一覧 ===")
    available = selector.list_available_capabilities()
    for cap in available:
        deps_status = "✅" if cap["dependencies_met"] else "❌"
        print(f"{deps_status} {cap['description']} ({cap['class']})")
        if not cap["dependencies_met"]:
            print(f"   不足依存: {', '.join(cap['missing_dependencies'])}")
    
    print("\n✅ 全テストケース実行完了")
