"""
ImprovementManager - コード改善管理モジュール（LLM統合版）

LLMConnector を使用してコード評価・改善提案を生成する。
LLM が利用できない場合は、テンプレートベースにフォールバック。

完成: 2026-07-01
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    from .llm_connector import LLMConnector
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


class ImprovementManager:
    """
    コード改善管理
    
    機能:
    - LLMベースのコード評価
    - 改善提案の生成
    - 品質スコアリング
    - 改善要求の管理
    """
    
    def __init__(self, lab_dir: Path):
        """
        初期化
        
        Args:
            lab_dir: LABディレクトリのパス
        """
        self.lab_dir = Path(lab_dir)
        self.improvement_dir = self.lab_dir / "improvements"
        self.improvement_history_dir = self.lab_dir / "improvement_history"
        self.improvement_results_dir = self.lab_dir / "improvement_results"
        
        # ディレクトリ作成
        self.improvement_dir.mkdir(parents=True, exist_ok=True)
        self.improvement_history_dir.mkdir(parents=True, exist_ok=True)
        self.improvement_results_dir.mkdir(parents=True, exist_ok=True)
        
        # LLMConnector の初期化
        self.llm_connector = None
        if LLM_AVAILABLE:
            try:
                self.llm_connector = LLMConnector(
                    lab_dir=self.lab_dir,
                    model="llama-3.1-8b-instant"
                )
            except Exception as e:
                print(f"LLMConnector initialization failed: {e}")
        
        # 統計情報
        self.stats = {
            "total_evaluations": 0,
            "llm_evaluations": 0,
            "template_evaluations": 0,
            "improvements_generated": 0
        }
    
    def is_llm_available(self) -> bool:
        """LLMが利用可能かチェック"""
        return (
            self.llm_connector is not None 
            and self.llm_connector.is_available()
        )
    
    def evaluate_code(
        self,
        code: str,
        purpose: str = "Application development",
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        コードを評価
        
        Args:
            code: 評価対象のコード
            purpose: コードの目的
            use_llm: LLMを使用するか
        
        Returns:
            dict: 評価結果
        """
        self.stats["total_evaluations"] += 1
        
        if use_llm and self.is_llm_available():
            return self._evaluate_with_llm(code, purpose)
        else:
            return self._evaluate_with_template(code, purpose)
    
    def _evaluate_with_llm(self, code: str, purpose: str) -> Dict[str, Any]:
        """LLMを使用してコード評価"""
        self.stats["llm_evaluations"] += 1
        
        try:
            evaluation = self.llm_connector.evaluate_code(
                code=code,
                purpose=purpose,
                criteria=[
                    "Code correctness",
                    "Performance",
                    "Best practices",
                    "Error handling",
                    "Documentation"
                ]
            )
            
            evaluation["mode"] = "llm"
            return evaluation
            
        except Exception as e:
            print(f"LLM evaluation failed: {e}")
            return self._evaluate_with_template(code, purpose)
    
    def _evaluate_with_template(self, code: str, purpose: str) -> Dict[str, Any]:
        """テンプレートベースのコード評価"""
        self.stats["template_evaluations"] += 1
        
        # 基本的なチェック
        has_imports = "import" in code
        has_functions = "def " in code
        has_classes = "class " in code
        has_comments = "#" in code or '"""' in code
        has_error_handling = "try:" in code or "except:" in code
        
        score = 50  # ベーススコア
        
        if has_imports:
            score += 5
        if has_functions or has_classes:
            score += 15
        if has_comments:
            score += 10
        if has_error_handling:
            score += 10
        
        # コードの長さで追加評価
        lines = code.strip().split("\n")
        if len(lines) > 10:
            score += 5
        if len(lines) > 50:
            score += 5
        
        score = min(score, 100)
        
        strengths = []
        weaknesses = []
        suggestions = []
        
        if has_functions or has_classes:
            strengths.append("Structured code with functions/classes")
        else:
            weaknesses.append("No functions or classes defined")
            suggestions.append("Consider organizing code into functions")
        
        if has_comments:
            strengths.append("Includes documentation")
        else:
            weaknesses.append("Lacks documentation")
            suggestions.append("Add comments and docstrings")
        
        if has_error_handling:
            strengths.append("Has error handling")
        else:
            weaknesses.append("No error handling")
            suggestions.append("Add try-except blocks for robustness")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "mode": "template"
        }
    
    def generate_improvement_suggestion(
        self,
        code: str,
        evaluation: Dict[str, Any],
        purpose: str = "",
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        改善提案を生成
        
        Args:
            code: 対象コード
            evaluation: 評価結果
            purpose: 目的
            use_llm: LLMを使用するか
        
        Returns:
            dict: 改善提案
        """
        self.stats["improvements_generated"] += 1
        
        if use_llm and self.is_llm_available():
            return self._generate_improvement_with_llm(code, evaluation, purpose)
        else:
            return self._generate_improvement_with_template(code, evaluation)
    
    def _generate_improvement_with_llm(
        self,
        code: str,
        evaluation: Dict[str, Any],
        purpose: str
    ) -> Dict[str, Any]:
        """LLMを使用して改善提案生成"""
        try:
            issue = (
                f"Current score: {evaluation['score']}/100. "
                f"Weaknesses: {', '.join(evaluation.get('weaknesses', []))}"
            )
            
            improvement = self.llm_connector.generate_improvement_suggestion(
                code=code,
                issue=issue,
                context={
                    "evaluation": evaluation,
                    "purpose": purpose
                }
            )
            
            improvement["mode"] = "llm"
            return improvement
            
        except Exception as e:
            print(f"LLM improvement generation failed: {e}")
            return self._generate_improvement_with_template(code, evaluation)
    
    def _generate_improvement_with_template(
        self,
        code: str,
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """テンプレートベースの改善提案生成"""
        suggestions = evaluation.get("suggestions", [])
        
        return {
            "suggestions": suggestions,
            "priority": "medium" if evaluation.get("score", 50) < 70 else "low",
            "mode": "template",
            "message": "Consider the following improvements: " + ", ".join(suggestions)
        }
    
    def create_improvement_request(
        self,
        code: str,
        build_result: Dict[str, Any],
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        改善要求を作成
        
        Args:
            code: 評価対象コード
            build_result: ビルド結果
            use_llm: LLMを使用するか
        
        Returns:
            dict: 改善要求の結果
        """
        purpose = build_result.get("purpose", "Application development")
        
        # コード評価
        evaluation = self.evaluate_code(code, purpose, use_llm)
        
        # スコアが高い場合は改善不要
        if evaluation["score"] >= 80:
            return {
                "status": "good",
                "score": evaluation["score"],
                "message": "Code quality is excellent. No improvements needed.",
                "mode": evaluation.get("mode", "template")
            }
        
        # 改善提案を生成
        improvement = self.generate_improvement_suggestion(
            code, evaluation, purpose, use_llm
        )
        
        # 改善要求を保存
        request = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "improvement_request",
            "purpose": purpose,
            "evaluation": evaluation,
            "improvement": improvement,
            "status": "pending",
            "improvement_requests": improvement.get("suggestions", []),
            "builder_hint": (
                "前回の成果物評価を反映し、次回生成時は以下の改善要求を優先してください。"
            )
        }
        
        request_file = self._save_improvement_request(request)
        
        return {
            "status": "improvement_needed",
            "score": evaluation["score"],
            "request_file": str(request_file),
            "suggestions": evaluation.get("suggestions", []),
            "mode": evaluation.get("mode", "template")
        }
    
    def _save_improvement_request(self, request: Dict[str, Any]) -> Path:
        """改善要求を保存"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        request_file = (
            self.improvement_dir 
            / f"improvement_request_{timestamp}.json"
        )
        
        with open(request_file, "w", encoding="utf-8") as f:
            json.dump(request, f, ensure_ascii=False, indent=2)
        
        return request_file
    
    def load_latest_improvement_request(self) -> tuple:
        """
        最新の改善要求を読み込み
        
        Returns:
            tuple: (改善要求データ, ファイルパス)
        """
        files = sorted(
            self.improvement_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if not files:
            return {}, "改善要求はまだありません。"
        
        latest = files[0]
        
        with open(latest, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data, str(latest)
    
    def format_improvement_prompt(self, request: Dict[str, Any]) -> str:
        """
        改善要求をプロンプト形式にフォーマット
        
        Args:
            request: 改善要求データ
        
        Returns:
            str: フォーマット済みプロンプト
        """
        if not request:
            return ""
        
        lines = []
        lines.append("\n\n=== 改善要求 ===")
        
        suggestions = request.get("improvement_requests", [])
        if suggestions:
            lines.append("次の点を改善してください:")
            for suggestion in suggestions:
                lines.append(f"- {suggestion}")
        
        hint = request.get("builder_hint", "")
        if hint:
            lines.append(f"\nヒント: {hint}")
        
        return "\n".join(lines)
    
    def save_improvement_build_history(
        self,
        purpose: str,
        improved_purpose: str,
        request_file: str,
        build_result: Dict[str, Any]
    ) -> Path:
        """
        改善ビルド履歴を保存
        
        Args:
            purpose: 元の目的
            improved_purpose: 改善要求を含む目的
            request_file: 改善要求ファイル
            build_result: ビルド結果
        
        Returns:
            Path: 履歴ファイルパス
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        history_file = (
            self.improvement_history_dir
            / f"improvement_build_{timestamp}.json"
        )
        
        data = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "purpose": purpose,
            "improved_purpose": improved_purpose,
            "request_file": request_file,
            "build_result": build_result
        }
        
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return history_file
    
    def diagnose(self) -> Dict[str, Any]:
        """
        診断情報を取得
        
        Returns:
            dict: 診断情報
        """
        improvement_files = list(self.improvement_dir.glob("*.json"))
        history_files = list(self.improvement_history_dir.glob("*.json"))
        
        return {
            "improvement_request_count": len(improvement_files),
            "improvement_build_history_count": len(history_files),
            "llm_available": self.is_llm_available(),
            "stats": self.stats,
            "status": "OK" if self.is_llm_available() else "LLM unavailable",
            "mode": "llm" if self.is_llm_available() else "template"
        }
    
    def format_diagnosis(self) -> str:
        """診断情報をフォーマット"""
        diagnosis = self.diagnose()
        
        lines = []
        lines.append("=== ImprovementManager 診断 ===")
        lines.append(f"改善要求数: {diagnosis['improvement_request_count']}")
        lines.append(f"改善Build履歴数: {diagnosis['improvement_build_history_count']}")
        lines.append(f"LLM利用可能: {diagnosis['llm_available']}")
        lines.append(f"状態: {diagnosis['status']}")
        lines.append(f"モード: {diagnosis['mode']}")
        lines.append("")
        lines.append("統計情報:")
        for key, value in diagnosis['stats'].items():
            lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
