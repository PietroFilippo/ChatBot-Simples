"""
Classe base para eliminar a duplicação de código entre provedores de LLM.
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from src.interfaces import ILLMProvider
from src.config import GlobalConfig

logger = GlobalConfig.get_logger('base_provider')


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
        self.validation_error_count = 0  # Novo: erros de validação pós-resposta
        self.last_request_time = None
        
        # Inicializa a configuração específica do provedor
        self._setup()
        logger.info(f"Provedor {self.name} inicializado")
    
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
            logger.warning(f"Provedor {self.name} não disponível")
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            # Rastreamento de estatísticas comuns
            self.request_count += 1
            self.last_request_time = time.time()
            
            logger.debug(f"Gerando resposta via {self.name} (request #{self.request_count})")
            
            # Delega para a implementação específica do provedor
            response = self._generate_response_impl(message, **kwargs)
            
            logger.debug(f"Resposta gerada: {len(response) if response else 0} chars")
            return response
            
        except Exception as e:
            self.error_count += 1
            error_msg = f"Erro na API {self.name}: {str(e)}"
            logger.error(f"Erro no provedor {self.name}: {e}")
            return error_msg
    
    def increment_validation_error(self, error_type: str = "validation"):
        """
        Incrementa contador de erros de validação pós-resposta.
        
        Args:
            error_type: Tipo do erro para logging
        """
        self.validation_error_count += 1
        logger.warning(f"Erro de {error_type} incrementado para {self.name}: total {self.validation_error_count}")
    
    def get_total_errors(self) -> int:
        """Retorna o total de erros (API + validação)."""
        return self.error_count + self.validation_error_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas comuns para todos os provedores."""
        total_errors = self.get_total_errors()
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "validation_error_count": self.validation_error_count,
            "total_errors": total_errors,
            "last_request_time": self.last_request_time,
            "success_rate": (
                (self.request_count - total_errors) / self.request_count 
                if self.request_count > 0 else 0
            )
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de desempenho para todos os provedores."""
        uptime = time.time() - (self.last_request_time or time.time())
        total_errors = self.get_total_errors()
        success_rate = ((self.request_count - total_errors) / max(self.request_count, 1)) * 100
        
        return {
            "requests_made": self.request_count,
            "api_errors": self.error_count,
            "validation_errors": self.validation_error_count,
            "total_errors": total_errors,
            "success_rate": f"{success_rate:.1f}%",
            "last_request": self.last_request_time,
            "uptime_minutes": max(0, uptime / 60),
            "status": self.status,
            "provider_name": self.name
        } 