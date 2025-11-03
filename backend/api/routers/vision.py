"""
AI Vision API Router for food photo analysis
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from services.ai.vision import analyze_food_image, food_vision_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze-food")
async def analyze_food_photo(
    file: UploadFile = File(..., description="Image file of food to analyze")
):
    """
    Analyze a food photo using AI Vision (Gemini/Claude)

    Upload an image of food and get detailed nutritional analysis including:
    - Dish identification
    - Ingredient detection with portions
    - Nutritional breakdown
    - NOM-051 seals analysis
    - Health score
    - Personalized recommendations

    **Supported formats**: JPG, JPEG, PNG, WEBP
    **Max file size**: 10MB
    """
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Supported types: {', '.join(allowed_types)}"
            )

        # Read file content
        image_bytes = await file.read()

        # Validate file size (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {max_size / (1024*1024)}MB"
            )

        logger.info(f"Analyzing food photo: {file.filename} ({len(image_bytes)} bytes)")

        # Analyze image with AI Vision
        result = await analyze_food_image(image_bytes)

        # Add metadata
        result["metadata"] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size_bytes": len(image_bytes),
            "ai_model": food_vision_service.model_mode,
            "gemini_available": food_vision_service.gemini_available,
            "claude_available": food_vision_service.claude_available
        }

        logger.info(
            f"Analysis completed for {file.filename}. "
            f"Confidence: {result.get('confidence_score', 0)}"
        )

        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing food photo: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        )


@router.get("/health")
async def vision_health():
    """
    Check AI Vision service health and configuration
    """
    return {
        "status": "healthy",
        "service": "ai-vision",
        "models": {
            "gemini": {
                "available": food_vision_service.gemini_available,
                "model": "gemini-1.5-pro-latest" if food_vision_service.gemini_available else None
            },
            "claude": {
                "available": food_vision_service.claude_available,
                "model": "claude-3-5-sonnet-20241022" if food_vision_service.claude_available else None
            }
        },
        "mode": food_vision_service.model_mode,
        "confidence_threshold": food_vision_service.gemini_available or food_vision_service.claude_available
    }


@router.get("/config")
async def get_vision_config():
    """
    Get current AI Vision configuration
    """
    return {
        "ai_vision_mode": food_vision_service.model_mode,
        "gemini_available": food_vision_service.gemini_available,
        "claude_available": food_vision_service.claude_available,
        "models": {
            "gemini": "gemini-1.5-pro-latest",
            "claude": "claude-3-5-sonnet-20241022"
        },
        "supported_formats": ["image/jpeg", "image/jpg", "image/png", "image/webp"],
        "max_file_size_mb": 10
    }
