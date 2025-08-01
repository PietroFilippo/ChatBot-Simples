"""
Exemplo de implementação de um novo provedor - OpenAI Provider.
Este arquivo serve como template/placeholder para adicionar novos provedores.

Para usar OpenAI real:
- pip install openai
- Configurar OPENAI_API_KEY no .env ou use o arquivo setup_env.py
- Descomente as seções marcadas como "IMPLEMENTAÇÃO REAL"
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from src.interfaces import ILLMProvider

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
        
        # Lista de modelos disponíveis (exemplo)
        self.available_models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o"
        ]
        
        self._setup()
    
    def _setup(self):
        """
        Configura o provedor OpenAI.
        
        NOTA: Esta é uma implementação MOCK/EXEMPLO.
        Para implementação real, descomente e ajuste o código abaixo.
        """
        try:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                # ===== PARA IMPLEMENTAÇÃO REAL DESCOMENTE =====
                # from openai import OpenAI
                # 
                # self.client = OpenAI(api_key=openai_key)
                # 
                # # Testa a conexão
                # test_response = self.client.chat.completions.create(
                #     model=self.current_model,
                #     messages=[{"role": "user", "content": "Hello"}],
                #     max_tokens=5
                # )
                # 
                # self.status = "available"
                # print(f"OpenAI Provider configurado com modelo {self.current_model}")
                
                # ===== IMPLEMENTAÇÃO MOCK (PARA DEMONSTRAÇÃO) =====
                print("OpenAI Provider em modo MOCK - implemente a lógica real!")
                self.status = "mock"  # Status especial para indicar mock
                
            else:
                print("OPENAI_API_KEY não encontrada")
                self.status = "unavailable"
                
        except Exception as e:
            print(f"❌ Erro ao configurar OpenAI: {e}")
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
    
    def generate_response(self, message: str) -> str:
        """
        Gera uma resposta para a mensagem.
        
        NOTA: Esta é uma implementação MOCK/EXEMPLO.
        """
        if not self.is_available():
            return f"Provedor {self.name} não disponível. Implemente a lógica real!"
        
        try:
            # ===== IMPLEMENTAÇÃO REAL (DESCOMENTE PARA USAR) =====
            # response = self.client.chat.completions.create(
            #     model=self.current_model,
            #     messages=[{"role": "user", "content": message}],
            #     max_tokens=1000,
            #     temperature=0.7
            # )
            # return response.choices[0].message.content
            
            # ===== IMPLEMENTAÇÃO MOCK (PARA DEMONSTRAÇÃO) =====
            return f"[MOCK OpenAI] Resposta simulada para: {message[:50]}..."
            
        except Exception as e:
            return f"Erro na API {self.name}: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provedor."""
        return {
            "provider": self.name,
            "status": self.status,
            "speed": "medium",  # openai é geralmente mais lento que groq
            "cost": "paid",     # openai é pago
            "current_model": self.current_model,
            "description": "API OpenAI com modelos GPT de alta qualidade",
            "context_length": "4096-128k tokens (dependendo do modelo)",
            "rate_limit": "Varia conforme plano",
            "advantages": [
                "Modelos de altíssima qualidade", 
                "Suporte a múltiplas modalidades",
                "Documentação excelente"
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
            # self.client = OpenAI(api_key=openai_key)
            # self.current_model = model
            # print(f"Modelo alterado para {model} no {self.name}")
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
        return {
            "avg_response_time": "~2-8s",
            "reliability": "99.9%",
            "cost_per_request": "Varia ($0.0005-$0.03/1K tokens)",
            "quality": "Excelente",
            "requests_per_minute": "Depende do plano",
            "note": "Estatísticas estimadas - este é um exemplo mock"
        }