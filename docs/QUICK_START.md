# Environment Configuration - Quick Start Guide

**For Linux Dev Container / Mac / Linux Users**

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Setup Environment Files

```bash
# Option A: Using Makefile (recommended)
make setup-env

# Option B: Manual setup
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Step 2: Generate Secure Secrets

```bash
# Option A: Using Python (cross-platform)
python3 generate-secrets.py

# Option B: Using Bash script
bash generate-secrets.sh

# Option C: Using Makefile
make secrets

# Option D: Using OpenSSL directly
openssl rand -base64 32
```

Copy the generated secrets and paste them into `backend/.env`:
```bash
SECRET_KEY=<generated-secret>
SESSION_SECRET_KEY=<generated-secret>
```

### Step 3: Install Dependencies & Run

```bash
# Install dependencies
make install

# Start backend (in one terminal)
make run-backend

# Start frontend (in another terminal)
make run-frontend
```

---

## 📁 Available Scripts

### For Linux/Mac/Dev Container:

| Script | Purpose | Command |
|--------|---------|---------|
| `generate-secrets.py` | Generate secrets (Python) | `python3 generate-secrets.py` |
| `generate-secrets.sh` | Generate secrets (Bash) | `bash generate-secrets.sh` |
| `frontend/setup-env.sh` | Setup frontend env | `cd frontend && bash setup-env.sh` |

### For Windows:

| Script | Purpose | Command |
|--------|---------|---------|
| `generate-secrets.ps1` | Generate secrets (PowerShell) | `.\generate-secrets.ps1` |
| `frontend/setup-env.ps1` | Setup frontend env | `cd frontend; .\setup-env.ps1` |

---

## 🐳 Dev Container Notes

The project uses a **Linux Dev Container**, so:

✅ **Use these scripts:**
- `generate-secrets.py` (Python - works everywhere)
- `generate-secrets.sh` (Bash - Linux/Mac)
- `frontend/setup-env.sh` (Bash - Linux/Mac)
- Makefile targets (`make setup-env`, `make secrets`)

❌ **Don't use these:**
- `generate-secrets.ps1` (PowerShell - Windows only)
- `frontend/setup-env.ps1` (PowerShell - Windows only)

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/app_db

# Security - GENERATE THESE!
SECRET_KEY=<run generate-secrets.py>
SESSION_SECRET_KEY=<run generate-secrets.py>

# API Configuration
PROJECT_NAME="DevSecOps Social App"
VERSION=0.1.0
API_V1_STR=/api/v1

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### Frontend (`frontend/.env`)

```bash
# API Connection (must include /api/v1 to match backend versioning)
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_API_URL=http://localhost:8000/api/v1

# Feature Flags
VITE_ENABLE_SOCIAL_FEATURES=true
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false
```

---

## 🔧 Troubleshooting

### Problem: PowerShell scripts don't work in Dev Container

**Solution:** Use Python or Bash alternatives:
```bash
# Instead of: .\generate-secrets.ps1
python3 generate-secrets.py

# Instead of: cd frontend; .\setup-env.ps1
cd frontend && bash setup-env.sh
```

### Problem: Permission denied

**Solution:** Make scripts executable:
```bash
chmod +x generate-secrets.sh
chmod +x generate-secrets.py
chmod +x frontend/setup-env.sh
```

### Problem: OpenSSL not found

**Solution:** Use Python alternative:
```bash
python3 generate-secrets.py
```

---

## 📚 Full Documentation

For complete details, see:
- `TEAM_IMPLEMENTATION_REPORT.md` - Complete setup guide with testing
- `ENVIRONMENT_SETUP_GUIDE.md` - DevSecOps best practices
- `DEVSECOPS_SESSION_AUTH_GUIDE.md` - Session authentication guide

---

## ✅ Quick Verification

After setup, verify everything works:

```bash
# 1. Check backend config loads
cd backend
python3 -c "from app.core.config import settings; print(f'✅ {settings.PROJECT_NAME}')"

# 2. Check frontend .env exists
ls -la frontend/.env

# 3. Start services
make run-backend  # Terminal 1
make run-frontend # Terminal 2
```

**Expected:** Both services start without errors!

---

**Last Updated:** February 13, 2026  
**Platform:** Linux Dev Container / Cross-platform  
**Status:** ✅ Tested and working
