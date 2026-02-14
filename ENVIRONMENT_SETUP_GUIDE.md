# Environment Configuration Guide - DevSecOps Best Practices

**Project:** DevSecOps Full Stack Application  
**Date:** February 12, 2026  
**Purpose:** Secure and efficient environment variable management

---

## 📋 Table of Contents
1. [Current Project Structure](#current-project-structure)
2. [DevSecOps Best Practices](#devsecops-best-practices)
3. [Backend Environment Setup](#backend-environment-setup)
4. [Frontend Environment Setup](#frontend-environment-setup)
5. [Security Guidelines](#security-guidelines)
6. [Different Environments](#different-environments)
7. [CI/CD Integration](#cicd-integration)

---

## 🏗️ Current Project Structure

```
DevSecOps-Project/
├── .env                          ❌ NEVER CREATE (security risk)
├── .gitignore                    ✅ Already configured
├── backend/
│   ├── .env                      ✅ Local development (git-ignored)
│   ├── .env.example              ✅ Template (committed to git)
│   └── app/
│       └── core/
│           └── config.py         ✅ Configuration loader
├── frontend/
│   ├── .env                      ⚠️ CREATE THIS (git-ignored)
│   ├── .env.example              ⚠️ CREATE THIS (committed to git)
│   ├── .env.development          ⚠️ OPTIONAL (git-ignored)
│   ├── .env.production           ⚠️ OPTIONAL (git-ignored)
│   └── vite.config.js            ✅ Already configured
└── docker-compose.yml            ✅ For container environments
```

---

## 🔒 DevSecOps Best Practices

### ✅ DO's:
1. **Separate .env files per service** (backend/, frontend/)
2. **Use .env.example templates** (committed to git)
3. **Never commit real .env files** (.gitignore configured)
4. **Use different values per environment** (dev, staging, prod)
5. **Rotate secrets regularly** (especially API keys)
6. **Use environment-specific naming** (.env.development, .env.production)
7. **Document all variables** (in .env.example)
8. **Use secrets management tools** (for production)

### ❌ DON'T's:
1. **Never put .env in root** (confusing, security risk)
2. **Never commit secrets** (API keys, passwords, tokens)
3. **Never use production secrets locally**
4. **Don't share .env files via chat/email**
5. **Don't hardcode secrets in code**
6. **Don't use same secrets across environments**

---

## 🐍 Backend Environment Setup

### Location: `backend/.env`

**Already configured!** Your backend has:
- ✅ `.env` file (git-ignored)
- ✅ `.env.example` template
- ✅ Configuration loader in `app/core/config.py`

### Current Backend .env Structure:

```bash
# backend/.env (Local Development)

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./test.db
# For PostgreSQL: DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/app_db

# Security - JWT Settings
SECRET_KEY=dev-secret-key-change-in-production-12345678901234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Security - Session Settings
SESSION_SECRET_KEY=dev-session-secret-change-in-production-12345678901234567890
SESSION_EXPIRE_MINUTES=1440

# CORS - Frontend URLs
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:4173"]

# API Configuration
API_PORT=8000
API_V1_STR=/api/v1

# Environment
ENVIRONMENT=development
DEBUG=true
```

### Backend Environment Variables Explained:

| Variable | Purpose | DevSecOps Note |
|----------|---------|----------------|
| `DATABASE_URL` | Database connection string | Use different DBs per environment |
| `SECRET_KEY` | JWT token signing | Rotate regularly, min 32 chars |
| `SESSION_SECRET_KEY` | Session cookie signing | Different from JWT secret |
| `ALLOWED_ORIGINS` | CORS configuration | Restrict to known frontend URLs |
| `DEBUG` | Debug mode | Must be `false` in production |

---

## ⚛️ Frontend Environment Setup

### Location: `frontend/.env`

**⚠️ NEEDS TO BE CREATED!** Your frontend currently uses hardcoded URLs.

### Step 1: Create Frontend .env.example

```bash
# frontend/.env.example
# Copy this file to .env and update values for your environment

# API Configuration
VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000

# Environment
VITE_ENV=development

# Feature Flags
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false

# Optional: External Services (if needed)
# VITE_GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X
# VITE_SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

### Step 2: Create Frontend .env (Local Development)

```bash
# frontend/.env
# Local development environment

VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000
VITE_ENV=development
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false
```

### Step 3: Update Frontend Code to Use Environment Variables

**Current:** `frontend/src/services/auth.service.js`
```javascript
// ❌ Hardcoded - NOT DevSecOps compliant
const API_URL = 'http://localhost:8000/api';
```

**Updated:** (DevSecOps compliant)
```javascript
// ✅ Using environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Optional: Add timeout from env
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 10000;
```

### Step 4: Create Environment-Specific Files (Optional but Recommended)

```bash
# frontend/.env.development
VITE_API_URL=http://localhost:8000/api
VITE_ENV=development
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false

# frontend/.env.staging
VITE_API_URL=https://api-staging.yourproject.com/api
VITE_ENV=staging
VITE_ENABLE_DEBUG=false
VITE_ENABLE_ANALYTICS=true

# frontend/.env.production
VITE_API_URL=https://api.yourproject.com/api
VITE_ENV=production
VITE_ENABLE_DEBUG=false
VITE_ENABLE_ANALYTICS=true
```

### Important: Vite Environment Variable Rules

1. **Prefix Required:** All variables MUST start with `VITE_`
2. **Build Time:** Variables are embedded at build time (not runtime)
3. **Public Exposure:** All `VITE_` variables are exposed to client (no secrets!)
4. **Access:** Use `import.meta.env.VITE_YOUR_VAR`

---

## 🔐 Security Guidelines

### 1. **Secret Classification**

| Type | Location | Example | Git Tracked? |
|------|----------|---------|--------------|
| **Public Config** | Frontend .env | API URL, Feature flags | ❌ No (but safe if committed) |
| **Backend Secrets** | Backend .env | DB password, JWT secret | ❌ NEVER |
| **Templates** | .env.example | Placeholder values | ✅ Yes |
| **Production Secrets** | Secret Manager | Real credentials | ❌ NEVER |

### 2. **Secret Strength Requirements**

```bash
# ❌ WEAK - Never use these
SECRET_KEY=secret123
SESSION_SECRET_KEY=mysecret

# ✅ STRONG - Use cryptographically secure random strings
SECRET_KEY=a8f5f167f44f4964e6c998dee827110c1a9b4b3f1e2d5c6b7a8e9f0d1c2b3a4e5f6
SESSION_SECRET_KEY=7b2c9e1f6d4a8b3c5e7f9a1d3c5e7b9f1a3c5e7d9b1f3a5c7e9b1d3f5a7c9e1b3d5

# Generate secure secrets:
# Python: python -c "import secrets; print(secrets.token_hex(32))"
# PowerShell: [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
# OpenSSL: openssl rand -hex 32
```

### 3. **CORS Configuration**

```bash
# ❌ NEVER in production
ALLOWED_ORIGINS=["*"]

# ✅ Development (specific ports)
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# ✅ Production (specific domains)
ALLOWED_ORIGINS=["https://app.yourproject.com","https://www.yourproject.com"]
```

### 4. **Git Configuration**

Ensure `.gitignore` has:
```gitignore
# Environment variables
.env
.env.*
!.env.example

# Backup files (people sometimes create these)
.env.backup
.env.old
*.env.bak
```

---

## 🌍 Different Environments

### Development Environment

**Backend:** `backend/.env`
```bash
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev-secret-key-only
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

**Frontend:** `frontend/.env.development`
```bash
VITE_API_URL=http://localhost:8000/api
VITE_ENV=development
VITE_ENABLE_DEBUG=true
```

---

### Staging Environment

**Backend:** Environment variables set in hosting platform (Heroku, AWS, Azure)
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@staging-db.region.provider.com/dbname
SECRET_KEY=<generated-staging-secret>
DEBUG=false
ALLOWED_ORIGINS=["https://staging.yourproject.com"]
ENVIRONMENT=staging
```

**Frontend:** `frontend/.env.staging`
```bash
VITE_API_URL=https://api-staging.yourproject.com/api
VITE_ENV=staging
VITE_ENABLE_DEBUG=false
VITE_ENABLE_ANALYTICS=true
```

**Build Command:**
```bash
npm run build -- --mode staging
```

---

### Production Environment

**Backend:** Secrets stored in secret manager (AWS Secrets Manager, Azure Key Vault, etc.)
```bash
DATABASE_URL=<from-secret-manager>
SECRET_KEY=<from-secret-manager>
SESSION_SECRET_KEY=<from-secret-manager>
DEBUG=false
ALLOWED_ORIGINS=["https://app.yourproject.com"]
ENVIRONMENT=production
```

**Frontend:** `frontend/.env.production`
```bash
VITE_API_URL=https://api.yourproject.com/api
VITE_ENV=production
VITE_ENABLE_DEBUG=false
VITE_ENABLE_ANALYTICS=true
```

**Build Command:**
```bash
npm run build -- --mode production
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

env:
  # Public configuration (safe to commit)
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.12'

jobs:
  test-backend:
    runs-on: ubuntu-latest
    env:
      # Test environment variables
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: test-secret-key-for-ci-only
      DEBUG: true
      
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
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
          pytest

  test-frontend:
    runs-on: ubuntu-latest
    env:
      VITE_API_URL: http://localhost:8000/api
      VITE_ENV: test
      
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          
      - name: Install dependencies
        run: |
          cd frontend
          npm install
          
      - name: Run tests
        run: |
          cd frontend
          npm test

  deploy-production:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy Backend
        env:
          # Secrets from GitHub Secrets
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
          SECRET_KEY: ${{ secrets.PROD_SECRET_KEY }}
          SESSION_SECRET_KEY: ${{ secrets.PROD_SESSION_SECRET }}
        run: |
          # Deploy backend with secrets from GitHub Secrets
          
      - name: Build & Deploy Frontend
        env:
          VITE_API_URL: https://api.yourproject.com/api
          VITE_ENV: production
        run: |
          cd frontend
          npm run build
          # Deploy build files
```

---

## 📝 Quick Setup Checklist

### For Your Team:

#### Backend Developer:
- [x] ✅ `backend/.env` exists (already done)
- [x] ✅ `backend/.env.example` exists (already done)
- [x] ✅ `.gitignore` configured (already done)
- [ ] ⚠️ Verify secrets are strong (check and regenerate if weak)
- [ ] ⚠️ Document all variables in .env.example

#### Frontend Developer:
- [ ] ⚠️ Create `frontend/.env.example` (use template above)
- [ ] ⚠️ Create `frontend/.env` for local development
- [ ] ⚠️ Update `auth.service.js` to use `import.meta.env.VITE_API_URL`
- [ ] ⚠️ Update `userDashboard.service.js` to use env variables
- [ ] ⚠️ Test with different API URLs

#### DevOps/Team Lead:
- [ ] ⚠️ Set up secrets in GitHub Secrets
- [ ] ⚠️ Configure environment variables in hosting platform
- [ ] ⚠️ Create staging environment
- [ ] ⚠️ Set up secret rotation policy
- [ ] ⚠️ Update CI/CD pipeline with proper env vars

---

## 🛠️ Implementation Steps for Your Team

### Step 1: Create Frontend .env Files (10 minutes)

```powershell
# In project root
cd frontend

# Create .env.example
@"
# Frontend Environment Variables
# Copy this to .env and update values

VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000
VITE_ENV=development
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false
"@ | Out-File -FilePath .env.example -Encoding utf8

# Create .env for local development
Copy-Item .env.example .env
```

### Step 2: Update Frontend Services (15 minutes)

**File:** `frontend/src/services/auth.service.js`

```javascript
// Add at the top of the file
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000;

// Update axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  withCredentials: true
});
```

### Step 3: Update Backend Secrets (5 minutes)

```powershell
cd backend

# Generate new strong secret
$secret = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
Write-Host "New SECRET_KEY: $secret"

# Update backend/.env with new secret
```

### Step 4: Test Everything (10 minutes)

```powershell
# Terminal 1: Start backend
cd backend
.\start_server.ps1

# Terminal 2: Start frontend
cd frontend
npm run dev

# Verify:
# 1. Frontend loads at http://localhost:3000 or 5173
# 2. Can register new user
# 3. Can login
# 4. Check browser console for API URL
```

### Step 5: Document for Team (5 minutes)

Update your `README.md`:
```markdown
## Environment Setup

### Backend
1. Copy `backend/.env.example` to `backend/.env`
2. Update database URL if using PostgreSQL
3. Generate strong secrets for production

### Frontend
1. Copy `frontend/.env.example` to `frontend/.env`
2. Update `VITE_API_URL` if backend runs on different port
3. Set `VITE_ENV` to 'development'
```

---

## 🎯 Summary: Why This Approach?

### DevSecOps Benefits:

1. **Security** 🔒
   - Secrets never committed to git
   - Different secrets per environment
   - Easy to rotate credentials

2. **Flexibility** 🔄
   - Easy to switch between environments
   - Team members can have different local configs
   - CI/CD can inject environment-specific values

3. **Maintainability** 🛠️
   - Clear documentation via .env.example
   - Easy onboarding for new team members
   - Centralized configuration

4. **Compliance** ✅
   - Follows security best practices
   - Audit trail in secret managers
   - Separation of concerns

5. **Scalability** 📈
   - Easy to add new environments
   - Works with any hosting platform
   - Compatible with Docker/Kubernetes

---

## 📚 Additional Resources

- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [FastAPI Settings Management](https://fastapi.tiangolo.com/advanced/settings/)
- [12-Factor App: Config](https://12factor.net/config)
- [OWASP: Secure Configuration](https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration)

---

## ❓ FAQ

**Q: Why not use a single .env in the root?**  
A: Separation of concerns. Backend and frontend have different needs, dependencies, and deployment processes.

**Q: Can I commit .env to a private repository?**  
A: No! Even private repos can be compromised. Use .env.example instead.

**Q: How do I share .env values with my team?**  
A: Share .env.example (committed to git) and communicate secrets via secure channels (password manager, encrypted chat).

**Q: What if I accidentally commit .env?**  
A: 
1. Remove it from git history: `git filter-branch` or `git-filter-repo`
2. Rotate ALL secrets immediately
3. Update .gitignore

**Q: How often should we rotate secrets?**  
A: 
- Development: Every 90 days
- Production: Every 30-60 days
- After team member leaves: Immediately
- After security incident: Immediately

---

**Last Updated:** February 12, 2026  
**Maintained By:** DevSecOps Team  
**Questions?** Ask in team chat or create an issue

