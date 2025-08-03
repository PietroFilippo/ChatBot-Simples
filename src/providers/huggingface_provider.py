"""
Implementação do provedor Hugging Face Inference Providers API (2024).
Oferece acesso a modelos através da nova API unificada.
"""

import os
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import requests
from src.interfaces import ILLMProvider
from src.config import GlobalConfig

# Carrega as variáveis de ambiente
load_dotenv()


class HuggingFaceProvider(ILLMProvider):
    """Provedor Hugging Face implementando a interface ILLMProvider."""
    
    def __init__(self):
        """Inicializa o provedor Hugging Face."""
        self.name = "huggingface"
        self.base_url = "https://router.huggingface.co/v1/chat/completions"
        self.models_url = "https://router.huggingface.co/v1/models"
        self.current_model = os.getenv("HUGGINGFACE_DEFAULT_MODEL", "google/gemma-2-2b-it")
        self.status = "unavailable"
        self.api_key = None
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        # Modelos testados que funcionaram
        self.available_models = [
            "google/gemma-2-2b-it",
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            "microsoft/phi-4",
            "Qwen/Qwen2.5-Coder-32B-Instruct",
            "deepseek-ai/DeepSeek-R1"
        ]
        
        self._setup()
    
    def _setup(self):
        """Configura o provedor Hugging Face."""
        try:
            self.api_key = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
            if self.api_key:
                # Marca como disponível se a chave existe e tem o formato correto
                if self.api_key.startswith('hf_') and len(self.api_key) > 30:
                    self.status = "available"
                    # Mostra configurações globais que serão usadas
                    params = GlobalConfig.get_generation_params()
                    print(f"Hugging Face Provider configurado com modelo {self.current_model}")
                    print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                else:
                    print("Chave Hugging Face com formato inválido")
                    self.status = "unavailable"
            else:
                print("HUGGINGFACE_API_KEY ou HF_TOKEN não encontrada")
                self.status = "unavailable"
        except Exception as e:
            print(f"Erro ao configurar Hugging Face: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        return self.status == "available"
    
    def generate_response(self, message: str, **kwargs) -> str:
        """Gera uma resposta para a mensagem usando a nova API."""
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            # Atualiza estatísticas
            self.request_count += 1
            self.last_request_time = time.time()
            
            # Usa configurações globais centralizadas
            # kwargs ainda podem sobrescrever se necessário
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
                    content = result["choices"][0]["message"]["content"]
                    return content.strip() if content else "Resposta vazia"
                else:
                    return "Formato de resposta inesperado"
                    
            elif response.status_code == 503:
                return "Modelo está inicializando. Tente novamente em alguns segundos."
            else:
                self.error_count += 1
                error_detail = response.text[:200] if response.text else "Erro desconhecido"
                return f"Erro na API: {response.status_code} - {error_detail}"
                
        except requests.exceptions.Timeout:
            self.error_count += 1
            return "Timeout na requisição. Tente novamente."
        except Exception as e:
            self.error_count += 1
            return f"Erro na requisição: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        return {
            "name": self.name,
            "description": "Hugging Face Inference Providers - Acesso unificado a múltiplos modelos",
            "status": self.status,
            "current_model": self.current_model,
            "total_models": len(self.available_models),
            "rate_limit": "Varia por modelo e plano",
            "website": "https://huggingface.co",
            "pricing": "Tier gratuito + PRO disponível",
            "speed": "médio",  # Compatibilidade com interface
            "cost": "gratuito",  # Compatibilidade com interface
            "features": [
                "91+ modelos disponíveis",
                "API OpenAI-compatible",
                "Múltiplos provedores de inferência",
                "Modelos de última geração",
                "Suporte a conversação",
                "Rate limits generosos"
            ],
            "advantages": [
                "Acesso a modelos cutting-edge",
                "API unificada",
                "Sem vendor lock-in",
                "Performance empresarial"
            ]
        }
    
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        """Troca o modelo ativo."""
        if model not in self.available_models:
            print(f"Modelo '{model}' não está na lista de modelos testados")
            return False
        
        self.current_model = model
        print(f"Modelo alterado para {model} no {self.name}")
        return True
    
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        return self.current_model
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance."""
        uptime = time.time() - (self.last_request_time or time.time())
        success_rate = ((self.request_count - self.error_count) / max(self.request_count, 1)) * 100
        
        return {
            "requests_made": self.request_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "last_request": self.last_request_time,
            "uptime_minutes": max(0, uptime / 60),
            "status": self.status,
            "rate_limit_info": "Varia por modelo (consulte documentação)"
        } 