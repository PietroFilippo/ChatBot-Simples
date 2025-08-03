"""
Módulo de provedores extensível.
Implementa o Open/Closed Principle.
"""

from .groq_provider import GroqProvider
from .huggingface_provider import HuggingFaceProvider

__all__ = ['GroqProvider', 'HuggingFaceProvider'] 