# Sistema de IA Generativa Multi-Funcional

## Funcionalidades Principais

### Sistema de Provedores Extensível

- **BaseProvider Architecture** - Classe base que elimina duplicação de código entre providers
- **Plugin System** - Adicione novos provedores de LLM sem modificar código existente
- **Auto-Discovery** - Novos provedores são detectados e registrados automaticamente  
- **Fallback Inteligente** - Sistema escolhe o melhor provedor disponível
- **Zero Regressão** - Código existente permanece intocado ao adicionar funcionalidades
- **Configurações Globais Centralizadas** - Parâmetros unificados para todos os providers

### Chatbot Inteligente
- **Conversa natural** com memória de contexto
- **Diferentes personalidades** configuráveis (helpful, creative, technical)
- **Switching dinâmico** entre provedores LLM
- **Interface moderna** com componentes UI especializados

### Análise de Sentimentos
- **Análise contextual** usando LLM
- **Precisão alta** em diferentes linguages
- **Explicações detalhadas** dos resultados
- **Métricas de confiança** precisas

### Geração de Resumos
- **Diferentes estratégias**: Extrativa (NLTK) + Generativa (LangChain)
- **Tipos de resumo**: Informativo, Executivo, Criativo, Técnico
- **Comparação automática** de métodos
- **Métricas de compressão** detalhadas

### Analytics & Monitoramento
- **Status em tempo real** dos provedores
- **Métricas de performance** e uso
- **Estatísticas da sessão** detalhadas
- **Dashboard de configurações globais**

## Tecnologias Utilizadas

- **🐍 Python 3.8+** - Linguagem principal
- **🔗 LangChain** - Framework para aplicações LLM
- **🚀 Groq API** - LLM rápido e gratuito (Llama 3, Mixtral)
- **🤗 Hugging Face** - 91+ modelos open-source via API unificada
- **📱 Streamlit** - Interface web interativa
- **📊 NLTK** - Processamento de linguagem natural
- **🔧 Pydantic** - Validação de dados
- **📦 Pandas/NumPy** - Manipulação de dados
- **🏗️ ABC (Abstract Base Classes)** - Interfaces e contratos

## Configuração e Execução

### 1. **Clonar o Repositório**
```bash
git clone <ChatBot-Simples>
cd ChatBot
```

### 2. **Instalar as Dependências**
```bash
pip install -r requirements.txt
```

### 3. **Configuração Multi-Provider Automatizada**

O sistema inclui um setup inteligente que configura automaticamente **Groq** e **Hugging Face**, além de gerar templates para outros providers:

```bash
python setup_env.py
```

**O que o setup faz:**
- **Configura Groq** (gratuito) - provider principal ultra-rápido
- **Configura Hugging Face** (gratuito) - 91+ modelos open-source disponíveis
- **Gera templates prontos** para OpenAI, Claude, Gemini, etc.
- **Configurações globais centralizadas** (timeout, retry, debug)
- **Documentação inline** com links e instruções
- **Validação automática** de chaves API
- **Teste de configuração** pós-setup

#### **Configuração Manual Alternativa**
Ou também, para configuração manual, crie o arquivo `.env`:
```env
# Provider principal (ultra-rápido)
GROQ_API_KEY=sua_chave_groq_aqui

# Provider com múltiplos modelos open-source  
HUGGINGFACE_API_KEY=sua_chave_hf_aqui

# Configurações globais (aplicadas a todos os providers)
GLOBAL_TEMPERATURE=0.7
GLOBAL_MAX_TOKENS=1000
API_TIMEOUT=30
```

**Para obter chaves gratuitas:**
- **Groq**: [console.groq.com](https://console.groq.com/)
- **Hugging Face**: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 4. **Executar a Aplicação**
```bash
streamlit run app.py
```

### 5. **Ativação Rápida de Outros Providers**

O arquivo `.env` gerado já inclui **templates comentados** para ativação rápida:

```env
# Para ativar OpenAI: descomente e configure
# OPENAI_API_KEY=sk-proj-sua_chave_openai_aqui
# OPENAI_DEFAULT_MODEL=gpt-3.5-turbo

# Para ativar Claude: descomente e configure  
# ANTHROPIC_API_KEY=sk-ant-sua_chave_claude_aqui
# CLAUDE_DEFAULT_MODEL=claude-3-haiku-20240307

# Para ativar Gemini: descomente e configure
# GOOGLE_API_KEY=sua_chave_google_aqui
# GEMINI_DEFAULT_MODEL=gemini-pro
```

**Providers com templates prontos:**
- **OpenAI** (GPT-3.5, GPT-4, GPT-4o)
- **Anthropic Claude** (Haiku, Sonnet, Opus)  
- **Google Gemini** (Gemini Pro, Vision)
- **Cohere** (Command, Command-Light)
- **Azure OpenAI** (configuração completa)

Templates atualizados incluem configurações globais, estatísticas de performance, etc.

## Arquitetura do Sistema

### **Componentes Principais**

#### **1. BaseProvider (`src/providers/base_provider.py`)**
- **Elimina duplicação** - Centraliza funcionalidades comuns entre providers
- **Abstract Base Class** - Define interface obrigatória para todos os providers
- **Statistics tracking** - Métricas de performance padronizadas
- **Error handling** - Tratamento de erros consistente

#### **2. Provider Registry (`src/provider_registry.py`)**
- **Registro automático** de novos provedores
- **Seleção inteligente** do melhor provider disponível  
- **Switching dinâmico** entre providers
- **Fallback** em caso de indisponibilidade

#### **3. Configurações Centralizadas**
- **Constants (`ui/constants.py`)** - Strings, mensagens e configurações centralizadas
- **Validations (`ui/common_validations.py`)** - Validações reutilizáveis
- **Styles (`ui/styles.css`)** - CSS externalizado e organizado
- **Global Config (`src/config.py`)** - Parâmetros aplicados a todos os providers

#### **4. Componentes UI (`src/ui/components.py`)**
- **Single Responsibility** - cada componente tem uma função específica
- **Reutilizáveis** - componentes modulares e focados
- **Factory Pattern** - criação especializada de conjuntos de componentes
- **Separação clara** entre input, display, validation e settings

#### **5. Interfaces Abstratas (`src/interfaces.py`)**
- **Contratos claros** entre componentes
- **Implementação obrigatória** de métodos essenciais
- **Type safety** com typing hints
- **Documentação integrada**

### **Providers Implementados**

#### **Groq Provider (`src/providers/groq_provider.py`)**
- **Ultra-rápido** - API otimizada para velocidade
- **Gratuito** - 30 requests/minuto sem custo
- **Modelos**: Llama 3 70B, Llama 3 8B
- **Configurações globais** aplicadas automaticamente

#### **Hugging Face Provider (`src/providers/huggingface_provider.py`)**
- **91+ modelos** disponíveis via API unificada
- **OpenAI-compatible** - formato de requisição padronizado
- **Modelos testados**: Gemma 2, DeepSeek R1, Phi-4, Qwen2.5-Coder
- **Rate limits generosos** - 1,000+ requests/dia gratuito

## Como Adicionar um Novo Provedor

### **Método Rápido: Usar BaseProvider**

1. **Crie o arquivo do provider:**
   ```python
   from .base_provider import BaseProvider
   from src.config import GlobalConfig
   
   class MeuProvider(BaseProvider):
       def __init__(self):
           self.default_model = "modelo-padrao"
           self.current_model = os.getenv("MEU_PROVIDER_MODEL", self.default_model)
           
           super().__init__(
               name="meu_provider",
               available_models=["modelo1", "modelo2"]
           )
       
       def _setup(self):
           # Configuração específica do provider
           pass
       
       def _generate_response_impl(self, message: str, **kwargs) -> str:
           # Implementação da geração de resposta
           pass
   ```

2. **Benefícios do BaseProvider:**
   - **90% menos código** - Métodos comuns já implementados
   - **Statistics automáticas** - Tracking de requests, erros, etc.
   - **Error handling** - Tratamento padronizado de erros
   - **Performance stats** - Métricas de performance integradas

### **Método Detalhado: Implementação Customizada**

### 1. **Criar o Arquivo do Provedor**

Use os providers existentes como base:
- `groq_provider.py` - Implementação com LangChain
- `huggingface_provider.py` - Implementação com requests

**Recursos dos providers refatorados:**
- **BaseProvider inheritance** - Elimina duplicação de código
- **Configurações globais centralizadas** via `GlobalConfig`
- **Estatísticas de performance** integradas
- **Tratamento de erros** robusto

```python
from .base_provider import BaseProvider
from src.config import GlobalConfig

class MeuProvedor(BaseProvider):
    def __init__(self):
        self.default_model = "modelo-padrao"
        self.current_model = os.getenv("MEU_PROVIDER_MODEL", self.default_model)
        
        super().__init__(
            name="meu_provider",
            available_models=["modelo1", "modelo2"]
        )
    
    def _setup(self):
        # Configuração específica do provider
        pass
    
    def _generate_response_impl(self, message: str, **kwargs) -> str:
        # Implementação da geração de resposta
        pass
```

### 2. **Métodos Herdados do BaseProvider**

Ao herdar de `BaseProvider`, você automaticamente obtém:

```python
# Métodos já implementados (não precisa reescrever):
def get_name(self) -> str
def is_available(self) -> bool  
def get_available_models(self) -> List[str]
def get_current_model(self) -> str
def generate_response(self, message: str, **kwargs) -> str  # Com statistics
def get_stats(self) -> Dict[str, Any]
def get_performance_stats(self) -> Dict[str, Any]

# Métodos que você deve implementar:
def _setup(self) -> None  # Configuração específica
def _generate_response_impl(self, message: str, **kwargs) -> str  # Geração
```

### 3. **Atualizar Exportações**

Edite `src/providers/__init__.py` para exportar o novo provedor:

```python
from .base_provider import BaseProvider
from .groq_provider import GroqProvider
from .huggingface_provider import HuggingFaceProvider
from .meu_provider import MeuProvedor  # Adicione esta linha

__all__ = ['BaseProvider', 'GroqProvider', 'HuggingFaceProvider', 'MeuProvedor']
```

### 4. **Registro Automático**

O sistema registra automaticamente novos provedores através do `ProviderRegistry`. O registro acontece automaticamente no `__init__()` do registry.

### 5. **Configuração de Environment**

Adicione variáveis necessárias no `.env`:

```env
MEU_PROVIDER_API_KEY=sua_chave_aqui
MEU_PROVIDER_DEFAULT_MODEL=modelo_padrao
```

### 6. **Usar Configurações Globais**

Aproveite as configurações centralizadas:

```python
from src.config import GlobalConfig

# Em _setup
params = GlobalConfig.get_generation_params()
self.temperature = params["temperature"]
self.max_tokens = params["max_tokens"]

# Com overrides específicos se necessário
params = GlobalConfig.get_generation_params(temperature=0.9)
```

## **Configuração Avançada**

### **Configurações Globais Centralizadas**

O sistema usa configurações centralizadas através da classe `GlobalConfig`:

```env
# Parâmetros de geração (aplicados a todos os providers)
GLOBAL_TEMPERATURE=0.7       # Criatividade (0.0-1.0)  
GLOBAL_MAX_TOKENS=1000       # Tamanho máximo das respostas

# Configurações de API
API_TIMEOUT=30               # Timeout para todas as APIs
AUTO_RETRY=true              # Retry automático em falhas
MAX_RETRIES=3                # Máximo de tentativas

# Configurações de desenvolvimento
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
DEBUG_MODE=false             # Modo debug para desenvolvimento
```

### **Setup Automático Inteligente**

O `setup_env.py` inclui:

#### **Funcionalidades Avançadas:**
- **Validação automática** de chaves API (formato correto)
- **Backup automático** do `.env` existente antes de sobrescrever
- **Teste de configuração** pós-setup
- **Templates inline** com documentação completa
- **Próximos passos** claros após configuração

#### **Modo Interativo:**
- **Configurações avançadas** opcionais (temperatura, max_tokens, modelo)
- **Instruções contextuais** para obter cada tipo de chave
- **Validação em tempo real** com feedback claro

## Checklist para a Implementação

- [ ] Arquivo do provedor criado herdando de `BaseProvider`
- [ ] Métodos `_setup()` e `_generate_response_impl()` implementados
- [ ] Uso das configurações globais via `GlobalConfig`
- [ ] Tratamento de erros robusto
- [ ] Configuração via variáveis de ambiente
- [ ] Exportação no `src/providers/__init__.py`
- [ ] Testes básicos funcionando
- [ ] Documentação das configurações necessárias
- [ ] Performance stats automáticas via BaseProvider
- [ ] Atualização das constantes em `ui/constants.py` se necessário

Use a `BaseProvider` como classe base para um novo provider.

---

## **Recursos e Links Úteis**

### **APIs Gratuitas para Testar:**
- **Groq** (gratuito): [console.groq.com](https://console.groq.com/)
- **Hugging Face** (gratuito): [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **Google AI** (trial): [ai.google.dev](https://ai.google.dev)

### **Documentação Técnica:**
- **SOLID Principles**: Projeto implementa todos os 5 princípios
- **DRY Principle**: BaseProvider elimina duplicação de código
- **Plugin Architecture**: Sistema extensível sem modificações
- **Dependency Injection**: Registry modular e testável
- **Component Segregation**: UI components especializados
- **Centralized Configuration**: GlobalConfig para configurações unificadas

### **Para Desenvolvimento:**
- **Modo Debug**: Configure `DEBUG_MODE=true` no `.env`
- **Logs Detalhados**: Configure `LOG_LEVEL=DEBUG`
- **Configurações Customizadas**: Use overrides no `GlobalConfig`

---
