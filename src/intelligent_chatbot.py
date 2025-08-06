"""
Chatbot Inteligente com Gerenciamento Adaptativo de Contexto.
Versão otimizada que maximiza o uso da capacidade real dos modelos.
"""

from typing import Dict, Any, Optional
from src.interfaces import ILLMService, IChatbotService
from src.context_manager import IntelligentContextManager
from src.config import GlobalConfig
from datetime import datetime

logger = GlobalConfig.get_logger('chatbot')

class IntelligentChatbotV2(IChatbotService):
    """
    Chatbot avançado com gerenciamento inteligente de contexto.
    
    Características:
    - Contagem precisa de tokens
    - Otimização automática do contexto
    - Adaptação dinâmica aos limites do modelo
    - Priorização inteligente de mensagens
    - Métricas detalhadas de performance
    """
    
    def __init__(self, llm_service: ILLMService, personality: str = "helpful"):
        """
        Inicializa o chatbot inteligente.
        
        Args:
            llm_service: Serviço LLM injetado
            personality: Personalidade do chatbot
        """
        self._llm_service = llm_service
        self.personality = personality
        
        # Obtém o modelo atual do provider
        current_model = self._get_current_model_name()
        
        # Inicializa gerenciador de contexto inteligente
        self.context_manager = IntelligentContextManager(current_model)
        
        # Define prompt de sistema baseado na personalidade
        self.context_manager.set_system_prompt(self._get_personality_prompt())
        
        # Histórico completo para export/analytics
        self.full_conversation_history = []
        
        logger.info(f"Chatbot inteligente inicializado: personalidade={personality}, modelo={current_model}")
    
    def _get_current_model_name(self) -> str:
        """Obtém o nome do modelo atual do provider."""
        try:
            if hasattr(self._llm_service, 'get_current_provider'):
                provider = self._llm_service.get_current_provider()
                if provider and hasattr(provider, 'get_current_model'):
                    model_name = provider.get_current_model()
                    logger.debug(f"Modelo atual obtido: {model_name}")
                    return model_name
            logger.debug("Usando modelo padrão (default)")
            return "default"
        except Exception as e:
            logger.warning(f"Erro ao obter modelo atual, usando default: {e}")
            return "default"
    
    def _get_personality_prompt(self) -> str:
        """Retorna o prompt de personalidade otimizado."""
        personality_prompts = {
            "helpful": """Você é um assistente útil e prestativo. Forneça respostas claras, precisas e detalhadas. 
Seja educado, empático e focado em resolver problemas do usuário de forma eficiente.""",
            
            "creative": """Você é um assistente criativo e inovador. Use sua imaginação para fornecer respostas 
originais e interessantes. Seja expressivo, use analogias e exemplos criativos quando apropriado.""",
            
            "technical": """Você é um especialista técnico. Forneça respostas precisas, detalhadas e bem fundamentadas. 
Use terminologia técnica apropriada e inclua exemplos práticos quando relevante. Seja conciso mas completo."""
        }
        
        prompt = personality_prompts.get(self.personality, personality_prompts["helpful"])
        logger.debug(f"Prompt de personalidade definido: {self.personality}")
        return prompt
    
    def chat(self, message: str) -> str:
        """
        Processa uma mensagem usando gerenciamento inteligente de contexto.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta otimizada do chatbot
        """
        if not self._llm_service.is_available():
            error_msg = "❌ Serviço LLM não disponível. Configure uma API key."
            logger.warning("Tentativa de chat com serviço LLM indisponível")
            return error_msg
        
        try:
            logger.info(f"Processando mensagem: {len(message)} chars")
            
            # Verifica se modelo mudou e atualiza contexto se necessário
            self._check_and_update_model()
            
            # Adiciona mensagem do usuário ao contexto
            self.context_manager.add_message("user", message)
            
            # Gera contexto otimizado para o modelo
            if hasattr(self._llm_service, 'supports_message_format') and self._llm_service.supports_message_format():
                # Usa formato de mensagens se suportado
                context = self.context_manager.get_context_messages()
                response = self._llm_service.generate_response_from_messages(context)
                logger.debug("Usando formato de mensagens estruturadas")
            else:
                # Usa formato de string tradicional
                context = self.context_manager.get_context_for_model()
                response = self._llm_service.generate_response(f"{context}\n\nUsuário: {message}")
                logger.debug("Usando formato de string tradicional")
            
            # Adiciona resposta do assistente ao contexto
            provider_name = self._get_current_provider_name()
            self.context_manager.add_message("assistant", response, provider_name)
            
            # Atualiza histórico completo
            self._update_full_history(message, response)
            
            logger.info(f"Resposta gerada com sucesso: {len(response)} chars")
            return response
            
        except Exception as e:
            error_msg = f"❌ Erro no chatbot inteligente: {str(e)}"
            logger.error(f"Erro no processamento do chat: {e}")
            return error_msg
    
    def _check_and_update_model(self) -> None:
        """Verifica se o modelo mudou e atualiza o contexto se necessário."""
        current_model = self._get_current_model_name()
        if current_model != self.context_manager.model_name:
            logger.info(f"Modelo alterado: {self.context_manager.model_name} -> {current_model}")
            self.context_manager.update_model(current_model)
    
    def _get_current_provider_name(self) -> str:
        """Obtém o nome do provider atual."""
        try:
            if hasattr(self._llm_service, 'get_current_provider_name'):
                name = self._llm_service.get_current_provider_name()
                logger.debug(f"Provider atual: {name}")
                return name
            return "unknown"
        except Exception as e:
            logger.warning(f"Erro ao obter nome do provider: {e}")
            return "unknown"
    
    def _update_full_history(self, user_message: str, bot_response: str) -> None:
        """Atualiza o histórico completo para analytics."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": bot_response,
            "provider": self._get_current_provider_name(),
            "model": self.context_manager.model_name,
            "context_stats": self.context_manager.get_stats()
        }
        self.full_conversation_history.append(interaction)
        logger.debug(f"Histórico atualizado: {len(self.full_conversation_history)} interações")
    
    def clear_memory(self) -> None:
        """Limpa toda a memória do chatbot."""
        old_count = len(self.full_conversation_history)
        self.context_manager.clear_context()
        self.full_conversation_history.clear()
        logger.info(f"Memória limpa: {old_count} interações removidas")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas avançadas do chatbot.
        
        Returns:
            Dicionário com métricas detalhadas
        """
        context_stats = self.context_manager.get_stats()
        
        # Estatísticas básicas
        total_interactions = len(self.full_conversation_history)
        
        if total_interactions > 0:
            # Valida formato do histórico para evitar erros
            valid_interactions = []
            for interaction in self.full_conversation_history:
                if isinstance(interaction, dict) and "user" in interaction and "bot" in interaction:
                    valid_interactions.append(interaction)
                else:
                    # Log de debug para problemas de formato
                    logger.debug(f"⚠️  Interação com formato inválido ignorada: {type(interaction)}")
            
            if valid_interactions:
                # Calcula médias de tamanho apenas com interações válidas
                user_lengths = [len(interaction["user"]) for interaction in valid_interactions]
                bot_lengths = [len(interaction["bot"]) for interaction in valid_interactions]
                
                avg_user_length = sum(user_lengths) / len(user_lengths)
                avg_bot_length = sum(bot_lengths) / len(bot_lengths)
                
                # Análise de providers usados
                providers_used = set(interaction.get("provider", "unknown") for interaction in valid_interactions)
                
                # Análise temporal
                try:
                    first_interaction = datetime.fromisoformat(valid_interactions[0]["timestamp"])
                    session_duration = datetime.now() - first_interaction
                except (KeyError, ValueError):
                    session_duration = None
            else:
                avg_user_length = avg_bot_length = 0
                providers_used = set()
                session_duration = None
        else:
            avg_user_length = avg_bot_length = 0
            providers_used = set()
            session_duration = None
        
        return {
            # Estatísticas básicas
            "personality": self.personality,
            "total_interactions": total_interactions,
            "messages": total_interactions,  # ✅ Compatibilidade com app.py
            "avg_user_length": avg_user_length,
            "avg_bot_length": avg_bot_length,
            "providers_used": list(providers_used),
            "session_duration_minutes": session_duration.total_seconds() / 60 if session_duration else 0,
            
            # Estatísticas de contexto inteligente
            **context_stats,
            
            # Métricas de eficiência
            "context_optimization_active": True,
            "intelligent_pruning": True,
            "token_counting_method": type(self.context_manager.token_counter).__name__,
        }
    
    def get_context_analytics(self) -> Dict[str, Any]:
        """
        Retorna análises detalhadas do contexto para debugging e otimização.
        
        Returns:
            Análises avançadas do contexto
        """
        stats = self.context_manager.get_stats()
        
        # Análise das mensagens no contexto atual
        messages_analysis = []
        for entry in self.context_manager.conversation_history:
            messages_analysis.append({
                "role": entry.role,
                "tokens": entry.tokens,
                "importance_score": entry.importance_score,
                "age_minutes": (datetime.now() - entry.timestamp).total_seconds() / 60,
                "provider": entry.provider,
                "content_preview": entry.content[:50] + "..." if len(entry.content) > 50 else entry.content
            })
        
        return {
            "context_stats": stats,
            "messages_in_context": messages_analysis,
            "model_limits": {
                "max_context_tokens": self.context_manager.limits.max_context_tokens,
                "max_output_tokens": self.context_manager.limits.max_output_tokens,
                "available_tokens": self.context_manager.limits.available_tokens,
                "reserved_tokens": self.context_manager.limits.reserved_tokens
            },
            "optimization_history": {
                "total_messages_ever": len(self.full_conversation_history),
                "messages_in_context": len(self.context_manager.conversation_history),
                "pruning_efficiency": (len(self.full_conversation_history) - len(self.context_manager.conversation_history)) / max(1, len(self.full_conversation_history)) * 100
            }
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        Exporta toda a conversa com metadados avançados.
        
        Returns:
            Dicionário no formato esperado pelo app.py
        """
        try:
            # Dados básicos da exportação
            export_data = {
                "metadata": {
                    "personality": self.personality,
                    "export_timestamp": datetime.now().isoformat(),
                    "total_interactions": len(self.full_conversation_history),
                    "session_stats": self.get_stats()
                },
                "conversation_history": self.full_conversation_history,
                "analytics": self.get_context_analytics(),
                "export_info": {
                    "total_messages": len(self.full_conversation_history),
                    "export_format": "intelligent_chatbot_v2"
                }
            }
            
            # Gera conteúdo JSON
            import json
            json_content = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
            
            # Gera conteúdo TXT legível
            txt_lines = [
                f"=== CONVERSA EXPORTADA ===",
                f"Personalidade: {self.personality}",
                f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                f"Total de mensagens: {len(self.full_conversation_history)}",
                f"",
                f"=== HISTÓRICO DA CONVERSA ===",
                f""
            ]
            
            for i, interaction in enumerate(self.full_conversation_history, 1):
                if isinstance(interaction, dict) and "user" in interaction and "bot" in interaction:
                    timestamp = interaction.get("timestamp", "")
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            time_str = dt.strftime("%H:%M:%S")
                        except:
                            time_str = timestamp[:19] if len(timestamp) > 19 else timestamp
                    else:
                        time_str = "N/A"
                    
                    txt_lines.extend([
                        f"--- Interação {i} ({time_str}) ---",
                        f"👤 Usuário: {interaction['user']}",
                        f"🤖 Bot: {interaction['bot']}",
                        f"Provider: {interaction.get('provider', 'N/A')}",
                        f"Modelo: {interaction.get('model', 'N/A')}",
                        f""
                    ])
            
            # Adiciona estatísticas ao final
            stats = self.get_stats()
            txt_lines.extend([
                f"=== ESTATÍSTICAS DA SESSÃO ===",
                f"Personalidade: {stats['personality']}",
                f"Total de interações: {stats['total_interactions']}",
                f"Duração da sessão: {stats['session_duration_minutes']:.1f} minutos",
                f"Tamanho médio - Usuário: {stats['avg_user_length']:.0f} chars",
                f"Tamanho médio - Bot: {stats['avg_bot_length']:.0f} chars",
                f"Providers usados: {', '.join(stats['providers_used'])}",
                f"Contexto inteligente: Ativo",
                f"Método de contagem: {stats['token_counting_method']}",
                f"Tokens no contexto: {stats.get('total_tokens', 'N/A')}",
                f"Utilização do contexto: {stats.get('utilization_percentage', 0):.1f}%",
            ])
            
            txt_content = "\n".join(txt_lines)
            
            # Nomes dos arquivos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_json = f"conversa_chatbot_{timestamp}.json"
            filename_txt = f"conversa_chatbot_{timestamp}.txt"
            
            return {
                "success": True,
                "json_content": json_content,
                "filename_json": filename_json,
                "txt_content": txt_content,
                "filename_txt": filename_txt,
                "export_data": export_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao exportar conversa: {str(e)}"
            }
    
    def optimize_context_for_model(self, model_name: str) -> Dict[str, Any]:
        """
        Otimiza o contexto para um modelo específico.
        
        Args:
            model_name: Nome do modelo alvo
            
        Returns:
            Relatório da otimização
        """
        old_stats = self.context_manager.get_stats()
        
        # Atualiza para o novo modelo
        self.context_manager.update_model(model_name)
        
        new_stats = self.context_manager.get_stats()
        
        return {
            "optimization_report": {
                "old_model": old_stats["model_name"],
                "new_model": new_stats["model_name"],
                "old_utilization": old_stats["utilization_percentage"],
                "new_utilization": new_stats["utilization_percentage"],
                "messages_before": old_stats["total_messages"],
                "messages_after": new_stats["total_messages"],
                "tokens_before": old_stats["total_tokens"],
                "tokens_after": new_stats["total_tokens"],
                "efficiency_gain": new_stats["utilization_percentage"] - old_stats["utilization_percentage"]
            }
        }
    
    @property
    def conversation_history(self):
        """Propriedade para compatibilidade com a interface existente."""
        return self.full_conversation_history
    
    @conversation_history.setter
    def conversation_history(self, value):
        """Setter para permitir restauração do histórico."""
        self.full_conversation_history = value
        # Sincroniza com o context_manager se necessário
        if value and hasattr(self, 'context_manager'):
            # Reconstrói o contexto baseado no histórico fornecido
            self.context_manager.clear_context()
            for interaction in value:
                if isinstance(interaction, dict):
                    # Formato do app.py: {"user": "...", "bot": "...", ...}
                    if "user" in interaction and "bot" in interaction:
                        self.context_manager.add_message("user", interaction["user"])
                        provider = interaction.get("provider", "unknown")
                        self.context_manager.add_message("assistant", interaction["bot"], provider)
    
    @property
    def memory(self):
        """Propriedade para compatibilidade com a interface existente."""
        # Retorna uma versão simplificada do contexto atual
        return [f"{entry.role}: {entry.content[:100]}..." for entry in self.context_manager.conversation_history]
    
    @memory.setter  
    def memory(self, value):
        """Setter para permitir restauração da memória."""
        # Para compatibilidade, aceita mas não faz nada específico
        # pois o sistema inteligente gerencia automaticamente
        pass 