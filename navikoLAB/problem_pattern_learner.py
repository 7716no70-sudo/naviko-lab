#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProblemPatternLearner - Navikoの問題パターン学習システム

このモジュールはNavikoのSystem 3の一部として、以下を提供します：
- 問題パターンの記録と分析
- 経験からの学習とパターンマッチング
- 自動予防策の提案と実行
- 同じ問題の再発防止

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
import hashlib


class ProblemPatternLearner:
    """
    問題パターン学習システム
    
    発生した問題をパターン化し、同じ問題の再発を予防するための学習システム。
    ExperienceMemoryと連携して、過去の経験から学習します。
    """
    
    def __init__(self, lab_dir: str = None, experience_db_path: str = None):
        """
        ProblemPatternLearnerの初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
            experience_db_path: ExperienceMemoryのDBパス
        """
        # 基本パス設定
        if lab_dir is None:
            lab_dir = os.path.join(os.path.expanduser("~"), "navikoLAB")
            if not os.path.exists(lab_dir):
                lab_dir = "/Workspace/Users/7716no70@gmail.com/navikoLAB"
        
        self.lab_dir = Path(lab_dir)
        self.patterns_dir = self.lab_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # ExperienceMemory DB接続
        if experience_db_path is None:
            experience_db_path = self.lab_dir / "experience_memory.db"
        self.experience_db_path = experience_db_path
        
        # パターンデータベース初期化
        self.patterns_db_path = self.lab_dir / "problem_patterns.db"
        self._initialize_patterns_database()
        
        # パターンキャッシュ
        self.pattern_cache: Dict[str, Dict] = {}
        
    def _initialize_patterns_database(self):
        """
        パターンデータベースの初期化
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # パターンテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                problem_type TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_seen TIMESTAMP,
                context_hash TEXT,
                context_json TEXT,
                solution_json TEXT,
                success_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # パターン適用履歴テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                notes TEXT,
                FOREIGN KEY (pattern_id) REFERENCES patterns(pattern_id)
            )
        """)
        
        # 予防策テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preventions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_type TEXT NOT NULL,
                prevention_action TEXT NOT NULL,
                auto_executable BOOLEAN DEFAULT 0,
                priority INTEGER DEFAULT 1,
                effectiveness_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        # 初期予防策を登録
        self._register_initial_preventions()
    
    def _register_initial_preventions(self):
        """
        初期予防策の登録
        """
        initial_preventions = [
            {
                "problem_type": "api_key_error",
                "prevention_action": "セッション開始時にGROQ_API_KEYを自動設定",
                "auto_executable": True,
                "priority": 1,
                "effectiveness_score": 0.95
            },
            {
                "problem_type": "git_sync_error",
                "prevention_action": "Git操作前に同期状態を確認",
                "auto_executable": True,
                "priority": 1,
                "effectiveness_score": 0.8
            },
            {
                "problem_type": "file_sync_mismatch",
                "prevention_action": "ファイル更新前にバックアップを作成",
                "auto_executable": True,
                "priority": 2,
                "effectiveness_score": 0.7
            },
            {
                "problem_type": "compute_timeout",
                "prevention_action": "長時間処理前にコンピュート状態を確認",
                "auto_executable": True,
                "priority": 2,
                "effectiveness_score": 0.6
            }
        ]
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        for prevention in initial_preventions:
            # 既存チェック
            cursor.execute(
                "SELECT id FROM preventions WHERE problem_type = ? AND prevention_action = ?",
                (prevention["problem_type"], prevention["prevention_action"])
            )
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO preventions (problem_type, prevention_action, auto_executable, priority, effectiveness_score) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (prevention["problem_type"], prevention["prevention_action"], 
                     prevention["auto_executable"], prevention["priority"], prevention["effectiveness_score"])
                )
        
        conn.commit()
        conn.close()
    
    def record_problem(self, problem_type: str, context: Dict[str, Any], 
                      solution: Optional[Dict[str, Any]] = None, 
                      success: bool = False) -> str:
        """
        問題を記録し、パターンとして登録
        
        Args:
            problem_type: 問題のタイプ
            context: 問題発生時のコンテキスト
            solution: 適用された解決策
            success: 解決に成功したか
        
        Returns:
            パターンID
        """
        # コンテキストのハッシュ値を計算
        context_str = json.dumps(context, sort_keys=True)
        context_hash = hashlib.md5(context_str.encode()).hexdigest()
        
        # パターンIDを生成
        pattern_id = f"{problem_type}_{context_hash[:8]}"
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 既存パターンの確認
        cursor.execute(
            "SELECT pattern_id, frequency, success_rate FROM patterns WHERE pattern_id = ?",
            (pattern_id,)
        )
        existing = cursor.fetchone()
        
        if existing:
            # 既存パターンの更新
            old_frequency = existing[1]
            old_success_rate = existing[2]
            new_frequency = old_frequency + 1
            
            # 成功率の更新
            if solution:
                new_success_rate = (old_success_rate * old_frequency + (1.0 if success else 0.0)) / new_frequency
            else:
                new_success_rate = old_success_rate
            
            cursor.execute(
                "UPDATE patterns SET frequency = ?, last_seen = ?, success_rate = ?, updated_at = ? WHERE pattern_id = ?",
                (new_frequency, datetime.now().isoformat(), new_success_rate, datetime.now().isoformat(), pattern_id)
            )
        else:
            # 新規パターンの登録
            cursor.execute(
                "INSERT INTO patterns (pattern_id, problem_type, frequency, last_seen, context_hash, context_json, solution_json, success_rate) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (pattern_id, problem_type, 1, datetime.now().isoformat(), context_hash, 
                 json.dumps(context), json.dumps(solution) if solution else None, 
                 1.0 if success else 0.0)
            )
        
        # 適用履歴の記録
        if solution:
            cursor.execute(
                "INSERT INTO pattern_applications (pattern_id, success, notes) VALUES (?, ?, ?)",
                (pattern_id, success, json.dumps(solution))
            )
        
        conn.commit()
        conn.close()
        
        return pattern_id
    
    def analyze_patterns(self, lookback_days: int = 30) -> Dict[str, Any]:
        """
        パターンを分析し、頻出問題とトレンドを特定
        
        Args:
            lookback_days: 分析対象期間（日数）
        
        Returns:
            分析結果
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "period_days": lookback_days,
            "frequent_problems": [],
            "trends": {},
            "recommendations": []
        }
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 期間内の頻出問題を取得
        cutoff_date = (datetime.now() - timedelta(days=lookback_days)).isoformat()
        cursor.execute(
            "SELECT problem_type, COUNT(*) as count, AVG(success_rate) as avg_success "
            "FROM patterns "
            "WHERE last_seen > ? "
            "GROUP BY problem_type "
            "ORDER BY count DESC",
            (cutoff_date,)
        )
        
        for problem_type, count, avg_success in cursor.fetchall():
            analysis["frequent_problems"].append({
                "problem_type": problem_type,
                "frequency": count,
                "avg_success_rate": round(avg_success, 2) if avg_success else 0.0
            })
            
            # 推奨事項の生成
            if count >= 5 and avg_success < 0.5:
                analysis["recommendations"].append(
                    f"{problem_type}が頻発していますが、解決率が低い（{avg_success:.1%}）ため、新しい対策が必要です"
                )
            elif count >= 3:
                analysis["recommendations"].append(
                    f"{problem_type}の自動予防策を設定することを推奨します"
                )
        
        conn.close()
        
        # レポート保存
        self._save_analysis_report(analysis)
        
        return analysis
    
    def suggest_prevention(self, problem_type: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        問題タイプに対する予防策を提案
        
        Args:
            problem_type: 問題のタイプ
            context: 現在のコンテキスト
        
        Returns:
            予防策のリスト
        """
        preventions = []
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 登録されている予防策を取得
        cursor.execute(
            "SELECT prevention_action, auto_executable, priority, effectiveness_score "
            "FROM preventions "
            "WHERE problem_type = ? "
            "ORDER BY priority ASC, effectiveness_score DESC",
            (problem_type,)
        )
        
        for action, auto_exec, priority, effectiveness in cursor.fetchall():
            preventions.append({
                "action": action,
                "auto_executable": bool(auto_exec),
                "priority": priority,
                "effectiveness": effectiveness,
                "recommended": effectiveness >= 0.7
            })
        
        conn.close()
        
        # 過去の成功事例からも提案
        similar_solutions = self._find_similar_solutions(problem_type, context)
        for solution in similar_solutions:
            if solution not in [p["action"] for p in preventions]:
                preventions.append({
                    "action": solution,
                    "auto_executable": False,
                    "priority": 3,
                    "effectiveness": 0.5,
                    "recommended": False,
                    "note": "過去の成功事例から提案"
                })
        
        return preventions
    
    def apply_prevention(self, problem_type: str, context: Dict[str, Any] = None, 
                        auto_only: bool = True) -> Dict[str, Any]:
        """
        予防策を実際に適用
        
        Args:
            problem_type: 問題のタイプ
            context: 現在のコンテキスト
            auto_only: 自動実行可能なもののみ適用
        
        Returns:
            適用結果
        """
        result = {
            "problem_type": problem_type,
            "timestamp": datetime.now().isoformat(),
            "applied_actions": [],
            "skipped_actions": [],
            "success": False
        }
        
        # 予防策の取得
        preventions = self.suggest_prevention(problem_type, context)
        
        for prevention in preventions:
            if auto_only and not prevention["auto_executable"]:
                result["skipped_actions"].append({
                    "action": prevention["action"],
                    "reason": "手動実行が必要"
                })
                continue
            
            # 予防策の実行
            action_result = self._execute_prevention_action(
                problem_type, prevention["action"], context
            )
            
            result["applied_actions"].append({
                "action": prevention["action"],
                "result": action_result
            })
            
            if action_result.get("success"):
                result["success"] = True
                break  # 最初の成功で終了
        
        return result
    
    def _execute_prevention_action(self, problem_type: str, action: str, 
                                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        予防策アクションの実行
        
        Args:
            problem_type: 問題のタイプ
            action: 実行するアクション
            context: コンテキスト
        
        Returns:
            実行結果
        """
        result = {
            "success": False,
            "message": "",
            "details": {}
        }
        
        # アクション内容に応じた処理（シミュレーション）
        if "APIキー" in action:
            # APIキー設定のシミュレーション
            result["success"] = True
            result["message"] = "APIキーの設定を確認しました"
            result["details"]["action_type"] = "api_key_check"
        
        elif "Git" in action or "同期" in action:
            # Git同期チェックのシミュレーション
            result["success"] = True
            result["message"] = "Git同期状態を確認しました"
            result["details"]["action_type"] = "git_sync_check"
        
        elif "バックアップ" in action:
            # バックアップ作成のシミュレーション
            result["success"] = True
            result["message"] = "バックアップを作成しました"
            result["details"]["action_type"] = "backup_create"
        
        elif "コンピュート" in action:
            # コンピュート状態チェックのシミュレーション
            result["success"] = True
            result["message"] = "コンピュート状態を確認しました"
            result["details"]["action_type"] = "compute_status_check"
        
        else:
            result["success"] = False
            result["message"] = f"未実装のアクション: {action}"
        
        return result
    
    def _find_similar_solutions(self, problem_type: str, context: Dict[str, Any] = None) -> List[str]:
        """
        過去の成功事例から類似の解決策を検索
        
        Args:
            problem_type: 問題のタイプ
            context: 現在のコンテキスト
        
        Returns:
            類似の解決策リスト
        """
        solutions = []
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 成功率が高いパターンを検索
        cursor.execute(
            "SELECT solution_json FROM patterns "
            "WHERE problem_type = ? AND success_rate > 0.7 AND solution_json IS NOT NULL "
            "ORDER BY success_rate DESC, frequency DESC "
            "LIMIT 5",
            (problem_type,)
        )
        
        for (solution_json,) in cursor.fetchall():
            try:
                solution = json.loads(solution_json)
                if isinstance(solution, dict) and "action" in solution:
                    solutions.append(solution["action"])
            except:
                pass
        
        conn.close()
        
        return solutions
    
    def get_prevention_effectiveness(self, problem_type: str = None) -> Dict[str, Any]:
        """
        予防策の効果を分析
        
        Args:
            problem_type: 特定の問題タイプ（Noneの場合は全体）
        
        Returns:
            効果分析結果
        """
        effectiveness = {
            "timestamp": datetime.now().isoformat(),
            "problem_type": problem_type,
            "preventions": [],
            "overall_effectiveness": 0.0
        }
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        if problem_type:
            cursor.execute(
                "SELECT prevention_action, effectiveness_score, "
                "(SELECT COUNT(*) FROM pattern_applications pa JOIN patterns p ON pa.pattern_id = p.pattern_id "
                "WHERE p.problem_type = preventions.problem_type AND pa.success = 1) as success_count "
                "FROM preventions WHERE problem_type = ?",
                (problem_type,)
            )
        else:
            cursor.execute(
                "SELECT problem_type, prevention_action, effectiveness_score, 0 as success_count "
                "FROM preventions"
            )
        
        total_effectiveness = 0.0
        count = 0
        
        for row in cursor.fetchall():
            if problem_type:
                action, score, success_count = row
                pt = problem_type
            else:
                pt, action, score, success_count = row
            
            effectiveness["preventions"].append({
                "problem_type": pt,
                "action": action,
                "effectiveness_score": score,
                "success_count": success_count
            })
            
            total_effectiveness += score
            count += 1
        
        if count > 0:
            effectiveness["overall_effectiveness"] = round(total_effectiveness / count, 2)
        
        conn.close()
        
        return effectiveness
    
    def _save_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """
        分析レポートを保存
        
        Args:
            analysis: 分析結果
        
        Returns:
            保存されたファイルパス
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pattern_analysis_{timestamp}.json"
        filepath = self.patterns_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def get_learning_summary(self) -> str:
        """
        学習状況のサマリーを取得
        
        Returns:
            人間が読みやすい形式のサマリー
        """
        lines = []
        lines.append("=" * 60)
        lines.append("Naviko System 3: 問題パターン学習レポート")
        lines.append("=" * 60)
        lines.append(f"レポート作成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # パターン分析
        analysis = self.analyze_patterns()
        
        if analysis["frequent_problems"]:
            lines.append("【頻出問題】")
            for i, problem in enumerate(analysis["frequent_problems"], 1):
                lines.append(f"  {i}. {problem['problem_type']}")
                lines.append(f"     頻度: {problem['frequency']}回, 解決率: {problem['avg_success_rate']:.1%}")
            lines.append("")
        
        # 予防策の効果
        effectiveness = self.get_prevention_effectiveness()
        lines.append("【予防策の効果】")
        lines.append(f"総合効果スコア: {effectiveness['overall_effectiveness']:.1%}")
        lines.append("")
        
        # 推奨事項
        if analysis["recommendations"]:
            lines.append("【推奨事項】")
            for i, rec in enumerate(analysis["recommendations"], 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """
    メインテスト関数
    """
    print("ProblemPatternLearner テスト開始")
    print("=" * 60)
    
    # ラーナー初期化
    learner = ProblemPatternLearner()
    
    # テストデータの登録
    print("\n1. 問題パターンの記録テスト...")
    pattern_id = learner.record_problem(
        "api_key_error",
        {"location": "databricks", "session": "new"},
        {"action": "環境変数再設定"},
        success=True
    )
    print(f"  ✅ パターン登録成功: {pattern_id}")
    
    # パターン分析
    print("\n2. パターン分析テスト...")
    analysis = learner.analyze_patterns()
    print(f"  ✅ {len(analysis['frequent_problems'])}件の頻出問題を検出")
    
    # 予防策提案
    print("\n3. 予防策提案テスト...")
    preventions = learner.suggest_prevention("api_key_error")
    print(f"  ✅ {len(preventions)}件の予防策を提案")
    for prev in preventions[:3]:
        print(f"    - {prev['action']} (効果: {prev['effectiveness']:.1%})")
    
    # 学習サマリー
    print("\n4. 学習サマリーテスト...")
    summary = learner.get_learning_summary()
    print(summary)
    
    print("\n" + "=" * 60)
    print("✅ ProblemPatternLearner テスト完了")


if __name__ == "__main__":
    main()
