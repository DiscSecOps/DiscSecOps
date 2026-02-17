# auth.py - Authentication endpoints (ASYNC for PostgreSQL)
"""
Authentication endpoints (ASYNC for PostgreSQL)
Matches frontend expectations:
- POST /api/v1/auth/register - Create new user account
- POST /api/v1/auth/login - Login and get JWT token OR session
- Username-based authentication (not email!)
- Port 8000 (configured in main.py or frontend updated)
"""

import logging
import secrets
import traceback
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.core.security import get_password_hash, verify_password
from app.db.models import User, UserSession
from app.schemas.auth import SessionResponse, UserCreate, UserLogin, UserResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> SessionResponse:
    """
    Register a new user (ASYNC)

    Frontend sends POST request to /api/auth/register with:
    ```json
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "username": "optional_username"
    }
    ```

    Returns:
    - 201: User created successfully
    - 400: Username already registered
    """
    # Check if username already exists (ASYNC!)
    result = await db.execute(select(User).where(User.username == user_data.username))
    db_user = result.scalar_one_or_none()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Hash password using Argon2
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role_id=None, # Default role (can be set later)
        is_active=True,
        is_superuser=False,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Return success response matching frontend expectations
    return SessionResponse(
        success=True,
        username=new_user.username,
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login")
async def login(
    credentials: UserLogin, request: Request, response: Response, db: AsyncSession = Depends(get_db)
) -> SessionResponse:
    """
    Login user and create session (SESSION-BASED AUTH)

    Frontend sends POST request to /api/auth/login with:
    ```json
    {
        "username": "johndoe",
        "password": "SecurePass123!"
    }
    ```

    Returns:
    - 200: Login successful with session token
    - 401: Invalid credentials
    """
    try:
        # Find user by username with eager loading
        stmt = (
            select(User)
            .where(User.username == credentials.username)
            .execution_options(populate_existing=True)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Explicitly access all attributes now to force loading in async context
        _ = (
            user.id,
            user.username,
            user.email,
            user.full_name,
            user.role_id,
            user.is_active,
            user.is_superuser,
            user.created_at,
            user.updated_at,
            user.hashed_password,
        )

        # Verify password using Argon2
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

        # Session-based authentication (default now as per frontend team request)
        # Generate secure session token
        session_token = secrets.token_urlsafe(32)

        # Create session in database
        now = datetime.now()
        expires_at = now + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)
        new_session = UserSession(
            session_token=session_token,
            user_id=user.id,
            created_at=now,
            expires_at=expires_at,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        db.add(new_session)
        await db.commit()

        # Set HTTP-only cookie (more secure than localStorage)
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.SESSION_EXPIRE_MINUTES * 60,
        )

        # Build user response manually to avoid MissingGreenlet with async PostgreSQL
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role_id=user.role_id,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        return SessionResponse(
            success=True,
            username=user.username,
            session_token=session_token,
            user=user_response
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {type(e).__name__}: {str(e)}")
        logger.error(traceback.format_exc())
        # Add 'from e' here:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}") from e


@router.post("/logout")
async def logout(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """
    Logout user (invalidate session if using session-based auth)

    For JWT: Frontend just deletes the token (can't invalidate server-side)
    For Sessions: Delete session from database
    """
    session_token = request.cookies.get("session_token")

    if session_token:
        # Delete session from database
        result = await db.execute(
            select(UserSession).where(UserSession.session_token == session_token)
        )
        session = result.scalar_one_or_none()

        if session:
            await db.delete(session)
            await db.commit()

        # Clear cookie
        response.delete_cookie("session_token")

    return {"success": True, "message": "Logged out successfully"}


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Retrieve users.
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

# backend/app/api/auth.py -helper function to get current user from session (for session-based auth)

@router.get("/me")  # 👈 create one endpoint GET /api/auth/me
async def get_current_user(
    request: Request,           # 👈 receive request
    db: AsyncSession = Depends(get_db)  # 👈 conexione to db
) -> dict[str, Any]: # TODO: change to specific type later
    """
    Get current authenticated user
    Returns 401 if not authenticated
    """
    # 1️⃣ get session token from cookie (session-based auth)
    session_token = request.cookies.get("session_token")

    # 2️⃣ if no session token -> 401
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 3️⃣ search session in database (async) - find session by token
    session_result = await db.execute(
        select(UserSession).where(UserSession.session_token == session_token)
    )
    session = session_result.scalar_one_or_none()

    # 4️⃣ is session valid? (exists and not expired)
    if not session or session.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Session expired")

    # 5️⃣ find user by session.user_id (async)
    user_result = await db.execute(select(User).where(User.id == session.user_id))
    user = user_result.scalar_one_or_none()

    # 6️⃣ if no user -> 401 (should not happen if session is valid, but just in case)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 7️⃣ return user info (matching UserResponse schema, but we can return only relevant fields)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role_id": user.role_id,  # 👈 for future rols
        "is_active": user.is_active,
        "is_superuser": user.is_superuser
    }
