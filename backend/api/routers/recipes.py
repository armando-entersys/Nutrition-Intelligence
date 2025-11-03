"""
Recipe management endpoints with rating and commenting system
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from core.database import get_async_session
from core.auth import get_current_active_user, get_patient_or_nutritionist
from core.logging import log_success, log_error
from domain.recipes.models import Recipe, RecipeStatus, RecipeRating, MealType, DifficultyLevel
from domain.auth.models import AuthUser

router = APIRouter()

# Schemas for recipe rating and commenting
class RecipeRatingRequest(BaseModel):
    """Esquema para crear/actualizar rating de receta"""
    rating: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    comment: Optional[str] = Field(None, max_length=1000, description="Comentario opcional")

class RecipeRatingResponse(BaseModel):
    """Respuesta de rating de receta"""
    id: int
    recipe_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    helpful_votes: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    # User info for display
    user_name: Optional[str] = None
    user_role: Optional[str] = None

class RecipeWithRatingResponse(BaseModel):
    """Receta con información de ratings"""
    id: int
    title: str
    description: Optional[str]
    author_type: str
    servings: int
    prep_time_minutes: Optional[int]
    cook_time_minutes: Optional[int]
    difficulty: DifficultyLevel
    meal_types: Optional[List[MealType]]
    cuisine_type: Optional[str]
    dietary_tags: Optional[List[str]]
    total_calories: Optional[float]
    calories_per_serving: Optional[float]
    image_url: Optional[str]
    status: RecipeStatus
    rating_average: Optional[float]
    rating_count: int
    view_count: int
    created_at: datetime

class RecipeStatsResponse(BaseModel):
    """Estadísticas de rating de receta"""
    recipe_id: int
    average_rating: float
    total_ratings: int
    rating_distribution: Dict[str, int]  # {"5": 10, "4": 5, "3": 2, "2": 1, "1": 0}
    recent_ratings: List[RecipeRatingResponse]
    most_helpful_comments: List[RecipeRatingResponse]

@router.get("/", response_model=List[RecipeWithRatingResponse])
async def get_recipes(
    status: Optional[RecipeStatus] = Query(RecipeStatus.PUBLISHED),
    meal_type: Optional[MealType] = Query(None),
    difficulty: Optional[DifficultyLevel] = Query(None),
    min_rating: Optional[float] = Query(None, ge=1.0, le=5.0),
    cuisine_type: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    sort_by: str = Query("created_at", regex="^(created_at|rating_average|view_count|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    session: Session = Depends(get_async_session)
):
    """Get recipes with advanced filters and rating information"""
    try:
        # Base query
        query = select(Recipe).where(Recipe.status == status)
        
        # Apply filters
        if meal_type:
            # Filter recipes that include this meal type
            query = query.where(Recipe.meal_types.contains([meal_type]))
        
        if difficulty:
            query = query.where(Recipe.difficulty == difficulty)
            
        if min_rating:
            query = query.where(Recipe.rating_average >= min_rating)
            
        if cuisine_type:
            query = query.where(Recipe.cuisine_type == cuisine_type)
        
        # Apply sorting
        if sort_by == "rating_average":
            order_col = Recipe.rating_average.desc() if sort_order == "desc" else Recipe.rating_average.asc()
        elif sort_by == "view_count":
            order_col = Recipe.view_count.desc() if sort_order == "desc" else Recipe.view_count.asc()
        elif sort_by == "title":
            order_col = Recipe.title.desc() if sort_order == "desc" else Recipe.title.asc()
        else:  # created_at
            order_col = Recipe.created_at.desc() if sort_order == "desc" else Recipe.created_at.asc()
            
        query = query.order_by(order_col).limit(limit)
        
        result = await session.exec(query)
        recipes = result.all()
        
        # Convert to response format
        response = []
        for recipe in recipes:
            response.append(RecipeWithRatingResponse(
                id=recipe.id,
                title=recipe.title,
                description=recipe.description,
                author_type=recipe.author_type,
                servings=recipe.servings,
                prep_time_minutes=recipe.prep_time_minutes,
                cook_time_minutes=recipe.cook_time_minutes,
                difficulty=recipe.difficulty,
                meal_types=recipe.meal_types,
                cuisine_type=recipe.cuisine_type,
                dietary_tags=recipe.dietary_tags,
                total_calories=recipe.total_calories,
                calories_per_serving=recipe.calories_per_serving,
                image_url=recipe.image_url,
                status=recipe.status,
                rating_average=recipe.rating_average,
                rating_count=recipe.rating_count,
                view_count=recipe.view_count,
                created_at=recipe.created_at
            ))
        
        return response
        
    except Exception as e:
        log_error(f"Error obteniendo recetas: {str(e)}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recipes"
        )

@router.post("/")
async def create_recipe(
    recipe_data: dict,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """Create new recipe"""
    # TODO: Implement recipe creation with proper validation
    return {"message": "Recipe creation not implemented yet"}

@router.get("/{recipe_id}", response_model=RecipeWithRatingResponse)
async def get_recipe(
    recipe_id: int,
    session: Session = Depends(get_async_session)
):
    """Get recipe by ID with rating information and increment view count"""
    try:
        recipe = await session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Increment view count
        recipe.view_count += 1
        session.add(recipe)
        await session.commit()
        
        log_success(
            f"Receta visualizada: {recipe.title} (ID: {recipe_id})",
            business_context={
                "action": "recipe_view",
                "recipe_id": recipe_id,
                "view_count": recipe.view_count
            }
        )
        
        return RecipeWithRatingResponse(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            author_type=recipe.author_type,
            servings=recipe.servings,
            prep_time_minutes=recipe.prep_time_minutes,
            cook_time_minutes=recipe.cook_time_minutes,
            difficulty=recipe.difficulty,
            meal_types=recipe.meal_types,
            cuisine_type=recipe.cuisine_type,
            dietary_tags=recipe.dietary_tags,
            total_calories=recipe.total_calories,
            calories_per_serving=recipe.calories_per_serving,
            image_url=recipe.image_url,
            status=recipe.status,
            rating_average=recipe.rating_average,
            rating_count=recipe.rating_count,
            view_count=recipe.view_count,
            created_at=recipe.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error obteniendo receta {recipe_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recipe"
        )

# RATING AND COMMENTING ENDPOINTS

@router.post("/{recipe_id}/ratings", response_model=RecipeRatingResponse)
async def create_or_update_rating(
    recipe_id: int,
    rating_data: RecipeRatingRequest,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Crea o actualiza el rating de una receta por parte del usuario
    """
    try:
        # Verificar que la receta existe
        recipe = await session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        # Verificar si el usuario ya tiene un rating para esta receta
        existing_rating_query = select(RecipeRating).where(
            RecipeRating.recipe_id == recipe_id,
            RecipeRating.user_id == current_user.id
        )
        existing_result = await session.exec(existing_rating_query)
        existing_rating = existing_result.first()
        
        if existing_rating:
            # Actualizar rating existente
            old_rating = existing_rating.rating
            existing_rating.rating = rating_data.rating
            existing_rating.comment = rating_data.comment
            existing_rating.updated_at = datetime.utcnow()
            
            session.add(existing_rating)
            rating_to_return = existing_rating
            action = "rating_update"
            
            log_success(
                f"Rating actualizado para receta {recipe_id} por usuario {current_user.id}",
                business_context={
                    "action": action,
                    "recipe_id": recipe_id,
                    "user_id": current_user.id,
                    "old_rating": old_rating,
                    "new_rating": rating_data.rating
                }
            )
        else:
            # Crear nuevo rating
            new_rating = RecipeRating(
                recipe_id=recipe_id,
                user_id=current_user.id,
                rating=rating_data.rating,
                comment=rating_data.comment
            )
            
            session.add(new_rating)
            rating_to_return = new_rating
            action = "rating_creation"
            
            # Incrementar contador de ratings en la receta
            recipe.rating_count += 1
            session.add(recipe)
            
            log_success(
                f"Nuevo rating creado para receta {recipe_id} por usuario {current_user.id}",
                business_context={
                    "action": action,
                    "recipe_id": recipe_id,
                    "user_id": current_user.id,
                    "rating": rating_data.rating,
                    "has_comment": bool(rating_data.comment)
                }
            )
        
        await session.commit()
        await session.refresh(rating_to_return)
        
        # Recalcular promedio de rating
        await _recalculate_recipe_rating_average(session, recipe_id)
        
        return RecipeRatingResponse(
            id=rating_to_return.id,
            recipe_id=rating_to_return.recipe_id,
            user_id=rating_to_return.user_id,
            rating=rating_to_return.rating,
            comment=rating_to_return.comment,
            helpful_votes=rating_to_return.helpful_votes,
            created_at=rating_to_return.created_at,
            updated_at=rating_to_return.updated_at,
            user_name=f"{current_user.username}",
            user_role=current_user.primary_role.value
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error creando/actualizando rating para receta {recipe_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create or update rating"
        )

@router.get("/{recipe_id}/ratings", response_model=List[RecipeRatingResponse])
async def get_recipe_ratings(
    recipe_id: int,
    limit: int = Query(50, le=100),
    sort_by: str = Query("created_at", regex="^(created_at|rating|helpful_votes)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    session: Session = Depends(get_async_session)
):
    """
    Obtiene todos los ratings y comentarios de una receta
    """
    try:
        # Verificar que la receta existe
        recipe = await session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        # Query base
        query = select(RecipeRating).where(RecipeRating.recipe_id == recipe_id)
        
        # Apply sorting
        if sort_by == "rating":
            order_col = RecipeRating.rating.desc() if sort_order == "desc" else RecipeRating.rating.asc()
        elif sort_by == "helpful_votes":
            order_col = RecipeRating.helpful_votes.desc() if sort_order == "desc" else RecipeRating.helpful_votes.asc()
        else:  # created_at
            order_col = RecipeRating.created_at.desc() if sort_order == "desc" else RecipeRating.created_at.asc()
            
        query = query.order_by(order_col).limit(limit)
        
        result = await session.exec(query)
        ratings = result.all()
        
        # Convert to response format (in a real app, you'd join with users table)
        response = []
        for rating in ratings:
            response.append(RecipeRatingResponse(
                id=rating.id,
                recipe_id=rating.recipe_id,
                user_id=rating.user_id,
                rating=rating.rating,
                comment=rating.comment,
                helpful_votes=rating.helpful_votes,
                created_at=rating.created_at,
                updated_at=rating.updated_at,
                user_name=f"Usuario {rating.user_id}",  # Simplified - would join with users
                user_role="patient"  # Simplified
            ))
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error obteniendo ratings para receta {recipe_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recipe ratings"
        )

@router.get("/{recipe_id}/rating-stats", response_model=RecipeStatsResponse)
async def get_recipe_rating_stats(
    recipe_id: int,
    session: Session = Depends(get_async_session)
):
    """
    Obtiene estadísticas detalladas de rating de una receta
    """
    try:
        # Verificar que la receta existe
        recipe = await session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        
        # Obtener todos los ratings
        ratings_query = select(RecipeRating).where(RecipeRating.recipe_id == recipe_id)
        ratings_result = await session.exec(ratings_query)
        all_ratings = ratings_result.all()
        
        if not all_ratings:
            return RecipeStatsResponse(
                recipe_id=recipe_id,
                average_rating=0.0,
                total_ratings=0,
                rating_distribution={"5": 0, "4": 0, "3": 0, "2": 0, "1": 0},
                recent_ratings=[],
                most_helpful_comments=[]
            )
        
        # Calcular estadísticas
        total_ratings = len(all_ratings)
        average_rating = sum(r.rating for r in all_ratings) / total_ratings
        
        # Distribución de ratings
        rating_distribution = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
        for rating in all_ratings:
            rating_distribution[str(rating.rating)] += 1
        
        # Ratings recientes (últimos 10)
        recent_ratings = sorted(all_ratings, key=lambda x: x.created_at, reverse=True)[:10]
        recent_ratings_response = [RecipeRatingResponse(
            id=r.id,
            recipe_id=r.recipe_id,
            user_id=r.user_id,
            rating=r.rating,
            comment=r.comment,
            helpful_votes=r.helpful_votes,
            created_at=r.created_at,
            updated_at=r.updated_at,
            user_name=f"Usuario {r.user_id}",
            user_role="patient"
        ) for r in recent_ratings]
        
        # Comentarios más útiles (con más votos)
        helpful_comments = [r for r in all_ratings if r.comment and len(r.comment.strip()) > 0]
        helpful_comments = sorted(helpful_comments, key=lambda x: x.helpful_votes, reverse=True)[:5]
        helpful_comments_response = [RecipeRatingResponse(
            id=r.id,
            recipe_id=r.recipe_id,
            user_id=r.user_id,
            rating=r.rating,
            comment=r.comment,
            helpful_votes=r.helpful_votes,
            created_at=r.created_at,
            updated_at=r.updated_at,
            user_name=f"Usuario {r.user_id}",
            user_role="patient"
        ) for r in helpful_comments]
        
        return RecipeStatsResponse(
            recipe_id=recipe_id,
            average_rating=round(average_rating, 2),
            total_ratings=total_ratings,
            rating_distribution=rating_distribution,
            recent_ratings=recent_ratings_response,
            most_helpful_comments=helpful_comments_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error obteniendo estadísticas de rating para receta {recipe_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recipe rating stats"
        )

@router.post("/ratings/{rating_id}/helpful")
async def mark_rating_helpful(
    rating_id: int,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Marca un rating como útil (incrementa helpful_votes)
    """
    try:
        rating = await session.get(RecipeRating, rating_id)
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found"
            )
        
        # En una implementación real, verificarías que el usuario no haya marcado ya este rating
        # Por simplicidad, solo incrementamos el contador
        rating.helpful_votes += 1
        session.add(rating)
        await session.commit()
        
        log_success(
            f"Rating {rating_id} marcado como útil por usuario {current_user.id}",
            business_context={
                "action": "rating_helpful_vote",
                "rating_id": rating_id,
                "voter_user_id": current_user.id,
                "helpful_votes": rating.helpful_votes
            }
        )
        
        return {"message": "Rating marked as helpful", "helpful_votes": rating.helpful_votes}
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error marcando rating {rating_id} como útil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark rating as helpful"
        )

@router.delete("/ratings/{rating_id}")
async def delete_rating(
    rating_id: int,
    current_user: AuthUser = Depends(get_patient_or_nutritionist),
    session: Session = Depends(get_async_session)
):
    """
    Elimina un rating (solo el usuario que lo creó puede eliminarlo)
    """
    try:
        rating = await session.get(RecipeRating, rating_id)
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found"
            )
        
        # Verificar que el usuario es el dueño del rating
        if rating.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only delete your own ratings"
            )
        
        # Actualizar contador en la receta
        recipe = await session.get(Recipe, rating.recipe_id)
        if recipe:
            recipe.rating_count = max(0, recipe.rating_count - 1)
            session.add(recipe)
        
        # Eliminar rating
        await session.delete(rating)
        await session.commit()
        
        # Recalcular promedio
        if recipe:
            await _recalculate_recipe_rating_average(session, recipe.id)
        
        log_success(
            f"Rating {rating_id} eliminado por usuario {current_user.id}",
            business_context={
                "action": "rating_deletion",
                "rating_id": rating_id,
                "recipe_id": rating.recipe_id,
                "user_id": current_user.id
            }
        )
        
        return {"message": "Rating deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error eliminando rating {rating_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete rating"
        )

# Helper function
async def _recalculate_recipe_rating_average(session: Session, recipe_id: int):
    """
    Recalcula el promedio de rating de una receta
    """
    try:
        ratings_query = select(RecipeRating).where(RecipeRating.recipe_id == recipe_id)
        ratings_result = await session.exec(ratings_query)
        ratings = ratings_result.all()
        
        recipe = await session.get(Recipe, recipe_id)
        if recipe:
            if ratings:
                recipe.rating_average = sum(r.rating for r in ratings) / len(ratings)
                recipe.rating_count = len(ratings)
            else:
                recipe.rating_average = None
                recipe.rating_count = 0
            
            session.add(recipe)
            await session.commit()
            
    except Exception as e:
        log_error(f"Error recalculando promedio de rating para receta {recipe_id}: {str(e)}")