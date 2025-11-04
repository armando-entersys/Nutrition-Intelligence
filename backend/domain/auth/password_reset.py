"""
Password Reset Token Model
Tokens para recuperación de contraseña
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
import secrets

class TokenStatus(str, Enum):
    """Estado del token"""
    ACTIVE = "active"
    USED = "used"
    EXPIRED = "expired"
    REVOKED = "revoked"

class PasswordResetToken(SQLModel, table=True):
    """
    Tokens de recuperación de contraseña
    Los tokens expiran después de 1 hora y son de un solo uso
    """
    __tablename__ = "password_reset_tokens"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)

    # Token único
    token: str = Field(unique=True, index=True, max_length=255)

    # Usuario asociado
    user_id: int = Field(foreign_key="auth_users.id", index=True)
    email: str = Field(index=True, max_length=255)

    # Estado y control
    status: TokenStatus = Field(default=TokenStatus.ACTIVE)
    expires_at: datetime
    used_at: Optional[datetime] = Field(default=None)

    # Metadata
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def generate_token(cls) -> str:
        """Genera un token seguro de 32 caracteres"""
        return secrets.token_urlsafe(32)

    @classmethod
    def create_for_user(
        cls,
        user_id: int,
        email: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> "PasswordResetToken":
        """Crea un nuevo token de recuperación"""
        token = cls.generate_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)

        return cls(
            token=token,
            user_id=user_id,
            email=email,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )

    def is_valid(self) -> bool:
        """Verifica si el token es válido"""
        if self.status != TokenStatus.ACTIVE:
            return False
        if datetime.utcnow() > self.expires_at:
            self.status = TokenStatus.EXPIRED
            return False
        return True

    def mark_as_used(self) -> None:
        """Marca el token como usado"""
        self.status = TokenStatus.USED
        self.used_at = datetime.utcnow()

    def revoke(self) -> None:
        """Revoca el token"""
        self.status = TokenStatus.REVOKED
