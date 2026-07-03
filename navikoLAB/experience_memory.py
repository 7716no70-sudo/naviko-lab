"""
ExperienceMemory - エラー解決経験を蓄積・学習するモジュール

このモジュールは以下の機能を提供：
1. 解決したエラーをデータベースに記録
2. 類似エラーを検索
3. 成功率の高い解決策を提案
4. 学習履歴の可視化

使用例：
    memory = ExperienceMemory(lab_dir=Path("/path/to/navikoLAB"))
    
    # エラー解決を記録
    memory.record_solution(
        error_type="401_unauthorized",
        error_message="401 Client Error: Unauthorized",
        solution="環境変数のAPIキーを更新",
        success=True,
        context={"service": "Groq API"}
    )
    
    # 類似エラーを検索
    similar = memory.find_similar_errors("401 Unauthorized")
    
    # 最適な解決策を取得
    best = memory.get_best_solution("401_unauthorized")
"""

import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from difflib import SequenceMatcher


class ExperienceMemory:
    """エラー解決経験を蓄積・学習"""
    
    def __init__(self, lab_dir: Path):
        """
        初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        self.lab_dir = Path(lab_dir)
        self.experience_dir = self.lab_dir / "experience_memory"
        self.experience_dir.mkdir(exist_ok=True)
        
        # SQLiteデータベース初期化
        self.db_path = self.lab_dir / "experience_memory.db"
        self._init_database()
    
    def _init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # エラータイプテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT UNIQUE NOT NULL,
                category TEXT,
                severity TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                occurrence_count INTEGER DEFAULT 1
            )
        """)
        
        # 解決策テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                solution_text TEXT NOT NULL,
                solution_hash TEXT UNIQUE NOT NULL,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                total_uses INTEGER DEFAULT 0,
                avg_resolution_time REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (error_type) REFERENCES error_types(error_type)
            )
        """)
        
        # 解決履歴テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resolution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                solution_id INTEGER NOT NULL,
                success BOOLEAN NOT NULL,
                resolution_time REAL,
                context TEXT,
                resolved_at TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (solution_id) REFERENCES solutions(id),
                FOREIGN KEY (error_type) REFERENCES error_types(error_type)
            )
        """)
        
        # エラーパターンテーブル（類似性検索用）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                pattern TEXT NOT NULL,
                pattern_type TEXT,
                keywords TEXT,
                match_count INTEGER DEFAULT 0,
                FOREIGN KEY (error_type) REFERENCES error_types(error_type)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_solution(
        self,
        error_type: str,
        error_message: str,
        solution: str,
        success: bool,
        context: Dict[str, Any] = None,
        resolution_time: float = None,
        category: str = "General",
        severity: str = "Medium",
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        エラー解決を記録
        
        Args:
            error_type: エラータイプ（例：「401_unauthorized」）
            error_message: エラーメッセージ全文
            solution: 適用した解決策
            success: 解決に成功したか
            context: コンテキスト情報
            resolution_time: 解決にかかった時間（秒）
            category: エラーカテゴリー
            severity: 深刻度（Low/Medium/High）
            notes: 追加メモ
            
        Returns:
            記録結果
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        context_json = json.dumps(context or {}, ensure_ascii=False)
        solution_hash = self._hash_solution(solution)
        
        # エラータイプを記録/更新
        cursor.execute("""
            INSERT INTO error_types (error_type, category, severity, first_seen, last_seen, occurrence_count)
            VALUES (?, ?, ?, ?, ?, 1)
            ON CONFLICT(error_type) DO UPDATE SET
                last_seen = ?,
                occurrence_count = occurrence_count + 1
        """, (error_type, category, severity, now, now, now))
        
        # 解決策を記録/更新
        cursor.execute("""
            INSERT INTO solutions (error_type, solution_text, solution_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(solution_hash) DO UPDATE SET
                updated_at = ?
        """, (error_type, solution, solution_hash, now, now, now))
        
        # 解決策IDを取得
        cursor.execute("SELECT id FROM solutions WHERE solution_hash = ?", (solution_hash,))
        solution_id = cursor.fetchone()[0]
        
        # 成功/失敗カウントを更新
        if success:
            cursor.execute("""
                UPDATE solutions 
                SET success_count = success_count + 1,
                    total_uses = total_uses + 1
                WHERE id = ?
            """, (solution_id,))
        else:
            cursor.execute("""
                UPDATE solutions 
                SET failure_count = failure_count + 1,
                    total_uses = total_uses + 1
                WHERE id = ?
            """, (solution_id,))
        
        # 解決時間の平均を更新
        if resolution_time is not None:
            cursor.execute("""
                UPDATE solutions
                SET avg_resolution_time = (
                    (avg_resolution_time * (total_uses - 1) + ?) / total_uses
                )
                WHERE id = ?
            """, (resolution_time, solution_id))
        
        # 解決履歴を記録
        cursor.execute("""
            INSERT INTO resolution_history 
            (error_type, error_message, solution_id, success, resolution_time, context, resolved_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (error_type, error_message, solution_id, success, resolution_time, context_json, now, notes))
        
        # エラーパターンを抽出して記録
        self._extract_and_save_patterns(cursor, error_type, error_message)
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"解決策を記録しました: {error_type}",
            "solution_id": solution_id,
            "solution_hash": solution_hash
        }
    
    def _hash_solution(self, solution: str) -> str:
        """解決策のハッシュ値を生成"""
        return hashlib.sha256(solution.encode('utf-8')).hexdigest()[:16]
    
    def _extract_and_save_patterns(self, cursor, error_type: str, error_message: str):
        """エラーメッセージからパターンを抽出"""
        # キーワード抽出（簡易実装）
        keywords = []
        
        # ステータスコード
        if "401" in error_message:
            keywords.append("401")
        if "403" in error_message:
            keywords.append("403")
        if "404" in error_message:
            keywords.append("404")
        if "500" in error_message:
            keywords.append("500")
        
        # サービス名
        if "groq" in error_message.lower():
            keywords.append("Groq")
        if "api" in error_message.lower():
            keywords.append("API")
        if "unauthorized" in error_message.lower():
            keywords.append("Unauthorized")
        if "forbidden" in error_message.lower():
            keywords.append("Forbidden")
        
        keywords_str = ",".join(keywords)
        
        # パターンを保存
        cursor.execute("""
            INSERT INTO error_patterns (error_type, pattern, pattern_type, keywords, match_count)
            VALUES (?, ?, 'keyword', ?, 1)
            ON CONFLICT DO NOTHING
        """, (error_type, error_message[:200], keywords_str))
    
    def find_similar_errors(
        self, 
        error_message: str,
        threshold: float = 0.6,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        類似エラーを検索
        
        Args:
            error_message: 検索するエラーメッセージ
            threshold: 類似度の閾値（0.0〜1.0）
            limit: 取得件数
            
        Returns:
            類似エラーリスト
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # キーワードマッチング
        keywords = self._extract_keywords(error_message)
        
        # パターンテーブルから類似エラーを検索
        cursor.execute("""
            SELECT DISTINCT et.error_type, et.category, et.severity, 
                   et.occurrence_count, ep.pattern, ep.keywords
            FROM error_types et
            JOIN error_patterns ep ON et.error_type = ep.error_type
            ORDER BY et.occurrence_count DESC
        """)
        
        similar_errors = []
        for row in cursor.fetchall():
            error_type, category, severity, occurrence_count, pattern, pattern_keywords = row
            
            # 類似度計算
            similarity = self._calculate_similarity(error_message, pattern, keywords, pattern_keywords)
            
            if similarity >= threshold:
                # このエラータイプの最適解決策を取得
                best_solution = self._get_best_solution_for_type(cursor, error_type)
                
                similar_errors.append({
                    "error_type": error_type,
                    "category": category,
                    "severity": severity,
                    "occurrence_count": occurrence_count,
                    "similarity": similarity,
                    "best_solution": best_solution
                })
        
        conn.close()
        
        # 類似度でソート
        similar_errors.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similar_errors[:limit]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """テキストからキーワードを抽出"""
        keywords = []
        text_lower = text.lower()
        
        # ステータスコード
        for code in ["400", "401", "403", "404", "500", "502", "503"]:
            if code in text:
                keywords.append(code)
        
        # サービス・技術
        for keyword in ["api", "groq", "ollama", "python", "sql", "unauthorized", "forbidden", "not found"]:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _calculate_similarity(
        self, 
        text1: str, 
        text2: str, 
        keywords1: List[str],
        keywords2_str: str
    ) -> float:
        """2つのエラーメッセージの類似度を計算"""
        # テキストの類似度（SequenceMatcher）
        text_similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # キーワードの一致度
        keywords2 = keywords2_str.split(",") if keywords2_str else []
        keyword_matches = len(set(keywords1) & set(keywords2))
        keyword_similarity = keyword_matches / max(len(keywords1), len(keywords2), 1)
        
        # 総合類似度（テキスト40%、キーワード60%）
        return text_similarity * 0.4 + keyword_similarity * 0.6
    
    def _get_best_solution_for_type(self, cursor, error_type: str) -> Optional[Dict[str, Any]]:
        """特定のエラータイプの最適解決策を取得"""
        cursor.execute("""
            SELECT solution_text, success_count, failure_count, total_uses, avg_resolution_time
            FROM solutions
            WHERE error_type = ?
            ORDER BY (success_count * 1.0 / NULLIF(total_uses, 0)) DESC, success_count DESC
            LIMIT 1
        """, (error_type,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        solution_text, success_count, failure_count, total_uses, avg_resolution_time = row
        
        return {
            "solution": solution_text,
            "success_count": success_count,
            "failure_count": failure_count,
            "total_uses": total_uses,
            "success_rate": success_count / total_uses if total_uses > 0 else 0.0,
            "avg_resolution_time": avg_resolution_time
        }
    
    def get_best_solution(self, error_type: str) -> Optional[Dict[str, Any]]:
        """
        エラータイプの最適解決策を取得
        
        Args:
            error_type: エラータイプ
            
        Returns:
            最適解決策、存在しない場合はNone
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        solution = self._get_best_solution_for_type(cursor, error_type)
        
        conn.close()
        return solution
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        学習統計を取得
        
        Returns:
            統計情報
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 総エラータイプ数
        cursor.execute("SELECT COUNT(*) FROM error_types")
        total_error_types = cursor.fetchone()[0]
        
        # 総解決策数
        cursor.execute("SELECT COUNT(*) FROM solutions")
        total_solutions = cursor.fetchone()[0]
        
        # 総解決履歴数
        cursor.execute("SELECT COUNT(*) FROM resolution_history")
        total_resolutions = cursor.fetchone()[0]
        
        # 成功率
        cursor.execute("SELECT COUNT(*) FROM resolution_history WHERE success = 1")
        successful_resolutions = cursor.fetchone()[0]
        success_rate = successful_resolutions / total_resolutions if total_resolutions > 0 else 0.0
        
        # 最も頻繁なエラー
        cursor.execute("""
            SELECT error_type, occurrence_count, category
            FROM error_types
            ORDER BY occurrence_count DESC
            LIMIT 5
        """)
        top_errors = [
            {"error_type": row[0], "count": row[1], "category": row[2]}
            for row in cursor.fetchall()
        ]
        
        # 最も効果的な解決策
        cursor.execute("""
            SELECT s.solution_text, s.success_count, s.total_uses, s.error_type
            FROM solutions s
            WHERE s.total_uses >= 3
            ORDER BY (s.success_count * 1.0 / s.total_uses) DESC, s.success_count DESC
            LIMIT 5
        """)
        top_solutions = [
            {
                "solution": row[0][:100] + "..." if len(row[0]) > 100 else row[0],
                "success_count": row[1],
                "total_uses": row[2],
                "success_rate": row[1] / row[2] if row[2] > 0 else 0.0,
                "error_type": row[3]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            "total_error_types": total_error_types,
            "total_solutions": total_solutions,
            "total_resolutions": total_resolutions,
            "success_rate": success_rate,
            "top_errors": top_errors,
            "top_solutions": top_solutions
        }
    
    def format_statistics(self) -> str:
        """統計情報を整形して表示"""
        stats = self.get_statistics()
        
        output = []
        output.append("📊 Experience Memory 統計")
        output.append("=" * 60)
        output.append(f"記録されたエラータイプ: {stats['total_error_types']:,}")
        output.append(f"記録された解決策: {stats['total_solutions']:,}")
        output.append(f"総解決回数: {stats['total_resolutions']:,}")
        output.append(f"成功率: {stats['success_rate']:.1%}")
        output.append("")
        
        if stats['top_errors']:
            output.append("🔥 頻発エラー TOP 5:")
            output.append("-" * 60)
            for i, error in enumerate(stats['top_errors'], 1):
                output.append(f"  {i}. {error['error_type']} ({error['category']})")
                output.append(f"     発生回数: {error['count']:,}回")
        
        if stats['top_solutions']:
            output.append("")
            output.append("💡 最も効果的な解決策 TOP 5:")
            output.append("-" * 60)
            for i, solution in enumerate(stats['top_solutions'], 1):
                output.append(f"  {i}. {solution['solution']}")
                output.append(f"     成功率: {solution['success_rate']:.1%} ({solution['success_count']}/{solution['total_uses']})")
                output.append(f"     適用先: {solution['error_type']}")
        
        output.append("=" * 60)
        
        return "\n".join(output)
