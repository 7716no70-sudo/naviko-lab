# -*- coding: utf-8 -*-
"""
サンプルデータ処理プラグイン

データフィルタリングを実行する簡単なプラグイン例。

Author: Naviko Development Team
Date: 2026-07-08
"""

# プラグインシステムのインポート
# 注: sys.pathはplugin_loader.pyで自動設定されます
from navikoLAB.plugin_system import BasePlugin, PluginStatus


class SimpleDataProcessorPlugin(BasePlugin):
    """
    シンプルデータ処理プラグイン
    
    リストデータに対してフィルタリングや変換を行います。
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
            self._default_operation = config.get('default_operation', 'filter')
            self._status = PluginStatus.READY
            print(f"📊 SimpleDataProcessorPlugin 初期化完了 (operation: {self._default_operation})")
            return True
        except Exception as e:
            self._error_message = str(e)
            self._status = PluginStatus.ERROR
            return False
    
    def execute(self, **kwargs):
        """
        データ処理の実行
        
        Args:
            data (list): 処理対象データリスト
            operation (str): 処理種別 ('filter', 'map', 'reduce')
            condition (callable, optional): フィルタ条件関数
        
        Returns:
            list: 処理結果
        
        Raises:
            RuntimeError: プラグインが未初期化の場合
            ValueError: dataが指定されていない場合
        """
        if self._status != PluginStatus.READY:
            raise RuntimeError("プラグインが初期化されていません")
        
        data = kwargs.get('data')
        if data is None:
            raise ValueError("'data'引数が必要です")
        
        operation = kwargs.get('operation', self._default_operation)
        
        self._status = PluginStatus.RUNNING
        try:
            if operation == 'filter':
                # フィルタリング: 正の数だけを抽出
                result = [x for x in data if isinstance(x, (int, float)) and x > 0]
            elif operation == 'map':
                # マッピング: 2倍にする
                result = [x * 2 if isinstance(x, (int, float)) else x for x in data]
            elif operation == 'reduce':
                # 集約: 合計を計算
                result = sum(x for x in data if isinstance(x, (int, float)))
            else:
                raise ValueError(f"未対応の操作: {operation}")
            
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
        print("🛠️ SimpleDataProcessorPlugin クリーンアップ")
        self._status = PluginStatus.UNINITIALIZED
    
    def get_metadata(self):
        """
        プラグインメタデータの取得
        
        Returns:
            Dict[str, Any]: メタデータ辞書
        """
        return {
            'name': 'SimpleDataProcessorPlugin',
            'version': '1.0.0',
            'type': 'data_processor',
            'author': 'Naviko Team',
            'description': 'シンプルなデータ処理プラグイン（サンプル）',
            'dependencies': [],
            'priority': 20,
            'enabled_by_default': True,
            'config_schema': {
                'default_operation': {'type': 'string', 'default': 'filter'}
            },
            'tags': ['data', 'processor', 'sample']
        }
