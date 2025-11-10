"""
Open Food Facts API Client
Provides integration with Open Food Facts database for product information
"""
import logging
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Open Food Facts API configuration
OPEN_FOOD_FACTS_API_URL = "https://world.openfoodfacts.org/api/v2"
USER_AGENT = "Nutrition Intelligence Platform - Mexico - Version 1.0"


@dataclass
class ProductNutrition:
    """Nutrition data for a product"""
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    sugars: Optional[float] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    trans_fat: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None  # in mg


@dataclass
class ProductInfo:
    """Complete product information from Open Food Facts"""
    barcode: str
    product_name: str
    brands: Optional[str] = None
    categories: Optional[str] = None
    image_url: Optional[str] = None
    ingredients_text: Optional[str] = None
    nutrition: Optional[ProductNutrition] = None
    serving_size_g: Optional[float] = None
    countries: Optional[str] = None
    openfoodfacts_id: Optional[str] = None


class OpenFoodFactsClient:
    """Client for interacting with Open Food Facts API"""

    def __init__(self):
        self.api_url = OPEN_FOOD_FACTS_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        })

    def get_product_by_barcode(self, barcode: str) -> Optional[ProductInfo]:
        """
        Fetch product information from Open Food Facts by barcode

        Args:
            barcode: Product barcode (EAN-13, UPC-A, etc.)

        Returns:
            ProductInfo object if found, None otherwise
        """
        try:
            # Clean barcode (remove spaces and special characters)
            barcode_clean = barcode.strip().replace(" ", "").replace("-", "")

            url = f"{self.api_url}/product/{barcode_clean}"
            logger.info(f"Fetching product from Open Food Facts: {barcode_clean}")

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check if product was found
            if data.get("status") != 1:
                logger.warning(f"Product not found in Open Food Facts: {barcode_clean}")
                return None

            product_data = data.get("product", {})

            # Parse nutrition data
            nutrition_data = product_data.get("nutriments", {})
            nutrition = ProductNutrition(
                calories=self._get_nutrient(nutrition_data, "energy-kcal", "_100g"),
                proteins=self._get_nutrient(nutrition_data, "proteins", "_100g"),
                carbohydrates=self._get_nutrient(nutrition_data, "carbohydrates", "_100g"),
                sugars=self._get_nutrient(nutrition_data, "sugars", "_100g"),
                fat=self._get_nutrient(nutrition_data, "fat", "_100g"),
                saturated_fat=self._get_nutrient(nutrition_data, "saturated-fat", "_100g"),
                trans_fat=self._get_nutrient(nutrition_data, "trans-fat", "_100g"),
                fiber=self._get_nutrient(nutrition_data, "fiber", "_100g"),
                sodium=self._get_nutrient(nutrition_data, "sodium", "_100g", multiplier=1000)  # Convert g to mg
            )

            # Build ProductInfo object
            product_info = ProductInfo(
                barcode=barcode_clean,
                product_name=product_data.get("product_name", "Producto desconocido"),
                brands=product_data.get("brands"),
                categories=product_data.get("categories"),
                image_url=product_data.get("image_url"),
                ingredients_text=product_data.get("ingredients_text"),
                nutrition=nutrition,
                serving_size_g=self._parse_serving_size(product_data.get("serving_size")),
                countries=product_data.get("countries"),
                openfoodfacts_id=product_data.get("id")
            )

            logger.info(f"Product found: {product_info.product_name} ({product_info.brands})")
            return product_info

        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching product {barcode} from Open Food Facts")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching product {barcode} from Open Food Facts: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing product {barcode}: {e}", exc_info=True)
            return None

    def _get_nutrient(
        self,
        nutriments: Dict,
        nutrient_name: str,
        suffix: str = "_100g",
        multiplier: float = 1.0
    ) -> Optional[float]:
        """
        Extract nutrient value from nutriments dictionary

        Args:
            nutriments: Nutriments dictionary from Open Food Facts
            nutrient_name: Name of the nutrient (e.g., "proteins")
            suffix: Suffix to append to nutrient name (default "_100g")
            multiplier: Multiplier to apply to the value (default 1.0)

        Returns:
            Nutrient value as float, or None if not available
        """
        key = f"{nutrient_name}{suffix}"
        value = nutriments.get(key)

        if value is not None:
            try:
                return float(value) * multiplier
            except (ValueError, TypeError):
                logger.warning(f"Invalid nutrient value for {key}: {value}")
                return None
        return None

    def _parse_serving_size(self, serving_size_str: Optional[str]) -> Optional[float]:
        """
        Parse serving size string to grams

        Args:
            serving_size_str: Serving size string (e.g., "100g", "250ml")

        Returns:
            Serving size in grams, or None if not parseable
        """
        if not serving_size_str:
            return None

        try:
            # Remove spaces and convert to lowercase
            size_str = serving_size_str.strip().lower()

            # Extract number
            import re
            match = re.match(r'(\d+(?:\.\d+)?)', size_str)
            if match:
                value = float(match.group(1))

                # Assume grams/ml are roughly equivalent for liquids
                if 'g' in size_str or 'ml' in size_str:
                    return value
                elif 'kg' in size_str or 'l' in size_str:
                    return value * 1000

            return None

        except Exception as e:
            logger.warning(f"Error parsing serving size '{serving_size_str}': {e}")
            return None

    def search_products(
        self,
        query: str,
        country: str = "Mexico",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Search for products by name or brand

        Args:
            query: Search query string
            country: Filter by country (default "Mexico")
            page: Page number for pagination
            page_size: Number of results per page

        Returns:
            Dictionary with search results and metadata
        """
        try:
            url = f"{self.api_url}/search"
            params = {
                "search_terms": query,
                "countries_tags": country.lower(),
                "page": page,
                "page_size": page_size,
                "fields": "code,product_name,brands,image_url,nutriments,categories"
            }

            logger.info(f"Searching Open Food Facts: query='{query}', country={country}")

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            products = data.get("products", [])
            count = data.get("count", 0)

            logger.info(f"Found {count} products matching '{query}'")

            return {
                "count": count,
                "page": page,
                "page_size": page_size,
                "products": products
            }

        except Exception as e:
            logger.error(f"Error searching Open Food Facts: {e}", exc_info=True)
            return {
                "count": 0,
                "page": page,
                "page_size": page_size,
                "products": []
            }


# Global client instance
openfoodfacts_client = OpenFoodFactsClient()


# Convenience function
def get_product_by_barcode(barcode: str) -> Optional[ProductInfo]:
    """Get product information by barcode"""
    return openfoodfacts_client.get_product_by_barcode(barcode)
