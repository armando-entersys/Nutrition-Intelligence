"""
Notifications Router
Handles user notifications and alerts
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from core.database import get_async_session
from core.security import get_current_user_id
from domain.notifications.models import (
    Notification,
    NotificationType,
    NotificationPriority,
    NotificationStatus
)
from pydantic import BaseModel, Field

router = APIRouter()

# ============================================================================
# SCHEMAS / DTOs
# ============================================================================

class NotificationCreate(BaseModel):
    """Create notification"""
    title: str = Field(max_length=255)
    message: str = Field(max_length=1000)
    icon: Optional[str] = None
    type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.MEDIUM
    action: Optional[dict] = None
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    metadata: Optional[dict] = None
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[int] = None
    scheduled_for: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class NotificationUpdate(BaseModel):
    """Update notification"""
    title: Optional[str] = None
    message: Optional[str] = None
    icon: Optional[str] = None
    type: Optional[NotificationType] = None
    priority: Optional[NotificationPriority] = None
    status: Optional[NotificationStatus] = None
    action: Optional[dict] = None
    action_url: Optional[str] = None
    action_label: Optional[str] = None


class NotificationResponse(BaseModel):
    """Notification response with time_ago"""
    id: int
    user_id: int
    title: str
    message: str
    icon: Optional[str]
    type: str
    priority: str
    status: str
    action: Optional[dict]
    action_url: Optional[str]
    action_label: Optional[str]
    read: bool
    time: str  # Human-readable time ago
    created_at: datetime
    read_at: Optional[datetime]

    class Config:
        from_attributes = True


class UnreadCountResponse(BaseModel):
    """Unread notifications count"""
    count: int
    unread_count: int  # Alias for compatibility


# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

@router.get("", response_model=List[NotificationResponse])
async def get_notifications(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
    unread_only: bool = Query(default=False, description="Filter for unread notifications only"),
    limit: int = Query(default=50, le=100, description="Maximum number of notifications to return"),
    offset: int = Query(default=0, ge=0, description="Number of notifications to skip"),
    type: Optional[NotificationType] = Query(default=None, description="Filter by notification type"),
    priority: Optional[NotificationPriority] = Query(default=None, description="Filter by priority")
):
    """
    Get notifications for the current user

    Returns notifications ordered by created_at (newest first)
    """
    # Build query
    query = select(Notification).where(Notification.user_id == current_user_id)

    # Apply filters
    if unread_only:
        query = query.where(Notification.status == NotificationStatus.UNREAD)

    if type:
        query = query.where(Notification.type == type)

    if priority:
        query = query.where(Notification.priority == priority)

    # Order and pagination
    query = (
        query
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.exec(query)
    notifications = result.all()

    # Transform to response model with time_ago
    response_notifications = []
    for notif in notifications:
        response_notifications.append(
            NotificationResponse(
                id=notif.id,
                user_id=notif.user_id,
                title=notif.title,
                message=notif.message,
                icon=notif.icon,
                type=notif.type.value,
                priority=notif.priority.value,
                status=notif.status.value,
                action=notif.action,
                action_url=notif.action_url,
                action_label=notif.action_label,
                read=notif.is_read,
                time=notif.time_ago,
                created_at=notif.created_at,
                read_at=notif.read_at
            )
        )

    return response_notifications


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get count of unread notifications for the current user"""
    query = select(Notification).where(
        Notification.user_id == current_user_id,
        Notification.status == NotificationStatus.UNREAD
    )

    result = await session.exec(query)
    notifications = result.all()
    count = len(notifications)

    return UnreadCountResponse(count=count, unread_count=count)


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific notification by ID"""
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user_id
    )
    result = await session.exec(query)
    notification = result.first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        icon=notification.icon,
        type=notification.type.value,
        priority=notification.priority.value,
        status=notification.status.value,
        action=notification.action,
        action_url=notification.action_url,
        action_label=notification.action_label,
        read=notification.is_read,
        time=notification.time_ago,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new notification for the current user

    This endpoint allows users to create notifications (useful for testing or custom notifications)
    """
    notification = Notification(
        user_id=current_user_id,
        **notification_data.model_dump()
    )

    session.add(notification)
    await session.commit()
    await session.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        icon=notification.icon,
        type=notification.type.value,
        priority=notification.priority.value,
        status=notification.status.value,
        action=notification.action,
        action_url=notification.action_url,
        action_label=notification.action_label,
        read=notification.is_read,
        time=notification.time_ago,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Mark a notification as read"""
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user_id
    )
    result = await session.exec(query)
    notification = result.first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.mark_as_read()
    await session.commit()
    await session.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        icon=notification.icon,
        type=notification.type.value,
        priority=notification.priority.value,
        status=notification.status.value,
        action=notification.action,
        action_url=notification.action_url,
        action_label=notification.action_label,
        read=notification.is_read,
        time=notification.time_ago,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.put("/mark-all-read", response_model=dict)
async def mark_all_notifications_as_read(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Mark all unread notifications as read"""
    query = select(Notification).where(
        Notification.user_id == current_user_id,
        Notification.status == NotificationStatus.UNREAD
    )
    result = await session.exec(query)
    notifications = result.all()

    count = 0
    for notification in notifications:
        notification.mark_as_read()
        count += 1

    await session.commit()

    return {
        "message": f"{count} notifications marked as read",
        "count": count
    }


@router.put("/{notification_id}/unread", response_model=NotificationResponse)
async def mark_notification_as_unread(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Mark a notification as unread"""
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user_id
    )
    result = await session.exec(query)
    notification = result.first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.mark_as_unread()
    await session.commit()
    await session.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        icon=notification.icon,
        type=notification.type.value,
        priority=notification.priority.value,
        status=notification.status.value,
        action=notification.action,
        action_url=notification.action_url,
        action_label=notification.action_label,
        read=notification.is_read,
        time=notification.time_ago,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.put("/{notification_id}/archive", response_model=NotificationResponse)
async def archive_notification(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Archive a notification"""
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user_id
    )
    result = await session.exec(query)
    notification = result.first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.archive()
    await session.commit()
    await session.refresh(notification)

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        icon=notification.icon,
        type=notification.type.value,
        priority=notification.priority.value,
        status=notification.status.value,
        action=notification.action,
        action_url=notification.action_url,
        action_label=notification.action_label,
        read=notification.is_read,
        time=notification.time_ago,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a notification"""
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user_id
    )
    result = await session.exec(query)
    notification = result.first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    await session.delete(notification)
    await session.commit()

    return None


@router.delete("/all/clear", status_code=status.HTTP_200_OK)
async def clear_all_notifications(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete all notifications for the current user (read and archived only)"""
    query = select(Notification).where(
        Notification.user_id == current_user_id,
        Notification.status.in_([NotificationStatus.READ, NotificationStatus.ARCHIVED])
    )
    result = await session.exec(query)
    notifications = result.all()

    count = 0
    for notification in notifications:
        await session.delete(notification)
        count += 1

    await session.commit()

    return {
        "message": f"{count} notifications deleted",
        "count": count
    }
