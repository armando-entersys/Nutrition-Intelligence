"""
NOM-051 Seal Calculator
Calculates warning seals based on Official Mexican Standard NOM-051-SCFI/SSA1-2010
"""
import logging
from typing import Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# NOM-051 Phase 3 Thresholds (Oct 2025)
# These are the FINAL and most strict criteria

# Exceso de calorías: >= 275 kcal per 100g for solids, >= 70 kcal per 100ml for liquids
CALORIES_THRESHOLD_SOLID = 275  # kcal per 100g
CALORIES_THRESHOLD_LIQUID = 70  # kcal per 100ml

# Exceso de azúcares: >= 10% of total energy from added sugars
SUGARS_THRESHOLD_SOLID = 10  # g per 100g
SUGARS_THRESHOLD_LIQUID = 5   # g per 100ml

# Exceso de grasas saturadas: >= 10% of total energy
SATURATED_FAT_THRESHOLD_SOLID = 4   # g per 100g
SATURATED_FAT_THRESHOLD_LIQUID = 2  # g per 100ml

# Exceso de grasas trans: >= 1% of total energy
TRANS_FAT_THRESHOLD = 1.0  # g per 100g/ml

# Exceso de sodio
SODIUM_THRESHOLD_SOLID = 300  # mg per 100g
SODIUM_THRESHOLD_LIQUID = 100  # mg per 100ml


@dataclass
class NOM051Seals:
    """NOM-051 warning seals for a product"""
    exceso_calorias: bool = False
    exceso_azucares: bool = False
    exceso_grasas_saturadas: bool = False
    exceso_grasas_trans: bool = False
    exceso_sodio: bool = False
    contiene_edulcorantes: bool = False
    contiene_cafeina: bool = False

    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary"""
        return {
            "exceso_calorias": self.exceso_calorias,
            "exceso_azucares": self.exceso_azucares,
            "exceso_grasas_saturadas": self.exceso_grasas_saturadas,
            "exceso_grasas_trans": self.exceso_grasas_trans,
            "exceso_sodio": self.exceso_sodio,
            "contiene_edulcorantes": self.contiene_edulcorantes,
            "contiene_cafeina": self.contiene_cafeina
        }

    def count_seals(self) -> int:
        """Count total number of warning seals"""
        return sum([
            self.exceso_calorias,
            self.exceso_azucares,
            self.exceso_grasas_saturadas,
            self.exceso_grasas_trans,
            self.exceso_sodio,
            self.contiene_edulcorantes,
            self.contiene_cafeina
        ])


class NOM051Calculator:
    """Calculator for NOM-051 warning seals"""

    def calculate_seals(
        self,
        calorias: float,
        azucares: float,
        grasas_saturadas: float,
        grasas_trans: float,
        sodio: float,  # in mg
        is_liquid: bool = False,
        contiene_edulcorantes: bool = False,
        contiene_cafeina: bool = False
    ) -> NOM051Seals:
        """
        Calculate NOM-051 warning seals based on nutritional content

        Args:
            calorias: Calories per 100g/ml
            azucares: Sugars in grams per 100g/ml
            grasas_saturadas: Saturated fat in grams per 100g/ml
            grasas_trans: Trans fat in grams per 100g/ml
            sodio: Sodium in mg per 100g/ml
            is_liquid: Whether the product is liquid
            contiene_edulcorantes: Whether product contains sweeteners
            contiene_cafeina: Whether product contains caffeine

        Returns:
            NOM051Seals object with calculated seals
        """
        seals = NOM051Seals()

        # Select thresholds based on product type (solid or liquid)
        cal_threshold = CALORIES_THRESHOLD_LIQUID if is_liquid else CALORIES_THRESHOLD_SOLID
        sug_threshold = SUGARS_THRESHOLD_LIQUID if is_liquid else SUGARS_THRESHOLD_SOLID
        sat_fat_threshold = SATURATED_FAT_THRESHOLD_LIQUID if is_liquid else SATURATED_FAT_THRESHOLD_SOLID
        sod_threshold = SODIUM_THRESHOLD_LIQUID if is_liquid else SODIUM_THRESHOLD_SOLID

        # Calculate seals
        seals.exceso_calorias = calorias >= cal_threshold
        seals.exceso_azucares = azucares >= sug_threshold
        seals.exceso_grasas_saturadas = grasas_saturadas >= sat_fat_threshold
        seals.exceso_grasas_trans = grasas_trans >= TRANS_FAT_THRESHOLD
        seals.exceso_sodio = sodio >= sod_threshold
        seals.contiene_edulcorantes = contiene_edulcorantes
        seals.contiene_cafeina = contiene_cafeina

        logger.info(
            f"NOM-051 calculation: "
            f"{'liquid' if is_liquid else 'solid'}, "
            f"{seals.count_seals()} seals, "
            f"cal={calorias:.1f}, sug={azucares:.1f}g, "
            f"sat_fat={grasas_saturadas:.1f}g, trans={grasas_trans:.1f}g, sod={sodio:.1f}mg"
        )

        return seals

    def get_health_score(self, seals: NOM051Seals) -> Tuple[int, str, str]:
        """
        Calculate health score based on number of seals

        Args:
            seals: NOM051Seals object

        Returns:
            Tuple of (score, level, color)
            - score: 0-100 health score
            - level: "Excelente", "Bueno", "Moderado", "Pobre"
            - color: Hex color code
        """
        seal_count = seals.count_seals()

        if seal_count == 0:
            return 90, "Excelente", "#4CAF50"  # Green
        elif seal_count == 1:
            return 70, "Bueno", "#8BC34A"  # Light green
        elif seal_count == 2:
            return 50, "Moderado", "#FF9800"  # Orange
        elif seal_count == 3:
            return 30, "Pobre", "#FF5722"  # Deep orange
        else:  # 4 or more seals
            return 15, "Muy pobre", "#F44336"  # Red


# Global calculator instance
nom051_calculator = NOM051Calculator()


# Convenience function
def calculate_seals(
    calorias: float,
    azucares: float,
    grasas_saturadas: float,
    grasas_trans: float,
    sodio: float,
    is_liquid: bool = False,
    contiene_edulcorantes: bool = False,
    contiene_cafeina: bool = False
) -> NOM051Seals:
    """Calculate NOM-051 seals for a product"""
    return nom051_calculator.calculate_seals(
        calorias=calorias,
        azucares=azucares,
        grasas_saturadas=grasas_saturadas,
        grasas_trans=grasas_trans,
        sodio=sodio,
        is_liquid=is_liquid,
        contiene_edulcorantes=contiene_edulcorantes,
        contiene_cafeina=contiene_cafeina
    )
