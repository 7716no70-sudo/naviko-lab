# -*- coding: utf-8 -*-
"""
UniversalLLMConnector - マルチプロバイダーLLM統合

ローカルLLM（Ollama）とクラウドAPI（Groq等）を統一インターフェースで管理。
完全な自律性と強固なフォールバックチェーンを実現。

Author: Naviko LAB
Date: 2026-07-02
Version: 1.0.0
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import os

from navikoLAB.llm_connector import LLMConnector
from navikoLAB.ollama_provider import OllamaProvider


class UniversalLLMConnector:
    """
    マルチプロバイダーLLM統合コネクター
    
    ローカルLLM（Ollama）とクラウドAPI（Groq等）を統一管理。
    完全な自律性と強固なフォールバックを実現。
    """
    
    def __init__(
        self,
        lab_dir: Path,
        api_key: Optional[str] = None,
        default_provider: str = "local",
        ollama_model: str = "codellama:7b"
    ):
        """
        初期化
        
        Args:
            lab_dir: navikoLABディレクトリ
            api_key: Groq APIキー（クラウドバックアップ用）
            default_provider: デフォルトプロバイダー ("local" or "groq")
            ollama_model: 使用するOllamaモデル
        """
        self.lab_dir = lab_dir
        self.default_provider = default_provider
        
        # プロバイダー初期化
        self.providers = {}
        
        # ローカルOllamaプロバイダー
        try:
            self.providers["local"] = OllamaProvider(model=ollama_model)
        except Exception as e:
            print(f"⚠️ Ollama初期化失敗: {e}")
            self.providers["local"] = None
        
        # Groqクラウドプロバイダー
        try:
            self.providers["groq"] = LLMConnector(lab_dir=lab_dir, api_key=api_key)
        except Exception as e:
            print(f"⚠️ Groq初期化失敗: {e}")
            self.providers["groq"] = None
    
    def get_available_providers(self) -> List[str]:
        """利用可能なプロバイダーのリストを取得"""
        available = []
        
        if self.providers.get("local") and self.providers["local"].is_available():
            available.append("local")
        
        if self.providers.get("groq"):
            # LLMConnectorの利用可能性チェック（複数の方法を試す）
            groq_provider = self.providers["groq"]
            is_available = False
            
            # 方法1: llm_available属性をチェック（存在する場合）
            if hasattr(groq_provider, 'llm_available'):
                is_available = groq_provider.llm_available
            # 方法2: api_keyの存在をチェック
            elif hasattr(groq_provider, 'api_key') and groq_provider.api_key:
                is_available = True
            
            if is_available:
                available.append("groq")
        
        return available
    
    def generate_code(
        self,
        prompt: str,
        provider: Optional[str] = None,
        fallback_chain: Optional[List[str]] = None,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        コード生成（フォールバックチェーン付き）
        
        Args:
            prompt: 生成プロンプト
            provider: 使用するプロバイダー（Noneの場合はdefault_provider）
            fallback_chain: フォールバックチェーン（優先順位）
            max_tokens: 最大トークン数
        
        Returns:
            {
                "success": bool,
                "code": str,
                "provider_used": str,
                "mode": str,  # "local", "cloud", or "template"
                "error": str (optional)
            }
        """
        # フォールバックチェーンのデフォルト
        if fallback_chain is None:
            fallback_chain = ["local", "groq", "template"]
        
        # 指定されたプロバイダーを最優先
        if provider:
            fallback_chain = [provider] + [p for p in fallback_chain if p != provider]
        
        last_error = None
        
        for provider_name in fallback_chain:
            try:
                if provider_name == "template":
                    # 最終フォールバック: テンプレートモード
                    return {
                        "success": True,
                        "code": self._generate_template_code(prompt),
                        "provider_used": "template",
                        "mode": "template"
                    }
                
                provider_obj = self.providers.get(provider_name)
                
                if not provider_obj:
                    continue
                
                # ローカルOllama
                if provider_name == "local":
                    if not provider_obj.is_available():
                        continue
                    
                    print(f"🚀 使用モデル: {provider_obj.model} (local)")
                    code = provider_obj.generate(prompt, max_tokens=max_tokens)
                    
                    return {
                        "success": True,
                        "code": code,
                        "provider_used": provider_name,
                        "mode": "local",
                        "model": provider_obj.model
                    }
                
                # Groqクラウド
                elif provider_name == "groq":
                    # 利用可能性チェック
                    is_available = False
                    if hasattr(provider_obj, 'llm_available'):
                        is_available = provider_obj.llm_available
                    elif hasattr(provider_obj, 'api_key') and provider_obj.api_key:
                        is_available = True
                    
                    if not is_available:
                        continue
                    
                    print(f"🚀 使用モデル: Groq (cloud)")
                    result = provider_obj.generate_code(
                        purpose=prompt,
                        context="Code generation request"
                    )
                    
                    if result["success"]:
                        return {
                            "success": True,
                            "code": result["code"],
                            "provider_used": provider_name,
                            "mode": "cloud"
                        }
            
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ {provider_name} failed: {e}")
                continue
        
        # すべて失敗
        return {
            "success": False,
            "code": "",
            "provider_used": "none",
            "mode": "failed",
            "error": last_error or "All providers failed"
        }
    
    def _generate_template_code(self, prompt: str) -> str:
        """テンプレートコード生成（最終フォールバック）"""
        return f'''# -*- coding: utf-8 -*-
"""
{prompt}

NOTE: This is a basic template.
Please implement the actual functionality.
"""

def main():
    """Main function"""
    print("TODO: {prompt}")
    # Add implementation here
    pass

if __name__ == "__main__":
    main()
'''  
    
    def diagnose(self) -> Dict[str, Any]:
        """診断情報を取得"""
        available_providers = self.get_available_providers()
        
        diagnosis = {
            "default_provider": self.default_provider,
            "available_providers": available_providers,
            "providers": {}
        }
        
        for name, provider in self.providers.items():
            if provider:
                if name == "local":
                    diagnosis["providers"][name] = provider.get_info()
                elif name == "groq":
                    # Groqの利用可能性を柔軟にチェック
                    is_available = False
                    if hasattr(provider, 'llm_available'):
                        is_available = provider.llm_available
                    elif hasattr(provider, 'api_key') and provider.api_key:
                        is_available = True
                    
                    diagnosis["providers"][name] = {
                        "name": "groq",
                        "available": is_available,
                        "type": "cloud"
                    }
        
        return diagnosis
    
    def format_diagnosis(self) -> str:
        """診断情報をフォーマット"""
        diag = self.diagnose()
        
        output = []
        output.append("📡 UniversalLLMConnector 診断")
        output.append("=" * 60)
        output.append(f"デフォルトプロバイダー: {diag['default_provider']}")
        output.append(f"利用可能: {', '.join(diag['available_providers']) or 'None'}")
        output.append("
📊 プロバイダー状態:")
        
        for name, info in diag["providers"].items():
            status = "✅" if info.get("available") else "❌"
            output.append(f"  {status} {name}: {info.get('type', 'unknown')}")
            if name == "local" and info.get("available"):
                output.append(f"      モデル: {info.get('model')}")
        
        return "
".join(output)
