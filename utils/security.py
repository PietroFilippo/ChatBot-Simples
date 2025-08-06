"""
Módulo de segurança para sanitização de HTML e prevenção de XSS.
"""

import html
import re
from typing import Dict, Any, Optional
from src.config import GlobalConfig

logger = GlobalConfig.get_logger('security')


def sanitize_html_content(content: str, allow_basic_formatting: bool = True) -> str:
    """
    Sanitiza conteúdo HTML para prevenir XSS.
    
    Args:
        content: Conteúdo para sanitizar
        allow_basic_formatting: Se deve permitir formatação básica segura
        
    Returns:
        Conteúdo sanitizado
    """
    if not content:
        return ""
    
    # Primeiro, remove scripts e event handlers ANTES do escape
    sanitized = content
    
    # Remove scripts inline potenciais
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove event handlers potenciais (onclick, onerror, etc.)
    sanitized = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\s*on\w+\s*=\s*[^>\s]*', '', sanitized, flags=re.IGNORECASE)
    
    # Remove javascript: URLs
    sanitized = re.sub(r'javascript\s*:', '', sanitized, flags=re.IGNORECASE)
    
    # Remove outros atributos perigosos
    dangerous_attrs = ['onload', 'onerror', 'onmouseover', 'onmouseout', 'onfocus', 'onblur']
    for attr in dangerous_attrs:
        sanitized = re.sub(f'\\s*{attr}\\s*=\\s*[^>\\s]*', '', sanitized, flags=re.IGNORECASE)
    
    # Agora faz escape básico de HTML
    sanitized = html.escape(sanitized)
    
    if allow_basic_formatting:
        # Permite apenas tags seguras básicas
        safe_tags = {
            '&lt;b&gt;': '<b>',
            '&lt;/b&gt;': '</b>',
            '&lt;i&gt;': '<i>',
            '&lt;/i&gt;': '</i>',
            '&lt;strong&gt;': '<strong>',
            '&lt;/strong&gt;': '</strong>',
            '&lt;em&gt;': '<em>',
            '&lt;/em&gt;': '</em>',
            '&lt;br&gt;': '<br>',
            '&lt;br/&gt;': '<br/>',
        }
        
        for escaped, safe in safe_tags.items():
            sanitized = sanitized.replace(escaped, safe)
    
    logger.debug(f"Conteúdo sanitizado: {len(content)} -> {len(sanitized)} chars")
    return sanitized


def sanitize_user_input(user_input: str) -> str:
    """
    Sanitiza entrada do usuário removendo caracteres potencialmente perigosos.
    
    Args:
        user_input: Entrada do usuário
        
    Returns:
        Entrada sanitizada
    """
    if not user_input:
        return ""
    
    # Remove caracteres de controle perigosos
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', user_input)
    
    # Remove scripts inline potenciais
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove event handlers potenciais
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
    
    # Remove javascript: URLs
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    
    # Limita tamanho para prevenir ataques de DoS
    max_length = 50000  # 50KB
    if len(sanitized) > max_length:
        logger.warning(f"Input muito longo truncado: {len(sanitized)} -> {max_length}")
        sanitized = sanitized[:max_length]
    
    logger.debug(f"Input do usuário sanitizado: {len(user_input)} -> {len(sanitized)} chars")
    return sanitized.strip()


def create_safe_html(template: str, **kwargs) -> str:
    """
    Cria HTML seguro substituindo placeholders por valores sanitizados.
    
    Args:
        template: Template HTML com placeholders
        **kwargs: Valores para substituir (serão sanitizados automaticamente)
        
    Returns:
        HTML seguro
    """
    safe_values = {}
    
    for key, value in kwargs.items():
        if isinstance(value, str):
            safe_values[key] = sanitize_html_content(value, allow_basic_formatting=True)
        else:
            safe_values[key] = html.escape(str(value))
    
    try:
        result = template.format(**safe_values)
        logger.debug(f"HTML seguro criado: {len(template)} chars template")
        return result
    except KeyError as e:
        logger.error(f"Placeholder não encontrado no template: {e}")
        return html.escape(template)


def validate_and_sanitize_text(text: str, min_length: int = 1, max_length: int = 10000) -> Dict[str, Any]:
    """
    Valida e sanitiza texto de entrada.
    
    Args:
        text: Texto para validar
        min_length: Comprimento mínimo
        max_length: Comprimento máximo
        
    Returns:
        Resultado da validação com texto sanitizado
    """
    if not text or not text.strip():
        return {
            "valid": False,
            "error": "Texto não pode estar vazio",
            "sanitized_text": ""
        }
    
    # Sanitiza primeiro
    sanitized = sanitize_user_input(text)
    
    # Valida após sanitização
    if len(sanitized) < min_length:
        return {
            "valid": False,
            "error": f"Texto muito curto (mínimo {min_length} caracteres)",
            "sanitized_text": sanitized
        }
    
    if len(sanitized) > max_length:
        return {
            "valid": False,
            "error": f"Texto muito longo (máximo {max_length} caracteres)",
            "sanitized_text": sanitized[:max_length]
        }
    
    logger.info(f"Texto validado e sanitizado com sucesso: {len(text)} -> {len(sanitized)} chars")
    
    return {
        "valid": True,
        "sanitized_text": sanitized,
        "original_length": len(text),
        "sanitized_length": len(sanitized)
    }


def safe_streamlit_markdown(content: str, allow_html: bool = False) -> str:
    """
    Prepara conteúdo para uso seguro com st.markdown.
    
    Args:
        content: Conteúdo para exibir
        allow_html: Se deve permitir HTML (com sanitização)
        
    Returns:
        Conteúdo seguro para st.markdown
    """
    if not content:
        return ""
    
    if allow_html:
        # Sanitiza mas permite formatação básica
        safe_content = sanitize_html_content(content, allow_basic_formatting=True)
        logger.debug("Conteúdo preparado para st.markdown com HTML sanitizado")
        return safe_content
    else:
        # Escape completo
        safe_content = html.escape(content)
        logger.debug("Conteúdo preparado para st.markdown com escape completo")
        return safe_content


# Rate limiting simples para prevenir spam
class SimpleRateLimiter:
    """Rate limiter simples baseado em memória."""
    
    def __init__(self):
        self.requests = {}
        self.logger = GlobalConfig.get_logger('rate_limiter')
    
    def is_allowed(self, identifier: str, max_requests: int = 60, window_seconds: int = 60) -> bool:
        """
        Verifica se uma requisição é permitida.
        
        Args:
            identifier: Identificador único (IP, user_id, etc.)
            max_requests: Máximo de requisições no período
            window_seconds: Janela de tempo em segundos
            
        Returns:
            True se permitido, False caso contrário
        """
        import time
        
        now = time.time()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove requisições antigas
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < window_seconds
        ]
        
        # Verifica limite
        if len(self.requests[identifier]) >= max_requests:
            self.logger.warning(f"Rate limit excedido para {identifier}: {len(self.requests[identifier])} requisições")
            return False
        
        # Adiciona requisição atual
        self.requests[identifier].append(now)
        return True


# Instância global do rate limiter
rate_limiter = SimpleRateLimiter() 