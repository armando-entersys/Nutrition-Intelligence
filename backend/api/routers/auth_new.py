"""
Router de Autenticación con Roles Híbridos
Login, registro, gestión de sesiones y roles híbridos
"""
from fastapi import APIRouter, HTTPException, Depends, Request, status
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from datetime import datetime

from core.database import get_async_session
from core.auth import (
    AuthService, create_access_token, create_refresh_token, verify_token,
    get_current_user, get_current_active_user, 
    get_admin_user, get_nutritionist_user, get_patient_user,
    get_nutritionist_or_admin, get_patient_or_nutritionist
)
from domain.auth.models import (
    AuthUser, UserRole, AccountStatus, UserRoleAssignment,
    ROLE_PERMISSIONS, get_user_permissions
)
from core.logging import log_success, log_error

router = APIRouter()

# Schemas de entrada
class RegisterRequest(BaseModel):
    """Esquema para registro de usuario"""
    email: EmailStr = Field(..., description="Email único del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido")
    phone: Optional[str] = Field(None, description="Teléfono opcional")
    primary_role: UserRole = Field(..., description="Rol principal del usuario")

class LoginRequest(BaseModel):
    """Esquema para login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")

class RoleAssignmentRequest(BaseModel):
    """Esquema para asignar roles adicionales"""
    user_id: int = Field(..., description="ID del usuario")
    role: UserRole = Field(..., description="Rol a asignar")
    reason: Optional[str] = Field(None, description="Motivo de la asignación")

# Schemas de salida
class UserResponse(BaseModel):
    """Información básica del usuario"""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    phone: Optional[str]
    primary_role: UserRole
    secondary_roles: List[UserRole]
    account_status: AccountStatus
    is_email_verified: bool
    profile_completed: bool
    last_login: Optional[datetime]
    created_at: datetime

class LoginResponse(BaseModel):
    """Respuesta de login exitoso"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    permissions: List[str]
    dashboard_url: str

class RoleInfoResponse(BaseModel):
    """Información detallada de roles"""
    role: UserRole
    name: str
    description: str
    permissions: List[str]
    default_dashboard: str

# Endpoints de autenticación
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterRequest,
    session: Session = Depends(get_async_session)
):
    """
    Registra un nuevo usuario en el sistema
    """
    try:
        # Verificar si email ya existe
        email_statement = select(AuthUser).where(AuthUser.email == request.email)
        email_result = await session.exec(email_statement)
        if email_result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Verificar si username ya existe
        username_statement = select(AuthUser).where(AuthUser.username == request.username)
        username_result = await session.exec(username_statement)
        if username_result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Crear usuario
        new_user = AuthUser(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
            primary_role=request.primary_role,
            secondary_roles=[],
            account_status=AccountStatus.ACTIVE  # Para testing, cambiar a PENDING_VERIFICATION
        )
        
        # Establecer contraseña
        new_user.set_password(request.password)
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        log_success(
            f"Usuario registrado: {request.email} ({request.primary_role.value})",
            business_context={
                "action": "user_registration",
                "user_id": new_user.id,
                "user_email": request.email,
                "primary_role": request.primary_role.value
            }
        )
        
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            full_name=new_user.full_name,
            phone=new_user.phone,
            primary_role=new_user.primary_role,
            secondary_roles=new_user.secondary_roles,
            account_status=new_user.account_status,
            is_email_verified=new_user.is_email_verified,
            profile_completed=new_user.profile_completed,
            last_login=new_user.last_login,
            created_at=new_user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error en registro de usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=LoginResponse)
async def login_user(
    request: LoginRequest,
    http_request: Request,
    session: Session = Depends(get_async_session)
):
    """
    Autentica un usuario y devuelve tokens JWT
    """
    try:
        auth_service = AuthService(session)
        
        # Autenticar usuario
        user = await auth_service.authenticate_user(request.email, request.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Crear tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        
        # Crear sesión
        await auth_service.create_user_session(
            user, 
            ip_address=http_request.client.host,
            user_agent=http_request.headers.get("user-agent")
        )
        
        # Obtener permisos
        permissions = get_user_permissions(user)
        
        # Determinar dashboard URL basado en rol principal
        dashboard_url = f"/{ROLE_PERMISSIONS[user.primary_role]['default_dashboard']}"
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800,  # 30 minutos
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                phone=user.phone,
                primary_role=user.primary_role,
                secondary_roles=user.secondary_roles,
                account_status=user.account_status,
                is_email_verified=user.is_email_verified,
                profile_completed=user.profile_completed,
                last_login=user.last_login,
                created_at=user.created_at
            ),
            permissions=permissions,
            dashboard_url=dashboard_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/logout")
async def logout_user(
    current_user: AuthUser = Depends(get_current_active_user),
    session: Session = Depends(get_async_session)
):
    """
    Cierra la sesión del usuario actual
    """
    try:
        log_success(
            f"Usuario desconectado: {current_user.email}",
            business_context={
                "action": "user_logout",
                "user_id": current_user.id
            }
        )
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        log_error(f"Error en logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: AuthUser = Depends(get_current_active_user)
):
    """
    Obtiene información del usuario actual
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        full_name=current_user.full_name,
        phone=current_user.phone,
        primary_role=current_user.primary_role,
        secondary_roles=current_user.secondary_roles,
        account_status=current_user.account_status,
        is_email_verified=current_user.is_email_verified,
        profile_completed=current_user.profile_completed,
        last_login=current_user.last_login,
        created_at=current_user.created_at
    )

@router.get("/permissions")
async def get_user_permissions_endpoint(
    current_user: AuthUser = Depends(get_current_active_user)
):
    """
    Obtiene los permisos del usuario actual
    """
    permissions = get_user_permissions(current_user)
    
    return {
        "user_id": current_user.id,
        "primary_role": current_user.primary_role,
        "secondary_roles": current_user.secondary_roles,
        "permissions": permissions,
        "role_info": {
            role.value: ROLE_PERMISSIONS[role] 
            for role in current_user.get_all_roles()
        }
    }

# Gestión de roles (solo admins)
@router.post("/assign-role", dependencies=[Depends(get_admin_user)])
async def assign_role(
    request: RoleAssignmentRequest,
    admin_user: AuthUser = Depends(get_admin_user),
    session: Session = Depends(get_async_session)
):
    """
    Asigna un rol adicional a un usuario (solo admins)
    """
    try:
        # Buscar usuario objetivo
        statement = select(AuthUser).where(AuthUser.id == request.user_id)
        result = await session.exec(statement)
        target_user = result.first()
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar que no tenga ya este rol
        if target_user.has_role(request.role):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already has role {request.role.value}"
            )
        
        # Asignar rol secundario
        target_user.add_secondary_role(request.role)
        
        # Crear registro de asignación
        role_assignment = UserRoleAssignment(
            user_id=target_user.id,
            role=request.role,
            assigned_by=admin_user.id,
            reason=request.reason or f"Assigned by admin {admin_user.username}"
        )
        
        session.add(target_user)
        session.add(role_assignment)
        await session.commit()
        
        log_success(
            f"Rol {request.role.value} asignado a usuario {target_user.email} por {admin_user.email}",
            business_context={
                "action": "role_assignment",
                "target_user_id": target_user.id,
                "assigned_role": request.role.value,
                "assigned_by": admin_user.id
            }
        )
        
        return {
            "message": f"Role {request.role.value} assigned successfully",
            "user_id": target_user.id,
            "new_roles": target_user.get_all_roles()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error asignando rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Role assignment failed"
        )

@router.get("/roles", response_model=List[RoleInfoResponse])
async def get_available_roles():
    """
    Obtiene información sobre todos los roles disponibles
    """
    roles_info = []
    
    for role, info in ROLE_PERMISSIONS.items():
        roles_info.append(RoleInfoResponse(
            role=role,
            name=info["name"],
            description=info["description"],
            permissions=info["permissions"],
            default_dashboard=info["default_dashboard"]
        ))
    
    return roles_info

# Endpoints específicos por rol para testing
@router.get("/admin-only", dependencies=[Depends(get_admin_user)])
async def admin_only_endpoint():
    """Endpoint solo para administradores"""
    return {"message": "This is an admin-only endpoint"}

@router.get("/nutritionist-only", dependencies=[Depends(get_nutritionist_user)])
async def nutritionist_only_endpoint():
    """Endpoint solo para nutricionistas"""
    return {"message": "This is a nutritionist-only endpoint"}

@router.get("/patient-only", dependencies=[Depends(get_patient_user)])
async def patient_only_endpoint():
    """Endpoint solo para pacientes"""
    return {"message": "This is a patient-only endpoint"}

@router.get("/nutritionist-or-admin", dependencies=[Depends(get_nutritionist_or_admin)])
async def nutritionist_or_admin_endpoint():
    """Endpoint para nutricionistas o administradores"""
    return {"message": "This endpoint is for nutritionists or admins"}

@router.get("/hybrid-roles", dependencies=[Depends(get_patient_or_nutritionist)])
async def hybrid_roles_endpoint(
    current_user: AuthUser = Depends(get_patient_or_nutritionist)
):
    """
    Endpoint que demuestra roles híbridos
    Un nutricionista puede ser también paciente
    """
    return {
        "message": "This endpoint supports hybrid roles",
        "user_id": current_user.id,
        "primary_role": current_user.primary_role,
        "all_roles": current_user.get_all_roles(),
        "can_create_meal_plans": current_user.has_role(UserRole.NUTRITIONIST),
        "can_track_consumption": current_user.has_role(UserRole.PATIENT)
    }