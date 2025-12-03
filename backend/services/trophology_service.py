from typing import List, Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.trophology.models import FoodCategory, FoodCompatibility, FoodCombinationIssue, CompatibilitySeverity

class TrophologyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories(self) -> List[FoodCategory]:
        """Get all food categories."""
        result = await self.session.execute(select(FoodCategory))
        return result.scalars().all()

    async def get_compatibilities(self) -> List[FoodCompatibility]:
        """Get all compatibility rules."""
        result = await self.session.execute(select(FoodCompatibility))
        return result.scalars().all()

    async def validate_combination(self, category_ids: List[int]) -> Dict:
        """
        Validate a combination of food categories.
        
        Args:
            category_ids: List of category IDs to check
            
        Returns:
            Dict containing validation result, issues, and suggestions
        """
        if len(category_ids) < 2:
            return {
                "valid": True,
                "issues": [],
                "suggestions": ["Agrega más alimentos para verificar la combinación."]
            }

        issues = []
        suggestions = []
        
        # Check all pairs
        for i in range(len(category_ids)):
            for j in range(i + 1, len(category_ids)):
                id1 = category_ids[i]
                id2 = category_ids[j]
                
                # Query compatibility rule
                stmt = select(FoodCompatibility).where(
                    FoodCompatibility.category1_id == id1,
                    FoodCompatibility.category2_id == id2
                )
                result = await self.session.execute(stmt)
                rule = result.scalar_one_or_none()
                
                if rule:
                    # Get category names for better messages
                    cat1 = await self.session.get(FoodCategory, id1)
                    cat2 = await self.session.get(FoodCategory, id2)
                    
                    if not rule.compatible:
                        issue = FoodCombinationIssue(
                            category1=cat1.name,
                            category2=cat2.name,
                            reason=rule.reason or "Combinación no recomendada",
                            severity=rule.severity or CompatibilitySeverity.MEDIUM,
                            page_reference=rule.page_reference,
                            note=rule.note
                        )
                        issues.append(issue)
                    elif rule.note:
                        # It's compatible but has a note (e.g. "eat acidic first")
                        suggestions.append(f"{cat1.name} + {cat2.name}: {rule.note}")

        # General suggestions based on Lezaeta's rules
        if len(category_ids) > 3:
            suggestions.append("Regla de Oro: Simplifica tu comida a 1 o 2 productos para mejor digestión.")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions
        }
