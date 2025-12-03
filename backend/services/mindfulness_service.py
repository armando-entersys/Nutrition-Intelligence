from typing import Optional, List, Dict
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from domain.mindfulness.models import HungerLog, STOPPractice, HungerLevel

class MindfulnessService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_hunger(self, user_id: int, log_data: Dict) -> HungerLog:
        """Create hunger log."""
        log = HungerLog(user_id=user_id, **log_data)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_hunger_logs(self, user_id: int, limit: int = 10) -> List[HungerLog]:
        """Get recent hunger logs."""
        stmt = select(HungerLog).where(
            HungerLog.user_id == user_id
        ).order_by(desc(HungerLog.log_time)).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def log_stop_practice(self, user_id: int, practice_data: Dict) -> STOPPractice:
        """Create STOP practice log."""
        practice = STOPPractice(user_id=user_id, **practice_data)
        self.session.add(practice)
        await self.session.commit()
        await self.session.refresh(practice)
        return practice

    async def get_stop_practices(self, user_id: int, limit: int = 10) -> List[STOPPractice]:
        """Get recent STOP practices."""
        stmt = select(STOPPractice).where(
            STOPPractice.user_id == user_id
        ).order_by(desc(STOPPractice.practice_time)).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_stats(self, user_id: int) -> Dict:
        """Get mindfulness statistics."""
        hunger_logs = await self.get_hunger_logs(user_id, limit=30)
        stop_practices = await self.get_stop_practices(user_id, limit=30)
        
        total_hunger_logs = len(hunger_logs)
        total_stop_practices = len(stop_practices)
        
        # Calculate emotional eating percentage
        emotional_logs = sum(1 for log in hunger_logs if log.emotion_before)
        emotional_eating_rate = (emotional_logs / total_hunger_logs * 100) if total_hunger_logs > 0 else 0
        
        # Calculate stress reduction
        stress_reduction = 0
        if stop_practices:
            reductions = [p.stress_level_before - p.stress_level_after for p in stop_practices]
            stress_reduction = sum(reductions) / len(reductions)
            
        return {
            "total_hunger_logs": total_hunger_logs,
            "total_stop_practices": total_stop_practices,
            "emotional_eating_rate": round(emotional_eating_rate, 1),
            "avg_stress_reduction": round(stress_reduction, 1)
        }
