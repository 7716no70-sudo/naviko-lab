"""
Naviko LAB - LLM Connector Module
Groq API統合モジュール: 実際のAIによるコード生成、改善提案、評価を提供
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path


class LLMConnector:
    """
    Groq APIを使用したLLM接続クラス
    コード生成、改善提案、評価などの機能を提供
    """
    
    def __init__(
        self,
        lab_dir: Path,
        api_key: Optional[str] = None,
        model: str = "llama-3.1-8b-instant",
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        LLMConnectorの初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
            api_key: Groq APIキー (Noneの場合は環境変数から取得)
            model: 使用するモデル名
            max_retries: リトライ回数
            timeout: タイムアウト時間（秒）
        """
        self.lab_dir = Path(lab_dir)
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        
        # 履歴保存用ディレクトリ
        self.history_dir = self.lab_dir / "llm_history"
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        # Groq APIクライアントの初期化を試みる
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Groq APIクライアントの初期化"""
        try:
            # groqパッケージのインポートを試みる
            from groq import Groq
            
            if not self.api_key:
                print("Warning: GROQ_API_KEY is not set. LLM features will be disabled.")
                return
            
            self.client = Groq(api_key=self.api_key)
            print("✓ Groq API client initialized successfully")
            
        except ImportError:
            print("Warning: 'groq' package not found. Install with: pip install groq")
            print("LLM features will be disabled until the package is installed.")
        except Exception as e:
            print(f"Warning: Failed to initialize Groq client: {e}")
    
    def is_available(self) -> bool:
        """
        LLM接続が利用可能かどうかを確認
        
        Returns:
            bool: 利用可能ならTrue
        """
        return self.client is not None and bool(self.api_key)
    
    def generate_code(
        self,
        purpose: str,
        language: str = "python",
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        目的に基づいてコードを生成
        
        Args:
            purpose: コード生成の目的・要件
            language: 生成するコードの言語
            context: 追加のコンテキスト情報
            temperature: 生成の多様性（0.0-1.0）
            max_tokens: 最大トークン数
        
        Returns:
            Dict: 生成結果 {
                "success": bool,
                "code": str,
                "explanation": str,
                "language": str,
                "model": str,
                "timestamp": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "LLM is not available. Check API key and groq package installation.",
                "code": self._generate_fallback_code(purpose, language),
                "explanation": "Fallback code generated (LLM not available)",
                "language": language,
                "model": "fallback",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        
        prompt = self._build_code_generation_prompt(purpose, language, context)
        
        result = self._call_llm(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            operation="generate_code"
        )
        
        if result["success"]:
            # コードブロックを抽出
            code = self._extract_code_block(result["content"], language)
            
            return {
                "success": True,
                "code": code,
                "explanation": result["content"],
                "language": language,
                "model": self.model,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "usage": result.get("usage", {})
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "code": self._generate_fallback_code(purpose, language),
                "explanation": "Error occurred, fallback code generated",
                "language": language,
                "model": "fallback",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def generate_improvement_suggestion(
        self,
        code: str,
        issue: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        コードの改善提案を生成
        
        Args:
            code: 改善対象のコード
            issue: 問題点・改善したい内容
            context: 追加のコンテキスト情報
        
        Returns:
            Dict: 改善提案 {
                "success": bool,
                "suggestion": str,
                "improved_code": str,
                "explanation": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "LLM is not available",
                "suggestion": "LLM not available for improvement suggestions",
                "improved_code": code,
                "explanation": "Original code returned (LLM not available)"
            }
        
        prompt = self._build_improvement_prompt(code, issue, context)
        
        result = self._call_llm(
            prompt=prompt,
            temperature=0.5,
            max_tokens=2000,
            operation="generate_improvement"
        )
        
        if result["success"]:
            content = result["content"]
            improved_code = self._extract_code_block(content, "python")
            
            return {
                "success": True,
                "suggestion": content,
                "improved_code": improved_code if improved_code else code,
                "explanation": content,
                "model": self.model,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "usage": result.get("usage", {})
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "suggestion": "Failed to generate improvement",
                "improved_code": code,
                "explanation": result.get("error", "Error occurred")
            }
    
    def evaluate_code(
        self,
        code: str,
        purpose: str,
        criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        生成されたコードを評価
        
        Args:
            code: 評価対象のコード
            purpose: コードの目的
            criteria: 評価基準のリスト
        
        Returns:
            Dict: 評価結果 {
                "success": bool,
                "score": int (0-100),
                "strengths": List[str],
                "weaknesses": List[str],
                "suggestions": List[str],
                "evaluation": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "LLM is not available",
                "score": 50,
                "strengths": ["Code structure appears valid"],
                "weaknesses": ["Cannot perform detailed evaluation without LLM"],
                "suggestions": ["Install groq package and set API key for detailed evaluation"],
                "evaluation": "Basic evaluation only (LLM not available)"
            }
        
        prompt = self._build_evaluation_prompt(code, purpose, criteria)
        
        result = self._call_llm(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1500,
            operation="evaluate_code"
        )
        
        if result["success"]:
            evaluation = self._parse_evaluation(result["content"])
            return evaluation
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "score": 0,
                "strengths": [],
                "weaknesses": ["Evaluation failed"],
                "suggestions": ["Retry evaluation"],
                "evaluation": result.get("error", "Error occurred")
            }
    
    def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        operation: str = "general"
    ) -> Dict[str, Any]:
        """
        LLM APIを呼び出し（リトライ機能付き）
        
        Args:
            prompt: 送信するプロンプト
            temperature: 生成の多様性
            max_tokens: 最大トークン数
            operation: 操作の種類（ログ用）
        
        Returns:
            Dict: API応答 {
                "success": bool,
                "content": str,
                "usage": Dict,
                "error": str (失敗時)
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "LLM client not available"
            }
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert Python programmer and code assistant. Provide clear, well-structured, and working code."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.timeout
                )
                
                content = response.choices[0].message.content
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
                
                # 履歴を保存
                self._save_history(operation, prompt, content, usage)
                
                return {
                    "success": True,
                    "content": content,
                    "usage": usage
                }
                
            except Exception as e:
                error_msg = f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}"
                print(error_msg)
                
                if attempt == self.max_retries - 1:
                    return {
                        "success": False,
                        "error": f"All retry attempts failed: {str(e)}"
                    }
                
                # リトライ前に待機
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {
            "success": False,
            "error": "Max retries exceeded"
        }
    
    def _build_code_generation_prompt(
        self,
        purpose: str,
        language: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """コード生成用のプロンプトを構築"""
        prompt = f"""Generate {language} code for the following purpose:

Purpose: {purpose}

Requirements:
- Write clean, well-structured, and working code
- Include comments explaining key parts
- Follow best practices for {language}
- Make the code production-ready
"""
        
        if context:
            prompt += f"\n\nAdditional Context:\n{json.dumps(context, indent=2, ensure_ascii=False)}"
        
        prompt += f"\n\nProvide the complete {language} code within a code block."
        
        return prompt
    
    def _build_improvement_prompt(
        self,
        code: str,
        issue: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """改善提案用のプロンプトを構築"""
        prompt = f"""Analyze the following code and suggest improvements:

Current Code:
```python
{code}
```

Issue/Improvement Request: {issue}
"""
        
        if context:
            prompt += f"\n\nContext:\n{json.dumps(context, indent=2, ensure_ascii=False)}"
        
        prompt += """

Provide:
1. Analysis of the current code
2. Specific improvement suggestions
3. Improved version of the code

Include the improved code in a code block.
"""
        
        return prompt
    
    def _build_evaluation_prompt(
        self,
        code: str,
        purpose: str,
        criteria: Optional[List[str]]
    ) -> str:
        """コード評価用のプロンプトを構築"""
        prompt = f"""Evaluate the following code based on the given purpose:

Purpose: {purpose}

Code to Evaluate:
```python
{code}
```

Evaluation Criteria:
"""
        
        if criteria:
            for criterion in criteria:
                prompt += f"- {criterion}\n"
        else:
            prompt += """- Correctness: Does it achieve the purpose?
- Code Quality: Is it clean and well-structured?
- Best Practices: Does it follow Python best practices?
- Readability: Is it easy to understand?
- Completeness: Is it production-ready?
"""
        
        prompt += """

Provide your evaluation in the following format:

SCORE: [0-100]

STRENGTHS:
- [List specific strengths]

WEAKNESSES:
- [List specific weaknesses]

SUGGESTIONS:
- [List improvement suggestions]

OVERALL EVALUATION:
[Detailed evaluation text]
"""
        
        return prompt
    
    def _extract_code_block(self, text: str, language: str = "python") -> str:
        """
        テキストからコードブロックを抽出
        
        Args:
            text: 抽出元のテキスト
            language: コード言語
        
        Returns:
            str: 抽出されたコード
        """
        import re
        
        # マークダウンのコードブロックパターン
        pattern = f"```{language}\\s*\\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # 言語指定なしのコードブロック
        pattern = "```\\s*\\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # コードブロックが見つからない場合はテキスト全体を返す
        return text.strip()
    
    def _parse_evaluation(self, evaluation_text: str) -> Dict[str, Any]:
        """
        評価テキストをパース
        
        Args:
            evaluation_text: 評価テキスト
        
        Returns:
            Dict: パースされた評価結果
        """
        import re
        
        result = {
            "success": True,
            "score": 50,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "evaluation": evaluation_text
        }
        
        # SCOREを抽出
        score_match = re.search(r"SCORE:\s*(\d+)", evaluation_text, re.IGNORECASE)
        if score_match:
            result["score"] = int(score_match.group(1))
        
        # STRENGTHSを抽出
        strengths_match = re.search(
            r"STRENGTHS:\s*(.*?)(?=WEAKNESSES:|SUGGESTIONS:|OVERALL|$)",
            evaluation_text,
            re.DOTALL | re.IGNORECASE
        )
        if strengths_match:
            strengths_text = strengths_match.group(1).strip()
            result["strengths"] = [
                line.strip("- ").strip()
                for line in strengths_text.split("\n")
                if line.strip().startswith("-")
            ]
        
        # WEAKNESSESを抽出
        weaknesses_match = re.search(
            r"WEAKNESSES:\s*(.*?)(?=SUGGESTIONS:|OVERALL|$)",
            evaluation_text,
            re.DOTALL | re.IGNORECASE
        )
        if weaknesses_match:
            weaknesses_text = weaknesses_match.group(1).strip()
            result["weaknesses"] = [
                line.strip("- ").strip()
                for line in weaknesses_text.split("\n")
                if line.strip().startswith("-")
            ]
        
        # SUGGESTIONSを抽出
        suggestions_match = re.search(
            r"SUGGESTIONS:\s*(.*?)(?=OVERALL|$)",
            evaluation_text,
            re.DOTALL | re.IGNORECASE
        )
        if suggestions_match:
            suggestions_text = suggestions_match.group(1).strip()
            result["suggestions"] = [
                line.strip("- ").strip()
                for line in suggestions_text.split("\n")
                if line.strip().startswith("-")
            ]
        
        return result
    
    def _generate_fallback_code(self, purpose: str, language: str) -> str:
        """
        LLMが利用できない場合のフォールバックコード
        
        Args:
            purpose: コードの目的
            language: 言語
        
        Returns:
            str: フォールバックコード
        """
        if language.lower() == "python":
            return f'''"""
{purpose}

NOTE: This is a basic template generated without LLM.
Please implement the actual functionality.
"""

def main():
    """Main function"""
    print("TODO: Implement {purpose}")
    pass

if __name__ == "__main__":
    main()
'''
        else:
            return f"// TODO: Implement {purpose}\n// LLM not available for code generation"
    
    def _save_history(
        self,
        operation: str,
        prompt: str,
        response: str,
        usage: Dict[str, int]
    ):
        """
        LLM呼び出し履歴を保存
        
        Args:
            operation: 操作の種類
            prompt: 送信したプロンプト
            response: 受信したレスポンス
            usage: トークン使用量
        """
        try:
            history_file = (
                self.history_dir
                / f"llm_{operation}_{time.strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            history_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "operation": operation,
                "model": self.model,
                "prompt": prompt,
                "response": response,
                "usage": usage
            }
            
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Warning: Failed to save LLM history: {e}")
    
    def diagnose(self) -> Dict[str, Any]:
        """
        LLMコネクタの診断情報を取得
        
        Returns:
            Dict: 診断情報
        """
        history_files = list(self.history_dir.glob("*.json"))
        
        return {
            "available": self.is_available(),
            "api_key_set": bool(self.api_key),
            "client_initialized": self.client is not None,
            "model": self.model,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "history_count": len(history_files),
            "history_dir": str(self.history_dir)
        }
    
    def format_diagnosis(self, diagnosis: Optional[Dict[str, Any]] = None) -> str:
        """
        診断情報をフォーマット
        
        Args:
            diagnosis: 診断情報（Noneの場合は新規取得）
        
        Returns:
            str: フォーマットされた診断情報
        """
        if diagnosis is None:
            diagnosis = self.diagnose()
        
        lines = []
        lines.append("=== LLMConnector 診断 ===")
        lines.append(f"利用可能: {'✓' if diagnosis['available'] else '✗'}")
        lines.append(f"APIキー設定: {'✓' if diagnosis['api_key_set'] else '✗'}")
        lines.append(f"クライアント初期化: {'✓' if diagnosis['client_initialized'] else '✗'}")
        lines.append(f"モデル: {diagnosis['model']}")
        lines.append(f"最大リトライ: {diagnosis['max_retries']}")
        lines.append(f"タイムアウト: {diagnosis['timeout']}秒")
        lines.append(f"履歴件数: {diagnosis['history_count']}")
        lines.append(f"履歴ディレクトリ: {diagnosis['history_dir']}")
        
        return "\n".join(lines)
