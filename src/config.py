"""
Configurações globais do sistema.
Centraliza todas as configurações para facilitar manutenção.
"""

import os
import logging
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class GlobalConfig:
    """Classe para configurações globais do sistema."""
    
    # Configurações de geração (todos os providers)
    DEFAULT_TEMPERATURE = float(os.getenv("GLOBAL_TEMPERATURE", "0.7"))
    DEFAULT_MAX_TOKENS = int(os.getenv("GLOBAL_MAX_TOKENS", "1000"))
    
    # Configurações de API
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    AUTO_RETRY = os.getenv("AUTO_RETRY", "true").lower() == "true"
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Configurações de log
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    @classmethod
    def setup_logging(cls) -> logging.Logger:
        """
        Configura o sistema de logging estruturado.
        
        Returns:
            Logger configurado
        """
        # Configura o logger raiz
        logger = logging.getLogger('chatbot')
        logger.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))
        
        # Remove handlers existentes para evitar duplicação
        if logger.handlers:
            logger.handlers.clear()
        
        # Formatter estruturado
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para arquivo em produção
        if not cls.DEBUG_MODE:
            try:
                os.makedirs('logs', exist_ok=True)
                file_handler = logging.FileHandler('logs/chatbot.log', encoding='utf-8')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Não foi possível criar log de arquivo: {e}")
        
        # Configura loggers de bibliotecas externas para reduzir spam
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        
        logger.info("Sistema de logging configurado")
        return logger
    
    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        """
        Retorna um logger configurado.
        
        Args:
            name: Nome do logger (usa o módulo se não especificado)
            
        Returns:
            Logger configurado
        """
        if name is None:
            name = 'chatbot'
        
        return logging.getLogger(f'chatbot.{name}')
    
    @classmethod
    def get_generation_params(cls, **overrides) -> Dict[str, Any]:
        """
        Retorna parâmetros de geração padronizados.
        
        Args:
            **overrides: Parâmetros para sobrescrever os padrões
            
        Returns:
            Dicionário com parâmetros de geração
        """
        params = {
            "temperature": cls.DEFAULT_TEMPERATURE,
            "max_tokens": cls.DEFAULT_MAX_TOKENS,
            "timeout": cls.API_TIMEOUT
        }
        
        # Aplica overrides se fornecidos
        params.update(overrides)
        
        return params
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """
        Retorna configurações de API.
        
        Returns:
            Dicionário com configurações de API
        """
        return {
            "timeout": cls.API_TIMEOUT,
            "auto_retry": cls.AUTO_RETRY,
            "max_retries": cls.MAX_RETRIES
        }
    
    @classmethod
    def get_debug_info(cls) -> Dict[str, Any]:
        """
        Retorna informações de debug.
        
        Returns:
            Dicionário com informações de configuração
        """
        return {
            "temperature": cls.DEFAULT_TEMPERATURE,
            "max_tokens": cls.DEFAULT_MAX_TOKENS,
            "api_timeout": cls.API_TIMEOUT,
            "auto_retry": cls.AUTO_RETRY,
            "max_retries": cls.MAX_RETRIES,
            "log_level": cls.LOG_LEVEL,
            "debug_mode": cls.DEBUG_MODE
        }


# Inicializa o logging quando o módulo é importado
GlobalConfig.setup_logging() 