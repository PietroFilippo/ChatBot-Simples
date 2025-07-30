"""
Geração de resumos usando duas estratégias:
- Extrativa (baseada em frequência de palavras)
- LangChain (usando LLMs)
"""

from typing import Dict, Any
from collections import Counter
import re
import nltk
from src.llm_providers import llm_manager

class IntelligentSummarizer:
    """Gerador de resumos com diferentes estratégias"""

    def __init__(self):
        """Inicializa o sumarizador"""
        self.methods = {}
        self._setup_extractive()
        self._setup_langchain()
        print("Sumarizador inteligente inicializado")

    def _setup_extractive(self):
        """Configura sumarização extrativa"""
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

    def _setup_langchain(self):
        """Configura sumarização com LangChain"""
        if llm_manager.get_llm() is not None:
            self.methods["langchain"] = {
                "available": True,
                "speed": "slow",
                "quality": "very_high"
            }
            print("Sumarização LangChain configurada")
        else:
            self.methods["langchain"] = {"available": False}

    def summarize_extractive(self, text: str, num_sentences: int = 3) -> Dict[str, Any]:
        """Sumarização extrativa baseada em frequência de palavras"""
        if not self.methods["extractive"]["available"]:
            return {"error": "Sumarização extrativa não disponível"}

        try:
            sentences = nltk.sent_tokenize(text)
            if len(sentences) <= num_sentences:
                return {"summary": text, "method": "extractive", "compression_ratio": 1.0}

            words = re.findall(r'\w+', text.lower())

            try:
                from nltk.corpus import stopwords
                stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
            except:
                stop_words = {'de', 'da', 'do', 'dos', 'das', 'em', 'na', 'no', 'nos', 'nas', 'para', 'por', 'com', 'sem'}

            words = [word for word in words if word not in stop_words and len(word) > 2]
            word_freq = Counter(words)

            sentence_scores = {
                sentence: sum(word_freq.get(w, 0) for w in re.findall(r'\w+', sentence.lower()))
                for sentence in sentences
            }

            top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
            summary = ' '.join([s for s in sentences if s in top_sentences])

            return {
                "summary": summary,
                "method": "extractive",
                "compression_ratio": len(summary) / len(text)
            }

        except Exception as e:
            return {"error": f"Erro na sumarização extrativa: {e}"}

# Instância global
summarizer = IntelligentSummarizer()
