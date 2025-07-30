"""
Chatbot inteligente com memória conversacional usando LangChain.
Demonstra fluxos de IA generativa e boas práticas de desenvolvimento.
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
    
    def _clean_response(self, response: str) -> str:
        """Limpa a resposta removendo prefixos indesejados."""
        if not response:
            return "Desculpe, não consegui gerar uma resposta."
        
        # Remover prefixos comuns
        prefixes_to_remove = [
            "Assistente:",
            "Assistant:",
            "AI:",
            "Bot:",
            "Response:",
            "A:"
        ]
        
        for prefix in prefixes_to_remove:
            if response.strip().startswith(prefix):
                response = response.strip()[len(prefix):].strip()
        
        # Se a resposta estiver vazia após limpeza
        if not response.strip():
            return "Desculpe, não consegui gerar uma resposta adequada."
        
        return response.strip()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de conversação."""
        return self.conversation_history
    
    def clear_memory(self):
        """Limpa a memória conversacional."""
        self.memory.clear()
        self.conversation_history.clear()
        print("🧹 Memória do chatbot limpa!")
    
    def change_personality(self, new_personality: str):
        """Muda a personalidade do chatbot."""
        if new_personality in ["helpful", "creative", "technical"]:
            self.personality = new_personality
            print(f"Personalidade alterada para '{new_personality}'")
        else:
            print("Personalidade inválida. Use: helpful, creative, technical")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da conversa."""
        if not self.conversation_history:
            return {"messages": 0, "avg_length": 0}
        
        total_messages = len(self.conversation_history)
        avg_user_length = sum(len(msg["user"]) for msg in self.conversation_history) / total_messages
        avg_bot_length = sum(len(msg["bot"]) for msg in self.conversation_history) / total_messages
        
        return {
            "messages": total_messages,
            "avg_user_length": round(avg_user_length, 1),
            "avg_bot_length": round(avg_bot_length, 1),
            "personality": self.personality,
            "provider": "groq",
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        Prepara a conversa para download
        
        Returns:
            Dicionário com dados da conversa e informações para download
        """
        try:
            import json
            from datetime import datetime
            
            # Prepara dados para exportação
            export_data = {
                "export_info": {
                    "timestamp": datetime.now().isoformat(),
                    "total_messages": len(self.conversation_history),
                    "personality": self.personality,
                    "provider": "groq"
                },
                "conversation": self.conversation_history,
                "stats": self.get_stats()
            }
            
            # Gera o nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_json = f"conversa_chatbot_{timestamp}.json"
            filename_txt = f"conversa_chatbot_{timestamp}.txt"
            
            # Converte para JSON
            json_content = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            # Converte para texto simples
            txt_content = f"=== CONVERSA CHATBOT ===\n"
            txt_content += f"Data: {export_data['export_info']['timestamp']}\n"
            txt_content += f"Personalidade: {export_data['export_info']['personality']}\n"
            txt_content += f"Total de mensagens: {export_data['export_info']['total_messages']}\n\n"
            
            for i, msg in enumerate(self.conversation_history, 1):
                txt_content += f"[{i}] USUÁRIO: {msg['user']}\n"
                txt_content += f"[{i}] ASSISTENTE: {msg['bot']}\n\n"
            
            return {
                "success": True,
                "json_content": json_content,
                "txt_content": txt_content,
                "filename_json": filename_json,
                "filename_txt": filename_txt,
                "export_data": export_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao preparar conversa: {str(e)}"
            }
    
    def export_conversation_to_file(self, filepath: str, format_type: str = "json") -> str:
        """
        Exporta conversa para um arquivo específico (fallback method)
        
        Args:
            filepath: Caminho completo do arquivo
            format_type: Formato ('json' ou 'txt')
            
        Returns:
            Mensagem de resultado
        """
        try:
            import json
            from datetime import datetime
            import os
            
            # Prepara dados
            export_data = {
                "export_info": {
                    "timestamp": datetime.now().isoformat(),
                    "total_messages": len(self.conversation_history),
                    "personality": self.personality,
                    "provider": "groq"
                },
                "conversation": self.conversation_history,
                "stats": self.get_stats()
            }
            
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Salva o arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                if format_type.lower() == "json":
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                else:
                    # Formato de texto simples
                    f.write(f"=== CONVERSA CHATBOT ===\n")
                    f.write(f"Data: {export_data['export_info']['timestamp']}\n")
                    f.write(f"Personalidade: {export_data['export_info']['personality']}\n")
                    f.write(f"Total de mensagens: {export_data['export_info']['total_messages']}\n\n")
                    
                    for i, msg in enumerate(self.conversation_history, 1):
                        f.write(f"[{i}] USUÁRIO: {msg['user']}\n")
                        f.write(f"[{i}] ASSISTENTE: {msg['bot']}\n\n")
            
            return f"Conversa salva em: {filepath}"
            
        except Exception as e:
            return f"Erro ao salvar conversa: {str(e)}" 	