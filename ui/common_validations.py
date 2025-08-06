"""
Validações comuns centralizadas para eliminar duplicação.
Agora com segurança aprimorada e logging estruturado.
"""

import streamlit as st
from typing import Dict, Any
from src.config import GlobalConfig
from utils.security import validate_and_sanitize_text, rate_limiter

logger = GlobalConfig.get_logger('validations')


def validate_and_show_provider_status(provider_registry) -> bool:
    """
    Valida se há provedores disponíveis e mostra status.
    
    Args:
        provider_registry: Registro de provedores
        
    Returns:
        True se há provedores disponíveis
    """
    try:
        if not provider_registry.is_any_provider_available():
            logger.warning("Nenhum provedor LLM disponível")
            st.error("**⚠️ Nenhuma API configurada**")
            st.info("""
            Para usar este recurso, você precisa configurar pelo menos uma API:
            
            **Opção 1 - Setup Automatizado:**
        ```bash
        python setup_env.py
        ```
        
            **Opção 2 - Manual:**
            1. Acesse [console.groq.com](https://console.groq.com/) ou [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        2. Crie uma conta gratuita
        3. Gere uma API key
            4. Configure no arquivo `.env`
            """)
            return False
        
        current_provider = provider_registry.get_current_provider()
        if current_provider:
            logger.info(f"Provedor ativo validado: {current_provider.get_name()}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao validar status do provedor: {e}")
        st.error("Erro interno ao validar provedores")
        return False


def validate_text_input(text: str, min_length: int = 10, max_length: int = 10000) -> Dict[str, Any]:
    """
    Valida entrada de texto com sanitização de segurança.
    
    Args:
        text: Texto para validar
        min_length: Comprimento mínimo
        max_length: Comprimento máximo
        
    Returns:
        Resultado da validação
    """
    try:
        # Aplica rate limiting básico baseado no hash do texto
        text_hash = str(hash(text[:100]))  # Usa apenas os primeiros 100 chars para o hash
        
        if not rate_limiter.is_allowed(f"text_input_{text_hash}", max_requests=30, window_seconds=60):
            logger.warning(f"Rate limit excedido para validação de texto")
            return {
                "valid": False,
                "error": "Muitas requisições. Aguarde um momento antes de tentar novamente.",
                "text": ""
            }
        
        # Usa a validação segura
        result = validate_and_sanitize_text(text, min_length, max_length)
        
        if result["valid"]:
            logger.info(f"Texto validado com sucesso: {result['sanitized_length']} chars")
            return {
                "valid": True,
                "text": result["sanitized_text"]
            }
        else:
            logger.warning(f"Texto inválido: {result['error']}")
            return {
                "valid": False,
                "error": result["error"],
                "text": result.get("sanitized_text", "")
            }
            
    except Exception as e:
        logger.error(f"Erro ao validar texto: {e}")
        return {
            "valid": False,
            "error": "Erro interno na validação do texto",
            "text": ""
        }


def show_feature_unavailable(feature_name: str):
    """
    Mostra mensagem de recurso indisponível.
    
    Args:
        feature_name: Nome do recurso
    """
    logger.info(f"Recurso indisponível mostrado: {feature_name}")
    
    feature_messages = {
        "chatbot": "💬 Chatbot",
        "sentiment": "😀 Análise de Sentimentos", 
        "summarizer": "📝 Gerador de Resumos"
    }
    
    feature_display = feature_messages.get(feature_name, feature_name)
    
    st.warning(f"**{feature_display} temporariamente indisponível**")
    st.info("""
    **Para ativar este recurso:**
    
    1. **Configure uma API gratuita:**
       - Execute: `python setup_env.py`
       - Ou configure manualmente no arquivo `.env`
    
    2. **APIs gratuitas disponíveis:**
       - [Groq](https://console.groq.com/) - Ultra rápido
       - [Hugging Face](https://huggingface.co/settings/tokens) - 90+ modelos
    
    3. **Reinicie a aplicação após configurar**
    """)


def validate_api_response(response: str, provider_name: str = "API", provider_instance=None) -> Dict[str, Any]:
    """
    Valida resposta da API e detecta erros comuns.
    Agora incrementa contador de erros do provedor quando necessário.
    
    Args:
        response: Resposta da API
        provider_name: Nome do provedor
        provider_instance: Instância do provedor (para incrementar contador de erros)
        
    Returns:
        Resultado da validação
    """
    try:
        if not response:
            logger.warning(f"Resposta vazia recebida de {provider_name}")
            if provider_instance and hasattr(provider_instance, 'increment_validation_error'):
                provider_instance.increment_validation_error("empty_response")
            return {
                "valid": False,
                "error": f"Resposta vazia de {provider_name}"
            }
        
        # Verifica se é uma mensagem de erro
        error_indicators = [
            "❌", "erro", "error", "failed", "falhou", 
            "unauthorized", "forbidden", "rate limit",
            "quota exceeded", "timeout"
        ]
        
        response_lower = response.lower()
        for indicator in error_indicators:
            if indicator in response_lower:
                logger.error(f"Erro detectado na resposta de {provider_name}: {indicator}")
                if provider_instance and hasattr(provider_instance, 'increment_validation_error'):
                    provider_instance.increment_validation_error("content_error")
                return {
                    "valid": False,
                    "error": f"Erro em {provider_name}: {response[:100]}..."
                }
        
        # Valida tamanho da resposta
        if len(response) > 50000:  # 50KB
            logger.warning(f"Resposta muito longa de {provider_name}: {len(response)} chars")
            response = response[:50000] + "... [truncado]"
        
        logger.info(f"Resposta válida recebida de {provider_name}: {len(response)} chars")
        
        return {
            "valid": True,
            "response": response
        }
    
    except Exception as e:
        logger.error(f"Erro ao validar resposta de {provider_name}: {e}")
        if provider_instance and hasattr(provider_instance, 'increment_validation_error'):
            provider_instance.increment_validation_error("validation_exception")
        return {
            "valid": False,
            "error": f"Erro interno ao processar resposta de {provider_name}"
        }


def validate_file_upload(uploaded_file, max_size_mb: int = 10, allowed_types: list = None) -> Dict[str, Any]:
    """
    Valida arquivo enviado pelo usuário.
    
    Args:
        uploaded_file: Arquivo do Streamlit
        max_size_mb: Tamanho máximo em MB
        allowed_types: Tipos de arquivo permitidos
        
    Returns:
        Resultado da validação
    """
    if allowed_types is None:
        allowed_types = ['txt', 'pdf', 'docx', 'md']
    
    try:
        if uploaded_file is None:
            return {
                "valid": False,
                "error": "Nenhum arquivo selecionado"
            }
        
        # Verifica tamanho
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            logger.warning(f"Arquivo muito grande: {file_size_mb:.1f}MB > {max_size_mb}MB")
            return {
                "valid": False,
                "error": f"Arquivo muito grande ({file_size_mb:.1f}MB). Máximo: {max_size_mb}MB"
            }
        
        # Verifica tipo
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in allowed_types:
            logger.warning(f"Tipo de arquivo não permitido: {file_extension}")
            return {
                "valid": False,
                "error": f"Tipo de arquivo não suportado: .{file_extension}. Permitidos: {', '.join(allowed_types)}"
            }
        
        logger.info(f"Arquivo válido: {uploaded_file.name} ({file_size_mb:.1f}MB)")
        
        return {
            "valid": True,
            "file": uploaded_file,
            "size_mb": file_size_mb,
            "type": file_extension
        }
        
    except Exception as e:
        logger.error(f"Erro ao validar arquivo: {e}")
        return {
            "valid": False,
            "error": "Erro interno ao validar arquivo"
        } 