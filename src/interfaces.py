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


# Novas interfaces para Dependency Inversion

class ILLMService(ABC):
    """Interface para serviços de LLM - abstração de alto nível."""
    
    @abstractmethod
    def generate_response(self, message: str) -> str:
        """Gera uma resposta usando o LLM ativo."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se algum LLM está disponível."""
        pass
    
    @abstractmethod
    def get_current_provider_name(self) -> str:
        """Retorna o nome do provedor atual."""
        pass


class IChatbotService(ABC):
    """Interface para serviços de chatbot."""
    
    @abstractmethod
    def chat(self, message: str) -> str:
        """Processa uma mensagem de chat."""
        pass
    
    @abstractmethod
    def clear_memory(self) -> None:
        """Limpa a memória do chatbot."""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do chatbot."""
        pass


class ISentimentService(ABC):
    """Interface para serviços de análise de sentimento."""
    
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisa o sentimento de um texto."""
        pass
    
    @abstractmethod
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """Análise completa de sentimento."""
        pass


class ISummarizerService(ABC):
    """Interface para serviços de resumo."""
    
    @abstractmethod
    def summarize(self, text: str, num_sentences: int = 3) -> Dict[str, Any]:
        """Resume um texto."""
        pass
    
    @abstractmethod
    def summarize_comprehensive(self, text: str, **kwargs) -> Dict[str, Any]:
        """Resumo completo com múltiplas estratégias."""
        pass


class IDependencyContainer(ABC):
    """Interface para container de injeção de dependências."""
    
    @abstractmethod
    def register_singleton(self, interface: type, implementation: Any) -> None:
        """Registra um singleton."""
        pass
    
    @abstractmethod
    def register_transient(self, interface: type, factory: callable) -> None:
        """Registra uma factory transiente."""
        pass
    
    @abstractmethod
    def resolve(self, interface: type) -> Any:
        """Resolve uma dependência."""
        pass
    
    @abstractmethod
    def is_registered(self, interface: type) -> bool:
        """Verifica se uma interface está registrada."""
        pass 