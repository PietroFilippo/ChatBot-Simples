"""
Implementação específica do provedor Groq refatorado.
Agora usa BaseProvider para eliminar duplicação de código.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv
from .base_provider import BaseProvider
from src.config import GlobalConfig

# Carrega as variáveis de ambiente
load_dotenv()


class GroqProvider(BaseProvider):
    """Provedor Groq refatorado usando BaseProvider - 70% menos código!"""
    
    def __init__(self):
        # Define modelo padrão e current_model ANTES de chamar super()
        self.default_model = "llama3-70b-8192"
        self.current_model = os.getenv("DEFAULT_MODEL", self.default_model) or self.default_model
        
        # Chama o construtor da classe base com configurações específicas
        super().__init__(
            name="groq",
            available_models=[
                "llama3-70b-8192",
                "llama3-8b-8192",
                "gemma2-9b-it"    
            ]
        )
        # Não resetar self.llm aqui - ele já foi configurado no _setup()!
    
    def _setup(self):
        """Configuração específica do Groq."""
        try:
            # Recarrega .env para garantir que as variáveis estão atualizadas
            load_dotenv()
            groq_key = os.getenv("GROQ_API_KEY")
            
            if groq_key and groq_key.strip():
                try:
                    from langchain_groq import ChatGroq
                    
                    # Usa configurações globais centralizadas
                    params = GlobalConfig.get_generation_params()
                    
                    self.llm = ChatGroq(
                        api_key=groq_key,
                        model=self.current_model,
                        temperature=params["temperature"],
                        max_tokens=params["max_tokens"]
                    )
                    
                    # Só marca como disponível se o LLM foi criado com sucesso
                    if self.llm is not None:
                        self.status = "available"
                        print(f"Groq Provider configurado com modelo {self.current_model}")
                        print(f"Configurações: temp={params['temperature']}, max_tokens={params['max_tokens']}")
                    else:
                        self.status = "error"
                        print("Erro: LLM Groq não foi inicializado corretamente")
                        
                except ImportError as e:
                    print(f"Erro no import langchain_groq: {e}")
                    self.status = "error"
                    self.llm = None
                except Exception as e:
                    print(f"Erro ao criar ChatGroq: {e}")
                    self.status = "error"
                    self.llm = None
            else:
                print("GROQ_API_KEY não encontrada ou vazia")
                self.status = "unavailable"
        except Exception as e:
            print(f"Erro ao configurar Groq: {e}")
            self.status = "error"
            self.llm = None
    
    def _generate_response_impl(self, message: str, **kwargs) -> str:
        """Implementação específica da geração de resposta do Groq."""
        if self.llm is None:
            raise Exception("LLM não configurado. Verifique GROQ_API_KEY.")
        
        response = self.llm.invoke(message)
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    
    def get_info(self) -> Dict[str, Any]:
        """Informações específicas do Groq."""
        base_stats = self.get_stats()  # Estatísticas da classe base
        
        return {
            "provider": self.name,
            "status": self.status,
            "speed": "fast",
            "cost": "free",
            "current_model": self.current_model,
            "description": "API ultra-rápida com modelos Llama 3",
            "context_length": "8192 tokens",
            "rate_limit": "30 requests/minute (gratuito)",
            "advantages": ["Velocidade excepcional", "Modelos potentes", "100% Gratuito"],
            **base_stats  # Adiciona estatísticas comuns
        }
    
    def switch_model(self, model: str) -> bool:
        """Troca modelo específico do Groq."""
        if model not in self.available_models:
            print(f"Modelo '{model}' não disponível para {self.name}")
            return False
        
        try:
            load_dotenv()  # Recarrega .env
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key or not groq_key.strip():
                print("GROQ_API_KEY não encontrada ou vazia")
                return False
            
            from langchain_groq import ChatGroq
            
            # Usa configurações globais centralizadas
            params = GlobalConfig.get_generation_params()
            
            # Cria nova instância com modelo diferente
            self.llm = ChatGroq(
                api_key=groq_key,
                model=model,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"]
            )
            
            if self.llm is not None:
                self.current_model = model
                self.status = "available"
                print(f"Modelo do Groq alterado para: {model}")
                return True
            else:
                print("Erro ao criar nova instância do LLM")
                return False
            
        except Exception as e:
            print(f"Erro ao trocar modelo Groq: {e}")
            self.status = "error"
            return False 