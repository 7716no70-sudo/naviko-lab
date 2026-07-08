# -*- coding: utf-8 -*-
"""
サンプル音声プラグイン

音声合成をシミュレートする簡単なプラグイン例。

Author: Naviko Development Team
Date: 2026-07-08
"""

# プラグインシステムのインポート
# 注: sys.pathはplugin_loader.pyで自動設定されます
from navikoLAB.plugin_system import BasePlugin, PluginStatus


class SimpleVoicePlugin(BasePlugin):
    """
    シンプル音声プラグイン
    
    テキストを受け取り、音声合成をシミュレートします。
    （実際には音声を出さず、テキストを返すだけです）
    """
    
    def initialize(self, config):
        """
        プラグインの初期化
        
        Args:
            config (Dict[str, Any]): プラグイン設定
        
        Returns:
            bool: 初期化成功時 True
        """
        try:
            self._config = config
            self._voice_model = config.get('voice_model', 'default')
            self._speed = config.get('speed', 1.0)
            self._status = PluginStatus.READY
            print(f"🎤 SimpleVoicePlugin 初期化完了 (model: {self._voice_model}, speed: {self._speed})")
            return True
        except Exception as e:
            self._error_message = str(e)
            self._status = PluginStatus.ERROR
            return False
    
    def execute(self, **kwargs):
        """
        音声合成の実行（シミュレーション）
        
        Args:
            text (str): 合成するテキスト
            speed (float, optional): 再生速度
        
        Returns:
            str: 合成結果メッセージ
        
        Raises:
            RuntimeError: プラグインが未初期化の場合
            ValueError: textが指定されていない場合
        """
        if self._status != PluginStatus.READY:
            raise RuntimeError("プラグインが初期化されていません")
        
        text = kwargs.get('text')
        if not text:
            raise ValueError("'text'引数が必要です")
        
        speed = kwargs.get('speed', self._speed)
        
        self._status = PluginStatus.RUNNING
        try:
            # 音声合成シミュレーション
            result = f"🔊 [{self._voice_model}] '{text}' (速度: {speed}x)"
            self._status = PluginStatus.READY
            return result
        except Exception as e:
            self._status = PluginStatus.ERROR
            self._error_message = str(e)
            raise
    
    def cleanup(self):
        """
        リソースの解放
        """
        print("🛠️ SimpleVoicePlugin クリーンアップ")
        self._status = PluginStatus.UNINITIALIZED
    
    def get_metadata(self):
        """
        プラグインメタデータの取得
        
        Returns:
            Dict[str, Any]: メタデータ辞書
        """
        return {
            'name': 'SimpleVoicePlugin',
            'version': '1.0.0',
            'type': 'voice',
            'author': 'Naviko Team',
            'description': 'シンプルな音声合成プラグイン（サンプル）',
            'dependencies': [],
            'priority': 10,
            'enabled_by_default': True,
            'config_schema': {
                'voice_model': {'type': 'string', 'default': 'default'},
                'speed': {'type': 'float', 'default': 1.0}
            },
            'tags': ['voice', 'tts', 'sample']
        }
