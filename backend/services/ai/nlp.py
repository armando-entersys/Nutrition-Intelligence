"""
Natural Language Processing service for nutrition intelligence
"""
from typing import List, Dict, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)

class NutritionNLPService:
    """NLP service for nutrition-related text processing"""
    
    def __init__(self):
        self.food_synonyms = {
            "arroz": ["rice", "arroz blanco", "arroz integral"],
            "pollo": ["chicken", "pechuga", "muslo de pollo"],
            "frijoles": ["beans", "habichuelas", "judías"],
            "tortilla": ["tortilla de maíz", "tortilla de harina"]
        }
        
        # Common Mexican food patterns
        self.mexican_food_patterns = [
            r"tacos?\s+de\s+(\w+)",
            r"quesadillas?\s+de\s+(\w+)",
            r"sopa\s+de\s+(\w+)",
            r"agua\s+de\s+(\w+)"
        ]
    
    async def normalize_food_name(self, food_text: str) -> Dict[str, Any]:
        """
        Normalize and standardize food names
        
        Args:
            food_text: Raw food name or description
            
        Returns:
            Normalized food information
        """
        try:
            cleaned_text = food_text.lower().strip()
            
            # Remove common prefixes/suffixes
            cleaned_text = re.sub(r'\b(un|una|el|la|los|las)\b', '', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            # Check for synonyms
            normalized_name = cleaned_text
            for canonical, synonyms in self.food_synonyms.items():
                if any(synonym.lower() in cleaned_text for synonym in synonyms):
                    normalized_name = canonical
                    break
            
            # Extract Mexican food patterns
            mexican_match = None
            for pattern in self.mexican_food_patterns:
                match = re.search(pattern, cleaned_text)
                if match:
                    mexican_match = {
                        "type": pattern.split(r'\s+')[0],
                        "filling": match.group(1)
                    }
                    break
            
            return {
                "original_text": food_text,
                "normalized_name": normalized_name,
                "cleaned_text": cleaned_text,
                "mexican_food_match": mexican_match,
                "confidence": 0.8,
                "suggestions": [normalized_name, cleaned_text]
            }
            
        except Exception as e:
            logger.error(f"Error normalizing food name: {e}")
            return {
                "original_text": food_text,
                "normalized_name": food_text,
                "error": str(e)
            }
    
    async def extract_nutritional_info(self, text: str) -> Dict[str, Any]:
        """
        Extract nutritional information from text descriptions
        
        Args:
            text: Text containing nutritional information
            
        Returns:
            Extracted nutritional data
        """
        # TODO: Implement nutritional info extraction
        nutrition_patterns = {
            "calories": r"(\d+)\s*(?:cal|calorías|kcal)",
            "protein": r"(\d+(?:\.\d+)?)\s*g?\s*(?:proteína|protein)",
            "carbs": r"(\d+(?:\.\d+)?)\s*g?\s*(?:carbohidratos|carbs)",
            "fat": r"(\d+(?:\.\d+)?)\s*g?\s*(?:grasa|fat)"
        }
        
        extracted = {}
        for nutrient, pattern in nutrition_patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                extracted[nutrient] = float(match.group(1))
        
        return {
            "extracted_nutrition": extracted,
            "confidence": 0.7 if extracted else 0.0,
            "source_text": text
        }
    
    async def analyze_dietary_preferences(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for dietary preferences and restrictions
        
        Args:
            text: Text describing dietary preferences
            
        Returns:
            Dietary preference analysis
        """
        preferences = {
            "vegetarian": ["vegetariano", "vegetarian", "sin carne"],
            "vegan": ["vegano", "vegan", "sin productos animales"],
            "gluten_free": ["sin gluten", "gluten free", "celíaco"],
            "dairy_free": ["sin lácteos", "dairy free", "sin leche"],
            "low_carb": ["bajo en carbohidratos", "low carb", "keto"],
            "diabetic": ["diabético", "diabetic", "sin azúcar"]
        }
        
        detected_preferences = []
        text_lower = text.lower()
        
        for pref_type, keywords in preferences.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_preferences.append(pref_type)
        
        return {
            "detected_preferences": detected_preferences,
            "confidence": 0.85 if detected_preferences else 0.3,
            "source_text": text
        }
    
    async def classify_eating_disorder_signals(self, text: str) -> Dict[str, Any]:
        """
        Detect potential eating disorder signals in text (for nutritionist alerts)
        
        Args:
            text: Text to analyze for concerning patterns
            
        Returns:
            Risk assessment with recommendations
        """
        # WARNING SIGNALS - patterns that might indicate eating disorders
        warning_patterns = [
            r"no\s+(?:he\s+)?comido\s+(?:nada|muy poco)",
            r"(?:odio|detesto)\s+mi\s+cuerpo",
            r"necesito\s+(?:perder|bajar)\s+\d+\s*kg\s+(?:rápido|ya)",
            r"(?:vomité|vomitar)\s+después\s+de\s+comer",
            r"ejercicio\s+por\s+\d+\s+horas"
        ]
        
        risk_signals = []
        text_lower = text.lower()
        
        for pattern in warning_patterns:
            if re.search(pattern, text_lower):
                risk_signals.append(pattern)
        
        risk_level = "high" if len(risk_signals) >= 2 else "medium" if risk_signals else "low"
        
        return {
            "risk_level": risk_level,
            "detected_signals": len(risk_signals),
            "requires_attention": risk_level in ["high", "medium"],
            "recommended_action": "immediate_nutritionist_review" if risk_level == "high" else "monitor",
            "confidence": 0.75 if risk_signals else 0.2
        }

# Service instance
nutrition_nlp_service = NutritionNLPService()

# Convenience functions
async def normalize_food_name(food_text: str) -> Dict[str, Any]:
    """Normalize food name"""
    return await nutrition_nlp_service.normalize_food_name(food_text)

async def extract_nutritional_info(text: str) -> Dict[str, Any]:
    """Extract nutritional information from text"""
    return await nutrition_nlp_service.extract_nutritional_info(text)

async def analyze_dietary_preferences(text: str) -> Dict[str, Any]:
    """Analyze dietary preferences"""
    return await nutrition_nlp_service.analyze_dietary_preferences(text)

async def check_eating_disorder_signals(text: str) -> Dict[str, Any]:
    """Check for eating disorder warning signals"""
    return await nutrition_nlp_service.classify_eating_disorder_signals(text)