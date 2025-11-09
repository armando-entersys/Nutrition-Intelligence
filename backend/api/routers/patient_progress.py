"""
Patient Progress & Analytics Router
Advanced analytics and progress tracking for patients
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field

from core.database import get_async_session
from core.security import get_current_user_id, get_current_user_role
from domain.auth.models import UserRole
from domain.patients.models import AnthropometricRecord
from domain.recipes.models import MealPlan, MealEntry

router = APIRouter()

# ============================================================================
# SCHEMAS / DTOs
# ============================================================================

class ProgressDataPoint(BaseModel):
    """Single data point in progress timeline"""
    date: date
    value: float
    label: Optional[str] = None

class ProgressChartResponse(BaseModel):
    """Progress chart data"""
    metric: str
    unit: str
    data_points: List[ProgressDataPoint]
    start_date: date
    end_date: date
    trend: str  # "increasing", "decreasing", "stable"
    change_percentage: Optional[float] = None

class ProgressSummaryResponse(BaseModel):
    """Overall progress summary"""
    patient_id: int
    period_days: int
    start_date: date
    end_date: date

    # Weight metrics
    initial_weight: Optional[float] = None
    current_weight: Optional[float] = None
    weight_change: Optional[float] = None
    weight_change_percentage: Optional[float] = None

    # BMI metrics
    initial_bmi: Optional[float] = None
    current_bmi: Optional[float] = None
    bmi_change: Optional[float] = None

    # Measurements
    waist_change_cm: Optional[float] = None
    hip_change_cm: Optional[float] = None

    # Progress indicators
    total_records: int
    average_records_per_week: float
    trend: str

class AdherenceStats(BaseModel):
    """Meal plan adherence statistics"""
    patient_id: int
    period_start: date
    period_end: date

    total_planned_meals: int
    total_consumed_meals: int
    adherence_percentage: float

    # By meal type
    breakfast_adherence: float
    lunch_adherence: float
    dinner_adherence: float
    snacks_adherence: float

    # Streaks
    current_streak_days: int
    longest_streak_days: int

class ComparisonPeriod(BaseModel):
    """Period comparison data"""
    period: str  # "current_week", "last_week", "current_month", "last_month"
    start_date: date
    end_date: date
    avg_weight: Optional[float] = None
    avg_bmi: Optional[float] = None
    records_count: int

class MilestoneResponse(BaseModel):
    """Achievement milestone"""
    id: str
    title: str
    description: str
    achieved: bool
    achieved_date: Optional[date] = None
    progress_percentage: float
    icon: str

# ============================================================================
# PROGRESS ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/progress/summary", response_model=ProgressSummaryResponse)
async def get_progress_summary(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None),
    days: int = Query(default=30, ge=7, le=365, description="Number of days to analyze")
):
    """
    Get comprehensive progress summary for a patient

    Analyzes anthropometric records over specified period and provides
    summary statistics including weight changes, BMI evolution, and trends.
    """
    # Determine target patient
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own progress"
        )

    # Calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get all records in period
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.patient_id == target_patient_id,
        AnthropometricRecord.measurement_date >= start_date,
        AnthropometricRecord.measurement_date <= end_date
    ).order_by(AnthropometricRecord.measurement_date.asc())

    result = await session.exec(query)
    records = result.all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No anthropometric records found for this period"
        )

    # Get first and last records
    first_record = records[0]
    last_record = records[-1]

    # Calculate changes
    weight_change = None
    weight_change_pct = None
    if first_record.weight and last_record.weight:
        weight_change = last_record.weight - first_record.weight
        weight_change_pct = (weight_change / first_record.weight) * 100

    bmi_change = None
    if first_record.bmi and last_record.bmi:
        bmi_change = last_record.bmi - first_record.bmi

    waist_change = None
    if first_record.waist_cm and last_record.waist_cm:
        waist_change = last_record.waist_cm - first_record.waist_cm

    hip_change = None
    if first_record.hip_cm and last_record.hip_cm:
        hip_change = last_record.hip_cm - first_record.hip_cm

    # Determine trend
    trend = "stable"
    if weight_change:
        if abs(weight_change) > 0.5:  # More than 0.5kg change
            trend = "decreasing" if weight_change < 0 else "increasing"

    # Calculate average records per week
    weeks = days / 7
    avg_records_per_week = len(records) / weeks if weeks > 0 else 0

    return ProgressSummaryResponse(
        patient_id=target_patient_id,
        period_days=days,
        start_date=start_date,
        end_date=end_date,
        initial_weight=first_record.weight,
        current_weight=last_record.weight,
        weight_change=weight_change,
        weight_change_percentage=weight_change_pct,
        initial_bmi=first_record.bmi,
        current_bmi=last_record.bmi,
        bmi_change=bmi_change,
        waist_change_cm=waist_change,
        hip_change_cm=hip_change,
        total_records=len(records),
        average_records_per_week=round(avg_records_per_week, 2),
        trend=trend
    )


@router.get("/progress/chart/{metric}", response_model=ProgressChartResponse)
async def get_progress_chart(
    metric: str,
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None),
    days: int = Query(default=30, ge=7, le=365)
):
    """
    Get chart data for specific metric over time

    Supported metrics: weight, bmi, waist, hip, body_fat
    """
    # Validate metric
    valid_metrics = ["weight", "bmi", "waist", "hip", "body_fat"]
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metric. Must be one of: {', '.join(valid_metrics)}"
        )

    # Determine target patient
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own progress"
        )

    # Calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get records
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.patient_id == target_patient_id,
        AnthropometricRecord.measurement_date >= start_date,
        AnthropometricRecord.measurement_date <= end_date
    ).order_by(AnthropometricRecord.measurement_date.asc())

    result = await session.exec(query)
    records = result.all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found for this period"
        )

    # Extract data points based on metric
    data_points = []
    metric_field_map = {
        "weight": ("weight", "kg"),
        "bmi": ("bmi", "kg/m²"),
        "waist": ("waist_cm", "cm"),
        "hip": ("hip_cm", "cm"),
        "body_fat": ("body_fat_percentage", "%")
    }

    field_name, unit = metric_field_map[metric]

    for record in records:
        value = getattr(record, field_name, None)
        if value is not None:
            data_points.append(ProgressDataPoint(
                date=record.measurement_date,
                value=float(value),
                label=None
            ))

    if not data_points:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {metric} data found for this period"
        )

    # Calculate trend
    if len(data_points) >= 2:
        first_value = data_points[0].value
        last_value = data_points[-1].value
        change = last_value - first_value
        change_pct = (change / first_value * 100) if first_value != 0 else 0

        if abs(change_pct) < 1:
            trend = "stable"
        else:
            trend = "decreasing" if change < 0 else "increasing"
    else:
        trend = "stable"
        change_pct = 0

    return ProgressChartResponse(
        metric=metric,
        unit=unit,
        data_points=data_points,
        start_date=start_date,
        end_date=end_date,
        trend=trend,
        change_percentage=round(change_pct, 2) if change_pct else None
    )


@router.get("/progress/comparison", response_model=List[ComparisonPeriod])
async def get_period_comparison(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None)
):
    """
    Compare patient metrics across different time periods

    Returns averages for: current week, last week, current month, last month
    """
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own progress"
        )

    today = date.today()

    # Define periods
    periods = [
        {
            "name": "current_week",
            "start": today - timedelta(days=today.weekday()),
            "end": today
        },
        {
            "name": "last_week",
            "start": today - timedelta(days=today.weekday() + 7),
            "end": today - timedelta(days=today.weekday() + 1)
        },
        {
            "name": "current_month",
            "start": today.replace(day=1),
            "end": today
        },
        {
            "name": "last_month",
            "start": (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            "end": today.replace(day=1) - timedelta(days=1)
        }
    ]

    comparisons = []

    for period in periods:
        query = select(AnthropometricRecord).where(
            AnthropometricRecord.patient_id == target_patient_id,
            AnthropometricRecord.measurement_date >= period["start"],
            AnthropometricRecord.measurement_date <= period["end"]
        )

        result = await session.exec(query)
        records = result.all()

        # Calculate averages
        avg_weight = None
        avg_bmi = None

        if records:
            weights = [r.weight for r in records if r.weight]
            bmis = [r.bmi for r in records if r.bmi]

            avg_weight = sum(weights) / len(weights) if weights else None
            avg_bmi = sum(bmis) / len(bmis) if bmis else None

        comparisons.append(ComparisonPeriod(
            period=period["name"],
            start_date=period["start"],
            end_date=period["end"],
            avg_weight=round(avg_weight, 2) if avg_weight else None,
            avg_bmi=round(avg_bmi, 2) if avg_bmi else None,
            records_count=len(records)
        ))

    return comparisons


@router.get("/progress/milestones", response_model=List[MilestoneResponse])
async def get_milestones(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None)
):
    """
    Get patient achievement milestones

    Calculates and returns various achievement milestones based on
    progress data, consistency, and goals.
    """
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own milestones"
        )

    # Get all records
    query = select(AnthropometricRecord).where(
        AnthropometricRecord.patient_id == target_patient_id
    ).order_by(AnthropometricRecord.measurement_date.asc())

    result = await session.exec(query)
    records = result.all()

    milestones = []

    if len(records) >= 2:
        first_record = records[0]
        last_record = records[-1]

        # Milestone 1: First weigh-in
        milestones.append(MilestoneResponse(
            id="first_weighin",
            title="¡Primer Registro!",
            description="Completaste tu primera medición antropométrica",
            achieved=True,
            achieved_date=first_record.measurement_date,
            progress_percentage=100.0,
            icon="🎯"
        ))

        # Milestone 2: 5 kg lost (if applicable)
        if first_record.weight and last_record.weight:
            weight_lost = first_record.weight - last_record.weight

            if weight_lost >= 5:
                milestones.append(MilestoneResponse(
                    id="5kg_lost",
                    title="¡5 kg Menos!",
                    description="Has perdido 5 kilogramos",
                    achieved=True,
                    achieved_date=last_record.measurement_date,
                    progress_percentage=100.0,
                    icon="🏆"
                ))
            elif weight_lost > 0:
                progress = (weight_lost / 5) * 100
                milestones.append(MilestoneResponse(
                    id="5kg_lost",
                    title="Meta: 5 kg Menos",
                    description=f"Llevas {weight_lost:.1f} kg de 5 kg",
                    achieved=False,
                    achieved_date=None,
                    progress_percentage=round(progress, 1),
                    icon="🎯"
                ))

        # Milestone 3: Consistency (10 records)
        if len(records) >= 10:
            milestones.append(MilestoneResponse(
                id="consistency_10",
                title="¡Constante!",
                description="Has registrado 10 mediciones",
                achieved=True,
                achieved_date=records[9].measurement_date,
                progress_percentage=100.0,
                icon="📊"
            ))
        else:
            progress = (len(records) / 10) * 100
            milestones.append(MilestoneResponse(
                id="consistency_10",
                title="Meta: 10 Registros",
                description=f"Llevas {len(records)} de 10 registros",
                achieved=False,
                achieved_date=None,
                progress_percentage=round(progress, 1),
                icon="📊"
            ))

        # Milestone 4: One month tracking
        days_tracking = (last_record.measurement_date - first_record.measurement_date).days
        if days_tracking >= 30:
            milestones.append(MilestoneResponse(
                id="one_month",
                title="¡Un Mes!",
                description="Has llevado seguimiento por un mes",
                achieved=True,
                achieved_date=first_record.measurement_date + timedelta(days=30),
                progress_percentage=100.0,
                icon="📅"
            ))
        else:
            progress = (days_tracking / 30) * 100
            milestones.append(MilestoneResponse(
                id="one_month",
                title="Meta: Un Mes",
                description=f"Llevas {days_tracking} de 30 días",
                achieved=False,
                achieved_date=None,
                progress_percentage=round(progress, 1),
                icon="📅"
            ))

    return milestones


@router.get("/progress/adherence", response_model=AdherenceStats)
async def get_adherence_stats(
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session),
    patient_id: Optional[int] = Query(default=None),
    days: int = Query(default=30, ge=7, le=90)
):
    """
    Get meal plan adherence statistics

    Analyzes how well the patient is following their meal plans
    """
    target_patient_id = patient_id if patient_id else current_user_id

    # Verify access
    if current_user_role == UserRole.PATIENT and target_patient_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own adherence stats"
        )

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get active meal plans in period
    plans_query = select(MealPlan).where(
        MealPlan.patient_id == target_patient_id,
        MealPlan.is_active == True,
        MealPlan.start_date <= end_date,
        (MealPlan.end_date >= start_date) | (MealPlan.end_date.is_(None))
    )

    plans_result = await session.exec(plans_query)
    meal_plans = plans_result.all()

    if not meal_plans:
        return AdherenceStats(
            patient_id=target_patient_id,
            period_start=start_date,
            period_end=end_date,
            total_planned_meals=0,
            total_consumed_meals=0,
            adherence_percentage=0.0,
            breakfast_adherence=0.0,
            lunch_adherence=0.0,
            dinner_adherence=0.0,
            snacks_adherence=0.0,
            current_streak_days=0,
            longest_streak_days=0
        )

    # Get all meal entries for these plans
    plan_ids = [p.id for p in meal_plans]

    entries_query = select(MealEntry).where(
        MealEntry.meal_plan_id.in_(plan_ids),
        MealEntry.meal_date >= start_date,
        MealEntry.meal_date <= end_date
    )

    entries_result = await session.exec(entries_query)
    entries = entries_result.all()

    # Calculate statistics
    total_planned = len(entries)
    total_consumed = sum(1 for e in entries if e.consumed)

    adherence_pct = (total_consumed / total_planned * 100) if total_planned > 0 else 0

    # By meal type (simplified - would need meal_type field in MealEntry)
    # For now, returning dummy data
    breakfast_adherence = adherence_pct
    lunch_adherence = adherence_pct
    dinner_adherence = adherence_pct
    snacks_adherence = adherence_pct

    # Calculate streaks (simplified)
    current_streak = 0
    longest_streak = 0

    return AdherenceStats(
        patient_id=target_patient_id,
        period_start=start_date,
        period_end=end_date,
        total_planned_meals=total_planned,
        total_consumed_meals=total_consumed,
        adherence_percentage=round(adherence_pct, 2),
        breakfast_adherence=round(breakfast_adherence, 2),
        lunch_adherence=round(lunch_adherence, 2),
        dinner_adherence=round(dinner_adherence, 2),
        snacks_adherence=round(snacks_adherence, 2),
        current_streak_days=current_streak,
        longest_streak_days=longest_streak
    )
