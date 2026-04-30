# auth.py - Authentication endpoints (ASYNC for PostgreSQL)
"""
Authentication endpoints (ASYNC for PostgreSQL)
Matches frontend expectations:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- POST /api/v1/auth/logout
"""

import logging
import secrets
import traceback
from datetime import datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.core.security import get_password_hash, verify_password
from app.db.models import User, UserSession
from app.schemas.auth import SessionResponse, UserCreate, UserLogin, UserResponse

# -----------------------------
# LOGGER
# -----------------------------
logger = logging.getLogger("auth")

# -----------------------------
# RATE LIMITER
# -----------------------------
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> SessionResponse:

    username = await db.execute(select(User).where(User.username == user_data.username))
    if username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    email = await db.execute(
        select(User).where(func.lower(User.email) == func.lower(user_data.email))
    )
    if email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already taken")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info({
        "event": "user_registered",
        "username": new_user.username,
        "user_id": new_user.id
    })
    print(f"✅ REGISTER: {new_user.username} (ID: {new_user.id})")

    return SessionResponse(
        success=True,
        username=new_user.username,
        session_token=None,
        user=UserResponse.model_validate(new_user)
    )


# -----------------------------
# LOGIN (with rate limiting + logging)
# -----------------------------
@router.post("/login", response_model=SessionResponse)
@limiter.limit("5/minute")
async def login(
    credentials: UserLogin,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> SessionResponse:

    try:
        # Find user
        result = await db.execute(
            select(User).where(User.username == credentials.username)
        )
        user = result.scalar_one_or_none()

        if not user:
            client_ip = request.client.host if request.client else "unknown"
            logger.warning({
                "event": "auth_failed",
                "username": credentials.username,
                "ip": client_ip,
                "reason": "user_not_found"
            })
            print(f"❌ LOGIN FAILED: {credentials.username} - {client_ip} - User not found")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            client_ip = request.client.host if request.client else "unknown"
            logger.warning({
                "event": "auth_failed",
                "username": credentials.username,
                "ip": client_ip,
                "reason": "invalid_password"
            })
            print(f"❌ LOGIN FAILED: {credentials.username} - {client_ip} - Invalid password")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Check active
        if not user.is_active:
            client_ip = request.client.host if request.client else "unknown"
            logger.warning({
                "event": "auth_failed",
                "username": credentials.username,
                "ip": client_ip,
                "reason": "inactive_account"
            })
            print(f"❌ LOGIN FAILED: {credentials.username} - {client_ip} - Inactive account")
            raise HTTPException(status_code=403, detail="Account is inactive")

        # SUCCESS LOG
        client_ip = request.client.host if request.client else "unknown"
        logger.info({
            "event": "auth_success",
            "user_id": user.id,
            "username": user.username,
            "ip": client_ip
        })
        print(f"🔐 LOGIN SUCCESS: {user.username} (ID: {user.id}) - {client_ip}")

        # Create session
        session_token = secrets.token_urlsafe(32)
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

        secure_flag = settings.ENVIRONMENT == "production"
        samesite_value: Literal["lax", "none"] = "none" if secure_flag else "lax"

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=secure_flag,
            samesite=samesite_value,
            max_age=settings.SESSION_EXPIRE_MINUTES * 60,
            path="/",
        )

        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
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
        logger.error({
            "event": "auth_error",
            "error": str(e),
            "trace": traceback.format_exc()
        })
        print(f"🚨 AUTH ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed due to server error") from e


# -----------------------------
# GET CURRENT USER
# -----------------------------
async def get_current_user_from_session(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:

    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_result = await db.execute(
        select(UserSession)
        .where(UserSession.session_token == session_token)
        .where(UserSession.expires_at > datetime.now())
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    user_result = await db.execute(select(User).where(User.id == session.user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user_from_session)
) -> UserResponse:

    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


# -----------------------------
# LOGOUT
# -----------------------------
@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:

    session_token = request.cookies.get("session_token")

    if session_token:
        result = await db.execute(
            select(UserSession).where(UserSession.session_token == session_token)
        )
        session = result.scalar_one_or_none()

        if session:
            await db.delete(session)
            await db.commit()

        secure_flag = settings.ENVIRONMENT == "production"
        samesite_value: Literal["lax", "none"] = "none" if secure_flag else "lax"

        response.delete_cookie(
            "session_token",
            path="/",
            secure=secure_flag,
            samesite=samesite_value
        )

    logger.info({
        "event": "logout",
        "ip": (request.client.host if request.client else "unknown")
    })

    return {"success": True, "message": "Logged out successfully"}
# settings. VERSION
