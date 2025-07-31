"""
Configuração e gerenciamento de provedores de LLM (Language Learning Models).
Integração com Groq API e preparação para múltiplos provedores.
"""

import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import warnings

# Carrega as variáveis de ambiente
load_dotenv()

class LLMProvider:
    """Classe para gerenciar múltiplos provedores de LLM."""
    
    def __init__(self):
        self.providers = {}
        self.current_provider = None
        self._setup_providers()
    
    def _setup_providers(self):
        """Configura os provedores disponíveis."""
        # 1. Groq API
        self._setup_groq()
        
        # 2. Espaço para futuras APIs
        # Seleciona o melhor provedor disponível
        self._select_best_provider()
    
    def _setup_groq(self):
        """Configura o provedor Groq (gratuito)."""
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                # Modelo padrão
                default_model = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
                
                # Importar somente quando necessário para evitar erros
                from langchain_groq import ChatGroq
                
                self.providers["groq"] = {
                    "llm": ChatGroq(
                        api_key=groq_key,
                        model=default_model,
                        temperature=0.7,
                        max_tokens=1000
                    ),
                    "status": "available",
                    "speed": "fast",
                    "cost": "free",
                    "current_model": default_model
                }
                print("Groq API configurada com sucesso")
            else:
                self.providers["groq"] = {
                    "llm": None,
                    "status": "unavailable", 
                    "speed": "fast",
                    "cost": "free",
                    "current_model": None
                }
                print("⚠️ Groq API key não encontrada")
        except Exception as e:
            print(f"Erro ao configurar Groq: {e}")
            self.providers["groq"] = {
                "llm": None,
                "status": "error",
                "speed": "fast", 
                "cost": "free",
                "current_model": None
            }
    
    def _select_best_provider(self):
        """Seleciona o melhor provedor disponível."""
        # Ordem de preferência: Groq > Futuras APIs
        available_providers = [name for name, info in self.providers.items() 
                             if info["status"] == "available"]
        
        if "groq" in available_providers:
            self.current_provider = "groq"
        elif available_providers:
            self.current_provider = available_providers[0]
        else:
            self.current_provider = None
        
        if self.current_provider:
            print(f"Provedor ativo: {self.current_provider}")
        else:
            print("Nenhum provedor disponível")
    
    def get_llm(self, provider: Optional[str] = None):
        """Retorna o LLM do provedor especificado ou ativo."""
        target_provider = provider or self.current_provider
        
        if target_provider and target_provider in self.providers:
            provider_info = self.providers[target_provider]
            if provider_info["status"] == "available":
                return provider_info["llm"]
        
        return None
    
    def invoke_llm(self, message: str) -> str:
        """
        Método unificado para invocar o LLM independente do provedor.
        
        Args:
            message: Mensagem para enviar ao LLM
            
        Returns:
            Resposta do LLM ou mensagem de erro
        """
        if not self.current_provider:
            return "Nenhum provedor LLM configurado. Configure uma API key."
        
        try:
            llm = self.get_llm()
            
            if llm is None:
                return f"Provedor {self.current_provider} não disponível. Verifique a configuração."
            
            # Para Groq, usar invoke
            if self.current_provider == "groq":
                response = llm.invoke(message)
                # Extrair conteúdo da resposta
                if hasattr(response, 'content'):
                    return response.content
                else:
                    return str(response)
            
            # Espaço para outros provedores no futuro
            else:
                return f"Provedor {self.current_provider} não implementado!"
                
        except Exception as e:
            print(f"Erro ao invocar {self.current_provider}: {e}")
            return f"Erro na API {self.current_provider}: {str(e)}"
    
    def get_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """Retorna informações sobre provedores disponíveis."""
        return {
            provider: {
                "status": info["status"],
                "speed": info["speed"],
                "cost": info["cost"]
            }
            for provider, info in self.providers.items()
        }
    
    def switch_provider(self, provider: str) -> bool:
        """Muda para um provedor específico."""
        if provider not in self.providers:
            print(f"Provedor '{provider}' não existe")
            return False
        
        if self.providers[provider]["status"] != "available":
            print(f"Provedor '{provider}' não está disponível")
            return False
        
        self.current_provider = provider
        print(f"Mudando para provedor: {provider}")
        return True
    
    def get_provider_info(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Retorna informações detalhadas sobre um provedor específico."""
        target_provider = provider or self.current_provider
        
        if not target_provider or target_provider not in self.providers:
            return {"error": f"Provedor '{target_provider}' não encontrado"}
        
        info = self.providers[target_provider].copy()
        
        # Adiciona informações extras baseadas no provedor
        if target_provider == "groq":
            info.update({
                "provider": "groq",
                "description": "API ultra-rápida com modelos Llama 3",
                "model": "llama3-70b-8192",
                "context_length": "8192 tokens",
                "rate_limit": "30 requests/minute (gratuito)",
                "advantages": ["Velocidade excepcional", "Modelos potentes", "100% Gratuito"]
            })
        
        # Espaço para outras APIs no futuro
        
        return info
    
    def list_available_models(self, provider: Optional[str] = None) -> List[str]:
        """Lista modelos disponíveis para um provedor."""
        target_provider = provider or self.current_provider
        
        model_lists = {
            "groq": [
                "llama3-70b-8192",
                "llama3-8b-8192"
            ]

        }
        
        return model_lists.get(target_provider, [])
    
    def get_performance_stats(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Retorna estatísticas de performance de um provedor."""
        target_provider = provider or self.current_provider
        
        stats = {
            "groq": {
                "avg_response_time": "~1-3s",
                "reliability": "99%",
                "cost_per_request": "R$ 0,00",
                "quality": "Excelente"
            }
            # Espaço para outras APIs no futuro
        }
        
        return stats.get(target_provider, {})

    def is_any_provider_available(self) -> bool:
        """Verifica se algum provedor está disponível."""
        return self.current_provider is not None
    
    def is_groq_available(self) -> bool:
        """Verifica se o Groq está disponível."""
        return (self.providers.get("groq", {}).get("status") == "available")

    def switch_model(self, provider: str, model: str) -> bool:
        """Troca o modelo de um provedor específico."""
        if provider not in self.providers:
            print(f"Provedor '{provider}' não existe")
            return False
        
        if self.providers[provider]["status"] != "available":
            print(f"Provedor '{provider}' não está disponível")
            return False
        
        # Verifica se o modelo é válido para o provedor
        available_models = self.list_available_models(provider)
        if model not in available_models:
            print(f"Modelo '{model}' não disponível para {provider}")
            return False
        
        try:
            if provider == "groq":
                # Recria a instância do ChatGroq com o novo modelo
                groq_key = os.getenv("GROQ_API_KEY")
                from langchain_groq import ChatGroq
                
                self.providers["groq"]["llm"] = ChatGroq(
                    api_key=groq_key,
                    model=model,
                    temperature=0.7,
                    max_tokens=1000
                )
                self.providers["groq"]["current_model"] = model
                
            # Espaço para outros provedores no futuro
            
            print(f"Modelo alterado para {model} no {provider}")
            return True
            
        except Exception as e:
            print(f"Erro ao trocar modelo: {e}")
            return False
    
    def get_current_model(self, provider: Optional[str] = None) -> str:
        """Retorna o modelo atual de um provedor."""
        target_provider = provider or self.current_provider
        
        if target_provider and target_provider in self.providers:
            return self.providers[target_provider].get("current_model", "Unknown")
        
        return "Unknown"

# Instância global do gerenciador de LLM
llm_manager = LLMProvider() 