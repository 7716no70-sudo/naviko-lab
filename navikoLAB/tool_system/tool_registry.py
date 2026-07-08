# -*- coding: utf-8 -*-
"""
Naviko Tool System - ツールレジストリ

このモジュールは、ツールの登録・検索・管理を提供します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from typing import Dict, List, Optional, Callable, Any
from .tool_metadata import ToolMetadata, ToolCategory, ToolComplexity
import threading


class ToolRegistry:
    """
    ツールレジストリ（シングルトン）
    
    すべてのツールを一元管理するレジストリ。
    プラグインシステムのUniversalPluginRegistryと同様の設計パターン。
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        """初期化（直接呼び出し禁止、get_instance()を使用）"""
        if ToolRegistry._instance is not None:
            raise RuntimeError("ToolRegistryはシングルトンです。get_instance()を使用してください。")
        
        self._tools: Dict[str, Dict[str, Any]] = {}  # tool_name -> {metadata, function}
        self._category_index: Dict[str, List[str]] = {}  # category -> [tool_names]
        self._tag_index: Dict[str, List[str]] = {}  # tag -> [tool_names]
    
    @classmethod
    def get_instance(cls) -> "ToolRegistry":
        """シングルトンインスタンス取得"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def register_tool(
        self,
        metadata: ToolMetadata,
        function: Callable,
        force: bool = False
    ) -> bool:
        """
        ツールを登録
        
        Args:
            metadata (ToolMetadata): ツールメタデータ
            function (Callable): ツール実行関数
            force (bool): 既存ツールを上書きするか
        
        Returns:
            bool: 登録成功ならTrue
        """
        tool_name = metadata.name
        
        # 重複チェック
        if tool_name in self._tools and not force:
            print(f"⚠️ ツール '{tool_name}' は既に登録されています（force=True で上書き可能）")
            return False
        
        # ツール登録
        self._tools[tool_name] = {
            "metadata": metadata,
            "function": function
        }
        
        # カテゴリインデックス更新
        category_key = metadata.category.value
        if category_key not in self._category_index:
            self._category_index[category_key] = []
        if tool_name not in self._category_index[category_key]:
            self._category_index[category_key].append(tool_name)
        
        # タグインデックス更新
        for tag in metadata.tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = []
            if tool_name not in self._tag_index[tag]:
                self._tag_index[tag].append(tool_name)
        
        return True
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        ツール取得
        
        Args:
            tool_name (str): ツール名
        
        Returns:
            Optional[Dict[str, Any]]: ツール情報（metadata, function）
        """
        return self._tools.get(tool_name)
    
    def search_by_category(self, category: ToolCategory) -> List[ToolMetadata]:
        """
        カテゴリでツール検索
        
        Args:
            category (ToolCategory): 検索カテゴリ
        
        Returns:
            List[ToolMetadata]: マッチしたツールのメタデータリスト
        """
        tool_names = self._category_index.get(category.value, [])
        return [self._tools[name]["metadata"] for name in tool_names]
    
    def search_by_tag(self, tag: str) -> List[ToolMetadata]:
        """
        タグでツール検索
        
        Args:
            tag (str): 検索タグ
        
        Returns:
            List[ToolMetadata]: マッチしたツールのメタデータリスト
        """
        tool_names = self._tag_index.get(tag, [])
        return [self._tools[name]["metadata"] for name in tool_names]
    
    def search_by_complexity(self, complexity: ToolComplexity) -> List[ToolMetadata]:
        """
        複雑度でツール検索
        
        Args:
            complexity (ToolComplexity): 検索複雑度
        
        Returns:
            List[ToolMetadata]: マッチしたツールのメタデータリスト
        """
        results = []
        for tool_info in self._tools.values():
            if tool_info["metadata"].complexity == complexity:
                results.append(tool_info["metadata"])
        return results
    
    def execute_tool(self, tool_name: str, **params) -> Any:
        """
        ツール実行
        
        Args:
            tool_name (str): ツール名
            **params: ツールのパラメータ
        
        Returns:
            Any: ツールの実行結果
        
        Raises:
            ValueError: ツールが見つからない、パラメータ不正
            Exception: ツール実行エラー
        """
        tool_info = self.get_tool(tool_name)
        if tool_info is None:
            raise ValueError(f"ツール '{tool_name}' が見つかりません")
        
        metadata = tool_info["metadata"]
        function = tool_info["function"]
        
        # パラメータ検証
        valid, error = metadata.validate_params(params)
        if not valid:
            raise ValueError(f"パラメータエラー: {error}")
        
        # 実行
        try:
            return function(**params)
        except Exception as e:
            raise Exception(f"ツール '{tool_name}' 実行エラー: {e}")
    
    def list_all_tools(self) -> List[ToolMetadata]:
        """
        すべてのツールのメタデータを取得
        
        Returns:
            List[ToolMetadata]: すべてのツールメタデータ
        """
        return [tool_info["metadata"] for tool_info in self._tools.values()]
    
    def print_status(self):
        """レジストリ状態を表示"""
        print("\n" + "=" * 50)
        print("🔧 Naviko Tool Registry Status")
        print("=" * 50)
        print(f"Total tools: {len(self._tools)}")
        print()
        
        # カテゴリ別に表示
        for category_key, tool_names in sorted(self._category_index.items()):
            print(f"[{category_key}]: {len(tool_names)} tool(s)")
            for tool_name in tool_names:
                tool_info = self._tools[tool_name]
                metadata = tool_info["metadata"]
                print(f"  - {metadata.name} v{metadata.version}")
                print(f"    {metadata.description}")
        
        print("=" * 50)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        統計情報取得
        
        Returns:
            Dict[str, Any]: 統計情報
        """
        return {
            "total_tools": len(self._tools),
            "categories": {k: len(v) for k, v in self._category_index.items()},
            "tags": {k: len(v) for k, v in self._tag_index.items()},
            "complexity_distribution": {
                "simple": len(self.search_by_complexity(ToolComplexity.SIMPLE)),
                "moderate": len(self.search_by_complexity(ToolComplexity.MODERATE)),
                "complex": len(self.search_by_complexity(ToolComplexity.COMPLEX))
            }
        }


__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["ToolRegistry"]
