"""
Trophology Service - Food Combination Validation
Based on Manuel Lezaeta Acharán's Trophology rules
"""
from typing import List, Dict, Optional
from sqlmodel import Session, select
from domain.trophology.models import (
    FoodCategory,
    FoodCompatibility,
    FoodCombinationIssue,
    CompatibilitySeverity
)


class TrophologyService:
    """
    Service for validating food combinations according to Lezaeta's Trophology

    Main principle: "Para evitar los inconvenientes de las malas combinaciones,
    la mejor regla será simplificar cada comida a uno o dos productos"
    - Lezaeta, Página 119
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> List[FoodCategory]:
        """Get all food categories"""
        statement = select(FoodCategory)
        return list(self.db.exec(statement).all())

    def get_category_by_id(self, category_id: int) -> Optional[FoodCategory]:
        """Get a specific food category by ID"""
        return self.db.get(FoodCategory, category_id)

    def get_category_by_name(self, name: str) -> Optional[FoodCategory]:
        """Get a specific food category by name"""
        statement = select(FoodCategory).where(FoodCategory.name == name)
        return self.db.exec(statement).first()

    def validate_combination(
        self,
        category_ids: List[int]
    ) -> Dict[str, any]:
        """
        Validate a combination of food categories

        Args:
            category_ids: List of food category IDs to validate

        Returns:
            {
                "valid": bool,
                "issues": List[FoodCombinationIssue],
                "suggestions": List[str],
                "lezaeta_principle": str
            }
        """
        issues = []
        categories_involved = []

        # Get all categories
        for cat_id in category_ids:
            category = self.get_category_by_id(cat_id)
            if category:
                categories_involved.append(category)

        # Check if too many products (Lezaeta's rule: simplify to 1-2 products)
        if len(category_ids) > 2:
            # Add warning about complexity
            pass  # We'll handle this in suggestions

        # Check all pairwise combinations
        for i in range(len(category_ids)):
            for j in range(i + 1, len(category_ids)):
                cat1_id = category_ids[i]
                cat2_id = category_ids[j]

                # Look for compatibility rule (bidirectional)
                statement = select(FoodCompatibility).where(
                    (
                        (FoodCompatibility.category1_id == cat1_id) &
                        (FoodCompatibility.category2_id == cat2_id)
                    ) | (
                        (FoodCompatibility.category1_id == cat2_id) &
                        (FoodCompatibility.category2_id == cat1_id)
                    )
                )
                compatibility = self.db.exec(statement).first()

                # If there's a rule and it's incompatible, add to issues
                if compatibility and not compatibility.compatible:
                    cat1 = self.get_category_by_id(cat1_id)
                    cat2 = self.get_category_by_id(cat2_id)

                    issue = FoodCombinationIssue(
                        category1=cat1.name,
                        category2=cat2.name,
                        reason=compatibility.reason,
                        severity=compatibility.severity,
                        page_reference=compatibility.page_reference,
                        note=compatibility.note
                    )
                    issues.append(issue)

        # Generate suggestions
        suggestions = self._generate_suggestions(category_ids, categories_involved, issues)

        # Determine if overall valid
        valid = len(issues) == 0

        # Add Lezaeta's principle
        lezaeta_principle = self._get_relevant_principle(len(category_ids), valid)

        return {
            "valid": valid,
            "issues": [issue.model_dump() for issue in issues],
            "suggestions": suggestions,
            "lezaeta_principle": lezaeta_principle
        }

    def _generate_suggestions(
        self,
        category_ids: List[int],
        categories: List[FoodCategory],
        issues: List[FoodCombinationIssue]
    ) -> List[str]:
        """Generate helpful suggestions based on issues found"""
        suggestions = []

        # Suggestion about complexity (>2 products)
        if len(category_ids) > 2:
            suggestions.append(
                'Según Lezaeta: "Para evitar los inconvenientes de las malas combinaciones, '
                'la mejor regla será simplificar cada comida a uno o dos productos, '
                'variando éstos en las diversas comidas del día o mejor cada día." (Página 119)'
            )

        # Specific suggestions based on issues
        category_names = [cat.name for cat in categories]

        # Check for potato + bread/cereal issue
        if "Almidones" in category_names:
            for issue in issues:
                if "Almidones" in [issue.category1, issue.category2]:
                    if "papas" in issue.reason.lower() or "cereales" in issue.reason.lower():
                        suggestions.append(
                            "⚠️ REGLA CRÍTICA: NO mezclar papas con pan, cereales (trigo, maíz, arroz, avena). "
                            "Pueden consumirse en comidas separadas. La fécula de las papas con el almidón "
                            "de los cereales entra en fermentación malsana. (Página 118-119)"
                        )
                        break

        # Check for fruit + vegetable issue
        if any("Frutas" in cat for cat in category_names) and "Hortalizas/Verduras" in category_names:
            suggestions.append(
                "Las frutas y hortalizas son de naturaleza opuesta: "
                "hortalizas contienen sales minerales, frutas contienen ácidos y azúcares. "
                "Consúmalas en comidas separadas. (Página 119)"
            )

        # Check for acidic fruits + starches
        if "Frutas Ácidas" in category_names and "Almidones" in category_names:
            suggestions.append(
                "Frutas ácidas (naranjas, limones) NO deben mezclarse con almidones (pan, cereales, papas). "
                "Los ácidos impiden el desdoblamiento normal de los almidones, causando fermentación. (Página 118)"
            )

        # Suggestion about acidic + oily fruits (GOOD combination)
        if "Frutas Ácidas" in category_names and "Frutas Aceitosas" in category_names:
            suggestions.append(
                "✓ BUENA COMBINACIÓN: Frutas ácidas + frutas aceitosas. "
                "Consejo de Lezaeta: Comer primero las ácidas (ej: naranjas con nueces). (Página 118)"
            )

        # General digestive health reminder
        if not suggestions:
            suggestions.append(
                '✓ Esta combinación no presenta problemas conocidos según Lezaeta. '
                'Recuerde: "La mitad de la digestión se hace en la boca" - mastique cuidadosamente. (Página 117)'
            )

        return suggestions

    def _get_relevant_principle(self, num_products: int, valid: bool) -> str:
        """Get relevant Lezaeta principle based on situation"""
        if num_products > 2:
            return (
                'Principio de Lezaeta: "Simplificar cada comida a uno o dos productos, '
                'variando éstos en las diversas comidas del día" (Página 119)'
            )
        elif not valid:
            return (
                'Principio fundamental: "No hay enfermo con buena digestión, ni persona sana '
                'con mala digestión" (Página 113) - Evite combinaciones que causen fermentación.'
            )
        else:
            return (
                'Señal de buena digestión según Lezaeta: "Los excrementos son inodoros, '
                'color bronce y no duros ni diarreicos" (Página 115)'
            )

    def get_compatibilities_for_category(
        self,
        category_id: int
    ) -> Dict[str, List[FoodCategory]]:
        """
        Get all compatible and incompatible categories for a given category

        Returns:
            {
                "compatible": List[FoodCategory],
                "incompatible": List[FoodCategory]
            }
        """
        compatible = []
        incompatible = []

        # Get all compatibility rules involving this category
        statement = select(FoodCompatibility).where(
            (FoodCompatibility.category1_id == category_id) |
            (FoodCompatibility.category2_id == category_id)
        )
        compatibilities = self.db.exec(statement).all()

        for comp in compatibilities:
            # Determine which is the "other" category
            other_id = comp.category2_id if comp.category1_id == category_id else comp.category1_id
            other_category = self.get_category_by_id(other_id)

            if other_category:
                if comp.compatible:
                    compatible.append(other_category)
                else:
                    incompatible.append(other_category)

        return {
            "compatible": compatible,
            "incompatible": incompatible
        }

    def get_all_compatibility_rules(self) -> List[FoodCompatibility]:
        """Get all compatibility rules"""
        statement = select(FoodCompatibility)
        return list(self.db.exec(statement).all())

    def search_categories_by_food(self, food_name: str) -> List[FoodCategory]:
        """
        Search which categories a food might belong to

        Args:
            food_name: Name of the food (e.g., "naranja", "papa", "nuez")

        Returns:
            List of categories that might contain this food
        """
        food_name_lower = food_name.lower()

        statement = select(FoodCategory).where(
            FoodCategory.examples.contains(food_name_lower)
        )

        return list(self.db.exec(statement).all())
