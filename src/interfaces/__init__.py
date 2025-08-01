"""
Módulo de Interfaces Segregadas.

Este módulo organiza interfaces em diferentes categorias:
- core_interfaces: Interfaces básicas e fundamentais
- composite_interfaces: Combinações de interfaces básicas
- use_case_interfaces: Interfaces específicas para casos de uso
"""

# Core Interfaces - Funcionalidades básicas
from .core_interfaces import (
    # Interfaces básicas
    IIdentifiable,
    IAvailabilityCheck,
    IInformationProvider,
    IPerformanceMetrics,
    
    # Interfaces de texto
    ITextProcessor,
    ITextGenerator,
    ITextAnalyzer,
    ITextSummarizer,
    
    # Interfaces de modelos
    IModelProvider,
    IModelSwitcher,
    
    # Interfaces de conversação
    IConversationManager,
    IMemoryManager,
    IConversationExporter,
    IStatisticsProvider,
    
    # Interfaces de registro
    IRegistrable,
    IRegistry,
    IProviderRegistry,
)

# Composite Interfaces - Combinações funcionais
from .composite_interfaces import (
    # LLM Provider interfaces
    IBasicLLMProvider,
    IAdvancedLLMProvider,
    IFullLLMProvider,
    ILLMProvider,  # Alias para IFullLLMProvider
    
    # Service interfaces
    IBasicLLMService,
    ILLMService,
    
    # Chatbot interfaces
    IBasicChatbot,
    IChatbotWithMemory,
    IChatbotWithStats,
    IChatbotService,
    
    # Text processing interfaces
    ISentimentAnalyzer,
    ISentimentService,  # Alias
    ISummarizerService,
    
    # Dependency injection
    IDependencyContainer,
)

# Use Case Interfaces - Casos de uso específicos
from .use_case_interfaces import (
    # Analytics
    IAnalyticsProvider,
    IHealthCheck,
    ISystemInfo,
    
    # Configuration
    IConfigurable,
    IPersonalizable,
    
    # Validation
    ITextValidator,
    IInputSanitizer,
    
    # Export/Import
    IDataExporter,
    IDataImporter,
    IFileOperations,
    
    # Logging
    ILoggable,
    IAuditable,
    
    # Cache
    ICacheable,
    ICacheManager,
    
    # Error handling
    IErrorHandler,
    IFallbackProvider,
    
    # Testing
    IMockable,
    ITestable,
    
    # Security
    ISecureService,
    IRateLimited,
)

# Principais interfaces para uso externo
__all__ = [
    # ===== INTERFACES PRINCIPAIS =====
    'ILLMProvider',      # Interface completa para provedores LLM
    'ILLMService',       # Interface para serviços LLM
    'IChatbotService',   # Interface completa para chatbots
    'ISentimentService', # Interface para análise de sentimento
    'ISummarizerService', # Interface para resumos
    'IProviderRegistry', # Interface para registro de provedores
    'IDependencyContainer', # Interface para DI container
    
    # ===== INTERFACES BÁSICAS =====
    'IIdentifiable',
    'IAvailabilityCheck',
    'ITextGenerator',
    'IConversationManager',
    'IMemoryManager',
    
    # ===== INTERFACES DE CASO DE USO =====
    'IHealthCheck',
    'IConfigurable',
    'ITextValidator',
    'IDataExporter',
    'ICacheable',
    'ITestable',
    
    # ===== INTERFACES GRADUAIS =====
    'IBasicLLMProvider',    # Funcionalidade mínima
    'IAdvancedLLMProvider', # Funcionalidade média
    'IFullLLMProvider',     # Funcionalidade completa
    
    'IBasicChatbot',        # Chat simples
    'IChatbotWithMemory',   # Chat com memória
    'IChatbotWithStats',    # Chat com estatísticas
] 