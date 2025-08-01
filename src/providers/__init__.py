"""
Módulo de provedores extensível.
Implementa o Open/Closed Principle.
"""

from .groq_provider import GroqProvider

__all__ = ['GroqProvider'] 