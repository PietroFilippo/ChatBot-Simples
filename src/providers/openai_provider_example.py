"""
Exemplo de implementação de um novo provedor - OpenAI Provider.
Este arquivo serve como template/placeholder para adicionar novos provedores.

Para usar OpenAI real:
- pip install openai
- Configurar OPENAI_API_KEY no .env ou use o arquivo setup_env.py
- Descomente as seções marcadas como "IMPLEMENTAÇÃO REAL"
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


class OpenAIProviderExample(ILLMProvider):
    """
    Exemplo de provedor OpenAI implementando a interface ILLMProvider.
    
    Este é um TEMPLATE/PLACEHOLDER mostrando como implementar um novo provider.
    Para usar um provider real, substitua a lógica mock pela implementação real.
    """
    
    def __init__(self):
        """Inicializa o provedor OpenAI (exemplo)."""
        self.name = "openai"  # Nome único do provedor
        self.client = None    # Cliente da API (será inicializado no _setup)
        self.current_model = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")
        self.status = "unavailable"
        self.api_key = None
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        # Lista de modelos disponíveis (exemplo)
        self.available_models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini"
        ]
        
        self._setup()
    
    def _setup(self):
        """
        Configura o provedor OpenAI.
        
        NOTA: Esta é uma implementação MOCK/EXEMPLO.
        Para implementação real, descomente e ajuste o código abaixo.
        """
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if self.api_key:
                # ===== PARA IMPLEMENTAÇÃO REAL DESCOMENTE =====
                # from openai import OpenAI
                # 
                # self.client = OpenAI(api_key=self.api_key)
                # 
                # # Testa a conexão
                # test_response = self.client.chat.completions.create(
                #     model=self.current_model,
                #     messages=[{"role": "user", "content": "Hello"}],
                #     max_tokens=5
                # )
                # 
                # self.status = "available"
                # # Mostra configurações globais que serão usadas
                # params = GlobalConfig.get_generation_params()
                # print(f"OpenAI Provider configurado com modelo {self.current_model}")
                # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                
                # ===== IMPLEMENTAÇÃO MOCK (PARA DEMONSTRAÇÃO) =====
                print("OpenAI Provider em modo MOCK - implemente a lógica real!")
                self.status = "mock"  # Status especial para indicar mock
                
            else:
                print("OPENAI_API_KEY não encontrada")
                self.status = "unavailable"
                
        except Exception as e:
            print(f"Erro ao configurar OpenAI: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        """Retorna o nome do provedor."""
        return self.name
    
    def is_available(self) -> bool:
        """
        Verifica se o provedor está disponível.
        
        NOTA: Em modo mock, retorna False para não interferir no sistema.
        Para implementação real, mude para: return self.status == "available"
        """
        # Para implementação real:
        # return self.status == "available"
        
        # Para modo mock (não interfere no sistema):
        return False
    
    def generate_response(self, message: str, **kwargs) -> str:
        """
        Gera uma resposta para a mensagem.
        
        NOTA: Esta é uma implementação MOCK/EXEMPLO.
        """
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Implemente a lógica real!"
        
        try:
            # Atualiza estatísticas
            self.request_count += 1
            self.last_request_time = time.time()
            
            # Usa configurações globais centralizadas
            # kwargs ainda podem sobrescrever se necessário
            params = GlobalConfig.get_generation_params(**kwargs)
            
            # ===== IMPLEMENTAÇÃO REAL (DESCOMENTE PARA USAR) =====
            # response = self.client.chat.completions.create(
            #     model=self.current_model,
            #     messages=[{"role": "user", "content": message}],
            #     max_tokens=params["max_tokens"],
            #     temperature=params["temperature"],
            #     timeout=params["timeout"]
            # )
            # return response.choices[0].message.content.strip()
            
            # ===== IMPLEMENTAÇÃO MOCK (PARA DEMONSTRAÇÃO) =====
            return f"[MOCK OpenAI] Resposta simulada para: {message[:50]}..."
            
        except Exception as e:
            self.error_count += 1
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        return {
            "name": self.name,
            "description": "API OpenAI com modelos GPT de alta qualidade",
            "status": self.status,
            "current_model": self.current_model,
            "total_models": len(self.available_models),
            "rate_limit": "Varia conforme plano",
            "website": "https://openai.com",
            "pricing": "Pago - varia por modelo",
            "speed": "medium",  # Compatibilidade com interface
            "cost": "paid",     # Compatibilidade com interface
            "features": [
                "Modelos de altíssima qualidade",
                "Suporte a múltiplas modalidades",
                "Documentação excelente",
                "Ampla variedade de modelos",
                "API bem estabelecida"
            ],
            "advantages": [
                "Modelos de altíssima qualidade", 
                "Suporte a múltiplas modalidades",
                "Documentação excelente",
                "Comunidade ativa"
            ],
            "note": "ESTE É UM EXEMPLO/MOCK - Implemente a lógica real!"
        }
    
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        """
        Troca o modelo ativo.
        
        NOTA: Implementação mock - para uso real, implemente a lógica da API.
        """
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            # ===== IMPLEMENTAÇÃO REAL (DESCOMENTE PARA USAR) =====
            # openai_key = os.getenv("OPENAI_API_KEY")
            # if not openai_key:
            #     print("OPENAI_API_KEY não encontrada")
            #     return False
            # 
            # from openai import OpenAI
            # 
            # # Usa configurações globais centralizadas
            # params = GlobalConfig.get_generation_params()
            # 
            # self.client = OpenAI(api_key=openai_key)
            # self.current_model = model
            # print(f"Modelo alterado para {model} no {self.name}")
            # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
            # return True
            
            # ===== IMPLEMENTAÇÃO MOCK =====
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
        """Retorna estatísticas de performance."""
        uptime = time.time() - (self.last_request_time or time.time())
        success_rate = ((self.request_count - self.error_count) / max(self.request_count, 1)) * 100
        
        return {
            "requests_made": self.request_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "last_request": self.last_request_time,
            "uptime_minutes": max(0, uptime / 60),
            "status": self.status,
            "rate_limit_info": "Varia conforme plano OpenAI",
            "note": "Estatísticas reais - este provider está em modo mock"
        }
