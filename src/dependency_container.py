"""
Container de Injeção de Dependências.
Permite inversão de controle e testabilidade.
"""

from typing import Any, Dict, Type, Callable
from src.interfaces import IDependencyContainer


class DependencyContainer(IDependencyContainer):
    """
    Container simples de injeção de dependências.
    Implementa o padrão Service Locator com inversão de controle.
    """
    
    def __init__(self):
        """Inicializa o container."""
        self._singletons: Dict[Type, Any] = {}
        self._transients: Dict[Type, Callable] = {}
        self._singleton_instances: Dict[Type, Any] = {}
    
    def register_singleton(self, interface: Type, implementation: Any) -> None:
        """
        Registra um singleton - mesma instância sempre.
        
        Args:
            interface: Interface ou tipo base
            implementation: Instância a ser retornada
        """
        self._singletons[interface] = implementation
        print(f"Singleton registrado: {interface.__name__} -> {type(implementation).__name__}")
    
    def register_transient(self, interface: Type, factory: Callable) -> None:
        """
        Registra uma factory transiente - nova instância a cada chamada.
        
        Args:
            interface: Interface ou tipo base  
            factory: Função que cria instâncias
        """
        self._transients[interface] = factory
        print(f"Transient registrado: {interface.__name__} -> factory")
    
    def resolve(self, interface: Type) -> Any:
        """
        Resolve uma dependência.
        
        Args:
            interface: Interface a ser resolvida
            
        Returns:
            Instância da implementação
            
        Raises:
            ValueError: Se a interface não estiver registrada
        """
        # Verifica singleton primeiro
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Verifica singleton instance cache
        if interface in self._singleton_instances:
            return self._singleton_instances[interface]
        
        # Verifica transient
        if interface in self._transients:
            factory = self._transients[interface]
            return factory()
        
        raise ValueError(f"Interface {interface.__name__} não registrada no container")
    
    def is_registered(self, interface: Type) -> bool:
        """
        Verifica se uma interface está registrada.
        
        Args:
            interface: Interface a verificar
            
        Returns:
            True se registrada, False caso contrário
        """
        return interface in self._singletons or interface in self._transients
    
    def register_singleton_factory(self, interface: Type, factory: Callable) -> None:
        """
        Registra um singleton usando factory (lazy loading).
        
        Args:
            interface: Interface ou tipo base
            factory: Função que cria a instância (chamada apenas uma vez)
        """
        def lazy_factory():
            if interface not in self._singleton_instances:
                self._singleton_instances[interface] = factory()
            return self._singleton_instances[interface]
        
        self._transients[interface] = lazy_factory
        print(f"✅ Singleton Factory registrado: {interface.__name__}")
    
    def clear(self) -> None:
        """Limpa todas as dependências registradas."""
        self._singletons.clear()
        self._transients.clear()
        self._singleton_instances.clear()
        print("🧹 Container de dependências limpo")
    
    def get_registered_interfaces(self) -> Dict[str, str]:
        """
        Retorna informações sobre interfaces registradas.
        
        Returns:
            Dicionário com interface -> tipo de registro
        """
        result = {}
        
        for interface in self._singletons:
            result[interface.__name__] = "Singleton"
        
        for interface in self._transients:
            if interface in self._singleton_instances:
                result[interface.__name__] = "Singleton (Lazy)"
            else:
                result[interface.__name__] = "Transient"
        
        return result


# Instância global do container
container = DependencyContainer() 