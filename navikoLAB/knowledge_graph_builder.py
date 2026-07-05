#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KnowledgeGraphBuilder - Navikoの知識グラフ構築システム

このモジュールはNavikoのSystem 3 Phase 3の一部として、以下を提供します：
- 問題間の関連性マッピング（グラフデータベース的構造）
- 類似問題の自動検出（類似度計算）
- 解決策の推論エンジン（パターンマッチング）
- 全モジュール統合インターフェース

Author: Naviko Development Team
Version: 1.0.0
Date: 2026-07-05
"""

import os
import json
import sqlite3
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import defaultdict, Counter


class KnowledgeGraphBuilder:
    """
    知識グラフ構築システム
    
    問題パターン間の関連性を分析し、グラフ構造で知識を管理します。
    """
    
    def __init__(self, lab_dir: str = None):
        """
        KnowledgeGraphBuilderの初期化
        
        Args:
            lab_dir: navikoLABディレクトリのパス
        """
        if lab_dir is None:
            lab_dir = os.path.join(os.path.expanduser("~"), "navikoLAB")
            if not os.path.exists(lab_dir):
                lab_dir = "/Workspace/Users/7716no70@gmail.com/naviko-lab/navikoLAB"
        
        self.lab_dir = Path(lab_dir)
        self.patterns_db_path = self.lab_dir / "problem_patterns.db"
        self.graph_cache_path = self.lab_dir / "knowledge_graph.json"
        
        # グラフ構造（隣接リスト）
        self.knowledge_graph: Dict[str, List[Dict]] = self._load_graph()
        
        # 類似度計算の閾値
        self.similarity_threshold = 0.6
    
    def _load_graph(self) -> Dict[str, List[Dict]]:
        """知識グラフのロード"""
        if self.graph_cache_path.exists():
            try:
                with open(self.graph_cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_graph(self):
        """知識グラフの保存"""
        try:
            with open(self.graph_cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_graph, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"グラフ保存エラー: {e}")
    
    def build_knowledge_graph(self) -> Dict[str, Any]:
        """
        知識グラフの構築
        
        Returns:
            グラフ構築結果
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 全パターンを取得
        cursor.execute("""
            SELECT 
                pattern_id, problem_type, context_json, solution_json,
                success_rate, frequency
            FROM patterns
        """)
        
        patterns = cursor.fetchall()
        conn.close()
        
        # グラフをリセット
        self.knowledge_graph = {}
        
        # ノード追加（各パターン）
        for pattern in patterns:
            pat_id = pattern[0]
            self.knowledge_graph[pat_id] = {
                'problem_type': pattern[1],
                'success_rate': pattern[4],
                'frequency': pattern[5],
                'edges': []
            }
        
        # エッジ追加（類似度に基づく）
        edge_count = 0
        for i, pattern_a in enumerate(patterns):
            for pattern_b in patterns[i+1:]:
                similarity = self._calculate_similarity(pattern_a, pattern_b)
                
                if similarity >= self.similarity_threshold:
                    pat_a_id = pattern_a[0]
                    pat_b_id = pattern_b[0]
                    
                    # 双方向エッジを追加
                    self.knowledge_graph[pat_a_id]['edges'].append({
                        'target': pat_b_id,
                        'similarity': similarity,
                        'relation_type': 'similar'
                    })
                    
                    self.knowledge_graph[pat_b_id]['edges'].append({
                        'target': pat_a_id,
                        'similarity': similarity,
                        'relation_type': 'similar'
                    })
                    
                    edge_count += 1
        
        # グラフ保存
        self._save_graph()
        
        return {
            'node_count': len(self.knowledge_graph),
            'edge_count': edge_count,
            'avg_connections': edge_count * 2 / len(self.knowledge_graph) if self.knowledge_graph else 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_similarity(
        self,
        pattern_a: Tuple,
        pattern_b: Tuple
    ) -> float:
        """
        2つのパターン間の類似度を計算
        
        Args:
            pattern_a: パターンA（id, type, context_json, solution_json, success_rate, frequency）
            pattern_b: パターンB（同上）
        
        Returns:
            類似度（0.0-1.0）
        """
        # 問題タイプの類似度
        type_similarity = 1.0 if pattern_a[1] == pattern_b[1] else 0.0
        
        # コンテキストの類似度
        try:
            context_a = json.loads(pattern_a[2]) if pattern_a[2] else {}
            context_b = json.loads(pattern_b[2]) if pattern_b[2] else {}
            context_similarity = self._jaccard_similarity(
                set(context_a.keys()), set(context_b.keys())
            )
        except (json.JSONDecodeError, TypeError):
            context_similarity = 0.0
        
        # 解決策の類似度
        try:
            solution_a = json.loads(pattern_a[3]) if pattern_a[3] else {}
            solution_b = json.loads(pattern_b[3]) if pattern_b[3] else {}
            solution_similarity = self._jaccard_similarity(
                set(solution_a.keys()), set(solution_b.keys())
            )
        except (json.JSONDecodeError, TypeError):
            solution_similarity = 0.0
        
        # 成功率の類似度
        success_a = pattern_a[4] if pattern_a[4] else 0.5
        success_b = pattern_b[4] if pattern_b[4] else 0.5
        success_similarity = 1.0 - abs(success_a - success_b)
        
        # 加重平均
        total_similarity = (
            type_similarity * 0.4 +
            context_similarity * 0.3 +
            solution_similarity * 0.2 +
            success_similarity * 0.1
        )
        
        return total_similarity
    
    def _jaccard_similarity(self, set_a: Set, set_b: Set) -> float:
        """ジャッカード係数による類似度計算"""
        if not set_a and not set_b:
            return 1.0
        if not set_a or not set_b:
            return 0.0
        
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        
        return intersection / union if union > 0 else 0.0
    
    def find_similar_problems(
        self,
        problem_type: str,
        context: Dict[str, Any] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        類似問題の自動検出
        
        Args:
            problem_type: 問題タイプ
            context: コンテキスト情報
            top_k: 上位K件を返す
        
        Returns:
            類似問題リスト
        """
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        # 全パターンを取得
        cursor.execute("""
            SELECT 
                pattern_id, problem_type, context_json, solution_json,
                success_rate, frequency
            FROM patterns
        """)
        
        patterns = cursor.fetchall()
        conn.close()
        
        # 類似度計算
        similarities = []
        
        for pattern in patterns:
            pat_id, pat_type, ctx_json, sol_json, success_rate, frequency = pattern
            
            # 問題タイプのマッチング
            type_score = 1.0 if pat_type == problem_type else 0.3
            
            # コンテキストのマッチング
            if context:
                try:
                    pat_context = json.loads(ctx_json) if ctx_json else {}
                    context_score = self._jaccard_similarity(
                        set(context.keys()), set(pat_context.keys())
                    )
                except (json.JSONDecodeError, TypeError):
                    context_score = 0.0
            else:
                context_score = 0.5
            
            # 総合スコア
            total_score = type_score * 0.7 + context_score * 0.3
            
            if total_score >= 0.3:  # 最低閾値
                similarities.append({
                    'pattern_id': pat_id,
                    'problem_type': pat_type,
                    'similarity_score': total_score,
                    'success_rate': success_rate,
                    'frequency': frequency,
                    'solution': json.loads(sol_json) if sol_json else {}
                })
        
        # スコアでソート
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities[:top_k]
    
    def infer_solution(
        self,
        problem_type: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        解決策の推論エンジン
        
        Args:
            problem_type: 問題タイプ
            context: コンテキスト情報
        
        Returns:
            推論された解決策
        """
        # 類似問題を検索
        similar_problems = self.find_similar_problems(
            problem_type, context, top_k=3
        )
        
        if not similar_problems:
            return {
                'success': False,
                'reason': '類似する問題が見つかりませんでした',
                'recommendation': '新しい問題として記録し、手動で解決策を検討してください'
            }
        
        # 最も類似度が高く、成功率も高い解決策を選択
        best_solution = max(
            similar_problems,
            key=lambda x: x['similarity_score'] * 0.6 + x['success_rate'] * 0.4
        )
        
        # 信頼度計算
        confidence = (
            best_solution['similarity_score'] * 0.5 +
            best_solution['success_rate'] * 0.3 +
            min(1.0, best_solution['frequency'] / 5) * 0.2
        )
        
        return {
            'success': True,
            'solution': best_solution['solution'],
            'confidence': confidence,
            'source_pattern': best_solution['pattern_id'],
            'similarity': best_solution['similarity_score'],
            'historical_success_rate': best_solution['success_rate'],
            'alternatives': similar_problems[1:] if len(similar_problems) > 1 else []
        }
    
    def traverse_graph(
        self,
        start_pattern_id: str,
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        グラフの探索（幅優先探索）
        
        Args:
            start_pattern_id: 開始パターンID
            max_depth: 最大探索深度
        
        Returns:
            探索結果
        """
        if start_pattern_id not in self.knowledge_graph:
            return {
                'visited': [],
                'path_count': 0,
                'insights': ['指定されたパターンが見つかりませんでした']
            }
        
        visited = set()
        queue = [(start_pattern_id, 0)]  # (pattern_id, depth)
        paths = []
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            paths.append({
                'pattern_id': current_id,
                'problem_type': self.knowledge_graph[current_id]['problem_type'],
                'depth': depth
            })
            
            # 隣接ノードをキューに追加
            for edge in self.knowledge_graph[current_id]['edges']:
                neighbor_id = edge['target']
                if neighbor_id not in visited:
                    queue.append((neighbor_id, depth + 1))
        
        return {
            'visited': list(visited),
            'paths': paths,
            'path_count': len(paths),
            'insights': self._generate_traversal_insights(paths)
        }
    
    def _generate_traversal_insights(self, paths: List[Dict]) -> List[str]:
        """探索結果からの洞察生成"""
        insights = []
        
        if not paths:
            return ['探索結果がありません']
        
        # 深度分布
        depth_counts = Counter(p['depth'] for p in paths)
        max_depth = max(depth_counts.keys())
        
        insights.append(
            f"{len(paths)}個の関連パターンが見つかりました（最大深度: {max_depth}）"
        )
        
        # 問題タイプ分布
        type_counts = Counter(p['problem_type'] for p in paths)
        most_common_type = type_counts.most_common(1)[0]
        
        insights.append(
            f"最も多い問題タイプ: {most_common_type[0]} ({most_common_type[1]}件)"
        )
        
        return insights
    
    def diagnose_knowledge_graph(self) -> Dict[str, Any]:
        """
        知識グラフ全体の診断
        
        Returns:
            診断結果
        """
        if not self.knowledge_graph:
            return {
                'status': 'empty',
                'health_score': 0.0,
                'recommendations': ['知識グラフが構築されていません。build_knowledge_graph()を実行してください']
            }
        
        # ノード数
        node_count = len(self.knowledge_graph)
        
        # エッジ数と平均接続数
        total_edges = sum(
            len(node['edges']) for node in self.knowledge_graph.values()
        )
        avg_connections = total_edges / node_count if node_count > 0 else 0
        
        # 孤立ノード（エッジがない）
        isolated_nodes = [
            node_id for node_id, node in self.knowledge_graph.items()
            if len(node['edges']) == 0
        ]
        
        # ハブノード（接続数が多い）
        hub_nodes = [
            (node_id, len(node['edges']))
            for node_id, node in self.knowledge_graph.items()
            if len(node['edges']) >= 5
        ]
        hub_nodes.sort(key=lambda x: x[1], reverse=True)
        
        # ヘルススコア
        health_score = min(1.0, (
            (node_count / 10) * 0.3 +
            min(1.0, avg_connections / 3) * 0.4 +
            (1.0 - len(isolated_nodes) / node_count if node_count > 0 else 0) * 0.3
        ))
        
        # 推奨事項
        recommendations = []
        
        if node_count < 5:
            recommendations.append("パターン数が少ないです。より多くの問題を記録してください")
        
        if avg_connections < 1.0:
            recommendations.append("ノード間の接続が少ないです。類似度閾値を調整してください")
        
        if len(isolated_nodes) > node_count * 0.3:
            recommendations.append(
                f"{len(isolated_nodes)}個の孤立ノードがあります。パターンの多様性を確認してください"
            )
        
        if not recommendations:
            recommendations.append("知識グラフは良好な状態です")
        
        return {
            'status': 'healthy' if health_score >= 0.7 else 'needs_improvement',
            'health_score': health_score,
            'node_count': node_count,
            'edge_count': total_edges // 2,  # 双方向エッジのため2で割る
            'avg_connections': avg_connections,
            'isolated_nodes_count': len(isolated_nodes),
            'hub_nodes': hub_nodes[:5],
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """テスト実行用のメイン関数"""
    print("=== KnowledgeGraphBuilder Test ===")
    print()
    
    builder = KnowledgeGraphBuilder()
    
    print("1. グラフ構築:")
    result = builder.build_knowledge_graph()
    print(f"   ノード数: {result['node_count']}")
    print(f"   エッジ数: {result['edge_count']}")
    print(f"   平均接続数: {result['avg_connections']:.2f}")
    print()
    
    print("2. システム診断:")
    diagnosis = builder.diagnose_knowledge_graph()
    print(f"   ヘルススコア: {diagnosis['health_score']:.2f}")
    print(f"   ステータス: {diagnosis['status']}")
    print(f"   推奨事項: {len(diagnosis['recommendations'])}件")
    print()
    
    print("✅ KnowledgeGraphBuilder テスト完了")


if __name__ == "__main__":
    main()
