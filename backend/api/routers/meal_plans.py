"""
Meal Plans Router
Complete meal planning system with basic and weekly plans
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role
from domain.auth.models import UserRole
from domain.recipes.models import (
    MealPlan,
    MealEntry,
    MealType,
    Recipe
)
from domain.meal_plans.weekly_planner import (
    WeeklyMealPlan,
    DailyMealPlan,
    MealAssignment,
    PlanStatus,
    WeekDay
)

router = APIRouter()

# ============================================================================
# SCHEMAS / DTOs
# ============================================================================

class MealPlanCreate(BaseModel):
    """Create basic meal plan"""
    patient_id: int
    name: str = Field(max_length=200)
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    daily_calories_target: float
    daily_protein_target: float
    daily_carbs_target: float
    daily_fat_target: float
    generated_by: str = Field(default="manual", max_length=20)
    generation_params: Optional[dict] = None


class MealPlanUpdate(BaseModel):
    """Update basic meal plan"""
    name: Optional[str] = None
    description: Optional[str] = None
    end_date: Optional[date] = None
    daily_calories_target: Optional[float] = None
    daily_protein_target: Optional[float] = None
    daily_carbs_target: Optional[float] = None
    daily_fat_target: Optional[float] = None
    is_active: Optional[bool] = None


class MealPlanResponse(BaseModel):
    """Basic meal plan response"""
    id: int
    patient_id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: Optional[date]
    daily_calories_target: float
    daily_protein_target: float
    daily_carbs_target: float
    daily_fat_target: float
    is_active: bool
    approved_by_nutritionist: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MealEntryCreate(BaseModel):
    """Create meal entry"""
    meal_date: date
    meal_type: MealType
    recipe_id: Optional[int] = None
    recipe_servings: Optional[float] = 1.0
    ad_hoc_items: Optional[List[dict]] = None  # [{food_id, quantity, unit}]


class MealEntryUpdate(BaseModel):
    """Update meal entry"""
    meal_type: Optional[MealType] = None
    recipe_id: Optional[int] = None
    recipe_servings: Optional[float] = None
    consumed: Optional[bool] = None
    consumption_notes: Optional[str] = None


class MealEntryResponse(BaseModel):
    """Meal entry response"""
    id: int
    meal_plan_id: int
    meal_date: date
    meal_type: str
    recipe_id: Optional[int]
    recipe_servings: Optional[float]
    consumed: bool
    consumed_at: Optional[datetime]
    planned_calories: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class WeeklyMealPlanCreate(BaseModel):
    """Create weekly meal plan"""
    patient_id: int
    nutritionist_id: int
    plan_name: str = Field(max_length=200)
    description: Optional[str] = None
    week_start_date: date
    target_calories_per_day: float
    target_equivalents: dict  # {group: amount}
    allow_substitutions: bool = True
    nutritionist_notes: Optional[str] = None
    patient_instructions: Optional[str] = None


class WeeklyMealPlanUpdate(BaseModel):
    """Update weekly meal plan"""
    plan_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[PlanStatus] = None
    allow_substitutions: Optional[bool] = None
    nutritionist_notes: Optional[str] = None
    patient_instructions: Optional[str] = None


class WeeklyMealPlanResponse(BaseModel):
    """Weekly meal plan response"""
    id: int
    patient_id: int
    nutritionist_id: int
    plan_name: str
    description: Optional[str]
    week_start_date: date
    week_end_date: date
    status: str
    target_calories_per_day: float
    completion_percentage: float
    is_current_week: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DailyMealPlanCreate(BaseModel):
    """Create daily meal plan"""
    plan_date: date
    week_day: WeekDay
    daily_calorie_target: float
    daily_equivalents_target: dict
    daily_notes: Optional[str] = None
    special_instructions: Optional[str] = None


class MealAssignmentCreate(BaseModel):
    """Create meal assignment"""
    recipe_id: int
    meal_type: MealType
    planned_time: Optional[str] = None  # "08:00"
    servings: float = 1.0
    calculated_equivalents: dict
    calculated_calories: float
    preparation_notes: Optional[str] = None
    priority: int = Field(default=3, ge=1, le=5)


class MealAssignmentUpdate(BaseModel):
    """Update meal assignment"""
    servings: Optional[float] = None
    is_consumed: Optional[bool] = None
    actual_servings: Optional[float] = None
    patient_rating: Optional[int] = Field(default=None, ge=1, le=5)
    patient_comments: Optional[str] = None


# ============================================================================
# BASIC MEAL PLANS ENDPOINTS
# ============================================================================

@router.get("", response_model=List[MealPlanResponse])
async def get_meal_plans(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None, description="Filter by patient ID"),
    is_active: Optional[bool] = Query(default=None, description="Filter by active status"),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Get meal plans

    - Patients can only see their own meal plans
    - Nutritionists can see meal plans for their assigned patients
    - Admins can see all meal plans
    """
    query = select(MealPlan)

    # Apply role-based filtering
    if current_user_role == UserRole.PATIENT:
        # Patients see only their own plans
        query = query.where(MealPlan.patient_id == current_user_id)
    elif current_user_role == UserRole.NUTRITIONIST:
        # Nutritionists see plans for their assigned patients
        # TODO: Add join with patients table to filter by nutritionist_id
        if patient_id:
            query = query.where(MealPlan.patient_id == patient_id)
    # Admins see all plans (no additional filter)

    # Apply optional filters
    if patient_id and current_user_role == UserRole.ADMIN:
        query = query.where(MealPlan.patient_id == patient_id)

    if is_active is not None:
        query = query.where(MealPlan.is_active == is_active)

    # Order and paginate
    query = (
        query
        .order_by(MealPlan.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.exec(query)
    meal_plans = result.all()

    return [MealPlanResponse.model_validate(mp) for mp in meal_plans]


@router.get("/{meal_plan_id}", response_model=MealPlanResponse)
async def get_meal_plan(
    meal_plan_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Get specific meal plan by ID"""
    query = select(MealPlan).where(MealPlan.id == meal_plan_id)
    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Verify access
    if current_user_role == UserRole.PATIENT:
        if meal_plan.patient_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own meal plans"
            )

    return MealPlanResponse.model_validate(meal_plan)


@router.get("/{patient_id}/today", response_model=Optional[MealPlanResponse])
async def get_today_meal_plan(
    patient_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Get today's active meal plan for a patient"""
    # Verify access
    if current_user_role == UserRole.PATIENT and patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own meal plans"
        )

    today = date.today()

    query = select(MealPlan).where(
        MealPlan.patient_id == patient_id,
        MealPlan.start_date <= today,
        (MealPlan.end_date >= today) | (MealPlan.end_date.is_(None)),
        MealPlan.is_active == True
    )

    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        return None

    return MealPlanResponse.model_validate(meal_plan)


@router.post("", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_meal_plan(
    meal_plan_data: MealPlanCreate,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create new meal plan

    Only nutritionists and admins can create meal plans
    """
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can create meal plans"
        )

    # Validate dates
    if meal_plan_data.end_date and meal_plan_data.end_date < meal_plan_data.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date"
        )

    meal_plan = MealPlan(
        **meal_plan_data.model_dump(),
        created_by_id=current_user_id,
        created_at=datetime.utcnow()
    )

    session.add(meal_plan)
    await session.commit()
    await session.refresh(meal_plan)

    return MealPlanResponse.model_validate(meal_plan)


@router.put("/{meal_plan_id}", response_model=MealPlanResponse)
async def update_meal_plan(
    meal_plan_id: int,
    meal_plan_data: MealPlanUpdate,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Update meal plan"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can update meal plans"
        )

    query = select(MealPlan).where(MealPlan.id == meal_plan_id)
    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Update fields
    update_data = meal_plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal_plan, field, value)

    meal_plan.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(meal_plan)

    return MealPlanResponse.model_validate(meal_plan)


@router.delete("/{meal_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal_plan(
    meal_plan_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete meal plan"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can delete meal plans"
        )

    query = select(MealPlan).where(MealPlan.id == meal_plan_id)
    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    await session.delete(meal_plan)
    await session.commit()

    return None


# ============================================================================
# MEAL ENTRIES ENDPOINTS
# ============================================================================

@router.get("/{meal_plan_id}/entries", response_model=List[MealEntryResponse])
async def get_meal_entries(
    meal_plan_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    meal_type: Optional[MealType] = Query(default=None)
):
    """Get meal entries for a meal plan"""
    # Verify meal plan exists
    query = select(MealPlan).where(MealPlan.id == meal_plan_id)
    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Get entries
    query = select(MealEntry).where(MealEntry.meal_plan_id == meal_plan_id)

    if start_date:
        query = query.where(MealEntry.meal_date >= start_date)
    if end_date:
        query = query.where(MealEntry.meal_date <= end_date)
    if meal_type:
        query = query.where(MealEntry.meal_type == meal_type)

    query = query.order_by(MealEntry.meal_date.asc(), MealEntry.created_at.asc())

    result = await session.exec(query)
    entries = result.all()

    return [MealEntryResponse.model_validate(e) for e in entries]


@router.post("/{meal_plan_id}/entries", response_model=MealEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_meal_entry(
    meal_plan_id: int,
    entry_data: MealEntryCreate,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Add meal entry to meal plan"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can add meal entries"
        )

    # Verify meal plan exists
    query = select(MealPlan).where(MealPlan.id == meal_plan_id)
    result = await session.exec(query)
    meal_plan = result.first()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Create entry
    entry = MealEntry(
        meal_plan_id=meal_plan_id,
        **entry_data.model_dump(),
        created_at=datetime.utcnow()
    )

    session.add(entry)
    await session.commit()
    await session.refresh(entry)

    return MealEntryResponse.model_validate(entry)


@router.put("/{meal_plan_id}/entries/{entry_id}", response_model=MealEntryResponse)
async def update_meal_entry(
    meal_plan_id: int,
    entry_id: int,
    entry_data: MealEntryUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Update meal entry"""
    query = select(MealEntry).where(
        MealEntry.id == entry_id,
        MealEntry.meal_plan_id == meal_plan_id
    )
    result = await session.exec(query)
    entry = result.first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal entry not found"
        )

    # Update fields
    update_data = entry_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)

    # If marking as consumed, set timestamp
    if update_data.get("consumed") and not entry.consumed_at:
        entry.consumed_at = datetime.utcnow()

    entry.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(entry)

    return MealEntryResponse.model_validate(entry)


@router.delete("/{meal_plan_id}/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal_entry(
    meal_plan_id: int,
    entry_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete meal entry"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can delete meal entries"
        )

    query = select(MealEntry).where(
        MealEntry.id == entry_id,
        MealEntry.meal_plan_id == meal_plan_id
    )
    result = await session.exec(query)
    entry = result.first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal entry not found"
        )

    await session.delete(entry)
    await session.commit()

    return None


# ============================================================================
# WEEKLY MEAL PLANS ENDPOINTS
# ============================================================================

@router.get("/weekly", response_model=List[WeeklyMealPlanResponse])
async def get_weekly_meal_plans(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None),
    status: Optional[PlanStatus] = Query(default=None),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Get weekly meal plans"""
    query = select(WeeklyMealPlan)

    # Apply role-based filtering
    if current_user_role == UserRole.PATIENT:
        query = query.where(WeeklyMealPlan.patient_id == current_user_id)
    elif current_user_role == UserRole.NUTRITIONIST:
        if patient_id:
            query = query.where(WeeklyMealPlan.patient_id == patient_id)
        else:
            query = query.where(WeeklyMealPlan.nutritionist_id == current_user_id)
    elif patient_id:
        query = query.where(WeeklyMealPlan.patient_id == patient_id)

    if status:
        query = query.where(WeeklyMealPlan.status == status)

    query = (
        query
        .order_by(WeeklyMealPlan.week_start_date.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.exec(query)
    plans = result.all()

    return [WeeklyMealPlanResponse.model_validate(p) for p in plans]


@router.get("/weekly/current", response_model=Optional[WeeklyMealPlanResponse])
async def get_current_weekly_plan(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None)
):
    """Get current week's meal plan"""
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own meal plans"
        )

    today = date.today()

    query = select(WeeklyMealPlan).where(
        WeeklyMealPlan.patient_id == target_patient_id,
        WeeklyMealPlan.week_start_date <= today,
        WeeklyMealPlan.week_end_date >= today,
        WeeklyMealPlan.status == PlanStatus.ACTIVE
    )

    result = await session.exec(query)
    plan = result.first()

    if not plan:
        return None

    return WeeklyMealPlanResponse.model_validate(plan)


@router.post("/weekly", response_model=WeeklyMealPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_weekly_meal_plan(
    plan_data: WeeklyMealPlanCreate,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Create weekly meal plan"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can create weekly meal plans"
        )

    # Calculate week end date (always Sunday, 6 days after start)
    week_end_date = plan_data.week_start_date + timedelta(days=6)

    plan = WeeklyMealPlan(
        **plan_data.model_dump(),
        week_end_date=week_end_date,
        created_at=datetime.utcnow()
    )

    session.add(plan)
    await session.commit()
    await session.refresh(plan)

    return WeeklyMealPlanResponse.model_validate(plan)


@router.put("/weekly/{plan_id}/publish", response_model=WeeklyMealPlanResponse)
async def publish_weekly_plan(
    plan_id: int,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    """Publish weekly meal plan (change status to ACTIVE)"""
    if current_user_role not in [UserRole.NUTRITIONIST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only nutritionists and admins can publish meal plans"
        )

    query = select(WeeklyMealPlan).where(WeeklyMealPlan.id == plan_id)
    result = await session.exec(query)
    plan = result.first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weekly meal plan not found"
        )

    plan.status = PlanStatus.ACTIVE
    plan.published_at = datetime.utcnow()
    plan.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(plan)

    return WeeklyMealPlanResponse.model_validate(plan)
