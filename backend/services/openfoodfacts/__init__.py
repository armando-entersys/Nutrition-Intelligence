"""Open Food Facts integration services"""
from .client import openfoodfacts_client, get_product_by_barcode

__all__ = ['openfoodfacts_client', 'get_product_by_barcode']
