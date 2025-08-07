"""
Constantes centralizadas para eliminar strings hardcoded e magic numbers.
"""

from typing import Dict

# Mensagens de erro padronizadas
ERROR_MESSAGES = {
    "no_provider": "**Nenhuma API configurada**",
    "invalid_text": "Por favor, insira um texto válido",
    "text_too_short": "Texto deve ter pelo menos {min_length} caracteres",
    "processing": "Processando.",
    "api_error": "Erro na API {provider}: {error}",
    "timeout": "Timeout na requisição. Tente novamente.",
    "model_unavailable": "Modelo '{model}' não disponível para {provider}",
    "provider_unavailable": "Provedor {provider} não disponível. Verifique a configuração.",
    "NO_PROVIDERS": "Nenhuma API registrada",
    "SETUP_REQUIRED": "Configure uma API para usar o sistema.",
    "UNKNOWN_ERROR": "Erro desconhecido",
}

# Mensagens de sucesso
SUCCESS_MESSAGES = {
    "provider_configured": "{provider} configurado com sucesso",
    "model_switched": "Modelo alterado para: {model}",
    "analysis_complete": "Análise concluída",
    "history_preserved": "Histórico preservado: {count} mensagens",
    "HISTORY_CLEARED": "Histórico limpo.",
    "APIS_RELOADED": "APIs recarregadas.",
}

# Mensagens da interface do usuário
UI_MESSAGES = {
    "PAGE_TITLE": "IA Generativa Multi-Funcional",
    "MAIN_HEADER": "Sistema de IA Generativa Multi-Funcional",
    "SUBTITLE": "Utilização de <strong>LangChain</strong>, <strong>LLMs gratuitos</strong> e <strong>fluxos de IA</strong>",
    "PROVIDER_HELP": """Selecione o provedor de LLM.
Para configurar outras APIs de maneira local com suas chaves, baixe o repositório do projeto e siga as instruções.""",
    "SETUP_INSTRUCTIONS": {
        "huggingface": """
        **Para configurar Hugging Face:**
        1. Execute: `python setup_env.py`
        2. Configure sua chave quando solicitado
        3. Obtenha grátis em: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        """,
        "groq": """
        **Para configurar Groq:**
        1. Execute: `python setup_env.py`
        2. Configure sua chave quando solicitado
        3. Obtenha grátis em: [console.groq.com](https://console.groq.com/)
        """
    },
    "SETUP_GUIDE": """
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
    """
}

# Nomes de display para providers
PROVIDER_NAMES = {
    "groq": "🚀 Groq",
    "huggingface": "🤗 Hugging Face",
    "openai": "🤖 OpenAI",
    "claude": "🧠 Claude",
}

# Nomes de display para modelos
MODEL_NAMES = {
    # Groq models
    "llama3-70b-8192": "🦙 Llama 3 70B",
    "llama3-8b-8192": "🦙 Llama 3 8B",
    "gemma2-9b-it": "🔷 Gemma 2 9B",
    
    # Hugging Face models
    "openai/gpt-oss-120b": "💻 GPT-OSS 120B",
    "google/gemma-2-2b-it": "🔷 Gemma 2 2B Instruct",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": "🧠 DeepSeek R1 Distill 1.5B",
    "microsoft/phi-4": "🔷 Microsoft Phi-4",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "💻 Qwen 2.5 Coder 32B",
    "deepseek-ai/DeepSeek-R1": "🧠 DeepSeek R1 (Reasoning)",
    "openai/gpt-oss-20b": "💻 GPT-OSS 20B",	
}

# Informações do sistema
SYSTEM_INFO = {
    "PROJECT_TECHNOLOGIES": """
    - LangChain
    - Groq API (gratuita)
    - Hugging Face API (gratuita)
    - Análise de Sentimentos (LLM)
    - Geração de Resumos
    - Chatbot
    """,
    "MODEL_INFO": {
        # Groq models
        "llama3-70b-8192": {"size": "70B", "speed": "Rápido", "quality": "Excelente", "context": "8K"},
        "llama3-8b-8192": {"size": "8B", "speed": "Rápido", "quality": "Bom", "context": "8K"},
        "gemma2-9b-it": {"size": "9B", "speed": "Rápido", "quality": "Bom", "context": "8K"},
        
        # Hugging Face models
        "openai/gpt-oss-120b": {"size": "120B", "speed": "Rápido", "quality": "Excelente", "context": "128K"},
        "google/gemma-2-2b-it": {"size": "2B", "speed": "Rápido", "quality": "Bom", "context": "8K"},
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": {"size": "1.5B", "speed": "Rápido", "quality": "Bom", "context": "32K"},
        "microsoft/phi-4": {"size": "14B", "speed": "Rápido", "quality": "Muito Bom", "context": "16K"},
        "Qwen/Qwen2.5-Coder-32B-Instruct": {"size": "32B", "speed": "Médio", "quality": "Excelente", "context": "32K"},
        "deepseek-ai/DeepSeek-R1": {
            "size": "236B", 
            "speed": "Lento", 
            "quality": "Excepcional", 
            "context": "128K",
            "special": "🧠 Modelo de Reasoning - Demora mais para responder pois 'pensa' antes de dar a resposta final. O output inclui o processo de raciocínio completo."
        },
        "openai/gpt-oss-20b": {
            "size": "21.5B",
            "speed": "Rápido",
            "quality": "Excelente",
            "context": "131K",
        }
    },
    "CONFIG_GUIDE": """
    Para alterar as configurações globais:
    
    1. **Execute o setup:**
    ```bash
    python setup_env.py
    ```
    
    2. **Ou edite o arquivo `.env` manualmente:**
    ```bash
    GLOBAL_TEMPERATURE=0.7      # Criatividade (0.0-1.0)
    GLOBAL_MAX_TOKENS=1000      # Tamanho máximo das respostas
    API_TIMEOUT=30              # Timeout em segundos
    AUTO_RETRY=true             # Retry automático
    MAX_RETRIES=3               # Número de tentativas
    LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
    DEBUG_MODE=false            # Modo debug
    ```
    
    3. **Execute localmente:**
    ```bash
    streamlit run app.py
    ```
    **Ou reinicie a aplicação** caso já esteja rodando para aplicar as mudanças.
    """,
    "FOOTER": """
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🤖 <strong>Sistema de IA Generativa Multi-Funcional</strong></p>
        <p><em>Tecnologias: Python • LangChain • Streamlit • Groq • NLTK</em></p>
        <p style="margin-top: 1rem;">
            <a href="https://github.com/PietroFilippo/ChatBot-Simples" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">
                Repositório no GitHub
            </a>
        </p>
    </div>
    """
}

# Textos de exemplo
EXAMPLE_TEXTS = {
    "SENTIMENT": [
        "Estou muito feliz com os resultados do projeto! A equipe trabalhou de forma excepcional e superou todas as expectativas.",
        
        "Infelizmente, o sistema apresentou vários bugs críticos que me deixaram muito frustrado e preocupado com os prazos.",
        
        "Estou triste e com raiva ao mesmo tempo. Esperava muito mais dessa apresentação, mas foi uma grande decepção.",
        
        "Que surpresa incrível! Não esperava receber essa notícia hoje. Estou cheio de alegria e esperança para o futuro.",
        
        "Sinto uma mistura de medo e esperança. O novo projeto é desafiador, mas também pode trazer grandes oportunidades.",
        
        "O comportamento dele me causou nojo e indignação. Como alguém pode agir dessa forma? Estou completamente decepcionado.",
        
        "Amo muito essa empresa e tenho carinho por todos os colegas. Trabalhar aqui tem sido uma experiência maravilhosa.",
        
        "Estou ansioso e preocupado com os resultados, mas também mantenho a confiança de que tudo dará certo no final."
    ],
    "SUMMARIZER": """A inteligência artificial (IA) é uma das tecnologias mais revolucionárias do século XXI, transformando drasticamente a forma como vivemos, trabalhamos e interagimos com o mundo. Desde sistemas de recomendação em plataformas de streaming até carros autônomos, a IA está presente em inúmeras aplicações do nosso cotidiano.

Os modelos de linguagem de grande escala, como GPT e BERT, representam um marco significativo no processamento de linguagem natural. Estes modelos são capazes de compreender contexto, gerar texto coerente e realizar tarefas complexas de compreensão textual. A arquitetura transformer, introduzida em 2017, revolucionou o campo e se tornou a base para a maioria dos modelos de IA generativa atuais.

No entanto, o desenvolvimento da IA também traz desafios importantes. Questões éticas, como viés algorítmico, privacidade de dados e o impacto no mercado de trabalho, precisam ser cuidadosamente consideradas. É essencial desenvolver IA de forma responsável, garantindo que os benefícios sejam amplamente distribuídos e os riscos minimizados.

O futuro da IA promete ainda mais avanços, com pesquisas em andamento sobre IA geral artificial, computação quântica aplicada à IA e sistemas multimodais que podem processar texto, imagem e áudio simultaneamente. Estas inovações têm o potencial de resolver problemas complexos em áreas como medicina, mudanças climáticas e educação."""
}

# Emojis para sentimentos
SENTIMENT_EMOJIS = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
    "mixed": "🎭",
    "very_positive": "🤩",
    "very_negative": "😢",
}

# Emojis para complexidade emocional
COMPLEXITY_EMOJIS = {
    "simple": "🔵",
    "moderate": "🟡",
    "complex": "🔴",
}

# Cores para diferentes categorias
COLORS = {
    "positive": "#28a745",  # Verde
    "negative": "#dc3545",  # Vermelho
    "neutral": "#6c757d",   # Cinza
    "primary": "#667eea",   # Azul primário
    "secondary": "#764ba2", # Roxo secundário
}

# Configurações de UI
UI_CONFIG = {
    "max_text_display_length": 500,
    "min_text_length": 10,
    "chat_message_height": 200,
    "sidebar_width": 300,
    "default_temperature": 0.7,
    "default_max_tokens": 1000,
}

# URLs importantes
URLS = {
    "groq_console": "https://console.groq.com/",
    "huggingface_tokens": "https://huggingface.co/settings/tokens",
    "github_repo": "https://github.com/PietroFilippo/ChatBot-Simples",
    "documentation": "#",  # Placeholder
}

# Instruções de configuração
CONFIG_INSTRUCTIONS = {
    "groq": """
    **Para configurar Groq:**
    1. Execute: `python setup_env.py`
    2. Configure sua chave quando solicitado
    3. Obtenha grátis em: [console.groq.com](https://console.groq.com/)
    """,
    "huggingface": """
    **Para configurar Hugging Face:**
    1. Execute: `python setup_env.py`
    2. Configure sua chave quando solicitado
    3. Obtenha grátis em: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
    """,
}

# Status indicators
STATUS_INDICATORS = {
    "available": "✅",
    "unavailable": "⚙️",
    "error": "❌",
    "loading": "⏳",
    "active": "🎯",
}

# Personalidades do chatbot
CHATBOT_PERSONALITIES = {
    "helpful": {
        "name": "Útil",
        "emoji": "🤝",
        "description": "Assistente prestativo e direto"
    },
    "creative": {
        "name": "Criativo", 
        "emoji": "🎨",
        "description": "Pensador criativo e imaginativo"
    },
    "technical": {
        "name": "Técnico",
        "emoji": "🔧",
        "description": "Especialista técnico detalhado"
    },
}

# Tipos de resumo
SUMMARY_TYPES = {
    "informative": {
        "name": "Informativo",
        "emoji": "📋",
        "description": "Resumo factual e objetivo"
    },
    "executive": {
        "name": "Executivo",
        "emoji": "💼", 
        "description": "Resumo para tomada de decisão"
    },
    "creative": {
        "name": "Criativo",
        "emoji": "🎭",
        "description": "Resumo com estilo narrativo"
    },
    "technical": {
        "name": "Técnico",
        "emoji": "⚙️",
        "description": "Resumo com foco técnico"
    },
}

# Limites e configurações
LIMITS = {
    "max_chat_history": 50,
    "max_file_size_mb": 10,
    "max_text_length": 50000,
    "min_summary_length": 50,
    "max_retries": 3,
    "request_timeout": 30,
} 