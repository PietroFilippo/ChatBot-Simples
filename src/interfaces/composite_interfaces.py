"""
Interfaces Compostas - Composite Interfaces.
Combina interfaces segregadas para funcionalidades específicas.
"""

from abc import ABC
from .core_interfaces import (
    IIdentifiable, IAvailabilityCheck, IInformationProvider, IPerformanceMetrics,
    ITextGenerator, IModelProvider, IModelSwitcher,
    IConversationManager, IMemoryManager, IConversationExporter, IStatisticsProvider,
    ITextAnalyzer, ITextSummarizer, IProviderRegistry
)


# ========================================
# INTERFACES COMPOSTAS - LLM Provider
# ========================================

class IBasicLLMProvider(IIdentifiable, IAvailabilityCheck, ITextGenerator):
    """
    Interface básica para provedores LLM.
    Combina apenas funcionalidades essenciais.
    """
    pass


class IAdvancedLLMProvider(IBasicLLMProvider, IModelProvider, IModelSwitcher):
    """
    Interface avançada para provedores LLM.
    Inclui gerenciamento de modelos.
    """
    pass


class IFullLLMProvider(IAdvancedLLMProvider, IInformationProvider, IPerformanceMetrics):
    """
    Interface completa para provedores LLM.
    Inclui todas as funcionalidades disponíveis.
    """
    pass


# ========================================
# INTERFACES COMPOSTAS - Services
# ========================================

class IBasicLLMService(IAvailabilityCheck, ITextGenerator):
    """
    Interface básica para serviços LLM.
    Apenas funcionalidades essenciais.
    """
    pass


class ILLMService(IBasicLLMService, IIdentifiable):
    """
    Interface completa para serviços LLM de alto nível.
    """
    
    def get_current_provider_name(self) -> str:
        """Alias para get_name() para compatibilidade."""
        return self.get_name()


# ========================================
# INTERFACES COMPOSTAS - Chatbot
# ========================================

class IBasicChatbot(IConversationManager):
    """
    Interface básica para chatbots.
    Apenas conversação.
    """
    pass


class IChatbotWithMemory(IBasicChatbot, IMemoryManager):
    """
    Interface para chatbots com memória.
    """
    pass


class IChatbotWithStats(IChatbotWithMemory, IStatisticsProvider):
    """
    Interface para chatbots com estatísticas.
    """
    pass


class IChatbotService(IChatbotWithStats, IConversationExporter):
    """
    Interface completa para serviços de chatbot.
    """
    pass


# ========================================
# INTERFACES COMPOSTAS - Text Processing
# ========================================

class ISentimentAnalyzer(ITextAnalyzer):
    """
    Interface específica para análise de sentimento.
    """
    
    def analyze(self, text: str) -> dict:
        """Alias para analyze_text para compatibilidade."""
        return self.analyze_text(text)
    
    def analyze_comprehensive(self, text: str) -> dict:
        """Análise completa de sentimento."""
        return self.analyze_text(text)


class ISummarizerService(ITextSummarizer):
    """
    Interface específica para serviços de resumo.
    """
    
    def summarize(self, text: str, num_sentences: int = 3) -> dict:
        """Alias para summarize_text para compatibilidade."""
        result = self.summarize_text(text, num_sentences)
        return {"summary": result}
    
    def summarize_comprehensive(self, text: str, **kwargs) -> dict:
        """Resumo completo com múltiplas estratégias."""
        length = kwargs.get("num_sentences", 3)
        result = self.summarize_text(text, length)
        return {"summaries": {"main": {"summary": result}}}


# ========================================
# INTERFACES COMPOSTAS - Dependency Injection
# ========================================

class IDependencyContainer(ABC):
    """Interface para container de injeção de dependências."""
    
    def register_singleton(self, interface: type, implementation: any) -> None:
        """Registra um singleton."""
        pass
    
    def register_transient(self, interface: type, factory: callable) -> None:
        """Registra uma factory transiente."""
        pass
    
    def resolve(self, interface: type) -> any:
        """Resolve uma dependência."""
        pass
    
    def is_registered(self, interface: type) -> bool:
        """Verifica se uma interface está registrada."""
        pass


# ========================================
# ALIASES PARA COMPATIBILIDADE
# ========================================

# Aliases para manter compatibilidade com código existente
ILLMProvider = IFullLLMProvider
ISentimentService = ISentimentAnalyzer 