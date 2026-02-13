"""
Authentication schemas
Request and response models for registration, login, and user data
Updated to match frontend expectations: username-based login!
"""
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    """
    Schema for user registration request from frontend

    Frontend sends (from RegisterPage.jsx):
    {
        "username": "johndoe",
        "password": "SecurePass123!"
        "full_name": "John Doe",  # Optional
        "email": "john.doe@example.com"
    }
    """
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    full_name: str | None = Field(None, max_length=100, description="User's full name")
    email: EmailStr | None = Field(None, description="User's email address")

class UserLogin(BaseModel):
    """
    Schema for user login request from frontend

    Frontend sends (from LoginPage.jsx and auth.service.js):
    {
        "username": "johndoe",
        "password": "SecurePass123!"
    }

    Note: Frontend uses USERNAME, not email!
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """
    Schema for user data in API responses

    Note: Never includes password or hashed_password
    Email removed as per frontend team request
    """
    id: int
    username: str
    email: str | None  # Changed from EmailStr to str since email is always None now
    full_name: str | None
    role: str  # "user", "admin", "manager"
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True  # Allows creation from SQLAlchemy models


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
    username: str
    session_token: str | None = None  # Only if using session-based auth
    user: UserResponse | None = None


class TokenData(BaseModel):
    """
    Schema for decoded token data
    Used internally for token validation
    """
    username: str | None = None
