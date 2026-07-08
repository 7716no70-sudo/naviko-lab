# -*- coding: utf-8 -*-
"""
Naviko Self Growth Engine - 自己成長エンジン

このモジュールは、実行結果を学習し、パフォーマンスを評価・改善します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import threading


class PerformanceRecord:
    """パフォーマンス記録"""
    
    def __init__(
        self,
        capability_name: str,
        success: bool,
        execution_time: float,
        context: Dict[str, Any],
        result: Any,
        timestamp: Optional[datetime] = None
    ):
        self.capability_name = capability_name
        self.success = success
        self.execution_time = execution_time
        self.context = context
        self.result = result
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "capability_name": self.capability_name,
            "success": self.success,
            "execution_time": self.execution_time,
            "context": self.context,
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat()
        }


class SelfGrowthEngine:
    """
    自己成長エンジン（シングルトン）
    
    実行結果を記録・分析し、パフォーマンスを評価して改善提案を行います。
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        """初期化（直接呼び出し禁止、get_instance()を使用）"""
        if SelfGrowthEngine._instance is not None:
            raise RuntimeError("SelfGrowthEngineはシングルトンです。get_instance()を使用してください。")
        
        self._records: List[PerformanceRecord] = []
        self._capability_stats: Dict[str, Dict[str, Any]] = {}
        self._improvement_suggestions: List[Dict[str, Any]] = []
    
    @classmethod
    def get_instance(cls) -> "SelfGrowthEngine":
        """シングルトンインスタンス取得"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def record_performance(
        self,
        capability_name: str,
        success: bool,
        execution_time: float,
        context: Dict[str, Any],
        result: Any
    ):
        """
        パフォーマンス記録
        
        Args:
            capability_name (str): 能力名（ツール/プラグイン名）
            success (bool): 成功フラグ
            execution_time (float): 実行時間（秒）
            context (Dict[str, Any]): コンテキスト情報
            result (Any): 実行結果
        """
        record = PerformanceRecord(
            capability_name=capability_name,
            success=success,
            execution_time=execution_time,
            context=context,
            result=result
        )
        
        self._records.append(record)
        
        # 統計更新
        self._update_capability_stats(record)
        
        # 履歴が1000件を超えたら古いものを削除
        if len(self._records) > 1000:
            self._records.pop(0)
    
    def _update_capability_stats(self, record: PerformanceRecord):
        """能力統計更新"""
        name = record.capability_name
        
        if name not in self._capability_stats:
            self._capability_stats[name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_execution_time": 0.0,
                "avg_execution_time": 0.0,
                "success_rate": 0.0
            }
        
        stats = self._capability_stats[name]
        stats["total_executions"] += 1
        
        if record.success:
            stats["successful_executions"] += 1
        else:
            stats["failed_executions"] += 1
        
        stats["total_execution_time"] += record.execution_time
        stats["avg_execution_time"] = stats["total_execution_time"] / stats["total_executions"]
        stats["success_rate"] = stats["successful_executions"] / stats["total_executions"] * 100
    
    def analyze_performance(self, capability_name: Optional[str] = None) -> Dict[str, Any]:
        """
        パフォーマンス分析
        
        Args:
            capability_name (Optional[str]): 分析対象の能力名（Noneの場合は全体）
        
        Returns:
            Dict[str, Any]: 分析結果
        """
        if capability_name:
            # 特定能力の分析
            stats = self._capability_stats.get(capability_name, {})
            return {
                "capability_name": capability_name,
                "stats": stats,
                "recommendations": self._generate_recommendations(capability_name)
            }
        else:
            # 全体の分析
            total_executions = sum(s["total_executions"] for s in self._capability_stats.values())
            total_success = sum(s["successful_executions"] for s in self._capability_stats.values())
            
            return {
                "total_executions": total_executions,
                "total_success": total_success,
                "overall_success_rate": (total_success / total_executions * 100) if total_executions > 0 else 0,
                "capability_count": len(self._capability_stats),
                "top_performers": self._get_top_performers(5),
                "improvement_needed": self._get_improvement_needed(5)
            }
    
    def _generate_recommendations(self, capability_name: str) -> List[str]:
        """改善提案生成"""
        stats = self._capability_stats.get(capability_name)
        if not stats:
            return []
        
        recommendations = []
        
        # 成功率が低い
        if stats["success_rate"] < 50:
            recommendations.append(f"成功率が{stats['success_rate']:.1f}%と低いです。エラーハンドリングの改善を検討してください。")
        
        # 実行時間が長い
        if stats["avg_execution_time"] > 5.0:
            recommendations.append(f"平均実行時間が{stats['avg_execution_time']:.2f}秒と長いです。パフォーマンス最適化を検討してください。")
        
        # 実行回数が少ない
        if stats["total_executions"] < 5:
            recommendations.append("実行回数が少ないため、統計的な信頼性が低いです。")
        
        return recommendations
    
    def _get_top_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """高パフォーマンス能力取得"""
        sorted_stats = sorted(
            self._capability_stats.items(),
            key=lambda x: (x[1]["success_rate"], -x[1]["avg_execution_time"]),
            reverse=True
        )
        
        return [
            {
                "name": name,
                "success_rate": stats["success_rate"],
                "avg_execution_time": stats["avg_execution_time"]
            }
            for name, stats in sorted_stats[:limit]
        ]
    
    def _get_improvement_needed(self, limit: int = 5) -> List[Dict[str, Any]]:
        """改善が必要な能力取得"""
        sorted_stats = sorted(
            self._capability_stats.items(),
            key=lambda x: (x[1]["success_rate"], -x[1]["avg_execution_time"])
        )
        
        return [
            {
                "name": name,
                "success_rate": stats["success_rate"],
                "avg_execution_time": stats["avg_execution_time"],
                "recommendations": self._generate_recommendations(name)
            }
            for name, stats in sorted_stats[:limit]
        ]
    
    def get_learning_data(self) -> Dict[str, Any]:
        """
        学習データ取得
        
        Returns:
            Dict[str, Any]: 学習データ
        """
        return {
            "total_records": len(self._records),
            "capability_stats": self._capability_stats.copy(),
            "improvement_suggestions": self._improvement_suggestions.copy()
        }
    
    def export_data(self, file_path: str):
        """
        データをJSONファイルにエクスポート
        
        Args:
            file_path (str): 出力ファイルパス
        """
        data = {
            "records": [r.to_dict() for r in self._records],
            "capability_stats": self._capability_stats,
            "improvement_suggestions": self._improvement_suggestions,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def print_status(self):
        """状態表示"""
        analysis = self.analyze_performance()
        
        print("\n" + "=" * 60)
        print("🌱 Naviko Self Growth Engine Status")
        print("=" * 60)
        print(f"総実行回数: {analysis['total_executions']} 回")
        print(f"成功回数: {analysis['total_success']} 回")
        print(f"全体成功率: {analysis['overall_success_rate']:.1f}%")
        print(f"登録能力数: {analysis['capability_count']}")
        print()
        
        if analysis['top_performers']:
            print("🏆 トップパフォーマー:")
            for i, perf in enumerate(analysis['top_performers'], 1):
                print(f"  {i}. {perf['name']}")
                print(f"     成功率: {perf['success_rate']:.1f}%, 平均時間: {perf['avg_execution_time']:.2f}秒")
        
        print()
        
        if analysis['improvement_needed']:
            print("⚠️ 改善が必要:")
            for i, item in enumerate(analysis['improvement_needed'], 1):
                print(f"  {i}. {item['name']}")
                print(f"     成功率: {item['success_rate']:.1f}%, 平均時間: {item['avg_execution_time']:.2f}秒")
                if item['recommendations']:
                    for rec in item['recommendations']:
                        print(f"     💡 {rec}")
        
        print("=" * 60)


__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["SelfGrowthEngine", "PerformanceRecord"]
