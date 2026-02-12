"""
User model for authentication (Async SQLAlchemy 2.0)
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Role(Base):
    """
    Role model for system and circle permissions
    """
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


class User(Base):
    """
    User model for authentication with async PostgreSQL

    Attributes:
        id: Unique user identifier
        email: User's email (UNIQUE, PRIMARY LOGIN FIELD)
        username: User's username (optional/display only)
        full_name: User's full name
        hashed_password: Argon2 hashed password
        role_id: ForeignKey to Role.id
        is_active: Whether user account is active
        is_superuser: Whether user has admin privileges
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication - EMAIL is primary login
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # User information
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Role-based access control
    role_id: Mapped[int | None] = mapped_column(nullable=True) # ForeignKey to Role.id
    
    # Legacy role field (optional, can be removed later or mapped to role_id)
    # role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

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


class Circle(Base):
    """
    Circle model for groups of users
    """
    __tablename__ = "circles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)  # ForeignKey to User.id
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class CircleMember(Base):
    """
    Association table for Circle members
    """
    __tablename__ = "circle_members"

    circle_id: Mapped[int] = mapped_column(primary_key=True)  # ForeignKey to Circle.id
    user_id: Mapped[int] = mapped_column(primary_key=True)    # ForeignKey to User.id
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Post(Base):
    """
    Post model for user content
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(nullable=False, index=True) # ForeignKey to User.id
    circle_id: Mapped[int | None] = mapped_column(nullable=True, index=True) # ForeignKey to Circle.id (optional)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title}, author_id={self.author_id})>"


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
