"""
Módulo de provedores extensível e refatorado.
Implementa o Open/Closed Principle com BaseProvider para eliminar duplicação.
"""

from .base_provider import BaseProvider
from .groq_provider import GroqProvider
from .huggingface_provider import HuggingFaceProvider

__all__ = ['BaseProvider', 'GroqProvider', 'HuggingFaceProvider'] 