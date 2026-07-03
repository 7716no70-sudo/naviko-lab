"""
ErrorDiagnosticEngine - エラー自動診断・解決提案モジュール

このモジュールは以下の機能を提供：
1. エラーを自動診断して原因を特定
2. 日本語で解決策を提案
3. ワンクリック自動修復
4. ExperienceMemoryと連携して過去の経験から学習

使用例：
    engine = ErrorDiagnosticEngine(
        lab_dir=Path("/path/to/navikoLAB"),
        experience_memory=ExperienceMemory(lab_dir)
    )
    
    # エラー診断
    diagnosis = engine.diagnose_error("401 Client Error: Unauthorized for url: https://api.groq.com/...")
    
    # 解決策提案
    solutions = engine.suggest_solutions(diagnosis)
    
    # 自動修復
    result = engine.auto_fix(solutions[0])
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


class ErrorDiagnosticEngine:
    """エラー自動診断・解決提案エンジン"""
    
    def __init__(self, lab_dir: Path, experience_memory=None):
        """
        初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
            experience_memory: ExperienceMemoryインスタンス（オプション）
        """
        self.lab_dir = Path(lab_dir)
        self.experience_memory = experience_memory
        
        # エラーパターンライブラリ
        self.error_patterns = self._build_error_patterns()
    
    def _build_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """エラーパターンライブラリを構築"""
        return {
            "401_unauthorized": {
                "patterns": [
                    r"401.*Unauthorized",
                    r"Authentication.*failed",
                    r"Invalid.*API.*key"
                ],
                "category": "Authentication",
                "severity": "High",
                "common_causes": [
                    "APIキーが無効または期限切れ",
                    "環境変数が正しく設定されていない",
                    "APIキーの権限が不足"
                ],
                "auto_fixable": True
            },
            "403_forbidden": {
                "patterns": [
                    r"403.*Forbidden",
                    r"Access.*denied",
                    r"Permission.*denied"
                ],
                "category": "Authorization",
                "severity": "High",
                "common_causes": [
                    "アクセス権限が不足",
                    "リソースへのアクセスが制限されている",
                    "IPアドレスがブロックされている"
                ],
                "auto_fixable": False
            },
            "404_not_found": {
                "patterns": [
                    r"404.*Not Found",
                    r"File.*not found",
                    r"Module.*not found",
                    r"No such file"
                ],
                "category": "Resource",
                "severity": "Medium",
                "common_causes": [
                    "ファイルまたはモジュールが存在しない",
                    "パスが間違っている",
                    "インストールされていない"
                ],
                "auto_fixable": True
            },
            "500_internal_server": {
                "patterns": [
                    r"500.*Internal Server Error",
                    r"Server.*error",
                    r"Service.*unavailable"
                ],
                "category": "Server",
                "severity": "High",
                "common_causes": [
                    "サーバー側のエラー",
                    "リクエストの形式が不正",
                    "サービスが一時的にダウン"
                ],
                "auto_fixable": False
            },
            "module_not_found": {
                "patterns": [
                    r"ModuleNotFoundError",
                    r"No module named",
                    r"ImportError"
                ],
                "category": "Dependency",
                "severity": "Medium",
                "common_causes": [
                    "必要なパッケージがインストールされていない",
                    "パッケージ名のスペルミス",
                    "仮想環境が有効になっていない"
                ],
                "auto_fixable": True
            },
            "connection_error": {
                "patterns": [
                    r"Connection.*refused",
                    r"Connection.*timeout",
                    r"Network.*error",
                    r"Unable to connect"
                ],
                "category": "Network",
                "severity": "High",
                "common_causes": [
                    "ネットワーク接続が切れている",
                    "サーバーが起動していない",
                    "ファイアウォールがブロックしている"
                ],
                "auto_fixable": False
            },
            "syntax_error": {
                "patterns": [
                    r"SyntaxError",
                    r"Invalid syntax",
                    r"Unexpected token"
                ],
                "category": "Code",
                "severity": "Medium",
                "common_causes": [
                    "コードの構文エラー",
                    "括弧の対応が合っていない",
                    "インデントが不正"
                ],
                "auto_fixable": False
            }
        }
    
    def diagnose_error(self, error_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        エラーを診断
        
        Args:
            error_message: エラーメッセージ
            context: エラー発生時のコンテキスト
            
        Returns:
            診断結果
        """
        context = context or {}
        
        # エラータイプを特定
        error_type, pattern_match = self._identify_error_type(error_message)
        
        if not error_type:
            return {
                "success": False,
                "error_type": "unknown",
                "message": "エラータイプを特定できませんでした",
                "original_error": error_message
            }
        
        pattern_info = self.error_patterns[error_type]
        
        # 過去の経験から学習（ExperienceMemory連携）
        similar_errors = []
        learned_solution = None
        
        if self.experience_memory:
            similar_errors = self.experience_memory.find_similar_errors(error_message, threshold=0.5)
            if similar_errors:
                learned_solution = similar_errors[0].get("best_solution")
        
        diagnosis = {
            "success": True,
            "error_type": error_type,
            "category": pattern_info["category"],
            "severity": pattern_info["severity"],
            "original_error": error_message,
            "pattern_matched": pattern_match.group(0) if pattern_match else None,
            "common_causes": pattern_info["common_causes"],
            "auto_fixable": pattern_info["auto_fixable"],
            "similar_errors_found": len(similar_errors),
            "learned_solution": learned_solution,
            "context": context,
            "diagnosed_at": datetime.now().isoformat()
        }
        
        return diagnosis
    
    def _identify_error_type(self, error_message: str) -> Tuple[Optional[str], Optional[re.Match]]:
        """エラータイプを特定"""
        for error_type, pattern_info in self.error_patterns.items():
            for pattern in pattern_info["patterns"]:
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    return error_type, match
        
        return None, None
    
    def suggest_solutions(self, diagnosis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解決策を提案
        
        Args:
            diagnosis: 診断結果
            
        Returns:
            解決策リスト
        """
        error_type = diagnosis["error_type"]
        solutions = []
        
        # 学習済み解決策を最優先
        if diagnosis.get("learned_solution"):
            learned = diagnosis["learned_solution"]
            solutions.append({
                "priority": "highest",
                "source": "learned",
                "title": "🎓 過去の経験から（成功率: {:.0%}）".format(learned["success_rate"]),
                "description": learned["solution"],
                "auto_fixable": diagnosis["auto_fixable"],
                "success_rate": learned["success_rate"],
                "used_count": learned["total_uses"]
            })
        
        # エラータイプ別の標準的な解決策
        if error_type == "401_unauthorized":
            solutions.extend([
                {
                    "priority": "high",
                    "source": "built-in",
                    "title": "🔑 APIキーを更新",
                    "description": "環境変数 GROQ_API_KEY（または該当するAPIキー）を最新の有効なキーに更新してください。",
                    "steps": [
                        "1. APIプロバイダーのコンソールで新しいAPIキーを発行",
                        "2. システム環境変数を開く（Windows: sysdm.cpl → 環境変数）",
                        "3. 該当する環境変数を新しいキーに更新",
                        "4. アプリケーションを再起動"
                    ],
                    "auto_fixable": True,
                    "auto_fix_method": "update_api_key"
                },
                {
                    "priority": "medium",
                    "source": "built-in",
                    "title": "🔄 環境変数の再読み込み",
                    "description": "環境変数が正しく設定されているか確認し、アプリケーションを再起動してください。",
                    "steps": [
                        "1. コマンドプロンプトで 'echo %GROQ_API_KEY%' を実行",
                        "2. キーが表示されることを確認",
                        "3. アプリケーションを完全に終了",
                        "4. 新しいコマンドプロンプトで再起動"
                    ],
                    "auto_fixable": False
                }
            ])
        
        elif error_type == "module_not_found":
            module_name = self._extract_module_name(diagnosis["original_error"])
            solutions.extend([
                {
                    "priority": "high",
                    "source": "built-in",
                    "title": f"📦 {module_name} をインストール",
                    "description": f"pip install {module_name} を実行してパッケージをインストールしてください。",
                    "steps": [
                        f"1. コマンドプロンプトを開く",
                        f"2. 'pip install {module_name}' を実行",
                        f"3. インストール完了後、アプリケーションを再起動"
                    ],
                    "auto_fixable": True,
                    "auto_fix_method": "install_package",
                    "package_name": module_name
                }
            ])
        
        elif error_type == "404_not_found":
            solutions.extend([
                {
                    "priority": "high",
                    "source": "built-in",
                    "title": "📂 パスを確認",
                    "description": "ファイルまたはリソースのパスが正しいか確認してください。",
                    "steps": [
                        "1. エラーメッセージからファイル名を確認",
                        "2. ファイルが存在するか確認",
                        "3. パスの区切り文字が正しいか確認（Windows: \\、Linux/Mac: /）",
                        "4. 相対パスではなく絶対パスを使用"
                    ],
                    "auto_fixable": False
                }
            ])
        
        elif error_type == "connection_error":
            solutions.extend([
                {
                    "priority": "high",
                    "source": "built-in",
                    "title": "🌐 ネットワーク接続を確認",
                    "description": "インターネット接続とファイアウォール設定を確認してください。",
                    "steps": [
                        "1. インターネット接続を確認",
                        "2. ファイアウォールの設定を確認",
                        "3. サーバーが起動しているか確認（ローカルサービスの場合）",
                        "4. VPNを使用している場合は一時的に無効化して試す"
                    ],
                    "auto_fixable": False
                }
            ])
        
        # 一般的な解決策
        solutions.append({
            "priority": "low",
            "source": "built-in",
            "title": "📖 ドキュメントを確認",
            "description": "公式ドキュメントまたはオンラインフォーラムで詳細情報を確認してください。",
            "auto_fixable": False
        })
        
        # 優先度でソート
        priority_order = {"highest": 0, "high": 1, "medium": 2, "low": 3}
        solutions.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return solutions
    
    def _extract_module_name(self, error_message: str) -> str:
        """エラーメッセージからモジュール名を抽出"""
        match = re.search(r"No module named [\'\"]([^\'\"]+ )['\"]", error_message)
        if match:
            return match.group(1)
        
        match = re.search(r"ModuleNotFoundError:.*[\'\"]([^\'\"]+ )['\"]", error_message)
        if match:
            return match.group(1)
        
        return "unknown_module"
    
    def auto_fix(self, solution: Dict[str, Any], diagnosis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        自動修復を実行
        
        Args:
            solution: 解決策
            diagnosis: 診断結果（オプション）
            
        Returns:
            修復結果
        """
        if not solution.get("auto_fixable"):
            return {
                "success": False,
                "message": "この解決策は自動修復に対応していません。手動で実行してください。",
                "solution": solution
            }
        
        auto_fix_method = solution.get("auto_fix_method")
        
        if auto_fix_method == "install_package":
            return self._auto_fix_install_package(solution)
        
        elif auto_fix_method == "update_api_key":
            return self._auto_fix_update_api_key(solution)
        
        else:
            return {
                "success": False,
                "message": f"自動修復メソッド '{auto_fix_method}' は実装されていません。",
                "solution": solution
            }
    
    def _auto_fix_install_package(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """パッケージを自動インストール"""
        package_name = solution.get("package_name", "")
        
        if not package_name or package_name == "unknown_module":
            return {
                "success": False,
                "message": "パッケージ名を特定できませんでした。",
                "solution": solution
            }
        
        try:
            print(f"🔧 {package_name} をインストール中...")
            result = subprocess.run(
                ["pip", "install", package_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"✅ {package_name} のインストールに成功しました。",
                    "output": result.stdout,
                    "solution": solution
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ {package_name} のインストールに失敗しました。",
                    "error": result.stderr,
                    "solution": solution
                }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "インストールがタイムアウトしました。",
                "solution": solution
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"インストール中にエラーが発生しました: {str(e)}",
                "solution": solution
            }
    
    def _auto_fix_update_api_key(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """APIキーを自動更新（インタラクティブ）"""
        # この機能は実際にはGUIで実装すべき
        # ここではプレースホルダーとして情報を返す
        return {
            "success": False,
            "message": "APIキーの更新はGUIから実行してください。",
            "instructions": solution.get("steps", []),
            "solution": solution,
            "requires_user_input": True
        }
    
    def format_diagnosis(self, diagnosis: Dict[str, Any]) -> str:
        """診断結果を整形して表示"""
        if not diagnosis.get("success"):
            return f"❌ 診断失敗: {diagnosis.get('message')}"
        
        output = []
        output.append("🔍 エラー診断結果")
        output.append("=" * 60)
        output.append(f"エラータイプ: {diagnosis['error_type']}")
        output.append(f"カテゴリー: {diagnosis['category']}")
        output.append(f"深刻度: {diagnosis['severity']}")
        output.append(f"自動修復: {'可能' if diagnosis['auto_fixable'] else '不可'}")
        output.append("")
        
        output.append("📋 考えられる原因:")
        for i, cause in enumerate(diagnosis["common_causes"], 1):
            output.append(f"  {i}. {cause}")
        
        if diagnosis.get("learned_solution"):
            output.append("")
            output.append("🎓 過去の経験から:")
            learned = diagnosis["learned_solution"]
            output.append(f"  成功率: {learned['success_rate']:.0%} ({learned['success_count']}/{learned['total_uses']}回)")
            output.append(f"  解決策: {learned['solution']}")
        
        if diagnosis.get("similar_errors_found", 0) > 0:
            output.append("")
            output.append(f"💡 類似エラー: {diagnosis['similar_errors_found']}件の関連事例が見つかりました")
        
        output.append("=" * 60)
        
        return "\n".join(output)
    
    def format_solutions(self, solutions: List[Dict[str, Any]]) -> str:
        """解決策リストを整形して表示"""
        output = []
        output.append("💡 提案する解決策")
        output.append("=" * 60)
        
        for i, solution in enumerate(solutions, 1):
            output.append(f"\n{i}. {solution['title']}")
            output.append(f"   優先度: {solution['priority']}")
            output.append(f"   {solution['description']}")
            
            if solution.get("steps"):
                output.append(f"\n   📝 手順:")
                for step in solution["steps"]:
                    output.append(f"      {step}")
            
            if solution.get("auto_fixable"):
                output.append(f"\n   ✨ 自動修復対応")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
