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
from typing import Dict, List, Any
from dotenv import load_dotenv
from src.interfaces import ILLMProvider

load_dotenv()


class ClaudeProviderExample(ILLMProvider):
    """Exemplo de provedor Claude/Anthropic."""
    
    def __init__(self):
        """Inicializa o provedor Claude."""
        self.name = "claude"
        self.client = None
        self.current_model = os.getenv("CLAUDE_DEFAULT_MODEL", "claude-3-haiku-20240307")
        self.status = "unavailable"
        
        # Modelos Claude disponíveis
        self.available_models = [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229"  
        ]
        
        self._setup()
    
    def _setup(self):
        """Configura o provedor Claude."""
        try:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                # ===== PARA IMPLEMENTAÇÃO REAL DESCOMENTE =====
                # import anthropic
                # 
                # self.client = anthropic.Anthropic(api_key=api_key)
                # 
                # # Teste de conexão
                # test = self.client.messages.create(
                #     model=self.current_model,
                #     max_tokens=5,
                #     messages=[{"role": "user", "content": "Hi"}]
                # )
                # 
                # self.status = "available"
                # print(f"Claude Provider configurado: {self.current_model}")
                
                # ===== MOCK =====
                print("Claude Provider em modo MOCK")
                self.status = "mock"
                
            else:
                print("ANTHROPIC_API_KEY não encontrada")
                self.status = "unavailable"
                
        except Exception as e:
            print(f"Erro ao configurar Claude: {e}")
            self.status = "error"
    
    def get_name(self) -> str:
        return self.name
    
    def is_available(self) -> bool:
        # Mock sempre retorna False para não interferir
        return False
    
    def generate_response(self, message: str) -> str:
        if not self.is_available():
            return f"Claude provider indisponível (modo exemplo)"
        
        try:
            # ===== IMPLEMENTAÇÃO REAL =====
            # response = self.client.messages.create(
            #     model=self.current_model,
            #     max_tokens=1000,
            #     messages=[{"role": "user", "content": message}]
            # )
            # return response.content[0].text
            
            # ===== MOCK =====
            return f"[MOCK Claude] Simulação de resposta para: {message[:30]}..."
            
        except Exception as e:
            return f"Erro Claude: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "status": self.status,
            "speed": "fast",
            "cost": "paid",
            "current_model": self.current_model,
            "description": "Claude da Anthropic - modelo constitucional ético",
            "context_length": "200k tokens",
            "advantages": [
                "Respostas muito éticas e seguras",
                "Excelente em análise de texto longo",
                "Boa capacidade de raciocínio"
            ],
            "note": "EXEMPLO MOCK"
        }
    
    def get_available_models(self) -> List[str]:
        return self.available_models.copy()
    
    def switch_model(self, model: str) -> bool:
        if model not in self.available_models:
            return False
        
        self.current_model = model
        print(f"[MOCK] Claude modelo: {model}")
        return True
    
    def get_current_model(self) -> str:
        return self.current_model
    
    def get_performance_stats(self) -> Dict[str, Any]:
        return {
            "avg_response_time": "~3-7s",
            "reliability": "99.5%",
            "cost_per_request": "$0.0008-0.024/1K tokens",
            "quality": "Excelente",
            "note": "Estimativas - exemplo mock"
        } 