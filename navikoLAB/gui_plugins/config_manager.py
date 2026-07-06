# -*- coding: utf-8 -*-
"""
Naviko GUI Plugin System - 設定ファイル管理

このモジュールは、gui_config.jsonの読み込み・保存・デフォルト設定生成を管理します。

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

import json
import os
from typing import Dict, Any


class ConfigManager:
    """
    GUI設定ファイル管理クラス
    
    gui_config.jsonの読み込み・保存・デフォルト設定生成を提供します。
    
    使用例:
        config_manager = ConfigManager("/path/to/naviko-lab")
        config = config_manager.load_config()
        
        # プラグイン設定の取得
        renderer_type = config["character_renderer"]["type"]
        chat_type = config["chat_display"]["type"]
    """
    
    def __init__(self, base_dir: str):
        """
        ConfigManagerの初期化
        
        Args:
            base_dir (str): プロジェクトベースディレクトリ（gui_config.jsonが配置されるディレクトリ）
        """
        self.base_dir = base_dir
        self.config_file = os.path.join(base_dir, "gui_config.json")
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        デフォルト設定を取得
        
        Returns:
            Dict[str, Any]: デフォルト設定辞書
        
        Note:
            gui_config.jsonが存在しない場合、この設定が使用されます。
        """
        return {
            "character_renderer": {
                "type": "DefaultSprite",
                "config": {
                    "sprite_dir": "character_sprites/",
                    "default_emotion": "neutral",
                    "emotions": ["neutral", "happy", "sad", "angry", "surprised"],
                    "image_format": "png"
                }
            },
            "chat_display": {
                "type": "Conversational",
                "config": {
                    "font_size": 12,
                    "font_family": "Yu Gothic UI",
                    "colors": {
                        "user_bg": "#E3F2FD",
                        "user_fg": "#0D47A1",
                        "ai_bg": "#F3E5F5",
                        "ai_fg": "#4A148C",
                        "border": "#BDBDBD"
                    },
                    "padding": 10,
                    "message_spacing": 5
                }
            },
            "layout": {
                "window_size": [1200, 800],
                "character_area_width": 400,
                "chat_area_width": 800,
                "min_window_size": [800, 600]
            },
            "system": {
                "auto_save_config": True,
                "plugin_reload_on_change": False,
                "debug_mode": False
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """
        設定ファイルを読み込み
        
        Returns:
            Dict[str, Any]: 設定辞書
        
        Note:
            ファイルが存在しない場合、デフォルト設定を生成して保存します。
        
        Raises:
            json.JSONDecodeError: JSONファイルの解析に失敗した場合
        """
        if not os.path.exists(self.config_file):
            print(f"⚠️  設定ファイルが見つかりません: {self.config_file}")
            print("📝 デフォルト設定を生成します...")
            default_config = self.get_default_config()
            self.save_config(default_config)
            return default_config
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            print(f"✅ 設定ファイルを読み込みました: {self.config_file}")
            return config
        except json.JSONDecodeError as e:
            print(f"❌ 設定ファイルの解析に失敗しました: {e}")
            print("📝 デフォルト設定を使用します...")
            return self.get_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """
        設定ファイルを保存
        
        Args:
            config (Dict[str, Any]): 保存する設定辞書
        
        Raises:
            IOError: ファイル書き込みに失敗した場合
        """
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ 設定ファイルを保存しました: {self.config_file}")
        except IOError as e:
            print(f"❌ 設定ファイルの保存に失敗しました: {e}")
            raise
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        設定の妥当性を検証
        
        Args:
            config (Dict[str, Any]): 検証する設定辞書
        
        Returns:
            bool: 設定が妥当な場合True、不正な場合False
        
        Note:
            必須キーの存在確認、型チェックを行います。
        """
        required_keys = ["character_renderer", "chat_display", "layout"]
        
        for key in required_keys:
            if key not in config:
                print(f"❌ 必須キー '{key}' が設定に含まれていません。")
                return False
        
        # character_rendererの検証
        if "type" not in config["character_renderer"]:
            print("❌ character_renderer.type が設定されていません。")
            return False
        
        # chat_displayの検証
        if "type" not in config["chat_display"]:
            print("❌ chat_display.type が設定されていません。")
            return False
        
        # layoutの検証
        if "window_size" not in config["layout"]:
            print("❌ layout.window_size が設定されていません。")
            return False
        
        print("✅ 設定の検証に成功しました。")
        return True
    
    def update_config(self, path: str, value: Any) -> None:
        """
        設定の一部を更新
        
        Args:
            path (str): 更新するキーのパス（ドット区切り、例: "chat_display.config.font_size"）
            value (Any): 新しい値
        
        Example:
            config_manager.update_config("chat_display.config.font_size", 14)
        """
        config = self.load_config()
        
        # パスを分解
        keys = path.split(".")
        current = config
        
        # 最後のキーまで辿る
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 値を設定
        current[keys[-1]] = value
        
        # 保存
        self.save_config(config)
        print(f"✅ 設定を更新しました: {path} = {value}")


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["ConfigManager"]
