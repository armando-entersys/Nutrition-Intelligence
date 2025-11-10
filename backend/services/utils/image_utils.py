"""
Image utilities for product scanning and deduplication
"""
import hashlib
from io import BytesIO
from PIL import Image
import imagehash
from typing import Tuple, Optional


def calculate_image_hash(image_bytes: bytes, hash_type: str = "sha256") -> str:
    """
    Calculate SHA-256 hash of image bytes for exact duplicate detection

    Args:
        image_bytes: Image data as bytes
        hash_type: Hash algorithm to use (sha256, md5)

    Returns:
        Hexadecimal hash string
    """
    if hash_type == "sha256":
        return hashlib.sha256(image_bytes).hexdigest()
    elif hash_type == "md5":
        return hashlib.md5(image_bytes).hexdigest()
    else:
        raise ValueError(f"Unsupported hash type: {hash_type}")


def calculate_perceptual_hash(image_bytes: bytes) -> str:
    """
    Calculate perceptual hash (pHash) for similar image detection

    This hash is resistant to minor modifications like:
    - Slight compression
    - Minor cropping
    - Brightness/contrast changes

    Args:
        image_bytes: Image data as bytes

    Returns:
        Hexadecimal perceptual hash string
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Calculate perceptual hash
        phash = imagehash.phash(image)
        return str(phash)
    except Exception as e:
        raise ValueError(f"Error calculating perceptual hash: {e}")


def calculate_average_hash(image_bytes: bytes) -> str:
    """
    Calculate average hash (aHash) for quick similarity detection

    Args:
        image_bytes: Image data as bytes

    Returns:
        Hexadecimal average hash string
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')

        ahash = imagehash.average_hash(image)
        return str(ahash)
    except Exception as e:
        raise ValueError(f"Error calculating average hash: {e}")


def images_are_similar(hash1: str, hash2: str, threshold: int = 5) -> bool:
    """
    Compare two perceptual hashes to determine if images are similar

    Args:
        hash1: First hash (from imagehash)
        hash2: Second hash (from imagehash)
        threshold: Maximum hamming distance for similarity (default: 5)
                   0 = identical, <5 = very similar, 5-10 = similar

    Returns:
        True if images are similar, False otherwise
    """
    try:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        distance = h1 - h2  # Hamming distance
        return distance <= threshold
    except Exception:
        return False


def normalize_image_for_comparison(image_bytes: bytes, size: Tuple[int, int] = (800, 600)) -> bytes:
    """
    Normalize image for consistent comparison

    Args:
        image_bytes: Original image bytes
        size: Target size (width, height)

    Returns:
        Normalized image bytes
    """
    try:
        image = Image.open(BytesIO(image_bytes))

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize maintaining aspect ratio
        image.thumbnail(size, Image.Resampling.LANCZOS)

        # Save to bytes
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        raise ValueError(f"Error normalizing image: {e}")


def extract_image_metadata(image_bytes: bytes) -> dict:
    """
    Extract metadata from image

    Args:
        image_bytes: Image data as bytes

    Returns:
        Dictionary with image metadata
    """
    try:
        image = Image.open(BytesIO(image_bytes))

        return {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
            "aspect_ratio": round(image.width / image.height, 2) if image.height > 0 else 0,
        }
    except Exception as e:
        return {"error": str(e)}


# Install imagehash if not installed:
# pip install imagehash
