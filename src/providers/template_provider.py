"""
TEMPLATE PROVIDER - Base para implementação de novos provedores LLM
==================================================================

Este arquivo serve como template completo para implementar um novo provedor.
Copie este arquivo, renomeie e implemente a lógica específica da sua API.

PASSOS PARA IMPLEMENTAR UM NOVO PROVIDER:

1. Copie este arquivo para `seu_provider.py`
2. Renomeie a classe para `SeuProvider`
3. Altere self.name para o nome do seu provedor
4. Configure suas variáveis de ambiente
5. Implemente a lógica real nos métodos marcados
6. Teste o provider
7. Registre no provider_registry.py se necessário

ESTRUTURA OBRIGATÓRIA:
- Todos os métodos da interface ILLMProvider devem ser implementados
- Use GlobalConfig para configurações centralizadas
- Implemente estatísticas de performance
- Trate erros adequadamente
- Use timeout nas requisições
"""

import os
import sys
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para imports quando executado diretamente
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sys.path.insert(0, project_root)

from src.interfaces import ILLMProvider
from src.config import GlobalConfig

# Carrega as variáveis de ambiente
load_dotenv()


class TemplateProvider(ILLMProvider):
    """
    Template base para implementação de novos provedores LLM.
    
    INSTRUÇÕES:
    1. Renomeie esta classe para o nome do seu provedor
    2. Altere self.name para o identificador único
    3. Configure variáveis de ambiente apropriadas
    4. Implemente a lógica da API nos métodos marcados
    """
    
    def __init__(self):
        """Inicializa o provedor template."""
        # ===============================
        # CONFIGURAÇÕES BÁSICAS - MODIFIQUE AQUI
        # ===============================
        self.name = "template"  # ALTERE: Nome único do provedor
        self.base_url = "https://api.exemplo.com/v1"  # ALTERE: URL base da API
        self.client = None  # Cliente da API (se necessário)
        self.current_model = os.getenv("TEMPLATE_DEFAULT_MODEL", "modelo-padrao")  # ALTERE
        self.status = "unavailable"
        self.api_key = None
        
        # Estatísticas de performance (obrigatórias)
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        # ===============================
        # MODELOS DISPONÍVEIS - MODIFIQUE AQUI
        # ===============================
        self.available_models = [
            "modelo-padrao",
            "modelo-avancado",
            "modelo-rapido"
            # ALTERE: Adicione os modelos da sua API
        ]
        
        # Inicialização
        self._setup()
    
    def _setup(self):
        """
        Configura o provedor template.
        
        INSTRUÇÕES: Implemente aqui a lógica de inicialização:
        - Verificação de API key
        - Inicialização do cliente
        - Teste de conexão
        - Configuração de status
        """
        try:
            # ALTERE: Nome da variável de ambiente da API key
            self.api_key = os.getenv("TEMPLATE_API_KEY")  
            
            if self.api_key:
                # ===============================
                # IMPLEMENTE AQUI: CONFIGURAÇÃO REAL
                # ===============================
                # Exemplo:
                # from sua_biblioteca import SeuCliente
                # 
                # self.client = SeuCliente(api_key=self.api_key)
                # 
                # # Teste de conexão (opcional mas recomendado)
                # test_response = self.client.test_connection()
                # 
                # self.status = "available"
                # # Mostra configurações globais que serão usadas
                # params = GlobalConfig.get_generation_params()
                # print(f"{self.name} Provider configurado com modelo {self.current_model}")
                # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                
                # ===============================
                # EXEMPLO MOCK (REMOVA QUANDO IMPLEMENTAR)
                # ===============================
                print(f"{self.name} Provider em modo MOCK - implemente a lógica real!")
                self.status = "mock"  # Use "available" quando implementar
                
            else:
                print(f"TEMPLATE_API_KEY não encontrada")  # ALTERE: Nome da variável
                self.status = "unavailable"
                
        except Exception as e:
            print(f"Erro ao configurar {self.name}: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """
        Verifica se o provedor está disponível.
        
        INSTRUÇÕES: Para implementação real, use:
        return self.status == "available"
        """
        # Para implementação real:
        # return self.status == "available"
        
        # Para modo mock (não interfere no sistema):
        return False
    
    def generate_response(self, message: str, **kwargs) -> str:
        """
        Gera uma resposta para a mensagem.
        
        INSTRUÇÕES: Este é o método principal - implemente aqui a lógica
        de chamada para sua API de LLM.
        """
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Verifique a configuração."
        
        try:
            # Atualiza estatísticas (obrigatório)
            self.request_count += 1
            self.last_request_time = time.time()
            
            # Usa configurações globais centralizadas (obrigatório)
            # kwargs ainda podem sobrescrever se necessário
            params = GlobalConfig.get_generation_params(**kwargs)
            
            # ===============================
            # IMPLEMENTE AQUI: LÓGICA DA API REAL
            # ===============================
            # Exemplo para API REST:
            # 
            # payload = {
            #     "model": self.current_model,
            #     "messages": [{"role": "user", "content": message}],
            #     "max_tokens": params["max_tokens"],
            #     "temperature": params["temperature"]
            # }
            # 
            # headers = {
            #     "Authorization": f"Bearer {self.api_key}",
            #     "Content-Type": "application/json"
            # }
            # 
            # response = requests.post(
            #     f"{self.base_url}/chat/completions",
            #     headers=headers,
            #     json=payload,
            #     timeout=params["timeout"]
            # )
            # 
            # if response.status_code == 200:
            #     result = response.json()
            #     return result["choices"][0]["message"]["content"].strip()
            # else:
            #     self.error_count += 1
            #     return f"Erro na API: {response.status_code} - {response.text[:200]}"
            
            # ===============================
            # EXEMPLO MOCK (REMOVA QUANDO IMPLEMENTAR)
            # ===============================
            return f"[MOCK {self.name}] Resposta simulada para: {message[:50]}..."
            
        except Exception as e:
            self.error_count += 1
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o provedor.
        
        INSTRUÇÕES: Customize as informações do seu provedor.
        """
        return {
            "name": self.name,
            "description": "Template provider - substitua pela descrição real",  # ALTERE
            "status": self.status,
            "current_model": self.current_model,
            "total_models": len(self.available_models),
            "rate_limit": "Consulte documentação da API",  # ALTERE
            "website": "https://exemplo.com",  # ALTERE
            "pricing": "Consulte site oficial",  # ALTERE
            "speed": "medium",     # ALTERE: "fast", "medium", "slow"
            "cost": "unknown",     # ALTERE: "free", "paid", "freemium"
            "features": [
                "Lista de recursos",  # ALTERE
                "Funcionalidades específicas",
                "Vantagens da API"
            ],
            "advantages": [
                "Pontos fortes",  # ALTERE
                "Diferencial do provedor",
                "Benefícios únicos"
            ],
            "note": "ESTE É UM TEMPLATE - Implemente a lógica real!"
        }
    
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        """
        Troca o modelo ativo.
        
        INSTRUÇÕES: Implemente aqui a lógica para trocar modelos,
        se a API suportar múltiplos modelos.
        """
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            # ===============================
            # IMPLEMENTE AQUI: TROCA DE MODELO REAL
            # ===============================
            # Se precisar recriar cliente:
            # api_key = os.getenv("TEMPLATE_API_KEY")
            # if not api_key:
            #     print("TEMPLATE_API_KEY não encontrada")
            #     return False
            # 
            # from sua_biblioteca import SeuCliente
            # 
            # # Usa configurações globais centralizadas
            # params = GlobalConfig.get_generation_params()
            # 
            # self.client = SeuCliente(
            #     api_key=api_key,
            #     model=model
            # )
            # self.current_model = model
            # print(f"Modelo alterado para {model} no {self.name}")
            # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
            # return True
            
            # ===============================
            # EXEMPLO MOCK (REMOVA QUANDO IMPLEMENTAR)
            # ===============================
            self.current_model = model
            print(f"[MOCK] Modelo alterado para {model} no {self.name}")
            return True
            
        except Exception as e:
            print(f"Erro ao trocar modelo: {e}")
            return False
    
    def get_current_model(self) -> str:
        """Retorna o modelo atual."""
        return self.current_model
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de performance.
        
        OBRIGATÓRIO: Este método deve retornar estatísticas reais.
        """
        uptime = time.time() - (self.last_request_time or time.time())
        success_rate = ((self.request_count - self.error_count) / max(self.request_count, 1)) * 100
        
        return {
            "requests_made": self.request_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "last_request": self.last_request_time,
            "uptime_minutes": max(0, uptime / 60),
            "status": self.status,
            "rate_limit_info": "Consulte documentação da API",  # ALTERE
            "note": "Estatísticas reais de uso"
        }


# ===============================
# EXEMPLO DE USO E TESTE
# ===============================
if __name__ == "__main__":
    """
    Teste básico do provider template.
    Execute este arquivo para testar sua implementação.
    """
    
    print("=== TESTE DO TEMPLATE PROVIDER ===")
    
    # Inicializa o provider
    provider = TemplateProvider()
    
    # Testa métodos básicos
    print(f"Nome: {provider.get_name()}")
    print(f"Disponível: {provider.is_available()}")
    print(f"Modelo atual: {provider.get_current_model()}")
    print(f"Modelos disponíveis: {provider.get_available_models()}")
    
    # Testa geração de resposta
    response = provider.generate_response("Olá, como você está?")
    print(f"Resposta: {response}")
    
    # Testa informações
    info = provider.get_info()
    print(f"Info: {info['description']}")
    
    # Testa estatísticas
    stats = provider.get_performance_stats()
    print(f"Requests: {stats['requests_made']}")
    
    print("=== TESTE CONCLUÍDO ===") 