# -*- coding: utf-8 -*-
"""
Naviko Plugin System - プラグインローダー

このモジュールは、プラグインの自動検出、動的ロード、登録を行う
PluginLoaderを提供します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

import os
import sys
import importlib.util
import inspect
from pathlib import Path
from typing import List, Optional, Type

from .base_plugin import BasePlugin, PluginStatus
from .plugin_types import PluginMetadata
from .universal_plugin_registry import UniversalPluginRegistry


class PluginLoader:
    """
    プラグインローダー
    
    指定されたディレクトリからプラグインを自動検出し、
    動的にロードしてUniversalPluginRegistryに登録します。
    
    Example:
        loader = PluginLoader()
        loader.load_plugins_from_directory("navikoLAB/plugins")
    """
    
    def __init__(self, registry: Optional[UniversalPluginRegistry] = None):
        """
        初期化
        
        Args:
            registry (Optional[UniversalPluginRegistry]): プラグインレジストリ
                                                           （None の場合はシングルトンを使用）
        """
        self._registry = registry or UniversalPluginRegistry.get_instance()
    
    def load_plugins_from_directory(self, directory_path: str, 
                                     recursive: bool = True,
                                     auto_initialize: bool = True) -> int:
        """
        指定されたディレクトリからプラグインをロード
        
        Args:
            directory_path (str): プラグインディレクトリのパス
            recursive (bool): サブディレクトリも再帰的に検索するか
            auto_initialize (bool): ロード後に自動でinitialize()を呼び出すか
        
        Returns:
            int: 成功したプラグイン数
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"⚠️  ディレクトリが存在しません: {directory_path}")
            return 0
        
        if not directory.is_dir():
            print(f"⚠️  パスがディレクトリではありません: {directory_path}")
            return 0
        
        print(f"🔍 プラグイン検索中: {directory_path}")
        
        # プラグインファイルを検索
        plugin_files = self._discover_plugin_files(directory, recursive)
        print(f"📝 検出されたファイル: {len(plugin_files)}件")
        
        loaded_count = 0
        
        for plugin_file in plugin_files:
            try:
                # モジュールをロード
                module = self._load_module_from_file(plugin_file)
                if module is None:
                    continue
                
                # BasePluginのサブクラスを検出
                plugin_classes = self._extract_plugin_classes(module)
                
                # 各プラグインクラスをインスタンス化・登録
                for plugin_class in plugin_classes:
                    if self._instantiate_and_register(plugin_class, auto_initialize):
                        loaded_count += 1
            
            except Exception as e:
                print(f"❌ プラグインロードエラー ({plugin_file.name}): {e}")
        
        print(f"✅ ロード成功: {loaded_count}/{len(plugin_files)} プラグイン")
        return loaded_count
    
    def _discover_plugin_files(self, directory: Path, recursive: bool) -> List[Path]:
        """
        プラグインファイル(.py)を検索
        
        Args:
            directory (Path): 検索対象ディレクトリ
            recursive (bool): 再帰検索するか
        
        Returns:
            List[Path]: プラグインファイルのリスト
        """
        plugin_files = []
        
        if recursive:
            # 再帰検索
            for py_file in directory.rglob("*.py"):
                # __init__.py と __pycache__ は除外
                if py_file.name == "__init__.py" or "__pycache__" in str(py_file):
                    continue
                plugin_files.append(py_file)
        else:
            # 直接子のみ
            for py_file in directory.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                plugin_files.append(py_file)
        
        return plugin_files
    
    def _load_module_from_file(self, file_path: Path) -> Optional[object]:
        """
        ファイルからPythonモジュールを動的ロード
        
        Args:
            file_path (Path): Pythonファイルのパス
        
        Returns:
            Optional[object]: ロードされたモジュール（失敗時は None）
        """
        try:
            # naviko-labのルートディレクトリをsys.pathに追加
            # プラグインファイルが navikoLAB.plugin_system をインポートできるようにする
            naviko_root = file_path.resolve().parents[3]  # naviko-lab/
            if str(naviko_root) not in sys.path:
                sys.path.insert(0, str(naviko_root))
            
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            
            if spec is None or spec.loader is None:
                print(f"⚠️  モジュールスペックが取得できません: {file_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            return module
        
        except Exception as e:
            print(f"⚠️  モジュールロードエラー ({file_path.name}): {e}")
            return None
    
    def _extract_plugin_classes(self, module: object) -> List[Type[BasePlugin]]:
        """
        モジュールからBasePluginのサブクラスを抽出
        
        Args:
            module (object): 検索対象モジュール
        
        Returns:
            List[Type[BasePlugin]]: プラグインクラスのリスト
        """
        plugin_classes = []
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # BasePluginのサブクラスかつBasePlugin自身ではない
            if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                # モジュール内で定義されたクラスのみ（インポートされたクラスは除外）
                if obj.__module__ == module.__name__:
                    plugin_classes.append(obj)
        
        return plugin_classes
    
    def _instantiate_and_register(self, plugin_class: Type[BasePlugin], 
                                    auto_initialize: bool) -> bool:
        """
        プラグインインスタンスを生成し、レジストリに登録
        
        Args:
            plugin_class (Type[BasePlugin]): プラグインクラス
            auto_initialize (bool): 自動初期化するか
        
        Returns:
            bool: 登録成功時 True
        """
        try:
            # プラグインインスタンス生成
            plugin = plugin_class()
            
            # メタデータ取得
            metadata_dict = plugin.get_metadata()
            metadata = PluginMetadata.from_dict(metadata_dict)
            
            # 既に登録されているかチェック
            if self._registry.is_plugin_registered(metadata.name):
                print(f"⚠️  プラグインは既に登録済み: {metadata.name}")
                return False
            
            # 自動初期化
            if auto_initialize:
                default_config = {}  # デフォルト設定
                if not plugin.initialize(default_config):
                    print(f"⚠️  プラグイン初期化失敗: {metadata.name}")
                    return False
            
            # レジストリに登録
            if self._registry.register_plugin(plugin, metadata):
                return True
            else:
                return False
        
        except Exception as e:
            print(f"❌ プラグインインスタンス化エラー ({plugin_class.__name__}): {e}")
            import traceback
            traceback.print_exc()
            return False


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["PluginLoader"]
