# -*- coding: utf-8 -*-
"""
Naviko Plugin System - 汎用プラグイン基底クラス

このモジュールは、Naviko汎用プラグインシステムの基底クラスを定義します。
全ての拡張機能プラグイン（音声、データ処理、外部API連携等）はBasePluginを継承して実装します。

Author: Naviko Development Team
Date: 2026-07-08
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum


class PluginStatus(Enum):
    """プラグインの実行状態"""
    UNINITIALIZED = "uninitialized"  # 未初期化
    READY = "ready"                  # 実行可能
    RUNNING = "running"              # 実行中
    ERROR = "error"                  # エラー状態
    DISABLED = "disabled"            # 無効化


class BasePlugin(ABC):
    """
    汎用プラグインの抽象基底クラス
    
    全てのNavikoプラグイン（音声、データ処理、外部API連携、メモリ拡張等）は
    このクラスを継承して実装します。
    
    プラグイン実装者は、以下のメソッドを必ず実装してください：
    - initialize(): プラグインの初期化
    - execute(): プラグインの主処理
    - cleanup(): リソースの解放
    - get_metadata(): プラグイン情報の提供
    
    Attributes:
        _status (PluginStatus): 現在のプラグイン状態
        _config (Dict[str, Any]): プラグイン設定
        _error_message (Optional[str]): エラーメッセージ（エラー時のみ）
    
    Example:
        class MyVoicePlugin(BasePlugin):
            def initialize(self, config: Dict[str, Any]) -> bool:
                self._config = config
                return True
            
            def execute(self, **kwargs) -> Any:
                text = kwargs.get('text', '')
                # 音声処理実装...
                return result
            
            def cleanup(self) -> None:
                # リソース解放...
                pass
            
            def get_metadata(self) -> Dict[str, Any]:
                return {
                    'name': 'MyVoicePlugin',
                    'version': '1.0.0',
                    'type': 'voice'
                }
    """
    
    def __init__(self):
        """
        基底コンストラクタ
        
        サブクラスで__init__をオーバーライドする場合は、
        必ず super().__init__() を呼び出してください。
        """
        self._status: PluginStatus = PluginStatus.UNINITIALIZED
        self._config: Dict[str, Any] = {}
        self._error_message: Optional[str] = None
    
    @property
    def status(self) -> PluginStatus:
        """プラグインの現在状態を取得"""
        return self._status
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        プラグインの初期化
        
        Args:
            config (Dict[str, Any]): プラグイン設定辞書
                例: {
                    "api_key": "xxxx",
                    "timeout": 30,
                    "retry_count": 3
                }
        
        Returns:
            bool: 初期化成功時 True、失敗時 False
        
        Note:
            初期化成功時は self._status を PluginStatus.READY に設定してください。
            失敗時は self._error_message にエラー内容を設定し、False を返してください。
        
        Example:
            def initialize(self, config: Dict[str, Any]) -> bool:
                try:
                    self._config = config
                    self._api_client = APIClient(config['api_key'])
                    self._status = PluginStatus.READY
                    return True
                except Exception as e:
                    self._error_message = str(e)
                    self._status = PluginStatus.ERROR
                    return False
        """
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        プラグインの主処理
        
        Args:
            **kwargs: プラグイン固有の引数
                例:
                - 音声プラグイン: text="こんにちは", speed=1.0
                - データ処理プラグイン: data=[...], operation="filter"
                - API連携プラグイン: endpoint="/users", method="GET"
        
        Returns:
            Any: プラグイン処理結果（プラグインごとに異なる型）
        
        Raises:
            RuntimeError: プラグインが未初期化の場合
            ValueError: 引数が不正な場合
            Exception: プラグイン処理中のエラー
        
        Note:
            実行前に self._status が READY かチェックしてください。
            実行中は self._status を RUNNING に設定することを推奨します。
        
        Example:
            def execute(self, **kwargs) -> str:
                if self._status != PluginStatus.READY:
                    raise RuntimeError("Plugin not initialized")
                
                text = kwargs.get('text')
                if not text:
                    raise ValueError("'text' argument is required")
                
                self._status = PluginStatus.RUNNING
                try:
                    result = self._process(text)
                    self._status = PluginStatus.READY
                    return result
                except Exception as e:
                    self._status = PluginStatus.ERROR
                    self._error_message = str(e)
                    raise
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        リソースの解放
        
        プラグイン終了時やシステムシャットダウン時に呼び出されます。
        API接続のクローズ、ファイルハンドルの解放、スレッドの停止等を行ってください。
        
        Note:
            cleanup完了後は self._status を UNINITIALIZED に設定してください。
        
        Example:
            def cleanup(self) -> None:
                if hasattr(self, '_api_client'):
                    self._api_client.close()
                if hasattr(self, '_worker_thread'):
                    self._worker_thread.stop()
                self._status = PluginStatus.UNINITIALIZED
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        プラグインメタデータの取得
        
        Returns:
            Dict[str, Any]: プラグイン情報辞書
                必須フィールド:
                - name (str): プラグイン名
                - version (str): バージョン（セマンティックバージョニング推奨）
                - type (str): プラグインタイプ（voice, data_processor, external_api 等）
                - author (str): 作成者
                - description (str): プラグインの説明
                
                オプションフィールド:
                - dependencies (List[str]): 依存プラグイン名のリスト
                - priority (int): 実行優先度（数値が大きいほど優先）
                - enabled_by_default (bool): デフォルト有効化フラグ
                - config_schema (Dict): 設定スキーマ
        
        Example:
            def get_metadata(self) -> Dict[str, Any]:
                return {
                    'name': 'VoiceSynthesizer',
                    'version': '1.2.0',
                    'type': 'voice',
                    'author': 'Naviko Team',
                    'description': 'Text-to-speech synthesis plugin',
                    'dependencies': ['AudioOutputPlugin'],
                    'priority': 10,
                    'enabled_by_default': True,
                    'config_schema': {
                        'voice_model': {'type': 'string', 'required': True},
                        'speed': {'type': 'float', 'default': 1.0}
                    }
                }
        """
        pass
    
    # ============================================================
    # ユーティリティメソッド（サブクラスで利用可能）
    # ============================================================
    
    def get_status(self) -> PluginStatus:
        """
        現在のプラグイン状態を取得
        
        Returns:
            PluginStatus: 現在の状態
        """
        return self._status
    
    def get_error_message(self) -> Optional[str]:
        """
        エラーメッセージを取得
        
        Returns:
            Optional[str]: エラーメッセージ（エラー状態でない場合は None）
        """
        return self._error_message
    
    def is_ready(self) -> bool:
        """
        プラグインが実行可能か判定
        
        Returns:
            bool: 実行可能な場合 True
        """
        return self._status == PluginStatus.READY
    
    def disable(self) -> None:
        """
        プラグインを無効化
        
        cleanup() を呼び出さずに一時的に無効化します。
        """
        if self._status not in [PluginStatus.UNINITIALIZED, PluginStatus.ERROR]:
            self._status = PluginStatus.DISABLED
    
    def enable(self) -> None:
        """
        プラグインを有効化
        
        無効化されたプラグインを READY 状態に戻します。
        """
        if self._status == PluginStatus.DISABLED:
            self._status = PluginStatus.READY
    
    def __str__(self) -> str:
        """文字列表現"""
        metadata = self.get_metadata()
        return f"{metadata.get('name', 'Unknown')} v{metadata.get('version', '0.0.0')} [{self._status.value}]"
    
    def __repr__(self) -> str:
        """デバッグ用文字列表現"""
        metadata = self.get_metadata()
        return (
            f"<{self.__class__.__name__} "
            f"name='{metadata.get('name')}' "
            f"version='{metadata.get('version')}' "
            f"status={self._status.value}>"
        )


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["BasePlugin", "PluginStatus"]
