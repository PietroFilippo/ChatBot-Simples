"""
Gerenciador de Contexto Inteligente para LLMs.
Sistema adaptativo que otimiza o uso do contexto baseado na capacidade real dos modelos.
"""

import tiktoken
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import json

@dataclass
class ModelContextLimits:
    """Configurações de contexto específicas por modelo."""
    max_context_tokens: int
    max_output_tokens: int
    reserved_tokens: int = 200  # Reservado para prompts de sistema
    
    @property
    def available_tokens(self) -> int:
        """Tokens disponíveis para histórico após reservas."""
        return self.max_context_tokens - self.max_output_tokens - self.reserved_tokens

@dataclass
class ConversationEntry:
    """Entrada individual da conversa com metadados."""
    timestamp: datetime
    role: str  # 'user' ou 'assistant'
    content: str
    tokens: int
    importance_score: float = 1.0  # Para priorização inteligente
    provider: str = ""

class TokenCounter(ABC):
    """Interface abstrata para contagem de tokens."""
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Conta tokens em um texto."""
        pass

class TikTokenCounter(TokenCounter):
    """Contador de tokens usando tiktoken (mais preciso)."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback para encoding padrão se modelo não for reconhecido
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Conta tokens usando tiktoken."""
        return len(self.encoding.encode(text))

class ApproximateTokenCounter(TokenCounter):
    """Contador aproximado baseado em heurísticas (fallback)."""
    
    def count_tokens(self, text: str) -> int:
        """Aproximação: ~4 chars = 1 token para texto em português."""
        return max(1, len(text) // 4)

class IntelligentContextManager:
    """
    Gerenciador de contexto inteligente que adapta dinamicamente
    o contexto baseado na capacidade real dos modelos.
    """
    
    # Configurações específicas por modelo
    MODEL_LIMITS = {
        # Groq Models
        "llama3-70b-8192": ModelContextLimits(8192, 1000, 200),
        "llama3-8b-8192": ModelContextLimits(8192, 1000, 200),
        "gemma2-9b-it": ModelContextLimits(8192, 1000, 200),
        
        # HuggingFace Models  
        "google/gemma-2-2b-it": ModelContextLimits(8192, 1000, 200),
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": ModelContextLimits(32768, 2000, 500),
        "microsoft/phi-4": ModelContextLimits(16384, 1500, 300),
        "Qwen/Qwen2.5-Coder-32B-Instruct": ModelContextLimits(32768, 2000, 500),
        "deepseek-ai/DeepSeek-R1": ModelContextLimits(131072, 4000, 1000),
        
        # Fallback padrão
        "default": ModelContextLimits(4096, 1000, 200)
    }
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.conversation_history: List[ConversationEntry] = []
        self.system_prompt = ""
        
        # Inicializa contador de tokens
        self.token_counter = self._initialize_token_counter()
        
        # Obtém limites do modelo
        self.limits = self.MODEL_LIMITS.get(model_name, self.MODEL_LIMITS["default"])
    
    def _initialize_token_counter(self) -> TokenCounter:
        """Inicializa o contador de tokens mais apropriado."""
        try:
            return TikTokenCounter(self.model_name)
        except Exception:
            # Fallback para contador aproximado
            return ApproximateTokenCounter()
    
    def set_system_prompt(self, prompt: str) -> None:
        """Define o prompt de sistema."""
        self.system_prompt = prompt
    
    def add_message(self, role: str, content: str, provider: str = "") -> None:
        """
        Adiciona uma mensagem ao histórico com contagem automática de tokens.
        
        Args:
            role: 'user' ou 'assistant'
            content: Conteúdo da mensagem
            provider: Nome do provider que gerou a resposta (se aplicável)
        """
        tokens = self.token_counter.count_tokens(content)
        importance_score = self._calculate_importance_score(role, content, tokens)
        
        entry = ConversationEntry(
            timestamp=datetime.now(),
            role=role,
            content=content,
            tokens=tokens,
            importance_score=importance_score,
            provider=provider
        )
        
        self.conversation_history.append(entry)
        
        # Otimiza contexto automaticamente após adicionar
        self._optimize_context()
    
    def _calculate_importance_score(self, role: str, content: str, tokens: int) -> float:
        """
        Calcula score de importância para priorização inteligente.
        
        Fatores considerados:
        - Mensagens do usuário são mais importantes (1.2x)
        - Mensagens recentes são mais importantes
        - Mensagens muito curtas ou muito longas podem ser menos importantes
        - Perguntas têm maior importância
        """
        base_score = 1.0
        
        # Bonus para mensagens do usuário
        if role == "user":
            base_score *= 1.2
        
        # Bonus para perguntas
        if "?" in content:
            base_score *= 1.1
        
        # Penalidade para mensagens muito curtas (provavelmente menos informativas)
        if tokens < 5:
            base_score *= 0.8
        
        # Penalidade para mensagens extremamente longas (podem ser verbosas)
        if tokens > 500:
            base_score *= 0.9
        
        return base_score
    
    def _optimize_context(self) -> None:
        """
        Otimiza o contexto removendo mensagens menos importantes
        quando necessário para manter dentro dos limites.
        """
        if not self.conversation_history:
            return
        
        current_tokens = self._calculate_total_tokens()
        available_tokens = self.limits.available_tokens
        
        if current_tokens <= available_tokens:
            return  # Contexto já está dentro dos limites
        
        # Estratégia híbrida: mantém as mais recentes + mais importantes
        self._apply_hybrid_pruning_strategy(available_tokens)
    
    def _calculate_total_tokens(self) -> int:
        """Calcula o total de tokens no contexto atual."""
        system_tokens = self.token_counter.count_tokens(self.system_prompt) if self.system_prompt else 0
        history_tokens = sum(entry.tokens for entry in self.conversation_history)
        return system_tokens + history_tokens
    
    def _apply_hybrid_pruning_strategy(self, target_tokens: int) -> None:
        """
        Aplica estratégia híbrida de poda:
        1. Sempre mantém as 2 mensagens mais recentes
        2. Remove mensagens antigas com menor score de importância
        3. Preserva pares pergunta-resposta quando possível
        """
        if len(self.conversation_history) <= 2:
            return  # Muito poucas mensagens para podar
        
        # Sempre preserva as 2 mensagens mais recentes
        protected_count = 2
        protected_entries = self.conversation_history[-protected_count:]
        candidate_entries = self.conversation_history[:-protected_count]
        
        # Ordena candidatos por importância (decrescente)
        candidate_entries.sort(key=lambda x: x.importance_score, reverse=True)
        
        # Constrói novo histórico mantendo os protegidos
        new_history = []
        current_tokens = sum(entry.tokens for entry in protected_entries)
        
        # Adiciona prompt de sistema aos tokens
        if self.system_prompt:
            current_tokens += self.token_counter.count_tokens(self.system_prompt)
        
        # Adiciona candidatos em ordem de importância até atingir o limite
        for entry in candidate_entries:
            if current_tokens + entry.tokens <= target_tokens:
                new_history.append(entry)
                current_tokens += entry.tokens
            else:
                break
        
        # Reconstrói histórico: candidatos selecionados + protegidos (em ordem cronológica)
        new_history.sort(key=lambda x: x.timestamp)
        new_history.extend(protected_entries)
        
        self.conversation_history = new_history
    
    def get_context_for_model(self) -> str:
        """
        Retorna o contexto formatado para envio ao modelo.
        
        Returns:
            String formatada com o contexto completo
        """
        context_parts = []
        
        # Adiciona prompt de sistema se existir
        if self.system_prompt:
            context_parts.append(f"Sistema: {self.system_prompt}")
        
        # Adiciona histórico da conversa
        if self.conversation_history:
            context_parts.append("\nContexto da conversa:")
            for entry in self.conversation_history:
                role_name = "Usuário" if entry.role == "user" else "Assistente"
                context_parts.append(f"{role_name}: {entry.content}")
        
        return "\n".join(context_parts)
    
    def get_context_messages(self) -> List[Dict[str, str]]:
        """
        Retorna o contexto no formato de mensagens para APIs que suportam.
        
        Returns:
            Lista de dicionários com role/content
        """
        messages = []
        
        # Adiciona prompt de sistema se existir
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Adiciona histórico da conversa
        for entry in self.conversation_history:
            messages.append({
                "role": entry.role,
                "content": entry.content
            })
        
        return messages
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas do contexto.
        
        Returns:
            Dicionário com métricas e informações
        """
        total_tokens = self._calculate_total_tokens()
        available_tokens = self.limits.available_tokens
        
        return {
            "model_name": self.model_name,
            "total_messages": len(self.conversation_history),
            "total_tokens": total_tokens,
            "available_tokens": available_tokens,
            "utilization_percentage": (total_tokens / available_tokens * 100) if available_tokens > 0 else 0,
            "system_prompt_tokens": self.token_counter.count_tokens(self.system_prompt) if self.system_prompt else 0,
            "max_context_tokens": self.limits.max_context_tokens,
            "max_output_tokens": self.limits.max_output_tokens,
        }
    
    def clear_context(self) -> None:
        """Limpa todo o contexto mantendo configurações."""
        self.conversation_history.clear()

    
    def update_model(self, new_model_name: str) -> None:
        """
        Atualiza o modelo e reotimiza o contexto para os novos limites.
        
        Args:
            new_model_name: Nome do novo modelo
        """
        old_model = self.model_name
        self.model_name = new_model_name
        
        # Atualiza limites e contador de tokens
        self.limits = self.MODEL_LIMITS.get(new_model_name, self.MODEL_LIMITS["default"])
        self.token_counter = self._initialize_token_counter()
        
        # Recalcula tokens de todas as mensagens com novo contador
        for entry in self.conversation_history:
            entry.tokens = self.token_counter.count_tokens(entry.content)
        
        # Reotimiza contexto para novos limites
        self._optimize_context()
        
        print(f"Contexto otimizado para {new_model_name} (era {old_model})")
        
        # Mostra estatísticas da migração
        stats = self.get_stats()
        print(f"Utilização atual: {stats['utilization_percentage']:.1f}% ({stats['total_tokens']}/{stats['available_tokens']} tokens)") 