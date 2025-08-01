#!/usr/bin/env python3
"""
Script de Configuração Multi-Provider LLM

Este script configura automaticamente:
- Groq API (principal - gratuito)
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
    print("=" * 50)
    print("Configura Groq (gratuito)")
    print("Prepara templates para outros providers")
    print("Inclui instruções de extensão")
    print("=" * 50)

def print_section(title: str):
    """Exibe seção formatada."""
    print(f"\n {title}")
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

def create_env_file(groq_key: Optional[str], settings: dict) -> bool:
    """
    Cria o arquivo .env com as configurações e templates para futuros providers
    
    Args:
        groq_key: Chave da API Groq
        settings: Configurações avançadas
        
    Returns:
        True se criado com sucesso
    """
    try:
        env_content = f"""# ================================================================
# CONFIGURAÇÃO MULTI-PROVIDER LLM
# Gerado automaticamente em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ================================================================

# ================================
# GROQ API (ATIVO)
# ================================
# Documentação: https://console.groq.com/docs
# Rate Limit: 30 requests/minuto (gratuito)
# Modelos: llama3-70b-8192, llama3-8b-8192
"""
        
        if groq_key:
            env_content += f"GROQ_API_KEY={groq_key}\n"
        else:
            env_content += "# GROQ_API_KEY=gsk_sua_key_aqui\n"
        
        env_content += f"""

# ================================
# OPENAI API (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://platform.openai.com/docs
# Rate Limit: Varia conforme plano
# Modelos: gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o

# OPENAI_API_KEY=sk-proj-sua_chave_openai_aqui
# OPENAI_DEFAULT_MODEL=gpt-3.5-turbo
# OPENAI_TEMPERATURE=0.7
# OPENAI_MAX_TOKENS=1000

# ================================
# ANTHROPIC CLAUDE API (TEMPLATE PRONTO)
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
# GOOGLE GEMINI API (TEMPLATE PRONTO)
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
# HUGGING FACE API (TEMPLATE PRONTO)
# ================================
# Para ativar: descomente as linhas abaixo e configure sua chave
# Documentação: https://huggingface.co/docs/api-inference/

# HUGGINGFACE_API_KEY=hf_sua_chave_huggingface_aqui
# HUGGINGFACE_DEFAULT_MODEL=microsoft/DialoGPT-medium
# HUGGINGFACE_TEMPERATURE=0.7
# HUGGINGFACE_MAX_TOKENS=1000

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
CRIATIVIDADE={settings['temperature']}
MAX_TOKENS={settings['max_tokens']}

# ================================
# CONFIGURAÇÕES GLOBAIS
# ================================
# Configurações que se aplicam a todos os providers

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
# - Mantenha suas API keys seguras
# - Nunca compartilhe suas chaves publicamente

# ================================
# RECURSOS E DOCUMENTAÇÃO
# ================================
# Links úteis para cada provider:
#
# Groq (Ativo): https://console.groq.com/
# OpenAI: https://platform.openai.com/
# Anthropic: https://console.anthropic.com/
# Google AI: https://ai.google.dev/
# Cohere: https://dashboard.cohere.ai/
# Azure OpenAI: https://azure.microsoft.com/services/cognitive-services/openai-service/
# Hugging Face: https://huggingface.co/inference-api
#
# Para adicionar novos providers:
# 1. Crie src/providers/nome_provider.py
# 2. Implemente a interface ILLMProvider
# 3. Adicione ao src/providers/__init__.py
# 4. Configure as variáveis de ambiente acima
# 5. Execute: streamlit run app.py

# ================================
# EXEMPLO DE CONFIGURAÇÃO RÁPIDA
# ================================
# Para ativar OpenAI rapidamente:
# 1. Descomente a linha OPENAI_API_KEY acima
# 2. Cole sua chave da OpenAI
# 3. Salve este arquivo
# 4. Execute: streamlit run app.py
# 5. OpenAI aparecerá automaticamente na interface
"""
        
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
        
        if create_env_file(groq_key, settings):
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