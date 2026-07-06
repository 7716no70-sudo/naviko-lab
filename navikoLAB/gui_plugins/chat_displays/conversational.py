# -*- coding: utf-8 -*-
"""
Naviko GUI Plugin System - ConversationalChat

対話式チャット表示プラグイン（デフォルト実装）
現在のNaviko.pyのチャット表示機能をプラグイン化

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Dict, Any, Optional
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from base import ChatDisplay


class ConversationalChat(ChatDisplay):
    """
    対話式チャット表示プラグイン
    
    ScrolledTextを使用した従来の対話スタイルのチャット表示。
    ユーザーメッセージは右寄せ（青色）、AIメッセージは左寄せ（白色）で表示。
    
    設定例（gui_config.json）:
    {
        "font_size": 10,
        "font_family": "MS Gothic",
        "bg_color": "#2d2d2d",
        "fg_color": "#ffffff",
        "user_color": "#6366f1",
        "ai_color": "#a8a8a8",
        "user_text_color": "#e0e7ff",
        "ai_text_color": "#ffffff"
    }
    """
    
    def __init__(self):
        """コンストラクタ"""
        self.config: Dict[str, Any] = {}
        self.widget: Optional[scrolledtext.ScrolledText] = None
        self.parent: Optional[tk.Widget] = None
    
    def initialize(self, parent: tk.Widget, config: Dict[str, Any]) -> None:
        """
        プラグインの初期化
        
        Args:
            parent (tk.Widget): 親ウィジェット
            config (Dict[str, Any]): プラグイン設定
                - font_size (int): フォントサイズ（デフォルト: 10）
                - font_family (str): フォント名（デフォルト: "MS Gothic"）
                - bg_color (str): 背景色（デフォルト: "#2d2d2d"）
                - fg_color (str): 文字色（デフォルト: "#ffffff"）
                - user_color (str): ユーザー名の色（デフォルト: "#6366f1"）
                - ai_color (str): AI名の色（デフォルト: "#a8a8a8"）
                - user_text_color (str): ユーザーメッセージの色（デフォルト: "#e0e7ff"）
                - ai_text_color (str): AIメッセージの色（デフォルト: "#ffffff"）
        """
        self.config = config
        self.parent = parent
        
        # デフォルト値の設定
        font_size = config.get("font_size", 10)
        font_family = config.get("font_family", "MS Gothic")
        bg_color = config.get("bg_color", "#2d2d2d")
        fg_color = config.get("fg_color", "#ffffff")
        
        # ScrolledTextウィジェットの作成
        self.widget = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            bg=bg_color,
            fg=fg_color,
            font=(font_family, font_size),
            bd=0
        )
        self.widget.pack(
            padx=10,
            pady=5,
            fill=tk.BOTH,
            expand=True
        )
        
        # タグの設定（色・配置）
        user_color = config.get("user_color", "#6366f1")
        ai_color = config.get("ai_color", "#a8a8a8")
        user_text_color = config.get("user_text_color", "#e0e7ff")
        ai_text_color = config.get("ai_text_color", "#ffffff")
        
        self.widget.tag_config(
            "user_title",
            foreground=user_color,
            justify="right"
        )
        self.widget.tag_config(
            "user_text",
            foreground=user_text_color,
            justify="right"
        )
        self.widget.tag_config(
            "navi_title",
            foreground=ai_color
        )
        self.widget.tag_config(
            "navi_text",
            foreground=ai_text_color
        )
        
        # 初期メッセージ
        self.display_ai_message(
            "…はぁ。起動しました。指示をどうぞ。",
            emotion="neutral"
        )
        
        print("✅ ConversationalChat初期化完了")
        print(f"   - フォント: {font_family} {font_size}pt")
        print(f"   - ユーザー色: {user_color}")
        print(f"   - AI色: {ai_color}")
    
    def display_user_message(self, text: str) -> None:
        """
        ユーザーメッセージの表示
        
        Args:
            text (str): 表示するメッセージ
        """
        if not self.widget:
            print("⚠️ ConversationalChat: 未初期化")
            return
        
        self.widget.configure(state="normal")
        
        # ユーザー名表示（右寄せ）
        self.widget.insert(
            tk.END,
            "
" + " " * 30 + "【ナオさん】
",
            "user_title"
        )
        
        # メッセージ表示（右寄せ）
        self.widget.insert(
            tk.END,
            text + "
",
            "user_text"
        )
        
        # 自動スクロール
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
    
    def display_ai_message(self, text: str, emotion: str = "neutral") -> None:
        """
        AIメッセージの表示
        
        Args:
            text (str): 表示するメッセージ
            emotion (str): 感情表現（未使用・将来拡張用）
        """
        if not self.widget:
            print("⚠️ ConversationalChat: 未初期化")
            return
        
        self.widget.configure(state="normal")
        
        # AI名表示（左寄せ）
        self.widget.insert(
            tk.END,
            "
【ナビ子】
",
            "navi_title"
        )
        
        # メッセージ表示（左寄せ）
        self.widget.insert(
            tk.END,
            f"{text}
",
            "navi_text"
        )
        
        # 自動スクロール
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
    
    def clear_display(self) -> None:
        """
        チャット表示のクリア
        
        全てのメッセージを削除します。
        """
        if not self.widget:
            print("⚠️ ConversationalChat: 未初期化")
            return
        
        self.widget.configure(state="normal")
        self.widget.delete("1.0", tk.END)
        self.widget.configure(state="disabled")
        print("🧹 チャット表示をクリアしました")
    
    def get_widget(self) -> tk.Widget:
        """
        チャット表示ウィジェットの取得
        
        Returns:
            tk.Widget: ScrolledTextウィジェット
        
        Raises:
            RuntimeError: 未初期化の場合
        """
        if not self.widget:
            raise RuntimeError(
                "ConversationalChat: 未初期化です。initialize()を先に呼び出してください。"
            )
        return self.widget


# プラグイン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__plugin_name__ = "Conversational"
__plugin_class__ = ConversationalChat
