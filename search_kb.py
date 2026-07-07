#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知識ベース検索スクリプト
Naviko Knowledge Base Search Tool
"""

import os
import re
from typing import List, Dict, Optional

class KnowledgeBaseSearch:
    """知識ベース検索クラス"""
    
    def __init__(self, kb_root: str = "docs/knowledge_base"):
        self.kb_root = kb_root
    
    def search(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        知識ベースを検索
        
        Args:
            query: 検索キーワード
            category: カテゴリ（phases/errors/rules/guides）
        
        Returns:
            検索結果リスト
        """
        results = []
        search_dir = self.kb_root
        
        if category:
            search_dir = os.path.join(self.kb_root, category)
        
        # ディレクトリが存在しない場合
        if not os.path.exists(search_dir):
            return results
        
        # Markdownファイルを検索
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 大文字小文字を区別しない検索
                    if query.lower() in content.lower():
                        results.append({
                            'path': path,
                            'file': file,
                            'category': os.path.basename(root),
                            'preview': self._extract_preview(content, query)
                        })
        
        return results
    
    def _extract_preview(self, content: str, query: str, context_lines: int = 3) -> str:
        """検索キーワード周辺のプレビューを抽出"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                preview = '\n'.join(lines[start:end])
                return preview[:300] + '...' if len(preview) > 300 else preview
        
        # 見つからない場合は最初の200文字
        return content[:200] + '...'
    
    def list_categories(self) -> List[str]:
        """カテゴリ一覧を取得"""
        categories = []
        
        if os.path.exists(self.kb_root):
            for item in os.listdir(self.kb_root):
                path = os.path.join(self.kb_root, item)
                if os.path.isdir(path) and not item.startswith('.'):
                    categories.append(item)
        
        return sorted(categories)
    
    def list_files(self, category: Optional[str] = None) -> List[str]:
        """ファイル一覧を取得"""
        files = []
        search_dir = self.kb_root
        
        if category:
            search_dir = os.path.join(self.kb_root, category)
        
        if os.path.exists(search_dir):
            for root, dirs, filenames in os.walk(search_dir):
                for filename in filenames:
                    if filename.endswith('.md') and filename != 'README.md':
                        rel_path = os.path.relpath(os.path.join(root, filename), self.kb_root)
                        files.append(rel_path)
        
        return sorted(files)

def search_kb(query: str, category: Optional[str] = None) -> List[Dict]:
    """
    知識ベース検索のショートカット関数
    
    Args:
        query: 検索キーワード
        category: カテゴリ（phases/errors/rules/guides）
    
    Returns:
        検索結果リスト
    """
    kb = KnowledgeBaseSearch()
    return kb.search(query, category)

# CLI実行用
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search_kb.py <query> [category]")
        print("Example: python search_kb.py 'Git同期エラー'")
        print("Example: python search_kb.py 'Phase D-2' phases")
        sys.exit(1)
    
    query = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    
    kb = KnowledgeBaseSearch()
    results = kb.search(query, category)
    
    if results:
        print(f"\n🔍 検索結果: {len(results)}件")
        print("=" * 70)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['file']}")
            print(f"   📁 カテゴリ: {result['category']}")
            print(f"   📄 パス: {result['path']}")
            print(f"   📝 プレビュー:\n{result['preview']}")
            print("-" * 70)
    else:
        print(f"\n❌ '{query}' に一致する結果が見つかりませんでした")
        print("\n💡 ヒント:")
        print("  - 別のキーワードを試してください")
        print("  - カテゴリを指定してみてください（phases/errors/rules/guides）")
