<<<<<<< Updated upstream
﻿"""Naviko GUI Plugin System
拡張可能なプラグイン式GUIアーキテクチャ
"""
=======
# -*- coding: utf-8 -*-
"""
Naviko GUI Plugin System

拡張可能なプラグイン式GUIアーキテクチャ。
キャラクター表示とチャット表示をプラグイン化し、
簡単に切り替え・拡張できる設計。

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

from .base import CharacterRenderer, ChatDisplay
from .registry import PluginRegistry, register_default_plugins
from .config_manager import ConfigManager

__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = [
    "CharacterRenderer",
    "ChatDisplay",
    "PluginRegistry",
    "ConfigManager",
    "register_default_plugins",
    "initialize_plugin_system",
]


def initialize_plugin_system() -> None:
    """
    プラグインシステムの初期化
    
    デフォルトプラグイン（DefaultSprite, Conversational）を登録します。
    Navikoシステム起動時に一度だけ呼び出してください。
    
    使用例:
        from navikoLAB.gui_plugins import initialize_plugin_system
        initialize_plugin_system()  # デフォルトプラグイン登録
    """
    register_default_plugins()
>>>>>>> Stashed changes
