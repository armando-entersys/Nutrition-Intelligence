"""
Trophology domain models
Based on Manuel Lezaeta Acharan's "La Medicina Natural al Alcance de Todos" (1927)
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CompatibilitySeverity(str, Enum):
    """Severity level of food combination incompatibility"""
    HIGH = "high"      # Fermentación malsana, muy perjudicial
    MEDIUM = "medium"  # Fermentación moderada
    LOW = "low"        # Fermentación leve

class FoodCategory(SQLModel, table=True):
    """
    Food categories according to Lezaeta's Trophology

    Categories:
    1. Frutas Ácidas (Acidic fruits)
    2. Frutas Dulces (Sweet fruits)
    3. Frutas Aceitosas (Oily fruits - nuts, avocado)
    4. Frutas Harináceas (Starchy fruits - chestnuts, plantains)
    5. Almidones (Starches - potatoes, cereals, bread)
    6. Hortalizas/Verduras (Vegetables)
    7. Proteínas (Proteins - eggs, cheese, legumes)
    8. Azúcares (Sugars - honey, sugar)
    9. Grasas (Fats - oils, olives)
    """
    __tablename__ = "food_categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None)

    # Examples of foods in this category (stored as comma-separated string)
    examples: Optional[str] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    compatibilities_as_category1: List["FoodCompatibility"] = Relationship(
        back_populates="category1",
        sa_relationship_kwargs={
            "foreign_keys": "[FoodCompatibility.category1_id]",
            "cascade": "all, delete-orphan"
        }
    )
    compatibilities_as_category2: List["FoodCompatibility"] = Relationship(
        back_populates="category2",
        sa_relationship_kwargs={
            "foreign_keys": "[FoodCompatibility.category2_id]",
            "cascade": "all, delete-orphan"
        }
    )


class FoodCompatibility(SQLModel, table=True):
    """
    Food compatibility rules between categories
    Based on Lezaeta's combination rules to avoid fermentation and digestive issues
    """
    __tablename__ = "food_compatibilities"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys to food categories
    category1_id: int = Field(foreign_key="food_categories.id", index=True)
    category2_id: int = Field(foreign_key="food_categories.id", index=True)

    # Compatibility
    compatible: bool = Field(default=True)

    # If incompatible, why?
    reason: Optional[str] = Field(default=None)

    # Severity of incompatibility
    severity: Optional[CompatibilitySeverity] = Field(default=None)

    # Additional notes (e.g., "eat acidic fruits first")
    note: Optional[str] = Field(default=None)

    # Page reference from Lezaeta's book
    page_reference: Optional[str] = Field(default=None, max_length=20)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    category1: FoodCategory = Relationship(
        back_populates="compatibilities_as_category1",
        sa_relationship_kwargs={"foreign_keys": "[FoodCompatibility.category1_id]"}
    )
    category2: FoodCategory = Relationship(
        back_populates="compatibilities_as_category2",
        sa_relationship_kwargs={"foreign_keys": "[FoodCompatibility.category2_id]"}
    )


class FoodCombinationIssue(SQLModel):
    """
    Pydantic model (not a table) for representing combination validation issues
    Used in API responses
    """
    category1: str
    category2: str
    reason: str
    severity: CompatibilitySeverity
    page_reference: Optional[str] = None
    note: Optional[str] = None
