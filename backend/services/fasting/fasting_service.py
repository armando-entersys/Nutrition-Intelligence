from sqlmodel import Session, select, desc
from datetime import datetime, timedelta, time
from typing import Optional, List
from domain.fasting.models import FastingWindow, FastingLog, FastingStats
from domain.users.models import User

class FastingService:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_window(self, user_id: int) -> FastingWindow:
        """Get user's fasting window or create default 16:8 (12pm-8pm)"""
        statement = select(FastingWindow).where(FastingWindow.user_id == user_id, FastingWindow.active == True)
        window = self.session.exec(statement).first()
        
        if not window:
            # Default: 16:8 protocol (Eating window 12:00 - 20:00)
            window = FastingWindow(
                user_id=user_id,
                start_time=time(12, 0),
                end_time=time(20, 0),
                duration_hours=8,
                active=True
            )
            self.session.add(window)
            self.session.commit()
            self.session.refresh(window)
            
        return window

    def update_window(self, user_id: int, start_time: time, end_time: time) -> FastingWindow:
        """Update user's fasting window configuration"""
        window = self.get_or_create_window(user_id)
        
        window.start_time = start_time
        window.end_time = end_time
        
        # Calculate duration
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
            
        duration = (end_dt - start_dt).total_seconds() / 3600
        window.duration_hours = int(duration)
        window.updated_at = datetime.utcnow()
        
        self.session.add(window)
        self.session.commit()
        self.session.refresh(window)
        return window

    def get_last_log(self, user_id: int) -> Optional[FastingLog]:
        """Get the most recent fasting log"""
        statement = select(FastingLog).where(FastingLog.user_id == user_id).order_by(desc(FastingLog.log_date))
        return self.session.exec(statement).first()

    def start_fast(self, user_id: int, start_time: datetime = None) -> FastingLog:
        """
        Start a fast (record last meal time).
        Usually happens at the end of the eating window.
        """
        if not start_time:
            start_time = datetime.utcnow()
            
        today = start_time.date()
        window = self.get_or_create_window(user_id)
        
        # Check if log exists for today
        statement = select(FastingLog).where(FastingLog.user_id == user_id, FastingLog.log_date == today)
        log = self.session.exec(statement).first()
        
        if not log:
            log = FastingLog(
                user_id=user_id,
                window_id=window.id,
                log_date=today
            )
            
        log.last_meal_time = start_time
        log.updated_at = datetime.utcnow()
        
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def end_fast(self, user_id: int, end_time: datetime = None) -> FastingLog:
        """
        End a fast (record first meal time).
        Usually happens at the start of the eating window.
        """
        if not end_time:
            end_time = datetime.utcnow()
            
        today = end_time.date()
        window = self.get_or_create_window(user_id)
        
        # Check if log exists for today
        statement = select(FastingLog).where(FastingLog.user_id == user_id, FastingLog.log_date == today)
        log = self.session.exec(statement).first()
        
        if not log:
            log = FastingLog(
                user_id=user_id,
                window_id=window.id,
                log_date=today
            )
        
        log.first_meal_time = end_time
        
        # Calculate fasting hours from PREVIOUS day's last_meal_time
        # Find previous log with a last_meal_time
        prev_statement = select(FastingLog).where(
            FastingLog.user_id == user_id, 
            FastingLog.log_date < today,
            FastingLog.last_meal_time != None
        ).order_by(desc(FastingLog.log_date))
        
        prev_log = self.session.exec(prev_statement).first()
        
        if prev_log and prev_log.last_meal_time:
            duration = (end_time - prev_log.last_meal_time).total_seconds() / 3600
            log.fasting_hours = round(duration, 2)
            
            # Autophagy starts after 12 hours (simplified model)
            if duration > 12:
                log.autophagy_hours = round(duration - 12, 2)
            else:
                log.autophagy_hours = 0
                
            # Check adherence (did they wait long enough?)
            # Simplified: if fasted > (24 - window.duration_hours) - 1 hour buffer
            target_fast_hours = 24 - window.duration_hours
            log.adherence = duration >= (target_fast_hours - 1)
            
        log.updated_at = datetime.utcnow()
        
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def get_current_status(self, user_id: int) -> FastingStats:
        """Calculate current fasting status and stats"""
        window = self.get_or_create_window(user_id)
        now = datetime.utcnow()
        
        # Determine if currently fasting
        # Logic: 
        # 1. Find last action (start fast or end fast)
        # 2. If last action was start_fast (last_meal_time) -> Currently Fasting
        # 3. If last action was end_fast (first_meal_time) -> Currently Eating
        
        last_log = self.get_last_log(user_id)
        
        is_fasting = False
        current_fast_hours = 0.0
        autophagy_active = False
        
        if last_log:
            # Check if we have a last_meal_time (start of fast)
            if last_log.last_meal_time:
                # If we ALSO have a first_meal_time for the SAME day that is LATER, then we are eating
                # But usually first_meal_time comes BEFORE last_meal_time in a day
                # E.g. Eat at 12pm (first), Stop at 8pm (last)
                
                # If today's log has last_meal_time, we are fasting since then
                if last_log.log_date == now.date():
                    is_fasting = True
                    start_fast_time = last_log.last_meal_time
                # If yesterday's log has last_meal_time, and today has NO first_meal_time, we are fasting
                elif not self._has_broken_fast_today(user_id, now.date()):
                    is_fasting = True
                    start_fast_time = last_log.last_meal_time
                else:
                    is_fasting = False
            else:
                # No last meal time recorded for this log
                # Check if we broke fast today
                if last_log.first_meal_time and last_log.log_date == now.date():
                    is_fasting = False
                else:
                    # Fallback
                    is_fasting = False
        
        if is_fasting:
            duration = (now - start_fast_time).total_seconds() / 3600
            current_fast_hours = round(duration, 2)
            autophagy_active = duration > 12
            
        # Calculate stats (placeholders for now)
        stats = FastingStats(
            in_fasting_window=not is_fasting, # If not fasting, we are in eating window (simplified)
            current_fast_hours=current_fast_hours,
            autophagy_active=autophagy_active,
            window_start=window.start_time.strftime("%H:%M"),
            window_end=window.end_time.strftime("%H:%M"),
            time_until_window_start=0, # TODO: Calculate
            time_until_window_end=0,   # TODO: Calculate
            adherence_7d=0.0,
            adherence_30d=0.0,
            total_autophagy_hours_7d=0.0,
            total_autophagy_hours_30d=0.0,
            avg_fasting_hours_7d=0.0,
            avg_fasting_hours_30d=0.0,
            current_streak=0,
            longest_streak=0
        )
        
        return stats

    def _has_broken_fast_today(self, user_id: int, today: date) -> bool:
        statement = select(FastingLog).where(
            FastingLog.user_id == user_id, 
            FastingLog.log_date == today,
            FastingLog.first_meal_time != None
        )
        return self.session.exec(statement).first() is not None
