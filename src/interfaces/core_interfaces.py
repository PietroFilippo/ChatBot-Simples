"""
Interfaces Segregadas - Core Interfaces.
Interfaces pequenas, específicas e coesas.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .composite_interfaces import ILLMProvider


# ========================================
# INTERFACES BÁSICAS - Core Contracts
# ========================================

class IIdentifiable(ABC):
    """Interface para objetos que têm identificação."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome/identificador."""
        pass


class IAvailabilityCheck(ABC):
    """Interface para verificação de disponibilidade."""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se está disponível."""
        pass


class IInformationProvider(ABC):
    """Interface para provedores de informação."""
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações gerais."""
        pass


class IPerformanceMetrics(ABC):
    """Interface para métricas de performance."""
    
    @abstractmethod
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance."""
        pass


# ========================================
# INTERFACES DE TEXTO - Text Processing
# ========================================

class ITextProcessor(ABC):
    """Interface base para processamento de texto."""
    
    @abstractmethod
    def process_text(self, text: str) -> str:
        """Processa um texto."""
        pass


class ITextGenerator(ABC):
    """Interface específica para geração de texto."""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Gera uma resposta a partir de um prompt."""
        pass


class ITextAnalyzer(ABC):
    """Interface específica para análise de texto."""
    
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analisa um texto e retorna resultados."""
        pass


class ITextSummarizer(ABC):
    """Interface específica para resumo de texto."""
    
    @abstractmethod
    def summarize_text(self, text: str, length: int = 3) -> str:
        """Resume um texto."""
        pass


# ========================================
# INTERFACES DE MODELOS - Model Management
# ========================================

class IModelProvider(ABC):
    """Interface para provedores de modelos."""
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        pass
    
    @abstractmethod
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        pass


class IModelSwitcher(ABC):
    """Interface para troca de modelos."""
    
    @abstractmethod
    def switch_model(self, model: str) -> bool:
        """Troca para um modelo específico."""
        pass


# ========================================
# INTERFACES DE CONVERSAÇÃO - Conversation
# ========================================

class IConversationManager(ABC):
    """Interface para gerenciamento de conversas."""
    
    @abstractmethod
    def chat(self, message: str) -> str:
        """Processa uma mensagem de chat."""
        pass


class IMemoryManager(ABC):
    """Interface para gerenciamento de memória."""
    
    @abstractmethod
    def clear_memory(self) -> None:
        """Limpa a memória."""
        pass


class IConversationExporter(ABC):
    """Interface para exportação de conversas."""
    
    @abstractmethod
    def export_conversation(self) -> Dict[str, Any]:
        """Exporta a conversa."""
        pass


class IStatisticsProvider(ABC):
    """Interface para provedores de estatísticas."""
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas."""
        pass


# ========================================
# INTERFACES DE REGISTRO - Registry
# ========================================

class IRegistrable(ABC):
    """Interface para objetos que podem ser registrados."""
    pass


class IRegistry(ABC):
    """Interface base para registros."""
    
    @abstractmethod
    def register(self, name: str, item: Any) -> bool:
        """Registra um item."""
        pass
    
    @abstractmethod
    def unregister(self, name: str) -> bool:
        """Remove um item."""
        pass
    
    @abstractmethod
    def get(self, name: str) -> Optional[Any]:
        """Obtém um item."""
        pass


class IProviderRegistry(ABC):
    """Interface específica para registro de provedores."""
    
    @abstractmethod
    def register_provider(self, provider: 'ILLMProvider') -> bool:
        """Registra um provedor."""
        pass
    
    @abstractmethod
    def get_available_providers(self) -> Dict[str, Any]:
        """Retorna provedores disponíveis."""
        pass
    
    @abstractmethod
    def get_current_provider(self) -> Optional['ILLMProvider']:
        """Retorna o provedor atual."""
        pass
    
    @abstractmethod
    def switch_provider(self, provider_name: str) -> bool:
        """Troca de provedor."""
        pass 