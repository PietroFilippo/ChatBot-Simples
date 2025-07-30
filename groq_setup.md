#Como Configurar o Groq API

### 1. Gerar API Key

1. Acesse: https://console.groq.com/keys
2. Clique em "Create API Key"
3. Dê um nome
4. Copie a key (começa com `gsk_...`)

### 2. Configuração e execução automática do projeto

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar configuração automática
python setup_env.py

# 3. Executar aplicação
streamlit run app.py
```

## Modelos Disponíveis

| Modelo | Descrição | Velocidade | Qualidade |
|--------|-----------|------------|-----------|
| `llama3-70b-8192` | **Recomendado** - Melhor qualidade | Rápido | Excelente |
| `llama3-8b-8192` | Mais rápido, boa qualidade | Ultra Rápido | Muito Boa |


## Limites Gratuitos

- **6.000 requests/minuto**
- **30.000 tokens/minuto**
- **Sem limite diário**
- **Sem expiração**

## Troubleshooting

### Erro: "Groq API key não encontrada"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz
2. Confirme que a key começa com `gsk_`
3. Não deixe espaços na linha: `GROQ_API_KEY=gsk_...`

### Erro: "Rate limit exceeded"

**Solução:**
1. Aguarde alguns segundos
2. O limite é bem alto, raramente acontece

### Erro: "Invalid API key"

**Solução:**
1. Gere uma nova key em: https://console.groq.com/keys
2. Confirme que copiou a key completa

---