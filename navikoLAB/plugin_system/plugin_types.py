# -*- coding: utf-8 -*-
"""
Naviko Plugin System - プラグインタイプ定義

このモジュールは、Navikoプラグインシステムのプラグインタイプと
メタデータクラスを定義します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class PluginType(Enum):
    """
    プラグインタイプ列挙
    
    Navikoプラグインシステムでサポートされるプラグインタイプ。
    新しいプラグインタイプを追加する場合は、この列挙に追加してください。
    
    Attributes:
        VOICE: 音声関連プラグイン（TTS, STT, 音声合成等）
        DATA_PROCESSOR: データ処理プラグイン（フィルタリング、変換、集約等）
        EXTERNAL_API: 外部API連携プラグイン（REST API, GraphQL等）
        GUI_EXTENSION: GUI拡張プラグイン（ウィジェット、テーマ等）
        MEMORY_ENHANCER: メモリ拡張プラグイン（長期記憶、知識グラフ等）
        TOOL: ツールプラグイン（ユーティリティ、ヘルパー関数等）
        INTEGRATION: 統合プラグイン（サードパーティサービス統合）
        AGENT: エージェントプラグイン（自律エージェント、マルチエージェント）
        CUSTOM: カスタムプラグイン（上記以外の独自プラグイン）
    """
    VOICE = "voice"
    DATA_PROCESSOR = "data_processor"
    EXTERNAL_API = "external_api"
    GUI_EXTENSION = "gui_extension"
    MEMORY_ENHANCER = "memory_enhancer"
    TOOL = "tool"
    INTEGRATION = "integration"
    AGENT = "agent"
    CUSTOM = "custom"
    
    @classmethod
    def from_string(cls, type_str: str) -> 'PluginType':
        """
        文字列からPluginTypeを取得
        
        Args:
            type_str (str): プラグインタイプ文字列
        
        Returns:
            PluginType: 対応するPluginType
        
        Raises:
            ValueError: 不正なプラグインタイプ文字列の場合
        """
        try:
            return cls(type_str)
        except ValueError:
            raise ValueError(
                f"不正なプラグインタイプ: {type_str}. "
                f"有効なタイプ: {[t.value for t in cls]}"
            )


@dataclass
class PluginMetadata:
    """
    プラグインメタデータクラス
    
    プラグインの詳細情報を保持し、検索・管理を容易にします。
    
    Attributes:
        name (str): プラグイン名（一意識別子）
        version (str): バージョン（セマンティックバージョニング x.y.z）
        plugin_type (PluginType): プラグインタイプ
        author (str): 作成者
        description (str): プラグインの説明
        dependencies (List[str]): 依存プラグイン名のリスト
        priority (int): 実行優先度（0-100、値が大きいほど優先）
        enabled_by_default (bool): デフォルトで有効化するか
        config_schema (Dict[str, Any]): 設定スキーマ（JSON Schema形式）
        tags (List[str]): 検索用タグ
        homepage (Optional[str]): プラグインのホームページURL
        license (Optional[str]): ライセンス識別子（MIT, Apache-2.0 等）
    
    Example:
        metadata = PluginMetadata(
            name="VoiceSynthesizer",
            version="1.2.0",
            plugin_type=PluginType.VOICE,
            author="Naviko Team",
            description="Text-to-speech synthesis plugin",
            dependencies=["AudioOutputPlugin"],
            priority=10,
            enabled_by_default=True,
            config_schema={
                "voice_model": {"type": "string", "required": True},
                "speed": {"type": "float", "default": 1.0}
            },
            tags=["voice", "tts", "speech"]
        )
    """
    # 必須フィールド
    name: str
    version: str
    plugin_type: PluginType
    author: str
    description: str
    
    # オプションフィールド
    dependencies: List[str] = field(default_factory=list)
    priority: int = 50  # デフォルト優先度は中程度
    enabled_by_default: bool = True
    config_schema: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    homepage: Optional[str] = None
    license: Optional[str] = None
    
    def __post_init__(self):
        """
        初期化後のバリデーション
        """
        # プラグイン名の検証
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("プラグイン名は空文字列にできません")
        
        # バージョンの検証（簡易チェック）
        if not self.version or not self._is_valid_version(self.version):
            raise ValueError(
                f"不正なバージョン形式: {self.version}. "
                "セマンティックバージョニング (x.y.z) を使用してください"
            )
        
        # 優先度の検証
        if not 0 <= self.priority <= 100:
            raise ValueError(
                f"優先度は0-100の範囲で指定してください: {self.priority}"
            )
        
        # タイプが文字列の場合、PluginTypeに変換
        if isinstance(self.plugin_type, str):
            self.plugin_type = PluginType.from_string(self.plugin_type)
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """
        バージョン形式の簡易検証
        
        Args:
            version (str): バージョン文字列
        
        Returns:
            bool: 有効な場合 True
        """
        parts = version.split(".")
        if len(parts) != 3:
            return False
        
        try:
            # 各部分が数値かチェック
            for part in parts:
                int(part)
            return True
        except ValueError:
            return False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PluginMetadata':
        """
        辞書からPluginMetadataインスタンスを生成
        
        Args:
            data (Dict[str, Any]): メタデータ辞書
        
        Returns:
            PluginMetadata: メタデータインスタンス
        
        Raises:
            ValueError: 必須フィールドが欠けている場合
        """
        required_fields = ["name", "version", "type", "author", "description"]
        for field_name in required_fields:
            if field_name not in data:
                raise ValueError(f"必須フィールド '{field_name}' がありません")
        
        # 'type'フィールドを'plugin_type'にマッピング
        plugin_type_str = data.get("type")
        plugin_type = PluginType.from_string(plugin_type_str)
        
        return cls(
            name=data["name"],
            version=data["version"],
            plugin_type=plugin_type,
            author=data["author"],
            description=data["description"],
            dependencies=data.get("dependencies", []),
            priority=data.get("priority", 50),
            enabled_by_default=data.get("enabled_by_default", True),
            config_schema=data.get("config_schema", {}),
            tags=data.get("tags", []),
            homepage=data.get("homepage"),
            license=data.get("license")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        メタデータを辞書形式に変換
        
        Returns:
            Dict[str, Any]: メタデータ辞書
        """
        return {
            "name": self.name,
            "version": self.version,
            "type": self.plugin_type.value,
            "author": self.author,
            "description": self.description,
            "dependencies": self.dependencies,
            "priority": self.priority,
            "enabled_by_default": self.enabled_by_default,
            "config_schema": self.config_schema,
            "tags": self.tags,
            "homepage": self.homepage,
            "license": self.license
        }
    
    def has_dependency(self, plugin_name: str) -> bool:
        """
        指定されたプラグインに依存しているか判定
        
        Args:
            plugin_name (str): プラグイン名
        
        Returns:
            bool: 依存している場合 True
        """
        return plugin_name in self.dependencies
    
    def matches_tag(self, tag: str) -> bool:
        """
        指定されたタグにマッチするか判定
        
        Args:
            tag (str): 検索タグ
        
        Returns:
            bool: マッチする場合 True
        """
        return tag.lower() in [t.lower() for t in self.tags]
    
    def __str__(self) -> str:
        """文字列表現"""
        return f"{self.name} v{self.version} ({self.plugin_type.value}) by {self.author}"
    
    def __repr__(self) -> str:
        """デバッグ用文字列表現"""
        return (
            f"<PluginMetadata name='{self.name}' version='{self.version}' "
            f"type='{self.plugin_type.value}' priority={self.priority}>"
        )


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["PluginType", "PluginMetadata"]
