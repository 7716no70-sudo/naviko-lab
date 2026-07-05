#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SelfEvolutionEngine - Navikoの自己進化エンジン

このモジュールはNavikoのSystem 3 Phase 3の一部として、以下を提供します：
- 学習データに基づく自動コード改善提案
- 新しいエラーパターンの自動登録機能
- 予防策の効果測定と最適化
- MetaCognitionEngineとの高度な連携

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import json
import sqlite3
import ast
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
import hashlib
import difflib


class SelfEvolutionEngine:
    """
    自己進化エンジン
    
    学習データを分析し、Navikoシステム自身を自動的に改善します。
    """
    
    def __init__(self, lab_dir: str = None):
        """
        SelfEvolutionEngineの初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        # 基本パス設定
        if lab_dir is None:
            lab_dir = os.path.join(os.path.expanduser("~"), "navikoLAB")
            if not os.path.exists(lab_dir):
                lab_dir = "/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB"
        
        self.lab_dir = Path(lab_dir)
        
        # データベースパス
        self.patterns_db_path = self.lab_dir / "problem_patterns.db"
        self.evolution_log_path = self.lab_dir / "evolution_log.json"
        
        # 進化履歴
        self.evolution_history: List[Dict] = self._load_evolution_history()
        
        # 改善提案の閾値
        self.thresholds = {
            'min_pattern_frequency': 3,  # 改善提案を出す最小パターン頻度
            'min_success_improvement': 0.1,  # 最小成功率改善（10%）
            'confidence_level': 0.7  # 提案の信頼度レベル
        }
    
    def _load_evolution_history(self) -> List[Dict]:
        """
        進化履歴のロード
        
        Returns:
            進化履歴リスト
        """
        if self.evolution_log_path.exists():
            try:
                with open(self.evolution_log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return []
    
    def _save_evolution_history(self):
        """
        進化履歴の保存
        """
        try:
            with open(self.evolution_log_path, 'w', encoding='utf-8') as f:
                json.dump(self.evolution_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"進化履歴保存エラー: {e}")
    
    def propose_code_improvements(
        self,
        module_path: str = None
    ) -> List[Dict[str, Any]]:
        """
        学習データに基づく自動コード改善提案
        
        Args:
            module_path: 分析対象のモジュールパス（Noneで全モジュール）
        
        Returns:
            改善提案リスト
            [
                {
                    'target': 'module_name',
                    'improvement_type': 'optimization' | 'bug_fix' | 'enhancement',
                    'description': '...',
                    'code_changes': {...},
                    'expected_impact': {...},
                    'confidence': 0.0-1.0
                },
                ...
            ]
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 頻発する問題パターンを取得
        cursor.execute("""
            SELECT 
                problem_type,
                COUNT(*) as frequency,
                AVG(success_rate) as avg_success,
                GROUP_CONCAT(context_json) as contexts
            FROM patterns
            GROUP BY problem_type
            HAVING frequency >= ?
            ORDER BY frequency DESC
        """, (self.thresholds['min_pattern_frequency'],))
        
        frequent_patterns = cursor.fetchall()
        conn.close()
        
        proposals = []
        
        for problem_type, frequency, avg_success, contexts_str in frequent_patterns:
            # コンテキストを解析
            contexts = self._parse_contexts(contexts_str)
            
            # 改善提案を生成
            proposal = self._generate_improvement_proposal(
                problem_type, frequency, avg_success, contexts
            )
            
            if proposal:
                proposals.append(proposal)
        
        # 信頼度でソート
        proposals.sort(key=lambda x: x['confidence'], reverse=True)
        
        # 進化履歴に記録
        self._record_proposals(proposals)
        
        return proposals
    
    def _parse_contexts(self, contexts_str: str) -> List[Dict]:
        """
        コンテキスト文字列をパース
        
        Args:
            contexts_str: カンマ区切りのJSON文字列
        
        Returns:
            コンテキストリスト
        """
        if not contexts_str:
            return []
        
        contexts = []
        for ctx_str in contexts_str.split(','):
            try:
                if ctx_str.strip():
                    contexts.append(json.loads(ctx_str))
            except json.JSONDecodeError:
                continue
        
        return contexts
    
    def _generate_improvement_proposal(
        self,
        problem_type: str,
        frequency: int,
        avg_success: float,
        contexts: List[Dict]
    ) -> Optional[Dict]:
        """
        改善提案を生成
        
        Args:
            problem_type: 問題タイプ
            frequency: 発生頻度
            avg_success: 平均成功率
            contexts: コンテキストリスト
        
        Returns:
            改善提案（生成できない場合はNone）
        """
        # 問題タイプに基づく改善タイプの決定
        improvement_type = self._determine_improvement_type(
            problem_type, avg_success
        )
        
        if not improvement_type:
            return None
        
        # 具体的な改善内容の生成
        description, code_changes = self._generate_specific_improvements(
            problem_type, improvement_type, contexts
        )
        
        # 期待される効果の推定
        expected_impact = self._estimate_impact(
            frequency, avg_success, improvement_type
        )
        
        # 信頼度の計算
        confidence = self._calculate_proposal_confidence(
            frequency, len(contexts), avg_success
        )
        
        if confidence < self.thresholds['confidence_level']:
            return None
        
        return {
            'target': problem_type,
            'improvement_type': improvement_type,
            'description': description,
            'code_changes': code_changes,
            'expected_impact': expected_impact,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
    
    def _determine_improvement_type(
        self,
        problem_type: str,
        avg_success: float
    ) -> Optional[str]:
        """
        改善タイプを決定
        
        Args:
            problem_type: 問題タイプ
            avg_success: 平均成功率
        
        Returns:
            改善タイプ
        """
        # 成功率が低い場合はバグ修正
        if avg_success < 0.5:
            return 'bug_fix'
        
        # APIエラー関連は最適化
        if 'api' in problem_type.lower() or 'timeout' in problem_type.lower():
            return 'optimization'
        
        # Git関連は機能強化
        if 'git' in problem_type.lower():
            return 'enhancement'
        
        # その他は最適化
        return 'optimization'
    
    def _generate_specific_improvements(
        self,
        problem_type: str,
        improvement_type: str,
        contexts: List[Dict]
    ) -> Tuple[str, Dict]:
        """
        具体的な改善内容を生成
        
        Args:
            problem_type: 問題タイプ
            improvement_type: 改善タイプ
            contexts: コンテキストリスト
        
        Returns:
            (説明, コード変更内容)
        """
        description = ""
        code_changes = {}
        
        if improvement_type == 'bug_fix':
            description = (
                f"{problem_type}の問題が頻発しています。"
                "エラーハンドリングの追加または修正を推奨します。"
            )
            code_changes = {
                'type': 'add_error_handling',
                'location': self._identify_error_location(problem_type, contexts),
                'suggested_code': self._generate_error_handling_code(problem_type)
            }
        
        elif improvement_type == 'optimization':
            description = (
                f"{problem_type}のパフォーマンス改善が可能です。"
                "リトライロジックまたはタイムアウト設定の最適化を推奨します。"
            )
            code_changes = {
                'type': 'optimize_retry_logic',
                'location': self._identify_optimization_location(problem_type, contexts),
                'suggested_code': self._generate_optimization_code(problem_type)
            }
        
        elif improvement_type == 'enhancement':
            description = (
                f"{problem_type}の機能強化が推奨されます。"
                "自動リカバリー機能の追加を検討してください。"
            )
            code_changes = {
                'type': 'add_auto_recovery',
                'location': self._identify_enhancement_location(problem_type, contexts),
                'suggested_code': self._generate_enhancement_code(problem_type)
            }
        
        return description, code_changes
    
    def _identify_error_location(
        self,
        problem_type: str,
        contexts: List[Dict]
    ) -> str:
        """
        エラー発生場所を特定
        
        Args:
            problem_type: 問題タイプ
            contexts: コンテキストリスト
        
        Returns:
            場所の説明
        """
        # コンテキストから頻出する場所を特定
        locations = []
        for ctx in contexts:
            if 'file' in ctx:
                locations.append(ctx['file'])
            elif 'module' in ctx:
                locations.append(ctx['module'])
        
        if locations:
            most_common = Counter(locations).most_common(1)[0][0]
            return f"ファイル: {most_common}"
        
        return "場所不明（コンテキスト分析が必要）"
    
    def _identify_optimization_location(
        self,
        problem_type: str,
        contexts: List[Dict]
    ) -> str:
        """
        最適化対象場所を特定
        
        Args:
            problem_type: 問題タイプ
            contexts: コンテキストリスト
        
        Returns:
            場所の説明
        """
        return self._identify_error_location(problem_type, contexts)
    
    def _identify_enhancement_location(
        self,
        problem_type: str,
        contexts: List[Dict]
    ) -> str:
        """
        機能強化対象場所を特定
        
        Args:
            problem_type: 問題タイプ
            contexts: コンテキストリスト
        
        Returns:
            場所の説明
        """
        return self._identify_error_location(problem_type, contexts)

    def _generate_error_handling_code(self, problem_type: str) -> str:
        """
        エラーハンドリングコードを生成
        
        Args:
            problem_type: 問題タイプ
        
        Returns:
            生成されたコード
        """
        if 'api' in problem_type.lower():
            return '''try:
    # API呼び出し
    response = api_call()
except requests.exceptions.Timeout:
    print("API呼び出しがタイムアウトしました")
    response = fallback_response()
except requests.exceptions.RequestException as e:
    print(f"APIエラー: {e}")
    log_error(e)
    raise'''
        
        return '''try:
    result = operation()
except Exception as e:
    print(f"エラー: {e}")
    handle_error(e)
    raise'''
    
    def _generate_optimization_code(self, problem_type: str) -> str:
        """
        最適化コードを生成
        
        Args:
            problem_type: 問題タイプ
        
        Returns:
            生成されたコード
        """
        if 'timeout' in problem_type.lower():
            return '''import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        return wrapper
    return decorator'''
        
        return '# パフォーマンス最適化コード'
    
    def _generate_enhancement_code(self, problem_type: str) -> str:
        """
        機能強化コードを生成
        
        Args:
            problem_type: 問題タイプ
        
        Returns:
            生成されたコード
        """
        if 'git' in problem_type.lower():
            return '''def auto_recover_git_state():
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if 'nothing to commit' in result.stdout:
            return True
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto-recovery'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False'''
        
        return '# 自動リカバリー機能コード'
    
    def _estimate_impact(
        self,
        frequency: int,
        avg_success: float,
        improvement_type: str
    ) -> Dict[str, Any]:
        """
        改善による期待効果を推定
        
        Args:
            frequency: 問題発生頻度
            avg_success: 平均成功率
            improvement_type: 改善タイプ
        
        Returns:
            期待効果
        """
        if improvement_type == 'bug_fix':
            success_improvement = 0.3
        elif improvement_type == 'optimization':
            success_improvement = 0.2
        else:
            success_improvement = 0.15
        
        new_success_rate = min(1.0, avg_success + success_improvement)
        affected_cases = frequency
        improved_cases = int(affected_cases * success_improvement)
        
        return {
            'success_rate_improvement': success_improvement,
            'new_predicted_success_rate': new_success_rate,
            'affected_cases': affected_cases,
            'improved_cases': improved_cases,
            'severity': 'high' if frequency > 10 else 'medium' if frequency > 5 else 'low'
        }
    
    def _calculate_proposal_confidence(
        self,
        frequency: int,
        context_count: int,
        avg_success: float
    ) -> float:
        """
        提案の信頼度を計算
        """
        data_confidence = min(1.0, frequency / 10)
        context_confidence = min(1.0, context_count / 5)
        success_confidence = 1.0 - avg_success
        
        return (
            data_confidence * 0.4 +
            context_confidence * 0.3 +
            success_confidence * 0.3
        )
    
    def _record_proposals(self, proposals: List[Dict]):
        """改善提案を進化履歴に記録"""
        for proposal in proposals:
            self.evolution_history.append({
                'type': 'proposal',
                'timestamp': datetime.now().isoformat(),
                'data': proposal
            })
        self._save_evolution_history()
    
    def register_new_pattern_automatically(
        self,
        error_info: Dict[str, Any]
    ) -> bool:
        """
        新しいエラーパターンの自動登録
        
        Args:
            error_info: エラー情報
        
        Returns:
            登録成功したかどうか
        """
        try:
            conn = sqlite3.connect(self.patterns_db_path)
            cursor = conn.cursor()
            
            pattern_data = f"{error_info['error_type']}_{error_info.get('error_message', '')}"
            pattern_id = hashlib.md5(pattern_data.encode()).hexdigest()
            
            context_str = json.dumps(error_info.get('context', {}), sort_keys=True)
            context_hash = hashlib.md5(context_str.encode()).hexdigest()
            
            cursor.execute("""
                SELECT pattern_id, frequency, success_rate
                FROM patterns
                WHERE pattern_id = ?
            """, (pattern_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                old_frequency = existing[1]
                old_success_rate = existing[2]
                new_frequency = old_frequency + 1
                new_success_rate = (
                    (old_success_rate * old_frequency + (1 if error_info.get('success', False) else 0)) /
                    new_frequency
                )
                
                cursor.execute("""
                    UPDATE patterns
                    SET frequency = ?, success_rate = ?, last_seen = ?, updated_at = ?
                    WHERE pattern_id = ?
                """, (
                    new_frequency, new_success_rate,
                    error_info.get('timestamp', datetime.now().isoformat()),
                    datetime.now().isoformat(), pattern_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO patterns (
                        pattern_id, problem_type, frequency, last_seen,
                        context_hash, context_json, success_rate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern_id, error_info['error_type'], 1,
                    error_info.get('timestamp', datetime.now().isoformat()),
                    context_hash, context_str,
                    1.0 if error_info.get('success', False) else 0.0
                ))
            
            cursor.execute("""
                INSERT INTO pattern_applications (pattern_id, success, notes)
                VALUES (?, ?, ?)
            """, (
                pattern_id, error_info.get('success', False),
                error_info.get('error_message', '')
            ))
            
            conn.commit()
            conn.close()
            
            self.evolution_history.append({
                'type': 'auto_registration',
                'timestamp': datetime.now().isoformat(),
                'pattern_id': pattern_id,
                'error_type': error_info['error_type']
            })
            self._save_evolution_history()
            
            return True
            
        except Exception as e:
            print(f"パターン自動登録エラー: {e}")
            return False

    def measure_prevention_effectiveness(self) -> Dict[str, Any]:
        """
        予防策の効果測定
        
        Returns:
            効果測定結果
            {
                'overall_effectiveness': 0.0-1.0,
                'prevention_stats': {...},
                'top_preventions': [...],
                'recommendations': [...]
            }
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 予防策テーブルからデータを取得
        cursor.execute("""
            SELECT 
                prevention_id,
                pattern_id,
                prevention_type,
                applied_count,
                success_count,
                last_applied
            FROM preventions
        """)
        
        preventions = cursor.fetchall()
        
        if not preventions:
            conn.close()
            return {
                'overall_effectiveness': 0.0,
                'prevention_stats': {
                    'total_preventions': 0,
                    'active_preventions': 0,
                    'avg_success_rate': 0.0
                },
                'top_preventions': [],
                'recommendations': ['予防策データがありません']
            }
        
        # 効果分析
        prevention_stats = []
        total_success = 0
        total_applied = 0
        
        for prev_id, pat_id, prev_type, applied, success, last_applied in preventions:
            if applied > 0:
                success_rate = success / applied
                total_success += success
                total_applied += applied
                
                prevention_stats.append({
                    'prevention_id': prev_id,
                    'pattern_id': pat_id,
                    'type': prev_type,
                    'success_rate': success_rate,
                    'applied_count': applied,
                    'last_applied': last_applied
                })
        
        # 全体効果
        overall_effectiveness = total_success / total_applied if total_applied > 0 else 0.0
        
        # トップ予防策（成功率と適用回数で評価）
        prevention_stats.sort(
            key=lambda x: x['success_rate'] * min(1.0, x['applied_count'] / 10),
            reverse=True
        )
        top_preventions = prevention_stats[:5]
        
        # 改善推奨
        recommendations = self._generate_prevention_recommendations(
            prevention_stats, overall_effectiveness
        )
        
        conn.close()
        
        result = {
            'overall_effectiveness': overall_effectiveness,
            'prevention_stats': {
                'total_preventions': len(preventions),
                'active_preventions': len(prevention_stats),
                'avg_success_rate': overall_effectiveness,
                'total_applications': total_applied,
                'total_successes': total_success
            },
            'top_preventions': top_preventions,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        # 進化履歴に記録
        self.evolution_history.append({
            'type': 'effectiveness_measurement',
            'timestamp': datetime.now().isoformat(),
            'data': result
        })
        self._save_evolution_history()
        
        return result
    
    def _generate_prevention_recommendations(
        self,
        prevention_stats: List[Dict],
        overall_effectiveness: float
    ) -> List[str]:
        """
        予防策の改善推奨を生成
        
        Args:
            prevention_stats: 予防策統計
            overall_effectiveness: 全体効果
        
        Returns:
            推奨事項リスト
        """
        recommendations = []
        
        # 全体効果の評価
        if overall_effectiveness >= 0.8:
            recommendations.append(
                f"✅ 予防策の全体効果は優秀です（{overall_effectiveness:.1%}）"
            )
        elif overall_effectiveness >= 0.6:
            recommendations.append(
                f"⚡ 予防策の全体効果は良好です（{overall_effectiveness:.1%}）が、"
                "改善の余地があります"
            )
        else:
            recommendations.append(
                f"⚠️ 予防策の全体効果が低いです（{overall_effectiveness:.1%}）。"
                "予防策の見直しが必要です"
            )
        
        # 低効果の予防策を特定
        low_effectiveness = [
            p for p in prevention_stats
            if p['success_rate'] < 0.5 and p['applied_count'] >= 3
        ]
        
        if low_effectiveness:
            recommendations.append(
                f"{len(low_effectiveness)}個の予防策が低い成功率を示しています。"
                "これらの改善または削除を検討してください"
            )
        
        # 使用頻度が低い予防策
        unused = [
            p for p in prevention_stats
            if p['applied_count'] < 2
        ]
        
        if unused and len(unused) > len(prevention_stats) * 0.3:
            recommendations.append(
                f"{len(unused)}個の予防策がほとんど使用されていません。"
                "効果的な予防策の適用を増やしてください"
            )
        
        return recommendations
    
    def optimize_prevention_strategies(self) -> Dict[str, Any]:
        """
        予防策の最適化
        
        Returns:
            最適化結果
            {
                'removed_preventions': [...],
                'enhanced_preventions': [...],
                'new_suggestions': [...]
            }
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        removed = []
        enhanced = []
        new_suggestions = []
        
        # 低効果の予防策を削除
        cursor.execute("""
            SELECT prevention_id, pattern_id, applied_count, success_count
            FROM preventions
            WHERE applied_count >= ? AND (success_count * 1.0 / applied_count) < 0.3
        """, (self.thresholds['min_pattern_frequency'],))
        
        low_effectiveness_preventions = cursor.fetchall()
        
        for prev_id, pat_id, applied, success in low_effectiveness_preventions:
            cursor.execute("DELETE FROM preventions WHERE prevention_id = ?", (prev_id,))
            removed.append({
                'prevention_id': prev_id,
                'pattern_id': pat_id,
                'reason': f'低効果（成功率: {success/applied:.1%}）'
            })
        
        # 高効果の予防策を強化（priority up）
        cursor.execute("""
            SELECT prevention_id, pattern_id, applied_count, success_count
            FROM preventions
            WHERE applied_count >= ? AND (success_count * 1.0 / applied_count) >= 0.8
        """, (self.thresholds['min_pattern_frequency'],))
        
        high_effectiveness_preventions = cursor.fetchall()
        
        for prev_id, pat_id, applied, success in high_effectiveness_preventions:
            # 優先度を上げる（実装は予防策テーブルにpriorityカラムがある場合）
            enhanced.append({
                'prevention_id': prev_id,
                'pattern_id': pat_id,
                'success_rate': success / applied,
                'action': '優先度を上げる'
            })
        
        # 新しい予防策の提案（頻発するが予防策がないパターン）
        cursor.execute("""
            SELECT p.pattern_id, p.problem_type, p.frequency
            FROM patterns p
            LEFT JOIN preventions pr ON p.pattern_id = pr.pattern_id
            WHERE p.frequency >= ? AND pr.prevention_id IS NULL
        """, (self.thresholds['min_pattern_frequency'],))
        
        patterns_without_prevention = cursor.fetchall()
        
        for pat_id, prob_type, freq in patterns_without_prevention:
            new_suggestions.append({
                'pattern_id': pat_id,
                'problem_type': prob_type,
                'frequency': freq,
                'suggestion': f'{prob_type}に対する予防策の作成を推奨'
            })
        
        conn.commit()
        conn.close()
        
        result = {
            'removed_preventions': removed,
            'enhanced_preventions': enhanced,
            'new_suggestions': new_suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        # 進化履歴に記録
        self.evolution_history.append({
            'type': 'optimization',
            'timestamp': datetime.now().isoformat(),
            'data': result
        })
        self._save_evolution_history()
        
        return result
    
    def diagnose_evolution_system(self) -> Dict[str, Any]:
        """
        進化システム全体の診断
        
        Returns:
            診断結果
        """
        # 進化履歴の分析
        total_proposals = sum(
            1 for h in self.evolution_history 
            if h.get('type') == 'proposal'
        )
        
        total_registrations = sum(
            1 for h in self.evolution_history 
            if h.get('type') == 'auto_registration'
        )
        
        total_optimizations = sum(
            1 for h in self.evolution_history 
            if h.get('type') == 'optimization'
        )
        
        # 最近の活動（過去30日）
        recent_date = datetime.now() - timedelta(days=30)
        recent_activities = [
            h for h in self.evolution_history
            if datetime.fromisoformat(h['timestamp']) > recent_date
        ]
        
        # ヘルススコア
        health_score = min(1.0, (
            (total_proposals * 0.3 +
             total_registrations * 0.4 +
             total_optimizations * 0.3) / 20
        ))
        
        return {
            'health_score': health_score,
            'total_improvements': len(self.evolution_history),
            'proposals_count': total_proposals,
            'auto_registrations_count': total_registrations,
            'optimizations_count': total_optimizations,
            'recent_activities': len(recent_activities),
            'status': 'active' if len(recent_activities) > 0 else 'inactive',
            'timestamp': datetime.now().isoformat()
        }


def main():
    """テスト実行用のメイン関数"""
    print("=== SelfEvolutionEngine Test ===")
    print()
    
    engine = SelfEvolutionEngine()
    
    print("1. システム診断:")
    diagnosis = engine.diagnose_evolution_system()
    print(f"   ヘルススコア: {diagnosis['health_score']:.2f}")
    print(f"   ステータス: {diagnosis['status']}")
    print(f"   改善提案: {diagnosis['proposals_count']}件")
    print(f"   自動登録: {diagnosis['auto_registrations_count']}件")
    print()
    
    print("2. コード改善提案:")
    proposals = engine.propose_code_improvements()
    print(f"   提案数: {len(proposals)}件")
    for i, prop in enumerate(proposals[:3], 1):
        print(f"   {i}. {prop['target']}: {prop['improvement_type']}")
        print(f"      信頼度: {prop['confidence']:.2f}")
    print()
    
    print("✅ SelfEvolutionEngine テスト完了")


if __name__ == "__main__":
    main()
