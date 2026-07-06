#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaskAnalyzer - Navikoタスク分析エンジン

ユーザーの要求（音声テキスト）を分析し、必要なタスクに自動分解する。

例:
  入力: "プレゼン資料作成して"
  出力: {
      "main_goal": "プレゼン資料作成",
      "sub_tasks": [
          {"type": "information_gathering", "priority": 1, "description": "情報収集"},
          {"type": "data_processing", "priority": 2, "description": "データ整理"},
          {"type": "document_generation", "priority": 3, "description": "資料生成"}
      ],
      "estimated_time": "30分"
  }
"""

import re
from typing import Dict, List, Optional
from datetime import datetime


class TaskAnalyzer:
    """
    タスク分析エンジン
    
    ユーザーの要求を分析し、実行可能なタスクに分解する。
    """
    
    def __init__(self):
        """
        TaskAnalyzerの初期化
        """
        # タスクタイプの定義
        self.task_types = {
            "information_gathering": {
                "keywords": ["調べて", "検索", "情報", "調査", "リサーチ", "探して"],
                "description": "情報収集",
                "capability": "DeepSearchEngine",
                "estimated_minutes": 5
            },
            "code_generation": {
                "keywords": ["アプリ", "プログラム", "コード", "作成", "開発", "実装"],
                "description": "コード生成",
                "capability": "AppProjectBuilder",
                "estimated_minutes": 15
            },
            "code_improvement": {
                "keywords": ["改善", "最適化", "リファクタリング", "修正", "バグ", "エラー"],
                "description": "コード改善",
                "capability": "ImprovementManager",
                "estimated_minutes": 10
            },
            "data_processing": {
                "keywords": ["データ", "分析", "整理", "処理", "集計", "統計"],
                "description": "データ処理",
                "capability": "DataProcessor",
                "estimated_minutes": 10
            },
            "document_generation": {
                "keywords": ["資料", "ドキュメント", "レポート", "プレゼン", "まとめ"],
                "description": "ドキュメント生成",
                "capability": "DocumentGenerator",
                "estimated_minutes": 15
            },
            "conversation": {
                "keywords": ["教えて", "説明", "どう", "なに", "いつ", "どこ", "だれ"],
                "description": "会話・質問応答",
                "capability": "ConversationEngine",
                "estimated_minutes": 2
            }
        }
    
    def analyze(self, user_request: str) -> Dict:
        """
        ユーザー要求を分析し、タスクに分解
        
        Args:
            user_request: ユーザーの要求テキスト（音声から変換されたもの）
        
        Returns:
            分析結果の辞書:
            {
                "main_goal": str,  # メインゴール
                "sub_tasks": List[Dict],  # サブタスクのリスト
                "estimated_time": str,  # 推定時間
                "complexity": str,  # 複雑度 (low/medium/high)
                "requires_confirmation": bool  # 確認が必要か
            }
        """
        if not user_request or not user_request.strip():
            return self._empty_result()
        
        # テキストを正規化
        normalized_text = user_request.strip().lower()
        
        # メインゴールを抽出
        main_goal = self._extract_main_goal(user_request)
        
        # タスクタイプを検出
        detected_types = self._detect_task_types(normalized_text)
        
        # サブタスクを生成
        sub_tasks = self._generate_sub_tasks(detected_types, normalized_text)
        
        # 推定時間を計算
        estimated_time = self._calculate_estimated_time(sub_tasks)
        
        # 複雑度を判定
        complexity = self._assess_complexity(sub_tasks)
        
        # 確認が必要かどうか
        requires_confirmation = self._requires_confirmation(sub_tasks, normalized_text)
        
        return {
            "main_goal": main_goal,
            "sub_tasks": sub_tasks,
            "estimated_time": estimated_time,
            "complexity": complexity,
            "requires_confirmation": requires_confirmation,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _empty_result(self) -> Dict:
        """空の要求の場合の結果"""
        return {
            "main_goal": "不明",
            "sub_tasks": [],
            "estimated_time": "0分",
            "complexity": "low",
            "requires_confirmation": False,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _extract_main_goal(self, user_request: str) -> str:
        """
        メインゴールを抽出
        
        Args:
            user_request: ユーザー要求テキスト
        
        Returns:
            メインゴールの文字列
        """
        # 「～して」「～作って」「～教えて」等のパターンを探す
        patterns = [
            r'(.+?)(?:して|作って|教えて|調べて|分析して|改善して)',
            r'(.+)',  # フォールバック: 全文
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_request)
            if match:
                goal = match.group(1).strip()
                if goal:
                    return goal
        
        return user_request.strip()
    
    def _detect_task_types(self, normalized_text: str) -> List[str]:
        """
        テキストから該当するタスクタイプを検出
        
        Args:
            normalized_text: 正規化されたテキスト
        
        Returns:
            検出されたタスクタイプのリスト
        """
        detected = []
        
        for task_type, config in self.task_types.items():
            for keyword in config["keywords"]:
                if keyword in normalized_text:
                    if task_type not in detected:
                        detected.append(task_type)
                    break
        
        # 何も検出されなかった場合はconversationとする
        if not detected:
            detected.append("conversation")
        
        return detected
    
    def _generate_sub_tasks(self, detected_types: List[str], normalized_text: str) -> List[Dict]:
        """
        検出されたタスクタイプからサブタスクを生成
        
        Args:
            detected_types: 検出されたタスクタイプのリスト
            normalized_text: 正規化されたテキスト
        
        Returns:
            サブタスクのリスト
        """
        sub_tasks = []
        priority = 1
        
        # 複合タスクの場合の順序調整
        # 例: プレゼン資料作成 = 情報収集 → データ処理 → ドキュメント生成
        if "document_generation" in detected_types:
            # ドキュメント生成には事前準備が必要
            task_order = []
            
            if "information_gathering" not in detected_types:
                # 情報収集が必要
                task_order.append("information_gathering")
            
            if "data_processing" in detected_types:
                task_order.append("data_processing")
            
            task_order.append("document_generation")
            
            # 既存のdetected_typesから重複を削除して追加
            for t in detected_types:
                if t not in task_order:
                    task_order.append(t)
            
            detected_types = task_order
        
        # コード生成の場合
        elif "code_generation" in detected_types:
            task_order = ["code_generation"]
            
            # 改善も必要か
            if "code_improvement" in detected_types:
                task_order.append("code_improvement")
            
            # 既存のdetected_typesから重複を削除して追加
            for t in detected_types:
                if t not in task_order:
                    task_order.append(t)
            
            detected_types = task_order
        
        # サブタスクを生成
        for task_type in detected_types:
            if task_type in self.task_types:
                config = self.task_types[task_type]
                sub_tasks.append({
                    "type": task_type,
                    "priority": priority,
                    "description": config["description"],
                    "capability": config["capability"],
                    "estimated_minutes": config["estimated_minutes"]
                })
                priority += 1
        
        return sub_tasks
    
    def _calculate_estimated_time(self, sub_tasks: List[Dict]) -> str:
        """
        推定時間を計算
        
        Args:
            sub_tasks: サブタスクのリスト
        
        Returns:
            推定時間の文字列（例: "15分", "1時間")
        """
        total_minutes = sum(task["estimated_minutes"] for task in sub_tasks)
        
        if total_minutes < 60:
            return f"{total_minutes}分"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes == 0:
                return f"{hours}時間"
            else:
                return f"{hours}時間{minutes}分"
    
    def _assess_complexity(self, sub_tasks: List[Dict]) -> str:
        """
        タスクの複雑度を評価
        
        Args:
            sub_tasks: サブタスクのリスト
        
        Returns:
            複雑度 ("low", "medium", "high")
        """
        task_count = len(sub_tasks)
        total_minutes = sum(task["estimated_minutes"] for task in sub_tasks)
        
        if task_count == 1 and total_minutes <= 5:
            return "low"
        elif task_count <= 2 and total_minutes <= 20:
            return "medium"
        else:
            return "high"
    
    def _requires_confirmation(self, sub_tasks: List[Dict], normalized_text: str) -> bool:
        """
        確認が必要かどうかを判定
        
        Args:
            sub_tasks: サブタスクのリスト
            normalized_text: 正規化されたテキスト
        
        Returns:
            確認が必要な場合True
        """
        # 複雑度が高い場合は確認
        complexity = self._assess_complexity(sub_tasks)
        if complexity == "high":
            return True
        
        # 破壊的な操作を含む場合は確認
        destructive_keywords = ["削除", "消す", "リセット", "初期化"]
        for keyword in destructive_keywords:
            if keyword in normalized_text:
                return True
        
        return False


# テスト用のmain関数
if __name__ == "__main__":
    analyzer = TaskAnalyzer()
    
    # テストケース
    test_cases = [
        "プレゼン資料作成して",
        "データ分析して",
        "アプリ作成して",
        "コードを改善して",
        "機械学習について教えて"
    ]
    
    print("=== TaskAnalyzer テスト ===")
    for test in test_cases:
        print(f"\n入力: {test}")
        result = analyzer.analyze(test)
        print(f"メインゴール: {result['main_goal']}")
        print(f"推定時間: {result['estimated_time']}")
        print(f"複雑度: {result['complexity']}")
        print(f"サブタスク:")
        for task in result['sub_tasks']:
            print(f"  {task['priority']}. {task['description']} ({task['capability']})")
