"""
ProcessRecorder - ユーザーの作業プロセスを記録・再現するモジュール

このモジュールは以下の機能を提供：
1. ユーザーの作業手順を自動記録
2. 手順をテンプレート化して保存
3. 異なるテーマで同じプロセスを再現

使用例：
    recorder = ProcessRecorder(lab_dir=Path("/path/to/navikoLAB"))
    
    # 記録開始
    recorder.start_recording("Google_AI_Studio_App_Creation")
    
    # ステップを記録
    recorder.record_step("API Key取得", {"service": "Google AI Studio"})
    recorder.record_step("プロジェクト初期化", {"name": "calculator_app"})
    
    # テンプレート保存
    recorder.save_template("AI_Studio_App_Creation", description="AI Studioアプリ作成手順")
    
    # 再現
    result = recorder.replay_process("AI_Studio_App_Creation", new_theme="天気予報アプリ")
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class ProcessRecorder:
    """ユーザーの作業プロセスを記録・再現"""
    
    def __init__(self, lab_dir: Path):
        """
        初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        self.lab_dir = Path(lab_dir)
        self.process_templates_dir = self.lab_dir / "process_templates"
        self.process_templates_dir.mkdir(exist_ok=True)
        
        # SQLiteデータベース初期化
        self.db_path = self.lab_dir / "process_recorder.db"
        self._init_database()
        
        # 現在の記録セッション
        self.current_recording = None
        self.current_steps = []
        
    def _init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # プロセステンプレートテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT UNIQUE NOT NULL,
                description TEXT,
                category TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                steps_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                total_executions INTEGER DEFAULT 0
            )
        """)
        
        # プロセス実行履歴テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT NOT NULL,
                theme TEXT NOT NULL,
                executed_at TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                duration_seconds REAL,
                result_summary TEXT,
                FOREIGN KEY (template_name) REFERENCES process_templates(template_name)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def start_recording(self, process_name: str, description: str = "") -> Dict[str, Any]:
        """
        プロセスの記録開始
        
        Args:
            process_name: プロセス名
            description: プロセスの説明
            
        Returns:
            記録セッション情報
        """
        if self.current_recording:
            return {
                "success": False,
                "error": f"既に記録中です: {self.current_recording['name']}"
            }
        
        self.current_recording = {
            "name": process_name,
            "description": description,
            "started_at": datetime.now().isoformat(),
            "category": self._infer_category(process_name)
        }
        self.current_steps = []
        
        return {
            "success": True,
            "message": f"プロセス記録開始: {process_name}",
            "session": self.current_recording
        }
    
    def record_step(
        self, 
        action: str, 
        context: Dict[str, Any],
        step_type: str = "action",
        expected_outcome: str = ""
    ) -> Dict[str, Any]:
        """
        作業ステップを記録
        
        Args:
            action: 実行するアクション（例：「APIキー取得」）
            context: アクションのコンテキスト情報
            step_type: ステップタイプ（action/input/output/validation）
            expected_outcome: 期待される結果
            
        Returns:
            記録結果
        """
        if not self.current_recording:
            return {
                "success": False,
                "error": "記録セッションが開始されていません"
            }
        
        step = {
            "step_number": len(self.current_steps) + 1,
            "action": action,
            "context": context,
            "step_type": step_type,
            "expected_outcome": expected_outcome,
            "recorded_at": datetime.now().isoformat(),
            "variables": self._extract_variables(context)
        }
        
        self.current_steps.append(step)
        
        return {
            "success": True,
            "message": f"ステップ {step['step_number']} を記録: {action}",
            "step": step
        }
    
    def _extract_variables(self, context: Dict[str, Any]) -> List[str]:
        """コンテキストから変数を抽出"""
        variables = []
        for key, value in context.items():
            if isinstance(value, str) and value:
                variables.append(key)
        return variables
    
    def _infer_category(self, process_name: str) -> str:
        """プロセス名からカテゴリーを推測"""
        name_lower = process_name.lower()
        
        if any(kw in name_lower for kw in ["api", "studio", "google", "ai"]):
            return "AI_Development"
        elif any(kw in name_lower for kw in ["app", "application", "build"]):
            return "App_Development"
        elif any(kw in name_lower for kw in ["data", "analysis", "search"]):
            return "Data_Analysis"
        elif any(kw in name_lower for kw in ["test", "debug", "fix"]):
            return "Testing_Debugging"
        else:
            return "General"
    
    def save_template(
        self, 
        template_name: str, 
        description: str = "",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """
        現在の記録セッションをテンプレートとして保存
        
        Args:
            template_name: テンプレート名
            description: テンプレートの説明
            tags: タグリスト
            
        Returns:
            保存結果
        """
        if not self.current_recording:
            return {
                "success": False,
                "error": "記録セッションが開始されていません"
            }
        
        if not self.current_steps:
            return {
                "success": False,
                "error": "記録されたステップがありません"
            }
        
        template = {
            "template_name": template_name,
            "description": description or self.current_recording["description"],
            "category": self.current_recording["category"],
            "steps": self.current_steps,
            "total_steps": len(self.current_steps),
            "created_at": datetime.now().isoformat(),
            "tags": tags or [],
            "metadata": {
                "original_process": self.current_recording["name"],
                "recording_started": self.current_recording["started_at"]
            }
        }
        
        # JSONファイルとして保存
        template_file = self.process_templates_dir / f"{template_name}.json"
        template_file.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # データベースに登録
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO process_templates 
            (template_name, description, category, created_at, updated_at, steps_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            template_name,
            template["description"],
            template["category"],
            template["created_at"],
            template["created_at"],
            len(self.current_steps)
        ))
        
        conn.commit()
        conn.close()
        
        # 記録セッションをクリア
        self.current_recording = None
        self.current_steps = []
        
        return {
            "success": True,
            "message": f"テンプレート '{template_name}' を保存しました",
            "template_file": str(template_file),
            "steps_count": len(template["steps"])
        }
    
    def load_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        テンプレートを読み込み
        
        Args:
            template_name: テンプレート名
            
        Returns:
            テンプレート情報、存在しない場合はNone
        """
        template_file = self.process_templates_dir / f"{template_name}.json"
        
        if not template_file.exists():
            return None
        
        try:
            return json.loads(template_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"テンプレート読み込みエラー: {e}")
            return None
    
    def list_templates(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        保存されたテンプレート一覧を取得
        
        Args:
            category: カテゴリーでフィルタ（オプション）
            
        Returns:
            テンプレートリスト
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT template_name, description, category, steps_count, 
                       success_count, total_executions, created_at
                FROM process_templates
                WHERE category = ?
                ORDER BY created_at DESC
            """, (category,))
        else:
            cursor.execute("""
                SELECT template_name, description, category, steps_count, 
                       success_count, total_executions, created_at
                FROM process_templates
                ORDER BY created_at DESC
            """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                "template_name": row[0],
                "description": row[1],
                "category": row[2],
                "steps_count": row[3],
                "success_count": row[4],
                "total_executions": row[5],
                "created_at": row[6],
                "success_rate": row[4] / row[5] if row[5] > 0 else 0.0
            })
        
        conn.close()
        return templates
    
    def replay_process(
        self, 
        template_name: str, 
        new_theme: str,
        variable_overrides: Dict[str, Any] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        テンプレートを使って別のテーマでプロセスを再現
        
        Args:
            template_name: 使用するテンプレート名
            new_theme: 新しいテーマ（例：「天気予報アプリ」）
            variable_overrides: 変数の上書き値
            dry_run: ドライラン（実行せず計画のみ表示）
            
        Returns:
            実行結果
        """
        template = self.load_template(template_name)
        
        if not template:
            return {
                "success": False,
                "error": f"テンプレート '{template_name}' が見つかりません"
            }
        
        variable_overrides = variable_overrides or {}
        start_time = datetime.now()
        
        # ステップを新しいテーマで置き換え
        adapted_steps = []
        for step in template["steps"]:
            adapted_step = self._adapt_step_to_theme(step, new_theme, variable_overrides)
            adapted_steps.append(adapted_step)
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "template": template_name,
                "theme": new_theme,
                "steps": adapted_steps,
                "message": "ドライラン完了。実際には実行されていません。"
            }
        
        # 実際のプロセス実行（シミュレーション）
        execution_result = {
            "template": template_name,
            "theme": new_theme,
            "started_at": start_time.isoformat(),
            "steps_executed": [],
            "success": True
        }
        
        for step in adapted_steps:
            step_result = {
                "step_number": step["step_number"],
                "action": step["action"],
                "status": "success",
                "message": f"✅ {step['action']} 完了"
            }
            execution_result["steps_executed"].append(step_result)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        execution_result["completed_at"] = end_time.isoformat()
        execution_result["duration_seconds"] = duration
        
        # データベースに実行履歴を保存
        self._save_execution_history(template_name, new_theme, True, duration, execution_result)
        
        return execution_result
    
    def _adapt_step_to_theme(
        self, 
        step: Dict[str, Any], 
        new_theme: str,
        variable_overrides: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ステップを新しいテーマに適応"""
        adapted_step = step.copy()
        adapted_context = step["context"].copy()
        
        # コンテキストの変数を新しいテーマで置き換え
        for var in step["variables"]:
            if var in variable_overrides:
                adapted_context[var] = variable_overrides[var]
            elif var in adapted_context:
                # 一般的なキーワードを新しいテーマで置き換え
                original_value = adapted_context[var]
                if isinstance(original_value, str):
                    adapted_context[var] = self._replace_theme_in_text(original_value, new_theme)
        
        adapted_step["context"] = adapted_context
        adapted_step["adapted_theme"] = new_theme
        
        return adapted_step
    
    def _replace_theme_in_text(self, text: str, new_theme: str) -> str:
        """テキスト内のテーマ関連キーワードを置き換え"""
        # シンプルな実装：元のテーマを新しいテーマに置換
        # 実際の実装ではLLMを使ってコンテキストを理解して置換
        return text  # TODO: LLM統合で改善
    
    def _save_execution_history(
        self, 
        template_name: str, 
        theme: str, 
        success: bool, 
        duration: float,
        result: Dict[str, Any]
    ):
        """実行履歴を保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 実行履歴を追加
        cursor.execute("""
            INSERT INTO process_executions 
            (template_name, theme, executed_at, success, duration_seconds, result_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            template_name,
            theme,
            datetime.now().isoformat(),
            success,
            duration,
            json.dumps(result, ensure_ascii=False)
        ))
        
        # テンプレート統計を更新
        cursor.execute("""
            UPDATE process_templates
            SET total_executions = total_executions + 1,
                success_count = success_count + ?,
                updated_at = ?
            WHERE template_name = ?
        """, (1 if success else 0, datetime.now().isoformat(), template_name))
        
        conn.commit()
        conn.close()
    
    def get_execution_history(
        self, 
        template_name: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        実行履歴を取得
        
        Args:
            template_name: テンプレート名でフィルタ（オプション）
            limit: 取得件数
            
        Returns:
            実行履歴リスト
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if template_name:
            cursor.execute("""
                SELECT template_name, theme, executed_at, success, duration_seconds
                FROM process_executions
                WHERE template_name = ?
                ORDER BY executed_at DESC
                LIMIT ?
            """, (template_name, limit))
        else:
            cursor.execute("""
                SELECT template_name, theme, executed_at, success, duration_seconds
                FROM process_executions
                ORDER BY executed_at DESC
                LIMIT ?
            """, (limit,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "template_name": row[0],
                "theme": row[1],
                "executed_at": row[2],
                "success": bool(row[3]),
                "duration_seconds": row[4]
            })
        
        conn.close()
        return history
    
    def format_template_info(self, template_name: str) -> str:
        """テンプレート情報を整形して表示"""
        template = self.load_template(template_name)
        if not template:
            return f"❌ テンプレート '{template_name}' が見つかりません"
        
        output = []
        output.append(f"📋 プロセステンプレート: {template['template_name']}")
        output.append("=" * 60)
        output.append(f"説明: {template['description']}")
        output.append(f"カテゴリー: {template['category']}")
        output.append(f"作成日時: {template['created_at']}")
        output.append(f"ステップ数: {template['total_steps']}")
        output.append("")
        output.append("📝 実行手順:")
        output.append("-" * 60)
        
        for step in template['steps']:
            output.append(f"{step['step_number']}. {step['action']}")
            if step.get('expected_outcome'):
                output.append(f"   期待結果: {step['expected_outcome']}")
        
        output.append("=" * 60)
        
        return "\n".join(output)
