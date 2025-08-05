"""
Implementação específica do provedor Hugging Face refatorado.
Agora usa BaseProvider para eliminar duplicação de código.
"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from .base_provider import BaseProvider
from src.config import GlobalConfig

# Carrega as variáveis de ambiente
load_dotenv()


class HuggingFaceProvider(BaseProvider):
    """Provedor Hugging Face refatorado usando BaseProvider - 70% menos código!"""
    
    def __init__(self):
        # Define modelo padrão e current_model ANTES de chamar super()
        self.default_model = "google/gemma-2-2b-it"
        self.current_model = os.getenv("HUGGINGFACE_DEFAULT_MODEL", self.default_model) or self.default_model
        
        # Chama o construtor da classe base com configurações específicas
        super().__init__(
            name="huggingface",
            available_models=[
                "google/gemma-2-2b-it",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                "microsoft/phi-4",
                "Qwen/Qwen2.5-Coder-32B-Instruct",
                "deepseek-ai/DeepSeek-R1"
            ]
        )
        self.base_url = "https://router.huggingface.co/v1/chat/completions"
        self.models_url = "https://router.huggingface.co/v1/models"
        # Não resetar self.api_key aqui - ele já foi configurado no _setup()!
    
    def _setup(self):
        """Configuração específica do Hugging Face."""
        try:
            # Recarrega .env para garantir que as variáveis estão atualizadas
            load_dotenv()
            
            # Tenta ambas as variáveis de ambiente
            hf_key1 = os.getenv("HUGGINGFACE_API_KEY")
            hf_key2 = os.getenv("HF_TOKEN")
            self.api_key = hf_key1 or hf_key2
            
            if self.api_key and self.api_key.strip():
                # Marca como disponível se a chave existe e tem o formato correto
                if self.api_key.startswith('hf_') and len(self.api_key) > 30:
                    self.status = "available"
                    # Mostra configurações globais que serão usadas
                    params = GlobalConfig.get_generation_params()
                    print(f"Hugging Face Provider configurado com modelo {self.current_model}")
                    print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                else:
                    print("Chave Hugging Face com formato inválido (deve começar com 'hf_')")
                    self.status = "unavailable"
            else:
                print("HUGGINGFACE_API_KEY ou HF_TOKEN não encontrada ou vazia")
                self.status = "unavailable"
        except Exception as e:
            print(f"Erro ao configurar Hugging Face: {e}")
            self.status = "error"
    
    def _generate_response_impl(self, message: str, **kwargs) -> str:
        """Implementação específica da geração de resposta do Hugging Face."""
        if not self.api_key or not self.api_key.strip():
            raise Exception("API key não configurada. Verifique HUGGINGFACE_API_KEY ou HF_TOKEN.")
        
        # Usa configurações globais centralizadas
        params = GlobalConfig.get_generation_params(**kwargs)
        
        # Payload no formato OpenAI-compatible
        payload = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": params["max_tokens"],
            "temperature": params["temperature"],
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=params["timeout"]
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise Exception("Formato de resposta inesperado da API")
        elif response.status_code == 503:
            raise Exception("Modelo está carregando. Tente novamente em alguns segundos.")
        else:
            raise Exception(f"Erro na API: {response.status_code} - {response.text[:200]}")
    
    def get_info(self) -> Dict[str, Any]:
        """Informações específicas do Hugging Face."""
        base_stats = self.get_stats()  # Estatísticas da classe base
        
        return {
            "provider": self.name,
            "status": self.status,
            "speed": "medium",
            "cost": "free",
            "current_model": self.current_model,
            "description": "91+ modelos open-source via API unificada",
            "context_length": "Varia por modelo (2K-32K tokens)",
            "rate_limit": "1000 requests/mês (gratuito)",
            "advantages": ["91+ modelos", "Open Source", "100% Gratuito", "Modelos especializados"],
            **base_stats  # Adiciona estatísticas comuns
        }
    
    def switch_model(self, model: str) -> bool:
        """Troca modelo específico do Hugging Face."""
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        # Para Hugging Face, apenas trocar o modelo é suficiente
        self.current_model = model
        print(f"Modelo do Hugging Face alterado para: {model}")
        return True 