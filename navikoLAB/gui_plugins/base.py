<<<<<<< Updated upstream
# -*- coding: utf-8 -*-
=======
# -*- coding: utf-8 -*-
>>>>>>> Stashed changes
"""
Naviko GUI Plugin System - 抽象基底クラス定義

このモジュールは、Naviko GUIプラグインシステムの抽象基底クラスを定義します。
全てのキャラクターレンダラーとチャット表示プラグインは、これらのクラスを継承して実装します。

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

from abc import ABC, abstractmethod
import tkinter as tk
from typing import Dict, Any, Optional


class CharacterRenderer(ABC):
    """
    キャラクター表示プラグインの抽象基底クラス
    
    全てのキャラクターレンダラー（2Dスプライト、3Dモデル、Live2D等）は
    このクラスを継承して実装します。
    
    プラグイン実装者は、以下のメソッドを必ず実装してください：
    - initialize(): プラグインの初期化
    - render(): キャラクターの描画
    - update_emotion(): 感情表現の更新
    - cleanup(): リソースの解放
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        プラグインの初期化
        
        Args:
            config (Dict[str, Any]): プラグイン設定（gui_config.jsonから読み込まれる）
                例: {
                    "sprite_dir": "character_sprites/",
                    "default_emotion": "neutral"
                }
        
        Raises:
            ValueError: 設定が不正な場合
            FileNotFoundError: 必要なリソースファイルが見つからない場合
        """
        pass
    
    @abstractmethod
    def render(self, emotion: str, canvas: tk.Canvas) -> None:
        """
        キャラクターの描画
        
        Args:
            emotion (str): 表示する感情（例: "neutral", "happy", "sad", "angry"）
            canvas (tk.Canvas): 描画対象のTkinter Canvas
        
        Raises:
            ValueError: 未対応の感情が指定された場合
        """
        pass
    
    @abstractmethod
    def update_emotion(self, emotion: str) -> None:
        """
        感情表現の更新（描画なし）
        
        Args:
            emotion (str): 更新する感情
        
        Note:
            このメソッドは内部状態のみを更新します。
            実際の描画には render() を呼び出してください。
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        リソースの解放
        
        プラグイン終了時に呼び出されます。
        画像メモリ、3Dモデルデータ等のリソースを解放してください。
        """
        pass


class ChatDisplay(ABC):
    """
    チャット表示プラグインの抽象基底クラス
    
    全てのチャット表示プラグイン（会話式、ノベル風、RPG風等）は
    このクラスを継承して実装します。
    
    プラグイン実装者は、以下のメソッドを必ず実装してください：
    - initialize(): プラグインの初期化
    - display_user_message(): ユーザーメッセージの表示
    - display_ai_message(): AIメッセージの表示
    - clear_display(): 表示内容のクリア
    - get_widget(): ウィジェットの取得
    """
    
    @abstractmethod
    def initialize(self, parent: tk.Widget, config: Dict[str, Any]) -> None:
        """
        プラグインの初期化
        
        Args:
            parent (tk.Widget): 親ウィジェット（通常はFrameまたはCanvas）
            config (Dict[str, Any]): プラグイン設定（gui_config.jsonから読み込まれる）
                例: {
                    "font_size": 12,
                    "colors": {
                        "user_bg": "#E3F2FD",
                        "ai_bg": "##F3E5F5"
                    }
                }
        
        Raises:
            ValueError: 設定が不正な場合
        """
        pass
    
    @abstractmethod
    def display_user_message(self, text: str) -> None:
        """
        ユーザーメッセージの表示
        
        Args:
            text (str): 表示するメッセージテキスト
        
        Note:
            メッセージの整形、背景色、フォント等はプラグイン実装に委ねられます。
        """
        pass
    
    @abstractmethod
    def display_ai_message(self, text: str, emotion: str = "neutral") -> None:
        """
        AIメッセージの表示
        
        Args:
            text (str): 表示するメッセージテキスト
            emotion (str, optional): AI感情表現. Defaults to "neutral".
        
        Note:
            emotionパラメータは、キャラクターレンダラーと連携して
            表情変化を実現する際に使用されます。
        """
        pass
    
    @abstractmethod
    def clear_display(self) -> None:
        """
        表示内容のクリア
        
        チャット履歴や表示中のメッセージを全てクリアします。
        """
        pass
    
    @abstractmethod
    def get_widget(self) -> tk.Widget:
        """
        ウィジェットの取得
        
        Returns:
            tk.Widget: プラグインのルートウィジェット
        
        Note:
            親ウィンドウにこのウィジェットを配置することで、
            チャット表示が統合されます。
        """
        pass


# プラグインシステムのバージョン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__all__ = ["CharacterRenderer", "ChatDisplay"]
