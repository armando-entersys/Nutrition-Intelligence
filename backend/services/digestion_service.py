from typing import Optional, List, Dict
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from domain.digestion.models import DigestionLog, StoolConsistency, StoolColor

class DigestionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_digestion(self, user_id: int, log_data: Dict) -> DigestionLog:
        """Create or update digestion log for today."""
        today = date.today()
        
        # Check if log exists for today
        stmt = select(DigestionLog).where(
            DigestionLog.user_id == user_id,
            DigestionLog.log_date == today
        )
        result = await self.session.execute(stmt)
        existing_log = result.scalar_one_or_none()
        
        if existing_log:
            # Update existing
            for key, value in log_data.items():
                if hasattr(existing_log, key) and value is not None:
                    setattr(existing_log, key, value)
            existing_log.updated_at = datetime.utcnow()
            log = existing_log
        else:
            # Create new
            log = DigestionLog(user_id=user_id, log_date=today, **log_data)
            self.session.add(log)
            
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_today_log(self, user_id: int) -> Optional[DigestionLog]:
        """Get digestion log for today."""
        stmt = select(DigestionLog).where(
            DigestionLog.user_id == user_id,
            DigestionLog.log_date == date.today()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history(self, user_id: int, limit: int = 7) -> List[DigestionLog]:
        """Get digestion history."""
        stmt = select(DigestionLog).where(
            DigestionLog.user_id == user_id
        ).order_by(desc(DigestionLog.log_date)).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_stats(self, user_id: int) -> Dict:
        """Get digestion statistics (last 30 days)."""
        history = await self.get_history(user_id, limit=30)
        
        if not history:
            return {
                "avg_comfort": 0,
                "bronze_stool_percentage": 0,
                "common_symptoms": []
            }
            
        total_logs = len(history)
        avg_comfort = sum(log.comfort_level for log in history) / total_logs
        
        bronze_count = sum(1 for log in history if log.stool_color == StoolColor.BRONZE)
        bronze_percentage = (bronze_count / total_logs) * 100
        
        symptoms_count = {
            "bloating": sum(1 for log in history if log.bloating),
            "gas": sum(1 for log in history if log.gas),
            "acidity": sum(1 for log in history if log.acidity),
            "abdominal_pain": sum(1 for log in history if log.abdominal_pain)
        }
        
        # Sort symptoms by frequency
        common_symptoms = sorted(
            [k for k, v in symptoms_count.items() if v > 0],
            key=lambda k: symptoms_count[k],
            reverse=True
        )
        
        return {
            "avg_comfort": round(avg_comfort, 1),
            "bronze_stool_percentage": round(bronze_percentage, 1),
            "common_symptoms": common_symptoms
        }
