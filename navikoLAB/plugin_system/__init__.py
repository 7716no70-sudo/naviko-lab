# -*- coding: utf-8 -*-
"""
Naviko Plugin System

汎用プラグインシステムパッケージ

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from .base_plugin import BasePlugin, PluginStatus
from .plugin_types import PluginType, PluginMetadata
from .universal_plugin_registry import UniversalPluginRegistry
# plugin_loaderは循環インポートを避けるため、直接インポートする
# from .plugin_loader import PluginLoader

__version__ = "1.0.0"
__author__ = "Naviko Development Team"

__all__ = [
    "BasePlugin",
    "PluginStatus",
    "PluginType",
    "PluginMetadata",
    "UniversalPluginRegistry",
    # "PluginLoader",  # 循環インポートを避けるためコメントアウト
]
