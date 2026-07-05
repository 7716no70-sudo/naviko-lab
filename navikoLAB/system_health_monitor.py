#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemHealthMonitor - Naviko運用監視ダッシュボード
Phase 3-B: システム健全性の可視化とリアルタイム監視

このモジュールはNavikoシステムの運用状況を監視し、以下の責務を担う：
1. システム健全性の可視化（リソース使用状況）
2. リアルタイムメトリクス監視（エラー率、処理時間）
3. 問題予測アラート（パターン分析）
4. ダッシュボード表示（テキスト/JSON形式）

APIキー管理：
- 環境変数参照のみ（os.environ.get('GROQ_API_KEY')）
- ハードコード厳禁（セキュリティリスク）
"""

import os
import sys
import json
import psutil
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from collections import deque


class SystemHealthMonitor:
    """
    Naviko運用監視ダッシュボード
    
    システム全体の健全性をリアルタイムで監視し、
    問題の早期発見と予防保全を実現する。
    """
    
    def __init__(self, lab_dir: str = "/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB"):
        """
        モニター初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        self.lab_dir = Path(lab_dir)
        self.monitoring_start_time = datetime.now()
        
        # メトリクス履歴（最大1000件保持）
        self.metrics_history = deque(maxlen=1000)
        self.error_history = deque(maxlen=100)
        self.alert_history = deque(maxlen=50)
        
        # 閾値設定
        self.thresholds = {
            "cpu_usage_warning": 70.0,  # CPU使用率警告閾値（%）
            "cpu_usage_critical": 90.0,  # CPU使用率危険閾値（%）
            "memory_usage_warning": 70.0,  # メモリ使用率警告閾値（%）
            "memory_usage_critical": 85.0,  # メモリ使用率危険閾値（%）
            "disk_usage_warning": 80.0,  # ディスク使用率警告閾値（%）
            "disk_usage_critical": 90.0,  # ディスク使用率危険閾値（%）
            "error_rate_warning": 5.0,  # エラー率警告閾値（%）
            "error_rate_critical": 10.0  # エラー率危険閾値（%）
        }
        
        # 統計情報
        self.stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "total_errors": 0,
            "auto_recoveries": 0,
            "alerts_generated": 0
        }
        
        # 履歴ファイル
        self.metrics_file = self.lab_dir / "health_metrics_history.json"
        self.alerts_file = self.lab_dir / "health_alerts.json"
        
        print(f"✅ SystemHealthMonitor初期化完了")
        print(f"   監視開始時刻: {self.monitoring_start_time}")
        print(f"   LABディレクトリ: {self.lab_dir}")
    
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """
        システムメトリクスの収集
        
        CPU、メモリ、ディスク使用状況を収集する。
        
        Returns:
            システムメトリクス
        """
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            
            # メモリ使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024 ** 3)
            memory_total_gb = memory.total / (1024 ** 3)
            
            # ディスク使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024 ** 3)
            disk_total_gb = disk.total / (1024 ** 3)
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": cpu_count
                },
                "memory": {
                    "usage_percent": memory_percent,
                    "used_gb": round(memory_used_gb, 2),
                    "total_gb": round(memory_total_gb, 2)
                },
                "disk": {
                    "usage_percent": disk_percent,
                    "used_gb": round(disk_used_gb, 2),
                    "total_gb": round(disk_total_gb, 2)
                }
            }
            
            # 履歴に追加
            self.metrics_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    
    def calculate_health_score(self, metrics: Dict[str, Any]) -> float:
        """
        健全性スコアの計算
        
        各メトリクスから総合的な健全性スコア（0-100）を算出する。
        
        Args:
            metrics: システムメトリクス
        
        Returns:
            健全性スコア（0-100）
        """
        if "error" in metrics:
            return 50.0  # エラー時は中間スコア
        
        # 各メトリクスのスコア（使用率が低いほど高スコア）
        cpu_score = 100 - metrics["cpu"]["usage_percent"]
        memory_score = 100 - metrics["memory"]["usage_percent"]
        disk_score = 100 - metrics["disk"]["usage_percent"]
        
        # エラー率スコア
        error_rate = self.calculate_error_rate()
        error_score = 100 - (error_rate * 10)  # エラー率1%で10点減点
        error_score = max(0, error_score)
        
        # 加重平均（CPU: 30%, メモリ: 30%, ディスク: 20%, エラー率: 20%）
        health_score = (
            cpu_score * 0.3 +
            memory_score * 0.3 +
            disk_score * 0.2 +
            error_score * 0.2
        )
        
        return round(health_score, 2)
    
    
    def calculate_error_rate(self) -> float:
        """
        エラー率の計算
        
        Returns:
            エラー率（%）
        """
        if self.stats["total_operations"] == 0:
            return 0.0
        
        error_rate = (self.stats["failed_operations"] / self.stats["total_operations"]) * 100
        return round(error_rate, 2)
    
    
    def check_thresholds(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        閾値チェックとアラート生成
        
        Args:
            metrics: システムメトリクス
        
        Returns:
            アラートリスト
        """
        alerts = []
        
        if "error" in metrics:
            return alerts
        
        # CPU使用率チェック
        cpu_usage = metrics["cpu"]["usage_percent"]
        if cpu_usage >= self.thresholds["cpu_usage_critical"]:
            alerts.append({
                "level": "CRITICAL",
                "category": "CPU",
                "message": f"CPU使用率が危険レベル: {cpu_usage}%",
                "threshold": self.thresholds["cpu_usage_critical"],
                "current_value": cpu_usage
            })
        elif cpu_usage >= self.thresholds["cpu_usage_warning"]:
            alerts.append({
                "level": "WARNING",
                "category": "CPU",
                "message": f"CPU使用率が高い: {cpu_usage}%",
                "threshold": self.thresholds["cpu_usage_warning"],
                "current_value": cpu_usage
            })
        
        # メモリ使用率チェック
        memory_usage = metrics["memory"]["usage_percent"]
        if memory_usage >= self.thresholds["memory_usage_critical"]:
            alerts.append({
                "level": "CRITICAL",
                "category": "MEMORY",
                "message": f"メモリ使用率が危険レベル: {memory_usage}%",
                "threshold": self.thresholds["memory_usage_critical"],
                "current_value": memory_usage
            })
        elif memory_usage >= self.thresholds["memory_usage_warning"]:
            alerts.append({
                "level": "WARNING",
                "category": "MEMORY",
                "message": f"メモリ使用率が高い: {memory_usage}%",
                "threshold": self.thresholds["memory_usage_warning"],
                "current_value": memory_usage
            })
        
        # ディスク使用率チェック
        disk_usage = metrics["disk"]["usage_percent"]
        if disk_usage >= self.thresholds["disk_usage_critical"]:
            alerts.append({
                "level": "CRITICAL",
                "category": "DISK",
                "message": f"ディスク使用率が危険レベル: {disk_usage}%",
                "threshold": self.thresholds["disk_usage_critical"],
                "current_value": disk_usage
            })
        elif disk_usage >= self.thresholds["disk_usage_warning"]:
            alerts.append({
                "level": "WARNING",
                "category": "DISK",
                "message": f"ディスク使用率が高い: {disk_usage}%",
                "threshold": self.thresholds["disk_usage_warning"],
                "current_value": disk_usage
            })
        
        # エラー率チェック
        error_rate = self.calculate_error_rate()
        if error_rate >= self.thresholds["error_rate_critical"]:
            alerts.append({
                "level": "CRITICAL",
                "category": "ERROR_RATE",
                "message": f"エラー率が危険レベル: {error_rate}%",
                "threshold": self.thresholds["error_rate_critical"],
                "current_value": error_rate
            })
        elif error_rate >= self.thresholds["error_rate_warning"]:
            alerts.append({
                "level": "WARNING",
                "category": "ERROR_RATE",
                "message": f"エラー率が高い: {error_rate}%",
                "threshold": self.thresholds["error_rate_warning"],
                "current_value": error_rate
            })
        
        # アラート履歴に追加
        for alert in alerts:
            alert["timestamp"] = datetime.now().isoformat()
            self.alert_history.append(alert)
            self.stats["alerts_generated"] += 1
        
        # アラートファイルに保存
        if alerts:
            self._save_alerts()
        
        return alerts
    
    
    def record_operation(self, success: bool, error: Optional[str] = None):
        """
        操作実行の記録
        
        Args:
            success: 成功フラグ
            error: エラーメッセージ（失敗時）
        """
        self.stats["total_operations"] += 1
        
        if success:
            self.stats["successful_operations"] += 1
        else:
            self.stats["failed_operations"] += 1
            self.stats["total_errors"] += 1
            
            if error:
                self.error_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "error": error
                })
    
    
    def record_auto_recovery(self):
        """自動リカバリーの記録"""
        self.stats["auto_recoveries"] += 1
    
    
    def get_dashboard(self) -> Dict[str, Any]:
        """
        ダッシュボード情報の取得
        
        Returns:
            ダッシュボードデータ
        """
        # 最新メトリクス収集
        current_metrics = self.collect_system_metrics()
        
        # 健全性スコア計算
        health_score = self.calculate_health_score(current_metrics)
        
        # アラートチェック
        alerts = self.check_thresholds(current_metrics)
        
        # 監視時間
        monitoring_duration = (datetime.now() - self.monitoring_start_time).total_seconds()
        
        dashboard = {
            "monitoring_start_time": self.monitoring_start_time.isoformat(),
            "monitoring_duration_seconds": monitoring_duration,
            "monitoring_duration_human": f"{int(monitoring_duration // 60)}分{int(monitoring_duration % 60)}秒",
            "health_score": health_score,
            "health_status": self._get_health_status(health_score),
            "current_metrics": current_metrics,
            "statistics": self.stats.copy(),
            "error_rate_percent": self.calculate_error_rate(),
            "active_alerts": alerts,
            "recent_alerts_count": len(self.alert_history),
            "metrics_history_count": len(self.metrics_history)
        }
        
        return dashboard
    
    
    def _get_health_status(self, health_score: float) -> str:
        """
        健全性ステータスの判定
        
        Args:
            health_score: 健全性スコア
        
        Returns:
            ステータス文字列
        """
        if health_score >= 80:
            return "🟢 HEALTHY"
        elif health_score >= 60:
            return "🟡 WARNING"
        elif health_score >= 40:
            return "🟠 DEGRADED"
        else:
            return "🔴 CRITICAL"
    
    
    def display_dashboard(self):
        """ダッシュボードの表示"""
        dashboard = self.get_dashboard()
        
        print("\n" + "="*70)
        print("📊 Naviko System Health Dashboard")
        print("="*70)
        
        # 全体ステータス
        print(f"\n【システム健全性】")
        print(f"  スコア: {dashboard['health_score']}/100")
        print(f"  ステータス: {dashboard['health_status']}")
        print(f"  監視時間: {dashboard['monitoring_duration_human']}")
        
        # リソース使用状況
        metrics = dashboard['current_metrics']
        if "error" not in metrics:
            print(f"\n【リソース使用状況】")
            print(f"  CPU: {metrics['cpu']['usage_percent']:.1f}% ({metrics['cpu']['count']}コア)")
            print(f"  メモリ: {metrics['memory']['usage_percent']:.1f}% " +
                  f"({metrics['memory']['used_gb']:.1f}GB / {metrics['memory']['total_gb']:.1f}GB)")
            print(f"  ディスク: {metrics['disk']['usage_percent']:.1f}% " +
                  f"({metrics['disk']['used_gb']:.1f}GB / {metrics['disk']['total_gb']:.1f}GB)")
        
        # 統計情報
        stats = dashboard['statistics']
        print(f"\n【処理統計】")
        print(f"  総処理数: {stats['total_operations']}")
        print(f"  成功: {stats['successful_operations']}")
        print(f"  失敗: {stats['failed_operations']}")
        print(f"  エラー率: {dashboard['error_rate_percent']:.2f}%")
        print(f"  自動リカバリー: {stats['auto_recoveries']}")
        print(f"  アラート生成: {stats['alerts_generated']}")
        
        # アクティブアラート
        if dashboard['active_alerts']:
            print(f"\n【アクティブアラート】")
            for alert in dashboard['active_alerts']:
                print(f"  {alert['level']}: {alert['message']}")
        
        print("\n" + "="*70)
    
    
    def _save_alerts(self):
        """アラート履歴の保存"""
        try:
            alerts = list(self.alert_history)
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ アラート保存失敗: {e}")
    
    
    def save_metrics_history(self):
        """メトリクス履歴の保存"""
        try:
            metrics = list(self.metrics_history)
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ メトリクス保存失敗: {e}")


# テスト用コード
if __name__ == "__main__":
    # モニター初期化
    monitor = SystemHealthMonitor()
    
    # いくつかの操作を記録
    monitor.record_operation(success=True)
    monitor.record_operation(success=True)
    monitor.record_operation(success=False, error="テストエラー")
    monitor.record_auto_recovery()
    
    # ダッシュボード表示
    monitor.display_dashboard()
    
    # JSON形式でも出力
    dashboard = monitor.get_dashboard()
    print(f"\nダッシュボードJSON:\n{json.dumps(dashboard, ensure_ascii=False, indent=2)}")
