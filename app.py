"""
Sistema de IA Generativa Multi-Funcional
Interface principal usando Streamlit
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
from datetime import datetime
import json

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos do projeto
from src.llm_providers import llm_manager
from src.chatbot import IntelligentChatbot
from src.sentiment import sentiment_analyzer
from src.summarizer import summarizer
from utils.helpers import (
    measure_execution_time, format_text_for_display, clean_text,
    calculate_text_stats, get_emoji_for_sentiment, format_confidence_display,
    validate_text_input, create_download_link
)

# Configuração da página
st.set_page_config(
    page_title="IA Generativa Multi-Funcional",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para interface moderna
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-card {
        background: var(--background-color);
        border: 1px solid var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .feature-card h4 {
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: var(--text-color);
        margin: 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Compatibilidade com tema escuro */
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background: #262730;
            border-color: #464853;
            color: #fafafa;
        }
        
        .feature-card h4,
        .feature-card p {
            color: #fafafa;
        }
    }
    
    /* Força o tema escuro pro Streamlit */
    .stApp {
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --text-color: #fafafa;
    }
    
    .feature-card {
        background: #262730 !important;
        border-color: #464853 !important;
        color: #fafafa !important;
    }
    
    .feature-card h4,
    .feature-card p {
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)

def preserve_chatbot_state(new_personality: str = None):
    """
    Preserva o estado do chatbot quando recria a instância
    
    Args:
        new_personality: Nova personalidade (opcional, mantém a atual)
    """
    if hasattr(st.session_state, 'chatbot'):
        # Salva o estado atual
        old_history = st.session_state.chatbot.conversation_history.copy()
        old_memory = st.session_state.chatbot.memory.copy()
        old_personality = new_personality or st.session_state.chatbot.personality
        
        # Recria o chatbot com o mesmo estado
        st.session_state.chatbot = IntelligentChatbot(
            personality=old_personality
        )
        
        # Restaura o histórico preservado
        st.session_state.chatbot.conversation_history = old_history
        st.session_state.chatbot.memory = old_memory
        
        return len(old_history)
    return 0

def initialize_session_state():
    """Inicializa variáveis de sessão"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = IntelligentChatbot()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

def show_header():
    """Exibe o cabeçalho principal"""
    # Âncora para o topo da página
    st.markdown('<a id="page-top"></a>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">Sistema de IA Generativa Multi-Funcional</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Utilização de <strong>LangChain</strong>, <strong>LLMs gratuitos</strong> e <strong>fluxos de IA</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Configura sidebar com informações e configurações"""
    st.sidebar.title("⚙️ Configurações")
    
    # Seletor de Provedor LLM
    st.sidebar.subheader("🔗 Seletor de API")
    
    # Obtem provedores disponíveis
    providers = llm_manager.get_available_providers()
    available_providers = [name for name, info in providers.items() if info["status"] == "available"]
    all_providers = list(providers.keys())
    
    if available_providers:
        # Criação do mapeamento
        provider_names = {
            "groq": "🚀 Groq"
        }
        
        # Opções do selectbox
        options = [provider_names.get(p, p.title()) for p in available_providers]
        current_index = available_providers.index(llm_manager.current_provider) if llm_manager.current_provider in available_providers else 0
        
        # Selectbox para escolher provedor
        selected_display = st.sidebar.selectbox(
            "Escolha a API:",
            options,
            index=current_index,
            help="Selecione o provedor de LLM. Atualmente apenas Groq está disponível."
        )
        
        # Converte de volta para o nome interno
        selected_provider = None
        for internal_name, display_name in provider_names.items():
            if display_name == selected_display:
                selected_provider = internal_name
                break
        
        # Troca o provedor se necessário
        if selected_provider and selected_provider != llm_manager.current_provider:
            if llm_manager.switch_provider(selected_provider):
                st.sidebar.success(f"Mudou para: {selected_display}")
                
                # Preserva o histórico ao trocar o provedor
                msg_count = preserve_chatbot_state()
                if msg_count > 0:
                    st.sidebar.info(f"📊 Histórico preservado: {msg_count} mensagens")
                
                st.rerun()
    else:
        st.sidebar.error("❌ Nenhuma API configurada")
        st.sidebar.warning("Configure pelo menos uma API para usar o sistema")
    
    # Status dos provedores
    st.sidebar.subheader("📊 Status das APIs")
    
    for provider, info in providers.items():
        status_emoji = "" if info["status"] == "available" else "❌" if info["status"] == "unavailable" else "⚠️"
        speed_info = f"({info['speed']}, {info['cost']})"
        
        if provider == llm_manager.current_provider:
            st.sidebar.success(f"{status_emoji} **{provider.title()}** {speed_info} - ATIVO")
        elif info["status"] == "available":
            st.sidebar.info(f"{status_emoji} {provider.title()} {speed_info}")
        else:
            st.sidebar.error(f"{status_emoji} {provider.title()} {speed_info} - Não configurado")
    
    # Informações detalhadas do provedor ativo
    if llm_manager.current_provider and llm_manager.current_provider in providers:
        current_info = providers[llm_manager.current_provider]
        st.sidebar.markdown("---")
        
        # API Ativa com expander
        with st.sidebar.expander("🎯 API Ativa", expanded=True):
            st.markdown(f"- **Nome:** {llm_manager.current_provider.title()}")
            st.markdown(f"- **Velocidade:** {current_info['speed'].title()}")
            st.markdown(f"- **Custo:** {current_info['cost'].title()}")
        
        # Seletor de modelo com expander
        with st.sidebar.expander("🤖 Seletor de Modelo", expanded=False):
            available_models = llm_manager.list_available_models(llm_manager.current_provider)
            current_model = llm_manager.get_current_model(llm_manager.current_provider)
            
            if available_models:
                # Cria o mapeamento para modelos
                model_names = {
                    "llama3-70b-8192": "🦙 Llama 3 70B (Recomendado)",
                    "llama3-8b-8192": "🦙 Llama 3 8B (Rápido)"
                }
                
                # Opções para o selectbox
                model_options = [model_names.get(m, m) for m in available_models]
                
                # Encontrar índice atual
                try:
                    current_index = available_models.index(current_model)
                except ValueError:
                    current_index = 0
                
                # Selectbox para escolher modelo
                selected_display = st.selectbox(
                    "Escolha o modelo:",
                    model_options,
                    index=current_index,
                    help="Diferentes modelos têm características distintas: velocidade vs qualidade vs contexto.",
                    key="model_selector"
                )
                
                # Converte de volta para nome interno
                selected_model = None
                for internal_name, display_name in model_names.items():
                    if display_name == selected_display:
                        selected_model = internal_name
                        break
                
                # Troca o modelo se necessário
                if selected_model and selected_model != current_model:
                    if llm_manager.switch_model(llm_manager.current_provider, selected_model):
                        
                        # Preserva o histórico ao trocar o modelo
                        msg_count = preserve_chatbot_state()
                
                # Informações do modelo atual
                st.markdown("**📋 Modelo Atual:**")
                st.markdown(f"- **Nome:** {model_names.get(current_model, current_model)}")
                
                # Características dos modelos
                model_info = {
                    "llama3-70b-8192": {"size": "70B", "speed": "Médio", "quality": "Excelente", "context": "8K"},
                    "llama3-8b-8192": {"size": "8B", "speed": "Rápido", "quality": "Bom", "context": "8K"}
 
                }
                
                if current_model in model_info:
                    info = model_info[current_model]
                    st.markdown(f"- **Tamanho:** {info['size']}")
                    st.markdown(f"- **Velocidade:** {info['speed']}")
                    st.markdown(f"- **Qualidade:** {info['quality']}")
                    st.markdown(f"- **Contexto:** {info['context']} tokens")
            else:
                st.warning("Nenhum modelo disponível")
    
    # Configurações do chatbot
    st.sidebar.subheader("🤖 Chatbot")
    personality = st.sidebar.selectbox(
        "Personalidade:",
        ["helpful", "creative", "technical"],
        index=0,
        help="Escolha como o chatbot deve se comportar"
    )
    
    if hasattr(st.session_state, 'chatbot') and st.session_state.chatbot.personality != personality:
        # Preserva o histórico ao trocar personalidade
        msg_count = preserve_chatbot_state(personality)
    
    # Ações com o expander
    with st.sidebar.expander("🛠️ Ações", expanded=False):
        if st.button("🧹 Limpar Histórico do Chat", key="clear_chat_sidebar"):
            if hasattr(st.session_state, 'chatbot'):
                st.session_state.chatbot.clear_memory()
            st.session_state.chat_history = []
            st.success("Histórico limpo.")
            st.rerun()
        
        if st.button("🔄 Recarregar APIs", key="reload_apis_sidebar"):
            # Recria o gerenciador de LLM
            from src.llm_providers import LLMProvider
            import src.llm_providers
            src.llm_providers.llm_manager = LLMProvider()
            st.success("APIs recarregadas!")
            st.rerun()
    
    # Botão de download da conversa
    if hasattr(st.session_state, 'chatbot') and st.session_state.chatbot.conversation_history:
        with st.sidebar.expander("💾 Exportar Conversa", expanded=False):
            # Prepara os dados de exportação
            export_result = st.session_state.chatbot.export_conversation()
            
            if export_result.get("success", False):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Botão download JSON
                    st.download_button(
                        label="📄 JSON",
                        data=export_result["json_content"],
                        file_name=export_result["filename_json"],
                        mime="application/json",
                        help="Baixar conversa em formato JSON (estruturado)"
                    )
                
                with col2:
                    # Botão download TXT
                    st.download_button(
                        label="📝 TXT",
                        data=export_result["txt_content"],
                        file_name=export_result["filename_txt"],
                        mime="text/plain",
                        help="Baixar conversa em formato texto (legível)"
                    )
                
                # Informações adicionais
                total_msgs = export_result["export_data"]["export_info"]["total_messages"]
                st.info(f"📊 {total_msgs} mensagens prontas para download")
            else:
                st.error(export_result.get("error", "Erro desconhecido"))
    elif hasattr(st.session_state, 'chatbot'):
        st.sidebar.info("💬 Inicie uma conversa para habilitar o download")
    else:
        st.sidebar.warning("🤖 Chatbot não inicializado")
    
    # Informações do projeto
    with st.sidebar.expander("💡 Informações do Projeto"):
        st.markdown(f"""
        - LangChain
        - Groq API (gratuita)
        - Análise de Sentimentos (LLM)
        - Geração de Resumos
        - Chatbot Inteligente
        """)
    
    # Informações técnicas (expansível)
    with st.sidebar.expander("🔧 Informações Técnicas"):
        st.markdown(f"""
        - **Python:** {sys.version.split()[0]}
        - **Streamlit:** {st.__version__}
        - **API Ativa:** {llm_manager.current_provider or 'Nenhuma'}
        - **Status:** {providers.get(llm_manager.current_provider, {}).get('status', 'N/A')}
        """)
    
    if llm_manager.is_any_provider_available():
        st.sidebar.success("**Sistema ativo:** Todas as funcionalidades disponíveis.")
    else:
        st.sidebar.error("**Sistema inativo:** Configure uma API para usar.")

    # Setup de APIs
    if not llm_manager.is_any_provider_available():
        st.sidebar.subheader("Setup Necessário")
        st.sidebar.error("⚠️ Configure uma API para usar o sistema!")
        st.sidebar.markdown("""
        **Configurar Groq (Gratuito):**
        ```bash
        python setup_env.py
        ```
        
        **Ou manualmente:**
        1. Acesse [console.groq.com](https://console.groq.com/)
        2. Crie uma conta gratuita
        3. Gere uma API key
        4. Crie arquivo `.env` com:
        ```
        GROQ_API_KEY=sua_chave_aqui
        ```
        """)

