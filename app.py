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

def chatbot_tab():
    """Interface do chatbot."""
    st.header("💬 Chatbot Inteligente")
    
    # Verifica se algum provedor está disponível
    if not llm_manager.is_any_provider_available():
        st.error("❌ **Nenhuma API configurada**")
        st.warning("Configure uma API para usar o chatbot. Execute: `python setup_env.py`")
        st.info("🔗 APIs suportadas: Groq (gratuita)")
        return
    
    # Informações do sistema
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        personality = st.session_state.chatbot.personality if hasattr(st.session_state, 'chatbot') else "helpful"
        st.info(f"🎭 Personalidade atual: **{personality.title()}**")
    
    with col2:
        # Indica o provedor ativo
        provider_icons = {
            "groq": "🚀"
            # Espaço para outros provedores no futuro
        }
        icon = provider_icons.get(llm_manager.current_provider, "❓")
        st.success(f"{icon} **{llm_manager.current_provider.title() if llm_manager.current_provider else 'N/A'}**")
    
    with col3:
        stats = st.session_state.chatbot.get_stats() if hasattr(st.session_state, 'chatbot') else {"messages": 0}
        st.metric("Mensagens", stats.get("messages", 0))
    
    # Interface de chat
    chat_container = st.container()
    
    # Exibe o histórico
    with chat_container:
        for i, msg in enumerate(st.session_state.chat_history):
            # Mensagem do usuário
            st.markdown(f"""
            <div style="background: #2d3748; color: #ffffff; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #4299e1;">
                <strong>👤 Você ({msg['timestamp']}):</strong><br>
                {msg['user']}
            </div>
            """, unsafe_allow_html=True)
            
            # Resposta do bot
            provider_icon = provider_icons.get(msg.get('provider', 'unknown'), "❓")
            provider_name = msg.get('provider', 'unknown').title()
            st.markdown(f"""
            <div style="background: #4a5568; color: #ffffff; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #9f7aea;">
                <strong>{provider_icon} {provider_name} Assistant:</strong><br>
                {msg['bot']}
            </div>
            """, unsafe_allow_html=True)
    
    # Inicializa a variável de controle se não existir
    if 'chatbot_example_text' not in st.session_state:
        st.session_state.chatbot_example_text = ""
    
    # Controles de entrada
    # Caixa de texto principal (largura total)
    user_input = st.text_area(
        "Digite sua mensagem:",
        value=st.session_state.chatbot_example_text,
        placeholder="Faça uma pergunta ou inicie uma conversa...",
        height=100,
        key=f"chat_input_{len(st.session_state.chat_history)}"
    )

    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.3])
    
    with col1:
        send_button = st.button("📤 Enviar", type="primary", key=f"send_btn_{len(st.session_state.chat_history)}")
    
    with col2:
        if st.button("🧹 Limpar", key=f"clear_btn_{len(st.session_state.chat_history)}"):
            st.session_state.chatbot.clear_memory()
            st.session_state.chat_history = []
            st.session_state.chatbot_example_text = ""  # Limpa também o campo de exemplo
            st.success("Histórico limpo!")
            st.rerun()
    
    with col3:
        # Botão de exemplo
        if st.button("🎲 Exemplo", key=f"example_btn_{len(st.session_state.chat_history)}"):
            examples = [
                "Olá! Como você funciona?",
                "Explique o que é inteligência artificial",
                "Conte uma história criativa sobre robôs",
                "Quais são as melhores práticas de programação em Python?",
                "Compare os prós e contras da IA",
                "Como funciona o machine learning?"
            ]
            import random
            st.session_state.chatbot_example_text = random.choice(examples)
            st.rerun()
    
    with col4:
        # Botão HTML
        st.html("""
        <a href="#page-top" style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.25rem 0.75rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 0.5rem;
            text-align: center;
            font-weight: 400;
            font-size: 0.875rem;
            line-height: 1.6;
            height: 2.5rem;
            min-height: 2.5rem;
            box-sizing: border-box;
            cursor: pointer;
            border: 1px solid transparent;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 0;
            white-space: nowrap;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'" 
           onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='none'"
           onmousedown="this.style.transform='translateY(0px)'">
            ⬆️ Voltar ao Topo
        </a>
        """)
    
    # Processa a mensagem quando botão for clicado
    if send_button and user_input:
        current_provider = llm_manager.current_provider or "Sistema"
        with st.spinner(f"🤔 {current_provider.title()} está pensando..."):
            # Valida a entrada
            validation = validate_text_input(user_input, min_length=1, max_length=1000)
            
            if validation["valid"]:
                # Obtém a resposta do chatbot
                response = st.session_state.chatbot.chat(user_input)
                
                # Verifica se houve erro na resposta
                if response.startswith("❌"):
                    st.error(response)
                    return
                
                # Adiciona ao histórico da sessão
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    "timestamp": timestamp,
                    "user": user_input,
                    "bot": response,
                    "provider": llm_manager.current_provider or "unknown"
                })
                
                # Limpa o campo após enviar
                st.session_state.chatbot_example_text = ""
                
                st.rerun()
            else:
                st.error(validation["error"])

def sentiment_tab():
    """Interface de análise de sentimentos."""
    st.header("😀 Análise de Sentimentos")
    
    # Verifica se algum provedor está disponível
    if not llm_manager.is_any_provider_available():
        st.error("❌ **Nenhuma API configurada**")
        st.warning("Configure uma API para usar a análise de sentimentos. Execute: `python setup_env.py`")
        st.info("🔗 APIs suportadas: Groq (gratuita)")
        return
    
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Análise Inteligente com LLM</h4>
        <p>Utiliza <strong>LLM avançado</strong> para análise contextual e precisa de sentimentos com alta qualidade.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializa a variável de controle se não existir
    if 'sentiment_example_text' not in st.session_state:
        st.session_state.sentiment_example_text = ""
    
    # Input de texto
    text_input = st.text_area(
        "📝 Digite o texto para análise:",
        value=st.session_state.sentiment_example_text,
        placeholder="Exemplo: Estou muito feliz com os resultados do projeto!",
        height=150,
        key="sentiment_text_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        analyze_button = st.button("🔍 Analisar", type="primary", key="sentiment_analyze_btn")
    
    with col2:
        if st.button("📝 Exemplo", key="sentiment_example_btn"):
            examples = [
                "Estou muito feliz com os resultados do projeto! A equipe trabalhou de forma excepcional.",
                "Infelizmente, o sistema apresentou vários bugs e falhas críticas.",
                "O produto tem características interessantes, mas ainda precisa de melhorias.",
                "A apresentação foi absolutamente incrível! Superou todas as expectativas."
            ]
            import random
            st.session_state.sentiment_example_text = random.choice(examples)
            st.rerun()
    
    # Processa a análise
    if analyze_button and text_input:
        validation = validate_text_input(text_input)
        
        if validation["valid"]:
            text = validation["text"]
            
            with st.spinner("🧠 Analisando sentimentos do texto..."):
                # Análise completa
                results = sentiment_analyzer.analyze_comprehensive(text)
                
                # Estatísticas do texto
                stats = calculate_text_stats(text)
                
            # Exibe os resultados
            st.subheader("📈 Resultados da Análise")
            
            # Consenso geral (apenas um método por enquanto)
            consensus = results["consensus"]
            emoji = get_emoji_for_sentiment(consensus["sentiment"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{emoji}</h3>
                    <h4>{consensus['sentiment'].title()}</h4>
                    <p>Sentimento</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{consensus['confidence']:.1%}</h4>
                    <p>Confiança</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Resultados mais detalhados
            st.subheader("🔬 Análise Detalhada")
            
            for method, result in results["individual_results"].items():
                if "error" not in result:
                    with st.expander(f" {method.upper()} - {result['sentiment'].title()} ({result.get('confidence', 0):.1%})"):
                        st.json(result)
            
            # Estatísticas do texto
            st.subheader("📝 Estatísticas do Texto")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Palavras", stats["words"])
            with col2:
                st.metric("Frases", stats["sentences"])
            with col3:
                st.metric("Caracteres", stats["characters"])
            with col4:
                st.metric("Palavras/Frase", stats["avg_words_per_sentence"])
            
        else:
            st.error(validation["error"])



