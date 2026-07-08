# -*- coding: utf-8 -*-
"""
Naviko Plugin System

プラグインシステムのパッケージ

Author: Naviko Development Team
Version: 1.0.0
"""

from .base_plugin import BasePlugin, PluginStatus
from .plugin_types import PluginType
from .universal_plugin_registry import UniversalPluginRegistry
from .plugin_loader import PluginLoader

__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = [
    "BasePlugin",
    "PluginType",
    "PluginStatus",
    "UniversalPluginRegistry",
    "PluginLoader"
]
