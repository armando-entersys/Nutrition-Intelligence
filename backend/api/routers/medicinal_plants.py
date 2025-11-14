"""
Medicinal Plants API endpoints
Traditional Mexican Medicine Module
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role, UserRole
from domain.medicinal_plants.models import (
    MedicinalPlant,
    UserPlantLog,
    PlantHealthCondition,
    HerbalShop,
    PlantRecommendation,
    PlantCategory,
    EvidenceLevel,
    SafetyLevel,
    PreparationType
)
from schemas.medicinal_plants import (
    MedicinalPlantCreate,
    MedicinalPlantUpdate,
    MedicinalPlantResponse,
    MedicinalPlantSummary,
    UserPlantLogCreate,
    UserPlantLogUpdate,
    UserPlantLogResponse,
    HerbalShopCreate,
    HerbalShopUpdate,
    HerbalShopResponse,
    PlantSearchFilters,
    PlantListResponse,
    PlantRecommendationRequest,
    PlantRecommendationResponse
)

router = APIRouter()

# ===== Medicinal Plants Endpoints =====

@router.get("/", response_model=PlantListResponse)
async def get_medicinal_plants(
    category: Optional[PlantCategory] = Query(None),
    evidence_level: Optional[EvidenceLevel] = Query(None),
    safety_level: Optional[SafetyLevel] = Query(None),
    state: Optional[str] = Query(None),
    safe_in_pregnancy: Optional[bool] = Query(None),
    safe_for_children: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    featured_only: Optional[bool] = Query(False),
    validated_only: Optional[bool] = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get medicinal plants with filters and pagination

    Applies philosophy: No making assumptions - ask what filters user wants
    """
    try:
        # Build base query
        query = select(MedicinalPlant).where(MedicinalPlant.is_active == True)

        # Apply filters
        filters = []

        if category:
            filters.append(MedicinalPlant.primary_category == category)

        if evidence_level:
            filters.append(MedicinalPlant.evidence_level == evidence_level)

        if safety_level:
            filters.append(MedicinalPlant.safety_level == safety_level)

        if state:
            # Search in states_found JSON array
            filters.append(func.json_contains(MedicinalPlant.states_found, f'"{state}"'))

        if safe_in_pregnancy is not None:
            filters.append(MedicinalPlant.safe_in_pregnancy == safe_in_pregnancy)

        if safe_for_children is not None:
            filters.append(MedicinalPlant.safe_for_children == safe_for_children)

        if search:
            search_filter = or_(
                MedicinalPlant.scientific_name.ilike(f"%{search}%"),
                func.json_contains(MedicinalPlant.popular_names, f'"%{search}%"')
            )
            filters.append(search_filter)

        if featured_only:
            filters.append(MedicinalPlant.featured == True)

        if validated_only:
            filters.append(MedicinalPlant.validated_by_expert == True)

        if filters:
            query = query.where(and_(*filters))

        # Count total results
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # Execute query
        result = await session.execute(query)
        plants = result.scalars().all()

        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size

        # Convert to summary format
        plant_summaries = [
            MedicinalPlantSummary.from_orm(plant) for plant in plants
        ]

        return PlantListResponse(
            plants=plant_summaries,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    except Exception as e:
        print(f"Error in get_medicinal_plants: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching medicinal plants"
        )


@router.get("/featured", response_model=List[MedicinalPlantSummary])
async def get_featured_plants(
    limit: int = Query(6, le=20),
    session: AsyncSession = Depends(get_async_session)
):
    """Get featured medicinal plants for homepage"""
    try:
        query = select(MedicinalPlant).where(
            and_(
                MedicinalPlant.featured == True,
                MedicinalPlant.is_active == True
            )
        ).limit(limit)

        result = await session.execute(query)
        plants = result.scalars().all()

        return [MedicinalPlantSummary.from_orm(plant) for plant in plants]

    except Exception as e:
        print(f"Error in get_featured_plants: {e}")
        return []


@router.get("/categories", response_model=List[dict])
async def get_plant_categories(
    session: AsyncSession = Depends(get_async_session)
):
    """Get all plant categories with counts"""
    try:
        categories = []
        for cat in PlantCategory:
            count_query = select(func.count()).where(
                and_(
                    MedicinalPlant.primary_category == cat,
                    MedicinalPlant.is_active == True
                )
            )
            result = await session.execute(count_query)
            count = result.scalar()

            categories.append({
                "category": cat.value,
                "count": count
            })

        return categories

    except Exception as e:
        print(f"Error in get_plant_categories: {e}")
        return []


@router.get("/{plant_id}", response_model=MedicinalPlantResponse)
async def get_medicinal_plant(
    plant_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get specific medicinal plant by ID

    Increments view count automatically
    """
    plant = await session.get(MedicinalPlant, plant_id)

    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicinal plant not found"
        )

    if not plant.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicinal plant not available"
        )

    # Increment view count
    plant.view_count += 1
    session.add(plant)
    await session.commit()
    await session.refresh(plant)

    return plant


@router.post("/", response_model=MedicinalPlantResponse)
async def create_medicinal_plant(
    plant_data: MedicinalPlantCreate,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create new medicinal plant

    Only ADMIN and NUTRITIONIST roles can create plants
    """
    if current_role not in [UserRole.ADMIN, UserRole.NUTRITIONIST]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and nutritionists can create medicinal plants"
        )

    try:
        # Check if plant with same scientific name already exists
        existing_query = select(MedicinalPlant).where(
            MedicinalPlant.scientific_name == plant_data.scientific_name
        )
        result = await session.execute(existing_query)
        existing_plant = result.scalar_one_or_none()

        if existing_plant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plant with this scientific name already exists"
            )

        # Create new plant
        plant_dict = plant_data.model_dump()

        # Convert PreparationMethodSchema objects to dicts
        if 'preparation_methods' in plant_dict:
            plant_dict['preparation_methods'] = [
                method.model_dump() if hasattr(method, 'model_dump') else method
                for method in plant_dict['preparation_methods']
            ]

        new_plant = MedicinalPlant(**plant_dict)

        session.add(new_plant)
        await session.commit()
        await session.refresh(new_plant)

        return new_plant

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        print(f"Error creating medicinal plant: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating medicinal plant"
        )


@router.put("/{plant_id}", response_model=MedicinalPlantResponse)
async def update_medicinal_plant(
    plant_id: int,
    plant_data: MedicinalPlantUpdate,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Update medicinal plant - ADMIN and NUTRITIONIST only"""
    if current_role not in [UserRole.ADMIN, UserRole.NUTRITIONIST]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and nutritionists can update medicinal plants"
        )

    plant = await session.get(MedicinalPlant, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicinal plant not found"
        )

    try:
        # Update fields
        update_data = plant_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(plant, field, value)

        plant.updated_at = datetime.utcnow()

        session.add(plant)
        await session.commit()
        await session.refresh(plant)

        return plant

    except Exception as e:
        await session.rollback()
        print(f"Error updating medicinal plant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating medicinal plant"
        )


@router.delete("/{plant_id}")
async def delete_medicinal_plant(
    plant_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Soft delete medicinal plant - ADMIN only"""
    if current_role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete medicinal plants"
        )

    plant = await session.get(MedicinalPlant, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicinal plant not found"
        )

    # Soft delete
    plant.is_active = False
    plant.updated_at = datetime.utcnow()

    session.add(plant)
    await session.commit()

    return {"message": "Medicinal plant deleted successfully"}


# ===== User Plant Log Endpoints =====

@router.get("/logs/my-plants", response_model=List[UserPlantLogResponse])
async def get_my_plant_logs(
    current_user_id: int = Depends(get_current_user_id),
    still_using: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current user's plant usage logs"""
    try:
        query = select(UserPlantLog).where(UserPlantLog.user_id == current_user_id)

        if still_using is not None:
            query = query.where(UserPlantLog.still_using == still_using)

        result = await session.execute(query)
        logs = result.scalars().all()

        return logs

    except Exception as e:
        print(f"Error in get_my_plant_logs: {e}")
        return []


@router.post("/logs", response_model=UserPlantLogResponse)
async def create_plant_log(
    log_data: UserPlantLogCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create new plant usage log for current user

    Philosophy: User records their own experience (do your best)
    """
    try:
        # Verify plant exists
        plant = await session.get(MedicinalPlant, log_data.plant_id)
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicinal plant not found"
            )

        log_dict = log_data.model_dump()
        log_dict['user_id'] = current_user_id

        new_log = UserPlantLog(**log_dict)

        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)

        return new_log

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        print(f"Error creating plant log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating plant log"
        )


@router.put("/logs/{log_id}", response_model=UserPlantLogResponse)
async def update_plant_log(
    log_id: int,
    log_data: UserPlantLogUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update plant usage log - only own logs"""
    log = await session.get(UserPlantLog, log_id)

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant log not found"
        )

    if log.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own plant logs"
        )

    try:
        update_data = log_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(log, field, value)

        log.updated_at = datetime.utcnow()

        session.add(log)
        await session.commit()
        await session.refresh(log)

        return log

    except Exception as e:
        await session.rollback()
        print(f"Error updating plant log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating plant log"
        )


# ===== Herbal Shop Endpoints =====

@router.get("/shops/", response_model=List[HerbalShopResponse])
async def get_herbal_shops(
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    shop_type: Optional[str] = Query(None),
    verified_only: Optional[bool] = Query(False),
    limit: int = Query(50, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    """Get herbal shops with filters"""
    try:
        query = select(HerbalShop).where(HerbalShop.is_active == True)

        filters = []

        if city:
            filters.append(HerbalShop.city.ilike(f"%{city}%"))

        if state:
            filters.append(HerbalShop.state.ilike(f"%{state}%"))

        if shop_type:
            filters.append(HerbalShop.shop_type == shop_type)

        if verified_only:
            filters.append(HerbalShop.verified == True)

        if filters:
            query = query.where(and_(*filters))

        query = query.limit(limit)

        result = await session.execute(query)
        shops = result.scalars().all()

        return shops

    except Exception as e:
        print(f"Error in get_herbal_shops: {e}")
        return []


@router.post("/shops/", response_model=HerbalShopResponse)
async def create_herbal_shop(
    shop_data: HerbalShopCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Create new herbal shop - any authenticated user can contribute"""
    try:
        shop_dict = shop_data.model_dump()
        new_shop = HerbalShop(**shop_dict)

        session.add(new_shop)
        await session.commit()
        await session.refresh(new_shop)

        return new_shop

    except Exception as e:
        await session.rollback()
        print(f"Error creating herbal shop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating herbal shop"
        )


# ===== AI Recommendation Endpoints =====

@router.post("/recommendations/generate", response_model=PlantRecommendationResponse)
async def generate_plant_recommendations(
    request: PlantRecommendationRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Generate AI-powered plant recommendations based on user health profile

    Philosophy: Ask questions before recommending (no assumptions)
    TODO: Integrate with Gemini AI for intelligent recommendations
    """
    try:
        # For now, return a placeholder
        # This will be implemented with Gemini AI integration

        recommendation = PlantRecommendation(
            user_id=current_user_id,
            recommended_plants=[],  # Will be populated by AI
            health_conditions=request.health_conditions,
            symptoms=request.symptoms,
            ai_reasoning="AI integration pending",
            confidence_score=0.0,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        session.add(recommendation)
        await session.commit()
        await session.refresh(recommendation)

        return recommendation

    except Exception as e:
        await session.rollback()
        print(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating plant recommendations"
        )
