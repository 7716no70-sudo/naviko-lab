# -*- coding: utf-8 -*-
"""
Naviko Self Growth Engine - 自己成長エンジン

このモジュールは、実行履歴を記録し、パフォーマンスを評価して自己改善を提案します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import threading
import json


class PerformanceLevel(Enum):
    """パフォーマンスレベル"""
    EXCELLENT = "excellent"    # 優秀（成功率 >= 90%）
    GOOD = "good"              # 良好（成功率 >= 70%）
    FAIR = "fair"              # 普通（成功率 >= 50%）
    POOR = "poor"              # 要改善（成功率 < 50%）


class ExecutionRecord:
    """実行記録"""
    def __init__(
        self,
        capability_name: str,
        success: bool,
        execution_time: float,
        context: Dict[str, Any],
        result: Any,
        error: Optional[str] = None
    ):
        self.capability_name = capability_name
        self.success = success
        self.execution_time = execution_time
        self.context = context
        self.result = result
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "capability_name": self.capability_name,
            "success": self.success,
            "execution_time": self.execution_time,
            "context": self.context,
            "result": str(self.result),
            "error": self.error,
            "timestamp": self.timestamp
        }


class SelfGrowthEngine:
    """
    自己成長エンジン（シングルトン）
    
    実行履歴を記録し、パフォーマンスを分析して改善提案を生成します。
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        """初期化（直接呼び出し禁止、get_instance()を使用）"""
        if SelfGrowthEngine._instance is not None:
            raise RuntimeError("SelfGrowthEngineはシングルトンです。get_instance()を使用してください。")
        
        self._execution_history: List[ExecutionRecord] = []
        self._performance_stats: Dict[str, Dict[str, Any]] = {}
        self._learning_data: Dict[str, Any] = {
            "successful_patterns": [],
            "failed_patterns": [],
            "improvement_suggestions": []
        }
    
    @classmethod
    def get_instance(cls) -> "SelfGrowthEngine":
        """シングルトンインスタンス取得"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def record_execution(
        self,
        capability_name: str,
        success: bool,
        execution_time: float,
        context: Dict[str, Any],
        result: Any,
        error: Optional[str] = None
    ):
        """
        実行記録を保存
        
        Args:
            capability_name (str): 能力名（ツール名/プラグイン名）
            success (bool): 成功したか
            execution_time (float): 実行時間（秒）
            context (Dict[str, Any]): 実行コンテキスト
            result (Any): 実行結果
            error (Optional[str]): エラーメッセージ（失敗時）
        """
        record = ExecutionRecord(
            capability_name=capability_name,
            success=success,
            execution_time=execution_time,
            context=context,
            result=result,
            error=error
        )
        
        self._execution_history.append(record)
        
        # 履歴が1000件を超えたら古いものを削除
        if len(self._execution_history) > 1000:
            self._execution_history.pop(0)
        
        # パフォーマンス統計を更新
        self._update_performance_stats(capability_name, success, execution_time)
        
        # 学習データを更新
        self._update_learning_data(record)
    
    def _update_performance_stats(self, capability_name: str, success: bool, execution_time: float):
        """パフォーマンス統計更新"""
        if capability_name not in self._performance_stats:
            self._performance_stats[capability_name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_execution_time": 0.0,
                "avg_execution_time": 0.0,
                "success_rate": 0.0
            }
        
        stats = self._performance_stats[capability_name]
        stats["total_executions"] += 1
        stats["total_execution_time"] += execution_time
        
        if success:
            stats["successful_executions"] += 1
        else:
            stats["failed_executions"] += 1
        
        # 平均実行時間と成功率を計算
        stats["avg_execution_time"] = stats["total_execution_time"] / stats["total_executions"]
        stats["success_rate"] = (stats["successful_executions"] / stats["total_executions"]) * 100
    
    def _update_learning_data(self, record: ExecutionRecord):
        """学習データ更新"""
        pattern = {
            "capability": record.capability_name,
            "context": record.context,
            "timestamp": record.timestamp
        }
        
        if record.success:
            self._learning_data["successful_patterns"].append(pattern)
            # 最大100件まで
            if len(self._learning_data["successful_patterns"]) > 100:
                self._learning_data["successful_patterns"].pop(0)
        else:
            self._learning_data["failed_patterns"].append(pattern)
            if len(self._learning_data["failed_patterns"]) > 100:
                self._learning_data["failed_patterns"].pop(0)
    
    def get_performance_level(self, capability_name: str) -> PerformanceLevel:
        """
        パフォーマンスレベル取得
        
        Args:
            capability_name (str): 能力名
        
        Returns:
            PerformanceLevel: パフォーマンスレベル
        """
        stats = self._performance_stats.get(capability_name)
        if stats is None:
            return PerformanceLevel.FAIR
        
        success_rate = stats["success_rate"]
        
        if success_rate >= 90:
            return PerformanceLevel.EXCELLENT
        elif success_rate >= 70:
            return PerformanceLevel.GOOD
        elif success_rate >= 50:
            return PerformanceLevel.FAIR
        else:
            return PerformanceLevel.POOR
    
    def generate_improvement_suggestions(self) -> List[str]:
        """
        改善提案生成
        
        Returns:
            List[str]: 改善提案リスト
        """
        suggestions = []
        
        for capability_name, stats in self._performance_stats.items():
            level = self.get_performance_level(capability_name)
            
            if level == PerformanceLevel.POOR:
                suggestions.append(
                    f"⚠️ '{capability_name}' の成功率が低い（{stats['success_rate']:.1f}%）。"
                    f"パラメータや実装の見直しを検討してください。"
                )
            
            if stats["avg_execution_time"] > 10.0:
                suggestions.append(
                    f"⏱️ '{capability_name}' の実行時間が長い（平均{stats['avg_execution_time']:.2f}秒）。"
                    f"最適化を検討してください。"
                )
        
        # 学習データに保存
        self._learning_data["improvement_suggestions"] = suggestions
        
        return suggestions
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        実行履歴取得
        
        Args:
            limit (int): 取得件数
        
        Returns:
            List[Dict[str, Any]]: 実行履歴（新しい順）
        """
        return [record.to_dict() for record in self._execution_history[-limit:]][::-1]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        パフォーマンスレポート取得
        
        Returns:
            Dict[str, Any]: パフォーマンスレポート
        """
        total_executions = sum(stats["total_executions"] for stats in self._performance_stats.values())
        total_successful = sum(stats["successful_executions"] for stats in self._performance_stats.values())
        
        overall_success_rate = (total_successful / total_executions * 100) if total_executions > 0 else 0.0
        
        return {
            "total_executions": total_executions,
            "total_successful": total_successful,
            "overall_success_rate": overall_success_rate,
            "capability_stats": self._performance_stats.copy(),
            "improvement_suggestions": self.generate_improvement_suggestions()
        }
    
    def export_learning_data(self) -> str:
        """
        学習データをJSON形式でエクスポート
        
        Returns:
            str: JSON文字列
        """
        export_data = {
            "performance_stats": self._performance_stats,
            "learning_data": self._learning_data,
            "export_timestamp": datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def print_status(self):
        """状態表示"""
        report = self.get_performance_report()
        
        print("\n" + "=" * 60)
        print("🌱 Naviko Self Growth Engine Status")
        print("=" * 60)
        print(f"総実行回数: {report['total_executions']} 回")
        print(f"成功回数: {report['total_successful']} 回")
        print(f"全体成功率: {report['overall_success_rate']:.1f}%")
        print()
        
        if report["capability_stats"]:
            print("能力別パフォーマンス:")
            for capability, stats in sorted(report["capability_stats"].items()):
                level = self.get_performance_level(capability)
                level_emoji = {
                    PerformanceLevel.EXCELLENT: "🌟",
                    PerformanceLevel.GOOD: "✅",
                    PerformanceLevel.FAIR: "⚠️",
                    PerformanceLevel.POOR: "❌"
                }[level]
                
                print(f"  {level_emoji} {capability}")
                print(f"     実行: {stats['total_executions']}回, "
                      f"成功率: {stats['success_rate']:.1f}%, "
                      f"平均時間: {stats['avg_execution_time']:.2f}秒")
        
        print()
        
        if report["improvement_suggestions"]:
            print("改善提案:")
            for suggestion in report["improvement_suggestions"]:
                print(f"  {suggestion}")
        else:
            print("✅ 改善提案なし（すべて良好）")
        
        print("=" * 60)


__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["SelfGrowthEngine", "PerformanceLevel", "ExecutionRecord"]
