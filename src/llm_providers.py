"""
Configuração e gerenciamento de provedores de LLM (Language Learning Models).
Agora usando sistema extensível com Open/Closed Principle.
Mantém compatibilidade total com código existente.
"""

# Importa o novo sistema de registro
from src.provider_registry import provider_registry

# Classe de compatibilidade que mantém a interface original
class LLMProvider:
    """
    Classe de compatibilidade que mantém a interface original.
    Delega todas as operações para o novo ProviderRegistry.
    """
    
    def __init__(self):
        """Inicializa usando o registro de provedores."""
        self.registry = provider_registry
    
    @property
    def providers(self):
        """Propriedade de compatibilidade para acessar provedores."""
        all_providers = self.registry.get_all_providers_info()
        
        # Converte para o formato antigo
        legacy_format = {}
        for name, info in all_providers.items():
            provider = self.registry.get_provider(name)
            legacy_format[name] = {
                "llm": provider.llm if hasattr(provider, 'llm') else None,
                "status": "available" if provider.is_available() else "unavailable",
                "speed": info.get("speed", "unknown"),
                "cost": info.get("cost", "unknown"),
                "current_model": info.get("current_model", "unknown")
            }
        
        return legacy_format
    
    @property
    def current_provider(self):
        """Propriedade de compatibilidade para provedor atual."""
        provider = self.registry.get_current_provider()
        return provider.get_name() if provider else None
    
    def get_llm(self, provider: str = None):
        """Compatibilidade: retorna o LLM do provedor especificado ou ativo."""
        return self.registry.get_llm(provider)
    
    def invoke_llm(self, message: str) -> str:
        """Compatibilidade: método unificado para invocar o LLM."""
        return self.registry.invoke_llm(message)
    
    def get_available_providers(self):
        """Compatibilidade: retorna informações sobre provedores disponíveis."""
        available = self.registry.get_available_providers()
        return {
            name: {
                "status": "available",
                "speed": provider.get_info().get("speed", "unknown"),
                "cost": provider.get_info().get("cost", "unknown")
            }
            for name, provider in available.items()
        }
    
    def switch_provider(self, provider: str) -> bool:
        """Compatibilidade: muda para um provedor específico."""
        return self.registry.switch_provider(provider)
    
    def get_provider_info(self, provider: str = None):
        """Compatibilidade: retorna informações detalhadas sobre um provedor."""
        return self.registry.get_provider_info(provider)
    
    def list_available_models(self, provider: str = None):
        """Compatibilidade: lista modelos disponíveis para um provedor."""
        return self.registry.list_available_models(provider)
    
    def get_performance_stats(self, provider: str = None):
        """Compatibilidade: retorna estatísticas de performance de um provedor."""
        return self.registry.get_performance_stats(provider)
    
    def is_any_provider_available(self) -> bool:
        """Compatibilidade: verifica se algum provedor está disponível."""
        return self.registry.is_any_provider_available()
    
    def is_groq_available(self) -> bool:
        """Compatibilidade: verifica se o Groq está disponível."""
        groq_provider = self.registry.get_provider("groq")
        return groq_provider.is_available() if groq_provider else False
    
    def switch_model(self, provider: str, model: str) -> bool:
        """Compatibilidade: troca o modelo de um provedor específico."""
        return self.registry.switch_model(provider, model)
    
    def get_current_model(self, provider: str = None) -> str:
        """Compatibilidade: retorna o modelo atual de um provedor."""
        return self.registry.get_current_model(provider)


# Instância global que mantém compatibilidade
llm_manager = LLMProvider()

# Exporta também o registry para uso avançado
__all__ = ['llm_manager', 'provider_registry'] 