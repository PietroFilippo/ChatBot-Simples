"""
Componentes UI Especializados para Single Responsibility Principle.
Cada classe tem UMA responsabilidade específica na interface.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


# ========================================
# COMPONENTES DE EXIBIÇÃO - Display Components
# ========================================

class ChatMessageRenderer:
    """Responsabilidade única: renderizar mensagens de chat."""
    
    def __init__(self):
        self.provider_icons = {
            "groq": "🚀",
            "huggingface": "🤗",
            "unknown": "❓"
        }
    
    def render_user_message(self, message: str, timestamp: str) -> None:
        """Renderiza mensagem do usuário usando st.chat_message."""
        with st.chat_message("user"):
            st.markdown(f"**👤 Você ({timestamp}):**")
            st.markdown(message)
    
    def render_bot_message(self, message: str, provider: str) -> None:
        """Renderiza mensagem do bot usando st.chat_message."""
        icon = self.provider_icons.get(provider, self.provider_icons["unknown"])
        provider_name = provider.title()
        
        with st.chat_message("assistant"):
            st.markdown(f"**{icon} {provider_name} Assistant:**")
            st.markdown(message)
    
    def render_conversation_history(self, chat_history: List[Dict]) -> None:
        """Renderiza todo o histórico de conversa usando st.chat_message."""
        for msg in chat_history:
            self.render_user_message(msg['user'], msg['timestamp'])
            self.render_bot_message(msg['bot'], msg.get('provider', 'unknown'))


class MetricsDisplayer:
    """Responsabilidade única: exibir métricas e estatísticas."""
    
    def render_system_metrics(self, personality: str, provider_name: str, message_count: int) -> None:
        """Renderiza métricas do sistema."""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"🎭 Personalidade atual: **{personality.title()}**")
        
        with col2:
            icon = "🚀" if provider_name == "groq" else "🤗" if provider_name == "huggingface" else "❓"
            st.success(f"{icon} **{provider_name.title()}**")
        
        with col3:
            st.metric("Mensagens", message_count)
    
    def render_provider_metrics(self, all_providers: Dict[str, Any], available_count: int, current_name: str) -> None:
        """Renderiza métricas de provedores."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Provedores Registrados", len(all_providers))
        with col2:
            st.metric("Provedores Disponíveis", available_count)
        with col3:
            st.metric("Provedor Ativo", current_name.title())
    
    def render_text_statistics(self, stats: Dict[str, Any]) -> None:
        """Renderiza estatísticas de texto."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Palavras", stats["words"])
        with col2:
            st.metric("Frases", stats["sentences"])
        with col3:
            st.metric("Caracteres", stats["characters"])
        with col4:
            st.metric("Palavras/Frase", stats["avg_words_per_sentence"])


class StatusIndicator:
    """Responsabilidade única: indicar status de componentes."""
    
    def show_api_status(self, provider_name: str, is_available: bool, is_active: bool) -> None:
        """Mostra status de uma API."""
        if is_active and is_available:
            icon = "🟢"
            status_text = "ATIVO"
            st.success(f"{icon} **{provider_name.upper()}** - {status_text}")
        elif is_available:
            icon = "🔵"
            status_text = "DISPONÍVEL"
            st.info(f"{icon} **{provider_name.upper()}** - {status_text}")
        else:
            icon = "🔴"
            status_text = "INDISPONÍVEL"
            st.error(f"{icon} **{provider_name.upper()}** - {status_text}")
    
    def show_component_status(self, component_name: str, is_active: bool) -> None:
        """Mostra status de um componente."""
        status = "✅ Ativo" if is_active else "❌ Inativo"
        st.markdown(f"- **{component_name}:** {status}")


# ========================================
# COMPONENTES DE ENTRADA - Input Components
# ========================================

class InputCollector:
    """Responsabilidade única: coletar entrada do usuário."""
    
    def collect_chat_input(self, example_text: str, message_count: int) -> str:
        """Coleta entrada para chat."""
        user_input = st.chat_input(
            placeholder="Faça uma pergunta ou inicie uma conversa...",
            key=f"chat_input_{message_count}"
        )
        
        return user_input or ""
    
    def collect_text_for_analysis(self, example_text: str, placeholder: str, height: int = 150, context: str = "default") -> str:
        """Coleta texto para análise."""
        return st.text_area(
            "📝 Digite o texto para análise:",
            value=example_text,
            placeholder=placeholder,
            height=height,
            key=f"analysis_text_input_{context}"
        )
    
    def collect_summarizer_settings(self) -> Dict[str, Any]:
        """Coleta configurações do resumidor."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            summary_type = st.selectbox(
                "🎯 Tipo de Resumo:",
                ["informative", "executive", "creative", "technical"],
                help="Escolha o estilo do resumo"
            )
        
        with col2:
            max_sentences = st.slider(
                "📏 Frases (Extrativo):",
                min_value=1, max_value=10, value=3
            )
        
        return {
            "summary_type": summary_type,
            "max_sentences": max_sentences
        }


class ButtonController:
    """Responsabilidade única: gerenciar botões e ações."""
    
    def create_action_buttons(self, message_count: int) -> Dict[str, bool]:
        """Cria botões de ação e retorna estado."""
        # botões agrupados a esquerda
        col_buttons, col_empty = st.columns([2, 4])
        
        buttons = {}
        
        with col_buttons:
            # Subcolunas dentro da área dos botões para ficarem lado a lado
            subcol1, subcol2 = st.columns([1, 1])
            
            with subcol1:
                buttons["clear"] = st.button("🧹 Limpar", type="primary", key=f"clear_btn_{message_count}")
            
            with subcol2:
                self._render_back_to_top_button()
        
        # col_empty permanece vazia para manter layout consistente
        
        return buttons
    
    def _render_back_to_top_button(self) -> None:
        """Renderiza botão de voltar ao topo com estilo idêntico aos botões Streamlit"""
        st.markdown("""
        <div style="height: 2.5rem; display: flex; align-items: stretch;">
            <a href="#page-top" style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 100%;
                padding: 0.5rem 1rem;
                background-color: rgb(19, 23, 32);
                color: rgb(250, 250, 250);
                border: 1px solid rgb(70, 72, 83);
                border-radius: 0.5rem;
                text-decoration: none;
                font-weight: 400;
                font-size: 0.875rem;
                box-sizing: border-box;
                cursor: pointer;
                transition: all 0.2s ease;
                white-space: nowrap;
                font-family: 'Source Sans Pro', sans-serif;
            " onmouseover="this.style.borderColor='rgb(255, 75, 75)'; this.style.color='rgb(255, 75, 75)'" 
               onmouseout="this.style.borderColor='rgb(70, 72, 83)'; this.style.color='rgb(250, 250, 250)'">
                ⬆️ Voltar ao Topo
            </a>
        </div>
        """, unsafe_allow_html=True)


# ========================================
# COMPONENTES DE CONFIGURAÇÃO - Settings Components
# ========================================

class SettingsPanel:
    """Responsabilidade única: gerenciar painéis de configuração."""
    
    def render_provider_selector(self, available_providers: List[str], current_provider: str) -> Optional[str]:
        """Renderiza seletor de provedor."""
        if not available_providers:
            st.error("❌ Nenhuma API configurada")
            return None
        
        provider_names = {
            "groq": "🚀 Groq",
            "huggingface": "🤗 Hugging Face"
        }
        options = [provider_names.get(p, p.title()) for p in available_providers]
        
        try:
            current_index = available_providers.index(current_provider)
        except ValueError:
            current_index = 0
        
        selected_display = st.selectbox(
            "Escolha a API:",
            options,
            index=current_index,
            help="Selecione o provedor de LLM. Atualmente apenas Groq está disponível."
        )
        
        # Converte de volta para nome interno
        for internal_name, display_name in provider_names.items():
            if display_name == selected_display:
                return internal_name
        
        return None
    
    def render_personality_selector(self, current_personality: str) -> str:
        """Renderiza seletor de personalidade."""
        return st.selectbox(
            "Personalidade:",
            ["helpful", "creative", "technical"],
            index=["helpful", "creative", "technical"].index(current_personality),
            help="Escolha como o chatbot deve se comportar"
        )


# ========================================
# COMPONENTES DE VALIDAÇÃO - Validation Components
# ========================================

class InputValidator:
    """Responsabilidade única: validar entrada do usuário."""
    
    def validate_text_input(self, text: str, min_length: int = 1, max_length: int = 3000) -> Dict[str, Any]:
        """Valida entrada de texto."""
        if not text or not text.strip():
            return {
                "valid": False,
                "error": "Texto não pode estar vazio",
                "text": None
            }
        
        text = text.strip()
        
        if len(text) < min_length:
            return {
                "valid": False,
                "error": f"Texto deve ter pelo menos {min_length} caracteres",
                "text": None
            }
        
        if len(text) > max_length:
            return {
                "valid": False,
                "error": f"Texto deve ter no máximo {max_length} caracteres",
                "text": None
            }
        
        return {
            "valid": True,
            "error": None,
            "text": text
        }
    
    def validate_provider_available(self, provider_registry) -> Dict[str, Any]:
        """Valida se algum provedor está disponível."""
        if not provider_registry.is_any_provider_available():
            return {
                "valid": False,
                "error": "Nenhuma API configurada. Execute: python setup_env.py",
                "providers": []
            }
        
        return {
            "valid": True,
            "error": None,
            "providers": provider_registry.get_available_providers()
        }


# ========================================
# FÁBRICA DE COMPONENTES - Component Factory
# ========================================

class ComponentFactory:
    """Fábrica para criar componentes UI especializados."""
    
    @staticmethod
    def create_chat_components() -> Dict[str, Any]:
        """Cria conjunto de componentes para chat."""
        return {
            "message_renderer": ChatMessageRenderer(),
            "input_collector": InputCollector(),
            "button_controller": ButtonController(),
            "metrics_displayer": MetricsDisplayer(),
            "validator": InputValidator(),
            "status_indicator": StatusIndicator()
        }
    
    @staticmethod
    def create_analysis_components() -> Dict[str, Any]:
        """Cria conjunto de componentes para análise."""
        return {
            "input_collector": InputCollector(),
            "metrics_displayer": MetricsDisplayer(),
            "validator": InputValidator(),
            "status_indicator": StatusIndicator()
        }
    
    @staticmethod
    def create_settings_components() -> Dict[str, Any]:
        """Cria conjunto de componentes para configurações."""
        return {
            "settings_panel": SettingsPanel(),
            "status_indicator": StatusIndicator(),
            "metrics_displayer": MetricsDisplayer()
        } 