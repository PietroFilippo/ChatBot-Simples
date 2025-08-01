"""
Interfaces de Casos de Uso - Use Case Interfaces.
Interfaces específicas para casos de uso do sistema.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


# ========================================
# INTERFACES DE CASOS DE USO - Analytics
# ========================================

class IAnalyticsProvider(ABC):
    """Interface para provedores de analytics."""
    
    @abstractmethod
    def get_usage_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        pass


class IHealthCheck(ABC):
    """Interface para verificação de saúde do sistema."""
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verifica a saúde do sistema."""
        pass


class ISystemInfo(ABC):
    """Interface para informações do sistema."""
    
    @abstractmethod
    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações do sistema."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Configuration
# ========================================

class IConfigurable(ABC):
    """Interface para objetos configuráveis."""
    
    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> bool:
        """Configura o objeto."""
        pass
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Retorna a configuração atual."""
        pass


class IPersonalizable(ABC):
    """Interface para personalização."""
    
    @abstractmethod
    def set_personality(self, personality: str) -> bool:
        """Define a personalidade."""
        pass
    
    @abstractmethod
    def get_personality(self) -> str:
        """Retorna a personalidade atual."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Validation
# ========================================

class ITextValidator(ABC):
    """Interface para validação de texto."""
    
    @abstractmethod
    def validate_text(self, text: str) -> Dict[str, Any]:
        """Valida um texto."""
        pass


class IInputSanitizer(ABC):
    """Interface para sanitização de entrada."""
    
    @abstractmethod
    def sanitize_input(self, input_text: str) -> str:
        """Sanitiza texto de entrada."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Export/Import
# ========================================

class IDataExporter(ABC):
    """Interface para exportação de dados."""
    
    @abstractmethod
    def export_json(self) -> str:
        """Exporta dados em JSON."""
        pass
    
    @abstractmethod
    def export_text(self) -> str:
        """Exporta dados em texto."""
        pass


class IDataImporter(ABC):
    """Interface para importação de dados."""
    
    @abstractmethod
    def import_json(self, json_data: str) -> bool:
        """Importa dados de JSON."""
        pass


class IFileOperations(ABC):
    """Interface para operações de arquivo."""
    
    @abstractmethod
    def save_to_file(self, filepath: str, content: str) -> bool:
        """Salva conteúdo em arquivo."""
        pass
    
    @abstractmethod
    def load_from_file(self, filepath: str) -> str:
        """Carrega conteúdo de arquivo."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Logging
# ========================================

class ILoggable(ABC):
    """Interface para objetos que podem fazer log."""
    
    @abstractmethod
    def log_event(self, level: str, message: str) -> None:
        """Registra um evento."""
        pass


class IAuditable(ABC):
    """Interface para auditoria."""
    
    @abstractmethod
    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Retorna trilha de auditoria."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Cache
# ========================================

class ICacheable(ABC):
    """Interface para objetos que podem ser cacheados."""
    
    @abstractmethod
    def get_cache_key(self) -> str:
        """Retorna chave de cache."""
        pass
    
    @abstractmethod
    def is_cache_valid(self) -> bool:
        """Verifica se o cache é válido."""
        pass


class ICacheManager(ABC):
    """Interface para gerenciamento de cache."""
    
    @abstractmethod
    def get_cached(self, key: str) -> Optional[Any]:
        """Obtém item do cache."""
        pass
    
    @abstractmethod
    def set_cache(self, key: str, value: Any, ttl: int = 300) -> None:
        """Define item no cache."""
        pass
    
    @abstractmethod
    def clear_cache(self) -> None:
        """Limpa o cache."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Error Handling
# ========================================

class IErrorHandler(ABC):
    """Interface para tratamento de erros."""
    
    @abstractmethod
    def handle_error(self, error: Exception) -> str:
        """Trata um erro e retorna mensagem amigável."""
        pass


class IFallbackProvider(ABC):
    """Interface para provedores de fallback."""
    
    @abstractmethod
    def get_fallback_response(self, context: str) -> str:
        """Retorna resposta de fallback."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Testing
# ========================================

class IMockable(ABC):
    """Interface para objetos que podem ser mockados."""
    
    @abstractmethod
    def create_mock(self) -> 'IMockable':
        """Cria uma versão mock do objeto."""
        pass


class ITestable(ABC):
    """Interface para objetos testáveis."""
    
    @abstractmethod
    def run_self_test(self) -> Dict[str, Any]:
        """Executa auto-teste."""
        pass


# ========================================
# INTERFACES DE CASOS DE USO - Security
# ========================================

class ISecureService(ABC):
    """Interface para serviços seguros."""
    
    @abstractmethod
    def validate_input_security(self, input_data: str) -> bool:
        """Valida segurança da entrada."""
        pass
    
    @abstractmethod
    def sanitize_output(self, output_data: str) -> str:
        """Sanitiza saída."""
        pass


class IRateLimited(ABC):
    """Interface para controle de taxa."""
    
    @abstractmethod
    def is_rate_limited(self, identifier: str) -> bool:
        """Verifica se há limite de taxa."""
        pass
    
    @abstractmethod
    def consume_rate_limit(self, identifier: str) -> bool:
        """Consome limite de taxa."""
        pass 