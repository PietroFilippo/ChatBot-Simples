"""
Funções auxiliares e utilitários para o sistema.
"""

import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import re
import os

def measure_execution_time(func):
    """Decorator para medir tempo de execução de funções"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = round(end_time - start_time, 3)
        
        # Adiciona informação de tempo ao resultado se for dict
        if isinstance(result, dict) and "error" not in result:
            result["execution_time"] = execution_time
        
        return result
    return wrapper

def format_text_for_display(text: str, max_length: int = 500) -> str:
    """
    Formata texto para exibição, truncando se necessário
    
    Args:
        text: Texto para formatar
        max_length: Comprimento máximo
        
    Returns:
        Texto formatado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def clean_text(text: str) -> str:
    """
    Limpa e normaliza texto para processamento
    
    Args:
        text: Texto para limpar
        
    Returns:
        Texto limpo
    """
    # Remove os caracteres especiais excessivos
    text = re.sub(r'\s+', ' ', text)  # Múltiplos espaços
    text = re.sub(r'\n+', '\n', text)  # Múltiplas quebras de linha
    
    # Remove os espaços no início e fim
    text = text.strip()
    
    return text

