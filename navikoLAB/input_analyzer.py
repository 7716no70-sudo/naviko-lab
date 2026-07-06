#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InputAnalyzer - Naviko入力解析システム

ユーザーの入力テキストを解析し、インテント（意図）とエンティティ（キーワード）を抽出する。
GoalDecomposerへの入力データを準備する。

機能:
  - インテント分類（create, analyze, execute, search, help等）
  - エンティティ抽出（キーワード、ファイル名、技術スタック等）
  - 優先度判定
  - 複雑度評価

例:
  analyzer = InputAnalyzer("Flaskを使ってWebアプリを作成してください")
  intent = analyzer.classify_intent()  # "create"
  entities = analyzer.extract_entities()  # {"技術スタック": ["Flask"], "成果物": ["Webアプリ"]}
  priority = analyzer.get_priority()  # "normal"
"""

import re
from typing import Dict, List, Optional, Any


class InputAnalyzer:
    """
    入力解析システム
    
    ユーザーの入力テキストを解析し、
    インテントとエンティティを抽出する。
    """
    
    # インテントキーワードマッピング
    INTENT_KEYWORDS = {
        "create": ["作成", "作って", "作る", "生成", "書いて", "構築", "開発", "実装"],
        "analyze": ["分析", "解析", "調査", "調べて", "確認", "検証", "診断"],
        "execute": ["実行", "起動", "動かして", "走らせて", "テスト", "試して"],
        "search": ["検索", "探して", "見つけて", "調べて", "探索"],
        "modify": ["修正", "変更", "更新", "編集", "改善", "最適化"],
        "delete": ["削除", "消して", "除去", "クリア"],
        "help": ["ヘルプ", "助けて", "教えて", "説明", "どうすれば", "方法"],
        "explain": ["説明", "解説", "わかりやすく", "詳しく"],
    }
    
    # 技術スタックキーワード
    TECH_STACK_KEYWORDS = {
        "python": ["Python", "python", "パイソン"],
        "flask": ["Flask", "flask", "フラスク"],
        "django": ["Django", "django", "ジャンゴ"],
        "fastapi": ["FastAPI", "fastapi", "ファストAPI"],
        "react": ["React", "react", "リアクト"],
        "vue": ["Vue", "vue", "ビュー"],
        "javascript": ["JavaScript", "javascript", "JS", "js", "ジャバスクリプト"],
        "typescript": ["TypeScript", "typescript", "TS", "ts", "タイプスクリプト"],
        "sql": ["SQL", "sql", "エスキューエル"],
        "database": ["データベース", "DB", "db", "database"],
        "api": ["API", "api", "エーピーアイ"],
        "web": ["Web", "web", "ウェブ"],
        "machine_learning": ["機械学習", "ML", "ml", "マシンラーニング"],
        "ai": ["AI", "ai", "人工知能"],
    }
    
    # 成果物キーワード
    OUTPUT_KEYWORDS = {
        "application": ["アプリ", "アプリケーション", "ソフト", "システム"],
        "website": ["Webサイト", "ウェブサイト", "サイト", "ホームページ"],
        "api": ["API", "エンドポイント", "インターフェース"],
        "script": ["スクリプト", "プログラム", "コード"],
        "report": ["レポート", "報告書", "ドキュメント"],
        "dashboard": ["ダッシュボード", "管理画面", "可視化"],
        "model": ["モデル", "予測モデル", "学習モデル"],
    }
    
    def __init__(self, user_input: str):
        """
        InputAnalyzerの初期化
        
        Args:
            user_input: ユーザーの入力テキスト
        """
        self.user_input = user_input if user_input else ""
        self.intent = None
        self.entities = {}
        self.priority = "normal"
        self.complexity = "medium"
    
    def classify_intent(self) -> str:
        """
        インテント（意図）を分類
        
        Returns:
            インテント名（create, analyze, execute等）
        """
        if not self.user_input:
            return "unknown"
        
        # 各インテントのスコアを計算
        intent_scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in self.user_input)
            if score > 0:
                intent_scores[intent] = score
        
        # スコアが最も高いインテントを選択
        if intent_scores:
            self.intent = max(intent_scores, key=intent_scores.get)
        else:
            self.intent = "unknown"
        
        return self.intent
    
    def extract_entities(self) -> Dict[str, List[str]]:
        """
        エンティティ（キーワード）を抽出
        
        Returns:
            エンティティ辞書（カテゴリ: [値のリスト]）
        """
        entities = {
            "技術スタック": [],
            "成果物": [],
            "キーワード": []
        }
        
        # 技術スタック抽出
        for tech, keywords in self.TECH_STACK_KEYWORDS.items():
            if any(keyword in self.user_input for keyword in keywords):
                entities["技術スタック"].append(tech)
        
        # 成果物抽出
        for output, keywords in self.OUTPUT_KEYWORDS.items():
            if any(keyword in self.user_input for keyword in keywords):
                entities["成果物"].append(output)
        
        # 一般キーワード抽出（名詞的なもの）
        # 簡易的な実装（より高度な形態素解析は将来実装可能）
        words = re.findall(r'[ぁ-んァ-ヶー一-龥a-zA-Z]+', self.user_input)
        # 頻出する一般的な単語を除外
        stop_words = ["して", "ください", "お願い", "します", "ある", "する", "なる", "いる"]
        keywords = [word for word in words if len(word) >= 2 and word not in stop_words]
        entities["キーワード"] = keywords[:10]  # 最大10個
        
        self.entities = entities
        return entities
    
    def get_priority(self) -> str:
        """
        タスクの優先度を判定
        
        Returns:
            優先度（high, normal, low）
        """
        # 緊急キーワード
        urgent_keywords = ["緊急", "急いで", "今すぐ", "至急", "すぐに", "早く"]
        if any(keyword in self.user_input for keyword in urgent_keywords):
            self.priority = "high"
            return self.priority
        
        # 低優先度キーワード
        low_priority_keywords = ["後で", "時間があれば", "可能なら", "余裕があれば"]
        if any(keyword in self.user_input for keyword in low_priority_keywords):
            self.priority = "low"
            return self.priority
        
        self.priority = "normal"
        return self.priority
    
    def get_complexity(self) -> str:
        """
        タスクの複雑度を評価
        
        Returns:
            複雑度（simple, medium, complex）
        """
        # 技術スタック数でざっくり判定
        tech_count = len(self.entities.get("技術スタック", []))
        output_count = len(self.entities.get("成果物", []))
        
        # 複雑さを示すキーワード
        complex_keywords = ["統合", "連携", "複数", "高度", "複雑", "詳細", "最適化"]
        has_complex = any(keyword in self.user_input for keyword in complex_keywords)
        
        # 簡単さを示すキーワード
        simple_keywords = ["簡単", "シンプル", "基本", "単純", "最小限"]
        has_simple = any(keyword in self.user_input for keyword in simple_keywords)
        
        if has_simple or (tech_count == 0 and output_count <= 1):
            self.complexity = "simple"
        elif has_complex or tech_count >= 3 or output_count >= 3:
            self.complexity = "complex"
        else:
            self.complexity = "medium"
        
        return self.complexity
    
    def analyze(self) -> Dict[str, Any]:
        """
        入力テキストを完全解析
        
        Returns:
            解析結果（インテント、エンティティ、優先度、複雑度）
        """
        intent = self.classify_intent()
        entities = self.extract_entities()
        priority = self.get_priority()
        complexity = self.get_complexity()
        
        return {
            "user_input": self.user_input,
            "intent": intent,
            "entities": entities,
            "priority": priority,
            "complexity": complexity,
            "word_count": len(self.user_input)
        }
    
    def get_summary(self) -> str:
        """
        解析結果のサマリーを取得
        
        Returns:
            サマリー文字列
        """
        if not self.intent:
            self.analyze()
        
        summary_parts = [
            f"インテント: {self.intent}",
            f"優先度: {self.priority}",
            f"複雑度: {self.complexity}"
        ]
        
        if self.entities.get("技術スタック"):
            summary_parts.append(f"技術: {', '.join(self.entities['技術スタック'])}")
        
        if self.entities.get("成果物"):
            summary_parts.append(f"成果物: {', '.join(self.entities['成果物'])}")
        
        return " | ".join(summary_parts)


if __name__ == "__main__":
    # テストコード
    print("=" * 60)
    print("InputAnalyzer - Naviko入力解析システム")
    print("=" * 60)
    print()
    
    test_cases = [
        "Flaskを使ってWebアプリケーションを作成してください",
        "売上データを分析して可視化してください",
        "機械学習モデルを開発して予測を実行してください",
        "このエラーを修正してください",
        "Pythonの使い方を教えてください"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"【テストケース{i}】")
        print(f"入力: {test_input}")
        print()
        
        analyzer = InputAnalyzer(test_input)
        result = analyzer.analyze()
        
        print("解析結果:")
        print(f"  インテント: {result['intent']}")
        print(f"  優先度: {result['priority']}")
        print(f"  複雑度: {result['complexity']}")
        
        if result['entities']['技術スタック']:
            print(f"  技術スタック: {', '.join(result['entities']['技術スタック'])}")
        
        if result['entities']['成果物']:
            print(f"  成果物: {', '.join(result['entities']['成果物'])}")
        
        if result['entities']['キーワード']:
            print(f"  キーワード: {', '.join(result['entities']['キーワード'][:5])}")
        
        print()
        print(f"サマリー: {analyzer.get_summary()}")
        print("-" * 60)
        print()
    
    print("🎉 全てのテストケースが完了しました！")
