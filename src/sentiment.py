"""
Análise de sentimentos usando LLM generativo com emoções avançadas
"""

from typing import Dict, List, Any, Optional
from src.llm_providers import llm_manager
import warnings
import json
import re

# Suprime os warnings
warnings.filterwarnings("ignore")

class SentimentAnalyzer:
    """Analisador de sentimentos com LLM e emoções avançadas."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.methods = {}
        self.emotion_mapping = self._setup_emotion_mapping()
        self._setup_llm()
        
        print("Analisador de sentimentos avançado inicializado.")
    
    def _setup_emotion_mapping(self) -> Dict[str, Dict[str, Any]]:
        """Define o mapeamento de emoções específicas."""
        return {
            # Emoções básicas de Ekman + outras importantes
            "felicidade": {
                "emoji": "😊",
                "category": "positive",
                "intensity_levels": ["alegria_leve", "contentamento", "euforia", "êxtase"],
                "synonyms": ["alegria", "contentamento", "satisfação", "júbilo"]
            },
            "tristeza": {
                "emoji": "😢",
                "category": "negative", 
                "intensity_levels": ["melancolia", "tristeza", "depressão", "desespero"],
                "synonyms": ["melancolia", "pesar", "aflição", "desânimo"]
            },
            "raiva": {
                "emoji": "😠",
                "category": "negative",
                "intensity_levels": ["irritação", "aborrecimento", "raiva", "fúria"],
                "synonyms": ["irritação", "ira", "fúria", "aborrecimento", "indignação"]
            },
            "medo": {
                "emoji": "😨",
                "category": "negative",
                "intensity_levels": ["apreensão", "ansiedade", "medo", "terror"],
                "synonyms": ["ansiedade", "apreensão", "temor", "pânico", "terror"]
            },
            "nojo": {
                "emoji": "🤢",
                "category": "negative",
                "intensity_levels": ["desconforto", "aversão", "nojo", "repulsa"],
                "synonyms": ["aversão", "repulsa", "repugnância", "asco"]
            },
            "surpresa": {
                "emoji": "😲", 
                "category": "neutral",
                "intensity_levels": ["curiosidade", "surpresa", "espanto", "choque"],
                "synonyms": ["espanto", "admiração", "perplexidade", "choque"]
            },
            # Emoções adicionais importantes
            "amor": {
                "emoji": "🥰",
                "category": "positive",
                "intensity_levels": ["carinho", "afeto", "amor", "paixão"],
                "synonyms": ["carinho", "afeto", "ternura", "paixão", "adoração"]
            },
            "esperança": {
                "emoji": "🌟",
                "category": "positive", 
                "intensity_levels": ["otimismo", "esperança", "confiança", "fé"],
                "synonyms": ["otimismo", "expectativa", "confiança", "fé"]
            },
            "decepção": {
                "emoji": "😞",
                "category": "negative",
                "intensity_levels": ["insatisfação", "decepção", "desilusão", "desapontamento"],
                "synonyms": ["desilusão", "desapontamento", "frustração"]
            },
            "neutral": {
                "emoji": "😐",
                "category": "neutral",
                "intensity_levels": ["calma", "neutralidade", "indiferença"],
                "synonyms": ["neutralidade", "indiferença", "serenidade"]
            }
        }
    
    def _setup_llm(self):
        """Configura análise com LLM (mais contextual)."""
        if llm_manager.get_llm() is not None:
            self.methods["llm"] = {
                "available": True,
                "speed": "medium",
                "accuracy": "very_high"
            }
            self.methods["advanced_emotions"] = {
                "available": True,
                "speed": "medium", 
                "accuracy": "very_high",
                "supports_multiple": True
            }
            print("LLM configurado para análise avançada de emoções")
        else:
            self.methods["llm"] = {"available": False}
            self.methods["advanced_emotions"] = {"available": False}
    
    def analyze_llm(self, text: str) -> Dict[str, Any]:
        """Análise básica usando LLM (mantida para compatibilidade)."""
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
    
    def analyze_advanced_emotions(self, text: str) -> Dict[str, Any]:
        """Análise avançada de emoções múltiplas usando LLM."""
        if not self.methods["advanced_emotions"]["available"]:
            return {"error": "Análise avançada não disponível"}
        
        try:
            # Lista de emoções disponíveis para o prompt
            emotions_list = ", ".join(self.emotion_mapping.keys())
            
            prompt = f"""
            Analise as emoções presentes no texto abaixo. Pode haver múltiplas emoções simultaneamente.
            
            Emoções disponíveis: {emotions_list}
            
            Responda APENAS com um JSON no formato:
            {{
                "emotions": [
                    {{"emotion": "nome_da_emoção", "intensity": 0.0-1.0, "confidence": 0.0-1.0}},
                    {{"emotion": "outra_emoção", "intensity": 0.0-1.0, "confidence": 0.0-1.0}}
                ],
                "primary_emotion": "emoção_dominante",
                "emotional_complexity": "simple/moderate/complex",
                "overall_sentiment": "positive/negative/neutral/mixed",
                "explanation": "explicação detalhada das emoções detectadas"
            }}
            
            INSTRUÇÕES:
            - Detecte TODAS as emoções presentes, mesmo se fracas
            - Use apenas emoções da lista fornecida
            - intensity: quão forte é a emoção (0.0 = muito fraca, 1.0 = muito intensa)
            - confidence: quão certo você está da presença dessa emoção
            - emotional_complexity: "simple" (1 emoção), "moderate" (2-3), "complex" (4+)
            - overall_sentiment: "mixed" quando há emoções conflitantes
            
            Texto para análise:
            "{text}"
            
            JSON:
            """
            
            response = llm_manager.invoke_llm(prompt)
            
            # Tenta extrair JSON da resposta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    
                    # Processa e valida as emoções detectadas
                    emotions_detected = []
                    for emotion_data in result.get("emotions", []):
                        emotion_name = emotion_data.get("emotion", "").lower()
                        if emotion_name in self.emotion_mapping:
                            emotions_detected.append({
                                "emotion": emotion_name,
                                "intensity": float(emotion_data.get("intensity", 0.5)),
                                "confidence": float(emotion_data.get("confidence", 0.5)),
                                "emoji": self.emotion_mapping[emotion_name]["emoji"],
                                "category": self.emotion_mapping[emotion_name]["category"]
                            })
                    
                    # Calcula emoção primária
                    primary_emotion = result.get("primary_emotion", "neutral").lower()
                    if primary_emotion not in self.emotion_mapping:
                        # Se a emoção primária não é válida, usa a com maior intensidade
                        if emotions_detected:
                            primary_emotion = max(emotions_detected, key=lambda x: x["intensity"])["emotion"]
                        else:
                            primary_emotion = "neutral"
                    
                    return {
                        "emotions": emotions_detected,
                        "primary_emotion": primary_emotion,
                        "primary_emoji": self.emotion_mapping[primary_emotion]["emoji"],
                        "emotional_complexity": result.get("emotional_complexity", "simple"),
                        "overall_sentiment": result.get("overall_sentiment", "neutral"),
                        "explanation": result.get("explanation", "Análise avançada de emoções"),
                        "method": "advanced_emotions",
                        "emotions_count": len(emotions_detected),
                        "raw_response": response
                    }
                    
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    return {"error": f"Erro ao processar análise avançada: {e}"}
            
            # Fallback para análise simples se JSON falhar
            return self._fallback_emotion_analysis(text, response)
            
        except Exception as e:
            return {"error": f"Erro na análise avançada: {e}"}
    
    def _fallback_emotion_analysis(self, text: str, response: str) -> Dict[str, Any]:
        """Análise de fallback quando o JSON não pode ser extraído."""
        response_lower = response.lower()
        text_lower = text.lower()
        
        # Detecta emoções baseado em palavras-chave
        detected_emotions = []
        
        for emotion, info in self.emotion_mapping.items():
            score = 0
            # Verifica a emoção na resposta do LLM
            if emotion in response_lower:
                score += 0.7
            
            # Verifica sinônimos
            for synonym in info["synonyms"]:
                if synonym in response_lower or synonym in text_lower:
                    score += 0.3
            
            if score > 0:
                detected_emotions.append({
                    "emotion": emotion,
                    "intensity": min(score, 1.0),
                    "confidence": 0.6,
                    "emoji": info["emoji"],
                    "category": info["category"]
                })
        
        # Se nenhuma emoção detectada, assume neutral
        if not detected_emotions:
            detected_emotions = [{
                "emotion": "neutral",
                "intensity": 0.5,
                "confidence": 0.5,
                "emoji": "😐",
                "category": "neutral"
            }]
        
        primary_emotion = max(detected_emotions, key=lambda x: x["intensity"])["emotion"]
        
        return {
            "emotions": detected_emotions,
            "primary_emotion": primary_emotion,
            "primary_emoji": self.emotion_mapping[primary_emotion]["emoji"],
            "emotional_complexity": "simple" if len(detected_emotions) == 1 else "moderate",
            "overall_sentiment": "neutral",
            "explanation": "Análise de fallback baseada em palavras-chave",
            "method": "advanced_emotions_fallback",
            "emotions_count": len(detected_emotions),
            "raw_response": response
        }
    
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Análise completa usando LLM básico e análise avançada de emoções.
        
        Args:
            text: Texto para análise
            
        Returns:
            Resultado da análise
        """
        results = {
            "individual_results": {},
            "consensus": {},
            "advanced_analysis": {},
            "metadata": {
                "text_length": len(text),
                "methods_used": [],
                "timestamp": "now"
            }
        }
        
        # Executa a análise LLM básica
        if self.methods["llm"]["available"]:
            results["individual_results"]["llm"] = self.analyze_llm(text)
            if "error" not in results["individual_results"]["llm"]:
                results["metadata"]["methods_used"].append("llm")
        
        # Executa a análise avançada de emoções
        if self.methods["advanced_emotions"]["available"]:
            results["advanced_analysis"] = self.analyze_advanced_emotions(text)
            if "error" not in results["advanced_analysis"]:
                results["metadata"]["methods_used"].append("advanced_emotions")
        
        # Calcula o consenso básico (compatibilidade)
        if "llm" in results["individual_results"] and "error" not in results["individual_results"]["llm"]:
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
    
    def get_emotion_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna o mapeamento de emoções disponíveis.
        
        Returns:
            Dicionário com todas as emoções e suas propriedades
        """
        return self.emotion_mapping.copy()
    
    def get_emotions_by_category(self, category: str) -> List[str]:
        """
        Retorna emoções de uma categoria específica.
        
        Args:
            category: Categoria (positive, negative, neutral)
            
        Returns:
            Lista de emoções da categoria
        """
        return [
            emotion for emotion, info in self.emotion_mapping.items()
            if info["category"] == category
        ]

# Instância global do analisador
sentiment_analyzer = SentimentAnalyzer() 