from typing import Optional, List, Dict
from datetime import datetime, date, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from domain.fasting.models import FastingWindow, FastingLog, FastingStats
from domain.users.models import User

class FastingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_window(self, user_id: int) -> Optional[FastingWindow]:
        """Get user's active fasting window."""
        stmt = select(FastingWindow).where(
            FastingWindow.user_id == user_id,
            FastingWindow.active == True
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def configure_window(self, user_id: int, start_time: time, end_time: time) -> FastingWindow:
        """Configure or update user's fasting window."""
        # Deactivate existing windows
        existing = await self.get_window(user_id)
        if existing:
            existing.active = False
            self.session.add(existing)
        
        # Calculate duration
        # Handle overnight windows (e.g. 20:00 to 12:00 next day)
        # But usually eating window is during day. Let's assume simple case first.
        # If end < start, it crosses midnight.
        start_dt = datetime.combine(date.today(), start_time)
        end_dt = datetime.combine(date.today(), end_time)
        
        if end_time < start_time:
            end_dt += timedelta(days=1)
            
        duration = (end_dt - start_dt).total_seconds() / 3600
        
        window = FastingWindow(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            duration_hours=int(duration),
            active=True
        )
        self.session.add(window)
        await self.session.commit()
        await self.session.refresh(window)
        return window

    async def get_current_status(self, user_id: int) -> FastingStats:
        """Calculate real-time fasting status."""
        window = await self.get_window(user_id)
        if not window:
            # Return empty/default stats if no window configured
            return self._empty_stats()

        now = datetime.now()
        current_time = now.time()
        
        # Determine if in eating window
        # Simple case: start < end (e.g. 10:00 to 18:00)
        # Overnight: start > end (e.g. 18:00 to 02:00)
        in_window = False
        if window.start_time < window.end_time:
            in_window = window.start_time <= current_time <= window.end_time
        else:
            # Overnight window
            in_window = current_time >= window.start_time or current_time <= window.end_time

        # Calculate fasting hours (time since last meal)
        # Get last log
        stmt = select(FastingLog).where(FastingLog.user_id == user_id).order_by(desc(FastingLog.log_date)).limit(1)
        result = await self.session.execute(stmt)
        last_log = result.scalar_one_or_none()
        
        current_fast_hours = 0.0
        if last_log and last_log.last_meal_time:
            diff = now - last_log.last_meal_time
            current_fast_hours = diff.total_seconds() / 3600
        
        # Autophagy starts after 12 hours
        autophagy_active = current_fast_hours > 12
        
        # Calculate time until next state change
        # TODO: Implement precise time calculation
        
        return FastingStats(
            in_fasting_window=not in_window, # If not in eating window, we are fasting
            current_fast_hours=round(current_fast_hours, 1),
            autophagy_active=autophagy_active,
            window_start=window.start_time.strftime("%H:%M"),
            window_end=window.end_time.strftime("%H:%M"),
            time_until_window_start=0, # Placeholder
            time_until_window_end=0,   # Placeholder
            adherence_7d=0.0,          # Placeholder
            adherence_30d=0.0,         # Placeholder
            total_autophagy_hours_7d=0.0,
            total_autophagy_hours_30d=0.0,
            avg_fasting_hours_7d=0.0,
            avg_fasting_hours_30d=0.0,
            current_streak=0,
            longest_streak=0
        )

    def _empty_stats(self) -> FastingStats:
        return FastingStats(
            in_fasting_window=False,
            current_fast_hours=0.0,
            autophagy_active=False,
            window_start="--:--",
            window_end="--:--",
            time_until_window_start=0,
            time_until_window_end=0,
            adherence_7d=0.0,
            adherence_30d=0.0,
            total_autophagy_hours_7d=0.0,
            total_autophagy_hours_30d=0.0,
            avg_fasting_hours_7d=0.0,
            avg_fasting_hours_30d=0.0,
            current_streak=0,
            longest_streak=0
        )

    async def log_meal(self, user_id: int, meal_time: datetime = None) -> FastingLog:
        """Log a meal (either first or last of the day)."""
        if not meal_time:
            meal_time = datetime.now()
            
        today = meal_time.date()
        
        # Get or create log for today
        stmt = select(FastingLog).where(
            FastingLog.user_id == user_id,
            FastingLog.log_date == today
        )
        result = await self.session.execute(stmt)
        log = result.scalar_one_or_none()
        
        window = await self.get_window(user_id)
        if not window:
            # Should probably error or create default window
            pass

        if not log:
            log = FastingLog(
                user_id=user_id,
                window_id=window.id if window else 0, # Handle no window case
                log_date=today,
                first_meal_time=meal_time
            )
            self.session.add(log)
        else:
            # Update last meal time
            # If meal_time is earlier than first_meal, update first_meal
            if log.first_meal_time and meal_time < log.first_meal_time:
                log.first_meal_time = meal_time
            
            # Always update last_meal to the latest one
            if not log.last_meal_time or meal_time > log.last_meal_time:
                log.last_meal_time = meal_time
                
        await self.session.commit()
        await self.session.refresh(log)
        return log
