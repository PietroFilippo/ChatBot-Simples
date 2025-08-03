#!/usr/bin/env python3
"""
Script de Configuração Multi-Provider LLM

Este script configura automaticamente:
- Groq API (principal - gratuito)
- Hugging Face API
- Templates prontos para OpenAI, Claude, Gemini, etc.
- Configurações globais do sistema
- Instruções para adicionar novos providers

Uso: python setup_env.py
"""

import os
from typing import Optional
from datetime import datetime

def print_header():
    """Exibe cabeçalho do setup."""
    print("Script de Configuração Multi-Provider LLM")
    print("=" * 55)
    print("Configura Groq (gratuito)")
    print("Configura Hugging Face (gratuito)")
    print("Prepara templates para outros providers")
    print("Inclui instruções de extensão")
    print("=" * 55)

def print_section(title: str):
    """Exibe seção formatada."""
    print(f"\n🔹 {title}")
    print("-" * 40)

def validate_groq_key(key: str) -> bool:
    """
    Valida se a chave Groq tem formato correto
    
    Args:
        key: Chave da API Groq
        
    Returns:
        True se for válida, False caso contrário
    """
    if not key:
        return False
    
    # Chaves Groq começam com 'gsk_' e têm cerca de 50+ caracteres
    if key.startswith('gsk_') and len(key) > 40:
        return True
    
    return False

def validate_hf_key(key: str) -> bool:
    """
    Valida se a chave Hugging Face tem formato correto
    
    Args:
        key: Chave da API Hugging Face
        
    Returns:
        True se for válida, False caso contrário
    """
    if not key:
        return False
    
    # Chaves HF começam com 'hf_' e têm cerca de 30+ caracteres
    if key.startswith('hf_') and len(key) > 30:
        return True
    
    return False

def get_groq_key() -> Optional[str]:
    """
    Obtém chave da API Groq
    
    Returns:
        Chave da API ou None se pulada
    """
    print_section("CONFIGURAÇÃO DA API GROQ")
    
    print()
    print("Como obter a chave Groq gratuita:")
    print("   1. Acesse: https://console.groq.com/")
    print("   2. Faça cadastro")
    print("   3. Vá em 'API Keys'")
    print("   4. Clique 'Create API Key'")
    print("   5. Cole aqui a chave")
    print()
    
    while True:
        key = input("Cole sua chave Groq: ").strip()
        
        if validate_groq_key(key):
            print("Chave Groq válida")
            return key
        else:
            print("Chave inválida. Deve começar com 'gsk_' e ter mais de 40 caracteres.")
            print("   Exemplo: gsk_abc123def456...")
            
            retry = input("   Tentar novamente? (s/n): ").strip().lower()
            if retry in ['n', 'no', 'não']:
                return None

def get_huggingface_key() -> Optional[str]:
    """
    Obtém chave da API Hugging Face
    
    Returns:
        Chave da API ou None se pulada
    """
    print_section("CONFIGURAÇÃO DA API HUGGING FACE")
    
    print()
    print("Como obter a chave Hugging Face gratuita:")
    print("   1. Acesse: https://huggingface.co/settings/tokens")
    print("   2. Faça login/cadastro")
    print("   3. Clique 'New token'")
    print("   4. Selecione 'Read' permissions")
    print("   5. Cole aqui a chave")
    print()
    
    while True:
        key = input("Cole sua chave Hugging Face (ou Enter para pular): ").strip()
        
        if not key:
            print("Hugging Face pulado. Você pode configurar depois.")
            return None
        
        if validate_hf_key(key):
            print("Chave Hugging Face válida")
            return key
        else:
            print("Chave inválida. Deve começar com 'hf_' e ter mais de 30 caracteres.")
            print("   Exemplo: hf_abc123def456...")
            
            retry = input("   Tentar novamente? (s/n): ").strip().lower()
            if retry in ['n', 'no', 'não']:
                return None

def get_advanced_settings() -> dict:
    """
    Obtém configurações avançadas do usuário
    
    Returns:
        Dicionário com as configurações
    """
    print_section("CONFIGURAÇÕES AVANÇADAS (OPCIONAL)")
    
    settings = {}
    
    # Modelo padrão
    print("Escolha o modelo padrão do Groq:")
    print("   1. llama3-70b-8192 (Recomendado)")
    print("   2. llama3-8b-8192")
    
    model_choice = input("\nEscolha (1-2) ou Enter para padrão [1]: ").strip()
    
    models = {
        "1": "llama3-70b-8192",
        "2": "llama3-8b-8192"
    }
    
    settings["model"] = models.get(model_choice, "llama3-70b-8192")
    
    # Criatividade
    print(f"\nCriatividade das respostas:")
    print("   0.0 = Muito conservador/preciso")
    print("   0.7 = Balanceado (recomendado)")
    print("   1.0 = Muito criativo/variado")
    
    criatividade_input = input("\nCriatividade (0.0-1.0) ou Enter para padrão [0.7]: ").strip()
    
    try:
        criatividade = float(criatividade_input) if criatividade_input else 0.7
        settings["temperature"] = max(0.0, min(1.0, criatividade))
    except ValueError:
        settings["temperature"] = 0.7
    
    # Max tokens
    print(f"\nMáximo de tokens por resposta:")
    print("   500 = Respostas curtas")
    print("   1000 = Balanceado (recomendado)")
    print("   2000 = Respostas longas")
    
    tokens_input = input("\nMax tokens ou Enter para padrão [1000]: ").strip()
    
    try:
        tokens = int(tokens_input) if tokens_input else 1000
        settings["max_tokens"] = max(100, min(4000, tokens))
    except ValueError:
        settings["max_tokens"] = 1000
    
    return settings

def create_env_file(groq_key: Optional[str], hf_key: Optional[str], settings: dict) -> bool:
    """
    Cria arquivo .env com as configurações
    
    Args:
        groq_key: Chave da API Groq
        hf_key: Chave da API Hugging Face
        settings: Configurações avançadas
        
    Returns:
        True se criado com sucesso, False caso contrário
    """
    
    env_content = f"""# ================================
# CONFIGURAÇÃO AUTOMÁTICA LLM
# ================================
# Arquivo gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Para reconfigurar, execute: python setup_env.py
#
# IMPORTANTE: 
# - Este arquivo já está no .gitignore
# - Não compartilhe suas API keys
# - Mantenha suas chaves seguras

# ================================
# GROQ API (ATIVO)
# ================================
# Provider principal - gratuito e rápido
# Rate Limit: Generoso para uso pessoal
# Modelos: Llama 3
"""

    # Adiciona a configuração do Groq se a chave foi fornecida
    if groq_key:
        env_content += f"""
GROQ_API_KEY={groq_key}
"""
    else:
        env_content += """
# GROQ_API_KEY=sua_chave_groq_aqui
"""

    # Adiciona a configuração do Hugging Face se a chave foi fornecida
    if hf_key:
        env_content += f"""
# ================================
# HUGGING FACE API (ATIVO)
# ================================
# Modelos open-source gratuitos
# Rate Limit: 1,000 requests/dia (gratuito)
# Documentação: https://huggingface.co/docs/api-inference/

HUGGINGFACE_API_KEY={hf_key}
HF_TOKEN={hf_key}
HUGGINGFACE_DEFAULT_MODEL=google/flan-t5-large
"""
    else:
        env_content += """
# ================================
"""
    env_content += f"""
# ================================
# OPENAI API (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://platform.openai.com/docs/
# Rate Limit: Varia conforme plano

# OPENAI_API_KEY=sk-proj-sua_chave_openai_aqui
# OPENAI_DEFAULT_MODEL=gpt-3.5-turbo
# OPENAI_TEMPERATURE=0.7
# OPENAI_MAX_TOKENS=1000

# ================================
# ANTHROPIC CLAUDE (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://docs.anthropic.com/
# Rate Limit: Varia conforme plano
# Modelos: claude-3-haiku, claude-3-sonnet, claude-3-opus

# ANTHROPIC_API_KEY=sk-ant-sua_chave_claude_aqui
# CLAUDE_DEFAULT_MODEL=claude-3-haiku-20240307
# CLAUDE_TEMPERATURE=0.7
# CLAUDE_MAX_TOKENS=1000

# ================================
# GOOGLE GEMINI (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://ai.google.dev/docs
# Rate Limit: Varia conforme plano
# Modelos: gemini-pro, gemini-pro-vision

# GOOGLE_API_KEY=sua_chave_google_aqui
# GEMINI_DEFAULT_MODEL=gemini-pro
# GEMINI_TEMPERATURE=0.7
# GEMINI_MAX_TOKENS=1000

# ================================
# COHERE API (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://docs.cohere.com/
# Rate Limit: Varia conforme plano
# Modelos: command, command-light

# COHERE_API_KEY=sua_chave_cohere_aqui
# COHERE_DEFAULT_MODEL=command
# COHERE_TEMPERATURE=0.7
# COHERE_MAX_TOKENS=1000

# ================================
# AZURE OPENAI (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure suas credenciais
# Documentação: https://docs.microsoft.com/azure/cognitive-services/openai/

# AZURE_OPENAI_KEY=sua_chave_azure_aqui
# AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
# AZURE_OPENAI_VERSION=2023-12-01-preview
# AZURE_OPENAI_DEPLOYMENT=seu-deployment-name

# ================================
# TEMPLATE PARA NOVOS PROVIDERS
# ================================
# Para adicionar um novo provider, copie o template abaixo:
#
# SEU_PROVIDER_API_KEY=sua_chave_aqui
# SEU_PROVIDER_DEFAULT_MODEL=modelo_padrao
# SEU_PROVIDER_TEMPERATURE=0.7
# SEU_PROVIDER_MAX_TOKENS=1000
#
# Depois crie o arquivo: src/providers/seu_provider.py
# E adicione ao: src/providers/__init__.py

# ================================
# CONFIGURAÇÕES GROQ (ATIVAS) 
# ================================
DEFAULT_MODEL={settings['model']}

# ================================
# CONFIGURAÇÕES GLOBAIS
# ================================
# Configurações que se aplicam a todos os providers

# Parâmetros de geração (todos os providers)
GLOBAL_TEMPERATURE={settings['temperature']}
GLOBAL_MAX_TOKENS={settings['max_tokens']}

# Timeout para APIs (segundos)
API_TIMEOUT=30

# Retry automático em caso de erro
AUTO_RETRY=true
MAX_RETRIES=3

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# ================================
# DESENVOLVIMENTO E TESTE
# ================================
# Configurações para desenvolvimento

# Modo debug (mostra mais informações)
DEBUG_MODE=false

# Provider mock para testes (true/false)
ENABLE_MOCK_PROVIDER=false

# Cache de respostas para desenvolvimento
ENABLE_RESPONSE_CACHE=false

# ================================
# CONFIGURAÇÕES AUTOMÁTICAS
# ================================
# Este arquivo foi gerado pelo setup_env.py
# Para reconfigurar, execute: python setup_env.py
# 
# IMPORTANTE: 
# - Não commitar este arquivo no Git (já está no .gitignore)
# - Mantenha suas chaves API seguras
# - Para obter ajuda: python setup_env.py --help

# ================================
# DOCUMENTAÇÃO E LINKS ÚTEIS
# ================================
# GROQ Console: https://console.groq.com/
# Hugging Face Tokens: https://huggingface.co/settings/tokens
# OpenAI Platform: https://platform.openai.com/
# Anthropic Console: https://console.anthropic.com/
# Google AI Studio: https://ai.google.dev/
# Azure OpenAI: https://azure.microsoft.com/pt-br/products/ai-services/openai-service
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        return True
        
    except Exception as e:
        print(f"Erro ao criar arquivo .env: {e}")
        return False

def test_configuration():
    """Testa se a configuração está funcionando."""
    print_section("TESTANDO CONFIGURAÇÃO")
    
    print("Testando importação dos módulos")
    
    try:
        # Testar importações básicas
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from src.llm_providers import llm_manager
        
        print("Módulos importados com sucesso")
        
        # Testar provedores
        print(f"Status do Groq: {'Ativo' if llm_manager.is_groq_available() else 'Inativo'}")
        
        # Testar resposta
        if llm_manager.is_groq_available():
            response = llm_manager.invoke_llm("Diga olá")
            print(f"Teste de resposta: {response[:30]}...")
        else:
            print("Groq não ativo - verifique a configuração")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste: {e}")
        print("   Pode ser necessário instalar dependências:")
        print("   pip install -r requirements.txt")
        return False

def show_next_steps():
    """Mostra próximos passos para o usuário."""
    print_section("PRÓXIMOS PASSOS")
    
    print("Configuração concluída. Agora você pode:")
    print()
    print("1️Instalar dependências caso ainda não tenha feito:")
    print("   pip install -r requirements.txt")
    print()
    print("2️Executar a interface web:")
    print("   streamlit run app.py")
    print()
    print("3️Adicionar outros providers (opcional):")
    print("   • Edite o arquivo .env gerado")
    print("   • Descomente as seções dos providers desejados")
    print("   • Configure suas API keys")
    print("   • Implemente os providers em src/providers/")
    print()
    print("Templates prontos no .env para:")
    print("   OpenAI GPT")
    print("   • Anthropic Claude") 
    print("   • Google Gemini")
    print("   • Cohere")
    print("   • Azure OpenAI")
    print("   • Hugging Face")
    print()
    print("Documentação completa:")
    print("   • README.md - Visão geral")
    print("   • src/providers/README.md - Guia de implementação")
    print("   • PROVIDER_INTEGRATION_GUIDE.md - Guia completo")
    print()

def main():
    """Função principal do setup."""
    print_header()
    
    # Verificar se .env já existe
    if os.path.exists('.env'):
        print("Arquivo .env já existe.")
        overwrite = input("   Deseja sobrescrever? (s/n): ").strip().lower()
        
        if overwrite not in ['s', 'sim', 'y', 'yes']:
            print("Setup cancelado.")
            return
        
        # Backup do arquivo existente
        backup_name = f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename('.env', backup_name)
        print(f"Backup salvo como: {backup_name}")
    
    try:
        
        # Coletar informações
        groq_key = get_groq_key()
        hf_key = get_huggingface_key()
        
        # Configurações avançadas
        advanced = input("\nConfigurar opções avançadas? (s/n): ").strip().lower()
        if advanced in ['s', 'sim', 'y', 'yes']:
            settings = get_advanced_settings()
        else:
            settings = {
                "model": "llama3-70b-8192",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        
        # Criar arquivo .env
        print_section("CRIANDO ARQUIVO .ENV")
        
        if create_env_file(groq_key, hf_key, settings):
            print("Arquivo .env criado com sucesso")
            
            # Testar configuração
            if test_configuration():
                print("Configuração testada e funcionando")
            
            # Mostrar próximos passos
            show_next_steps()
            
        else:
            print("Erro ao criar arquivo .env")
            
    except KeyboardInterrupt:
        print("\nSetup cancelado pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("   Entre em contato ou tente configurar manualmente.")

if __name__ == "__main__":
    main() 