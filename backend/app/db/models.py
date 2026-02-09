"""
User model for authentication (Async SQLAlchemy 2.0)
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    User model for authentication with async PostgreSQL

    Attributes:
        id: Unique user identifier
        username: User's username (UNIQUE, PRIMARY LOGIN FIELD - matches frontend!)
        email: User's email (optional, for notifications/password reset)
        full_name: User's full name
        hashed_password: Argon2 hashed password
        role: User role (user, admin, manager) - for future RBAC
        is_active: Whether user account is active
        is_superuser: Whether user has admin privileges
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication - USERNAME is primary login (frontend expects this!)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # User information
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Role-based access control (for future features)
    role: Mapped[str] = mapped_column(
        String(20), default="user", nullable=False
    )  # "user", "admin", "manager"

    # Status flags
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


# Session model for session-based authentication (alternative to JWT)
class UserSession(Base):
    """
    User session model for session-based authentication
    Frontend team requested sessions instead of just JWT tokens
    """
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"
