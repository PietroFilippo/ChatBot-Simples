"""
Chatbot inteligente com memória conversacional usando LangChain.
"""

from typing import List, Dict, Any, Optional
from src.llm_providers import llm_manager
import json
from datetime import datetime

class IntelligentChatbot:
    """Chatbot avançado com personalidade e memória conversacional"""
    
    def __init__(self, personality: str = "helpful", memory_size: int = 10):
        """
        Inicializa o chatbot com personalidade e configurações
        
        Args:
            personality: Tipo de personalidade ('helpful', 'creative', 'technical')
            memory_size: Número de mensagens para manter em memória
        """
        self.personality = personality
        self.memory_size = memory_size
        self.conversation_history = []
        self.memory = []  # Memória simplificada
        
        print(f"🤖 Chatbot inicializado com personalidade '{personality}'")
    
    def _get_personality_prompt(self) -> str:
        """Retorna o prompt de personalidade."""
        personality_prompts = {
            "helpful": """Você é um assistente de IA muito útil e amigável. 
                         Responda SEMPRE na língua que o usuário está falando, de forma clara, prestativa e educada. 
                         Sempre tente ajudar o usuário da melhor forma possível.
                         Use a língua do usuário e de forma natural.""",
            
            "creative": """Você é um assistente de IA criativo e imaginativo. 
                          Responda SEMPRE na língua que o usuário está falando, de forma original, inspiradora e com um toque artístico. 
                          Use analogias e exemplos criativos.
                          Use a língua do usuário e de forma natural.""",
            
            "technical": """Você é um assistente de IA especializado em tecnologia. 
                           Responda SEMPRE na língua que o usuário está falando com precisão técnica, use terminologia apropriada, 
                           e forneça explicações detalhadas e estruturadas.
                           Use a língua do usuário e de forma natural."""
        }
        
        return personality_prompts.get(self.personality, personality_prompts["helpful"])
    
    def _build_context_message(self, message: str) -> str:
        """Constrói mensagem com contexto de personalidade e memória."""
        # Prompt de personalidade
        context = self._get_personality_prompt() + "\n\n"
        
        # Adiciona o histórico recente se houver
        if self.memory:
            context += "Histórico da conversa:\n"
            for entry in self.memory[-5:]:  # Últimas 5 interações
                context += f"Usuário: {entry['user']}\n"
                context += f"Assistente: {entry['bot']}\n"
            context += "\n"
        
        # Mensagem atual
        context += f"Usuário: {message}\nAssistente:"
        
        return context
    
    def chat(self, message: str) -> str:
        """
        Processa uma mensagem do usuário e retorna a resposta
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta do chatbot
        """
        try:
            # Adiciona o timestamp
            timestamp = datetime.now().strftime("%H:%M")
            
            # Construe uma mensagem com contexto
            context_message = self._build_context_message(message)
            
            # Obtém a resposta do LLM
            response = llm_manager.invoke_llm(context_message)
            
            # Limpa a resposta (remover possíveis prefixos)
            response = self._clean_response(response)
            
            # Salva na história e memória
            entry = {
                "timestamp": timestamp,
                "user": message,
                "bot": response,
                "provider": "groq"
            }
            
            self.conversation_history.append(entry)
            self.memory.append(entry)
            
            # Mantem apenas as últimas interações na memória
            if len(self.memory) > self.memory_size:
                self.memory = self.memory[-self.memory_size:]
            
            return response
            
        except Exception as e:
            error_msg = f"Desculpe, encontrei um erro: {str(e)}"
            print(f"Erro no chat: {e}")
            return error_msg