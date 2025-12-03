from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Any, List
from pydantic import BaseModel

from core.database import get_session
from api.routers.auth_new import get_current_user
from domain.users.models import User
from services.gamification.gamification_service import GamificationService

router = APIRouter()

class BadgeResponse(BaseModel):
    id: int
    nombre: str
    icono: str
    descripcion: str
    fecha_obtenido: str = None
    progreso: int = 0
    total: int = 0

class GamificationProfileResponse(BaseModel):
    nivel: int
    nombre_nivel: str
    xp_actual: int
    xp_siguiente_nivel: int
    xp_total: int
    racha_actual: int
    racha_maxima: int
    badges_obtenidos: List[BadgeResponse]
    badges_disponibles: List[BadgeResponse]

@router.get("/profile", response_model=GamificationProfileResponse)
def get_profile(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    service = GamificationService(session)
    profile = service.get_or_create_profile(current_user.id)
    
    # Calculate level name and next XP
    niveles = [
        (1, 'Novato', 100),
        (2, 'Guerrero Azteca', 300),
        (3, 'Águila Mexicana', 600),
        (4, 'Luchador', 1000),
        (5, 'Leyenda Nacional', 2000),
        (6, 'Patrimonio UNESCO', 99999),
    ]
    
    nombre_nivel = 'Novato'
    xp_siguiente = 100
    
    for lvl, name, max_xp in niveles:
        if profile.level == lvl:
            nombre_nivel = name
            xp_siguiente = max_xp
            break
            
    # Fetch earned badges
    earned_badges_data = []
    if current_user.badges:
        for ub in current_user.badges:
            if ub.badge:
                earned_badges_data.append(BadgeResponse(
                    id=ub.badge.id,
                    nombre=ub.badge.name,
                    icono=ub.badge.icon,
                    descripcion=ub.badge.description,
                    fecha_obtenido=ub.earned_at.strftime("%Y-%m-%d"),
                    progreso=100,
                    total=100
                ))

    # Fetch available badges (not earned yet)
    # This requires a service method to get all badges, for now we can leave empty or implement if BadgeService exists
    # Assuming we want to show some available badges
    available_badges_data = []
    
    return GamificationProfileResponse(
        nivel=profile.level,
        nombre_nivel=nombre_nivel,
        xp_actual=profile.current_xp,
        xp_siguiente_nivel=xp_siguiente,
        xp_total=profile.total_xp,
        racha_actual=profile.current_streak,
        racha_maxima=profile.max_streak,
        badges_obtenidos=earned_badges_data,
        badges_disponibles=available_badges_data
    )

@router.get("/leaderboard")
def get_leaderboard(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    service = GamificationService(session)
    leaderboard = service.get_leaderboard()
    
    # Add rank and check if it's current user
    for i, entry in enumerate(leaderboard):
        entry['posicion'] = i + 1
        # Check if this entry belongs to current user (simplified name check for now)
        # Ideally we'd return user_id in service and check here
        if entry['nombre'] == f"{current_user.first_name} {current_user.last_name}":
             entry['es_usuario'] = True
             
    return leaderboard
