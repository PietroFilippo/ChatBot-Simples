#!/usr/bin/env python3
"""
    Script para configurar automaticamente a API do Groq
"""

import os
from typing import Optional
from datetime import datetime

def print_header():
    """Exibe cabeçalho do setup."""
    print("Script para configurar automaticamente a API do Groq")

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
        settings["criatividade"] = max(0.0, min(1.0, criatividade))
    except ValueError:
        settings["criatividade"] = 0.7
    
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
    Cria o arquivo .env com as configurações
    
    Args:
        groq_key: Chave da API Groq
        settings: Configurações avançadas
        
    Returns:
        True se criado com sucesso
    """
    try:
        env_content = f"""# Configuração Automática
# Gerado automaticamente em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# ================================
# GROQ API (PRINCIPAL)
# ================================
"""
        
        if groq_key:
            env_content += f"GROQ_API_KEY={groq_key}\n"
        else:
            env_content += "# GROQ_API_KEY=gsk_sua_key_aqui\n"
        
        env_content += f"""
# ================================
# CONFIGURAÇÕES AVANÇADAS
# ================================
DEFAULT_MODEL={settings['model']}
CRIATIVIDADE={settings['criatividade']}
MAX_TOKENS={settings['max_tokens']}

# ================================
# CONFIGURAÇÕES AUTOMÁTICAS
# ================================
# Este arquivo foi gerado pelo setup_env.py
# Para reconfigurar, execute: python setup_env.py
# Não commitar este arquivo no Git (já está no .gitignore)

# ================================
# INFORMAÇÕES ÚTEIS
# ================================
# Groq Console: https://console.groq.com/
# Rate Limit: 30 requests/minuto (gratuito)
# Modelos disponíveis: llama3-70b-8192, llama3-8b-8192
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
    print("1-Instalar dependências:")
    print("   pip install -r requirements.txt")
    print()
    print("2-Executar a interface web:")
    print("   streamlit run app.py")
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
                "criatividade": 0.7,
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