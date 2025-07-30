"""
Configuração e gerenciamento de provedores de LLM (Language Learning Models).
"""

from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import os
import warnings
# Carrega as variáveis de ambiente
load_dotenv()
warnings.filterwarnings("ignore")

class LLMProvider:
    """Classe para gerenciar múltiplos provedores de LLM."""
    
    def __init__(self):
        self.providers = {}
        self.current_provider = None
        self._setup_providers()
    
    def _setup_providers(self):
        """Configura os provedores disponíveis."""
        self._setup_groq()
        self._select_best_provider()

    def _setup_groq(self):
        """Configura o provedor Groq (gratuito)."""
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                default_model = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
                from langchain_groq import ChatGroq
                
                self.providers["groq"] = {
                    "llm": ChatGroq(
                        api_key=groq_key,
                        model=default_model,
                        criatividade=0.7,
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
                print("Groq API key não encontrada")
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
        available = [p for p, info in self.providers.items() if info["status"] == "available"]
        self.current_provider = "groq" if "groq" in available else (available[0] if available else None)
        print(f"Provedor ativo: {self.current_provider}" if self.current_provider else "Nenhum provedor disponível")
    
    def get_llm(self, provider: Optional[str] = None):
        """Retorna o LLM do provedor especificado ou ativo."""
        target = provider or self.current_provider
        if target and target in self.providers:
            if self.providers[target]["status"] == "available":
                return self.providers[target]["llm"]
        return None
    
    def invoke_llm(self, message: str) -> str:
        """Método unificado para invocar LLM via provedor."""
        if not self.current_provider:
            return "Nenhum provedor LLM configurado. Configure uma API key."
        
        try:
            llm = self.get_llm()
            if llm is None:
                return f"Provedor {self.current_provider} não disponível."

            if self.current_provider == "groq":
                response = llm.invoke(message)
                return getattr(response, "content", str(response))
            else:
                return f"Provedor {self.current_provider} não implementado."
        
        except Exception as e:
            print(f"Erro ao invocar {self.current_provider}: {e}")
            return f"Erro na API {self.current_provider}: {str(e)}"
    
    def get_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """Retorna provedores disponíveis (placeholder)."""
        return {}
    
    def is_any_provider_available(self) -> bool:
        """Verifica se há provedor disponível."""
        return self.current_provider is not None

# Instância global (placeholder)
llm_manager = LLMProvider()

