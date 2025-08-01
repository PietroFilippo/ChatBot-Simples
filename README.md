# Sistema de IA Generativa Multi-Funcional

## Funcionalidades Principais

### Sistema de Provedores Extensível

- **Plugin System** - Adicione novos provedores de LLM sem modificar código existente
- **Auto-Discovery** - Novos provedores são detectados e registrados automaticamente  
- **Fallback Inteligente** - Sistema escolhe o melhor provedor disponível
- **Zero Regressão** - Código existente permanece intocado ao adicionar funcionalidades

## Funcionalidades Principais

### Chatbot Inteligente
- **Conversa natural** com memória de contexto
- **Diferentes personalidades** configuráveis (helpful, creative, technical)
- **Switching dinâmico** entre provedores LLM
- **Export de conversas** em JSON/TXT

### Análise de Sentimentos
- **Análise contextual** usando LLM
- **Precisão alta** em diferentes linguas
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

## Tecnologias Utilizadas

- **🐍 Python 3.8+** - Linguagem principal
- **🔗 LangChain** - Framework para aplicações LLM
- **🚀 Groq API** - LLM rápido e gratuito (Llama 3, Mixtral)
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

### 3. **Configuração Multi-Provider**

O sistema inclui um setup automático que configura Groq + templates para outros providers caso precise:

```bash
python setup_env.py
```

**O que o setup faz:**
- **Configura Groq** (gratuito) - principal provider
- **Gera templates prontos** para OpenAI, Claude, Gemini, etc.
- **Configurações globais** (timeout, retry, debug)
- **Documentação inline** com links e instruções

#### **Setup Manual Alternativo**
Ou também, para configuração manual, crie o arquivo `.env`:
```env
GROQ_API_KEY=sua_chave_groq_aqui
```

**Para obter uma chave Groq gratuita**: [console.groq.com](https://console.groq.com/)

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
- **Hugging Face** (modelos open-source)

## Como Adicionar um Novo Provedor

### **Método Rápido: Usar Templates**

1. **Configure o ambiente:**
   ```bash
   python setup_env.py  # Gera templates prontos
   ```

2. **Ative um provider:**
   - Abra o arquivo `.env` gerado
   - Descomente a seção do provider desejado
   - Configure sua API key
   - Salve o arquivo

3. **Implemente o provider (se não existir):**
   - Copie um template de `src/providers/` ou use um já existente
   - Customize para sua API ou descomente caso o provider seja um dos templates já existentes
   - Adicione ao `__init__.py`

### **Método Detalhado: Implementação Customizada**

### 1. **Criar o Arquivo do Provedor**

Use os templates em `src/providers/` como base:
- `openai_provider_example.py` - Template OpenAI
- `claude_provider_example.py` - Template Claude

```python
from src.interfaces import ILLMProvider

class MeuProvedor(ILLMProvider):
    def __init__(self):
        self.name = "meu_provider"
        # ... inicialização
    
    # Implementar todos os métodos abstratos da interface
```

### 2. **Implementar Métodos Obrigatórios**

Todos os provedores devem implementar a interface `ILLMProvider`:

```python
def get_name(self) -> str:
    """Nome único do provedor"""
    
def is_available(self) -> bool:
    """Verifica se está configurado e disponível"""
    
def generate_response(self, message: str) -> str:
    """Gera resposta usando a API"""
    
def get_info(self) -> Dict[str, Any]:
    """Informações sobre o provedor"""
    
def get_available_models(self) -> List[str]:
    """Lista modelos disponíveis"""
    
def switch_model(self, model: str) -> bool:
    """Troca modelo ativo"""
    
def get_current_model(self) -> str:
    """Modelo atual"""
    
def get_performance_stats(self) -> Dict[str, Any]:
    """Estatísticas de performance"""
```

### 3. **Atualizar Exportações**

Edite `__init__.py` para exportar o novo provedor:

```python
from .groq_provider import GroqProvider
from .meu_provider import MeuProvedor  # Adicione esta linha

__all__ = ['GroqProvider', 'MeuProvedor']  # Adicione ao __all__
```

### 4. **Registro Automático**

O sistema registra automaticamente novos provedores. Para registro manual:

```python
from src.providers import MeuProvedor
from src.provider_registry import provider_registry

# Registro manual (opcional)
provider_registry.register_provider(MeuProvedor())
```

### 5. **Configuração de Environment**

Adicione variáveis necessárias no `.env`:

```env
MEU_PROVIDER_API_KEY=sua_chave_aqui
MEU_PROVIDER_DEFAULT_MODEL=modelo_padrao
```
Ou use o arquivo `setup_env.py`

### 6. **Mapeamentos de UI (Opcional)**

Para nomes amigáveis na interface, edite `app.py`:

```python
# Em show_sidebar()
provider_names = {
    "groq": "🚀 Groq",
    "meu_provider": "🔥 Meu Provider"  # Adicione esta linha
}

# Em model selector
model_names = {
    "llama3-70b-8192": "🦙 Llama 3 70B",
    "meu_modelo": "🤖 Meu Modelo"  # Adicione modelos
}
```

## Templates Disponíveis

O projeto inclui templates prontos em `src/providers/` para facilitar a implementação:

### **OpenAI Template** (`openai_provider_example.py`)
- Estrutura completa para OpenAI API
- Configuração via variáveis de ambiente
- Documentação inline detalhada
- Implementação mock para testes
- Suporte para GPT-3.5, GPT-4, GPT-4o

### **Claude Template** (`claude_provider_example.py`)  
- Integração com Anthropic Claude API
- Suporte para modelos Haiku, Sonnet, Opus
- Configurações otimizadas para cada modelo
- Estrutura seguindo padrões do projeto

### **Templates de Configuração**
- **setup_env.py** - Templates automáticos no `.env`
- **Documentação inline** - Instruções em cada template

### **Como Usar os Templates:**

1. **Copie um template:**
   ```bash
   cp src/providers/openai_provider_example.py src/providers/meu_provider.py
   ```

2. **Customize para sua API:**
   - Substitua "OpenAI" pelo nome do seu provider
   - Ajuste URLs e parâmetros da API
   - Configure variáveis de ambiente

3. **Ative no sistema:**
   ```python
   # src/providers/__init__.py
   from .meu_provider import MeuProvider
   __all__ = ['GroqProvider', 'MeuProvider']
   ```

## **Configuração Avançada**

### **Setup Automático Inteligente**

O `setup_env.py` também possui:

#### **Configurações Globais:**
```env
# Gerado automaticamente pelo setup
API_TIMEOUT=30           # Timeout para todas as APIs
AUTO_RETRY=true          # Retry automático em falhas
MAX_RETRIES=3            # Máximo de tentativas
LOG_LEVEL=INFO           # Nível de log (DEBUG/INFO/WARNING/ERROR)
DEBUG_MODE=false         # Modo debug para desenvolvimento
ENABLE_MOCK_PROVIDER=false  # Provider mock para testes
```

#### **Atualização Segura:**
- **Backup automático** do `.env` existente
- **Validação** de chaves de API
- **Teste automático** da configuração
- **Próximos passos** claros após setup

## Checklist para a Implementação

- [ ] Arquivo do provedor criado
- [ ] Todos os métodos da interface implementados
- [ ] Tratamento de erros robusto
- [ ] Configuração via variáveis de ambiente
- [ ] Exportação no `__init__.py`
- [ ] Testes básicos funcionando
- [ ] Documentação das configurações necessárias
- [ ] Mapeamentos de UI (se necessário)

## Provedores Implementáveis

### **Principais APIs LLM:**
- **OpenAI**: GPT-3.5, GPT-4, GPT-4 Turbo, GPT-4o
- **Anthropic**: Claude 3 (Haiku, Sonnet, Opus)
- **Google**: Gemini Pro, Gemini Pro Vision
- **Cohere**: Command, Command-Light
- **Azure OpenAI**: GPT via Azure Cloud
- **AWS Bedrock**: Múltiplos modelos via AWS
- **Hugging Face**: Modelos open-source via API
- **Ollama**: Modelos locais
- **Together AI**: Modelos open-source hospedados 

---

## **Para Começar Rapidamente**

1. **Setup básico (2 minutos):**
   ```bash
   git clone <ChatBot-Simples>
   cd ChatBot
   pip install -r requirements.txt
   python setup_env.py
   streamlit run app.py
   ```

2. **Adicionar providers (30 segundos cada):**
   - Edite o `.env` gerado
   - Descomente a seção do provider desejado
   - Configure sua API key
   - Reinicie a aplicação

3. **Implementar provider customizado:**
   - Use templates em `src/providers/`
   - Siga o guia de implementação
   - Sistema detecta automaticamente

## **Recursos e Links Úteis**

### **APIs Gratuitas para Testar:**
- **Groq** (gratuito): [console.groq.com](https://console.groq.com/)
- **Hugging Face** (gratuito): [huggingface.co/inference-api](https://huggingface.co/inference-api)
- **Google AI** (trial): [ai.google.dev](https://ai.google.dev)

### **Documentação Técnica:**
- **SOLID Principles**: Projeto segue todos os 5 princípios
- **Plugin Architecture**: Sistema extensível sem modificações
- **Dependency Injection**: Arquitetura modular e testável
- **Interface Segregation**: Interfaces específicas e focadas

### **Para Desenvolvimento:**
- **Modo Debug**: Configure `DEBUG_MODE=true` no `.env`
- **Provider Mock**: Configure `ENABLE_MOCK_PROVIDER=true`
- **Logs Detalhados**: Configure `LOG_LEVEL=DEBUG`

---

**Dica**: Comece sempre com uma implementação mock para testar a integração, depois implemente a lógica real da API. 
