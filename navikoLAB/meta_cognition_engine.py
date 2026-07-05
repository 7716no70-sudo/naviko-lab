#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MetaCognitionEngine - Navikoのメタ認知システム

このモジュールはNavikoの「System 3」として機能し、以下を提供します：
- 自己診断：現在のシステム状態を分析
- 問題予測：過去のパターンから将来の問題を予測
- 戦略選択：最適な対処戦略を選択
- 自己改善：経験から学習し、思考プロセスを最適化

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib


class MetaCognitionEngine:
    """
    メタ認知エンジン - Navikoの自己認識・自己改善システム
    
    System 3の中核として、以下の機能を提供：
    - システム状態の自己診断
    - 問題パターンの予測
    - 最適な対処戦略の選択
    - 自己改善サイクルの管理
    """
    
    def __init__(self, lab_dir: str = None, experience_db_path: str = None):
        """
        MetaCognitionEngineの初期化
        
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
        self.reports_dir = self.lab_dir / "reports" / "meta_cognition"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # ExperienceMemory DB接続
        if experience_db_path is None:
            experience_db_path = self.lab_dir / "experience_memory.db"
        self.experience_db_path = experience_db_path
        
        # 対処戦略データベース
        self.strategy_database = self._initialize_strategy_database()
        
        # 診断履歴
        self.diagnosis_history: List[Dict] = []
        
    def _initialize_strategy_database(self) -> Dict[str, Dict[str, Any]]:
        """
        対処戦略データベースの初期化
        
        Returns:
            問題タイプごとの対処戦略辞書
        """
        return {
            "api_key_error": {
                "name": "APIキーエラー",
                "severity": "high",
                "auto_recoverable": True,
                "strategies": [
                    {
                        "name": "環境変数チェック",
                        "action": "check_env_vars",
                        "priority": 1,
                        "description": "GROQ_API_KEYの設定状態を確認"
                    },
                    {
                        "name": "自動再設定",
                        "action": "auto_reset_api_key",
                        "priority": 2,
                        "description": "カスタム指示からAPIキーを再設定"
                    },
                    {
                        "name": "手動確認要求",
                        "action": "request_manual_check",
                        "priority": 3,
                        "description": "ユーザーに手動確認を依頼"
                    }
                ]
            },
            "git_sync_error": {
                "name": "Git同期エラー",
                "severity": "medium",
                "auto_recoverable": True,
                "strategies": [
                    {
                        "name": "同期状態診断",
                        "action": "diagnose_git_state",
                        "priority": 1,
                        "description": "Workspace/GitHub/ローカルの同期状態を確認"
                    },
                    {
                        "name": "自動プル",
                        "action": "auto_git_pull",
                        "priority": 2,
                        "description": "最新の変更をプル"
                    },
                    {
                        "name": "リポジトリ再クローン",
                        "action": "reclone_repository",
                        "priority": 3,
                        "description": "リポジトリを削除して再クローン"
                    }
                ]
            },
            "file_sync_mismatch": {
                "name": "ファイル同期ズレ",
                "severity": "medium",
                "auto_recoverable": False,
                "strategies": [
                    {
                        "name": "差分分析",
                        "action": "analyze_file_diff",
                        "priority": 1,
                        "description": "ファイルサイズ・ハッシュ値を比較"
                    },
                    {
                        "name": "手動確認要求",
                        "action": "request_manual_sync",
                        "priority": 2,
                        "description": "ユーザーに同期方法を確認"
                    }
                ]
            },
            "module_missing": {
                "name": "モジュール欠損",
                "severity": "high",
                "auto_recoverable": False,
                "strategies": [
                    {
                        "name": "依存関係チェック",
                        "action": "check_dependencies",
                        "priority": 1,
                        "description": "必要なモジュールの存在を確認"
                    },
                    {
                        "name": "再インストール提案",
                        "action": "suggest_reinstall",
                        "priority": 2,
                        "description": "モジュールの再インストールを提案"
                    }
                ]
            },
            "compute_timeout": {
                "name": "コンピュートタイムアウト",
                "severity": "low",
                "auto_recoverable": True,
                "strategies": [
                    {
                        "name": "待機",
                        "action": "wait_for_compute",
                        "priority": 1,
                        "description": "コンピュート起動を待機"
                    },
                    {
                        "name": "再試行",
                        "action": "retry_execution",
                        "priority": 2,
                        "description": "処理を再試行"
                    }
                ]
            }
        }
    
    def diagnose_system_state(self) -> Dict[str, Any]:
        """
        現在のシステム状態を総合的に診断
        
        Returns:
            診断結果の辞書
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "components": {},
            "risks": [],
            "recommendations": []
        }
        
        # 1. 環境変数診断
        env_status = self._diagnose_environment_variables()
        diagnosis["components"]["environment"] = env_status
        
        # 2. ファイルシステム診断
        fs_status = self._diagnose_file_system()
        diagnosis["components"]["file_system"] = fs_status
        
        # 3. モジュール健全性診断
        module_status = self._diagnose_modules()
        diagnosis["components"]["modules"] = module_status
        
        # 4. ExperienceMemory診断
        memory_status = self._diagnose_experience_memory()
        diagnosis["components"]["experience_memory"] = memory_status
        
        # 5. リスク評価
        risks = self._evaluate_risks(diagnosis["components"])
        diagnosis["risks"] = risks
        
        # 6. 推奨事項生成
        recommendations = self._generate_recommendations(diagnosis["components"], risks)
        diagnosis["recommendations"] = recommendations
        
        # 7. 総合健全性判定
        overall_health = self._calculate_overall_health(diagnosis["components"], risks)
        diagnosis["overall_health"] = overall_health
        
        # 診断履歴に追加
        self.diagnosis_history.append(diagnosis)
        
        # レポート保存
        self._save_diagnosis_report(diagnosis)
        
        return diagnosis
    
    def _diagnose_environment_variables(self) -> Dict[str, Any]:
        """
        環境変数の診断
        
        Returns:
            環境変数の状態
        """
        status = {
            "status": "healthy",
            "api_keys": {},
            "issues": []
        }
        
        # 重要なAPIキーのチェック
        important_keys = ["GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
        
        for key in important_keys:
            value = os.environ.get(key)
            if value:
                status["api_keys"][key] = {
                    "set": True,
                    "length": len(value)
                }
            else:
                status["api_keys"][key] = {
                    "set": False,
                    "length": 0
                }
                if key == "GROQ_API_KEY":
                    status["issues"].append(f"{key}が未設定（401エラーのリスク）")
                    status["status"] = "warning"
        
        return status
    
    def _diagnose_file_system(self) -> Dict[str, Any]:
        """
        ファイルシステムの診断
        
        Returns:
            ファイルシステムの状態
        """
        status = {
            "status": "healthy",
            "files": {},
            "issues": []
        }
        
        # 重要ファイルの存在確認
        important_files = [
            "naviko.py",
            "navikoLAB/llm_connector.py",
            "navikoLAB/deep_search_engine.py",
            "navikoLAB/experience_memory.py",
            "navikoLAB/error_diagnostic_engine.py",
            "navikoLAB/process_recorder.py"
        ]
        
        workspace_base = Path("/Workspace/Users/7716no70@gmail.com")
        
        for file_path in important_files:
            full_path = workspace_base / file_path
            if full_path.exists():
                file_stat = full_path.stat()
                status["files"][file_path] = {
                    "exists": True,
                    "size": file_stat.st_size,
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                }
            else:
                status["files"][file_path] = {
                    "exists": False
                }
                status["issues"].append(f"{file_path}が見つかりません")
                status["status"] = "warning"
        
        return status
    
    def _diagnose_modules(self) -> Dict[str, Any]:
        """
        LABモジュールの健全性診断
        
        Returns:
            モジュールの状態
        """
        status = {
            "status": "healthy",
            "modules": {},
            "issues": []
        }
        
        # LABディレクトリのPythonファイルをチェック
        if self.lab_dir.exists():
            py_files = list(self.lab_dir.glob("*.py"))
            status["modules"]["count"] = len(py_files)
            status["modules"]["files"] = [f.name for f in py_files]
        else:
            status["issues"].append(f"LABディレクトリが見つかりません: {self.lab_dir}")
            status["status"] = "error"
        
        return status
    
    def _diagnose_experience_memory(self) -> Dict[str, Any]:
        """
        ExperienceMemoryの診断
        
        Returns:
            ExperienceMemoryの状態
        """
        status = {
            "status": "healthy",
            "database": {},
            "issues": []
        }
        
        # DBファイルの存在確認
        if Path(self.experience_db_path).exists():
            status["database"]["exists"] = True
            
            # DB接続テスト
            try:
                conn = sqlite3.connect(self.experience_db_path)
                cursor = conn.cursor()
                
                # テーブル存在確認
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = [row[0] for row in cursor.fetchall()]
                status["database"]["tables"] = tables
                
                # 経験レコード数
                if "experiences" in tables:
                    cursor.execute("SELECT COUNT(*) FROM experiences")
                    count = cursor.fetchone()[0]
                    status["database"]["experience_count"] = count
                
                conn.close()
            except Exception as e:
                status["issues"].append(f"DB接続エラー: {str(e)}")
                status["status"] = "warning"
        else:
            status["database"]["exists"] = False
            status["issues"].append("ExperienceMemory DBが見つかりません")
            status["status"] = "warning"
        
        return status
    
    def _evaluate_risks(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        システム状態からリスクを評価
        
        Args:
            components: 各コンポーネントの診断結果
        
        Returns:
            リスクのリスト
        """
        risks = []
        
        # 環境変数リスク
        env_status = components.get("environment", {})
        if env_status.get("status") == "warning":
            for issue in env_status.get("issues", []):
                risks.append({
                    "type": "api_key_error",
                    "severity": "high",
                    "description": issue,
                    "predicted_impact": "401エラーの頻発"
                })
        
        # ファイルシステムリスク
        fs_status = components.get("file_system", {})
        if fs_status.get("issues"):
            for issue in fs_status.get("issues", []):
                risks.append({
                    "type": "module_missing",
                    "severity": "high",
                    "description": issue,
                    "predicted_impact": "機能の一部が動作不能"
                })
        
        # ExperienceMemoryリスク
        memory_status = components.get("experience_memory", {})
        if memory_status.get("status") == "warning":
            risks.append({
                "type": "experience_memory_unavailable",
                "severity": "medium",
                "description": "ExperienceMemoryが利用不可",
                "predicted_impact": "学習機能の低下"
            })
        
        return risks
    
    def _generate_recommendations(self, components: Dict[str, Any], risks: List[Dict[str, Any]]) -> List[str]:
        """
        推奨事項の生成
        
        Args:
            components: 各コンポーネントの診断結果
            risks: 検出されたリスク
        
        Returns:
            推奨事項のリスト
        """
        recommendations = []
        
        # リスクベースの推奨
        for risk in risks:
            risk_type = risk["type"]
            if risk_type in self.strategy_database:
                strategy = self.strategy_database[risk_type]
                if strategy["auto_recoverable"]:
                    recommendations.append(
                        f"[自動対処可能] {strategy['name']}: "
                        f"{strategy['strategies'][0]['description']}"
                    )
                else:
                    recommendations.append(
                        f"[手動確認必要] {strategy['name']}: "
                        f"{strategy['strategies'][0]['description']}"
                    )
        
        # 一般的な推奨
        if not risks:
            recommendations.append("✅ システムは正常に動作しています")
        
        return recommendations
    
    def _calculate_overall_health(self, components: Dict[str, Any], risks: List[Dict[str, Any]]) -> str:
        """
        総合健全性スコアの計算
        
        Args:
            components: 各コンポーネントの診断結果
            risks: 検出されたリスク
        
        Returns:
            健全性レベル（healthy/warning/error）
        """
        # 重大なリスクがあるか
        high_severity_risks = [r for r in risks if r.get("severity") == "high"]
        if high_severity_risks:
            return "error"
        
        # 警告レベルのリスクがあるか
        if risks:
            return "warning"
        
        # 全コンポーネントが健全か
        for component in components.values():
            if component.get("status") in ["warning", "error"]:
                return "warning"
        
        return "healthy"
    
    def predict_problems(self, current_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        過去のパターンから将来の問題を予測
        
        Args:
            current_context: 現在の作業コンテキスト
        
        Returns:
            予測される問題のリスト
        """
        predictions = []
        
        # ExperienceMemoryから過去の問題パターンを取得
        try:
            conn = sqlite3.connect(self.experience_db_path)
            cursor = conn.cursor()
            
            # 過去30日間のエラー履歴を取得
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            cursor.execute(
                "SELECT error_type, context, COUNT(*) as frequency "
                "FROM experiences "
                "WHERE timestamp > ? AND error_type IS NOT NULL "
                "GROUP BY error_type "
                "ORDER BY frequency DESC",
                (thirty_days_ago,)
            )
            
            error_patterns = cursor.fetchall()
            
            for error_type, context, frequency in error_patterns:
                # 頻度が高い問題を予測
                if frequency >= 3:
                    predictions.append({
                        "problem_type": error_type,
                        "likelihood": "high" if frequency >= 5 else "medium",
                        "frequency": frequency,
                        "context": context,
                        "recommended_action": self._get_recommended_action(error_type)
                    })
            
            conn.close()
        except Exception as e:
            print(f"問題予測エラー: {e}")
        
        return predictions
    
    def select_strategy(self, problem_type: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        問題タイプに対する最適な対処戦略を選択
        
        Args:
            problem_type: 問題のタイプ
            context: 追加のコンテキスト情報
        
        Returns:
            選択された戦略、またはNone
        """
        if problem_type not in self.strategy_database:
            return None
        
        strategy_info = self.strategy_database[problem_type]
        
        # 最優先の戦略を選択（priority=1）
        selected_strategy = None
        for strategy in strategy_info["strategies"]:
            if strategy["priority"] == 1:
                selected_strategy = strategy
                break
        
        if selected_strategy:
            return {
                "problem_type": problem_type,
                "problem_name": strategy_info["name"],
                "severity": strategy_info["severity"],
                "auto_recoverable": strategy_info["auto_recoverable"],
                "strategy": selected_strategy,
                "alternative_strategies": [
                    s for s in strategy_info["strategies"] if s["priority"] > 1
                ]
            }
        
        return None
    
    def _get_recommended_action(self, error_type: str) -> str:
        """
        エラータイプに対する推奨アクションを取得
        
        Args:
            error_type: エラーのタイプ
        
        Returns:
            推奨アクション
        """
        if error_type in self.strategy_database:
            strategy = self.strategy_database[error_type]
            return strategy["strategies"][0]["description"]
        return "対処方法を確認してください"
    
    def self_evaluate(self) -> Dict[str, Any]:
        """
        自己評価：これまでの診断履歴から自身のパフォーマンスを評価
        
        Returns:
            自己評価結果
        """
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "diagnosis_count": len(self.diagnosis_history),
            "performance_metrics": {},
            "improvement_areas": []
        }
        
        if not self.diagnosis_history:
            evaluation["performance_metrics"]["status"] = "初回診断前"
            return evaluation
        
        # 健全性の推移を分析
        health_trend = [d["overall_health"] for d in self.diagnosis_history]
        evaluation["performance_metrics"]["health_trend"] = health_trend
        
        # 最新の状態
        latest_diagnosis = self.diagnosis_history[-1]
        evaluation["performance_metrics"]["current_health"] = latest_diagnosis["overall_health"]
        evaluation["performance_metrics"]["current_risks"] = len(latest_diagnosis["risks"])
        
        # 改善領域の特定
        if latest_diagnosis["overall_health"] != "healthy":
            for risk in latest_diagnosis["risks"]:
                evaluation["improvement_areas"].append(risk["description"])
        
        return evaluation
    
    def _save_diagnosis_report(self, diagnosis: Dict[str, Any]) -> str:
        """
        診断レポートを保存
        
        Args:
            diagnosis: 診断結果
        
        Returns:
            保存されたファイルパス
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"diagnosis_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(diagnosis, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def get_system_status_summary(self) -> str:
        """
        システム状態の簡易サマリーを取得
        
        Returns:
            人間が読みやすい形式のサマリー
        """
        diagnosis = self.diagnose_system_state()
        
        lines = []
        lines.append("=" * 60)
        lines.append("Naviko System 3: メタ認知診断レポート")
        lines.append("=" * 60)
        lines.append(f"診断時刻: {diagnosis['timestamp']}")
        lines.append(f"総合健全性: {diagnosis['overall_health'].upper()}")
        lines.append("")
        
        # リスク表示
        if diagnosis["risks"]:
            lines.append("【検出されたリスク】")
            for i, risk in enumerate(diagnosis["risks"], 1):
                lines.append(f"  {i}. [{risk['severity'].upper()}] {risk['description']}")
                lines.append(f"     影響: {risk['predicted_impact']}")
            lines.append("")
        
        # 推奨事項表示
        if diagnosis["recommendations"]:
            lines.append("【推奨事項】")
            for i, rec in enumerate(diagnosis["recommendations"], 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """
    メインテスト関数
    """
    print("MetaCognitionEngine テスト開始")
    print("=" * 60)
    
    # エンジン初期化
    engine = MetaCognitionEngine()
    
    # システム診断実行
    print("\n1. システム診断実行中...")
    summary = engine.get_system_status_summary()
    print(summary)
    
    # 問題予測
    print("\n2. 問題予測実行中...")
    predictions = engine.predict_problems()
    if predictions:
        print("予測される問題:")
        for pred in predictions:
            print(f"  - {pred['problem_type']} (頻度: {pred['frequency']}, 可能性: {pred['likelihood']})")
    else:
        print("  予測される問題はありません")
    
    # 自己評価
    print("\n3. 自己評価実行中...")
    evaluation = engine.self_evaluate()
    print(f"診断回数: {evaluation['diagnosis_count']}")
    print(f"現在の健全性: {evaluation['performance_metrics'].get('current_health', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("✅ MetaCognitionEngine テスト完了")


if __name__ == "__main__":
    main()
