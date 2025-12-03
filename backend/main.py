"""
Nutrition Intelligence Platform - Main FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import time
import uuid

from core.config import get_settings
from core.database import init_db
from core.logging import LoggingMiddleware, log_success, log_error
from core.sentry import init_sentry
from middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from middleware.security_headers import SecurityHeadersMiddleware, RateLimitByIPMiddleware
from api.routers import auth_simple, users, foods, recipes, meal_plans, nutritionists, patients, nutrition_calculator, weekly_planning, vision, laboratory, whatsapp, admin, notifications, patient_progress, nutritionist_chat, scanner, rag, medicinal_plants, admin_medicinal_plants, logs, trophology, fasting, gamification, digestion, mindfulness
from api.routers import auth_new, auth_complete

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Nutrition Intelligence Platform...")
    log_success("Sistema iniciando", business_context={"action": "system_startup"})

    # Initialize Sentry
    init_sentry()
    log_success("Sentry inicializado", business_context={"action": "sentry_init"})

    await init_db()
    log_success("Base de datos inicializada", business_context={"action": "database_init"})
    yield
    # Shutdown
    logger.info("Shutting down Nutrition Intelligence Platform...")
    log_success("Sistema cerrando", business_context={"action": "system_shutdown"})

def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="Nutrition Intelligence API",
        description="Plataforma integral de nutrición inteligente para profesionales y pacientes",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )

    # Security headers middleware
    app.add_middleware(SecurityHeadersMiddleware, environment=settings.environment)

    # Rate limiting for documentation endpoints
    app.add_middleware(RateLimitByIPMiddleware, requests_per_minute=60)

    # Logging middleware (PRIMERO para capturar todo)
    app.add_middleware(LoggingMiddleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
    
    # Request tracking middleware
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        logger.info(
            f"Request processed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "process_time": process_time
            }
        )
        
        return response
    
    # Exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Health check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "nutrition-intelligence-api",
            "version": "1.0.0"
        }

    # Include routers
    app.include_router(auth_complete.router, prefix="/api/v1", tags=["authentication"])  # New complete auth system
    # app.include_router(auth_simple.router, prefix="/api/v1/auth", tags=["auth"])  # Disabled - conflicts with auth_complete
    app.include_router(auth_new.router, prefix="/api/v1/auth-hybrid", tags=["auth-hybrid"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(foods.router, prefix="/api/v1/foods", tags=["foods"])
    app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
    app.include_router(meal_plans.router, prefix="/api/v1/meal-plans", tags=["meal-plans"])
    app.include_router(nutritionists.router, prefix="/api/v1/nutritionists", tags=["nutritionists"])
    app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
    app.include_router(nutrition_calculator.router, prefix="/api/v1/nutrition-calculator", tags=["nutrition-calculator"])
    app.include_router(weekly_planning.router, prefix="/api/v1/weekly-planning", tags=["weekly-planning"])
    
    # Import and include equivalences router
    from api.routers import equivalences
    app.include_router(equivalences.router, prefix="/api/v1/equivalences", tags=["equivalences"])

    # AI Vision router
    app.include_router(vision.router, prefix="/api/v1/vision", tags=["ai-vision"])

    # AI Nutritionist Chat router
    app.include_router(nutritionist_chat.router, prefix="/api/v1/nutritionist-chat", tags=["nutritionist-chat"])

    # NOM-051 Scanner router
    app.include_router(scanner.router, prefix="/api/v1/scanner", tags=["nom051-scanner"])

    # Laboratory Data router
    app.include_router(laboratory.router, prefix="/api/v1/laboratory", tags=["laboratory"])

    # WhatsApp router
    app.include_router(whatsapp.router, prefix="/api/v1/whatsapp", tags=["whatsapp"])

    # Admin router
    app.include_router(admin.router, prefix="/api/v1", tags=["admin"])

    # Notifications router
    app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

    # Patient Progress & Analytics router
    app.include_router(patient_progress.router, prefix="/api/v1/patient-progress", tags=["patient-progress"])

    # RAG (Retrieval Augmented Generation) router
    app.include_router(rag.router, prefix="/api/v1", tags=["rag"])

    # Medicinal Plants router - Traditional Mexican Medicine
    app.include_router(medicinal_plants.router, prefix="/api/v1/medicinal-plants", tags=["medicinal-plants"])

    # Admin Medicinal Plants router - Seeding and management
    app.include_router(admin_medicinal_plants.router, prefix="/api/v1", tags=["admin", "medicinal-plants"])

    # Frontend Logging router
    app.include_router(logs.router, prefix="/api/v1", tags=["logs"])

    # Trophology router - Lezaeta's food combination rules
    app.include_router(trophology.router, prefix="/api/v1/trophology", tags=["trophology"])

    # Fasting router
    app.include_router(fasting.router, prefix="/api/v1/fasting", tags=["fasting"])

    # Gamification router
    app.include_router(gamification.router, prefix="/api/v1/gamification", tags=["gamification"])

    # Digestion router
    app.include_router(digestion.router, prefix="/api/v1/digestion", tags=["digestion"])

    # Mindfulness router
    app.include_router(mindfulness.router, prefix="/api/v1/mindfulness", tags=["mindfulness"])

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
        log_level="info"
    )