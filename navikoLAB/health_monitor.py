# health_monitor.py
"""
ナビ子の健康状態監視モジュール
"""


class HealthMonitor:
    """システムの健康状態を監視するクラス"""
    
    def __init__(self):
        self.health_data = {
            "system_health": "良好",
            "health_score": 0.85,
            "warnings": []
        }
    
    def latest(self):
        """最新の健康状態を取得"""
        return {
            "system_health": self.health_data.get("system_health", "不明"),
            "health_score": self.health_data.get("health_score", 0.5),
            "warnings": self.health_data.get("warnings", []),
            "timestamp": "2024-01-01 00:00:00"
        }
    
    def summary(self):
        """健康状態のサマリーを取得"""
        latest = self.latest()
        return f"システム状態: {latest['system_health']}, スコア: {latest['health_score']}, 警告数: {len(latest['warnings'])}"
