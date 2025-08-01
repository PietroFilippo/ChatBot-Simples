"""
Contratos Comportamentais para Liskov Substitution Principle.
Define pré-condições, pós-condições e invariantes para interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Optional
import functools
import logging


# ========================================
# DECORATORS PARA CONTRATOS
# ========================================

def precondition(condition: Callable[..., bool], error_message: str = "Precondition failed"):
    """
    Decorator para pré-condições - validações que devem ser verdadeiras ANTES da execução.
    
    Args:
        condition: Função que valida a pré-condição
        error_message: Mensagem de erro personalizada
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                raise ValueError(f"{error_message} in {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def postcondition(condition: Callable[..., bool], error_message: str = "Postcondition failed"):
    """
    Decorator para pós-condições - validações que devem ser verdadeiras DEPOIS da execução.
    
    Args:
        condition: Função que valida a pós-condição 
        error_message: Mensagem de erro personalizada
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not condition(result, *args, **kwargs):
                raise ValueError(f"{error_message} in {func.__name__}")
            return result
        return wrapper
    return decorator


def invariant(condition: Callable, error_message: str = "Class invariant violated"):
    """
    Decorator para invariantes de classe - condições que devem sempre ser verdadeiras.
    
    Args:
        condition: Função que valida a invariante
        error_message: Mensagem de erro personalizada
    """
    def decorator(cls):
        original_init = cls.__init__
        
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if not condition(self):
                raise ValueError(f"{error_message} in {cls.__name__}")
        
        cls.__init__ = new_init
        
        # Adiciona validação a todos os métodos públicos
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                @functools.wraps(attr)
                def wrapper(self, *args, **kwargs):
                    result = attr(self, *args, **kwargs)
                    if not condition(self):
                        raise ValueError(f"{error_message} in {cls.__name__}.{attr_name}")
                    return result
                setattr(cls, attr_name, wrapper)
        
        return cls
    return decorator


# ========================================
# VALIDADORES DE CONTRATO ESPECÍFICOS
# ========================================

class ContractValidators:
    """Validadores reutilizáveis para contratos comportamentais."""
    
    @staticmethod
    def text_not_empty(*args, **kwargs) -> bool:
        """Valida que strings não estão vazias."""
        for arg in args:
            if isinstance(arg, str) and not arg.strip():
                return False
        return True
    
    @staticmethod
    def result_not_empty(result, *args, **kwargs) -> bool:
        """Valida que o resultado não está vazio."""
        if isinstance(result, str):
            return bool(result.strip())
        elif isinstance(result, (list, dict)):
            return len(result) > 0
        return result is not None
    
    @staticmethod
    def result_is_string(result, *args, **kwargs) -> bool:
        """Valida que o resultado é uma string."""
        return isinstance(result, str)
    
    @staticmethod
    def result_is_bool(result, *args, **kwargs) -> bool:
        """Valida que o resultado é um boolean."""
        return isinstance(result, bool)
    
    @staticmethod
    def result_is_dict(result, *args, **kwargs) -> bool:
        """Valida que o resultado é um dicionário."""
        return isinstance(result, dict)
    
    @staticmethod
    def result_is_list(result, *args, **kwargs) -> bool:
        """Valida que o resultado é uma lista."""
        return isinstance(result, list)
    
    @staticmethod
    def provider_has_name(self) -> bool:
        """Invariante: provedor deve sempre ter um nome válido."""
        return hasattr(self, 'get_name') and bool(self.get_name())


# ========================================
# INTERFACES COM CONTRATOS COMPORTAMENTAIS
# ========================================

class IContractedIdentifiable(ABC):
    """Interface com contratos para objetos identificáveis."""
    
    @abstractmethod
    @postcondition(ContractValidators.result_not_empty, "Name must not be empty")
    @postcondition(ContractValidators.result_is_string, "Name must be a string")
    def get_name(self) -> str:
        """
        Retorna o nome/identificador.
        
        Pós-condições:
        - Resultado não pode ser vazio
        - Resultado deve ser string
        """
        pass


class IContractedTextGenerator(ABC):
    """Interface com contratos para geradores de texto."""
    
    @abstractmethod
    @precondition(ContractValidators.text_not_empty, "Prompt must not be empty")
    @postcondition(ContractValidators.result_not_empty, "Response must not be empty")
    @postcondition(ContractValidators.result_is_string, "Response must be a string")
    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta a partir de um prompt.
        
        Pré-condições:
        - Prompt não pode ser vazio
        
        Pós-condições:
        - Resposta não pode ser vazia
        - Resposta deve ser string
        """
        pass


class IContractedAvailabilityCheck(ABC):
    """Interface com contratos para verificação de disponibilidade."""
    
    @abstractmethod
    @postcondition(ContractValidators.result_is_bool, "Availability must be boolean")
    def is_available(self) -> bool:
        """
        Verifica se está disponível.
        
        Pós-condições:
        - Resultado deve ser boolean
        """
        pass


# ========================================
# MIXIN PARA TESTING DE CONTRATOS
# ========================================

class ContractTestingMixin:
    """Mixin que fornece métodos para testar contratos LSP."""
    
    def test_substitutability(self, implementations: List[Any], test_cases: List[Dict]) -> Dict[str, Any]:
        """
        Testa se todas as implementações são intercambiáveis (LSP).
        
        Args:
            implementations: Lista de objetos que implementam a mesma interface
            test_cases: Lista de casos de teste {'method': str, 'args': tuple, 'kwargs': dict}
        
        Returns:
            Relatório de testes de substituibilidade
        """
        results = {
            "total_tests": len(test_cases) * len(implementations),
            "passed": 0,
            "failed": 0,
            "failures": [],
            "implementations_tested": len(implementations)
        }
        
        # Executa todos os casos de teste em todas as implementações
        for impl in implementations:
            impl_name = impl.__class__.__name__
            
            for i, test_case in enumerate(test_cases):
                try:
                    method_name = test_case['method']
                    args = test_case.get('args', ())
                    kwargs = test_case.get('kwargs', {})
                    
                    # Executa o método
                    method = getattr(impl, method_name)
                    result = method(*args, **kwargs)
                    
                    # Valida que o resultado atende ao contrato
                    self._validate_contract_compliance(method_name, result, args, kwargs)
                    
                    results["passed"] += 1
                    
                except Exception as e:
                    results["failed"] += 1
                    results["failures"].append({
                        "implementation": impl_name,
                        "test_case": i,
                        "method": test_case['method'],
                        "error": str(e)
                    })
        
        return results
    
    def _validate_contract_compliance(self, method_name: str, result: Any, args: tuple, kwargs: dict):
        """Valida se um resultado atende aos contratos esperados."""
        # Validações específicas por método
        if method_name == 'get_name':
            if not isinstance(result, str) or not result.strip():
                raise ValueError("get_name must return non-empty string")
        
        elif method_name == 'generate_response':
            if not isinstance(result, str) or not result.strip():
                raise ValueError("generate_response must return non-empty string")
        
        elif method_name == 'is_available':
            if not isinstance(result, bool):
                raise ValueError("is_available must return boolean")
    
    def generate_lsp_report(self, implementations: List[Any]) -> str:
        """
        Gera relatório detalhado de conformidade com LSP.
        
        Args:
            implementations: Lista de implementações a testar
        
        Returns:
            Relatório em formato texto
        """
        # Casos de teste padrão
        test_cases = [
            {'method': 'get_name', 'args': (), 'kwargs': {}},
            {'method': 'is_available', 'args': (), 'kwargs': {}},
        ]
        
        # Adiciona testes específicos se os métodos existirem
        for impl in implementations:
            if hasattr(impl, 'generate_response'):
                test_cases.append({
                    'method': 'generate_response', 
                    'args': ('test prompt',), 
                    'kwargs': {}
                })
        
        # Executa os testes
        results = self.test_substitutability(implementations, test_cases)
        
        # Gera o relatório
        report = f"""

## Implementações Testadas
"""
        
        for impl in implementations:
            impl_name = impl.__class__.__name__
            impl_failures = [f for f in results['failures'] if f['implementation'] == impl_name]
            status = "✅ CONFORME" if len(impl_failures) == 0 else f"❌ {len(impl_failures)} FALHAS"
            report += f"- **{impl_name}:** {status}\n"
        
        if results['failures']:
            report += "\n## Falhas Detalhadas\n"
            for failure in results['failures']:
                report += f"""
### {failure['implementation']}.{failure['method']}()
- **Erro:** {failure['error']}
- **Caso de teste:** {failure['test_case']}
"""
        
        return report


# ========================================
# FACTORY PARA TESTES DE CONTRATO
# ========================================

class ContractTestFactory:
    """Factory para criar testes de contrato específicos."""
    
    @staticmethod
    def create_llm_provider_tests() -> List[Dict]:
        """Cria casos de teste para provedores LLM."""
        return [
            {'method': 'get_name', 'args': (), 'kwargs': {}},
            {'method': 'is_available', 'args': (), 'kwargs': {}},
            {'method': 'generate_response', 'args': ('Hello, how are you?',), 'kwargs': {}},
        ]
    
    @staticmethod
    def create_chatbot_tests() -> List[Dict]:
        """Cria casos de teste para chatbots."""
        return [
            {'method': 'chat', 'args': ('Hello',), 'kwargs': {}},
            {'method': 'get_stats', 'args': (), 'kwargs': {}},
        ]
    
    @staticmethod
    def create_service_tests() -> List[Dict]:
        """Cria casos de teste para serviços."""
        return [
            {'method': 'is_available', 'args': (), 'kwargs': {}},
            {'method': 'generate_response', 'args': ('test',), 'kwargs': {}},
        ] 