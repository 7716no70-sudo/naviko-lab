<<<<<<< Updated upstream
﻿# -*- coding: utf-8 -*-
=======
# -*- coding: utf-8 -*-
>>>>>>> Stashed changes
"""
Naviko GUI Plugin System - DefaultSpriteRenderer

2D静止画キャラクターレンダラー（デフォルト実装）
現在のNaviko.pyのキャラクター表示機能をプラグイン化

Author: Naviko Development Team
Date: 2026-07-06
Version: 1.0.0
"""

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys
sys.path.append(str(Path(__file__).parent.parent))
from base import CharacterRenderer


class DefaultSpriteRenderer(CharacterRenderer):
    """
    デフォルト2Dスプライトキャラクターレンダラー
    
    spritesheet.webpから各感情のフレームを切り出し、
    Tkinter Canvasに描画します。
    
    設定例（gui_config.json）:
    {
        "sprite_dir": "./",
        "sprite_file": "spritesheet.webp",
        "base_width": 128,
        "base_height": 128,
        "default_emotion": "neutral",
        "emotions": ["idle", "waving", "failed", "waiting"],
        "scale": 1.0
    }
    """
    
    def __init__(self):
        """コンストラクタ"""
        self.config: Dict[str, Any] = {}
        self.current_emotion: str = "idle"
        self.raw_frames: Dict[str, List[Image.Image]] = {}
        self.tk_frames: Dict[str, List[ImageTk.PhotoImage]] = {}
        self.base_width: int = 128
        self.base_height: int = 128
        self.scale: float = 1.0
        self.spritesheet: Optional[Image.Image] = None
        self.canvas_image_id: Optional[int] = None
        self.current_frame_index: int = 0
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        プラグインの初期化
        
        Args:
            config (Dict[str, Any]): プラグイン設定
                - sprite_dir (str): スプライトシートのディレクトリ
                - sprite_file (str): スプライトシートファイル名
                - base_width (int): 基本フレーム幅
                - base_height (int): 基本フレーム高さ
                - default_emotion (str): デフォルト感情
                - emotions (dict): 感情別フレーム定義 {emotion: (row, count)}
                - scale (float): 表示スケール
        
        Raises:
            FileNotFoundError: スプライトシートが見つからない場合
            ValueError: 設定が不正な場合
        """
        self.config = config
        
        # 設定の検証
        required_keys = ["sprite_dir", "sprite_file", "emotions"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"必須設定項目 '{key}' がありません。")
        
        # 基本パラメータの取得
        self.base_width = config.get("base_width", 128)
        self.base_height = config.get("base_height", 128)
        self.scale = config.get("scale", 1.0)
        self.current_emotion = config.get("default_emotion", "idle")
        
        # スプライトシートのパスを構築
        sprite_dir = Path(config["sprite_dir"])
        sprite_file = config["sprite_file"]
        sprite_path = sprite_dir / sprite_file
        
        # スプライトシートの存在確認
        if not sprite_path.exists():
            raise FileNotFoundError(
                f"スプライトシートが見つかりません: {sprite_path}\n"
                f"設定を確認してください。"
            )
        
        # スプライトシートの読み込み
        print(f"📥 スプライトシート読み込み: {sprite_path}")
        self.spritesheet = Image.open(sprite_path).convert("RGBA")
        
        # フレームの切り出し
        self._extract_frames(config["emotions"])
        
        # Tkinter用画像の生成
        self._create_tk_images()
        
        print(f"✅ DefaultSpriteRenderer初期化完了")
        print(f"   - 感情: {list(self.raw_frames.keys())}")
        print(f"   - スケール: {self.scale}")
    
    def _extract_frames(self, emotions_config: Dict[str, tuple]) -> None:
        """
        スプライトシートから各感情のフレームを切り出す
        
        Args:
            emotions_config (Dict[str, tuple]): 感情別フレーム定義
                例: {"idle": (0, 4), "waving": (1, 4)}
                    (行番号, フレーム数)
        """
        for emotion, (row, frame_count) in emotions_config.items():
            self.raw_frames[emotion] = []
            y_pos = row * self.base_height
            
            for col in range(frame_count):
                x_pos = col * self.base_width
                cropped = self.spritesheet.crop(
                    (x_pos, y_pos, x_pos + self.base_width, y_pos + self.base_height)
                )
                self.raw_frames[emotion].append(cropped)
        
        print(f"   切り出し完了: {len(self.raw_frames)} 感情、"
              f"総フレーム数 {sum(len(frames) for frames in self.raw_frames.values())}")
    
    def _create_tk_images(self) -> None:
        """
        切り出したフレームをTkinter用画像に変換
        """
        w_size = int(self.base_width * self.scale)
        h_size = int(self.base_height * self.scale)
        
        for emotion, frames in self.raw_frames.items():
            self.tk_frames[emotion] = []
            for img in frames:
                resized = img.resize((w_size, h_size), Image.Resampling.NEAREST)
                self.tk_frames[emotion].append(ImageTk.PhotoImage(resized))
    
    def render(self, emotion: str, canvas: tk.Canvas) -> None:
        """
        キャラクターの描画
        
        Args:
            emotion (str): 表示する感情
            canvas (tk.Canvas): 描画対象のTkinter Canvas
        
        Raises:
            ValueError: 未対応の感情が指定された場合
        """
        if emotion not in self.tk_frames:
            available = list(self.tk_frames.keys())
            raise ValueError(
                f"未対応の感情: {emotion}\n"
                f"使用可能な感情: {available}"
            )
        
        frames_list = self.tk_frames[emotion]
        if not frames_list:
            return
        
        # フレームインデックスの循環
        if self.current_frame_index >= len(frames_list):
            self.current_frame_index = 0
        
        # Canvas上の画像を更新
        current_frame = frames_list[self.current_frame_index]
        
        if self.canvas_image_id is None:
            # 初回描画
            self.canvas_image_id = canvas.create_image(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2,
                image=current_frame
            )
        else:
            # 既存画像を更新
            canvas.itemconfig(self.canvas_image_id, image=current_frame)
        
        # 次フレームへ
        self.current_frame_index = (self.current_frame_index + 1) % len(frames_list)
    
    def update_emotion(self, emotion: str) -> None:
        """
        感情表現の更新（描画なし）
        
        Args:
            emotion (str): 更新する感情
        
        Raises:
            ValueError: 未対応の感情が指定された場合
        """
        if emotion not in self.raw_frames:
            available = list(self.raw_frames.keys())
            raise ValueError(
                f"未対応の感情: {emotion}\n"
                f"使用可能な感情: {available}"
            )
        
        self.current_emotion = emotion
        self.current_frame_index = 0  # フレームをリセット
        print(f"🎭 感情更新: {emotion}")
    
    def cleanup(self) -> None:
        """
        リソースの解放
        
        画像メモリを解放し、内部状態をリセットします。
        """
        # PIL画像を解放
        if self.spritesheet:
            self.spritesheet.close()
            self.spritesheet = None
        
        # raw_frames解放
        for frames in self.raw_frames.values():
            for img in frames:
                img.close()
        self.raw_frames.clear()
        
        # Tkinter画像解放
        self.tk_frames.clear()
        
        self.canvas_image_id = None
        self.current_frame_index = 0
        
        print("🧹 DefaultSpriteRenderer: リソース解放完了")


# プラグイン情報
__version__ = "1.0.0"
__author__ = "Naviko Development Team"
__plugin_name__ = "DefaultSprite"
__plugin_class__ = DefaultSpriteRenderer
