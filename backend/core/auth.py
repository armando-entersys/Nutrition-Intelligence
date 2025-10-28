"""
Sistema de Autenticación y Autorización
JWT tokens, middleware de autenticación, y decoradores de permisos
"""
from jose import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from core.config import get_settings
from core.database import get_async_session
from domain.auth.models import AuthUser, UserSession, UserRole, get_user_permissions, can_user_access
from core.logging import log_success, log_error

settings = get_settings()

# Configuración JWT
JWT_SECRET_KEY = settings.secret_key or "nutrition-intelligence-secret-key"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security scheme
security = HTTPBearer()

class AuthenticationError(HTTPException):
    """Errores de autenticación"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class AuthorizationError(HTTPException):
    """Errores de autorización"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

def create_access_token(user: AuthUser, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "primary_role": user.primary_role.value,
        "secondary_roles": [role.value for role in user.secondary_roles],
        "exp": expire,
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user: AuthUser) -> str:
    """Crea un token JWT de refresco"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "user_id": user.id,
        "exp": expire,
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.JWTError:
        raise AuthenticationError("Invalid token")

def generate_session_token() -> str:
    """Genera un token de sesión único"""
    return secrets.token_urlsafe(32)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_async_session)
) -> AuthUser:
    """
    Obtiene el usuario actual basado en el token JWT
    """
    try:
        # Verificar token
        payload = verify_token(credentials.credentials)
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise AuthenticationError("Invalid token payload")
        
        # Buscar usuario en base de datos
        statement = select(AuthUser).where(AuthUser.id == user_id)
        result = await session.exec(statement)
        user = result.first()
        
        if user is None:
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        # Actualizar última actividad
        user.last_login = datetime.utcnow()
        session.add(user)
        await session.commit()
        
        log_success(
            f"Usuario autenticado: {user.email} ({user.primary_role.value})",
            business_context={
                "action": "user_authentication",
                "user_id": user.id,
                "user_email": user.email,
                "primary_role": user.primary_role.value
            }
        )
        
        return user
        
    except AuthenticationError:
        raise
    except Exception as e:
        log_error(f"Error en autenticación: {str(e)}")
        raise AuthenticationError("Authentication failed")

async def get_current_active_user(
    current_user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """
    Obtiene el usuario actual verificando que esté activo
    """
    if not current_user.is_active:
        raise AuthenticationError("Inactive user")
    return current_user

def require_role(required_role: UserRole):
    """
    Decorador de dependencia que requiere un rol específico
    """
    async def role_checker(current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
        if not current_user.has_role(required_role):
            raise AuthorizationError(f"Role '{required_role.value}' required")
        return current_user
    
    return role_checker

def require_permission(required_permission: str):
    """
    Decorador de dependencia que requiere un permiso específico
    """
    async def permission_checker(current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
        if not can_user_access(current_user, required_permission):
            raise AuthorizationError(f"Permission '{required_permission}' required")
        return current_user
    
    return permission_checker

def require_any_role(required_roles: List[UserRole]):
    """
    Decorador de dependencia que requiere cualquiera de los roles especificados
    """
    async def role_checker(current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
        user_roles = current_user.get_all_roles()
        if not any(role in user_roles for role in required_roles):
            role_names = [role.value for role in required_roles]
            raise AuthorizationError(f"One of these roles required: {', '.join(role_names)}")
        return current_user
    
    return role_checker

# Dependencias específicas por rol
async def get_admin_user(current_user: AuthUser = Depends(require_role(UserRole.ADMIN))) -> AuthUser:
    """Obtiene usuario con rol de administrador"""
    return current_user

async def get_nutritionist_user(current_user: AuthUser = Depends(require_role(UserRole.NUTRITIONIST))) -> AuthUser:
    """Obtiene usuario con rol de nutricionista"""
    return current_user

async def get_patient_user(current_user: AuthUser = Depends(require_role(UserRole.PATIENT))) -> AuthUser:
    """Obtiene usuario con rol de paciente"""
    return current_user

async def get_nutritionist_or_admin(
    current_user: AuthUser = Depends(require_any_role([UserRole.NUTRITIONIST, UserRole.ADMIN]))
) -> AuthUser:
    """Obtiene usuario que sea nutricionista o administrador"""
    return current_user

async def get_patient_or_nutritionist(
    current_user: AuthUser = Depends(require_any_role([UserRole.PATIENT, UserRole.NUTRITIONIST]))
) -> AuthUser:
    """Obtiene usuario que sea paciente o nutricionista (roles híbridos)"""
    return current_user

class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def authenticate_user(self, email: str, password: str) -> Optional[AuthUser]:
        """Autentica un usuario con email y contraseña"""
        try:
            statement = select(AuthUser).where(AuthUser.email == email)
            result = await self.session.exec(statement)
            user = result.first()
            
            if not user:
                log_error(f"Intento de login fallido - Usuario no encontrado: {email}")
                return None
            
            if not user.verify_password(password):
                # Incrementar intentos fallidos
                user.failed_login_attempts += 1
                user.last_failed_login = datetime.utcnow()
                self.session.add(user)
                await self.session.commit()
                
                log_error(f"Intento de login fallido - Contraseña incorrecta: {email}")
                return None
            
            if not user.is_active:
                log_error(f"Intento de login fallido - Cuenta inactiva: {email}")
                return None
            
            # Login exitoso - resetear intentos fallidos
            user.failed_login_attempts = 0
            user.last_failed_login = None
            user.last_login = datetime.utcnow()
            user.login_count += 1
            self.session.add(user)
            await self.session.commit()
            
            log_success(
                f"Login exitoso: {email} ({user.primary_role.value})",
                business_context={
                    "action": "user_login",
                    "user_id": user.id,
                    "user_email": email,
                    "login_count": user.login_count
                }
            )
            
            return user
            
        except Exception as e:
            log_error(f"Error en autenticación de usuario {email}: {str(e)}")
            return None
    
    async def create_user_session(
        self, 
        user: AuthUser, 
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserSession:
        """Crea una nueva sesión de usuario"""
        try:
            # Generar tokens
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            session_token = generate_session_token()
            
            # Crear sesión
            user_session = UserSession(
                user_id=user.id,
                session_token=session_token,
                refresh_token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            self.session.add(user_session)
            await self.session.commit()
            await self.session.refresh(user_session)
            
            log_success(
                f"Sesión creada para usuario: {user.email}",
                business_context={
                    "action": "session_creation",
                    "user_id": user.id,
                    "session_id": user_session.id
                }
            )
            
            return user_session
            
        except Exception as e:
            log_error(f"Error creando sesión para usuario {user.id}: {str(e)}")
            raise
    
    async def logout_user(self, session_token: str) -> bool:
        """Cierra sesión de usuario"""
        try:
            statement = select(UserSession).where(
                UserSession.session_token == session_token,
                UserSession.is_active == True
            )
            result = await self.session.exec(statement)
            user_session = result.first()
            
            if user_session:
                user_session.is_active = False
                self.session.add(user_session)
                await self.session.commit()
                
                log_success(
                    f"Sesión cerrada: {user_session.user_id}",
                    business_context={
                        "action": "user_logout",
                        "user_id": user_session.user_id,
                        "session_id": user_session.id
                    }
                )
                return True
            
            return False
            
        except Exception as e:
            log_error(f"Error cerrando sesión {session_token}: {str(e)}")
            return False