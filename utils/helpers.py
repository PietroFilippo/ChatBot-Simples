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

def extract_keywords(text: str, top_k: int = 10) -> List[str]:
    """
    Extrai palavras-chave simples de um texto
    
    Args:
        text: Texto para análise
        top_k: Número de palavras-chave para retornar
        
    Returns:
        Lista de palavras-chave
    """
    # Palavras comuns para ignorar
    stopwords = {
        'de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
        'e', 'ou', 'mas', 'se', 'que', 'para', 'com', 'por', 'em', 'na', 'no', 'nas', 'nos',
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'that', 'for', 'with', 'by', 'in', 'on'
    }
    
    # Extrai as palavras
    words = re.findall(r'\b[a-záàâãéêíóôõúç]{3,}\b', text.lower())
    
    # Conta a frequência, ignorando as stopwords
    word_freq = {}
    for word in words:
        if word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Ordena por frequência
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, freq in sorted_words[:top_k]]

def calculate_text_stats(text: str) -> Dict[str, Any]:
    """
    Calcula estatísticas básicas de um texto
    
    Args:
        text: Texto para análise
        
    Returns:
        Dicionário com estatísticas
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return {
        "characters": len(text),
        "characters_no_spaces": len(text.replace(' ', '')),
        "words": len(words),
        "sentences": len(sentences),
        "paragraphs": len([p for p in text.split('\n\n') if p.strip()]),
        "avg_words_per_sentence": round(len(words) / len(sentences), 1) if sentences else 0,
        "avg_chars_per_word": round(len(text.replace(' ', '')) / len(words), 1) if words else 0
    }

def generate_text_hash(text: str) -> str:
    """
    Gera hash único para um texto
    
    Args:
        text: Texto para hash
        
    Returns:
        Hash MD5 do texto
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def save_to_cache(key: str, data: Any, cache_dir: str = "cache") -> bool:
    """
    Salva dados em cache local
    
    Args:
        key: Chave única para os dados
        data: Dados para salvar
        cache_dir: Diretório do cache
        
    Returns:
        Sucesso da operação
    """
    try:
        # Cria o diretório se não existir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Arquivo do cache
        cache_file = os.path.join(cache_dir, f"{key}.json")
        
        # Salvar com timestamp
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao salvar cache: {e}")
        return False

def load_from_cache(key: str, cache_dir: str = "cache", max_age_hours: int = 24) -> Optional[Any]:
    """
    Carrega dados do cache local.
    
    Args:
        key: Chave única dos dados
        cache_dir: Diretório do cache
        max_age_hours: Idade máxima do cache em horas
        
    Returns:
        Dados do cache ou None se não encontrado/expirado
    """
    try:
        cache_file = os.path.join(cache_dir, f"{key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # Verifica a idade do cache
        timestamp = datetime.fromisoformat(cache_data["timestamp"])
        max_age = timedelta(hours=max_age_hours)
        
        if datetime.now() - timestamp > max_age:
            # Cache expirado
            os.remove(cache_file)
            return None
        
        return cache_data["data"]
    
    except Exception as e:
        print(f"Erro ao carregar cache: {e}")
        return None

def format_duration(seconds: float) -> str:
    """
    Formata duração em formato legível.
    
    Args:
        seconds: Duração em segundos
        
    Returns:
        String formatada
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"

def validate_text_input(text: str, min_length: int = 10, max_length: int = 10000) -> Dict[str, Any]:
    """
    Valida entrada de texto.
    
    Args:
        text: Texto para validar
        min_length: Comprimento mínimo
        max_length: Comprimento máximo
        
    Returns:
        Resultado da validação
    """
    if not text or not text.strip():
        return {"valid": False, "error": "Texto não pode estar vazio"}
    
    text = text.strip()
    
    if len(text) < min_length:
        return {"valid": False, "error": f"Texto muito curto (mínimo {min_length} caracteres)"}
    
    if len(text) > max_length:
        return {"valid": False, "error": f"Texto muito longo (máximo {max_length} caracteres)"}
    
    return {"valid": True, "text": text}

def create_download_link(data: Union[str, Dict], filename: str, file_type: str = "json") -> str:
    """
    Cria link de download para dados.
    
    Args:
        data: Dados para download
        filename: Nome do arquivo
        file_type: Tipo do arquivo
        
    Returns:
        String com dados codificados para download
    """
    if file_type == "json":
        if isinstance(data, dict):
            content = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            content = str(data)
    else:
        content = str(data)
    
    import base64
    b64 = base64.b64encode(content.encode()).decode()
    
    return f"data:application/{file_type};base64,{b64}"

def get_emoji_for_sentiment(sentiment: str) -> str:
    """
    Retorna emoji correspondente ao sentimento.
    
    Args:
        sentiment: Sentimento (positivo/negativo/neutro)
        
    Returns:
        Emoji correspondente
    """
    emoji_map = {
        "positivo": "😊",
        "negativo": "😞", 
        "neutro": "😐",
        "positive": "😊",
        "negative": "😞",
        "neutral": "😐"
    }
    
    return emoji_map.get(sentiment.lower(), "❓")

def format_confidence_display(confidence: float) -> str:
    """
    Formata confiança para exibição.
    
    Args:
        confidence: Valor de confiança (0-1)
        
    Returns:
        String formatada com porcentagem e barras
    """
    percentage = confidence * 100
    bars = "█" * int(percentage / 10)
    empty_bars = "░" * (10 - int(percentage / 10))
    
    return f"{percentage:.1f}% {bars}{empty_bars}"

def get_system_info() -> Dict[str, Any]:
    """
    Retorna informações do sistema.
    
    Returns:
        Informações do sistema
    """
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "timestamp": datetime.now().isoformat()
    }

# Constantes úteis
COMMON_PHRASES = {
    "greeting": ["olá", "oi", "hello", "hi", "bom dia", "boa tarde", "boa noite"],
    "thanks": ["obrigado", "obrigada", "thanks", "valeu", "muito obrigado"],
    "goodbye": ["tchau", "adeus", "bye", "goodbye", "até logo", "falou"]
}

# Regex patterns úteis
PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "url": r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    "phone": r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}',
    "cpf": r'\d{3}\.\d{3}\.\d{3}-\d{2}'
} 