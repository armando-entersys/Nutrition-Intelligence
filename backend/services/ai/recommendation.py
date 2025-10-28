"""
AI Recommendation service for meal planning and nutrition suggestions
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging
import random

logger = logging.getLogger(__name__)

class NutritionRecommendationService:
    """AI-powered nutrition recommendation service"""
    
    def __init__(self):
        # Mock food database for recommendations
        self.healthy_foods = {
            "proteins": [
                {"id": 1, "name": "pechuga de pollo", "calories_per_100g": 165, "protein": 31},
                {"id": 2, "name": "pescado blanco", "calories_per_100g": 82, "protein": 18},
                {"id": 3, "name": "huevos", "calories_per_100g": 155, "protein": 13},
                {"id": 4, "name": "frijoles negros", "calories_per_100g": 132, "protein": 9}
            ],
            "carbs": [
                {"id": 5, "name": "arroz integral", "calories_per_100g": 111, "carbs": 23},
                {"id": 6, "name": "quinoa", "calories_per_100g": 120, "carbs": 22},
                {"id": 7, "name": "avena", "calories_per_100g": 68, "carbs": 12},
                {"id": 8, "name": "camote", "calories_per_100g": 86, "carbs": 20}
            ],
            "vegetables": [
                {"id": 9, "name": "brócoli", "calories_per_100g": 34, "fiber": 3},
                {"id": 10, "name": "espinacas", "calories_per_100g": 23, "iron": 2.7},
                {"id": 11, "name": "zanahorias", "calories_per_100g": 41, "vitamin_a": 835},
                {"id": 12, "name": "tomates", "calories_per_100g": 18, "lycopene": "high"}
            ]
        }
    
    async def suggest_daily_plan(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized daily meal plan suggestions
        
        Args:
            patient_profile: Patient profile with goals, restrictions, preferences
            
        Returns:
            Suggested daily meal plan with nutritional breakdown
        """
        try:
            # Extract patient data
            age = patient_profile.get("age", 30)
            weight = patient_profile.get("weight_kg", 70)
            height = patient_profile.get("height_cm", 170)
            activity_level = patient_profile.get("activity_level", "moderate")
            goals = patient_profile.get("goals", ["weight_maintenance"])
            restrictions = patient_profile.get("dietary_restrictions", [])
            
            # Calculate caloric needs (simplified)
            base_calories = self._calculate_base_calories(age, weight, height, activity_level)
            
            # Adjust for goals
            if "weight_loss" in goals:
                target_calories = base_calories - 500
            elif "weight_gain" in goals:
                target_calories = base_calories + 300
            else:
                target_calories = base_calories
            
            # Generate meal suggestions
            meal_plan = {
                "breakfast": self._suggest_meal("breakfast", target_calories * 0.25, restrictions),
                "morning_snack": self._suggest_meal("snack", target_calories * 0.10, restrictions),
                "lunch": self._suggest_meal("lunch", target_calories * 0.35, restrictions),
                "afternoon_snack": self._suggest_meal("snack", target_calories * 0.10, restrictions),
                "dinner": self._suggest_meal("dinner", target_calories * 0.20, restrictions)
            }
            
            # Calculate totals
            total_calories = sum(meal["calories"] for meal in meal_plan.values())
            total_protein = sum(meal["protein"] for meal in meal_plan.values())
            total_carbs = sum(meal["carbs"] for meal in meal_plan.values())
            total_fat = sum(meal["fat"] for meal in meal_plan.values())
            
            return {
                "date": date.today().isoformat(),
                "target_calories": target_calories,
                "meal_plan": meal_plan,
                "nutritional_summary": {
                    "total_calories": round(total_calories, 0),
                    "total_protein": round(total_protein, 1),
                    "total_carbs": round(total_carbs, 1),
                    "total_fat": round(total_fat, 1)
                },
                "recommendations": [
                    "Beber al menos 8 vasos de agua al día",
                    "Incluir ejercicio moderado 30 minutos diarios",
                    "Consumir alimentos a horarios regulares"
                ],
                "confidence_score": 0.82,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating meal plan: {e}")
            raise ValueError(f"Failed to generate meal plan: {str(e)}")
    
    async def suggest_recipe_alternatives(self, original_recipe_id: int, patient_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest alternative recipes based on dietary restrictions and preferences
        
        Args:
            original_recipe_id: ID of the original recipe
            patient_profile: Patient preferences and restrictions
            
        Returns:
            List of alternative recipe suggestions
        """
        # TODO: Implement recipe alternative suggestions
        return [
            {
                "recipe_id": 101,
                "name": "Ensalada de Quinoa con Pollo",
                "reason": "Lower calories, higher protein",
                "calorie_difference": -150,
                "match_score": 0.89
            },
            {
                "recipe_id": 102,
                "name": "Bowl de Vegetales Asados",
                "reason": "Vegetarian option, high fiber",
                "calorie_difference": -200,
                "match_score": 0.75
            }
        ]
    
    async def analyze_nutrition_gaps(self, food_log: List[Dict[str, Any]], target_nutrition: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze nutritional gaps in current diet
        
        Args:
            food_log: List of consumed foods with nutritional data
            target_nutrition: Target nutritional goals
            
        Returns:
            Analysis of nutritional gaps and recommendations
        """
        # Calculate current totals
        current_nutrition = {
            "calories": sum(food.get("calories", 0) for food in food_log),
            "protein": sum(food.get("protein", 0) for food in food_log),
            "carbs": sum(food.get("carbs", 0) for food in food_log),
            "fat": sum(food.get("fat", 0) for food in food_log),
            "fiber": sum(food.get("fiber", 0) for food in food_log)
        }
        
        # Calculate gaps
        gaps = {}
        recommendations = []
        
        for nutrient, target in target_nutrition.items():
            current = current_nutrition.get(nutrient, 0)
            gap = target - current
            gaps[nutrient] = {
                "target": target,
                "current": current,
                "gap": gap,
                "percentage_met": (current / target * 100) if target > 0 else 0
            }
            
            if gap > 0:
                if nutrient == "protein":
                    recommendations.append(f"Agregar {gap:.1f}g más de proteína - considera pollo, pescado o legumbres")
                elif nutrient == "fiber":
                    recommendations.append(f"Aumentar fibra en {gap:.1f}g - incluye más vegetales y frutas")
        
        return {
            "nutritional_gaps": gaps,
            "recommendations": recommendations,
            "overall_score": sum(min(100, gap["percentage_met"]) for gap in gaps.values()) / len(gaps),
            "priority_nutrients": [k for k, v in gaps.items() if v["percentage_met"] < 80]
        }
    
    def _calculate_base_calories(self, age: int, weight: float, height: float, activity_level: str) -> float:
        """Calculate base caloric needs using Mifflin-St Jeor equation"""
        # Simplified calculation for demo
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  # Male formula
        
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        return bmr * activity_multipliers.get(activity_level, 1.55)
    
    def _suggest_meal(self, meal_type: str, target_calories: float, restrictions: List[str]) -> Dict[str, Any]:
        """Generate meal suggestion for specific meal type"""
        # Simple mock implementation
        if meal_type == "breakfast":
            foods = ["avena con frutas", "huevos revueltos", "yogurt con granola"]
        elif meal_type == "lunch" or meal_type == "dinner":
            foods = ["pollo con vegetales", "pescado a la plancha", "ensalada de quinoa"]
        else:  # snack
            foods = ["frutas", "nueces", "yogurt natural"]
        
        selected_food = random.choice(foods)
        
        return {
            "name": selected_food,
            "calories": target_calories,
            "protein": target_calories * 0.20 / 4,  # 20% protein
            "carbs": target_calories * 0.50 / 4,    # 50% carbs
            "fat": target_calories * 0.30 / 9,      # 30% fat
            "suggestions": [f"Preparar {selected_food} con ingredientes frescos"]
        }

# Service instance
recommendation_service = NutritionRecommendationService()

# Convenience functions
async def suggest_daily_plan(patient_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Generate daily meal plan suggestions"""
    return await recommendation_service.suggest_daily_plan(patient_profile)

async def suggest_recipe_alternatives(recipe_id: int, patient_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Suggest recipe alternatives"""
    return await recommendation_service.suggest_recipe_alternatives(recipe_id, patient_profile)

async def analyze_nutrition_gaps(food_log: List[Dict[str, Any]], targets: Dict[str, float]) -> Dict[str, Any]:
    """Analyze nutritional gaps"""
    return await recommendation_service.analyze_nutrition_gaps(food_log, targets)