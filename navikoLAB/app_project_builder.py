# -*- coding: utf-8 -*-
"""
AppProjectBuilder - アプリケーションプロジェクトビルダー (LLM統合版)

LLMConnectorを統合し、AIパワード生成でアプリプロジェクトを構築します。
テンプレートベースの生成からAI生成へ移行し、より高品質な成果物を生成します。

機能:
- LLM駆動のmain.py生成
- LLM駆動のREADME.md生成
- 自動フォールバック（LLM利用不可時）
- 実行履歴の保存
- 診断情報の提供

作成日: 2026-07-01
LLM統合: 完了
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# LLMConnectorのインポート
try:
    from .llm_connector import LLMConnector
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    LLMConnector = None


class AppProjectBuilder:
    """
    アプリケーションプロジェクトビルダー（LLM統合版）
    
    Attributes:
        lab_dir (Path): LABディレクトリ
        llm_connector (LLMConnector): LLM接続
        action_planner: アクションプランナー
        workspace_manager: ワークスペースマネージャー
        artifact_writer: アーティファクトライター
        history_dir (Path): 履歴保存ディレクトリ
        stats (Dict): 統計情報
    """
    
    def __init__(
        self,
        lab_dir: Path,
        action_planner=None,
        workspace_manager=None,
        artifact_writer=None,
        api_key: Optional[str] = None
    ):
        """
        初期化
        
        Args:
            lab_dir: LABディレクトリのパス
            action_planner: ActionPlannerインスタンス（オプション）
            workspace_manager: WorkspaceManagerインスタンス（オプション）
            artifact_writer: ArtifactWriterインスタンス（オプション）
            api_key: Groq APIキー（オプション、環境変数からも取得可能）
        """
        self.lab_dir = Path(lab_dir)
        self.action_planner = action_planner
        self.workspace_manager = workspace_manager
        self.artifact_writer = artifact_writer
        
        # LLMConnectorの初期化
        if LLM_AVAILABLE and LLMConnector is not None:
            try:
                self.llm_connector = LLMConnector(
                    lab_dir=self.lab_dir,
                    model="llama-3.1-8b-instant",
                    api_key=api_key
                )
            except Exception as e:
                print(f"Warning: LLMConnector initialization failed: {e}")
                self.llm_connector = None
        else:
            self.llm_connector = None
        
        # 履歴保存ディレクトリ
        self.history_dir = self.lab_dir / "builder_history"
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        # 統計情報
        self.stats = {
            "total_builds": 0,
            "llm_builds": 0,
            "template_builds": 0,
            "successful_builds": 0,
            "failed_builds": 0
        }
    
    def build_basic_app_project(
        self,
        purpose: str,
        project_name: str,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        基本的なアプリプロジェクトを構築
        
        Args:
            purpose: プロジェクトの目的
            project_name: プロジェクト名
            use_llm: LLMを使用するかどうか（デフォルト: True）
        
        Returns:
            Dict: ビルド結果
                - success (bool): 成功したかどうか
                - status (str): ステータス
                - project_name (str): プロジェクト名
                - project_path (str): プロジェクトパス
                - mode (str): 使用したモード ("llm" or "template")
                - files (List[str]): 作成されたファイル
                - error (str, optional): エラーメッセージ
        """
        self.stats["total_builds"] += 1
        start_time = time.time()
        
        try:
            # プロジェクトフォルダ作成
            if self.workspace_manager:
                project = self.workspace_manager.create_project_folder(
                    project_name,
                    project_type="app"
                )
                project_dir = Path(project["project_dir"])
            else:
                # WorkspaceManagerがない場合は直接作成
                project_dir = self.lab_dir / "projects" / project_name
                project_dir.mkdir(parents=True, exist_ok=True)
            
            created_files = []
            
            # main.pyを生成
            mode = "unknown"
            if use_llm and self._is_llm_available():
                main_code = self._generate_main_with_llm(purpose)
                mode = "llm"
                self.stats["llm_builds"] += 1
            else:
                main_code = self._generate_main_template(purpose)
                mode = "template"
                self.stats["template_builds"] += 1
            
            main_file = project_dir / "main.py"
            main_file.write_text(main_code, encoding="utf-8")
            created_files.append(str(main_file))
            
            # README.mdを生成
            if use_llm and self._is_llm_available():
                readme_content = self._generate_readme_with_llm(purpose, project_name)
            else:
                readme_content = self._generate_readme_template(purpose, project_name)
            
            readme_file = project_dir / "README.md"
            readme_file.write_text(readme_content, encoding="utf-8")
            created_files.append(str(readme_file))
            
            # requirements.txt を生成
            requirements_content = self._generate_requirements(purpose)
            requirements_file = project_dir / "requirements.txt"
            requirements_file.write_text(requirements_content, encoding="utf-8")
            created_files.append(str(requirements_file))
            
            # notes.txt を生成
            notes_content = self._generate_notes(purpose, mode)
            notes_file = project_dir / "notes.txt"
            notes_file.write_text(notes_content, encoding="utf-8")
            created_files.append(str(notes_file))
            
            elapsed_time = time.time() - start_time
            
            result = {
                "success": True,
                "status": "completed",
                "project_name": project_name,
                "project_path": str(project_dir),
                "project_dir": str(project_dir),
                "mode": mode,
                "files": created_files,
                "elapsed_time": elapsed_time,
                "purpose": purpose
            }
            
            self.stats["successful_builds"] += 1
            
            # 履歴保存
            self._save_build_history(result)
            
            return result
            
        except Exception as e:
            self.stats["failed_builds"] += 1
            
            error_result = {
                "success": False,
                "status": "failed",
                "project_name": project_name,
                "error": str(e),
                "mode": "error"
            }
            
            self._save_build_history(error_result)
            
            return error_result
    
    def _generate_main_with_llm(self, purpose: str) -> str:
        """
        LLMを使用してmain.pyを生成
        
        Args:
            purpose: アプリケーションの目的
        
        Returns:
            str: 生成されたコード
        """
        try:
            result = self.llm_connector.generate_code(
                purpose=f"Create a complete Python application for: {purpose}",
                language="python",
                context={
                    "file_name": "main.py",
                    "requirements": [
                        "Clean and well-structured code",
                        "Include proper error handling",
                        "Add helpful comments in Japanese",
                        "Make it production-ready",
                        "Include a main() function",
                        "Add if __name__ == '__main__': guard",
                        "Write complete working code, not TODO placeholders"
                    ]
                },
                temperature=0.7,
                max_tokens=2000
            )
            
            if result["success"]:
                return result["code"]
            else:
                # LLM失敗時はテンプレートにフォールバック
                print(f"LLM generation failed: {result.get('error', 'Unknown error')}")
                return self._generate_main_template(purpose)
                
        except Exception as e:
            print(f"Error in LLM generation: {e}")
            return self._generate_main_template(purpose)
    
    def _generate_readme_with_llm(self, purpose: str, project_name: str) -> str:
        """
        LLMを使用してREADME.mdを生成
        
        Args:
            purpose: プロジェクトの目的
            project_name: プロジェクト名
        
        Returns:
            str: 生成されたREADME内容
        """
        try:
            result = self.llm_connector.generate_code(
                purpose=f"Create a professional README.md in Japanese for a project: {project_name}. Purpose: {purpose}",
                language="markdown",
                context={
                    "project_name": project_name,
                    "purpose": purpose,
                    "sections": [
                        "Title",
                        "Purpose (目的)",
                        "Features (機能)",
                        "Installation (インストール)",
                        "Usage (使い方)",
                        "Requirements (必要な環境)"
                    ]
                },
                temperature=0.5,
                max_tokens=1000
            )
            
            if result["success"]:
                return result["code"]
            else:
                return self._generate_readme_template(purpose, project_name)
                
        except Exception as e:
            print(f"Error in README generation: {e}")
            return self._generate_readme_template(purpose, project_name)
    
    def _generate_main_template(self, purpose: str) -> str:
        """
        テンプレートからmain.pyを生成（フォールバック）
        
        Args:
            purpose: アプリケーションの目的
        
        Returns:
            str: テンプレートコード
        """
        return f'''# -*- coding: utf-8 -*-
"""
{purpose}

NOTE: これは基本テンプレートです。
実際の機能を実装してください。
"""

def main():
    """メイン関数"""
    print("TODO: {purpose} の実装")
    # ここに実装を追加
    pass

if __name__ == "__main__":
    main()
'''
    
    def _generate_readme_template(self, purpose: str, project_name: str) -> str:
        """
        テンプレートからREADME.mdを生成（フォールバック）
        
        Args:
            purpose: プロジェクトの目的
            project_name: プロジェクト名
        
        Returns:
            str: テンプレートREADME
        """
        return f"""# {project_name}

## 目的

{purpose}

## 機能

- 基本的な機能（未実装）

## インストール

```bash
pip install -r requirements.txt
```

## 使い方

```bash
python main.py
```

## 必要な環境

- Python 3.7以上
"""
    
    def _generate_requirements(self, purpose: str) -> str:
        """
        requirements.txt を生成
        
        Args:
            purpose: プロジェクトの目的
        
        Returns:
            str: requirements.txt の内容
        """
        # 基本的な依存関係
        requirements = []
        
        purpose_lower = purpose.lower()
        
        # 目的に応じて依存関係を追加
        if "gui" in purpose_lower or "tkinter" in purpose_lower or "画面" in purpose_lower:
            # tkinterは標準ライブラリなので不要
            pass
        
        if "web" in purpose_lower or "flask" in purpose_lower or "django" in purpose_lower:
            requirements.append("flask>=2.0.0")
        
        if "データ" in purpose_lower or "data" in purpose_lower:
            requirements.append("pandas>=1.3.0")
            requirements.append("numpy>=1.21.0")
        
        if "グラフ" in purpose_lower or "可視化" in purpose_lower or "plot" in purpose_lower:
            requirements.append("matplotlib>=3.4.0")
        
        # 基本的な依存関係がない場合
        if not requirements:
            requirements.append("# No specific requirements")
            requirements.append("# Add your dependencies here")
        
        return "\n".join(requirements) + "\n"
    
    def _generate_notes(self, purpose: str, mode: str) -> str:
        """
        notes.txt を生成
        
        Args:
            purpose: プロジェクトの目的
            mode: 生成モード
        
        Returns:
            str: notes.txt の内容
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""プロジェクト生成メモ

生成日時: {timestamp}
生成モード: {mode}
目的: {purpose}

次のステップ:
1. main.py の実装を確認
2. 必要に応じて依存関係を追加
3. テストを実行
4. ドキュメントを更新

生成方式:
{'- LLM (Groq AI) を使用して生成' if mode == 'llm' else '- テンプレートベースで生成'}
"""
    
    def _is_llm_available(self) -> bool:
        """
        LLMが利用可能かチェック
        
        Returns:
            bool: 利用可能な場合True
        """
        return (
            self.llm_connector is not None 
            and hasattr(self.llm_connector, 'is_available')
            and self.llm_connector.is_available()
        )
    
    def _save_build_history(self, result: Dict[str, Any]) -> Path:
        """
        ビルド履歴を保存
        
        Args:
            result: ビルド結果
        
        Returns:
            Path: 保存先ファイルパス
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        history_file = self.history_dir / f"build_{timestamp}.json"
        
        history_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "result": result,
            "stats": self.stats.copy()
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        return history_file
    
    def diagnose_builder(self) -> Dict[str, Any]:
        """
        ビルダーの診断情報を取得
        
        Returns:
            Dict: 診断情報
                - llm_available (bool): LLMが利用可能か
                - llm_status (str): LLMの状態
                - stats (Dict): 統計情報
                - history_count (int): 履歴件数
                - latest_build (Dict, optional): 最新のビルド情報
        """
        # 最新のビルド履歴を取得
        history_files = sorted(
            self.history_dir.glob("build_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        latest_build = None
        if history_files:
            try:
                with open(history_files[0], 'r', encoding='utf-8') as f:
                    latest_build = json.load(f)
            except Exception:
                pass
        
        llm_available = self._is_llm_available()
        
        return {
            "llm_available": llm_available,
            "llm_status": "available" if llm_available else "unavailable",
            "stats": self.stats.copy(),
            "history_count": len(history_files),
            "latest_build": latest_build,
            "history_dir": str(self.history_dir)
        }
    
    def format_build_result(self, result: Dict[str, Any]) -> str:
        """
        ビルド結果を見やすい文字列に整形
        
        Args:
            result: ビルド結果
        
        Returns:
            str: 整形された結果
        """
        lines = ["=== AppProjectBuilder Result ==="]
        
        if result.get("success"):
            lines.append(f"Status: {result['status']}")
            lines.append(f"Project: {result['project_name']}")
            lines.append(f"Path: {result['project_path']}")
            lines.append(f"Mode: {result['mode']}")
            lines.append(f"Elapsed: {result.get('elapsed_time', 0):.2f}s")
            lines.append("")
            lines.append("Created Files:")
            for file_path in result.get("files", []):
                lines.append(f"  - {file_path}")
        else:
            lines.append(f"Status: {result['status']}")
            lines.append(f"Error: {result.get('error', 'Unknown error')}")
        
        return "\n".join(lines)
    
    def list_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        ビルド履歴を取得
        
        Args:
            limit: 取得する履歴の最大件数
        
        Returns:
            List[Dict]: ビルド履歴のリスト
        """
        history_files = sorted(
            self.history_dir.glob("build_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]
        
        histories = []
        for file_path in history_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    histories.append({
                        "file": file_path.name,
                        "data": data
                    })
            except Exception as e:
                print(f"Error loading history {file_path}: {e}")
        
        return histories
