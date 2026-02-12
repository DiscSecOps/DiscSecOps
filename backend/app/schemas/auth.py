"""
Authentication schemas
Request and response models for registration, login, and user data
Updated to match frontend expectations: username-based login!
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """
    Schema for user registration request from frontend
    """
    email: str = Field(..., description="User email (unique)")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    full_name: str | None = Field(None, max_length=100, description="User's full name")
    username: str | None = Field(None, max_length=50, description="Optional username")


class UserLogin(BaseModel):
    """
    Schema for user login request from frontend
    """
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """
    Schema for user data in API responses
    """
    id: int
    email: str
    username: str | None
    full_name: str | None
    role_id: int | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Schema for JWT token response after successful login

    Example response:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class SessionResponse(BaseModel):
    """
    Schema for session-based authentication response
    Frontend team requested sessions as alternative to JWT

    Example response:
    {
        "success": true,
        "username": "johndoe",
        "session_token": "abc123...",
        "user": {...}
    }
    """
    success: bool = Field(default=True)
    email: str | None = None
    username: str | None = None
    session_token: str | None = None  # Only if using session-based auth
    user: UserResponse | None = None


class TokenData(BaseModel):
    """
    Schema for decoded token data
    Used internally for token validation
    """
    username: str | None = None
