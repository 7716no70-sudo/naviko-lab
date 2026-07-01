# autonomous_goal_engine.py
"""
ナビ子の自律ゴール生成エンジン
"""


class AutonomousGoalEngine:
    """現在の状態から改善ゴールを自動生成するクラス"""
    
    def __init__(self):
        self.generated_goals = []
    
    def generate(self, current_state):
        """現在の状態から改善ゴールを生成
        
        Args:
            current_state: 現在のシステム状態（辞書形式）
        
        Returns:
            生成されたゴールのリスト
        """
        health_score = current_state.get("health_score", 0.5)
        warnings = current_state.get("warnings", [])
        
        goals = []
        
        # 健康スコアが低い場合
        if health_score < 0.7:
            goals.append({
                "type": "health_improvement",
                "priority": "高",
                "description": "システム健康スコアを0.8以上に改善する",
                "target_score": 0.8
            })
        
        # 警告がある場合
        if warnings:
            goals.append({
                "type": "warning_resolution",
                "priority": "中",
                "description": f"{len(warnings)}件の警告を解決する",
                "warning_count": len(warnings)
            })
        
        # 常に含まれる基本ゴール
        goals.append({
            "type": "continuous_improvement",
            "priority": "低",
            "description": "継続的な機能改善を実施する"
        })
        
        self.generated_goals.extend(goals)
        
        return goals
    
    def get_goals_history(self):
        """これまでに生成したゴールの履歴を取得"""
        return self.generated_goals
