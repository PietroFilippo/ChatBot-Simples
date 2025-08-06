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
from src.intelligent_chatbot import IntelligentChatbotV2
from src.config import GlobalConfig

logger = GlobalConfig.get_logger('bootstrap')


def configure_dependencies():
    """
    Configura todas as dependências do sistema.
    Implementa o padrão Composition Root.
    """
    logger.info("Iniciando configuração do sistema de dependências")
    
    try:
        # 1. Registra o Provider Registry como singleton
        container.register_singleton(IProviderRegistry, provider_registry)
        logger.debug("Provider Registry registrado como singleton")
        
        # 2. Registra o LLM Service como singleton
        def llm_service_factory():
            registry = container.resolve(IProviderRegistry)
            return LLMService(registry)
        
        container.register_singleton_factory(ILLMService, llm_service_factory)
        logger.debug("LLM Service registrado como singleton factory")
        
        # 3. Registra Chatbot Service como factory (transient) - VERSÃO INTELIGENTE
        def chatbot_factory(personality: str = "helpful"):
            llm_service = container.resolve(ILLMService)
            return IntelligentChatbotV2(llm_service, personality)
        
        container.register_transient(IChatbotService, lambda: chatbot_factory())
        logger.debug("Chatbot Service (IntelligentChatbotV2) registrado como transient")
        
        logger.info("Sistema de dependências configurado com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao configurar dependências: {e}")
        raise


def get_chatbot_with_di(personality: str = "helpful", memory_size: int = 10) -> IChatbotService:
    """
    Factory method para criar chatbot com DI.
    
    Args:
        personality: Personalidade do chatbot
        memory_size: O sistema inteligente gerencia automaticamente
        
    Returns:
        Instância do chatbot com dependências injetadas
    """
    try:
        if memory_size != 10:
            logger.debug(f"memory_size={memory_size} ignorado - Sistema inteligente gerencia automaticamente")
        
        llm_service = container.resolve(ILLMService)
        chatbot = IntelligentChatbotV2(llm_service, personality)
        
        logger.info(f"Chatbot criado com personalidade: {personality}")
        return chatbot
        
    except Exception as e:
        logger.error(f"Erro ao criar chatbot: {e}")
        raise


def get_llm_service() -> ILLMService:
    """
    Obtém o serviço LLM configurado.
    
    Returns:
        Instância do serviço LLM
    """
    try:
        service = container.resolve(ILLMService)
        logger.debug("Serviço LLM obtido com sucesso")
        return service
    except Exception as e:
        logger.error(f"Erro ao obter serviço LLM: {e}")
        raise


def get_provider_registry() -> IProviderRegistry:
    """
    Obtém o registro de provedores.
    
    Returns:
        Instância do registro de provedores
    """
    try:
        registry = container.resolve(IProviderRegistry)
        logger.debug("Registry de provedores obtido com sucesso")
        return registry
    except Exception as e:
        logger.error(f"Erro ao obter registry de provedores: {e}")
        raise


def get_dependency_info() -> dict:
    """
    Retorna informações sobre as dependências registradas.
    
    Returns:
        Dicionário com informações das dependências
    """
    try:
        info = {
            "registered_interfaces": container.get_registered_interfaces(),
            "provider_registry_available": container.is_registered(IProviderRegistry),
            "llm_service_available": container.is_registered(ILLMService),
            "chatbot_service_available": container.is_registered(IChatbotService),
            "chatbot_type": "IntelligentChatbotV2",
            "intelligent_context_enabled": True
        }
        
        logger.debug(f"Informações de dependência obtidas: {len(info)} itens")
        return info
        
    except Exception as e:
        logger.error(f"Erro ao obter informações de dependência: {e}")
        return {
            "error": str(e),
            "registered_interfaces": [],
            "provider_registry_available": False,
            "llm_service_available": False,
            "chatbot_service_available": False,
            "chatbot_type": "Error",
            "intelligent_context_enabled": False
        }


# Configuração automática quando o módulo é importado
try:
    configure_dependencies()
except Exception as e:
    logger.critical(f"Falha crítica na configuração de dependências: {e}")
    # Não re-raise aqui para evitar quebrar a importação do módulo 