"""
Sistema de Bootstrap para Injeção de Dependências.
Configura todas as dependências do sistema.
"""

from src.dependency_container import container
from src.interfaces import (
    ILLMService, IProviderRegistry, IChatbotService, 
    ISentimentService, ISummarizerService
)
from src.services.llm_service import LLMService
from src.provider_registry import provider_registry
from src.chatbot import IntelligentChatbot


def configure_dependencies():
    """
    Configura todas as dependências do sistema.
    Implementa o padrão Composition Root.
    """
    print("Configurando sistema de dependências")
    
    # 1. Registra o Provider Registry como singleton
    container.register_singleton(IProviderRegistry, provider_registry)
    
    # 2. Registra o LLM Service como singleton
    def llm_service_factory():
        registry = container.resolve(IProviderRegistry)
        return LLMService(registry)
    
    container.register_singleton_factory(ILLMService, llm_service_factory)
    
    # 3. Registra Chatbot Service como factory (transient)
    def chatbot_factory(personality: str = "helpful", memory_size: int = 10):
        llm_service = container.resolve(ILLMService)
        return IntelligentChatbot(llm_service, personality, memory_size)
    
    container.register_transient(IChatbotService, lambda: chatbot_factory())
    
    print("Dependências configuradas com sucesso.")


def get_chatbot_with_di(personality: str = "helpful", memory_size: int = 10) -> IChatbotService:
    """
    Factory method para criar chatbot com DI.
    
    Args:
        personality: Personalidade do chatbot
        memory_size: Tamanho da memória
        
    Returns:
        Instância do chatbot com dependências injetadas
    """
    llm_service = container.resolve(ILLMService)
    return IntelligentChatbot(llm_service, personality, memory_size)


def get_llm_service() -> ILLMService:
    """
    Obtém o serviço LLM configurado.
    
    Returns:
        Instância do serviço LLM
    """
    return container.resolve(ILLMService)


def get_provider_registry() -> IProviderRegistry:
    """
    Obtém o registro de provedores.
    
    Returns:
        Instância do registro de provedores
    """
    return container.resolve(IProviderRegistry)


def get_dependency_info() -> dict:
    """
    Retorna informações sobre as dependências registradas.
    
    Returns:
        Dicionário com informações das dependências
    """
    return {
        "registered_interfaces": container.get_registered_interfaces(),
        "provider_registry_available": container.is_registered(IProviderRegistry),
        "llm_service_available": container.is_registered(ILLMService),
        "chatbot_service_available": container.is_registered(IChatbotService)
    }


# Configuração automática quando o módulo é importado
configure_dependencies() 