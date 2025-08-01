"""
Geração de resumos usando múltiplas estratégias:
- Extrativa (baseada em frequência de palavras)
- LangChain (usando LLMs)
"""

from typing import Dict, List, Any, Optional
from collections import Counter
import re
import nltk
from src.llm_providers import llm_manager

class IntelligentSummarizer:
    """Gerador de resumos com múltiplas estratégias."""
    
    def __init__(self):
        """Inicializa o sumarizador."""
        self.methods = {}
        self._setup_extractive()
        self._setup_langchain()
        
        print("Sumarizador inteligente inicializado.")
    
    def _setup_extractive(self):
        """Configura sumarização extrativa."""
        try:
            # Baixar dados do NLTK se necessário
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords', quiet=True)
            
            self.methods["extractive"] = {
                "available": True,
                "speed": "fast",
                "quality": "medium"
            }
            print("Sumarização extrativa configurada")
            
        except Exception as e:
            print(f"⚠️  Sumarização extrativa não disponível: {e}")
            self.methods["extractive"] = {"available": False}
    
    def _setup_langchain(self):
        """Configura sumarização com LangChain."""
        if llm_manager.get_llm() is not None:
            self.methods["langchain"] = {
                "available": True,
                "speed": "slow",
                "quality": "very_high"
            }
            print("LangChain sumarização configurado")
        else:
            self.methods["langchain"] = {"available": False}
    
    def summarize_extractive(self, text: str, num_sentences: int = 3) -> Dict[str, Any]:
        """
        Sumarização extrativa baseada em frequência de palavras.
        
        Args:
            text: Texto para resumir
            num_sentences: Número de frases no resumo
            
        Returns:
            Resultado da sumarização
        """
        if not self.methods["extractive"]["available"]:
            return {"error": "Sumarização extrativa não disponível"}
        
        try:
            # Dividir em frases
            sentences = nltk.sent_tokenize(text)
            
            if len(sentences) <= num_sentences:
                return {
                    "summary": text,
                    "method": "extractive",
                    "compression_ratio": 1.0,
                    "details": {
                        "original_sentences": len(sentences),
                        "summary_sentences": len(sentences),
                        "note": "Texto já é curto o suficiente"
                    }
                }
            
            # Tokenizar palavras e calcular frequência
            words = re.findall(r'\w+', text.lower())
            
            # Filtrar stopwords se disponível
            try:
                from nltk.corpus import stopwords
                stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
                words = [word for word in words if word not in stop_words and len(word) > 2]
            except:
                # Se stopwords não estiver disponível, usar lista básica
                basic_stopwords = {'de', 'da', 'do', 'dos', 'das', 'em', 'na', 'no', 'nos', 'nas', 'para', 'por', 'com', 'sem', 'que', 'se', 'é', 'são', 'foi', 'foram', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
                words = [word for word in words if word not in basic_stopwords and len(word) > 2]
            
            # Calcular frequência das palavras
            word_freq = Counter(words)
            
            # Pontuar frases baseado na frequência das palavras
            sentence_scores = {}
            for sentence in sentences:
                sentence_words = re.findall(r'\w+', sentence.lower())
                score = sum(word_freq.get(word, 0) for word in sentence_words)
                sentence_scores[sentence] = score
            
            # Selecionar as melhores frases
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Ordenar frases na ordem original
            selected_sentences = [sent for sent, score in top_sentences]
            summary_sentences = []
            
            for original_sentence in sentences:
                if original_sentence in selected_sentences:
                    summary_sentences.append(original_sentence)
                    if len(summary_sentences) == num_sentences:
                        break
            
            summary = ' '.join(summary_sentences)
            
            return {
                "summary": summary,
                "method": "extractive",
                "compression_ratio": len(summary) / len(text),
                "details": {
                    "original_sentences": len(sentences),
                    "summary_sentences": len(summary_sentences),
                    "top_words": dict(word_freq.most_common(5)),
                    "sentence_scores": {sent[:50] + "...": score for sent, score in list(sentence_scores.items())[:3]}
                }
            }
            
        except Exception as e:
            return {"error": f"Erro na sumarização extrativa: {e}"}
    
    def summarize_langchain_simple(self, text: str, summary_type: str = "informative") -> Dict[str, Any]:
        """
        Sumarização simples usando LangChain.
        
        Args:
            text: Texto para resumir
            summary_type: Tipo de resumo (informative, executive, creative, technical)
            
        Returns:
            Resultado da sumarização
        """
        if not self.methods["langchain"]["available"]:
            return {"error": "LangChain não disponível"}
        
        try:
            # Definir prompts baseados no tipo
            prompts = {
                "informative": "Faça um resumo informativo e objetivo do texto abaixo, mantendo os pontos principais. Responda SEMPRE na língua que o usuário está falando:",
                "executive": "Faça um resumo executivo conciso do texto abaixo, focando em insights e conclusões. Responda SEMPRE na língua que o usuário está falando:",
                "creative": "Faça um resumo criativo e envolvente do texto abaixo, mantendo o essencial mas com linguagem atrativa. Responda SEMPRE na língua que o usuário está falando:",
                "technical": "Faça um resumo técnico detalhado do texto abaixo, preservando terminologias e conceitos importantes. Responda SEMPRE na língua que o usuário está falando:"
            }
            
            prompt_base = prompts.get(summary_type, prompts["informative"])
            
            prompt = f"""
            {prompt_base}
            
            Texto original:
            {text}
            
            Resumo:
            """
            
            summary = llm_manager.invoke_llm(prompt)
            
            return {
                "summary": summary,
                "method": "langchain_simple",
                "compression_ratio": len(summary) / len(text),
                "summary_type": summary_type,
                "details": {
                    "provider": "groq",
                    "prompt_type": summary_type,
                    "original_length": len(text),
                    "summary_length": len(summary)
                }
            }
            
        except Exception as e:
            return {"error": f"Erro LangChain simples: {e}"}
    
    def summarize_langchain_advanced(self, text: str, summary_type: str = "informative") -> Dict[str, Any]:
        """
        Sumarização avançada usando LangChain com múltiplas etapas.
        
        Args:
            text: Texto para resumir
            summary_type: Tipo de resumo
            
        Returns:
            Resultado da sumarização
        """
        if not self.methods["langchain"]["available"]:
            return {"error": "LangChain não disponível"}
        
        try:
            # Etapa 1: Extrair pontos principais
            extract_prompt = f"""
            Analise o texto abaixo e extraia os 5 pontos principais em formato de lista.
            RESPONDA SEMPRE NA LÍNGUA DO USUÁRIO:
            
            {text}
            
            Pontos principais:
            """
            
            key_points = llm_manager.invoke_llm(extract_prompt)
            
            # Etapa 2: Criar resumo baseado nos pontos
            summary_prompts = {
                "informative": "Baseado nos pontos principais abaixo, crie um resumo informativo e bem estruturado SEMPRE NA LÍNGUA DO USUÁRIO:",
                "executive": "Baseado nos pontos principais abaixo, crie um resumo executivo com foco em decisões e resultados SEMPRE NA LÍNGUA DO USUÁRIO:",
                "creative": "Baseado nos pontos principais abaixo, crie um resumo criativo e cativante SEMPRE NA LÍNGUA DO USUÁRIO:",
                "technical": "Baseado nos pontos principais abaixo, crie um resumo técnico preciso e detalhado SEMPRE NA LÍNGUA DO USUÁRIO:"
            }
            
            summary_prompt = f"""
            {summary_prompts.get(summary_type, summary_prompts["informative"])}
            
            Pontos principais:
            {key_points}
            
            Resumo final:
            """
            
            final_summary = llm_manager.invoke_llm(summary_prompt)
            
            return {
                "summary": final_summary,
                "method": "langchain_advanced",
                "compression_ratio": len(final_summary) / len(text),
                "summary_type": summary_type,
                "details": {
                    "provider": "groq",
                    "key_points": key_points,
                    "steps": ["extract_points", "create_summary"],
                    "original_length": len(text),
                    "summary_length": len(final_summary)
                }
            }
            
        except Exception as e:
            return {"error": f"Erro LangChain avançado: {e}"}
    
    def summarize_comprehensive(self, text: str, num_sentences: int = 3, summary_type: str = "informative") -> Dict[str, Any]:
        """
        Sumarização completa usando todos os métodos disponíveis.
        
        Args:
            text: Texto para resumir
            num_sentences: Número de frases para método extrativo
            summary_type: Tipo de resumo para métodos LangChain
            
        Returns:
            Resultado consolidado
        """
        results = {
            "summaries": {},
            "original_length": len(text),
            "statistics": {}
        }
        
        # Executar cada método disponível
        if self.methods["extractive"]["available"]:
            results["summaries"]["extractive"] = self.summarize_extractive(text, num_sentences)
        
        if self.methods["langchain"]["available"]:
            results["summaries"]["langchain_simple"] = self.summarize_langchain_simple(text, summary_type)
            results["summaries"]["langchain_advanced"] = self.summarize_langchain_advanced(text, summary_type)
        
        # Calcular estatísticas
        results["statistics"] = self._calculate_stats(results["summaries"])
        
        return results
    
    def _calculate_stats(self, summaries: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula estatísticas dos resumos gerados.
        
        Args:
            summaries: Dicionário com resumos de diferentes métodos
            
        Returns:
            Estatísticas consolidadas
        """
        valid_summaries = {
            method: result for method, result in summaries.items()
            if "error" not in result
        }
        
        if not valid_summaries:
            return {
                "successful_methods": 0,
                "average_compression": 0.0,
                "best_method": None
            }
        
        # Calcular compressão média
        compressions = [result["compression_ratio"] for result in valid_summaries.values()]
        avg_compression = sum(compressions) / len(compressions)
        
        # Encontrar melhor método (maior compressão = mais eficiente)
        best_method = max(valid_summaries.keys(), 
                         key=lambda m: valid_summaries[m]["compression_ratio"])
        
        return {
            "successful_methods": len(valid_summaries),
            "average_compression": avg_compression,
            "best_method": best_method,
            "compression_ratios": {method: result["compression_ratio"] 
                                 for method, result in valid_summaries.items()}
        }
    
    def get_available_methods(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna informações sobre métodos disponíveis.
        
        Returns:
            Dicionário com status e capacidades de cada método
        """
        return self.methods.copy()

# Instância global do sumarizador
summarizer = IntelligentSummarizer() 