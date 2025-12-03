from sqlmodel import Session, select, desc
from typing import List, Optional
from datetime import datetime
from domain.gamification.models import UserGamificationProfile, Badge, UserBadge
from domain.users.models import User

class GamificationService:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_profile(self, user_id: int) -> UserGamificationProfile:
        statement = select(UserGamificationProfile).where(UserGamificationProfile.user_id == user_id)
        profile = self.session.exec(statement).first()
        
        if not profile:
            profile = UserGamificationProfile(user_id=user_id)
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
            
        return profile

    def get_user_badges(self, user_id: int) -> List[UserBadge]:
        statement = select(UserBadge).where(UserBadge.user_id == user_id)
        return self.session.exec(statement).all()

    def get_available_badges(self, user_id: int) -> List[Badge]:
        # Return all badges (simplified)
        # In a real app, might filter out earned ones or show them as earned
        statement = select(Badge)
        return self.session.exec(statement).all()

    def get_leaderboard(self, limit: int = 10):
        statement = select(UserGamificationProfile).order_by(desc(UserGamificationProfile.total_xp)).limit(limit)
        profiles = self.session.exec(statement).all()
        
        # Enrich with user names
        leaderboard = []
        for p in profiles:
            user = self.session.get(User, p.user_id)
            leaderboard.append({
                "posicion": 0, # Filled later
                "nombre": f"{user.first_name} {user.last_name}" if user else "Usuario",
                "estado": "México", # Placeholder
                "xp": p.total_xp,
                "avatar_color": "#2196F3", # Placeholder
                "es_usuario": False # Filled in controller
            })
        return leaderboard

    def add_xp(self, user_id: int, amount: int):
        profile = self.get_or_create_profile(user_id)
        profile.current_xp += amount
        profile.total_xp += amount
        
        # Level up logic (simplified: Level = XP / 100)
        new_level = 1 + (profile.total_xp // 100)
        if new_level > profile.level:
            profile.level = new_level
            # TODO: Notify user of level up
            
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile
