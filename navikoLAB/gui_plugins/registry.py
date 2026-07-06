<<<<<<< Updated upstream
# -*- coding: utf-8 -*-
=======
# -*- coding: utf-8 -*-
>>>>>>> Stashed changes
"""
Naviko GUI Plugin System - プラグインレジストリ

このモジュールは、GUIプラグインの登録・取得を管理するPluginRegistryを提供します。
シングルトンパターンで実装され、アプリケーション全体で共有されます。

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

from typing import Dict, Type, Optional
from .base import CharacterRenderer, ChatDisplay


class PluginRegistry:
    """
    プラグインレジストリ（シングルトン）
    
    全てのキャラクターレンダラーとチャット表示プラグインを管理します。
    プラグインは型名（文字列）をキーとして登録・取得されます。
    
    使用例:
        # プラグイン登録
        registry = PluginRegistry.get_instance()
        registry.register_character_renderer("DefaultSprite", DefaultSpriteRenderer)
        registry.register_chat_display("Conversational", ConversationalChat)
        
        # プラグイン取得
        renderer_class = registry.get_character_renderer("DefaultSprite")
        chat_class = registry.get_chat_display("Conversational")
    """
    
    _instance: Optional['PluginRegistry'] = None
    
    def __init__(self):
        """
        プライベートコンストラクタ（シングルトンパターン）
        
        直接インスタンス化せず、get_instance()を使用してください。
        """
        if PluginRegistry._instance is not None:
            raise RuntimeError("PluginRegistry はシングルトンです。get_instance() を使用してください。")
        
        # プラグイン登録辞書
        self._character_renderers: Dict[str, Type[CharacterRenderer]] = {}
        self._chat_displays: Dict[str, Type[ChatDisplay]] = {}
        
        PluginRegistry._instance = self
    
    @staticmethod
    def get_instance() -> 'PluginRegistry':
        """
        PluginRegistry のシングルトンインスタンスを取得
        
        Returns:
            PluginRegistry: シングルトンインスタンス
        """
        if PluginRegistry._instance is None:
            PluginRegistry()
        return PluginRegistry._instance
    
    def register_character_renderer(self, plugin_type: str, renderer_class: Type[CharacterRenderer]) -> None:
        """
        キャラクターレンダラープラグインを登録
        
        Args:
            plugin_type (str): プラグイン型名（例: "DefaultSprite", "ThreeDModel"）
            renderer_class (Type[CharacterRenderer]): レンダラークラス
        
        Raises:
            ValueError: プラグイン型名が既に登録されている場合
            TypeError: renderer_class が CharacterRenderer のサブクラスでない場合
        
        Example:
            registry.register_character_renderer("DefaultSprite", DefaultSpriteRenderer)
        """
        if plugin_type in self._character_renderers:
            raise ValueError(f"キャラクターレンダラー '{plugin_type}' は既に登録されています。")
        
        if not issubclass(renderer_class, CharacterRenderer):
            raise TypeError(f"{renderer_class} は CharacterRenderer のサブクラスではありません。")
        
        self._character_renderers[plugin_type] = renderer_class
        print(f"✅ キャラクターレンダラー登録: {plugin_type} -> {renderer_class.__name__}")
    
    def register_chat_display(self, plugin_type: str, chat_class: Type[ChatDisplay]) -> None:
        """
        チャット表示プラグインを登録
        
        Args:
            plugin_type (str): プラグイン型名（例: "Conversational", "Novel", "RPG"）
            chat_class (Type[ChatDisplay]): チャット表示クラス
        
        Raises:
            ValueError: プラグイン型名が既に登録されている場合
            TypeError: chat_class が ChatDisplay のサブクラスでない場合
        
        Example:
            registry.register_chat_display("Conversational", ConversationalChat)
        """
        if plugin_type in self._chat_displays:
            raise ValueError(f"チャット表示プラグイン '{plugin_type}' は既に登録されています。")
        
        if not issubclass(chat_class, ChatDisplay):
            raise TypeError(f"{chat_class} は ChatDisplay のサブクラスではありません。")
        
        self._chat_displays[plugin_type] = chat_class
        print(f"✅ チャット表示プラグイン登録: {plugin_type} -> {chat_class.__name__}")
    
    def get_character_renderer(self, plugin_type: str) -> Type[CharacterRenderer]:
        """
        キャラクターレンダラープラグインを取得
        
        Args:
            plugin_type (str): プラグイン型名
        
        Returns:
            Type[CharacterRenderer]: レンダラークラス
        
        Raises:
            KeyError: 指定されたプラグイン型名が登録されていない場合
        
        Example:
            renderer_class = registry.get_character_renderer("DefaultSprite")
            renderer = renderer_class()
        """
        if plugin_type not in self._character_renderers:
            raise KeyError(
                f"キャラクターレンダラー '{plugin_type}' が見つかりません。\n"
                f"登録済みプラグイン: {list(self._character_renderers.keys())}"
            )
        return self._character_renderers[plugin_type]
    
    def get_chat_display(self, plugin_type: str) -> Type[ChatDisplay]:
        """
        チャット表示プラグインを取得
        
        Args:
            plugin_type (str): プラグイン型名
        
        Returns:
            Type[ChatDisplay]: チャット表示クラス
        
        Raises:
            KeyError: 指定されたプラグイン型名が登録されていない場合
        
        Example:
            chat_class = registry.get_chat_display("Conversational")
            chat = chat_class()
        """
        if plugin_type not in self._chat_displays:
            raise KeyError(
                f"チャット表示プラグイン '{plugin_type}' が見つかりません。\n"
                f"登録済みプラグイン: {list(self._chat_displays.keys())}"
            )
        return self._chat_displays[plugin_type]
    
    def list_character_renderers(self) -> list:
        """
        登録済みキャラクターレンダラーの一覧を取得
        
        Returns:
            list: プラグイン型名のリスト
        """
        return list(self._character_renderers.keys())
    
    def list_chat_displays(self) -> list:
        """
        登録済みチャット表示プラグインの一覧を取得
        
        Returns:
            list: プラグイン型名のリスト
        """
        return list(self._chat_displays.keys())
    
    def reset(self) -> None:
        """
        全てのプラグイン登録をクリア（テスト用）
        
        Warning:
            本番環境では使用しないでください。
        """
        self._character_renderers.clear()
        self._chat_displays.clear()
        print("⚠️  プラグインレジストリをリセットしました。")


<<<<<<< Updated upstream
# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["PluginRegistry"]
=======
def register_default_plugins() -> None:
    """
    デフォルトプラグインを登録
    
    DefaultSpriteRenderer と ConversationalChat を自動登録します。
    Navikoシステム起動時に一度だけ呼び出してください。
    """
    from .renderers.default_sprite import DefaultSpriteRenderer
    from .chat_displays.conversational import ConversationalChat
    
    registry = PluginRegistry.get_instance()
    
    # デフォルトプラグイン登録
    try:
        registry.register_character_renderer("DefaultSprite", DefaultSpriteRenderer)
    except ValueError:
        # 既に登録済みの場合はスキップ
        pass
    
    try:
        registry.register_chat_display("Conversational", ConversationalChat)
    except ValueError:
        # 既に登録済みの場合はスキップ
        pass
    
    print("📦 デフォルトプラグイン登録完了")
    print(f"   - キャラクターレンダラー: {registry.list_character_renderers()}")
    print(f"   - チャット表示: {registry.list_chat_displays()}")


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["PluginRegistry", "register_default_plugins"]
>>>>>>> Stashed changes
