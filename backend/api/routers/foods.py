"""
Food management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role, UserRole
from domain.foods.models import Food, FoodStatus, FoodCategory, FavoriteFood
from schemas.foods import FoodCreate, FoodUpdate, FoodResponse, FoodSearchParams
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[FoodResponse])
async def get_foods(
    status: Optional[FoodStatus] = Query(None),
    category: Optional[FoodCategory] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    session: AsyncSession = Depends(get_async_session)
):
    """Get foods with filters"""

    try:
        query = select(Food)

        # Apply simple filters without complex operations
        filters = []
        if status:
            filters.append(Food.status == status)
        if category:
            filters.append(Food.category == category)
        if search:
            filters.append(Food.name.ilike(f"%{search}%"))

        if filters:
            query = query.where(and_(*filters))

        # Apply pagination
        query = query.offset(offset).limit(limit)

        result = await session.execute(query)
        foods = result.scalars().all()

        return foods
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_foods: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list if there's an error
        return []

@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get specific food by ID"""
    
    food = await session.get(Food, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    return food

@router.post("/", response_model=FoodResponse)
async def create_food(
    food_data: FoodCreate,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Create new food item (requires approval unless admin)"""
    
    # Create food item
    food = Food(
        **food_data.dict(),
        proposed_by_id=current_user_id,
        status=FoodStatus.APPROVED if current_role == UserRole.ADMIN else FoodStatus.PENDING
    )
    
    # Auto-approve if admin
    if current_role == UserRole.ADMIN:
        food.approved_by_id = current_user_id
        food.approved_at = datetime.utcnow()
    
    session.add(food)
    await session.commit()
    await session.refresh(food)
    
    return food

@router.put("/{food_id}", response_model=FoodResponse)
async def update_food(
    food_id: int,
    food_data: FoodUpdate,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Update food item"""
    
    food = await session.get(Food, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    # Check permissions
    can_edit = (
        current_role == UserRole.ADMIN or
        (current_role == UserRole.NUTRITIONIST and food.status == FoodStatus.PENDING) or
        food.proposed_by_id == current_user_id
    )
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this food item"
        )
    
    # Update fields
    update_data = food_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(food, field, value)
    
    food.updated_at = datetime.utcnow()
    
    # Reset approval if content changed (unless admin)
    if current_role != UserRole.ADMIN and food.status == FoodStatus.APPROVED:
        food.status = FoodStatus.PENDING
        food.approved_by_id = None
        food.approved_at = None
    
    await session.commit()
    await session.refresh(food)
    
    return food

@router.post("/{food_id}/approve")
async def approve_food(
    food_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Approve pending food item (nutritionist/admin only)"""
    
    if current_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can approve foods"
        )
    
    food = await session.get(Food, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    if food.status != FoodStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food is not pending approval"
        )
    
    food.status = FoodStatus.APPROVED
    food.approved_by_id = current_user_id
    food.approved_at = datetime.utcnow()
    
    await session.commit()
    
    return {"message": "Food approved successfully"}

@router.post("/{food_id}/reject")
async def reject_food(
    food_id: int,
    reason: str,
    current_user_id: int = Depends(get_current_user_id),
    current_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Reject pending food item (nutritionist/admin only)"""
    
    if current_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can reject foods"
        )
    
    food = await session.get(Food, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    if food.status != FoodStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food is not pending approval"
        )
    
    food.status = FoodStatus.REJECTED
    food.approved_by_id = current_user_id
    food.approved_at = datetime.utcnow()
    # Store rejection reason in description or separate field
    
    await session.commit()
    
    return {"message": "Food rejected successfully"}

@router.get("/categories/", response_model=List[str])
async def get_food_categories():
    """Get list of food categories"""
    return [category.value for category in FoodCategory]

@router.get("/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, le=20),
    session: AsyncSession = Depends(get_async_session)
):
    """Get food search suggestions"""

    query = select(Food.name).where(
        and_(
            Food.status == FoodStatus.APPROVED,
            Food.name.ilike(f"%{q}%")
        )
    ).limit(limit)

    result = await session.execute(query)
    suggestions = result.scalars().all()

    return {"suggestions": suggestions}


# ============================================================================
# FAVORITE FOODS ENDPOINTS
# ============================================================================

@router.post("/favorites/{food_id}")
async def add_to_favorites(
    food_id: int,
    notes: Optional[str] = None,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Add food to user's favorites"""

    # Check if food exists
    food = await session.get(Food, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )

    # Check if already favorited
    existing_query = select(FavoriteFood).where(
        and_(
            FavoriteFood.user_id == current_user_id,
            FavoriteFood.food_id == food_id
        )
    )
    result = await session.execute(existing_query)
    existing = result.scalar_one_or_none()

    if existing:
        # Update notes if provided
        if notes is not None:
            existing.notes = notes
            await session.commit()
        return {
            "message": "Food already in favorites",
            "is_new": False,
            "favorite_id": existing.id
        }

    # Create new favorite
    favorite = FavoriteFood(
        user_id=current_user_id,
        food_id=food_id,
        notes=notes
    )

    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)

    return {
        "message": "Food added to favorites",
        "is_new": True,
        "favorite_id": favorite.id
    }


@router.delete("/favorites/{food_id}")
async def remove_from_favorites(
    food_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Remove food from user's favorites"""

    # Find the favorite
    query = select(FavoriteFood).where(
        and_(
            FavoriteFood.user_id == current_user_id,
            FavoriteFood.food_id == food_id
        )
    )
    result = await session.execute(query)
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not in favorites"
        )

    await session.delete(favorite)
    await session.commit()

    return {"message": "Food removed from favorites"}


@router.get("/favorites", response_model=List[FoodResponse])
async def get_user_favorites(
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get user's favorite foods"""

    # Query favorites with food details
    query = (
        select(Food)
        .join(FavoriteFood, Food.id == FavoriteFood.food_id)
        .where(FavoriteFood.user_id == current_user_id)
        .order_by(FavoriteFood.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    result = await session.execute(query)
    foods = result.scalars().all()

    return foods


@router.get("/{food_id}/is-favorite")
async def check_is_favorite(
    food_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Check if a food is in user's favorites"""

    query = select(FavoriteFood).where(
        and_(
            FavoriteFood.user_id == current_user_id,
            FavoriteFood.food_id == food_id
        )
    )
    result = await session.execute(query)
    favorite = result.scalar_one_or_none()

    return {
        "is_favorite": favorite is not None,
        "favorite_id": favorite.id if favorite else None,
        "notes": favorite.notes if favorite else None,
        "created_at": favorite.created_at if favorite else None
    }


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/statistics/top-favorites")
async def get_top_favorite_foods(
    limit: int = Query(10, le=50),
    session: AsyncSession = Depends(get_async_session)
):
    """Get most favorited foods across all users"""

    # Count favorites per food
    query = (
        select(
            Food,
            func.count(FavoriteFood.id).label('favorite_count')
        )
        .join(FavoriteFood, Food.id == FavoriteFood.food_id)
        .where(Food.status == FoodStatus.APPROVED)
        .group_by(Food.id)
        .order_by(func.count(FavoriteFood.id).desc())
        .limit(limit)
    )

    result = await session.execute(query)
    rows = result.all()

    return [
        {
            "food": row[0],
            "favorite_count": row[1]
        }
        for row in rows
    ]


@router.get("/statistics/by-category")
async def get_statistics_by_category(
    session: AsyncSession = Depends(get_async_session)
):
    """Get food statistics grouped by category"""

    # Get statistics per category
    query = (
        select(
            Food.category,
            func.count(Food.id).label('total_foods'),
            func.avg(Food.calories_per_serving).label('avg_calories'),
            func.avg(Food.protein_g).label('avg_protein'),
            func.avg(Food.carbs_g).label('avg_carbs'),
            func.avg(Food.fat_g).label('avg_fat'),
            func.count(FavoriteFood.id).label('total_favorites')
        )
        .outerjoin(FavoriteFood, Food.id == FavoriteFood.food_id)
        .where(Food.status == FoodStatus.APPROVED)
        .group_by(Food.category)
        .order_by(Food.category)
    )

    result = await session.execute(query)
    rows = result.all()

    return [
        {
            "category": row[0],
            "total_foods": row[1],
            "avg_calories": round(float(row[2]) if row[2] else 0, 2),
            "avg_protein_g": round(float(row[3]) if row[3] else 0, 2),
            "avg_carbs_g": round(float(row[4]) if row[4] else 0, 2),
            "avg_fat_g": round(float(row[5]) if row[5] else 0, 2),
            "total_favorites": row[6] if row[6] else 0
        }
        for row in rows
    ]


@router.get("/statistics/user-summary")
async def get_user_food_summary(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get summary of user's food interactions"""

    # Count user's favorites
    favorites_query = select(func.count(FavoriteFood.id)).where(
        FavoriteFood.user_id == current_user_id
    )
    favorites_result = await session.execute(favorites_query)
    total_favorites = favorites_result.scalar() or 0

    # Get category distribution of favorites
    category_query = (
        select(
            Food.category,
            func.count(FavoriteFood.id).label('count')
        )
        .join(FavoriteFood, Food.id == FavoriteFood.food_id)
        .where(FavoriteFood.user_id == current_user_id)
        .group_by(Food.category)
        .order_by(func.count(FavoriteFood.id).desc())
    )
    category_result = await session.execute(category_query)
    category_distribution = [
        {"category": row[0], "count": row[1]}
        for row in category_result.all()
    ]

    # Get most recent favorites
    recent_query = (
        select(Food)
        .join(FavoriteFood, Food.id == FavoriteFood.food_id)
        .where(FavoriteFood.user_id == current_user_id)
        .order_by(FavoriteFood.created_at.desc())
        .limit(5)
    )
    recent_result = await session.execute(recent_query)
    recent_favorites = recent_result.scalars().all()

    return {
        "total_favorites": total_favorites,
        "category_distribution": category_distribution,
        "recent_favorites": recent_favorites,
        "top_category": category_distribution[0]["category"] if category_distribution else None
    }