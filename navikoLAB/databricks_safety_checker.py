"""
DatabricksSafetyChecker - 事前安全チェッカー
Phase 2-B実装: 作業開始前の自動安全確認システム

Author: Naviko System
Created: 2026-07-05
Version: 1.0.0

機能:
- 作業開始前の自動チェック（APIキー、Git、ファイル同期、Workspace環境）
- 問題検出時の警告・自動修正
- Databricks環境特化の安全性確認
- AutoRecoveryEngineとの連携
"""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# AutoRecoveryEngineとの連携用
try:
    from auto_recovery_engine import AutoRecoveryEngine
    AUTO_RECOVERY_AVAILABLE = True
except ImportError:
    AUTO_RECOVERY_AVAILABLE = False


class DatabricksSafetyChecker:
    """
    Databricks事前安全チェッカー
    
    作業開始前に環境の安全性を自動チェックし、
    問題がある場合は警告または自動修正を実行します。
    
    主な機能:
    1. APIキー存在確認
    2. Git状態確認
    3. ファイル同期状態確認
    4. Databricks Workspace環境確認
    
    使用例:
        checker = DatabricksSafetyChecker()
        all_passed, results = checker.run_all_checks(auto_fix=True)
        if all_passed:
            print("作業開始可能")
        else:
            print(checker.format_check_report(results))
    """
    
    def __init__(self, workspace_root: str = "/Workspace/Users/7716no70@gmail.com/navikoLAB"):
        """
        初期化
        
        Args:
            workspace_root: Workspaceルートディレクトリ
        """
        self.workspace_root = Path(workspace_root)
        
        # AutoRecoveryEngine連携
        self.auto_recovery = None
        if AUTO_RECOVERY_AVAILABLE:
            try:
                self.auto_recovery = AutoRecoveryEngine(str(self.workspace_root))
            except Exception:
                pass
        
        # チェック項目定義
        self.checks = {
            "api_key": {
                "name": "APIキー確認",
                "check_func": self._check_api_key,
                "severity": "HIGH",
                "auto_fix": True
            },
            "git_status": {
                "name": "Git状態確認",
                "check_func": self._check_git_status,
                "severity": "MEDIUM",
                "auto_fix": False
            },
            "file_sync": {
                "name": "ファイル同期確認",
                "check_func": self._check_file_sync,
                "severity": "MEDIUM",
                "auto_fix": False
            },
            "workspace_env": {
                "name": "Workspace環境確認",
                "check_func": self._check_workspace_env,
                "severity": "LOW",
                "auto_fix": False
            }
        }
    
    def run_all_checks(self, auto_fix: bool = True) -> Tuple[bool, List[Dict]]:
        """
        全チェックを実行
        
        Args:
            auto_fix: 自動修正を実行するか
        
        Returns:
            (全チェック成功, チェック結果リスト)
        """
        results = []
        all_passed = True
        
        for check_id, check_config in self.checks.items():
            try:
                passed, details = check_config["check_func"]()
                
                result = {
                    "check_id": check_id,
                    "check_name": check_config["name"],
                    "severity": check_config["severity"],
                    "passed": passed,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                
                if not passed:
                    # 自動修正試行
                    if auto_fix and check_config.get("auto_fix"):
                        fixed = self._try_auto_fix(check_id, details)
                        result["auto_fixed"] = fixed
                        if fixed:
                            result["passed"] = True
                        else:
                            all_passed = False
                    else:
                        all_passed = False
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "check_id": check_id,
                    "check_name": check_config["name"],
                    "severity": "ERROR",
                    "passed": False,
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                })
                all_passed = False
        
        return all_passed, results
    
    def _check_api_key(self) -> Tuple[bool, Dict]:
        """
        APIキー存在確認
        
        Returns:
            (チェック合格, 詳細情報)
        """
        api_key = os.environ.get('GROQ_API_KEY')
        
        if not api_key:
            return False, {
                "message": "GROQ_API_KEYが環境変数に設定されていません",
                "suggestion": "APIキーを環境変数に設定してください",
                "auto_fixable": True
            }
        
        # キーの長さチェック（基本的な妥当性確認）
        if len(api_key) < 20:
            return False, {
                "message": "APIキーが短すぎます（無効な可能性）",
                "suggestion": "正しいAPIキーを設定してください",
                "auto_fixable": False
            }
        
        return True, {
            "message": "APIキーが正しく設定されています",
            "key_preview": f"{api_key[:20]}...{api_key[-10:]}"
        }
    
    def _check_git_status(self) -> Tuple[bool, Dict]:
        """
        Git状態確認
        
        Returns:
            (チェック合格, 詳細情報)
        """
        try:
            # Gitリポジトリ確認
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, {
                    "message": "Gitリポジトリが見つかりません",
                    "suggestion": "Gitリポジトリを初期化してください",
                    "auto_fixable": False
                }
            
            # 未コミットの変更確認
            uncommitted = result.stdout.strip()
            if uncommitted:
                files = uncommitted.split('\n')
                return False, {
                    "message": f"未コミットの変更があります（{len(files)}ファイル）",
                    "uncommitted_files": files[:5],
                    "suggestion": "変更をコミットしてください",
                    "auto_fixable": False
                }
            
            return True, {
                "message": "Git状態は正常です（コミット済み）"
            }
            
        except subprocess.TimeoutExpired:
            return False, {
                "message": "Git状態確認がタイムアウトしました",
                "suggestion": "Gitの状態を手動で確認してください",
                "auto_fixable": False
            }
        except FileNotFoundError:
            return False, {
                "message": "Gitコマンドが見つかりません",
                "suggestion": "Gitがインストールされているか確認してください",
                "auto_fixable": False
            }
        except Exception as e:
            return False, {
                "message": f"Git状態確認エラー: {str(e)}",
                "auto_fixable": False
            }
    
    def _check_file_sync(self) -> Tuple[bool, Dict]:
        """
        ファイル同期状態確認
        
        Returns:
            (チェック合格, 詳細情報)
        """
        # Phase 1ファイルの存在確認
        phase1_files = [
            "meta_cognition_engine.py",
            "problem_pattern_learner.py",
            "core_orchestrator.py"
        ]
        
        # Phase 2ファイルの存在確認
        phase2_files = [
            "auto_recovery_engine.py",
            "databricks_safety_checker.py"
        ]
        
        missing_files = []
        existing_files = []
        
        for file in phase1_files + phase2_files:
            file_path = self.workspace_root / file
            if file_path.exists():
                existing_files.append(file)
            else:
                missing_files.append(file)
        
        if missing_files:
            return False, {
                "message": f"{len(missing_files)}個のファイルが見つかりません",
                "missing_files": missing_files,
                "suggestion": "ファイルを同期してください",
                "auto_fixable": False
            }
        
        return True, {
            "message": "全ファイル存在確認完了",
            "existing_files": existing_files
        }
    
    def _check_workspace_env(self) -> Tuple[bool, Dict]:
        """
        Workspace環境確認
        
        Returns:
            (チェック合格, 詳細情報)
        """
        checks = []
        
        # Workspaceディレクトリ確認
        if self.workspace_root.exists():
            checks.append("✅ Workspaceディレクトリ存在")
        else:
            checks.append("❌ Workspaceディレクトリが見つかりません")
        
        # 書き込み権限確認
        test_file = self.workspace_root / ".write_test"
        try:
            test_file.touch()
            test_file.unlink()
            checks.append("✅ 書き込み権限あり")
        except Exception:
            checks.append("❌ 書き込み権限なし")
        
        # Python環境確認
        import sys
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        checks.append(f"✅ Python {python_version}")
        
        all_ok = all("✅" in check for check in checks)
        
        return all_ok, {
            "message": "Workspace環境正常" if all_ok else "Workspace環境に問題があります",
            "checks": checks
        }
    
    def _try_auto_fix(self, check_id: str, details: Dict) -> bool:
        """
        自動修正を試行
        
        Args:
            check_id: チェックID
            details: チェック詳細情報
        
        Returns:
            修正成功フラグ
        """
        if check_id == "api_key":
            # APIキー自動設定（AutoRecoveryEngine経由）
            if self.auto_recovery:
                test_error = Exception("401 Unauthorized: Invalid API key")
                success, strategy, fix_details = self.auto_recovery.auto_recover(test_error)
                return success
            else:
        　　
　　　　# AutoRecoveryがない場合は設定不可
　　　　             
        return False
    
    def format_check_report(self, results: List[Dict]) -> str:
        """
        チェックレポートをフォーマット
        
        Args:
            results: チェック結果リスト
        
        Returns:
            フォーマット済みレポート
        """
        report = ["=" * 70]
        report.append("DatabricksSafetyChecker - チェックレポート")
        report.append("=" * 70)
        
        # サマリー
        total = len(results)
        passed = sum(1 for r in results if r.get("passed"))
        failed = total - passed
        
        report.append(f"\n[サマリー]")
        report.append(f"  総チェック数: {total}")
        report.append(f"  合格: {passed}")
        report.append(f"  不合格: {failed}")
        report.append(f"  合格率: {passed/total*100:.1f}%")
        
        # 詳細
        report.append(f"\n[詳細]")
        for result in results:
            status = "✅" if result.get("passed") else "❌"
            report.append(f"\n{status} {result['check_name']} ({result['severity']})")
            report.append(f"   {result['details'].get('message', 'N/A')}")
            
            if result.get("auto_fixed"):
                report.append(f"   🔧 自動修正済み")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


# テスト用エントリーポイント
def test_databricks_safety_checker():
    """DatabricksSafetyCheckerのテスト"""
    print("=" * 70)
    print("DatabricksSafetyChecker - 動作テスト")
    print("=" * 70)
    
    # チェッカー初期化
    checker = DatabricksSafetyChecker()
    print(f"✅ 初期化完了")
    print(f"   - チェック項目: {len(checker.checks)}種類")
    print(f"   - AutoRecovery連携: {'有効' if AUTO_RECOVERY_AVAILABLE else '無効'}")
    
    # 全チェック実行
    all_passed, results = checker.run_all_checks(auto_fix=True)
    
    # レポート表示
    print("\n" + checker.format_check_report(results))
    
    # 結果
    if all_passed:
        print("\n✅ 全チェック合格 - 作業開始可能")
    else:
        print("\n⚠️ 一部チェック不合格 - 問題を確認してください")


if __name__ == "__main__":
    test_databricks_safety_checker()
