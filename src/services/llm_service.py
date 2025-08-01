"""
Serviço de LLM que implementa a abstração ILLMService.
Implementa Dependency Inversion Principle.
"""

from src.interfaces import ILLMService, IProviderRegistry


class LLMService(ILLMService):
    """
    Serviço de alto nível para operações LLM.
    Abstrai os detalhes dos provedores através de interface.
    """
    
    def __init__(self, provider_registry: IProviderRegistry):
        """
        Inicializa o serviço com dependência injetada.
        
        Args:
            provider_registry: Registro de provedores (abstração)
        """
        self._provider_registry = provider_registry
        print("LLMService inicializado.")
    
    def generate_response(self, message: str) -> str:
        """
        Gera uma resposta usando o LLM ativo.
        
        Args:
            message: Mensagem para o LLM
            
        Returns:
            Resposta gerada ou mensagem de erro
        """
        try:
            current_provider = self._provider_registry.get_current_provider()
            
            if not current_provider:
                return "Nenhum provedor LLM disponível. Configure uma API key."
            
            if not current_provider.is_available():
                return f"Provedor {current_provider.get_name()} não está disponível."
            
            return current_provider.generate_response(message)
            
        except Exception as e:
            return f"Erro no serviço LLM: {str(e)}"
    
    def is_available(self) -> bool:
        """
        Verifica se algum LLM está disponível.
        
        Returns:
            True se algum provedor estiver disponível
        """
        try:
            available_providers = self._provider_registry.get_available_providers()
            return len(available_providers) > 0
        except Exception:
            return False
    
    def get_current_provider_name(self) -> str:
        """
        Retorna o nome do provedor atual.
        
        Returns:
            Nome do provedor ativo ou "Nenhum"
        """
        try:
            current_provider = self._provider_registry.get_current_provider()
            return current_provider.get_name() if current_provider else "Nenhum"
        except Exception:
            return "Erro"
    
    def get_name(self) -> str:
        """
        Implementa IIdentifiable - retorna identificação do serviço.
        
        Returns:
            Nome do serviço LLM
        """
        return "LLMService"
    
    def get_provider_registry(self) -> IProviderRegistry:
        """
        Retorna o registro de provedores (para casos específicos).
        
        Returns:
            Interface do registro de provedores
        """
        return self._provider_registry 