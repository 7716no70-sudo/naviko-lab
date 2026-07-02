# -*- coding: utf-8 -*-
"""
DeepSearchEngine - ChatGPT風ディープサーチ機能

複雑な質問を分解し、複数のLLMで並列実行して包括的な回答を生成。
反復的な深掘りと信頼性評価で高品質な情報を提供。

Author: Naviko LAB
Date: 2026-07-02
Version: 1.0.0
"""

import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import concurrent.futures
from collections import defaultdict


class DeepSearchEngine:
    """
    ChatGPT風ディープサーチエンジン
    
    クエリ分解、並列実行、結果統合、反復深化を実装。
    完全な調査レポートを生成。
    """
    
    def __init__(self, connector):
        """
        初期化
        
        Args:
            connector: UniversalLLMConnector インスタンス
        """
        self.connector = connector
        self.search_history = []
    
    def search(
        self,
        query: str,
        depth: int = 2,
        use_parallel: bool = True,
        providers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        ディープサーチ実行
        
        Args:
            query: 検索クエリ
            depth: 深掘りの深さ（1-3推奨）
            use_parallel: 並列実行を使用するか
            providers: 使用するプロバイダーリスト（Noneで全て）
        
        Returns:
            {
                "success": bool,
                "query": str,
                "depth": int,
                "rounds": List[Dict],  # 各ラウンドの結果
                "final_answer": str,
                "confidence_score": float,
                "sources": List[str],
                "execution_time": float
            }
        """
        print("")
        print("🔍 ディープサーチ開始")
        print("")
        print("="*60)
        print(f"📝 クエリ: {query}")
        print(f"🔢 深さ: {depth}ラウンド")
        print(f"⚡ 並列実行: {'ON' if use_parallel else 'OFF'}")
        print("="*60)
        
        start_time = time.time()
        
        # 使用可能なプロバイダー取得
        if providers is None:
            providers = self.connector.get_available_providers()
            if not providers:
                providers = ["template"]  # フォールバック
        
        provider_list = ', '.join(providers)
        print(f"\n🎯 使用プロバイダー: {provider_list}")
        
        rounds = []
        current_query = query
        all_insights = []
        
        # 反復深化
        for round_num in range(1, depth + 1):
            separator = "=" * 60
            print(f"\n{separator}")
            print(f"🔄 ラウンド {round_num}/{depth}")
            print(separator)
            
            # ステップ1: クエリ分解
            sub_queries = self._decompose_query(current_query, round_num)
            print(f"\n📋 サブクエリ生成: {len(sub_queries)}個")
            for i, sq in enumerate(sub_queries, 1):
                print(f"  {i}. {sq}")
            
            # ステップ2: 並列実行
            print("\n⚡ 実行中...")
            if use_parallel and len(providers) > 1:
                results = self._parallel_search(sub_queries, providers)
            else:
                results = self._sequential_search(sub_queries, providers)
            
            # ステップ3: 結果統合
            print("\n🔄 結果統合中...")
            synthesis = self._synthesize_results(results, current_query)
            
            rounds.append({
                "round": round_num,
                "query": current_query,
                "sub_queries": sub_queries,
                "results": results,
                "synthesis": synthesis
            })
            
            all_insights.append(synthesis["answer"])
            
            print(f"\n✅ ラウンド {round_num} 完了")
            print(f"   信頼度: {synthesis['confidence']:.1%}")
            print(f"   ソース: {', '.join(synthesis['sources'])}")
            
            # 次のラウンドの質問生成
            if round_num < depth:
                current_query = self._generate_followup_query(
                    query, synthesis["answer"]
                )
                print(f"\n🔍 次の深掘り質問: {current_query}")
        
        # 最終統合
        final_separator = "=" * 60
        print(f"\n{final_separator}")
        print("📊 最終統合中...")
        print(final_separator)
        
        final_answer = self._create_final_answer(query, rounds)
        confidence_score = self._calculate_confidence(rounds)
        sources = self._collect_sources(rounds)
        
        elapsed = time.time() - start_time
        
        result = {
            "success": True,
            "query": query,
            "depth": depth,
            "rounds": rounds,
            "final_answer": final_answer,
            "confidence_score": confidence_score,
            "sources": sources,
            "execution_time": elapsed,
            "timestamp": datetime.now().isoformat()
        }
        
        # 履歴保存
        self.search_history.append(result)
        
        print("\n✅ ディープサーチ完了")
        print(f"   実行時間: {elapsed:.2f}秒")
        print(f"   信頼度スコア: {confidence_score:.1%}")
        print(f"   情報源: {len(sources)}個のプロバイダー")
        
        return result
    
    def _decompose_query(self, query: str, round_num: int) -> List[str]:
        """クエリを3-5個のサブクエリに分解"""
        if round_num == 1:
            decomposition_prompt = f"""次の質問を3-5個の具体的なサブクエリに分解してください。

質問: {query}

各サブクエリは独立して答えられるようにし、全体として元の質問を包括的にカバーしてください。
サブクエリのみを番号付きリストで出力してください（説明不要）。
"""
        else:
            decomposition_prompt = f"""次の質問について、さらに深い理解のための追加質問を3個生成してください。

元の質問: {query}

前回の回答では基本的な観点をカバーしました。
今回は、より高度な観点、実践的な応用、注意点などに焦点を当ててください。
質問のみを番号付きリストで出力してください（説明不要）。
"""
        
        try:
            result = self.connector.generate_code(
                prompt=decomposition_prompt,
                max_tokens=500
            )
            
            if result["success"]:
                text = result["code"]
                sub_queries = []
                
                for line in text.split('\n'):
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                        cleaned = line.lstrip('0123456789.-*) ').strip()
                        if cleaned and len(cleaned) > 10:
                            sub_queries.append(cleaned)
                
                if sub_queries:
                    return sub_queries[:5]
        
        except Exception as e:
            print(f"⚠️ クエリ分解失敗: {e}")
        
        # フォールバック
        if round_num == 1:
            return [
                f"{query}の基本的な概念と定義は何ですか？",
                f"{query}の主な特徴や利点は何ですか？",
                f"{query}の実践的な使用例を教えてください。"
            ]
        else:
            return [
                f"{query}のベストプラクティスは何ですか？",
                f"{query}でよくある落とし穴や注意点は何ですか？",
                f"{query}の将来の展望はどうですか？"
            ]
    
    def _parallel_search(self, queries: List[str], providers: List[str]) -> List[Dict[str, Any]]:
        """複数のクエリを並列実行"""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_query = {}
            for i, query in enumerate(queries):
                provider = providers[i % len(providers)]
                future = executor.submit(self._execute_single_query, query, provider)
                future_to_query[future] = query
            
            for future in concurrent.futures.as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                    query_preview = query[:50] + "..." if len(query) > 50 else query
                    print(f"  ✅ 完了: {query_preview}")
                except Exception as e:
                    query_preview = query[:50] + "..." if len(query) > 50 else query
                    print(f"  ❌ 失敗: {query_preview} - {e}")
                    results.append({
                        "query": query,
                        "answer": f"エラー: {str(e)}",
                        "provider": "none",
                        "success": False
                    })
        return results
    
    def _sequential_search(self, queries: List[str], providers: List[str]) -> List[Dict[str, Any]]:
        """複数のクエリを順次実行"""
        results = []
        for i, query in enumerate(queries):
            provider = providers[i % len(providers)]
            result = self._execute_single_query(query, provider)
            results.append(result)
            query_preview = query[:50] + "..." if len(query) > 50 else query
            print(f"  ✅ 完了 ({i+1}/{len(queries)}): {query_preview}")
        return results
    
    def _execute_single_query(self, query: str, provider: str) -> Dict[str, Any]:
        """単一クエリを実行"""
        try:
            result = self.connector.generate_code(
                prompt=query,
                provider=provider,
                max_tokens=1000
            )
            return {
                "query": query,
                "answer": result.get("code", ""),
                "provider": result.get("provider", provider),
                "mode": result.get("mode", "unknown"),
                "success": result.get("success", False)
            }
        except Exception as e:
            return {
                "query": query,
                "answer": f"エラー: {str(e)}",
                "provider": "none",
                "success": False
            }
    
    def _synthesize_results(self, results: List[Dict[str, Any]], original_query: str) -> Dict[str, Any]:
        """複数の結果を統合"""
        valid_results = [r for r in results if r.get("success", False)]
        if not valid_results:
            return {
                "answer": "情報を取得できませんでした。",
                "confidence": 0.0,
                "sources": []
            }
        
        combined_parts = []
        for r in valid_results:
            combined_parts.append(f"【{r['provider']}からの情報】\n{r['answer']}")
        combined_answers = "\n\n".join(combined_parts)
        
        synthesis_prompt = f"""以下は「{original_query}」という質問に対する複数の情報源からの回答です。
これらを統合して、包括的で正確な回答を作成してください。

{combined_answers}

統合回答:
"""
        
        try:
            synthesis_result = self.connector.generate_code(
                prompt=synthesis_prompt,
                max_tokens=1500
            )
            if synthesis_result["success"]:
                answer = synthesis_result["code"]
            else:
                answer = valid_results[0]["answer"]
        except:
            answer = valid_results[0]["answer"]
        
        confidence = len(valid_results) / len(results) if results else 0.0
        sources = list(set([r["provider"] for r in valid_results]))
        
        return {
            "answer": answer,
            "confidence": confidence,
            "sources": sources
        }
    
    def _generate_followup_query(self, original_query: str, previous_answer: str) -> str:
        """追加の深掘り質問を生成"""
        answer_preview = previous_answer[:500] + "..." if len(previous_answer) > 500 else previous_answer
        
        prompt = f"""元の質問: {original_query}

前回の回答:
{answer_preview}

この情報を踏まえて、さらに深く理解するための追加質問を1つ生成してください。
より実践的、応用的、または高度な観点からの質問にしてください。
質問のみを出力してください（説明不要）。
"""
        
        try:
            result = self.connector.generate_code(prompt=prompt, max_tokens=200)
            if result["success"]:
                text = result["code"].strip()
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                if lines:
                    return lines[0].lstrip('0123456789.-*) ').strip()
        except:
            pass
        
        return f"{original_query}の実践的な応用例とベストプラクティス"
    
    def _create_final_answer(self, query: str, rounds: List[Dict[str, Any]]) -> str:
        """最終的な包括的回答を生成"""
        insights = []
        for r in rounds:
            synthesis = r.get("synthesis", {})
            answer = synthesis.get("answer", "")
            if answer:
                insights.append(f"【ラウンド{r['round']}】\n{answer}")
        
        if not insights:
            return "十分な情報を収集できませんでした。"
        
        all_insights = "\n\n".join(insights)
        final_prompt = f"""以下は「{query}」という質問に対する段階的な調査結果です。
これらすべてを統合して、包括的で構造化された最終回答を作成してください。

{all_insights}

最終回答（要点を箇条書きで整理）:
"""
        
        try:
            result = self.connector.generate_code(prompt=final_prompt, max_tokens=2000)
            if result["success"]:
                return result["code"]
        except:
            pass
        
        # フォールバック: 最後のラウンドの回答を返す
        return rounds[-1]["synthesis"]["answer"]
    
    def _calculate_confidence(self, rounds: List[Dict[str, Any]]) -> float:
        """全体の信頼度スコアを計算"""
        if not rounds:
            return 0.0
        
        confidences = []
        for r in rounds:
            if "synthesis" in r:
                confidences.append(r["synthesis"]["confidence"])
        
        if not confidences:
            return 0.0
        
        return sum(confidences) / len(confidences)
    
    def _collect_sources(self, rounds: List[Dict[str, Any]]) -> List[str]:
        """すべてのラウンドから情報源を収集"""
        sources = set()
        for r in rounds:
            synthesis = r.get("synthesis", {})
            round_sources = synthesis.get("sources", [])
            sources.update(round_sources)
        return sorted(list(sources))
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """検索結果を見やすくフォーマット"""
        lines = []
        lines.append("\n" + "="*60)
        lines.append("🔍 ディープサーチ結果")
        lines.append("="*60)
        lines.append(f"\n📝 クエリ: {result['query']}")
        lines.append(f"🔢 深さ: {result['depth']}ラウンド")
        lines.append(f"⏱️  実行時間: {result['execution_time']:.2f}秒")
        lines.append(f"📊 信頼度: {result['confidence_score']:.1%}")
        lines.append(f"🎯 情報源: {', '.join(result['sources'])}")
        lines.append("\n" + "-"*60)
        lines.append("📖 最終回答")
        lines.append("-"*60)
        lines.append(result['final_answer'])
        lines.append("\n" + "="*60)
        return "\n".join(lines)


print("✅ DeepSearchEngine クラス定義完了")
print("   - クエリ分解")
print("   - 並列実行")
print("   - 結果統合")
print("   - 反復深化")
print("   - 信頼性評価")
print("   - ソース追跡")
