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
        new_personality: Nova personalidade (opcional, mantém a atual se None)
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


