# -*- coding: utf-8 -*-
"""
OllamaProvider - ローカルLLM統合プロバイダー

ローカルでOllama LLMを実行し、完全にオフラインで動作する。
Gemini/ChatGPTに依存せず、同等の能力をローカルで実現。

Author: Naviko LAB
Date: 2026-07-02
Version: 1.0.0
"""

import requests
import json
from typing import Optional, Dict, Any
import time


class OllamaProvider:
    """
    ローカルOllama LLM統合プロバイダー
    
    完全にオフラインで動作し、外部APIに依存しない。
    Gemini/ChatGPTと同等の能力をローカルで実現。
    """
    
    def __init__(self, model: str = "codellama:7b", api_url: str = "http://localhost:11434"):
        """
        初期化
        
        Args:
            model: 使用するOllamaモデル (codellama:7b, llama3.1:8b, deepseek-coder:6.7b等)
            api_url: Ollama APIのURL（デフォルト: localhost:11434）
        """
        self.model = model
        self.api_url = api_url
        self.name = "ollama"
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Ollamaが起動しているか確認"""
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=2)
            if response.status_code == 200:
                # 指定したモデルが利用可能か確認
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                return any(self.model in name for name in model_names)
            return False
        except:
            return False
    
    def is_available(self) -> bool:
        """現在の利用可能状態を返す"""
        return self.available
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """
        ローカルLLMでコード生成
        
        Args:
            prompt: 生成プロンプト
            max_tokens: 最大トークン数
            temperature: 生成の多様性（0.0-1.0）
        
        Returns:
            生成されたテキスト
        
        Raises:
            Exception: Ollama APIエラー時
        """
        if not self.is_available():
            raise Exception(f"Ollama not available. Model {self.model} not found or Ollama not running.")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json=payload,
                timeout=120  # 2分タイムアウト
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
        
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timeout (120s). Model may be too large or slow.")
        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    def get_info(self) -> Dict[str, Any]:
        """プロバイダー情報を取得"""
        return {
            "name": self.name,
            "model": self.model,
            "api_url": self.api_url,
            "available": self.available,
            "type": "local",
            "description": "ローカルOllama LLM - 完全オフライン動作"
        }
