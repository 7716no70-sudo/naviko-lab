# -*- coding: utf-8 -*-
"""
Naviko Plugin System - 汎用プラグインレジストリ

このモジュールは、全てのプラグインの登録・管理を行うUniversalPluginRegistryを提供します。
シングルトンパターンで実装され、アプリケーション全体で共有されます。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from typing import Dict, List, Type, Optional, Set
from .base_plugin import BasePlugin, PluginStatus
from .plugin_types import PluginType, PluginMetadata


class UniversalPluginRegistry:
    """
    汎用プラグインレジストリ（シングルトン）
    
    全てのNavikoプラグインを一元管理します。
    タイプ別の登録、依存関係の解決、優先度順のソート、検索機能を提供します。
    
    Attributes:
        _instance: シングルトンインスタンス
        _plugins: プラグインインスタンスの辞書 {plugin_name: plugin_instance}
        _metadata: プラグインメタデータの辞書 {plugin_name: PluginMetadata}
        _type_index: タイプ別インデックス {PluginType: Set[plugin_name]}
    
    Example:
        # プラグイン登録
        registry = UniversalPluginRegistry.get_instance()
        plugin = MyVoicePlugin()
        metadata = PluginMetadata(
            name="MyVoicePlugin",
            version="1.0.0",
            plugin_type=PluginType.VOICE,
            author="Me",
            description="My voice plugin"
        )
        registry.register_plugin(plugin, metadata)
        
        # プラグイン取得
        voice_plugins = registry.get_plugins_by_type(PluginType.VOICE)
    """
    
    _instance: Optional['UniversalPluginRegistry'] = None
    
    def __init__(self):
        """
        プライベートコンストラクタ（シングルトンパターン）
        
        直接インスタンス化せず、get_instance()を使用してください。
        """
        if UniversalPluginRegistry._instance is not None:
            raise RuntimeError(
                "UniversalPluginRegistry はシングルトンです。"
                "get_instance() を使用してください。"
            )
        
        # プラグイン登録ストレージ
        self._plugins: Dict[str, BasePlugin] = {}
        self._metadata: Dict[str, PluginMetadata] = {}
        self._type_index: Dict[PluginType, Set[str]] = {
            plugin_type: set() for plugin_type in PluginType
        }
        
        UniversalPluginRegistry._instance = self
    
    @staticmethod
    def get_instance() -> 'UniversalPluginRegistry':
        """
        シングルトンインスタンスを取得
        
        Returns:
            UniversalPluginRegistry: シングルトンインスタンス
        """
        if UniversalPluginRegistry._instance is None:
            UniversalPluginRegistry()
        return UniversalPluginRegistry._instance
    
    def register_plugin(self, plugin: BasePlugin, metadata: PluginMetadata) -> bool:
        """
        プラグインを登録
        
        Args:
            plugin (BasePlugin): プラグインインスタンス
            metadata (PluginMetadata): プラグインメタデータ
        
        Returns:
            bool: 登録成功時 True、失敗時 False
        
        Raises:
            ValueError: プラグイン名が既に登録されている場合
            TypeError: plugin が BasePlugin のサブクラスでない場合
        """
        plugin_name = metadata.name
        
        # 重複チェック
        if plugin_name in self._plugins:
            raise ValueError(f"プラグイン '{plugin_name}' は既に登録されています。")
        
        # 型チェック
        if not isinstance(plugin, BasePlugin):
            raise TypeError(
                f"{type(plugin).__name__} は BasePlugin のサブクラスではありません。"
            )
        
        # 依存関係チェック
        if not self._check_dependencies(metadata):
            print(f"⚠️  警告: プラグイン '{plugin_name}' の依存関係が満たされていません。")
            print(f"   必要な依存: {metadata.dependencies}")
            print(f"   現在登録済み: {list(self._plugins.keys())}")
            return False
        
        # 登録
        self._plugins[plugin_name] = plugin
        self._metadata[plugin_name] = metadata
        self._type_index[metadata.plugin_type].add(plugin_name)
        
        print(f"✅ プラグイン登録: {plugin_name} (type: {metadata.plugin_type.value}, priority: {metadata.priority})")
        return True
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを登録解除
        
        Args:
            plugin_name (str): プラグイン名
        
        Returns:
            bool: 解除成功時 True、失敗時 False
        """
        if plugin_name not in self._plugins:
            print(f"⚠️  プラグイン '{plugin_name}' は登録されていません。")
            return False
        
        # cleanup() を呼び出してリソース解放
        plugin = self._plugins[plugin_name]
        try:
            plugin.cleanup()
        except Exception as e:
            print(f"⚠️  プラグイン '{plugin_name}' のcleanup中にエラー: {e}")
        
        # 登録解除
        metadata = self._metadata[plugin_name]
        self._type_index[metadata.plugin_type].discard(plugin_name)
        del self._plugins[plugin_name]
        del self._metadata[plugin_name]
        
        print(f"🗑️  プラグイン登録解除: {plugin_name}")
        return True
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        プラグインインスタンスを取得
        
        Args:
            plugin_name (str): プラグイン名
        
        Returns:
            Optional[BasePlugin]: プラグインインスタンス（未登録の場合は None）
        """
        return self._plugins.get(plugin_name)
    
    def get_metadata(self, plugin_name: str) -> Optional[PluginMetadata]:
        """
        プラグインメタデータを取得
        
        Args:
            plugin_name (str): プラグイン名
        
        Returns:
            Optional[PluginMetadata]: プラグインメタデータ（未登録の場合は None）
        """
        return self._metadata.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: PluginType, 
                            sorted_by_priority: bool = True) -> List[BasePlugin]:
        """
        指定されたタイプのプラグイン一覧を取得
        
        Args:
            plugin_type (PluginType): プラグインタイプ
            sorted_by_priority (bool): 優先度順にソートするか（デフォルト: True）
        
        Returns:
            List[BasePlugin]: プラグインインスタンスのリスト
        """
        plugin_names = self._type_index.get(plugin_type, set())
        plugins = [self._plugins[name] for name in plugin_names if name in self._plugins]
        
        if sorted_by_priority:
            # 優先度が高い順にソート（降順）
            plugins.sort(
                key=lambda p: self._metadata[self._get_plugin_name(p)].priority,
                reverse=True
            )
        
        return plugins
    
    def get_all_plugins(self, sorted_by_priority: bool = False) -> List[BasePlugin]:
        """
        全てのプラグインを取得
        
        Args:
            sorted_by_priority (bool): 優先度順にソートするか（デフォルト: False）
        
        Returns:
            List[BasePlugin]: プラグインインスタンスのリスト
        """
        plugins = list(self._plugins.values())
        
        if sorted_by_priority:
            plugins.sort(
                key=lambda p: self._metadata[self._get_plugin_name(p)].priority,
                reverse=True
            )
        
        return plugins
    
    def find_plugins_by_tag(self, tag: str) -> List[BasePlugin]:
        """
        タグで検索してプラグインを取得
        
        Args:
            tag (str): 検索タグ
        
        Returns:
            List[BasePlugin]: マッチしたプラグインのリスト
        """
        matched_plugins = []
        for plugin_name, metadata in self._metadata.items():
            if metadata.matches_tag(tag):
                matched_plugins.append(self._plugins[plugin_name])
        return matched_plugins
    
    def is_plugin_registered(self, plugin_name: str) -> bool:
        """
        プラグインが登録されているか確認
        
        Args:
            plugin_name (str): プラグイン名
        
        Returns:
            bool: 登録されている場合 True
        """
        return plugin_name in self._plugins
    
    def list_plugin_names(self, plugin_type: Optional[PluginType] = None) -> List[str]:
        """
        登録されているプラグイン名の一覧を取得
        
        Args:
            plugin_type (Optional[PluginType]): フィルタリングするプラグインタイプ
                                                 （None の場合は全タイプ）
        
        Returns:
            List[str]: プラグイン名のリスト
        """
        if plugin_type is None:
            return list(self._plugins.keys())
        else:
            return list(self._type_index.get(plugin_type, set()))
    
    def get_plugin_count(self, plugin_type: Optional[PluginType] = None) -> int:
        """
        登録されているプラグイン数を取得
        
        Args:
            plugin_type (Optional[PluginType]): フィルタリングするプラグインタイプ
        
        Returns:
            int: プラグイン数
        """
        if plugin_type is None:
            return len(self._plugins)
        else:
            return len(self._type_index.get(plugin_type, set()))
    
    def clear(self) -> None:
        """
        全てのプラグインを登録解除（テスト用）
        
        Warning:
            本番環境では使用しないでください。
        """
        # 全プラグインのcleanupを呼び出し
        for plugin in self._plugins.values():
            try:
                plugin.cleanup()
            except Exception as e:
                print(f"⚠️  cleanup中にエラー: {e}")
        
        self._plugins.clear()
        self._metadata.clear()
        for plugin_type in PluginType:
            self._type_index[plugin_type].clear()
        
        print("⚠️  プラグインレジストリをクリアしました。")
    
    def print_status(self) -> None:
        """
        プラグインレジストリの状態を表示（デバッグ用）
        """
        print("\n=" * 50)
        print("📦 Naviko Plugin Registry Status")
        print("=" * 50)
        print(f"Total plugins: {len(self._plugins)}")
        print()
        
        for plugin_type in PluginType:
            count = len(self._type_index[plugin_type])
            if count > 0:
                print(f"[{plugin_type.value}]: {count} plugin(s)")
                for plugin_name in self._type_index[plugin_type]:
                    metadata = self._metadata[plugin_name]
                    plugin = self._plugins[plugin_name]
                    status = plugin.get_status()
                    print(f"  - {plugin_name} v{metadata.version} [{status.value}]")
                print()
        
        print("=" * 50)
    
    # ============================================================
    # プライベートメソッド
    # ============================================================
    
    def _check_dependencies(self, metadata: PluginMetadata) -> bool:
        """
        プラグインの依存関係をチェック
        
        Args:
            metadata (PluginMetadata): チェック対象のメタデータ
        
        Returns:
            bool: 全ての依存関係が満たされている場合 True
        """
        for dep_name in metadata.dependencies:
            if dep_name not in self._plugins:
                return False
        return True
    
    def _get_plugin_name(self, plugin: BasePlugin) -> str:
        """
        プラグインインスタンスから名前を取得
        
        Args:
            plugin (BasePlugin): プラグインインスタンス
        
        Returns:
            str: プラグイン名
        """
        for name, p in self._plugins.items():
            if p is plugin:
                return name
        return "Unknown"


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["UniversalPluginRegistry"]
