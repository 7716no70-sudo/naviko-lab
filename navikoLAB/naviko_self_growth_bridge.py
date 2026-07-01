# naviko_self_growth_bridge.py
"""
ナビ子の自己成長機能ブリッジ
health_monitor, autonomous_cycle_manager, autonomous_goal_engine を統合
"""

from .health_monitor import HealthMonitor
from .autonomous_cycle_manager import AutonomousCycleManager
from .autonomous_goal_engine import AutonomousGoalEngine


class NavikoSelfGrowthBridge:
    """ナビ子の自己成長機能を統合するブリッジクラス"""
    
    def __init__(self):
        self.health_monitor = HealthMonitor()
        self.cycle_manager = AutonomousCycleManager()
        self.goal_engine = AutonomousGoalEngine()
    
    def self_diagnose(self):
        """自己診断を実行"""
        latest_health = self.health_monitor.latest()
        summary = self.health_monitor.summary()
        
        return {
            "health_status": latest_health.get("system_health", "unknown"),
            "health_score": latest_health.get("health_score", 0.5),
            "warnings": latest_health.get("warnings", []),
            "summary": summary
        }
    
    def self_improve(self):
        """自己改善サイクルを実行"""
        # 現在の状態を取得
        current_state = self.self_diagnose()
        
        # ゴールを生成
        goals = self.goal_engine.generate(current_state)
        
        # 自律サイクルを実行
        cycle_result = self.cycle_manager.run_cycle()
        
        return {
            "goals": goals,
            "cycle_result": cycle_result,
            "new_state": self.self_diagnose()
        }
    
    def get_status(self):
        """現在の状態を取得"""
        return self.self_diagnose()


# 使用例
if __name__ == "__main__":
    bridge = NavikoSelfGrowthBridge()
    
    print("=== 自己診断 ===")
    diagnosis = bridge.self_diagnose()
    print(f"健康状態: {diagnosis['health_status']}")
    print(f"健康スコア: {diagnosis['health_score']}")
    print(f"警告: {diagnosis['warnings']}")
    
    print("\n=== 自己改善 ===")
    improvement = bridge.self_improve()
    print(f"生成されたゴール: {improvement['goals']}")
    print(f"サイクル状態: {improvement['cycle_result']['status']}")
