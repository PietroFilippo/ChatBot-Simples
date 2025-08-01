"""
Implementação específica do provedor Groq.
Segue o Open/Closed Principle - extensível sem modificar código existente.
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from src.interfaces import ILLMProvider

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
                
                self.llm = ChatGroq(
                    api_key=groq_key,
                    model=self.current_model,
                    temperature=0.7,
                    max_tokens=1000
                )
                self.status = "available"
                print(f"✅ Groq Provider configurado com modelo {self.current_model}")
            else:
                print("⚠️ GROQ_API_KEY não encontrada")
                self.status = "unavailable"
        except Exception as e:
            print(f"❌ Erro ao configurar Groq: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        return self.status == "available"
    
    def generate_response(self, message: str) -> str:
        """Gera uma resposta para a mensagem."""
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            response = self.llm.invoke(message)
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
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
            print(f"❌ Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key:
                print("❌ GROQ_API_KEY não encontrada")
                return False
            
            from langchain_groq import ChatGroq
            
            self.llm = ChatGroq(
                api_key=groq_key,
                model=model,
                temperature=0.7,
                max_tokens=1000
            )
            self.current_model = model
            print(f"✅ Modelo alterado para {model} no {self.name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao trocar modelo: {e}")
            return False
    
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        return self.current_model
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance."""
        return {
            "avg_response_time": "~1-3s",
            "reliability": "99%",
            "cost_per_request": "R$ 0,00",
            "quality": "Excelente",
            "requests_per_minute": "30 (gratuito)"
        } 