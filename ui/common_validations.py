"""
Validações comuns centralizadas para eliminar repetição.
"""

import streamlit as st
from typing import Dict, Any, Optional


def validate_and_show_provider_status(provider_registry) -> bool:
    """
    Valida se há provider disponível e mostra mensagens apropriadas.
    
    Args:
        provider_registry: Registro de providers
        
    Returns:
        True se há provider disponível, False caso contrário
    """
    # Verifica se há providers disponíveis
    available_providers = provider_registry.get_available_providers()
    
    if not available_providers:
        _show_no_provider_error()
        return False
    
    return True


def _show_no_provider_error():
    """Mostra erro padrão quando não há provider configurado."""
    st.error("**Nenhuma API configurada**")
    
    # Expander com instruções detalhadas
    with st.expander("📋 Como configurar uma API", expanded=True):
        st.markdown("""
        ### Opção 1: Configuração Automática (Recomendado)
        ```bash
        python setup_env.py
        ```
        
        ### Opção 2: Configuração Manual
        
        #### Groq (Gratuito)
        1. Acesse [console.groq.com](https://console.groq.com/)
        2. Crie uma conta gratuita
        3. Gere uma API key
        4. Adicione no arquivo `.env`:
        ```
        GROQ_API_KEY=sua_chave_aqui
        ```
        
        #### Hugging Face (Gratuito)
        1. Acesse [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        2. Crie um token gratuito
        3. Adicione no arquivo `.env`:
        ```
        HUGGINGFACE_API_KEY=seu_token_aqui
        ```
        
        ### Reinicie a aplicação
        Após configurar, reinicie o Streamlit para aplicar as mudanças.
        """)
    
    # Informações adicionais
    st.info("💡 APIs suportadas: **Groq** (gratuita) e **Hugging Face** (gratuita)")


def show_feature_unavailable(feature_name: str):
    """
    Mostra mensagem padrão quando feature não está disponível.
    
    Args:
        feature_name: Nome da funcionalidade
    """
    st.warning(f"⚠️ **{feature_name}** não disponível")
    st.info("Configure uma API para usar esta funcionalidade.")


def validate_text_input(text: str, min_length: int = 10, context: str = "texto") -> Dict[str, Any]:
    """
    Valida entrada de texto com regras comuns.
    
    Args:
        text: Texto para validar
        min_length: Comprimento mínimo
        context: Contexto da validação (para mensagens)
        
    Returns:
        Dict com resultado da validação
    """
    if not text or not text.strip():
        return {
            "valid": False,
            "error": f"Por favor, insira um {context}.",
            "type": "empty"
        }
    
    if len(text.strip()) < min_length:
        return {
            "valid": False,
            "error": f"{context.capitalize()} deve ter pelo menos {min_length} caracteres.",
            "type": "too_short"
        }
    
    return {
        "valid": True,
        "text": text.strip()
    }


def show_loading_message(message: str = "Processando..."):
    """Mostra mensagem de loading padronizada."""
    return st.empty().info(f"⏳ {message}")


def clear_loading_message(placeholder):
    """Remove mensagem de loading."""
    if placeholder:
        placeholder.empty() 