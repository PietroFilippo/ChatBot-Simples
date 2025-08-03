"""
Implementação específica do provedor Groq.
Segue o Open/Closed Principle - extensível sem modificar código existente.
"""

import os
import time
import requests
from typing import Dict, List, Any
from dotenv import load_dotenv
from src.interfaces import ILLMProvider
from src.config import GlobalConfig

# Carrega as variáveis de ambiente
load_dotenv()


class GroqProvider(ILLMProvider):
    """Provedor Groq implementando a interface ILLMProvider."""
    
    def __init__(self):
        """Inicializa o provedor Groq."""
        self.name = "groq"
        self.llm = None
        self.current_model = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
        self.status = "unavailable"
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        self.available_models = [
            "llama3-70b-8192",
            "llama3-8b-8192"
        ]
        
        self._setup()
    
    def _setup(self):
        """Configura o provedor Groq."""
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                from langchain_groq import ChatGroq
                
                # Usa configurações globais centralizadas
                params = GlobalConfig.get_generation_params()
                
                self.llm = ChatGroq(
                    api_key=groq_key,
                    model=self.current_model,
                    temperature=params["temperature"],
                    max_tokens=params["max_tokens"]
                )
                self.status = "available"
                print(f"Groq Provider configurado com modelo {self.current_model}")
                print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
            else:
                print("GROQ_API_KEY não encontrada")
                self.status = "unavailable"
        except Exception as e:
            print(f"Erro ao configurar Groq: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        return self.status == "available"
    
    def generate_response(self, message: str, **kwargs) -> str:
        """Gera uma resposta para a mensagem."""
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            # Atualiza estatísticas
            self.request_count += 1
            self.last_request_time = time.time()
            
            response = self.llm.invoke(message)
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            self.error_count += 1
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        return {
            "provider": self.name,
            "status": self.status,
            "speed": "fast",
            "cost": "free",
            "current_model": self.current_model,
            "description": "API ultra-rápida com modelos Llama 3",
            "context_length": "8192 tokens",
            "rate_limit": "30 requests/minute (gratuito)",
            "advantages": ["Velocidade excepcional", "Modelos potentes", "100% Gratuito"]
        }
    
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        """Troca o modelo ativo."""
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key:
                print("GROQ_API_KEY não encontrada")
                return False
            
            from langchain_groq import ChatGroq
            
            # Usa configurações globais centralizadas
            params = GlobalConfig.get_generation_params()
            
            self.llm = ChatGroq(
                api_key=groq_key,
                model=model,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"]
            )
            self.current_model = model
            print(f"Modelo alterado para {model} no {self.name}")
            print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
            return True
            
        except Exception as e:
            print(f"Erro ao trocar modelo: {e}")
            return False
    
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        return self.current_model
    
    def _make_request(self, payload: Dict) -> str:
        """Faz uma requisição para a API do groq."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{self.current_model}"
        
        try:
            self.request_count += 1
            self.last_request_time = time.time()
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Diferentes formatos de resposta dependendo do modelo
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text']
                    elif 'text' in result[0]:
                        return result[0]['text']
                elif isinstance(result, dict):
                    if 'generated_text' in result:
                        return result['generated_text']
                    elif 'text' in result:
                        return result['text']
                
                return str(result)
                
            elif response.status_code == 503:
                # Modelo está carregando
                return "Modelo está inicializando. Tente novamente em alguns segundos."
            else:
                self.error_count += 1
                return f"Erro na API: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            self.error_count += 1
            return "Timeout na requisição. Tente novamente."
        except Exception as e:
            self.error_count += 1
            return f"Erro na requisição: {str(e)}"
    
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
            "rate_limit_info": "30 requests/minuto (gratuito)"
        } 