# -*- coding: utf-8 -*-
"""
UniversalLLMConnector - マルチプロバイダーLLM統合
ローカルLLM（Ollama）とクラウドAPI（Groq等）を統一管理
"""
from pathlib import Path
from typing import Optional, List, Dict, Any
import sys

# OllamaProviderをインポート
try:
    from navikoLAB.ollama_provider import OllamaProvider
except ImportError:
    OllamaProvider = None

# LLMConnectorをインポート
try:
    from navikoLAB.llm_connector import LLMConnector
except ImportError:
    LLMConnector = None

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
        self.lab_dir = Path(lab_dir) if isinstance(lab_dir, str) else lab_dir
        self.default_provider = default_provider
        
        # プロバイダー初期化
        self.providers = {}
        
        # ローカルOllamaプロバイダー
        if OllamaProvider:
            try:
                self.providers["local"] = OllamaProvider(model=ollama_model)
            except Exception as e:
                print(f"⚠️ Ollama初期化失敗: {e}")
                self.providers["local"] = None
        else:
            self.providers["local"] = None
        
        # Groqクラウドプロバイダー
        if LLMConnector:
            try:
                self.providers["groq"] = LLMConnector(lab_dir=self.lab_dir, api_key=api_key)
            except Exception as e:
                print(f"⚠️ Groq初期化失敗: {e}")
                self.providers["groq"] = None
        else:
            self.providers["groq"] = None
    
    def get_available_providers(self) -> List[str]:
        """利用可能なプロバイダーのリストを取得"""
        available = []
        
        if self.providers.get("local") and self.providers["local"].is_available():
            available.append("local")
        
        if self.providers.get("groq"):
            groq_provider = self.providers["groq"]
            is_available = False
            
            if hasattr(groq_provider, 'llm_available'):
                is_available = groq_provider.llm_available
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
            fallback_chain: フォールバックチェーン（例: ["local", "groq", "template"]）
            max_tokens: 最大トークン数
        
        Returns:
            生成結果辞書 {success, code, provider, error}
        """
        # プロバイダー決定
        target_provider = provider or self.default_provider
        
        # フォールバックチェーン構築
        if fallback_chain is None:
            fallback_chain = [target_provider]
            available = self.get_available_providers()
            for p in available:
                if p not in fallback_chain:
                    fallback_chain.append(p)
            fallback_chain.append("template")
        
        # フォールバックチェーンで順番に試行
        for prov in fallback_chain:
            try:
                if prov == "template":
                    # テンプレートモード（最終フォールバック）
                    return {
                        "success": True,
                        "code": self._generate_template_code(prompt),
                        "provider": "template",
                        "mode": "template"
                    }
                
                provider_obj = self.providers.get(prov)
                if not provider_obj:
                    continue
                
                # ローカルOllama
                if prov == "local" and provider_obj.is_available():
                    code = provider_obj.generate(prompt, max_tokens=max_tokens)
                    return {
                        "success": True,
                        "code": code,
                        "provider": "local",
                        "mode": "llm",
                        "model": provider_obj.model
                    }
                
                # Groq
                elif prov == "groq":
                    if hasattr(provider_obj, 'generate_code'):
                        result = provider_obj.generate_code(
                            prompt=prompt,
                            max_tokens=max_tokens,
                            use_llm=True
                        )
                        if result.get("success"):
                            return {
                                "success": True,
                                "code": result.get("code", ""),
                                "provider": "groq",
                                "mode": "llm"
                            }
            
            except Exception as e:
                print(f"⚠️ {prov}で生成失敗: {e}")
                continue
        
        # 全て失敗
        return {
            "success": False,
            "code": "",
            "provider": "none",
            "error": "All providers failed"
        }
    
    def _generate_template_code(self, prompt: str) -> str:
        """テンプレートコード生成（フォールバック用）"""
        return f"""# -*- coding: utf-8 -*-
\"\"\"
{prompt}

NOTE: This is a basic template.
Please implement the actual functionality.
\"\"\"

def main():
    \"\"\"Main function\"\"\"
    print("TODO: {prompt}")
    # Add implementation here
    pass

if __name__ == "__main__":
    main()
"""
    
    def diagnose(self) -> Dict[str, Any]:
        """診断情報を取得"""
        diag = {
            "default_provider": self.default_provider,
            "available_providers": self.get_available_providers(),
            "providers": {}
        }
        
        for name, provider in self.providers.items():
            if provider is None:
                diag["providers"][name] = {"available": False, "error": "Not initialized"}
            elif name == "local":
                diag["providers"][name] = {
                    "available": provider.is_available(),
                    "type": "local",
                    "model": provider.model if hasattr(provider, 'model') else "unknown"
                }
            elif name == "groq":
                is_available = False
                if hasattr(provider, 'llm_available'):
                    is_available = provider.llm_available
                elif hasattr(provider, 'api_key') and provider.api_key:
                    is_available = True
                
                diag["providers"][name] = {
                    "available": is_available,
                    "type": "cloud"
                }
        
        return diag
    
    def format_diagnosis(self) -> str:
        """診断情報をフォーマット"""
        diag = self.diagnose()
        
        output = []
        output.append("📡 UniversalLLMConnector 診断")
        output.append("=" * 60)
        output.append(f"デフォルトプロバイダー: {diag['default_provider']}")
        output.append(f"利用可能: {', '.join(diag['available_providers']) or 'None'}")
        output.append("")
        output.append("📊 プロバイダー状態:")
        
        for name, info in diag["providers"].items():
            status = "✅" if info.get("available") else "❌"
            output.append(f"  {status} {name}: {info.get('type', 'unknown')}")
            if name == "local" and info.get("available"):
                output.append(f"      モデル: {info.get('model')}")
        
        return "\n".join(output)