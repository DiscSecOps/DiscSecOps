# DevSecOps Environment Best Practices - Session-Based Authentication

**Project:** DevSecOps Full Stack Application  
**Auth Method:** Session-Based (HTTP-only cookies)  
**Date:** February 12, 2026  
**Focus:** Practical DevSecOps with Security, Automation, CI/CD

---

## 🎯 Executive Summary: Our Session-Based Approach

**Key Difference from Token-Based:**
- ✅ **Sessions** → Secrets stored server-side (backend `.env` only)
- ✅ **HTTP-only cookies** → Frontend needs NO auth secrets
- ✅ **Simpler security** → Frontend `.env` has zero sensitive data
- ✅ **Better control** → Sessions can be revoked immediately server-side

---

## 📐 DevSecOps Principles Applied

### 1. **Security by Design** 🔒

| Principle | Implementation | Session-Based Benefit |
|-----------|----------------|----------------------|
| **Least Privilege** | Each service only knows what it needs | Frontend has ZERO auth secrets |
| **Defense in Depth** | Multiple security layers | Cookie flags + CORS + HTTPS |
| **Zero Trust** | Never trust, always verify | Backend validates every request |
| **Secrets Management** | External secret stores | Only backend needs secret manager |

### 2. **Automation** 🤖

| Aspect | Automation Strategy |
|--------|-------------------|
| **Environment Setup** | Scripts auto-create `.env` from templates |
| **Secret Rotation** | Automated via CI/CD pipeline |
| **Validation** | Pre-commit hooks check for leaked secrets |
| **Testing** | Different `.env` files per test environment |

### 3. **CI/CD Integration** 🚀

| Stage | Environment Strategy |
|-------|---------------------|
| **Development** | Local `.env` files (git-ignored) |
| **CI Testing** | Injected via GitHub Secrets |
| **Staging** | Secret manager (AWS/Azure) |
| **Production** | Secret manager + rotation |

### 4. **Reproducibility** 🔄

| Component | Strategy |
|-----------|----------|
| **Configuration** | `.env.example` files in git |
| **Documentation** | Inline comments in examples |
| **Defaults** | Fallback values in code |
| **Validation** | Config validation on startup |

---

## 🏗️ Architecture: Session-Based Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (.env)                          │
│  - VITE_API_URL (public)                                    │
│  - Feature flags (public)                                   │
│  - NO SECRETS ✅                                             │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ HTTP Request
                             │ + Session Cookie (HTTP-only)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (.env)                          │
│  🔒 SECRET_KEY (JWT signing - backup only)                  │
│  🔒 SESSION_SECRET_KEY (cookie signing) ← CRITICAL          │
│  🔒 DATABASE_URL (connection string)                        │
│  🔒 ALLOWED_ORIGINS (CORS whitelist)                        │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE                                │
│  - User credentials (hashed with Argon2)                    │
│  - Session data (session_token, user_id, expires_at)       │
└─────────────────────────────────────────────────────────────┘
```

**Security Benefits:**
- Frontend never sees secrets (HTTP-only cookie = JavaScript can't access)
- Session token never exposed to XSS attacks
- Backend controls everything (session validation, expiry, revocation)
- CSRF protection via SameSite cookie attribute

---

## 📂 File Structure: Where Everything Goes

### ✅ Recommended Structure (Our Implementation)

```
project-root/
│
├── .gitignore                          ← Protect .env files
├── ENVIRONMENT_SETUP_GUIDE.md          ← This document
├── docker-compose.yml                  ← Container orchestration
│
├── backend/                            ← Backend service
│   ├── .env                           ❌ NEVER COMMIT (secrets here)
│   ├── .env.example                   ✅ COMMIT (template)
│   ├── .env.development               ❌ NEVER COMMIT
│   ├── .env.test                      ✅ COMMIT (no real secrets)
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py              ✅ Configuration loader
│   │   │   └── security.py            ✅ Session management
│   │   └── main.py
│   └── tests/
│       └── .env.test                  ✅ Test-specific config
│
├── frontend/                           ← Frontend service
│   ├── .env                           ❌ NEVER COMMIT (but no secrets!)
│   ├── .env.example                   ✅ COMMIT (template)
│   ├── .env.development               ❌ NEVER COMMIT
│   ├── .env.production                ❌ NEVER COMMIT
│   ├── src/
│   │   └── services/
│   │       └── auth.service.js        ✅ Uses env vars
│   └── setup-env.ps1                  ✅ Setup automation
│
└── .github/
    └── workflows/
        └── ci-cd.yml                   ✅ CI/CD with secrets injection
```

### ❌ Anti-Patterns to Avoid

```
BAD-project/
├── .env                              ❌ Root .env (confusing)
├── config/
│   └── secrets.json                  ❌ Secrets in JSON
├── backend/
│   └── app/
│       └── config.py                 ❌ Hardcoded secrets
└── frontend/
    └── src/
        └── config.js                 ❌ API keys exposed
```

---

## 🔐 Session-Based Auth: Environment Variables Breakdown

### Backend Environment Variables (Critical Security)

```bash
# backend/.env

# ============================================================================
# SESSION SECURITY (Most Critical for Session-Based Auth)
# ============================================================================
# Used to sign session cookies - MUST be cryptographically secure
SESSION_SECRET_KEY=<64-char-random-hex>
SESSION_EXPIRE_MINUTES=1440  # 24 hours

# Session cookie configuration (secure defaults)
SESSION_COOKIE_HTTPONLY=true      # JavaScript cannot access
SESSION_COOKIE_SECURE=true        # HTTPS only (set false for local dev)
SESSION_COOKIE_SAMESITE=lax       # CSRF protection

# ============================================================================
# JWT SECURITY (Backup/API tokens if needed)
# ============================================================================
# Only needed if you also support JWT for mobile apps/APIs
SECRET_KEY=<64-char-random-hex>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================================================
# DATABASE (Session Storage)
# ============================================================================
# Sessions stored here - protect this connection string!
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/app_db

# Database pool settings (performance + security)
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30

# ============================================================================
# CORS (Critical for Session Cookies)
# ============================================================================
# Frontend origins that can send cookies
ALLOWED_ORIGINS=["https://app.yourproject.com","https://www.yourproject.com"]

# ⚠️ NEVER use "*" with credentials=true (browser blocks it)
# ⚠️ List specific domains only

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_PORT=8000
API_V1_STR=/api/v1
API_RATE_LIMIT=100  # requests per minute per IP

# ============================================================================
# SECURITY HEADERS
# ============================================================================
# Additional security for session-based auth
HSTS_MAX_AGE=31536000              # Enforce HTTPS
CSRF_PROTECTION=true               # Additional CSRF checks
SESSION_REGENERATE_ON_LOGIN=true  # Prevent session fixation

# ============================================================================
# LOGGING & MONITORING
# ============================================================================
LOG_LEVEL=INFO
LOG_SESSION_EVENTS=true  # Log session creation/deletion
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx  # Error tracking

# ============================================================================
# ENVIRONMENT
# ============================================================================
ENVIRONMENT=production
DEBUG=false
```

### Frontend Environment Variables (No Secrets!)

```bash
# frontend/.env

# ============================================================================
# API CONFIGURATION (Public - No Secrets!)
# ============================================================================
VITE_API_URL=https://api.yourproject.com/api
VITE_API_TIMEOUT=10000

# ============================================================================
# FEATURE FLAGS (Public)
# ============================================================================
VITE_ENV=production
VITE_ENABLE_DEBUG=false
VITE_ENABLE_ANALYTICS=true

# ============================================================================
# EXTERNAL SERVICES (Public IDs only - no secrets!)
# ============================================================================
VITE_GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X
VITE_SENTRY_DSN=https://public-key@sentry.io/xxxxx

# ============================================================================
# SESSION CONFIGURATION (Client-side awareness)
# ============================================================================
# These are just for UI behavior - no security impact
VITE_SESSION_TIMEOUT_WARNING=300000  # Warn 5 min before expiry
VITE_AUTO_LOGOUT_ON_INACTIVITY=true

# ⚠️ NEVER put session secrets here!
# ⚠️ Session validation happens server-side only
```

**Key Points:**
- Frontend has ZERO sensitive data (all `VITE_` vars are public)
- Backend holds all security-critical configuration
- Session secrets never leave the server

---

## 🛡️ DevSecOps Security Best Practices

### 1. Secret Generation (Automation)

**❌ Weak Secrets (NEVER use these):**
```bash
SECRET_KEY=secret123
SESSION_SECRET_KEY=mysessionkey
```

**✅ Strong Secrets (Automated generation):**

```powershell
# PowerShell - Generate secure secret
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

# Output: dGhpcyBpcyBhIHNlY3VyZSByYW5kb20gc3RyaW5nIG9mIDY0IGJpdHM=
```

```bash
# Linux/Mac - Generate secure secret
openssl rand -hex 32

# Output: a8f5f167f44f4964e6c998dee827110c1a9b4b3f1e2d5c6b7a8e9f0d1c2b3a4e5f6
```

```python
# Python - Generate secure secret
import secrets
print(secrets.token_hex(32))

# Output: 7b2c9e1f6d4a8b3c5e7f9a1d3c5e7b9f1a3c5e7d9b1f3a5c7e9b1d3f5a7c9e1b3d5
```

**Automation Script:**
```powershell
# setup-secrets.ps1
$sessionSecret = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
$jwtSecret = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

Write-Host "Add these to backend/.env:" -ForegroundColor Green
Write-Host "SESSION_SECRET_KEY=$sessionSecret"
Write-Host "SECRET_KEY=$jwtSecret"
```

---

### 2. Secret Rotation (Automation + CI/CD)

**Rotation Schedule:**
- **Development:** Every 90 days
- **Staging:** Every 30 days
- **Production:** Every 30 days + after incidents

**Automated Rotation Script:**
```python
# scripts/rotate-secrets.py
import os
import secrets
from datetime import datetime

def generate_secret():
    return secrets.token_hex(32)

def rotate_session_secret():
    """Rotate session secret with zero downtime"""
    # 1. Generate new secret
    new_secret = generate_secret()
    
    # 2. Keep old secret valid for 24h (grace period)
    old_secret = os.getenv('SESSION_SECRET_KEY')
    
    # 3. Update secret in secret manager
    update_secret_manager('SESSION_SECRET_KEY', new_secret)
    update_secret_manager('SESSION_SECRET_KEY_OLD', old_secret)
    
    # 4. Log rotation event
    log_rotation_event('SESSION_SECRET_KEY', datetime.now())
    
    # 5. Notify team
    send_notification('Session secret rotated')

if __name__ == '__main__':
    rotate_session_secret()
```

**CI/CD Integration:**
```yaml
# .github/workflows/rotate-secrets.yml
name: Rotate Secrets Monthly

on:
  schedule:
    - cron: '0 0 1 * *'  # 1st of every month
  workflow_dispatch:      # Manual trigger

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Rotate secrets
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          python scripts/rotate-secrets.py
      
      - name: Update staging
        run: |
          # Restart staging with new secrets
          kubectl rollout restart deployment/backend -n staging
      
      - name: Create PR for production
        run: |
          # Create PR for manual production approval
          gh pr create --title "Secret Rotation - $(date +%Y-%m)" \
                       --body "Automated monthly secret rotation"
```

---

### 3. Pre-Commit Hooks (Prevent Secret Leaks)

**Install git-secrets or detect-secrets:**
```bash
# Install detect-secrets
pip install detect-secrets

# Initialize in repo
detect-secrets scan > .secrets.baseline

# Add pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
detect-secrets scan --baseline .secrets.baseline
if [ $? -ne 0 ]; then
    echo "❌ Potential secrets detected! Commit blocked."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

**Pre-commit config:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json
```

---

### 4. Environment Validation (Fail Fast)

**Backend config validation:**
```python
# backend/app/core/config.py
from pydantic import BaseSettings, validator
import os
import sys

class Settings(BaseSettings):
    # Session configuration
    SESSION_SECRET_KEY: str
    SESSION_EXPIRE_MINUTES: int = 1440
    
    # Security validation
    @validator('SESSION_SECRET_KEY')
    def validate_session_secret(cls, v):
        """Ensure session secret is strong"""
        if len(v) < 32:
            raise ValueError('SESSION_SECRET_KEY must be at least 32 characters')
        if v in ['secret', 'changeme', 'dev-secret']:
            raise ValueError('SESSION_SECRET_KEY is too weak!')
        return v
    
    @validator('ALLOWED_ORIGINS')
    def validate_cors(cls, v, values):
        """Prevent dangerous CORS in production"""
        if values.get('ENVIRONMENT') == 'production':
            if '*' in v:
                raise ValueError('CORS wildcard (*) not allowed in production!')
        return v
    
    # Database validation
    DATABASE_URL: str
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v, values):
        """Ensure production uses secure database"""
        if values.get('ENVIRONMENT') == 'production':
            if 'sqlite' in v:
                raise ValueError('SQLite not allowed in production!')
            if 'sslmode' not in v:
                raise ValueError('Production database must use SSL!')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Validate on startup
try:
    settings = Settings()
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)
```

---

## 🔄 CI/CD Pipeline: Environment-Specific Deployment

### Development → Staging → Production Flow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  # Public configuration
  PYTHON_VERSION: '3.12'
  NODE_VERSION: '20'

jobs:
  # =====================================================
  # JOB 1: Test with isolated environment
  # =====================================================
  test-backend:
    runs-on: ubuntu-latest
    env:
      # Test environment - no real secrets
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SESSION_SECRET_KEY: test-session-secret-for-ci-only
      SECRET_KEY: test-jwt-secret-for-ci-only
      ALLOWED_ORIGINS: '["http://localhost:3000"]'
      ENVIRONMENT: test
      DEBUG: true
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      
      - name: Security scan
        run: |
          pip install bandit safety
          bandit -r backend/app
          safety check

  # =====================================================
  # JOB 2: Build frontend
  # =====================================================
  build-frontend:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [staging, production]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      
      - name: Set environment variables
        run: |
          if [ "${{ matrix.environment }}" == "staging" ]; then
            echo "VITE_API_URL=https://api-staging.yourproject.com/api" >> $GITHUB_ENV
            echo "VITE_ENV=staging" >> $GITHUB_ENV
          else
            echo "VITE_API_URL=https://api.yourproject.com/api" >> $GITHUB_ENV
            echo "VITE_ENV=production" >> $GITHUB_ENV
          fi
      
      - name: Build
        run: |
          cd frontend
          npm ci
          npm run build -- --mode ${{ matrix.environment }}
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: frontend-${{ matrix.environment }}
          path: frontend/dist

  # =====================================================
  # JOB 3: Deploy to staging (auto)
  # =====================================================
  deploy-staging:
    needs: [test-backend, build-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
      - name: Deploy backend
        env:
          # Secrets from GitHub Secrets
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
          SESSION_SECRET_KEY: ${{ secrets.STAGING_SESSION_SECRET }}
          SECRET_KEY: ${{ secrets.STAGING_JWT_SECRET }}
          ALLOWED_ORIGINS: '["https://staging.yourproject.com"]'
          ENVIRONMENT: staging
        run: |
          # Deploy to staging server
          # Inject env vars from GitHub Secrets
          
      - name: Download frontend artifact
        uses: actions/download-artifact@v4
        with:
          name: frontend-staging
      
      - name: Deploy frontend
        run: |
          # Deploy to CDN/hosting
          
      - name: Run smoke tests
        run: |
          # Test staging deployment
          curl https://api-staging.yourproject.com/health

  # =====================================================
  # JOB 4: Deploy to production (manual approval)
  # =====================================================
  deploy-production:
    needs: [test-backend, build-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: 
      name: production
      url: https://app.yourproject.com
    
    steps:
      - name: Deploy backend
        env:
          # Production secrets from AWS Secrets Manager
          # Retrieved via AWS CLI, not stored in GitHub
          AWS_REGION: ${{ secrets.AWS_REGION }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Retrieve secrets from AWS Secrets Manager
          DATABASE_URL=$(aws secretsmanager get-secret-value \
            --secret-id prod/database-url --query SecretString --output text)
          SESSION_SECRET=$(aws secretsmanager get-secret-value \
            --secret-id prod/session-secret --query SecretString --output text)
          
          # Deploy with retrieved secrets
          # (Secrets never stored in GitHub)
      
      - name: Deploy frontend
        run: |
          # Deploy production frontend
          
      - name: Health check
        run: |
          # Verify production deployment
          curl https://api.yourproject.com/health
```

**Key DevSecOps Points:**
1. ✅ Test environment uses dummy secrets (safe)
2. ✅ Staging uses GitHub Secrets (encrypted)
3. ✅ Production uses AWS Secrets Manager (not GitHub)
4. ✅ Manual approval required for production
5. ✅ Secrets never printed in logs

---

## 🐳 Docker & Containers

### Docker Compose for Local Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ========================================
  # PostgreSQL Database
  # ========================================
  db:
    image: postgres:16-alpine
    environment:
      # Load from .env file
      POSTGRES_USER: ${DB_USER:-user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
      POSTGRES_DB: ${DB_NAME:-app_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-user}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ========================================
  # Backend API
  # ========================================
  backend:
    build: ./backend
    env_file:
      - ./backend/.env  # Load environment variables
    environment:
      # Override specific values for container
      DATABASE_URL: postgresql+asyncpg://${DB_USER:-user}:${DB_PASSWORD:-password}@db:5432/${DB_NAME:-app_db}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app  # Hot reload
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # ========================================
  # Frontend
  # ========================================
  frontend:
    build: 
      context: ./frontend
      args:
        # Pass build-time env vars
        VITE_API_URL: ${VITE_API_URL:-http://localhost:8000/api}
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules  # Prevent overwrite
    environment:
      - VITE_API_URL=http://localhost:8000/api
      - VITE_ENV=development
    command: npm run dev

volumes:
  postgres_data:
```

**Usage:**
```bash
# Create .env for Docker Compose
cat > .env << EOF
DB_USER=user
DB_PASSWORD=dev-password-change-in-prod
DB_NAME=app_db
VITE_API_URL=http://localhost:8000/api
EOF

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all
docker-compose down
```

---

## 📊 Environment Comparison Table

| Aspect | Development | Staging | Production |
|--------|------------|---------|-----------|
| **Backend .env** | Local file | GitHub Secrets | AWS Secrets Manager |
| **Frontend .env** | Local file | Build-time injection | Build-time injection |
| **Database** | SQLite/Local PG | Managed PostgreSQL | Managed PostgreSQL + replica |
| **Session Secret** | Generated once | Rotated monthly | Rotated monthly + incidents |
| **CORS Origins** | localhost:3000,5173 | staging.domain.com | app.domain.com only |
| **DEBUG** | true | false | false |
| **HTTPS** | Optional | Required | Required |
| **Cookie Secure** | false | true | true |
| **Logging** | Console | CloudWatch/DataDog | CloudWatch + Alerts |
| **Secret Rotation** | Manual | Automated monthly | Automated monthly |
| **Backup Secrets** | No | 24h grace period | 24h grace period |

---

## 🎯 Session-Based Auth: Special Considerations

### 1. Session Storage Strategy

```python
# backend/app/core/session.py
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserSession

class SessionManager:
    """Manages session lifecycle with security best practices"""
    
    @staticmethod
    async def create_session(
        db: AsyncSession,
        user_id: int,
        ip_address: str,
        user_agent: str
    ) -> str:
        """
        Create new session with security metadata
        
        DevSecOps: Track IP and user agent for anomaly detection
        """
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(
            minutes=settings.SESSION_EXPIRE_MINUTES
        )
        
        # Store session in database
        session = UserSession(
            session_token=session_token,
            user_id=user_id,
            created_at=datetime.now(),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(session)
        await db.commit()
        
        # Log session creation (audit trail)
        logger.info(f"Session created: user={user_id}, ip={ip_address}")
        
        return session_token
    
    @staticmethod
    async def validate_session(
        db: AsyncSession,
        session_token: str,
        ip_address: str
    ) -> Optional[UserSession]:
        """
        Validate session with security checks
        
        DevSecOps: Detect session hijacking, expired sessions
        """
        result = await db.execute(
            select(UserSession).where(
                UserSession.session_token == session_token
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            logger.warning(f"Invalid session token from {ip_address}")
            return None
        
        # Check expiration
        if session.expires_at < datetime.now():
            logger.info(f"Expired session: user={session.user_id}")
            await db.delete(session)
            await db.commit()
            return None
        
        # Optional: Check IP consistency (anti-hijacking)
        if settings.SESSION_IP_CHECK and session.ip_address != ip_address:
            logger.warning(
                f"IP mismatch: session from {session.ip_address}, "
                f"request from {ip_address}"
            )
            # Optionally invalidate session
            return None
        
        return session
    
    @staticmethod
    async def revoke_session(
        db: AsyncSession,
        session_token: str
    ) -> bool:
        """
        Revoke session immediately
        
        DevSecOps: Instant revocation (advantage over JWT)
        """
        result = await db.execute(
            select(UserSession).where(
                UserSession.session_token == session_token
            )
        )
        session = result.scalar_one_or_none()
        
        if session:
            await db.delete(session)
            await db.commit()
            logger.info(f"Session revoked: user={session.user_id}")
            return True
        
        return False
    
    @staticmethod
    async def cleanup_expired_sessions(db: AsyncSession):
        """
        Periodic cleanup of expired sessions
        
        DevSecOps: Run via scheduled task (cron/celery)
        """
        result = await db.execute(
            select(UserSession).where(
                UserSession.expires_at < datetime.now()
            )
        )
        expired_sessions = result.scalars().all()
        
        for session in expired_sessions:
            await db.delete(session)
        
        await db.commit()
        
        count = len(expired_sessions)
        logger.info(f"Cleaned up {count} expired sessions")
        return count
```

### 2. Environment Variables for Session Security

```bash
# backend/.env - Session-specific configuration

# Session lifecycle
SESSION_EXPIRE_MINUTES=1440              # 24 hours
SESSION_INACTIVITY_TIMEOUT=30            # 30 minutes idle → logout
SESSION_CLEANUP_INTERVAL=3600            # Clean expired every hour

# Session security
SESSION_REGENERATE_ON_LOGIN=true         # Prevent session fixation
SESSION_IP_CHECK=false                   # Check IP consistency (optional)
SESSION_MAX_CONCURRENT=5                 # Max sessions per user

# Cookie security
SESSION_COOKIE_NAME=session_token
SESSION_COOKIE_HTTPONLY=true             # No JavaScript access
SESSION_COOKIE_SECURE=true               # HTTPS only
SESSION_COOKIE_SAMESITE=lax              # CSRF protection
SESSION_COOKIE_DOMAIN=.yourproject.com   # Subdomain sharing

# Database session storage
SESSION_TABLE_NAME=user_sessions
SESSION_INDEX_OPTIMIZATION=true          # Create indexes for performance
```

### 3. Frontend Session Handling (No Secrets!)

```javascript
// frontend/src/services/session.service.js

// All configuration from environment variables (no secrets!)
const API_URL = import.meta.env.VITE_API_URL;
const SESSION_WARNING_TIME = parseInt(
  import.meta.env.VITE_SESSION_TIMEOUT_WARNING || '300000'  // 5 min
);
const AUTO_LOGOUT = import.meta.env.VITE_AUTO_LOGOUT_ON_INACTIVITY === 'true';

class SessionManager {
  constructor() {
    this.activityTimer = null;
    this.warningTimer = null;
  }
  
  /**
   * Track user activity for inactivity timeout
   * DevSecOps: Auto-logout after inactivity
   */
  trackActivity() {
    if (!AUTO_LOGOUT) return;
    
    // Reset inactivity timer
    clearTimeout(this.activityTimer);
    
    this.activityTimer = setTimeout(() => {
      this.handleInactivity();
    }, SESSION_WARNING_TIME);
  }
  
  /**
   * Handle session timeout warning
   * DevSecOps: Give user chance to extend session
   */
  handleInactivity() {
    // Show warning modal
    const shouldExtend = confirm(
      'Your session is about to expire. Continue working?'
    );
    
    if (shouldExtend) {
      // Ping server to extend session
      fetch(`${API_URL}/auth/extend-session`, {
        method: 'POST',
        credentials: 'include'
      });
    } else {
      // Logout
      window.location.href = '/logout';
    }
  }
  
  /**
   * Initialize session monitoring
   */
  init() {
    // Track user activity
    const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];
    events.forEach(event => {
      document.addEventListener(event, () => this.trackActivity());
    });
    
    // Initial activity
    this.trackActivity();
  }
}

export const sessionManager = new SessionManager();
```

**Key Points:**
- Frontend has NO session secrets
- All security happens backend
- Frontend only tracks UI behavior
- Session validation always server-side

---

## 🎓 Practical DevSecOps Checklist

### ✅ Security Checklist

- [ ] **Secrets**: Generated with cryptographic randomness (min 32 bytes)
- [ ] **Git**: `.env` files in `.gitignore` (never committed)
- [ ] **Pre-commit**: Hooks detect secrets before commit
- [ ] **Validation**: Config validated on application startup
- [ ] **Rotation**: Automated secret rotation every 30 days
- [ ] **CORS**: Whitelist specific origins (never `*` in production)
- [ ] **Cookies**: HTTP-only, Secure, SameSite attributes set
- [ ] **Database**: Sessions stored in database (revokable)
- [ ] **Logging**: Session events logged for audit trail
- [ ] **Cleanup**: Expired sessions cleaned up periodically

### ✅ Automation Checklist

- [ ] **Setup**: Scripts auto-generate `.env` from templates
- [ ] **Secrets**: Automated secret generation scripts
- [ ] **Rotation**: CI/CD pipeline rotates secrets monthly
- [ ] **Testing**: Different `.env.test` for CI
- [ ] **Deployment**: Environment-specific builds
- [ ] **Validation**: Pre-deployment config checks
- [ ] **Monitoring**: Alerts for configuration issues

### ✅ CI/CD Checklist

- [ ] **Development**: Local `.env` files (git-ignored)
- [ ] **Testing**: GitHub Actions with test secrets
- [ ] **Staging**: Secrets from GitHub Secrets
- [ ] **Production**: Secrets from AWS/Azure Secrets Manager
- [ ] **Approval**: Manual approval for production
- [ ] **Rollback**: Ability to rollback with previous secrets
- [ ] **Grace Period**: 24h dual-secret support during rotation

### ✅ Reproducibility Checklist

- [ ] **Templates**: `.env.example` files committed
- [ ] **Documentation**: Inline comments explaining each variable
- [ ] **Defaults**: Fallback values in code
- [ ] **Scripts**: Setup automation for new developers
- [ ] **Docker**: `docker-compose.yml` with env injection
- [ ] **CI/CD**: Consistent across all environments

---

## 📚 Summary: Session-Based DevSecOps

### Why Session-Based is Better for DevSecOps:

1. **Simpler Security Model** 🔒
   - Frontend has ZERO secrets (all in backend `.env`)
   - Secrets never exposed to client (HTTP-only cookies)
   - Easier to audit (single source of truth)

2. **Better Control** 🎮
   - Instant revocation (delete session in DB)
   - No "token still valid" problem like JWT
   - Track active sessions per user

3. **Improved Automation** 🤖
   - Only backend needs secret management
   - Frontend build is simpler (no secret injection)
   - Fewer moving parts in CI/CD

4. **Enhanced Monitoring** 📊
   - All sessions visible in database
   - Easy to detect anomalies (IP changes, concurrent logins)
   - Better audit trail

5. **DevSecOps Alignment** ✅
   - Least privilege (frontend knows nothing about auth)
   - Defense in depth (cookie flags + CORS + HTTPS)
   - Zero trust (every request validated server-side)

---

## 🎯 Final Answer to Your Colleague

**"Here's how we handle environment files with session-based auth, aligned with DevSecOps:"**

### Structure:
```
backend/.env → All secrets (SESSION_SECRET_KEY, DATABASE_URL, etc.)
frontend/.env → Zero secrets (just public API URL, feature flags)
```

### Security:
- Backend secrets: Generated with crypto-random (32+ bytes)
- Frontend secrets: None! (HTTP-only cookies handle auth)
- Git: .env files never committed (only .env.example)
- Rotation: Automated monthly via CI/CD

### Automation:
- Setup scripts generate .env from templates
- Pre-commit hooks prevent secret leaks
- Config validation on startup (fail fast)
- CI/CD injects environment-specific values

### CI/CD:
- Development: Local .env files
- Staging: GitHub Secrets
- Production: AWS Secrets Manager (not GitHub)
- Manual approval for production deploys

### Session Benefits:
- Simpler (frontend has zero auth config)
- More secure (secrets never leave server)
- Better control (instant revocation)
- Easier automation (only backend needs secrets)

**This approach is practical, secure, and fully automated - true DevSecOps!** 🚀

---

**Last Updated:** February 12, 2026  
**Maintained By:** DevSecOps Team  
**Session-Based Auth:** Production-Ready ✅

