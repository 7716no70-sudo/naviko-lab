#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdvancedLearningAnalyzer - Navikoの高度な学習データ分析システム

このモジュールはNavikoのSystem 3 Phase 3の一部として、以下を提供します：
- 成功/失敗パターンの相関分析
- 予測精度向上アルゴリズム（単純ベイズ、決定木的手法）
- 時系列データからのトレンド予測
- ProblemPatternLearnerとの高度な連携

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import json
import sqlite3
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
import hashlib


class AdvancedLearningAnalyzer:
    """
    高度な学習データ分析システム
    
    ProblemPatternLearnerが蓄積した学習データを使って、
    より高度な予測と分析を実行します。
    """
    
    def __init__(self, lab_dir: str = None):
        """
        AdvancedLearningAnalyzerの初期化
        
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
        self.analysis_cache_path = self.lab_dir / "analysis_cache.json"
        
        # 分析結果キャッシュ
        self.analysis_cache: Dict[str, Any] = self._load_analysis_cache()
        
        # 機械学習モデルのパラメータ
        self.ml_params = {
            'min_samples': 3,  # 最小サンプル数
            'confidence_threshold': 0.6,  # 信頼度閾値
            'correlation_threshold': 0.5,  # 相関閾値
            'trend_window_days': 30  # トレンド分析期間（日）
        }
    
    def _load_analysis_cache(self) -> Dict:
        """
        分析結果キャッシュのロード
        
        Returns:
            キャッシュデータ
        """
        if self.analysis_cache_path.exists():
            try:
                with open(self.analysis_cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            'correlations': {},
            'predictions': {},
            'trends': {},
            'last_updated': None
        }
    
    def _save_analysis_cache(self):
        """
        分析結果キャッシュの保存
        """
        self.analysis_cache['last_updated'] = datetime.now().isoformat()
        try:
            with open(self.analysis_cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"キャッシュ保存エラー: {e}")

    def analyze_pattern_correlations(self) -> Dict[str, List[Dict]]:
        """
        パターン間の相関分析
        
        成功/失敗パターンの相関を分析し、どのパターンが
        どのパターンと関連しているかを明らかにします。
        
        Returns:
            相関分析結果
            {
                'high_correlations': [
                    {
                        'pattern_a': 'pattern_id_1',
                        'pattern_b': 'pattern_id_2',
                        'correlation_score': 0.85,
                        'co_occurrence_rate': 0.7,
                        'success_when_both': 0.9
                    },
                    ...
                ],
                'negative_correlations': [...],
                'insights': [...]
            }
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 全パターンとその適用履歴を取得
        cursor.execute("""
            SELECT 
                p.pattern_id,
                p.problem_type,
                p.success_rate,
                p.frequency,
                GROUP_CONCAT(pa.success || '|' || pa.applied_at) as applications
            FROM patterns p
            LEFT JOIN pattern_applications pa ON p.pattern_id = pa.pattern_id
            GROUP BY p.pattern_id
        """)
        
        patterns = cursor.fetchall()
        conn.close()
        
        # パターンペアの共起分析
        correlations = []
        
        for i, pattern_a in enumerate(patterns):
            for pattern_b in patterns[i+1:]:
                correlation = self._calculate_pattern_correlation(
                    pattern_a, pattern_b
                )
                
                if correlation['score'] >= self.ml_params['correlation_threshold']:
                    correlations.append({
                        'pattern_a': pattern_a[0],
                        'pattern_a_type': pattern_a[1],
                        'pattern_b': pattern_b[0],
                        'pattern_b_type': pattern_b[1],
                        'correlation_score': correlation['score'],
                        'co_occurrence_rate': correlation['co_occurrence'],
                        'success_when_both': correlation['joint_success']
                    })
        
        # 相関スコアでソート
        correlations.sort(key=lambda x: x['correlation_score'], reverse=True)
        
        # 結果を分類
        result = {
            'high_correlations': [
                c for c in correlations 
                if c['correlation_score'] >= 0.7
            ],
            'moderate_correlations': [
                c for c in correlations 
                if 0.5 <= c['correlation_score'] < 0.7
            ],
            'insights': self._generate_correlation_insights(correlations)
        }
        
        # キャッシュ更新
        self.analysis_cache['correlations'] = result
        self._save_analysis_cache()
        
        return result
    
    def _calculate_pattern_correlation(
        self, 
        pattern_a: Tuple, 
        pattern_b: Tuple
    ) -> Dict[str, float]:
        """
        2つのパターン間の相関スコアを計算
        
        Args:
            pattern_a: パターンA（id, type, success_rate, frequency, applications）
            pattern_b: パターンB（同上）
        
        Returns:
            相関スコア情報
        """
        # 適用履歴を解析
        apps_a = self._parse_applications(pattern_a[4])
        apps_b = self._parse_applications(pattern_b[4])
        
        if not apps_a or not apps_b:
            return {'score': 0.0, 'co_occurrence': 0.0, 'joint_success': 0.0}
        
        # 時間的近接性による共起チェック（同じ日に適用されたか）
        dates_a = {app['date'] for app in apps_a}
        dates_b = {app['date'] for app in apps_b}
        
        common_dates = dates_a & dates_b
        co_occurrence_rate = len(common_dates) / min(len(dates_a), len(dates_b))
        
        # 両方が適用された時の成功率
        joint_success_count = 0
        joint_total_count = 0
        
        for date in common_dates:
            success_a = any(
                app['date'] == date and app['success'] 
                for app in apps_a
            )
            success_b = any(
                app['date'] == date and app['success'] 
                for app in apps_b
            )
            
            joint_total_count += 1
            if success_a and success_b:
                joint_success_count += 1
        
        joint_success_rate = (
            joint_success_count / joint_total_count 
            if joint_total_count > 0 else 0.0
        )
        
        # 相関スコア = 共起率 × 成功率の類似度
        success_similarity = 1.0 - abs(
            pattern_a[2] - pattern_b[2]
        )  # success_rate
        
        correlation_score = (
            co_occurrence_rate * 0.6 + 
            success_similarity * 0.2 + 
            joint_success_rate * 0.2
        )
        
        return {
            'score': correlation_score,
            'co_occurrence': co_occurrence_rate,
            'joint_success': joint_success_rate
        }
    
    def _parse_applications(self, apps_string: str) -> List[Dict]:
        """
        適用履歴文字列をパース
        
        Args:
            apps_string: "success|timestamp,success|timestamp,..." 形式
        
        Returns:
            適用履歴リスト
        """
        if not apps_string:
            return []
        
        applications = []
        for app in apps_string.split(','):
            try:
                success_str, timestamp = app.split('|')
                success = success_str.strip() == '1' or success_str.strip().lower() == 'true'
                date = datetime.fromisoformat(timestamp).date()
                applications.append({
                    'success': success,
                    'date': date,
                    'timestamp': timestamp
                })
            except (ValueError, AttributeError):
                continue
        
        return applications
    
    def _generate_correlation_insights(self, correlations: List[Dict]) -> List[str]:
        """
        相関分析から洞察を生成
        
        Args:
            correlations: 相関分析結果
        
        Returns:
            洞察リスト
        """
        insights = []
        
        if not correlations:
            insights.append(
                "相関分析に十分なデータがありません。"
                "より多くのパターンを記録してください。"
            )
            return insights
        
        # 最も強い相関
        if correlations:
            top_corr = correlations[0]
            insights.append(
                f"最も強い相関: {top_corr['pattern_a_type']} と "
                f"{top_corr['pattern_b_type']} （スコア: {top_corr['correlation_score']:.2f}）"
            )
        
        # 高成功率の組み合わせ
        high_success_pairs = [
            c for c in correlations 
            if c['success_when_both'] >= 0.8
        ]
        
        if high_success_pairs:
            insights.append(
                f"{len(high_success_pairs)}組のパターンペアが "
                f"同時適用時に高い成功率（80%以上）を示しています。"
            )
        
        return insights

    def predict_problem_occurrence(
        self, 
        problem_type: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        問題発生確率の予測（単純ベイズ的手法）
        
        Args:
            problem_type: 問題タイプ
            context: コンテキスト情報
        
        Returns:
            予測結果
            {
                'probability': 0.75,
                'confidence': 0.8,
                'evidence': [...],
                'recommendations': [...]
            }
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 過去の同種問題の発生頻度
        cursor.execute("""
            SELECT 
                COUNT(*) as total_occurrences,
                AVG(success_rate) as avg_success,
                MAX(last_seen) as most_recent
            FROM patterns
            WHERE problem_type = ?
        """, (problem_type,))
        
        stats = cursor.fetchone()
        
        if not stats or stats[0] == 0:
            conn.close()
            return {
                'probability': 0.0,
                'confidence': 0.0,
                'evidence': ['該当する問題パターンのデータがありません'],
                'recommendations': [
                    '新しい問題タイプのため、慎重に対処してください'
                ]
            }
        
        total_occurrences, avg_success, most_recent = stats
        
        # 時間的近接性による確率調整
        if most_recent:
            try:
                days_since = (
                    datetime.now() - 
                    datetime.fromisoformat(most_recent)
                ).days
                
                # 最近発生したほど確率が高い
                time_factor = math.exp(-days_since / 30)
            except (ValueError, TypeError):
                time_factor = 0.5
        else:
            time_factor = 0.5
        
        # 基本確率 = 発生頻度 × 時間要因
        base_probability = min(1.0, total_occurrences / 100) * time_factor
        
        # コンテキストマッチングによる調整
        if context:
            context_factor = self._calculate_context_match(
                cursor, problem_type, context
            )
            final_probability = base_probability * (1 + context_factor) / 2
        else:
            final_probability = base_probability
        
        # 信頼度計算（サンプル数に基づく）
        confidence = min(1.0, total_occurrences / self.ml_params['min_samples'])
        
        conn.close()
        
        # エビデンス収集
        evidence = [
            f"過去{total_occurrences}回の同種問題を記録",
            f"平均成功率: {avg_success:.1%}" if avg_success else "成功率データなし",
            f"最終発生: {days_since}日前" if most_recent else "発生日不明"
        ]
        
        # 推奨事項生成
        recommendations = self._generate_prediction_recommendations(
            final_probability, avg_success, total_occurrences
        )
        
        result = {
            'probability': final_probability,
            'confidence': confidence,
            'evidence': evidence,
            'recommendations': recommendations,
            'historical_success_rate': avg_success or 0.0
        }
        
        # キャッシュ更新
        cache_key = f"{problem_type}_{datetime.now().date().isoformat()}"
        self.analysis_cache['predictions'][cache_key] = result
        self._save_analysis_cache()
        
        return result
    
    def _calculate_context_match(
        self, 
        cursor: sqlite3.Cursor,
        problem_type: str,
        context: Dict[str, Any]
    ) -> float:
        """
        コンテキストマッチング係数を計算
        
        Args:
            cursor: SQLiteカーソル
            problem_type: 問題タイプ
            context: コンテキスト情報
        
        Returns:
            マッチング係数（-1.0 〜 1.0）
        """
        # 過去の同種問題のコンテキストを取得
        cursor.execute("""
            SELECT context_json
            FROM patterns
            WHERE problem_type = ?
            AND context_json IS NOT NULL
        """, (problem_type,))
        
        past_contexts = []
        for row in cursor.fetchall():
            try:
                past_contexts.append(json.loads(row[0]))
            except (json.JSONDecodeError, TypeError):
                continue
        
        if not past_contexts:
            return 0.0
        
        # 類似度計算（共通キー数とその値の一致度）
        similarities = []
        for past_ctx in past_contexts:
            common_keys = set(context.keys()) & set(past_ctx.keys())
            if not common_keys:
                continue
            
            matching_values = sum(
                1 for key in common_keys 
                if context.get(key) == past_ctx.get(key)
            )
            similarity = matching_values / len(common_keys)
            similarities.append(similarity)
        
        if not similarities:
            return 0.0
        
        # 平均類似度を返す（-0.5 〜 0.5の範囲に正規化）
        avg_similarity = sum(similarities) / len(similarities)
        return (avg_similarity - 0.5) * 2  # -1.0 〜 1.0
    
    def _generate_prediction_recommendations(
        self,
        probability: float,
        success_rate: Optional[float],
        occurrences: int
    ) -> List[str]:
        """
        予測結果に基づく推奨事項を生成
        
        Args:
            probability: 発生確率
            success_rate: 成功率
            occurrences: 発生回数
        
        Returns:
            推奨事項リスト
        """
        recommendations = []
        
        # 確率に基づく推奨
        if probability > 0.7:
            recommendations.append(
                "⚠️ 高確率で問題が発生する可能性があります。"
                "事前対策を強く推奨します。"
            )
        elif probability > 0.4:
            recommendations.append(
                "⚡ 中程度の確率で問題が発生する可能性があります。"
                "予防策の準備を検討してください。"
            )
        else:
            recommendations.append(
                "✅ 問題発生の確率は低いですが、念のため注意してください。"
            )
        
        # 成功率に基づく推奨
        if success_rate is not None:
            if success_rate < 0.5:
                recommendations.append(
                    f"過去の成功率が{success_rate:.1%}と低いため、"
                    "代替手段の検討も推奨します。"
                )
            elif success_rate > 0.8:
                recommendations.append(
                    f"過去の成功率が{success_rate:.1%}と高いため、"
                    "標準的な対処方法が有効です。"
                )
        
        # データ量に基づく推奨
        if occurrences < self.ml_params['min_samples']:
            recommendations.append(
                f"⚠️ データサンプルが少ない（{occurrences}件）ため、"
                "予測の信頼度は低いです。慎重に判断してください。"
            )
        
        return recommendations

    def analyze_temporal_trends(
        self,
        problem_type: str = None,
        window_days: int = None
    ) -> Dict[str, Any]:
        """
        時系列データからのトレンド分析
        
        Args:
            problem_type: 分析対象の問題タイプ（Noneで全体）
            window_days: 分析期間（日）
        
        Returns:
            トレンド分析結果
            {
                'trend_direction': 'increasing' | 'stable' | 'decreasing',
                'trend_strength': 0.0-1.0,
                'forecast': {...},
                'anomalies': [...],
                'insights': [...]
            }
        """
        if window_days is None:
            window_days = self.ml_params['trend_window_days']
        
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 時系列データを取得
        query = """
            SELECT 
                DATE(applied_at) as date,
                COUNT(*) as count,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes
            FROM pattern_applications pa
            JOIN patterns p ON pa.pattern_id = p.pattern_id
            WHERE DATE(applied_at) >= DATE('now', '-{} days')
        """.format(window_days)
        
        if problem_type:
            query += " AND p.problem_type = ?"
            cursor.execute(query + " GROUP BY DATE(applied_at) ORDER BY date", (problem_type,))
        else:
            cursor.execute(query + " GROUP BY DATE(applied_at) ORDER BY date")
        
        time_series = cursor.fetchall()
        conn.close()
        
        if len(time_series) < 2:
            return {
                'trend_direction': 'unknown',
                'trend_strength': 0.0,
                'forecast': {},
                'anomalies': [],
                'insights': ['トレンド分析に十分なデータがありません']
            }
        
        # トレンド方向と強度を計算
        dates = [row[0] for row in time_series]
        counts = [row[1] for row in time_series]
        success_rates = [row[2] / row[1] if row[1] > 0 else 0 for row in time_series]
        
        # 単純線形回帰（最小二乗法）
        n = len(counts)
        x = list(range(n))
        y = counts
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        # 傾き（トレンド方向）
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        # トレンド方向の判定
        if slope > 0.1:
            trend_direction = 'increasing'
        elif slope < -0.1:
            trend_direction = 'decreasing'
        else:
            trend_direction = 'stable'
        
        # トレンド強度（R²）
        mean_y = sum_y / n
        ss_tot = sum((yi - mean_y) ** 2 for yi in y)
        intercept = (sum_y - slope * sum_x) / n
        ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
        
        trend_strength = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
        
        # 予測（次の7日間）
        forecast_days = 7
        forecast = []
        for i in range(forecast_days):
            future_x = n + i
            predicted_count = max(0, slope * future_x + intercept)
            forecast.append({
                'days_ahead': i + 1,
                'predicted_count': round(predicted_count, 1)
            })
        
        # 異常検出（平均から2標準偏差以上離れている日）
        mean_count = sum(counts) / len(counts)
        std_dev = math.sqrt(sum((c - mean_count) ** 2 for c in counts) / len(counts))
        
        anomalies = []
        for date, count, success_rate in zip(dates, counts, success_rates):
            if abs(count - mean_count) > 2 * std_dev:
                anomalies.append({
                    'date': date,
                    'count': count,
                    'deviation': abs(count - mean_count) / std_dev,
                    'success_rate': success_rate
                })
        
        # 洞察生成
        insights = self._generate_trend_insights(
            trend_direction, trend_strength, anomalies, success_rates
        )
        
        result = {
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'forecast': forecast,
            'anomalies': anomalies,
            'insights': insights,
            'data_points': len(time_series),
            'avg_success_rate': sum(success_rates) / len(success_rates) if success_rates else 0.0
        }
        
        # キャッシュ更新
        cache_key = f"{problem_type or 'all'}_{window_days}d"
        self.analysis_cache['trends'][cache_key] = result
        self._save_analysis_cache()
        
        return result
    
    def _generate_trend_insights(
        self,
        direction: str,
        strength: float,
        anomalies: List[Dict],
        success_rates: List[float]
    ) -> List[str]:
        """
        トレンド分析から洞察を生成
        
        Args:
            direction: トレンド方向
            strength: トレンド強度
            anomalies: 検出された異常
            success_rates: 成功率の時系列
        
        Returns:
            洞察リスト
        """
        insights = []
        
        # トレンド方向の洞察
        if direction == 'increasing':
            insights.append(
                f"📈 問題発生が増加傾向にあります（強度: {strength:.2f}）。"
                "予防策の強化を検討してください。"
            )
        elif direction == 'decreasing':
            insights.append(
                f"📉 問題発生が減少傾向にあります（強度: {strength:.2f}）。"
                "改善策が効果を発揮している可能性があります。"
            )
        else:
            insights.append(
                f"➡️ 問題発生は安定しています（強度: {strength:.2f}）。"
            )
        
        # 異常の洞察
        if anomalies:
            insights.append(
                f"⚠️ {len(anomalies)}日間で異常な発生パターンを検出しました。"
                "特定の日に問題が集中している可能性があります。"
            )
        
        # 成功率の洞察
        if success_rates:
            recent_avg = sum(success_rates[-7:]) / min(7, len(success_rates))
            overall_avg = sum(success_rates) / len(success_rates)
            
            if recent_avg > overall_avg + 0.1:
                insights.append(
                    f"✅ 最近の成功率（{recent_avg:.1%}）が全体平均（{overall_avg:.1%}）を上回っています。"
                )
            elif recent_avg < overall_avg - 0.1:
                insights.append(
                    f"⚠️ 最近の成功率（{recent_avg:.1%}）が全体平均（{overall_avg:.1%}）を下回っています。"
                )
        
        return insights
    
    def diagnose_learning_system(self) -> Dict[str, Any]:
        """
        学習システム全体の診断
        
        Returns:
            診断結果
            {
                'data_quality': {...},
                'prediction_accuracy': {...},
                'recommendations': [...],
                'health_score': 0.0-1.0
            }
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # データ品質チェック
        cursor.execute("SELECT COUNT(*) FROM patterns")
        total_patterns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pattern_applications")
        total_applications = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM patterns 
            WHERE frequency >= ?
        """, (self.ml_params['min_samples'],))
        reliable_patterns = cursor.fetchone()[0]
        
        data_quality = {
            'total_patterns': total_patterns,
            'total_applications': total_applications,
            'reliable_patterns': reliable_patterns,
            'reliability_ratio': reliable_patterns / total_patterns if total_patterns > 0 else 0.0
        }
        
        # 予測精度推定（最近の予測と実際の結果を比較）
        prediction_accuracy = self._estimate_prediction_accuracy(cursor)
        
        conn.close()
        
        # ヘルススコア計算
        health_score = self._calculate_health_score(
            data_quality, prediction_accuracy
        )
        
        # 推奨事項
        recommendations = self._generate_system_recommendations(
            data_quality, prediction_accuracy, health_score
        )
        
        return {
            'data_quality': data_quality,
            'prediction_accuracy': prediction_accuracy,
            'recommendations': recommendations,
            'health_score': health_score,
            'timestamp': datetime.now().isoformat()
        }
    
    def _estimate_prediction_accuracy(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """
        予測精度の推定
        
        Args:
            cursor: SQLiteカーソル
        
        Returns:
            予測精度情報
        """
        # 簡易的な精度推定（成功率の標準偏差から計算）
        cursor.execute("""
            SELECT AVG(success_rate), 
                   AVG(success_rate * success_rate)
            FROM patterns
            WHERE frequency >= ?
        """, (self.ml_params['min_samples'],))
        
        result = cursor.fetchone()
        if not result or result[0] is None:
            return {
                'estimated_accuracy': 0.0,
                'confidence': 0.0,
                'status': 'insufficient_data'
            }
        
        mean = result[0]
        mean_of_squares = result[1]
        variance = mean_of_squares - mean ** 2
        std_dev = math.sqrt(max(0, variance))
        
        # 精度 = 1 - (標準偏差 / 理論最大標準偏差)
        max_std_dev = 0.5  # 最大標準偏差（0.5で50%）
        estimated_accuracy = 1.0 - min(1.0, std_dev / max_std_dev)
        
        # 信頼度（データ量に基づく）
        cursor.execute("SELECT COUNT(*) FROM patterns WHERE frequency >= ?", 
                      (self.ml_params['min_samples'],))
        sample_count = cursor.fetchone()[0]
        confidence = min(1.0, sample_count / 10)  # 10パターン以上で信頼度1.0
        
        return {
            'estimated_accuracy': estimated_accuracy,
            'confidence': confidence,
            'status': 'reliable' if confidence >= 0.7 else 'developing'
        }
    
    def _calculate_health_score(
        self,
        data_quality: Dict,
        prediction_accuracy: Dict
    ) -> float:
        """
        システム全体のヘルススコアを計算
        
        Args:
            data_quality: データ品質情報
            prediction_accuracy: 予測精度情報
        
        Returns:
            ヘルススコア（0.0-1.0）
        """
        # データ品質スコア（40%）
        quality_score = (
            min(1.0, data_quality['total_patterns'] / 10) * 0.5 +
            min(1.0, data_quality['total_applications'] / 50) * 0.3 +
            data_quality['reliability_ratio'] * 0.2
        ) * 0.4
        
        # 予測精度スコア（60%）
        accuracy_score = (
            prediction_accuracy['estimated_accuracy'] * 0.7 +
            prediction_accuracy['confidence'] * 0.3
        ) * 0.6
        
        return quality_score + accuracy_score
    
    def _generate_system_recommendations(
        self,
        data_quality: Dict,
        prediction_accuracy: Dict,
        health_score: float
    ) -> List[str]:
        """
        システム全体の推奨事項を生成
        
        Args:
            data_quality: データ品質情報
            prediction_accuracy: 予測精度情報
            health_score: ヘルススコア
        
        Returns:
            推奨事項リスト
        """
        recommendations = []
        
        # ヘルススコアに基づく全体評価
        if health_score >= 0.8:
            recommendations.append(
                "✅ 学習システムは良好に動作しています。"
            )
        elif health_score >= 0.5:
            recommendations.append(
                "⚡ 学習システムは機能していますが、改善の余地があります。"
            )
        else:
            recommendations.append(
                "⚠️ 学習システムの品質向上が必要です。"
            )
        
        # データ品質の推奨
        if data_quality['total_patterns'] < 5:
            recommendations.append(
                f"より多くの問題パターンを記録してください（現在: {data_quality['total_patterns']}件）。"
            )
        
        if data_quality['reliability_ratio'] < 0.5:
            recommendations.append(
                "信頼できるパターン（十分なサンプル数）の割合が低いです。"
                "既存パターンの適用回数を増やしてください。"
            )
        
        # 予測精度の推奨
        if prediction_accuracy['status'] == 'insufficient_data':
            recommendations.append(
                "予測精度の評価に十分なデータがありません。"
            )
        elif prediction_accuracy['estimated_accuracy'] < 0.6:
            recommendations.append(
                f"予測精度が低い可能性があります（推定: {prediction_accuracy['estimated_accuracy']:.1%}）。"
                "パターンの精度向上を検討してください。"
            )
        
        return recommendations


# テスト用のメイン関数
def main():
    """
    テスト実行用のメイン関数
    """
    print("=== AdvancedLearningAnalyzer Test ===\n")
    
    # インスタンス作成
    analyzer = AdvancedLearningAnalyzer()
    
    # システム診断
    print("1. システム診断:")
    diagnosis = analyzer.diagnose_learning_system()
    print(f"   ヘルススコア: {diagnosis['health_score']:.2f}")
    print(f"   データ品質: {diagnosis['data_quality']}")
    print(f"   予測精度: {diagnosis['prediction_accuracy']}")
    print(f"   推奨事項: {len(diagnosis['recommendations'])}件\n")
    
    # 相関分析
    print("2. パターン相関分析:")
    correlations = analyzer.analyze_pattern_correlations()
    print(f"   高相関: {len(correlations['high_correlations'])}組")
    print(f"   中相関: {len(correlations['moderate_correlations'])}組")
    print(f"   洞察: {len(correlations['insights'])}件\n")
    
    print("✅ AdvancedLearningAnalyzer テスト完了")


if __name__ == "__main__":
    main()
