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
from domain.foods.models import Food, FoodStatus, FoodCategory
from schemas.foods import FoodCreate, FoodUpdate, FoodResponse, FoodSearchParams

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