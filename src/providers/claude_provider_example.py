"""
Exemplo de implementação de um provedor Claude/Anthropic.
Este arquivo demonstra como criar um provider para uma API específica.

INSTRUÇÕES:
Para usar Claude real:
- pip install anthropic
- Configure ANTHROPIC_API_KEY no .env ou use o arquivo setup_env.py
- Descomente a implementação real
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

load_dotenv()


class ClaudeProviderExample(ILLMProvider):
    """Exemplo de provedor Claude/Anthropic."""
    
    def __init__(self):
        """Inicializa o provedor Claude."""
        self.name = "claude"
        self.client = None
        self.current_model = os.getenv("CLAUDE_DEFAULT_MODEL", "claude-3-haiku-20240307")
        self.status = "unavailable"
        self.api_key = None
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        # Modelos Claude disponíveis
        self.available_models = [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229", 
            "claude-3-opus-20240229",
            "claude-3-5-sonnet-20240620"
        ]
        
        self._setup()
    
    def _setup(self):
        """Configura o provedor Claude."""
        try:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if self.api_key:
                # ===== PARA IMPLEMENTAÇÃO REAL DESCOMENTE =====
                # import anthropic
                # 
                # self.client = anthropic.Anthropic(api_key=self.api_key)
                # 
                # # Teste de conexão
                # test = self.client.messages.create(
                #     model=self.current_model,
                #     max_tokens=5,
                #     messages=[{"role": "user", "content": "Hi"}]
                # )
                # 
                # self.status = "available"
                # # Mostra configurações globais que serão usadas
                # params = GlobalConfig.get_generation_params()
                # print(f"Claude Provider configurado com modelo {self.current_model}")
                # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                
                # ===== MOCK =====
                print("Claude Provider em modo MOCK - implemente a lógica real!")
                self.status = "mock"
                
            else:
                print("ANTHROPIC_API_KEY não encontrada")
                self.status = "unavailable"
                
        except Exception as e:
            print(f"Erro ao configurar Claude: {e}")
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
        """Gera uma resposta para a mensagem."""
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Implemente a lógica real!"
        
        try:
            # Atualiza estatísticas
            self.request_count += 1
            self.last_request_time = time.time()
            
            # Usa configurações globais centralizadas
            # kwargs ainda podem sobrescrever se necessário
            params = GlobalConfig.get_generation_params(**kwargs)
            
            # ===== IMPLEMENTAÇÃO REAL =====
            # response = self.client.messages.create(
            #     model=self.current_model,
            #     max_tokens=params["max_tokens"],
            #     temperature=params["temperature"],
            #     messages=[{"role": "user", "content": message}],
            #     timeout=params["timeout"]
            # )
            # return response.content[0].text.strip()
            
            # ===== MOCK =====
            return f"[MOCK Claude] Simulação de resposta para: {message[:30]}..."
            
        except Exception as e:
            self.error_count += 1
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        return {
            "name": self.name,
            "description": "Claude da Anthropic - modelo constitucional ético",
            "status": self.status,
            "current_model": self.current_model,
            "total_models": len(self.available_models),
            "rate_limit": "Varia conforme plano",
            "website": "https://anthropic.com",
            "pricing": "Pago - varia por modelo",
            "speed": "fast",     # Compatibilidade com interface
            "cost": "paid",      # Compatibilidade com interface
            "features": [
                "Respostas muito éticas e seguras",
                "Excelente em análise de texto longo",
                "Boa capacidade de raciocínio",
                "Contexto de 200k tokens",
                "Modelo constitucional"
            ],
            "advantages": [
                "Respostas muito éticas e seguras",
                "Excelente em análise de texto longo",
                "Boa capacidade de raciocínio",
                "Contexto extenso"
            ],
            "note": "ESTE É UM EXEMPLO/MOCK - Implemente a lógica real!"
        }
    
    def get_available_models(self) -> List[str]:
        """Lista modelos disponíveis."""
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        """Troca o modelo ativo."""
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            # ===== IMPLEMENTAÇÃO REAL (DESCOMENTE PARA USAR) =====
            # anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            # if not anthropic_key:
            #     print("ANTHROPIC_API_KEY não encontrada")
            #     return False
            # 
            # import anthropic
            # 
            # # Usa configurações globais centralizadas
            # params = GlobalConfig.get_generation_params()
            # 
            # self.client = anthropic.Anthropic(api_key=anthropic_key)
            # self.current_model = model
            # print(f"Modelo alterado para {model} no {self.name}")
            # print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
            # return True
            
            # ===== IMPLEMENTAÇÃO MOCK =====
            self.current_model = model
            print(f"[MOCK] Claude modelo alterado para: {model}")
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
            "rate_limit_info": "Varia conforme plano Anthropic",
            "note": "Estatísticas reais - este provider está em modo mock"
        }

