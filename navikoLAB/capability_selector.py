#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CapabilitySelector - Naviko能力選択エンジン

TaskAnalyzerが分解したタスクを受け取り、対応する能力（Capability）をマッピングする。

例:
  入力: {
      "sub_tasks": [
          {"type": "information_gathering", "capability": "DeepSearchEngine"},
          {"type": "code_generation", "capability": "AppProjectBuilder"}
      ]
  }
  出力: {
      "selected_capabilities": [
          {
              "name": "DeepSearchEngine",
              "module": "deep_search_engine",
              "class": "DeepSearchEngine",
              "available": True,
              "priority": 1
          },
          {
              "name": "AppProjectBuilder",
              "module": "app_project_builder",
              "class": "AppProjectBuilder",
              "available": True,
              "priority": 2
          }
      ]
  }
"""

import os
import sys
from typing import Dict, List, Optional
from datetime import datetime


class CapabilitySelector:
    """
    能力選択エンジン
    
    TaskAnalyzerのタスク分解結果を受け取り、対応する能力を選択・マッピングする。
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        CapabilitySelectorの初期化
        
        Args:
            base_dir: navikoLABディレクトリの絶対パス（デフォルト: 自動検出）
        """
        # ベースディレクトリの設定
        if base_dir is None:
            # 自動検出: このファイルの場所から推定
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.base_dir = current_dir
        else:
            self.base_dir = base_dir
        
        # 能力の定義
        self.capabilities = {
            "DeepSearchEngine": {
                "module": "deep_search_engine",
                "class": "DeepSearchEngine",
                "description": "情報収集・リサーチ能力",
                "task_types": ["information_gathering"],
                "priority": 1,
                "dependencies": ["universal_llm_connector"]
            },
            "AppProjectBuilder": {
                "module": "app_project_builder",
                "class": "AppProjectBuilder",
                "description": "アプリケーション・コード生成能力",
                "task_types": ["code_generation"],
                "priority": 2,
                "dependencies": ["llm_connector"]
            },
            "ImprovementManager": {
                "module": "improvement_manager",
                "class": "ImprovementManager",
                "description": "コード改善・最適化能力",
                "task_types": ["code_improvement"],
                "priority": 3,
                "dependencies": ["llm_connector"]
            },
            "DataProcessor": {
                "module": "data_processor",
                "class": "DataProcessor",
                "description": "データ処理・分析能力",
                "task_types": ["data_processing"],
                "priority": 2,
                "dependencies": []
            },
            "DocumentGenerator": {
                "module": "document_generator",
                "class": "DocumentGenerator",
                "description": "ドキュメント・資料生成能力",
                "task_types": ["document_generation"],
                "priority": 3,
                "dependencies": []
            },
            "ConversationEngine": {
                "module": "conversation_engine",
                "class": "ConversationEngine",
                "description": "会話・質問応答能力",
                "task_types": ["conversation"],
                "priority": 1,
                "dependencies": []
            }
        }
        
        # 利用可能性キャッシュ
        self._availability_cache = {}
    
    def select_capabilities(self, task_analysis_result: Dict) -> Dict:
        """
        タスク分析結果から必要な能力を選択
        
        Args:
            task_analysis_result: TaskAnalyzerの分析結果
                {
                    "main_goal": str,
                    "sub_tasks": [
                        {
                            "type": str,
                            "priority": int,
                            "description": str,
                            "capability": str,
                            "estimated_minutes": int
                        }
                    ],
                    "estimated_time": str,
                    "complexity": str
                }
        
        Returns:
            選択された能力のリスト:
            {
                "selected_capabilities": [
                    {
                        "name": str,
                        "module": str,
                        "class": str,
                        "description": str,
                        "available": bool,
                        "priority": int,
                        "task": Dict  # 対応するタスク情報
                    }
                ],
                "unavailable_capabilities": [...],
                "missing_dependencies": [...]
            }
        """
        if not task_analysis_result or "sub_tasks" not in task_analysis_result:
            return self._empty_result()
        
        sub_tasks = task_analysis_result.get("sub_tasks", [])
        selected = []
        unavailable = []
        missing_deps = set()
        
        for task in sub_tasks:
            capability_name = task.get("capability")
            
            if not capability_name or capability_name not in self.capabilities:
                # 未知の能力
                unavailable.append({
                    "name": capability_name,
                    "reason": "Unknown capability",
                    "task": task
                })
                continue
            
            capability_config = self.capabilities[capability_name]
            
            # 利用可能性をチェック
            is_available, reason = self.check_capability_availability(capability_name)
            
            capability_info = {
                "name": capability_name,
                "module": capability_config["module"],
                "class": capability_config["class"],
                "description": capability_config["description"],
                "available": is_available,
                "priority": task.get("priority", capability_config["priority"]),
                "task": task
            }
            
            if is_available:
                selected.append(capability_info)
            else:
                capability_info["reason"] = reason
                unavailable.append(capability_info)
                
                # 依存関係の問題を記録
                if "Missing dependency" in reason:
                    for dep in capability_config.get("dependencies", []):
                        missing_deps.add(dep)
        
        return {
            "selected_capabilities": selected,
            "unavailable_capabilities": unavailable,
            "missing_dependencies": list(missing_deps),
            "selection_time": datetime.now().isoformat()
        }
    
    def check_capability_availability(self, capability_name: str) -> tuple:
        """
        能力の利用可能性をチェック
        
        Args:
            capability_name: 能力名
        
        Returns:
            (is_available: bool, reason: str)
        """
        # キャッシュ確認
        if capability_name in self._availability_cache:
            return self._availability_cache[capability_name]
        
        if capability_name not in self.capabilities:
            result = (False, f"Unknown capability: {capability_name}")
            self._availability_cache[capability_name] = result
            return result
        
        capability_config = self.capabilities[capability_name]
        module_name = capability_config["module"]
        
        # モジュールファイルの存在確認
        module_path = os.path.join(self.base_dir, f"{module_name}.py")
        
        if not os.path.exists(module_path):
            result = (False, f"Module file not found: {module_path}")
            self._availability_cache[capability_name] = result
            return result
        
        # 依存関係のチェック
        dependencies = capability_config.get("dependencies", [])
        for dep in dependencies:
            dep_path = os.path.join(self.base_dir, f"{dep}.py")
            if not os.path.exists(dep_path):
                result = (False, f"Missing dependency: {dep}")
                self._availability_cache[capability_name] = result
                return result
        
        # インポート可能性のチェック（簡易版）
        try:
            # sys.pathにbase_dirを追加（一時的）
            if self.base_dir not in sys.path:
                sys.path.insert(0, self.base_dir)
            
            # モジュールインポート試行
            __import__(module_name)
            
            result = (True, "Available")
            self._availability_cache[capability_name] = result
            return result
        
        except Exception as e:
            result = (False, f"Import error: {str(e)}")
            self._availability_cache[capability_name] = result
            return result
    
    def get_capability_priority(self, capability_name: str) -> int:
        """
        能力の優先度を取得
        
        Args:
            capability_name: 能力名
        
        Returns:
            優先度（数値が小さいほど高優先度）
        """
        if capability_name in self.capabilities:
            return self.capabilities[capability_name]["priority"]
        return 999  # 未知の能力は最低優先度
    
    def get_capability_info(self, capability_name: str) -> Optional[Dict]:
        """
        能力の詳細情報を取得
        
        Args:
            capability_name: 能力名
        
        Returns:
            能力情報の辞書、または存在しない場合はNone
        """
        if capability_name in self.capabilities:
            return self.capabilities[capability_name].copy()
        return None
    
    def list_all_capabilities(self) -> List[Dict]:
        """
        全ての利用可能な能力をリスト
        
        Returns:
            能力情報のリスト
        """
        all_capabilities = []
        
        for name, config in self.capabilities.items():
            is_available, reason = self.check_capability_availability(name)
            
            capability_info = {
                "name": name,
                "module": config["module"],
                "class": config["class"],
                "description": config["description"],
                "task_types": config["task_types"],
                "priority": config["priority"],
                "dependencies": config["dependencies"],
                "available": is_available,
                "reason": reason if not is_available else "Available"
            }
            
            all_capabilities.append(capability_info)
        
        # 優先度順にソート
        all_capabilities.sort(key=lambda x: x["priority"])
        
        return all_capabilities
    
    def _empty_result(self) -> Dict:
        """空の結果"""
        return {
            "selected_capabilities": [],
            "unavailable_capabilities": [],
            "missing_dependencies": [],
            "selection_time": datetime.now().isoformat()
        }
    
    def clear_cache(self):
        """利用可能性キャッシュをクリア"""
        self._availability_cache.clear()


# テスト用のmain関数
if __name__ == "__main__":
    selector = CapabilitySelector()
    
    print("=== CapabilitySelector テスト ===\n")
    
    # テストケース1: プレゼン資料作成
    print("【テスト 1: プレゼン資料作成】")
    task_result_1 = {
        "main_goal": "プレゼン資料作成",
        "sub_tasks": [
            {
                "type": "information_gathering",
                "priority": 1,
                "description": "情報収集",
                "capability": "DeepSearchEngine",
                "estimated_minutes": 5
            },
            {
                "type": "document_generation",
                "priority": 2,
                "description": "ドキュメント生成",
                "capability": "DocumentGenerator",
                "estimated_minutes": 15
            }
        ],
        "estimated_time": "20分",
        "complexity": "medium"
    }
    
    result_1 = selector.select_capabilities(task_result_1)
    print(f"選択された能力: {len(result_1['selected_capabilities'])}個")
    for cap in result_1["selected_capabilities"]:
        print(f"  - {cap['name']}: {cap['description']} (優先度: {cap['priority']})")
    
    if result_1["unavailable_capabilities"]:
        print(f"利用不可能な能力: {len(result_1['unavailable_capabilities'])}個")
        for cap in result_1["unavailable_capabilities"]:
            print(f"  - {cap['name']}: {cap.get('reason', 'Unknown')}")
    
    print()
    
    # テストケース2: アプリ作成
    print("【テスト 2: アプリ作成】")
    task_result_2 = {
        "main_goal": "アプリ作成",
        "sub_tasks": [
            {
                "type": "code_generation",
                "priority": 1,
                "description": "コード生成",
                "capability": "AppProjectBuilder",
                "estimated_minutes": 15
            }
        ],
        "estimated_time": "15分",
        "complexity": "medium"
    }
    
    result_2 = selector.select_capabilities(task_result_2)
    print(f"選択された能力: {len(result_2['selected_capabilities'])}個")
    for cap in result_2["selected_capabilities"]:
        print(f"  - {cap['name']}: {cap['description']} (利用可能: {cap['available']})")
    
    print()
    
    # 全能力リスト
    print("【全能力リスト】")
    all_caps = selector.list_all_capabilities()
    print(f"総能力数: {len(all_caps)}個")
    for cap in all_caps:
        status = "✅" if cap["available"] else "❌"
        print(f"  {status} {cap['name']}: {cap['description']}")
    
    print("\n✅ 全テスト完了")
