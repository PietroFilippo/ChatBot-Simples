"""
Chatbot inteligente com memória conversacional usando LangChain.
Demonstra fluxos de IA generativa e boas práticas de desenvolvimento.
Implementa Dependency Inversion Principle.
"""

from typing import List, Dict, Any, Optional
from src.interfaces import ILLMService, IChatbotService
import json
from datetime import datetime


class IntelligentChatbot(IChatbotService):
    """Chatbot avançado com personalidade e memória conversacional."""
    
    def __init__(self, llm_service: ILLMService, personality: str = "helpful", memory_size: int = 10):
        """
        Inicializa o chatbot com dependência injetada.
        
        Args:
            llm_service: Serviço LLM (abstração injetada)
            personality: Tipo de personalidade ('helpful', 'creative', 'technical')
            memory_size: Número de mensagens para manter em memória
        """
        self._llm_service = llm_service
        self.personality = personality
        self.memory_size = memory_size
        self.conversation_history = []
        self.memory = []  # Memória simplificada
        
        print(f"Chatbot inicializado - personalidade '{personality}'")
    
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
        """Constrói mensagem com contexto e personalidade."""
        # Prompt de personalidade
        personality_prompt = self._get_personality_prompt()
        
        # Contexto de memória
        memory_context = ""
        if self.memory:
            memory_context = "\n\nContexto da conversa anterior:\n"
            for mem in self.memory[-3:]:  # Últimas 3 interações
                memory_context += f"- {mem}\n"
        
        # Mensagem completa
        full_message = f"{personality_prompt}\n{memory_context}\n\nUsuário: {message}"
        
        return full_message
    
    def _update_memory(self, user_message: str, bot_response: str):
        """Atualiza a memória conversacional."""
        memory_entry = f"User: {user_message[:100]}... | Bot: {bot_response[:100]}..."
        self.memory.append(memory_entry)
        
        # Mantém apenas as últimas interações
        if len(self.memory) > self.memory_size:
            self.memory = self.memory[-self.memory_size:]
    
    def chat(self, message: str) -> str:
        """
        Processa uma mensagem de chat.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta do chatbot
        """
        # Verifica se o serviço LLM está disponível
        if not self._llm_service.is_available():
            return "Serviço LLM não disponível. Configure uma API key."
        
        try:
            # Constrói a mensagem com contexto
            context_message = self._build_context_message(message)
            
            # Gera resposta usando o serviço LLM injetado
            response = self._llm_service.generate_response(context_message)
            
            # Atualiza memória e histórico
            self._update_memory(message, response)
            self._add_to_conversation_history(message, response)
            
            return response
            
        except Exception as e:
            error_msg = f"Erro no chatbot: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _add_to_conversation_history(self, user_message: str, bot_response: str):
        """Adiciona interação ao histórico completo."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": bot_response,
            "provider": self._llm_service.get_current_provider_name()
        }
        self.conversation_history.append(interaction)
    
    def clear_memory(self) -> None:
        """Limpa a memória do chatbot."""
        self.memory.clear()
        self.conversation_history.clear()
        print("🧹 Memória do chatbot limpa")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do chatbot.
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.conversation_history:
            return {
                "messages": 0,
                "avg_user_length": 0,
                "avg_bot_length": 0,
                "personality": self.personality,
                "provider": self._llm_service.get_current_provider_name()
            }
        
        user_lengths = [len(conv["user"]) for conv in self.conversation_history]
        bot_lengths = [len(conv["bot"]) for conv in self.conversation_history]
        
        return {
            "messages": len(self.conversation_history),
            "avg_user_length": sum(user_lengths) / len(user_lengths),
            "avg_bot_length": sum(bot_lengths) / len(bot_lengths),
            "personality": self.personality,
            "provider": self._llm_service.get_current_provider_name()
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        Exporta a conversa em formato estruturado.
        
        Returns:
            Dados de exportação com conteúdo em JSON e TXT
        """
        if not self.conversation_history:
            return {"success": False, "error": "Nenhuma conversa para exportar"}
        
        try:
            # Dados para exportação
            export_data = {
                "export_info": {
                    "total_messages": len(self.conversation_history),
                    "personality": self.personality,
                    "provider": self._llm_service.get_current_provider_name(),
                    "exported_at": datetime.now().isoformat()
                },
                "conversation": self.conversation_history
            }
            
            # Conteúdo JSON
            json_content = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            # Conteúdo TXT
            txt_content = f"Conversa do Chatbot - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            txt_content += f"Personalidade: {self.personality}\n"
            txt_content += f"Provedor: {self._llm_service.get_current_provider_name()}\n"
            txt_content += "=" * 50 + "\n\n"
            
            for i, conv in enumerate(self.conversation_history, 1):
                txt_content += f"[{i}] {conv['timestamp']}\n"
                txt_content += f"👤 Usuário: {conv['user']}\n"
                txt_content += f"🤖 Bot: {conv['bot']}\n\n"
            
            # Nomes dos arquivos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_json = f"chatbot_conversa_{timestamp}.json"
            filename_txt = f"chatbot_conversa_{timestamp}.txt"
            
            return {
                "success": True,
                "export_data": export_data,
                "json_content": json_content,
                "txt_content": txt_content,
                "filename_json": filename_json,
                "filename_txt": filename_txt
            }
            
        except Exception as e:
            return {"success": False, "error": f"Erro na exportação: {str(e)}"} 