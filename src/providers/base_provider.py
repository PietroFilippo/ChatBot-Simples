"""
Classe base para eliminar a duplicação de código entre provedores de LLM.
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from src.interfaces import ILLMProvider
from src.config import GlobalConfig


class BaseProvider(ILLMProvider, ABC):
    """
    Classe base para todos os provedores de LLM para eliminar a duplicação de código.
    Implementa funcionalidade comum que todos os provedores compartilham.
    """
    
    def __init__(self, name: str, available_models: List[str]):
        """Inicializa o provedor base com atributos comuns."""
        self.name = name
        self.available_models = available_models
        self.status = "unavailable"
        # Não defina current_model aqui - deixe as subclasses lidarem com isso
        
        # Rastreamento de estatísticas (comum a todos os provedores)
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        # Inicializa a configuração específica do provedor
        self._setup()
    
    @abstractmethod
    def _setup(self):
        """Lógica de configuração específica do provedor. Deve ser implementada pelas subclasses."""
        pass
    
    @abstractmethod
    def _generate_response_impl(self, message: str, **kwargs) -> str:
        """Gerar resposta específica do provedor. Deve ser implementada pelas subclasses."""
        pass
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        return self.status == "available"
    
    def get_available_models(self) -> List[str]:
        """Retorna os modelos disponíveis."""
        return self.available_models.copy()
    
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        return getattr(self, 'current_model', None)
    
    def generate_response(self, message: str, **kwargs) -> str:
        """
        Gera resposta com rastreamento de estatísticas comuns.
        Delega a geração real para _generate_response_impl.
        """
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            # Rastreamento de estatísticas comuns
            self.request_count += 1
            self.last_request_time = time.time()
            
            # Delega para a implementação específica do provedor
            return self._generate_response_impl(message, **kwargs)
            
        except Exception as e:
            self.error_count += 1
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas comuns para todos os provedores."""
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "last_request_time": self.last_request_time,
            "success_rate": (
                (self.request_count - self.error_count) / self.request_count 
                if self.request_count > 0 else 0
            )
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de desempenho para todos os provedores."""
        uptime = time.time() - (self.last_request_time or time.time())
        success_rate = ((self.request_count - self.error_count) / max(self.request_count, 1)) * 100
        
        return {
            "requests_made": self.request_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "last_request": self.last_request_time,
            "uptime_minutes": max(0, uptime / 60),
            "status": self.status,
            "provider_name": self.name
        } 