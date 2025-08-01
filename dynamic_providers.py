"""
Sistema de IA Generativa Multi-Funcional - Para versão Cloud
Interface principal com configuração dinâmica de providers e via web
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
import importlib

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração da página
st.set_page_config(
    page_title="IA Generativa Multi-Funcional",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DynamicProvider:
    """Provider genérico configurável via interface web"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.status = "available" if self._validate_config() else "unavailable"
    
    def _validate_config(self) -> bool:
        """Valida se a configuração está completa"""
        required_fields = ["api_key", "base_url", "model"]
        return all(field in self.config and self.config[field] for field in required_fields)
    
    def generate_response(self, message: str) -> str:
        """Gera resposta usando o provider configurado"""
        try:
            # Para OpenAI-compatible APIs
            if self.config.get("type") == "openai_compatible":
                return self._generate_openai_compatible(message)
            # Para Anthropic
            elif self.config.get("type") == "anthropic":
                return self._generate_anthropic(message)
            # Para outros tipos
            else:
                return f"🤖 Provider {self.name} configurado. Mensagem: '{message}'"
        except Exception as e:
            return f"❌ Erro no provider {self.name}: {str(e)}"
    
    def _generate_openai_compatible(self, message: str) -> str:
        """Gera resposta para APIs compatíveis com OpenAI"""
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.config["model"],
                "messages": [{"role": "user", "content": message}],
                "max_tokens": self.config.get("max_tokens", 1000),
                "temperature": self.config.get("temperature", 0.7)
            }
            
            response = requests.post(
                f"{self.config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ Erro na API: {response.status_code} - {response.text}"
                
        except ImportError:
            return "❌ Biblioteca 'requests' não instalada. Execute: pip install requests"
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    def _generate_anthropic(self, message: str) -> str:
        """Gera resposta para API Anthropic"""
        try:
            import requests
            
            headers = {
                "x-api-key": self.config['api_key'],
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.config["model"],
                "max_tokens": self.config.get("max_tokens", 1000),
                "messages": [{"role": "user", "content": message}]
            }
            
            response = requests.post(
                f"{self.config['base_url']}/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                return f"❌ Erro na API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    def is_available(self) -> bool:
        return self.status == "available"
    
    def get_name(self) -> str:
        return self.name
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "status": self.status,
            "type": self.config.get("type", "custom"),
            "model": self.config.get("model", "unknown"),
            "configured_by": "user"
        }

class ProviderManager:
    """Gerenciador de providers dinâmicos"""
    
    def __init__(self):
        self.providers = {}
        self.current_provider = None
        self._load_builtin_providers()
        self._load_user_providers()
    
    def _load_builtin_providers(self):
        """Carrega providers built-in (Groq)"""
        groq_key = os.getenv("GROQ_API_KEY") or st.session_state.get("groq_key")
        
        if groq_key:
            self.providers["groq"] = DynamicProvider("groq", {
                "type": "groq",
                "api_key": groq_key,
                "base_url": "https://api.groq.com/openai/v1",
                "model": "llama3-70b-8192"
            })
            if not self.current_provider:
                self.current_provider = self.providers["groq"]
    
    def _load_user_providers(self):
        """Carrega providers configurados pelo usuário"""
        if 'user_providers' in st.session_state:
            for name, config in st.session_state.user_providers.items():
                self.providers[name] = DynamicProvider(name, config)
    
    def add_provider(self, name: str, config: Dict[str, Any]) -> bool:
        """Adiciona um novo provider"""
        try:
            provider = DynamicProvider(name, config)
            self.providers[name] = provider
            
            # Salvar na sessão
            if 'user_providers' not in st.session_state:
                st.session_state.user_providers = {}
            st.session_state.user_providers[name] = config
            
            return True
        except Exception as e:
            st.error(f"Erro ao adicionar provider: {e}")
            return False
    
    def get_available_providers(self) -> List[str]:
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def get_current_provider(self) -> Optional[DynamicProvider]:
        return self.current_provider
    
    def switch_provider(self, name: str) -> bool:
        if name in self.providers and self.providers[name].is_available():
            self.current_provider = self.providers[name]
            return True
        return False

def setup_api_keys():
    """Configurar chaves API via interface ou ambiente"""
    
    # Verificar se há chave no ambiente (para deploy)
    groq_key = os.getenv("GROQ_API_KEY")
    
    # Verificar se usuário já configurou na sessão
    if 'groq_key' in st.session_state:
        groq_key = st.session_state.groq_key
        os.environ["GROQ_API_KEY"] = groq_key
    
    # Interface para configurar providers
    show_provider_configuration()
    
    # Retorna True se há pelo menos um provider disponível
    provider_manager = ProviderManager()
    return len(provider_manager.get_available_providers()) > 0

def show_provider_configuration():
    """Interface para configurar providers"""
    
    with st.sidebar.expander("🔧 Configurar Providers", expanded=False):
        
        # Aba para Groq (built-in)
        st.markdown("### 🚀 Groq (Built-in)")
        
        groq_key = st.text_input(
            "Chave Groq:",
            type="password",
            placeholder="gsk_...",
            help="API gratuita - console.groq.com",
            key="groq_api_key"
        )
        
        if groq_key and groq_key.startswith("gsk_"):
            st.session_state.groq_key = groq_key
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("✅ Groq configurado.")
        
        st.markdown("---")
        
        # Interface para adicionar providers customizados
        st.markdown("### ➕ Adicionar Provider Customizado")
        
        provider_name = st.text_input(
            "Nome do Provider:",
            placeholder="ex: meu-openai",
            key="new_provider_name"
        )
        
        provider_type = st.selectbox(
            "Tipo de API:",
            ["openai_compatible", "anthropic", "custom"],
            help="Escolha o tipo de API",
            key="new_provider_type"
        )
        
        if provider_type == "openai_compatible":
            st.markdown("**Configuração OpenAI/Compatible:**")
            
            api_key = st.text_input(
                "API Key:",
                type="password",
                key="new_provider_key"
            )
            
            base_url = st.text_input(
                "Base URL:",
                value="https://api.openai.com/v1",
                help="URL base da API",
                key="new_provider_url"
            )
            
            model = st.text_input(
                "Modelo:",
                value="gpt-3.5-turbo",
                help="Nome do modelo",
                key="new_provider_model"
            )
            
        elif provider_type == "anthropic":
            st.markdown("**Configuração Anthropic:**")
            
            api_key = st.text_input(
                "API Key:",
                type="password",
                placeholder="sk-ant-...",
                key="new_provider_key"
            )
            
            base_url = st.text_input(
                "Base URL:",
                value="https://api.anthropic.com/v1",
                key="new_provider_url"
            )
            
            model = st.text_input(
                "Modelo:",
                value="claude-3-haiku-20240307",
                key="new_provider_model"
            )
        
        else:  # custom
            st.markdown("**Configuração Customizada:**")
            api_key = st.text_input("API Key:", type="password", key="new_provider_key")
            base_url = st.text_input("Base URL:", key="new_provider_url")
            model = st.text_input("Modelo:", key="new_provider_model")
        
        # Configurações avançadas
        with st.expander("⚙️ Configurações Avançadas"):
            temperature = st.slider("Temperature:", 0.0, 2.0, 0.7, key="new_provider_temp")
            max_tokens = st.number_input("Max Tokens:", 1, 4000, 1000, key="new_provider_tokens")
        
        # Botão para adicionar
        if st.button("➕ Adicionar Provider", key="add_provider_btn"):
            if provider_name and api_key and base_url and model:
                config = {
                    "type": provider_type,
                    "api_key": api_key,
                    "base_url": base_url,
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                provider_manager = ProviderManager()
                if provider_manager.add_provider(provider_name, config):
                    st.success(f"✅ Provider '{provider_name}' adicionado.")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar provider")
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

def show_provider_status():
    """Mostra status dos providers configurados"""
    provider_manager = ProviderManager()
    available_providers = provider_manager.get_available_providers()
    
    if available_providers:
        st.sidebar.success(f"✅ {len(available_providers)} provider(s) configurado(s)")
        
        # Seletor de provider ativo
        current_provider = provider_manager.get_current_provider()
        current_name = current_provider.get_name() if current_provider else available_providers[0]
        
        selected_provider = st.sidebar.selectbox(
            "Provider Ativo:",
            available_providers,
            index=available_providers.index(current_name) if current_name in available_providers else 0,
            key="active_provider"
        )
        
        if selected_provider != current_name:
            provider_manager.switch_provider(selected_provider)
            st.rerun()
        
        # Mostrar informações do provider ativo
        with st.sidebar.expander("ℹ️ Info do Provider Ativo"):
            provider_info = provider_manager.get_current_provider().get_info()
            for key, value in provider_info.items():
                st.markdown(f"- **{key.title()}**: {value}")
    
    else:
        st.sidebar.warning("⚠️ Configure pelo menos um provider")

def main():
    """Função principal"""
    
    # CSS customizado
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
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho
    st.markdown('<h1 class="main-header">Sistema de IA Multi-Funcional - Avançado</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Configure <strong>qualquer provider</strong> via interface web
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configurar providers
    has_providers = setup_api_keys()
    
    # Mostrar status na sidebar
    show_provider_status()
    
    # Interface principal
    if not has_providers:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Configure Providers via Interface Web!</h3>
            <p>Este sistema permite configurar qualquer provider de IA através da interface web.</p>
            
            <h4>🔧 Providers Suportados:</h4>
            <ul>
                <li><strong>🚀 Groq</strong> - API gratuita (built-in)</li>
                <li><strong>🤖 OpenAI</strong> - GPT-3.5, GPT-4, etc.</li>
                <li><strong>🧠 Anthropic</strong> - Claude Haiku, Sonnet, Opus</li>
                <li><strong>🔧 APIs Customizadas</strong> - Qualquer API compatível</li>
            </ul>
            
            <p><strong>👈 Use a sidebar para configurar seus providers!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Interface completa com providers configurados
        show_full_interface()

def show_full_interface():
    """Interface completa quando há providers configurados"""
    
    # Abas principais
    tab1, tab2, tab3 = st.tabs(["🤖 Chatbot", "😊 Análise de Sentimentos", "📝 Resumos"])
    
    with tab1:
        chatbot_interface()
    
    with tab2:
        sentiment_interface()
    
    with tab3:
        summarizer_interface()

def chatbot_interface():
    """Interface do chatbot com providers dinâmicos"""
    st.header("🤖 Chatbot Inteligente")
    
    provider_manager = ProviderManager()
    current_provider = provider_manager.get_current_provider()
    
    if current_provider:
        st.info(f"🔗 Usando: **{current_provider.get_name()}** - {current_provider.get_info()['model']}")
    
    # Área de chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gerar resposta
        try:
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    if current_provider:
                        response = current_provider.generate_response(prompt)
                    else:
                        response = "❌ Nenhum provider configurado"
                    
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")

def sentiment_interface():
    """Interface de análise de sentimentos"""
    st.header("😊 Análise de Sentimentos")
    st.info("🔗 Usando o provider ativo para análise contextual")
    
    text_input = st.text_area(
        "Digite o texto para análise:",
        placeholder="Digite aqui um texto para analisar o sentimento...",
        height=150
    )
    
    if st.button("🔍 Analisar", type="primary"):
        if text_input:
            provider_manager = ProviderManager()
            current_provider = provider_manager.get_current_provider()
            
            if current_provider:
                with st.spinner("Analisando sentimentos..."):
                    prompt = f"Analise o sentimento do seguinte texto e responda apenas com: POSITIVO, NEGATIVO ou NEUTRO, seguido de uma breve explicação:\n\n{text_input}"
                    response = current_provider.generate_response(prompt)
                    
                    # Extrair sentimento da resposta
                    sentiment = "Indefinido"
                    if "POSITIVO" in response.upper():
                        sentiment = "😊 Positivo"
                    elif "NEGATIVO" in response.upper():
                        sentiment = "😞 Negativo"
                    elif "NEUTRO" in response.upper():
                        sentiment = "😐 Neutro"
                    
                    st.success(f"**Sentimento**: {sentiment}")
                    st.info(f"**Análise**: {response}")
            else:
                st.error("❌ Configure um provider primeiro")

def summarizer_interface():
    """Interface do gerador de resumos"""
    st.header("📝 Gerador de Resumos")
    st.info("🔗 Usando o provider ativo para geração de resumos")
    
    text_input = st.text_area(
        "Digite o texto para resumir:",
        placeholder="Cole aqui um texto longo que você gostaria de resumir...",
        height=200
    )
    
    summary_type = st.selectbox(
        "🎯 Tipo de Resumo:",
        ["informativo", "executivo", "criativo", "técnico"]
    )
    
    if st.button("📋 Resumir", type="primary"):
        if text_input:
            provider_manager = ProviderManager()
            current_provider = provider_manager.get_current_provider()
            
            if current_provider:
                with st.spinner("Gerando resumo..."):
                    prompt = f"Faça um resumo {summary_type} do seguinte texto:\n\n{text_input}"
                    response = current_provider.generate_response(prompt)
                    
                    st.success("✅ Resumo gerado!")
                    st.markdown(f"**{response}**")
            else:
                st.error("❌ Configure um provider primeiro")

if __name__ == "__main__":
    main() 