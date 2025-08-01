"""
Interfaces abstratas para o sistema de IA Generativa.
Abertas para extensão, fechadas para modificação.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class ILLMProvider(ABC):
    """Interface abstrata para provedores de LLM."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        pass
    
    @abstractmethod
    def generate_response(self, message: str) -> str:
        """Gera uma resposta para a mensagem."""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        pass
    
    @abstractmethod
    def switch_model(self, model: str) -> bool:
        """Troca o modelo ativo."""
        pass
    
    @abstractmethod
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        pass
    
    @abstractmethod
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance."""
        pass


class IProviderRegistry(ABC):
    """Interface para registro de provedores."""
    
    @abstractmethod
    def register_provider(self, provider: ILLMProvider) -> bool:
        """Registra um novo provedor."""
        pass
    
    @abstractmethod
    def unregister_provider(self, provider_name: str) -> bool:
        """Remove um provedor."""
        pass
    
    @abstractmethod
    def get_provider(self, provider_name: str) -> Optional[ILLMProvider]:
        """Obtém um provedor específico."""
        pass
    
    @abstractmethod
    def get_available_providers(self) -> Dict[str, ILLMProvider]:
        """Retorna todos os provedores disponíveis."""
        pass
    
    @abstractmethod
    def get_current_provider(self) -> Optional[ILLMProvider]:
        """Retorna o provedor atual."""
        pass
    
    @abstractmethod
    def switch_provider(self, provider_name: str) -> bool:
        """Troca para um provedor específico."""
        pass 