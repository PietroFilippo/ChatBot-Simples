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
from src.llm_providers import provider_registry
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
    available_providers_dict = provider_registry.get_available_providers()
    available_providers = list(available_providers_dict.keys())  # Convert to list of names
    all_providers = provider_registry.get_all_providers_info()
    
    if available_providers:
        # Criação do mapeamento
        provider_names = {
            "groq": "🚀 Groq"
        }
        
        # Opções do selectbox
        options = [provider_names.get(p, p.title()) for p in available_providers]
        current_provider = provider_registry.get_current_provider()
        current_index = available_providers.index(current_provider.get_name()) if current_provider and current_provider.get_name() in available_providers else 0
        
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
        if selected_provider and selected_provider != current_provider.get_name():
            if provider_registry.switch_provider(selected_provider):
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
    with st.sidebar.expander("📊 Status das APIs", expanded=False):
        for name, info in all_providers.items():
            provider = provider_registry.get_provider(name)
            status_emoji = "✅" if provider.is_available() else "❌"
            speed_info = f"({info['speed']}, {info['cost']})"
            
            if provider == current_provider:
                st.success(f"{status_emoji} **{name.title()}** {speed_info} - ATIVO")
            elif provider.is_available():
                st.info(f"{status_emoji} {name.title()} {speed_info}")
            else:
                st.error(f"{status_emoji} {name.title()} {speed_info} - Não configurado")
    
    # Informações detalhadas do provedor ativo
    current_provider = provider_registry.get_current_provider()
    if current_provider:
        current_info = all_providers[current_provider.get_name()]
        
        # API Ativa
        with st.sidebar.expander("🎯 API Ativa"):
            st.markdown(f"- **Nome:** {current_provider.get_name().title()}")
            st.markdown(f"- **Velocidade:** {current_info['speed'].title()}")
            st.markdown(f"- **Custo:** {current_info['cost'].title()}")
        
        # Seletor de modelo
        with st.sidebar.expander("🤖 Seletor de Modelo", expanded=False):
            available_models = current_provider.get_available_models()
            current_model = current_provider.get_current_model()
            
            if available_models:
                # Cria o mapeamento para modelos
                model_names = {
                    "llama3-70b-8192": "🦙 Llama 3 70B",
                    "llama3-8b-8192": "🦙 Llama 3 8B"
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
                    if current_provider.switch_model(selected_model):
                        
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
        - **API Ativa:** {current_provider.get_name() if current_provider else 'Nenhuma'}
        - **Status:** {current_provider.is_available() if current_provider else 'N/A'}
        """)

    # Setup de APIs
    if not provider_registry.is_any_provider_available():
        st.sidebar.subheader("Setup Necessário")
        st.sidebar.error("⚠️ Configure uma API para usar o sistema.")
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
    if not provider_registry.is_any_provider_available():
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
        current_provider = provider_registry.get_current_provider()
        icon = provider_icons.get(current_provider.get_name(), "❓")
        st.success(f"{icon} **{current_provider.get_name().title() if current_provider else 'N/A'}**")
    
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
        current_provider = provider_registry.get_current_provider()
        with st.spinner(f"🤔 {current_provider.get_name().title()} está pensando..."):
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
                    "provider": current_provider.get_name()
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
    if not provider_registry.is_any_provider_available():
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

def summarizer_tab():
    """Interface do gerador de resumos."""
    st.header("📝 Gerador de Resumos")
    
    # Verificar se algum provedor está disponível
    if not provider_registry.is_any_provider_available():
        st.error("❌ **Nenhuma API configurada**")
        st.warning("Configure uma API para usar o gerador de resumos. Execute: `python setup_env.py`")
        st.info("🔗 APIs suportadas: Groq (gratuita)")
        return
    
    st.markdown("""
    <div class="feature-card">
        <h4>⚡ Sumarização Inteligente</h4>
        <p>Múltiplas estratégias: <strong>Extrativa</strong> e <strong>LangChain</strong> com diferentes estilos e níveis de detalhe.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar variável de controle se não existir
    if 'summarizer_example_text' not in st.session_state:
        st.session_state.summarizer_example_text = ""
    
    # Input de texto
    text_input = st.text_area(
        "📄 Digite o texto para resumir:",
        value=st.session_state.summarizer_example_text,
        placeholder="Cole aqui um texto longo que você gostaria de resumir...",
        height=200,
        key="summarizer_text_input"
    )
    
    # Configurações
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
    
    with col3:
        # Placeholder para manter o layout
        st.write("")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        summarize_button = st.button("📋 Resumir", type="primary", key="summarizer_btn")
    
    with col2:
        if st.button("📰 Exemplo", key="summarizer_example_btn"):
            example_text = """A inteligência artificial (IA) é uma das tecnologias mais revolucionárias do século XXI, transformando drasticamente a forma como vivemos, trabalhamos e interagimos com o mundo. Desde sistemas de recomendação em plataformas de streaming até carros autônomos, a IA está presente em inúmeras aplicações do nosso cotidiano.

Os modelos de linguagem de grande escala, como GPT e BERT, representam um marco significativo no processamento de linguagem natural. Estes modelos são capazes de compreender contexto, gerar texto coerente e realizar tarefas complexas de compreensão textual. A arquitetura transformer, introduzida em 2017, revolucionou o campo e se tornou a base para a maioria dos modelos de IA generativa atuais.

No entanto, o desenvolvimento da IA também traz desafios importantes. Questões éticas, como viés algorítmico, privacidade de dados e o impacto no mercado de trabalho, precisam ser cuidadosamente consideradas. É essencial desenvolver IA de forma responsável, garantindo que os benefícios sejam amplamente distribuídos e os riscos minimizados.

O futuro da IA promete ainda mais avanços, com pesquisas em andamento sobre IA geral artificial, computação quântica aplicada à IA e sistemas multimodais que podem processar texto, imagem e áudio simultaneamente. Estas inovações têm o potencial de resolver problemas complexos em áreas como medicina, mudanças climáticas e educação."""
            
            st.session_state.summarizer_example_text = example_text
            st.rerun()
    
    # Processar sumarização
    if summarize_button and text_input:
        validation = validate_text_input(text_input, min_length=100)
        
        if validation["valid"]:
            text = validation["text"]
            
            with st.spinner("📝 Gerando resumos..."):
                # Sumarização completa
                results = summarizer.summarize_comprehensive(
                    text,
                    num_sentences=max_sentences,
                    summary_type=summary_type
                )
            
            # Exibir resultados
            st.subheader("📄 Resumos Gerados")
            
            # Estatísticas gerais
            stats = results["statistics"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Métodos", stats["successful_methods"])
            with col2:
                st.metric("Compressão Média", f"{stats['average_compression']:.1%}")
            with col3:
                st.metric("Texto Original", f"{results['original_length']} chars")
            with col4:
                st.metric("Melhor Método", stats["best_method"])
            
            # Resumos individuais
            for method, result in results["summaries"].items():
                if "error" not in result:
                    compression = result.get("compression_ratio", 0)
                    
                    with st.expander(f"{method.upper()} - Compressão: {compression:.1%}"):
                        st.markdown(f"**Resumo:**")
                        st.markdown(result["summary"])
                        
                        if "details" in result:
                            st.markdown("**Detalhes Técnicos:**")
                            st.json(result["details"])
            
        else:
            st.error(validation["error"])

def analytics_tab():
    """Interface de analytics e métricas."""
    st.header("📊 Analytics e Métricas")
    
    # Nova seção: Sistema de Provedores Extensível
    st.subheader("🔧 Sistema de Provedores LLM")
    
    # Informações sobre todos os provedores registrados
    all_providers = provider_registry.get_all_providers_info()
    available_providers = provider_registry.get_available_providers()
    current_provider = provider_registry.get_current_provider()
    
    # Métricas de provedores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Provedores Registrados", len(all_providers))
    with col2:
        st.metric("Provedores Disponíveis", len(available_providers))
    with col3:
        current_name = current_provider.get_name() if current_provider else "Nenhum"
        st.metric("Provedor Ativo", current_name.title())
    
    # Lista de provedores com detalhes
    st.markdown("### 🎯 Provedores Registrados")
    
    for name, info in all_providers.items():
        provider = provider_registry.get_provider(name)
        is_active = current_provider and current_provider.get_name() == name
        is_available = provider.is_available()
        
        # Ícone baseado no status
        if is_active and is_available:
            icon = "🟢"
            status_text = "ATIVO"
        elif is_available:
            icon = "🔵"
            status_text = "DISPONÍVEL"
        else:
            icon = "🔴"
            status_text = "INDISPONÍVEL"
        
        with st.expander(f"{icon} {name.upper()} - {status_text}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Informações Básicas:**")
                st.markdown(f"• **Descrição:** {info.get('description', 'N/A')}")
                st.markdown(f"• **Velocidade:** {info.get('speed', 'N/A')}")
                st.markdown(f"• **Custo:** {info.get('cost', 'N/A')}")
                st.markdown(f"• **Modelo Atual:** {info.get('current_model', 'N/A')}")
                
                # Botão para trocar provedor (se disponível)
                if is_available and not is_active:
                    if st.button(f"🔄 Trocar para {name.title()}", key=f"switch_{name}"):
                        if provider_registry.switch_provider(name):
                            st.success(f"✅ Trocado para {name.title()}!")
                            st.rerun()
                        else:
                            st.error(f"❌ Erro ao trocar para {name.title()}")
            
            with col2:
                st.markdown("**Estatísticas de Performance:**")
                stats = provider.get_performance_stats()
                for key, value in stats.items():
                    display_key = key.replace("_", " ").title()
                    st.markdown(f"• **{display_key}:** {value}")
                
                # Vantagens
                if "advantages" in info:
                    st.markdown("**Vantagens:**")
                    for advantage in info["advantages"]:
                        st.markdown(f"• {advantage}")
    
    # Separador visual
    st.divider()
    
    # Métricas dos analisadores (seção existente)
    st.subheader("⚙️ Capacidades dos Analisadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**😀 Análise de Sentimentos**")
        sentiment_methods = sentiment_analyzer.get_available_methods()
        
        for method, info in sentiment_methods.items():
            if info.get("available", False):
                st.success(f"✅ {method.upper()} - {info.get('speed', 'N/A')} / {info.get('accuracy', 'N/A')}")
            else:
                st.error(f"❌ {method.upper()} - Indisponível")
    
    with col2:
        st.markdown("**📝 Geração de Resumos**")
        summarizer_methods = summarizer.get_available_methods()
        
        for method, info in summarizer_methods.items():
            if info.get("available", False):
                st.success(f"✅ {method.title()} - {info.get('speed', 'N/A')} / {info.get('quality', 'N/A')}")
            else:
                st.error(f"❌ {method.title()} - Indisponível")
    
    # Estatísticas da sessão
    st.subheader("📈 Estatísticas da Sessão")
    
    if hasattr(st.session_state, 'chatbot'):
        chatbot_stats = st.session_state.chatbot.get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Mensagens do Chat", chatbot_stats.get("messages", 0))
        with col2:
            st.metric("Tamanho Médio (User)", f"{chatbot_stats.get('avg_user_length', 0):.0f}")
        with col3:
            st.metric("Tamanho Médio (Bot)", f"{chatbot_stats.get('avg_bot_length', 0):.0f}")
        with col4:
            st.metric("Personalidade", chatbot_stats.get("personality", "N/A").title())
    
    # Modelos disponíveis do provedor atual
    if current_provider and current_provider.is_available():
        st.subheader("🤖 Modelos Disponíveis (Provedor Atual)")
        
        models = current_provider.get_available_models()
        current_model = current_provider.get_current_model()
        
        for model in models:
            if model == current_model:
                st.success(f"✅ **{model}** - ATIVO (Modelo atual)")
            else:
                st.info(f"🔄 {model} - Disponível")
    
    # Informações do sistema
    st.subheader("💻 Informações do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🐍 Python & Dependências:**")
        groq_provider = provider_registry.get_provider("groq")
        groq_status = "Configurado" if groq_provider and groq_provider.is_available() else "Não configurado"
        
        st.code(f"""
Python: {sys.version.split()[0]}
Streamlit: {st.__version__}
LangChain: Instalado
Groq: {groq_status}
        """)
    
    with col2:
        st.markdown("**📊 Status dos Componentes:**")
        groq_provider = provider_registry.get_provider("groq")
        groq_available = groq_provider and groq_provider.is_available()
        
        components_status = {
            "Groq API": "✅ Ativo" if groq_available else "❌ Inativo",
            "Análise Sentimentos": "✅ Ativo" if sentiment_analyzer.get_available_methods().get("llm", {}).get("available") else "❌ Inativo",
            "Resumos": "✅ Ativo" if summarizer.get_available_methods().get("langchain", {}).get("available") else "❌ Inativo",
            "Chatbot": "✅ Ativo" if provider_registry.is_any_provider_available() else "❌ Inativo"
        }
        
        for component, status in components_status.items():
            st.markdown(f"- **{component}:** {status}")

def main():
    """Função principal da aplicação."""
    # Inicializa o estado da sessão
    initialize_session_state()
    
    # Mostra o cabeçalho
    show_header()
    
    # Configura o sidebar
    show_sidebar()
    
    # Cria as abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chatbot", 
        "📊 Sentimentos", 
        "📝 Resumos", 
        "📈 Analytics"
    ])
    
    with tab1:
        chatbot_tab()
    
    with tab2:
        sentiment_tab()
    
    with tab3:
        summarizer_tab()
    
    with tab4:
        analytics_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🤖 <strong>Sistema de IA Generativa Multi-Funcional</strong></p>
        <p><em>Tecnologias: Python • LangChain • Streamlit • Groq • NLTK</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 

