#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GoalDecomposer - Navikoゴール分解システム

メインゴールを複数のサブゴールに分解し、実行可能なタスクに落とし込む。
CapabilitySelectorへの入力データを準備する。

機能:
  - メインゴールの分解
  - サブゴール生成
  - 依存関係の定義
  - 実行順序の決定
  - サブゴールの優先度設定

例:
  decomposer = GoalDecomposer("Flaskを使ってWebアプリを作成してください")
  goals = decomposer.decompose()
  # {"main_goal": "Webアプリ作成", "sub_goals": ["環境構築", "基本コード作成", "テスト"]}
"""

import re
from typing import Dict, List, Optional, Any


class GoalDecomposer:
    """
    ゴール分解システム
    
    メインゴールを分解して実行可能な
    サブゴールのリストを生成する。
    """
    
    # インテント別の標準サブゴールテンプレート
    INTENT_TEMPLATES = {
        "create": [
            "要件定義",
            "設計・構造決定",
            "環境構築",
            "基本実装",
            "テスト・検証",
            "ドキュメント作成"
        ],
        "analyze": [
            "データ収集",
            "データクリーニング",
            "探索的分析",
            "可視化",
            "レポート作成"
        ],
        "execute": [
            "環境確認",
            "実行準備",
            "実行",
            "結果確認",
            "ログ記録"
        ],
        "modify": [
            "現状確認",
            "変更箇所特定",
            "修正実装",
            "テスト",
            "反映"
        ],
        "search": [
            "検索クエリ作成",
            "情報収集",
            "フィルタリング",
            "結果整理"
        ]
    }
    
    # 技術スタック別の追加サブゴール
    TECH_SPECIFIC_GOALS = {
        "flask": ["Flaskアプリケーション構造作成", "ルート定義", "テンプレート作成"],
        "django": ["Djangoプロジェクト作成", "モデル定義", "ビュー・URLconf設定"],
        "react": ["Reactアプリ初期化", "コンポーネント作成", "状態管理設定"],
        "database": ["データベース設計", "スキーマ定義", "マイグレーション"],
        "api": ["API設計", "エンドポイント実装", "認証設定"],
        "machine_learning": ["データ前処理", "モデル選択", "学習・評価", "最適化"],
    }
    
    def __init__(self, user_input: str, intent: str = "unknown"):
        """
        GoalDecomposerの初期化
        
        Args:
            user_input: ユーザーの入力テキスト
            intent: インテント（未指定の場合は自動推定）
        """
        self.user_input = user_input if user_input else ""
        self.intent = intent
        self.main_goal = ""
        self.sub_goals = []
        self.dependencies = {}
    
    def _extract_main_goal(self) -> str:
        """
        メインゴールを抽出
        
        Returns:
            メインゴール文字列
        """
        # ユーザー入力から不要な部分を削除
        goal = self.user_input
        
        # 敬語・依頼表現を削除
        goal = re.sub(r'(してください|お願いします|してほしい|したい)$', '', goal)
        goal = re.sub(r'^(できれば|可能なら|もし可能なら)', '', goal)
        
        # 長すぎる場合は最初の50文字まで
        if len(goal) > 50:
            goal = goal[:50] + "..."
        
        self.main_goal = goal.strip()
        return self.main_goal
    
    def _generate_base_sub_goals(self) -> List[str]:
        """
        インテントに基づいて基本サブゴールを生成
        
        Returns:
            サブゴールのリスト
        """
        # インテントが不明な場合はcreateとして扱う
        if self.intent == "unknown":
            self.intent = "create"
        
        # テンプレートから基本サブゴールを取得
        template = self.INTENT_TEMPLATES.get(self.intent, self.INTENT_TEMPLATES["create"])
        
        return template.copy()
    
    def _add_tech_specific_goals(self, base_goals: List[str]) -> List[str]:
        """
        技術スタック固有のサブゴールを追加
        
        Args:
            base_goals: 基本サブゴールのリスト
        
        Returns:
            技術固有のゴールを追加したリスト
        """
        enhanced_goals = base_goals.copy()
        
        # 入力から技術スタックを検出
        for tech, goals in self.TECH_SPECIFIC_GOALS.items():
            if tech in self.user_input.lower():
                # 「基本実装」の後に技術固有のゴールを挿入
                if "基本実装" in enhanced_goals:
                    idx = enhanced_goals.index("基本実装") + 1
                    for goal in reversed(goals):
                        enhanced_goals.insert(idx, goal)
                else:
                    enhanced_goals.extend(goals)
        
        return enhanced_goals
    
    def _simplify_goals(self, goals: List[str]) -> List[str]:
        """
        複雑度に応じてサブゴールを簡略化
        
        Args:
            goals: サブゴールのリスト
        
        Returns:
            簡略化されたサブゴールのリスト
        """
        # 簡単さを示すキーワード
        simple_keywords = ["簡単", "シンプル", "基本", "単純", "最小限"]
        
        if any(keyword in self.user_input for keyword in simple_keywords):
            # 基本的なステップのみに絞る
            essential_goals = []
            essential_steps = ["要件定義", "基本実装", "テスト", "実行", "結果確認"]
            
            for goal in goals:
                if any(step in goal for step in essential_steps):
                    essential_goals.append(goal)
            
            # 最低3ステップは確保
            if len(essential_goals) < 3:
                return goals[:3]
            
            return essential_goals
        
        return goals
    
    def _define_dependencies(self, sub_goals: List[str]) -> Dict[str, List[str]]:
        """
        サブゴール間の依存関係を定義
        
        Args:
            sub_goals: サブゴールのリスト
        
        Returns:
            依存関係辞書（サブゴール: [前提となるサブゴールのリスト]）
        """
        dependencies = {}
        
        # 基本的には順次実行
        for i, goal in enumerate(sub_goals):
            if i == 0:
                dependencies[goal] = []
            else:
                dependencies[goal] = [sub_goals[i-1]]
        
        # 特定のパターンでは並列実行可能
        parallel_patterns = [
            (["データ収集", "環境構築"], ["要件定義"]),
            (["テスト", "ドキュメント作成"], ["基本実装"]),
        ]
        
        for parallel_goals, prereq in parallel_patterns:
            parallel_in_list = [g for g in parallel_goals if g in sub_goals]
            prereq_in_list = [g for g in prereq if g in sub_goals]
            
            if len(parallel_in_list) >= 2 and prereq_in_list:
                for goal in parallel_in_list:
                    dependencies[goal] = prereq_in_list
        
        self.dependencies = dependencies
        return dependencies
    
    def decompose(self) -> Dict[str, Any]:
        """
        メインゴールを分解して実行可能なサブゴールを生成
        
        Returns:
            分解結果（メインゴール、サブゴール、依存関係）
        """
        # メインゴールを抽出
        main_goal = self._extract_main_goal()
        
        # 基本サブゴールを生成
        base_goals = self._generate_base_sub_goals()
        
        # 技術固有のゴールを追加
        enhanced_goals = self._add_tech_specific_goals(base_goals)
        
        # 複雑度に応じて簡略化
        simplified_goals = self._simplify_goals(enhanced_goals)
        
        # 依存関係を定義
        dependencies = self._define_dependencies(simplified_goals)
        
        self.sub_goals = simplified_goals
        
        return {
            "main_goal": main_goal,
            "sub_goals": simplified_goals,
            "dependencies": dependencies,
            "total_steps": len(simplified_goals)
        }
    
    def get_execution_order(self) -> List[List[str]]:
        """
        実行順序を取得（並列実行可能なものはグループ化）
        
        Returns:
            実行順序のリスト（各要素は並列実行可能なサブゴールのリスト）
        """
        if not self.dependencies:
            self.decompose()
        
        # トポロジカルソート風のアルゴリズム
        execution_order = []
        completed = set()
        
        while len(completed) < len(self.sub_goals):
            # 前提条件が全て完了しているサブゴールを抽出
            ready = []
            for goal in self.sub_goals:
                if goal in completed:
                    continue
                prereqs = self.dependencies.get(goal, [])
                if all(p in completed for p in prereqs):
                    ready.append(goal)
            
            if not ready:
                # デッドロック回避（依存関係がおかしい場合）
                remaining = [g for g in self.sub_goals if g not in completed]
                ready = remaining[:1]
            
            execution_order.append(ready)
            completed.update(ready)
        
        return execution_order
    
    def get_summary(self) -> str:
        """
        分解結果のサマリーを取得
        
        Returns:
            サマリー文字列
        """
        if not self.sub_goals:
            self.decompose()
        
        return f"メインゴール: {self.main_goal} | サブゴール数: {len(self.sub_goals)}"


if __name__ == "__main__":
    # テストコード
    print("=" * 60)
    print("GoalDecomposer - Navikoゴール分解システム")
    print("=" * 60)
    print()
    
    test_cases = [
        ("Flaskを使ってWebアプリケーションを作成してください", "create"),
        ("売上データを分析して可視化してください", "analyze"),
        ("機械学習モデルを開発して予測を実行してください", "create"),
        ("このエラーを修正してください", "modify"),
        ("簡単なPythonスクリプトを書いてください", "create"),
    ]
    
    for i, (test_input, intent) in enumerate(test_cases, 1):
        print(f"【テストケース{i}】")
        print(f"入力: {test_input}")
        print(f"インテント: {intent}")
        print()
        
        decomposer = GoalDecomposer(test_input, intent)
        result = decomposer.decompose()
        
        print("分解結果:")
        print(f"  メインゴール: {result['main_goal']}")
        print(f"  サブゴール数: {result['total_steps']}")
        print()
        
        print("  サブゴール:")
        for j, goal in enumerate(result['sub_goals'], 1):
            prereqs = result['dependencies'].get(goal, [])
            if prereqs:
                print(f"    {j}. {goal} (前提: {', '.join(prereqs)})")
            else:
                print(f"    {j}. {goal}")
        print()
        
        print("  実行順序:")
        execution_order = decomposer.get_execution_order()
        for level, goals in enumerate(execution_order, 1):
            if len(goals) == 1:
                print(f"    Level {level}: {goals[0]}")
            else:
                print(f"    Level {level}: {', '.join(goals)} (並列実行可能)")
        
        print("-" * 60)
        print()
    
    print("🎉 全てのテストケースが完了しました！")
