"""
Main FastAPI application (ASYNC with PostgreSQL)
Initializes the API with authentication endpoints and CORS for frontend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.endpoints import auth
from app.db.models import Base
from app.core.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    Creates database tables on startup
    """
    # Create all tables on startup (async)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Application runs here
    
    # Cleanup on shutdown (if needed)
    await engine.dispose()


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Social application backend with authentication",
    lifespan=lifespan
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include authentication router at /api/auth (matches frontend expectations!)
# Frontend expects: http://localhost:5000/api/auth/login
app.include_router(auth.router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "DevSecOps Social App API",
        "version": settings.VERSION,
        "status": "running",
        "database": "PostgreSQL (Async)",
        "auth_endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login (supports JWT and sessions)",
            "logout": "POST /api/auth/logout"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check for monitoring
    Frontend can use this to verify backend is running
    """
    return {"status": "healthy", "database": "PostgreSQL"}


@app.get("/api/health")
async def api_health():
    """API-specific health check"""
    return {"status": "healthy", "api_version": settings.VERSION}
