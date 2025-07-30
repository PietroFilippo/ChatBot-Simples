"""
Análise de sentimentos usando LLM generativo
"""

from typing import Dict, List, Any, Optional
from src.llm_providers import llm_manager
import warnings

# Suprime os warnings
warnings.filterwarnings("ignore")

class SentimentAnalyzer:
    """Analisador de sentimentos com LLM."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.methods = {}
        self._setup_llm()
        
        print("Analisador de sentimentos inicializado.")
    
    def _setup_llm(self):
        """Configura análise com LLM (mais contextual)."""
        if llm_manager.get_llm() is not None:
            self.methods["llm"] = {
                "available": True,
                "speed": "medium",
                "accuracy": "very_high"
            }
            print("LLM configurado para análise")
        else:
            self.methods["llm"] = {"available": False}
    
    def analyze_llm(self, text: str) -> Dict[str, Any]:
        """Análise usando LLM."""
        if not self.methods["llm"]["available"]:
            return {"error": "LLM não disponível"}
        
        try:
            prompt = f"""
            Analise o sentimento do texto abaixo e responda APENAS com um JSON no formato:
            {{"sentiment": "positive/negative/neutral", "confidence": 0.0-1.0, "explanation": "breve explicação"}}
            
            IMPORTANTE: 
            - Responda SEMPRE na língua que o usuário está falando
            - Use apenas "positive", "negative" ou "neutral" para sentiment
            
            Texto para análise:
            "{text}"
            
            JSON:
            """
            
            response = llm_manager.invoke_llm(prompt)
            
            # Tenta extrair JSON da resposta
            import json
            import re
            
            # Procura por JSON na resposta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    return {
                        "sentiment": result.get("sentiment", "neutral"),
                        "confidence": float(result.get("confidence", 0.5)),
                        "explanation": result.get("explanation", "Análise LLM"),
                        "method": "llm",
                        "raw_response": response
                    }
                except json.JSONDecodeError:
                    pass
            
            # Fallback: análise simples da resposta
            response_lower = response.lower()
            if "positive" in response_lower or "positivo" in response_lower:
                sentiment = "positive"
                confidence = 0.7
            elif "negative" in response_lower or "negativo" in response_lower:
                sentiment = "negative"
                confidence = 0.7
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "explanation": response[:100] + "..." if len(response) > 100 else response,
                "method": "llm",
                "raw_response": response
            }
            
        except Exception as e:
            return {"error": f"Erro LLM: {e}"}
    
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Análise completa usando LLM.
        
        Args:
            text: Texto para análise
            
        Returns:
            Resultado da análise
        """
        results = {
            "individual_results": {},
            "consensus": {},
            "metadata": {
                "text_length": len(text),
                "methods_used": [],
                "timestamp": "now"
            }
        }
        
        # Executa a análise LLM
        if self.methods["llm"]["available"]:
            results["individual_results"]["llm"] = self.analyze_llm(text)
            if "error" not in results["individual_results"]["llm"]:
                results["metadata"]["methods_used"].append("llm")
        
        # Calcula o consenso (apenas LLM por enquanto/código deve ser expandido com futuros métodos)
        if results["metadata"]["methods_used"]:
            llm_result = results["individual_results"]["llm"]
            results["consensus"] = {
                "sentiment": llm_result["sentiment"],
                "confidence": llm_result["confidence"],
                "agreement": "unanimous",
                "agreement_ratio": 1.0,
                "methods_count": 1,
                "individual_sentiments": [llm_result["sentiment"]],
                "individual_confidences": [llm_result["confidence"]]
            }
        else:
            results["consensus"] = {
                "sentiment": "neutral",
                "confidence": 0.0,
                "agreement": "none",
                "methods_count": 0
            }
        
        return results
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Análise em lote de múltiplos textos.
        
        Args:
            texts: Lista de textos para análise
            
        Returns:
            Lista de resultados de análise
        """
        return [self.analyze_comprehensive(text) for text in texts]
    
    def get_available_methods(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna informações sobre os métodos disponíveis.
        
        Returns:
            Dicionário com status e capacidades de cada método
        """
        return self.methods.copy()

# Instância global do analisador
sentiment_analyzer = SentimentAnalyzer() 