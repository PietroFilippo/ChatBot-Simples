"""
Sistema de registro extensível para provedores de LLM.
Aberto para extensão, fechado para modificação.
"""

from typing import Dict, List, Any, Optional
from src.interfaces import ILLMProvider, IProviderRegistry
from src.providers import GroqProvider


class ProviderRegistry(IProviderRegistry):
    """
    Registro extensível de provedores de LLM.
    Permite adicionar novos provedores sem modificar código existente.
    """
    
    def __init__(self):
        """Inicializa o registro de provedores."""
        self._providers: Dict[str, ILLMProvider] = {}
        self._current_provider: Optional[ILLMProvider] = None
        
        # Auto-registro dos provedores padrão
        self._auto_register_default_providers()
        
        # Seleciona o melhor provedor disponível
        self._select_best_provider()
    
    def _auto_register_default_providers(self):
        """Registra automaticamente os provedores padrão."""
        try:
            # Registra Groq
            groq_provider = GroqProvider()
            self.register_provider(groq_provider)
            
        except Exception as e:
            print(f"⚠️ Erro no auto-registro: {e}")
    
    def register_provider(self, provider: ILLMProvider) -> bool:
        """
        Registra um novo provedor.
        
        Args:
            provider: Instância do provedor que implementa ILLMProvider
            
        Returns:
            True se registrado com sucesso, False caso contrário
        """
        try:
            provider_name = provider.get_name()
            
            if provider_name in self._providers:
                print(f"⚠️ Provedor '{provider_name}' já existe. Substituindo...")
            
            self._providers[provider_name] = provider
            print(f"✅ Provedor '{provider_name}' registrado com sucesso")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao registrar provedor: {e}")
            return False
    
    def unregister_provider(self, provider_name: str) -> bool:
        """
        Remove um provedor do registro.
        
        Args:
            provider_name: Nome do provedor a ser removido
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        if provider_name not in self._providers:
            print(f"⚠️ Provedor '{provider_name}' não encontrado")
            return False
        
        # Se for o provedor atual, seleciona outro
        if self._current_provider and self._current_provider.get_name() == provider_name:
            del self._providers[provider_name]
            self._select_best_provider()
        else:
            del self._providers[provider_name]
        
        print(f"✅ Provedor '{provider_name}' removido")
        return True
    
    def get_provider(self, provider_name: str) -> Optional[ILLMProvider]:
        """
        Obtém um provedor específico.
        
        Args:
            provider_name: Nome do provedor
            
        Returns:
            Instância do provedor ou None se não encontrado
        """
        return self._providers.get(provider_name)
    
    def get_available_providers(self) -> Dict[str, ILLMProvider]:
        """
        Retorna todos os provedores disponíveis.
        
        Returns:
            Dicionário com provedores disponíveis
        """
        return {
            name: provider for name, provider in self._providers.items()
            if provider.is_available()
        }
    
    def get_current_provider(self) -> Optional[ILLMProvider]:
        """
        Retorna o provedor atual.
        
        Returns:
            Provedor atual ou None se nenhum disponível
        """
        return self._current_provider
    
    def switch_provider(self, provider_name: str) -> bool:
        """
        Troca para um provedor específico.
        
        Args:
            provider_name: Nome do provedor
            
        Returns:
            True se trocou com sucesso, False caso contrário
        """
        provider = self.get_provider(provider_name)
        
        if not provider:
            print(f"❌ Provedor '{provider_name}' não encontrado")
            return False
        
        if not provider.is_available():
            print(f"❌ Provedor '{provider_name}' não está disponível")
            return False
        
        self._current_provider = provider
        print(f"✅ Trocado para provedor: {provider_name}")
        return True
    
    def _select_best_provider(self):
        """Seleciona automaticamente o melhor provedor disponível."""
        # Ordem de preferência: groq > outros provedores
        preference_order = ["groq"]
        
        available_providers = self.get_available_providers()
        
        # Tenta provedores na ordem de preferência
        for preferred in preference_order:
            if preferred in available_providers:
                self._current_provider = available_providers[preferred]
                print(f"🎯 Provedor ativo: {preferred}")
                return
        
        # Se não achou nenhum preferido, pega qualquer um disponível
        if available_providers:
            provider_name = list(available_providers.keys())[0]
            self._current_provider = available_providers[provider_name]
            print(f"🎯 Provedor ativo: {provider_name}")
        else:
            self._current_provider = None
            print("⚠️ Nenhum provedor disponível")
    
    # Métodos de compatibilidade com a interface
    def invoke_llm(self, message: str) -> str:
        """
        Método de compatibilidade para invocar o LLM atual.
        
        Args:
            message: Mensagem para o LLM
            
        Returns:
            Resposta do LLM ou mensagem de erro
        """
        if not self._current_provider:
            return "❌ Nenhum provedor LLM configurado. Configure uma API key ou use o Mock Provider."
        
        return self._current_provider.generate_response(message)
    
    def get_llm(self, provider_name: Optional[str] = None):
        """
        Método de compatibilidade para obter o LLM.
        
        Args:
            provider_name: Nome do provedor (opcional)
            
        Returns:
            Instância do LLM ou None
        """
        target_provider = self._current_provider
        
        if provider_name:
            target_provider = self.get_provider(provider_name)
        
        if target_provider and target_provider.is_available():
            # Para Groq, retorna a instância interna do LLM
            if hasattr(target_provider, 'llm'):
                return target_provider.llm
        
        return None
    
    def is_any_provider_available(self) -> bool:
        """Verifica se algum provedor está disponível."""
        return len(self.get_available_providers()) > 0
    
    def get_provider_info(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Retorna informações de um provedor."""
        target_provider = self._current_provider
        
        if provider_name:
            target_provider = self.get_provider(provider_name)
        
        if not target_provider:
            return {"error": f"Provedor '{provider_name}' não encontrado"}
        
        return target_provider.get_info()
    
    def list_available_models(self, provider_name: Optional[str] = None) -> List[str]:
        """Lista modelos disponíveis de um provedor."""
        target_provider = self._current_provider
        
        if provider_name:
            target_provider = self.get_provider(provider_name)
        
        if not target_provider:
            return []
        
        return target_provider.get_available_models()
    
    def switch_model(self, provider_name: str, model: str) -> bool:
        """Troca o modelo de um provedor."""
        provider = self.get_provider(provider_name)
        
        if not provider:
            return False
        
        return provider.switch_model(model)
    
    def get_current_model(self, provider_name: Optional[str] = None) -> str:
        """Retorna o modelo atual de um provedor."""
        target_provider = self._current_provider
        
        if provider_name:
            target_provider = self.get_provider(provider_name)
        
        if not target_provider:
            return "Unknown"
        
        return target_provider.get_current_model()
    
    def get_performance_stats(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Retorna estatísticas de performance de um provedor."""
        target_provider = self._current_provider
        
        if provider_name:
            target_provider = self.get_provider(provider_name)
        
        if not target_provider:
            return {}
        
        return target_provider.get_performance_stats()
    
    def get_all_providers_info(self) -> Dict[str, Dict[str, Any]]:
        """Retorna informações de todos os provedores registrados."""
        return {
            name: provider.get_info()
            for name, provider in self._providers.items()
        }


# Instância global do registro de provedores
provider_registry = ProviderRegistry() 