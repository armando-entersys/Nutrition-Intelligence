"""
Modelos de Autenticación y Autorización
Sistema híbrido que soporta múltiples roles por usuario
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from sqlalchemy import JSON
import hashlib

class UserRole(str, Enum):
    """Roles disponibles en el sistema"""
    ADMIN = "admin"                 # Administrador del sistema
    NUTRITIONIST = "nutritionist"   # Nutricionista profesional
    PATIENT = "patient"             # Paciente
    SUPPORT = "support"             # Soporte técnico

class AccountStatus(str, Enum):
    """Estados de cuenta"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class AuthUser(SQLModel, table=True):
    """
    Usuario base del sistema con soporte para múltiples roles
    Un nutricionista puede ser también paciente (roles híbridos)
    """
    __tablename__ = "auth_users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Información básica
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    password_hash: str = Field(max_length=255)
    
    # Información personal
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    
    # Estado y configuración
    account_status: AccountStatus = Field(default=AccountStatus.PENDING_VERIFICATION)
    is_email_verified: bool = Field(default=False)
    is_phone_verified: bool = Field(default=False)
    
    # Roles (híbridos)
    primary_role: UserRole = Field(description="Rol principal del usuario")
    secondary_roles: List[UserRole] = Field(default=[], sa_column=Column(JSON), description="Roles adicionales")
    
    # Metadatos de autenticación
    last_login: Optional[datetime] = Field(default=None)
    login_count: int = Field(default=0)
    failed_login_attempts: int = Field(default=0)
    last_failed_login: Optional[datetime] = Field(default=None)
    password_changed_at: Optional[datetime] = Field(default=None)
    
    # Configuración de cuenta
    profile_completed: bool = Field(default=False)
    preferences: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user_sessions: List["UserSession"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[UserSession.user_id]"}
    )
    role_assignments: List["UserRoleAssignment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[UserRoleAssignment.user_id]"}
    )
    
    def set_password(self, password: str) -> None:
        """Establece la contraseña hasheada (usando hashlib temporalmente)"""
        # TODO: Replace with bcrypt for production
        salt = "nutrition_salt_2025"  # Fixed salt for simplicity
        combined = f"{password}{salt}"
        self.password_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        self.password_changed_at = datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """Verifica la contraseña (usando hashlib temporalmente)"""
        # TODO: Replace with bcrypt for production
        salt = "nutrition_salt_2025"  # Fixed salt for simplicity
        combined = f"{password}{salt}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest() == self.password_hash
    
    def has_role(self, role: UserRole) -> bool:
        """Verifica si el usuario tiene un rol específico"""
        return role == self.primary_role or role in self.secondary_roles
    
    def get_all_roles(self) -> List[UserRole]:
        """Obtiene todos los roles del usuario"""
        roles = [self.primary_role]
        roles.extend(self.secondary_roles)
        return list(set(roles))  # Elimina duplicados
    
    def add_secondary_role(self, role: UserRole) -> None:
        """Añade un rol secundario"""
        if role not in self.secondary_roles and role != self.primary_role:
            self.secondary_roles.append(role)
    
    def remove_secondary_role(self, role: UserRole) -> None:
        """Remueve un rol secundario"""
        if role in self.secondary_roles:
            self.secondary_roles.remove(role)
    
    @property
    def full_name(self) -> str:
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self) -> bool:
        """Verifica si la cuenta está activa"""
        return self.account_status == AccountStatus.ACTIVE

class UserSession(SQLModel, table=True):
    """Sesiones de usuario activas"""
    __tablename__ = "user_sessions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_users.id", index=True)
    
    # Información de la sesión
    session_token: str = Field(unique=True, index=True, max_length=255)
    refresh_token: Optional[str] = Field(default=None, max_length=255)
    expires_at: datetime
    
    # Información del cliente
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    device_info: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Estado
    is_active: bool = Field(default=True)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: AuthUser = Relationship(
        back_populates="user_sessions",
        sa_relationship_kwargs={"foreign_keys": "[UserSession.user_id]"}
    )

class UserRoleAssignment(SQLModel, table=True):
    """
    Asignaciones de roles con metadatos adicionales
    Permite rastrear quién asignó qué rol y cuándo
    """
    __tablename__ = "user_role_assignments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_users.id", index=True)
    role: UserRole = Field(index=True)
    
    # Metadatos de asignación
    assigned_by: Optional[int] = Field(default=None, foreign_key="auth_users.id")
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None, description="Rol temporal")
    
    # Contexto de asignación
    reason: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deactivated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: AuthUser = Relationship(
        back_populates="role_assignments",
        sa_relationship_kwargs={"foreign_keys": "[UserRoleAssignment.user_id]"}
    )

class PasswordResetToken(SQLModel, table=True):
    """Tokens para recuperación de contraseña"""
    __tablename__ = "password_reset_tokens"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_users.id", index=True)
    
    token: str = Field(unique=True, index=True, max_length=255)
    expires_at: datetime
    is_used: bool = Field(default=False)
    used_at: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmailVerificationToken(SQLModel, table=True):
    """Tokens para verificación de email"""
    __tablename__ = "email_verification_tokens"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_users.id", index=True)
    
    token: str = Field(unique=True, index=True, max_length=255)
    email: str = Field(max_length=255, description="Email a verificar")
    expires_at: datetime
    is_used: bool = Field(default=False)
    used_at: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Constantes para configuración de roles
ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        "name": "Administrador",
        "description": "Acceso completo al sistema",
        "permissions": [
            "manage_users", "manage_roles", "view_logs", "system_config",
            "manage_nutritionists", "manage_patients", "view_all_data"
        ],
        "default_dashboard": "admin"
    },
    UserRole.NUTRITIONIST: {
        "name": "Nutricionista",
        "description": "Profesional de la nutrición",
        "permissions": [
            "create_meal_plans", "calculate_nutrition", "manage_patients",
            "view_equivalences", "create_recipes", "assign_diets"
        ],
        "default_dashboard": "nutritionist"
    },
    UserRole.PATIENT: {
        "name": "Paciente",
        "description": "Usuario que recibe atención nutricional",
        "permissions": [
            "view_meal_plan", "track_consumption", "rate_recipes",
            "view_progress", "update_profile", "view_equivalences"
        ],
        "default_dashboard": "patient"
    },
    UserRole.SUPPORT: {
        "name": "Soporte",
        "description": "Soporte técnico",
        "permissions": [
            "view_logs", "assist_users", "reset_passwords", "view_system_status"
        ],
        "default_dashboard": "support"
    }
}

# Funciones helper
def get_role_permissions(role: UserRole) -> List[str]:
    """Obtiene los permisos de un rol"""
    return ROLE_PERMISSIONS.get(role, {}).get("permissions", [])

def get_user_permissions(user: AuthUser) -> List[str]:
    """Obtiene todos los permisos de un usuario basado en sus roles"""
    permissions = set()
    for role in user.get_all_roles():
        permissions.update(get_role_permissions(role))
    return list(permissions)

def can_user_access(user: AuthUser, required_permission: str) -> bool:
    """Verifica si un usuario tiene un permiso específico"""
    user_permissions = get_user_permissions(user)
    return required_permission in user_permissions