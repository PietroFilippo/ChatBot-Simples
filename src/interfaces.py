"""
Interfaces abstratas para o sistema de IA Generativa.

NOTA: Este arquivo mantém compatibilidade com código existente.
As novas interfaces segregadas estão em src/interfaces/
"""

# Importa as novas interfaces segregadas
from src.interfaces import *

# Mantém imports antigos para compatibilidade
# (As novas interfaces já estão disponíveis através do import acima)

# ANTES: Interface muito grande
# class ILLMProvider(ABC):
#     def get_name(self) -> str: pass           # Identificação
#     def is_available(self) -> bool: pass      # Disponibilidade  
#     def generate_response(self, msg: str): pass  # Geração
#     def get_info(self) -> Dict: pass          # Informações
#     def get_models(self) -> List: pass        # Modelos
#     def switch_model(self, model: str): pass  # Mudança de modelo
#     def get_current_model(self) -> str: pass  # Modelo atual
#     def get_stats(self) -> Dict: pass         # Estatísticas

# AGORA: Interfaces segregadas
# IIdentifiable        - Apenas identificação
# IAvailabilityCheck   - Apenas verificação de disponibilidade  
# ITextGenerator       - Apenas geração de texto
# IInformationProvider - Apenas informações
# IModelProvider       - Apenas listagem de modelos
# IModelSwitcher       - Apenas troca de modelos
# IPerformanceMetrics  - Apenas estatísticas

# Composição final:
# IFullLLMProvider = IIdentifiable + IAvailabilityCheck + ITextGenerator + 
#                    IInformationProvider + IModelProvider + IModelSwitcher + 
#                    IPerformanceMetrics

# Interfaces graduais disponíveis:
# IBasicLLMProvider    - Funcionalidade mínima
# IAdvancedLLMProvider - Funcionalidade média  
# IFullLLMProvider     - Funcionalidade completa