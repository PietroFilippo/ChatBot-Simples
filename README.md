# Sistema de IA Generativa Multi-Funcional

## Funcionalidades Principais

### Chatbot
- **Conversa natural** com memória de contexto
- **Diferentes personalidades** configuráveis (helpful, creative, technical)
- **Switching dinâmico** entre provedores LLM

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

## 🚀 Configuração e Execução

### 1. **Clonar o Repositório**
```bash
git clone <ChatBot-Simples>
cd ChatBot
```

### 2. **Instalar as Dependências**
```bash
pip install -r requirements.txt
```

### 3. **Configurar API Key**
```bash
python setup_env.py
```

Ou manualmente, criar o arquivo `.env`:
```env
GROQ_API_KEY=sua_chave_groq_aqui
```

**Para obter uma chave Groq gratuita em**: [console.groq.com](https://console.groq.com/)

### 4. **Executar a Aplicação**
```bash
streamlit run app.py
```