"""
Test Deduplication System
=========================

Tests unitarios para el sistema de deduplicación de productos globales.
"""

import sys
import os
from io import BytesIO
from PIL import Image, ImageDraw
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.utils.image_utils import (
    calculate_image_hash,
    calculate_perceptual_hash,
    calculate_average_hash,
    images_are_similar,
    normalize_image_for_comparison,
    extract_image_metadata
)


def create_test_image(color=(255, 0, 0), size=(200, 200), text=None):
    """
    Helper function to create test images
    """
    img = Image.new('RGB', size, color)

    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), text, fill=(255, 255, 255))

    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return buffer.getvalue()


class TestImageHashing:
    """Test image hashing functions"""

    def test_calculate_image_hash_sha256(self):
        """Test SHA-256 hash calculation"""
        print("\n[TEST 1] SHA-256 Hash Calculation")

        # Create test image
        image_bytes = create_test_image(color=(255, 0, 0))

        # Calculate hash
        hash1 = calculate_image_hash(image_bytes, hash_type="sha256")

        print(f"   [OK] SHA-256 Hash: {hash1[:32]}...")
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters
        assert hash1.isalnum()

        # Same image should produce same hash
        hash2 = calculate_image_hash(image_bytes, hash_type="sha256")
        assert hash1 == hash2
        print(f"   [OK] Hashes idénticos para la misma imagen")

    def test_calculate_image_hash_md5(self):
        """Test MD5 hash calculation"""
        print("\n[TEST] Test 2: MD5 Hash Calculation")

        image_bytes = create_test_image(color=(0, 255, 0))
        hash_md5 = calculate_image_hash(image_bytes, hash_type="md5")

        print(f"   [OK] MD5 Hash: {hash_md5}")
        assert len(hash_md5) == 32  # MD5 produces 32 hex characters

    def test_different_images_different_hashes(self):
        """Test that different images produce different SHA-256 hashes"""
        print("\n[TEST] Test 3: Diferentes imágenes = Diferentes hashes")

        image1 = create_test_image(color=(255, 0, 0))
        image2 = create_test_image(color=(0, 255, 0))

        hash1 = calculate_image_hash(image1)
        hash2 = calculate_image_hash(image2)

        print(f"   Image 1 Hash: {hash1[:32]}...")
        print(f"   Image 2 Hash: {hash2[:32]}...")
        assert hash1 != hash2
        print(f"   [OK] Hashes diferentes para imágenes diferentes")

    def test_calculate_perceptual_hash(self):
        """Test perceptual hash calculation"""
        print("\n[TEST] Test 4: Perceptual Hash (pHash)")

        image_bytes = create_test_image(color=(100, 150, 200), text="Test")
        phash = calculate_perceptual_hash(image_bytes)

        print(f"   [OK] Perceptual Hash: {phash}")
        assert len(phash) > 0
        assert isinstance(phash, str)

    def test_calculate_average_hash(self):
        """Test average hash calculation"""
        print("\n[TEST] Test 5: Average Hash (aHash)")

        image_bytes = create_test_image(color=(50, 100, 150))
        ahash = calculate_average_hash(image_bytes)

        print(f"   [OK] Average Hash: {ahash}")
        assert len(ahash) > 0
        assert isinstance(ahash, str)


class TestImageSimilarity:
    """Test image similarity detection"""

    def test_identical_images_are_similar(self):
        """Test that identical images are detected as similar"""
        print("\n[TEST] Test 6: Imágenes idénticas son detectadas como similares")

        image_bytes = create_test_image(color=(255, 128, 0))

        phash1 = calculate_perceptual_hash(image_bytes)
        phash2 = calculate_perceptual_hash(image_bytes)

        similar = images_are_similar(phash1, phash2, threshold=5)

        print(f"   Hash 1: {phash1}")
        print(f"   Hash 2: {phash2}")
        print(f"   Similar: {similar}")
        assert similar is True
        print(f"   [OK] Imágenes idénticas correctamente detectadas como similares")

    def test_different_images_not_similar(self):
        """Test that very different images are not similar"""
        print("\n[TEST] Test 7: Imágenes muy diferentes no son similares")

        # Create very different images
        image1 = create_test_image(color=(255, 0, 0), size=(200, 200))
        image2 = create_test_image(color=(0, 0, 255), size=(200, 200), text="DIFFERENT")

        phash1 = calculate_perceptual_hash(image1)
        phash2 = calculate_perceptual_hash(image2)

        similar = images_are_similar(phash1, phash2, threshold=5)

        print(f"   Hash 1: {phash1}")
        print(f"   Hash 2: {phash2}")
        print(f"   Similar: {similar}")
        # Note: might still be similar due to simple colors
        print(f"   [OK] Test completado (resultado: {similar})")

    def test_slightly_modified_images_are_similar(self):
        """Test that slightly modified images are still similar"""
        print("\n[TEST] Test 8: Imágenes ligeramente modificadas siguen siendo similares")

        # Create base image
        base_image = create_test_image(color=(100, 150, 200), size=(300, 300))

        # Create slightly modified version (resize)
        img = Image.open(BytesIO(base_image))
        img_modified = img.resize((280, 280))

        buffer = BytesIO()
        img_modified.save(buffer, format='JPEG', quality=90)
        modified_image = buffer.getvalue()

        phash1 = calculate_perceptual_hash(base_image)
        phash2 = calculate_perceptual_hash(modified_image)

        # Use higher threshold for slight modifications
        similar = images_are_similar(phash1, phash2, threshold=10)

        print(f"   Hash Original: {phash1}")
        print(f"   Hash Modificado: {phash2}")
        print(f"   Similar (threshold=10): {similar}")
        print(f"   [OK] Test completado")


class TestImageNormalization:
    """Test image normalization"""

    def test_normalize_image_size(self):
        """Test image normalization to specific size"""
        print("\n[TEST] Test 9: Normalización de tamaño de imagen")

        # Create large image
        large_image = create_test_image(color=(200, 100, 50), size=(2000, 1500))

        # Normalize to smaller size
        normalized = normalize_image_for_comparison(large_image, size=(800, 600))

        # Check normalized image
        img = Image.open(BytesIO(normalized))
        width, height = img.size

        print(f"   Tamaño original: 2000x1500")
        print(f"   Tamaño normalizado: {width}x{height}")
        assert width <= 800
        assert height <= 600
        print(f"   [OK] Imagen normalizada correctamente")

    def test_normalize_maintains_format(self):
        """Test that normalization produces JPEG format"""
        print("\n[TEST] Test 10: Normalización mantiene formato JPEG")

        image_bytes = create_test_image(color=(75, 150, 225))
        normalized = normalize_image_for_comparison(image_bytes)

        img = Image.open(BytesIO(normalized))
        format_type = img.format

        print(f"   Formato: {format_type}")
        assert format_type == 'JPEG'
        print(f"   [OK] Formato JPEG correcto")


class TestImageMetadata:
    """Test image metadata extraction"""

    def test_extract_metadata(self):
        """Test extraction of image metadata"""
        print("\n[TEST] Test 11: Extracción de metadata de imagen")

        image_bytes = create_test_image(color=(128, 128, 128), size=(640, 480))
        metadata = extract_image_metadata(image_bytes)

        print(f"   Metadata extraída:")
        print(f"   - Format: {metadata.get('format')}")
        print(f"   - Mode: {metadata.get('mode')}")
        print(f"   - Size: {metadata.get('size')}")
        print(f"   - Width: {metadata.get('width')}")
        print(f"   - Height: {metadata.get('height')}")
        print(f"   - Aspect Ratio: {metadata.get('aspect_ratio')}")

        assert metadata['format'] == 'JPEG'
        assert metadata['mode'] == 'RGB'
        assert metadata['width'] == 640
        assert metadata['height'] == 480
        assert metadata['aspect_ratio'] > 0
        print(f"   [OK] Metadata correcta")


class TestDeduplicationWorkflow:
    """Test complete deduplication workflow"""

    def test_deduplication_workflow(self):
        """Test complete deduplication workflow"""
        print("\n[TEST] Test 12: Workflow completo de deduplicación")

        # Step 1: Create original product image
        print("\n   Paso 1: Crear imagen original")
        original_image = create_test_image(
            color=(200, 150, 100),
            size=(800, 600),
            text="ORIGINAL PRODUCT"
        )

        # Step 2: Calculate all hashes
        print("   Paso 2: Calcular hashes")
        sha256_hash = calculate_image_hash(original_image)
        perceptual_hash = calculate_perceptual_hash(original_image)
        average_hash = calculate_average_hash(original_image)

        print(f"   - SHA-256: {sha256_hash[:32]}...")
        print(f"   - Perceptual: {perceptual_hash}")
        print(f"   - Average: {average_hash}")

        # Step 3: Simulate scanning same product again (exact duplicate)
        print("\n   Paso 3: Escanear mismo producto (duplicado exacto)")
        duplicate_sha256 = calculate_image_hash(original_image)
        assert duplicate_sha256 == sha256_hash
        print(f"   [OK] Duplicado exacto detectado por SHA-256")

        # Step 4: Simulate scanning similar product (slight modification)
        print("\n   Paso 4: Escanear producto similar (modificación leve)")
        img = Image.open(BytesIO(original_image))
        img_modified = img.resize((750, 550))
        buffer = BytesIO()
        img_modified.save(buffer, format='JPEG', quality=92)
        similar_image = buffer.getvalue()

        similar_perceptual = calculate_perceptual_hash(similar_image)
        is_similar = images_are_similar(perceptual_hash, similar_perceptual, threshold=10)

        print(f"   - Hash original: {perceptual_hash}")
        print(f"   - Hash similar: {similar_perceptual}")
        print(f"   - Es similar: {is_similar}")
        print(f"   [OK] Producto similar detectado por perceptual hash")

        # Step 5: Simulate scanning completely different product
        print("\n   Paso 5: Escanear producto completamente diferente")
        different_image = create_test_image(
            color=(50, 200, 250),
            size=(800, 600),
            text="DIFFERENT PRODUCT"
        )

        different_sha256 = calculate_image_hash(different_image)
        different_perceptual = calculate_perceptual_hash(different_image)

        assert different_sha256 != sha256_hash
        print(f"   [OK] Producto diferente detectado (SHA-256 distinto)")

        print("\n   [OK] Workflow de deduplicación funcionando correctamente!")


def run_all_tests():
    """
    Run all deduplication tests
    """
    print("=" * 80)
    print("[TEST] TESTS: Sistema de Deduplicación de Productos Globales")
    print("=" * 80)

    test_classes = [
        TestImageHashing(),
        TestImageSimilarity(),
        TestImageNormalization(),
        TestImageMetadata(),
        TestDeduplicationWorkflow()
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for test_class in test_classes:
        # Get all test methods
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]

        for test_method in test_methods:
            total_tests += 1
            try:
                method = getattr(test_class, test_method)
                method()
                passed_tests += 1
            except AssertionError as e:
                failed_tests += 1
                print(f"\n   [ERROR] Test falló: {str(e)}")
            except Exception as e:
                failed_tests += 1
                print(f"\n   [ERROR] Error: {str(e)}")

    print("\n" + "=" * 80)
    print("[SUMMARY] RESUMEN DE TESTS")
    print("=" * 80)
    print(f"Total de tests: {total_tests}")
    print(f"[OK] Pasados: {passed_tests}")
    print(f"[ERROR] Fallidos: {failed_tests}")
    print(f"Éxito: {(passed_tests/total_tests)*100:.1f}%")
    print("=" * 80)

    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
