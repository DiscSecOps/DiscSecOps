# DevSecOps Social Application - Backend

Python backend environment setup for the DevSecOps Social Application project.

## 📋 Project Overview

This is the Python backend environment setup for a social application project following DevSecOps principles.

## 🏗️ Project Structure

```
backend/
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── pyproject.toml            # Python project configuration
└── setup.ps1                 # Quick setup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

**Option 1: Quick Setup (Recommended)**
```powershell
.\setup.ps1
```

**Option 2: Manual Setup**

1. **Create virtual environment:**
```powershell
python -m venv venv
```

2. **Activate virtual environment:**
```powershell
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Create environment file:**
```powershell
copy .env.example .env
# Edit .env and update SECRET_KEY and other settings
```

## 🧪 Testing

**Run tests (when implemented):**
```powershell
pytest
```

**Run tests with coverage:**
```powershell
pytest --cov=app --cov-report=html
```

## 🔒 Security

### Environment Variables
Never commit `.env` file with real secrets! Use `.env.example` as template.

### Security Tools (Development):
```powershell
# Check for security vulnerabilities in dependencies
safety check

# Scan code for security issues (when code is added)
bandit -r app/
```

## 📊 Code Quality

**Format code (when implemented):**
```powershell
black app/ tests/
```

**Sort imports:**
```powershell
isort app/ tests/
```

**Lint code:**
```powershell
flake8 app/ tests/
```

**Type checking:**
```powershell
mypy app/
```

## 🎯 Development Workflow

1. **Create feature branch** from main
2. **Implement feature** with tests
3. **Run tests locally**: `pytest`
4. **Check code quality**: `black`, `flake8`, `mypy`
5. **Security scan**: `bandit`, `safety`
6. **Commit and push** to feature branch
7. **Create Pull Request**
8. **Code review** by team
9. **Merge** to main

## 🛠️ Technology Stack

- **Framework:** FastAPI (to be implemented)
- **Server:** Uvicorn
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib + bcrypt
- **Validation:** Pydantic
- **Database:** SQLAlchemy (SQLite for dev, PostgreSQL for prod)
- **Testing:** pytest
- **Code Quality:** black, flake8, mypy, isort
- **Security:** bandit, safety

## 📖 Next Steps

1. ✅ Environment setup completed (Issue #8)
2. 🔄 Create application structure
3. 🔄 Implement database models
4. 🔄 Implement authentication
5. 🔄 Implement user management
6. 🔄 Implement circles functionality
7. 🔄 Setup CI/CD pipeline
8. 🔄 Add Docker configuration
9. 🔄 Deploy to production

## 🤝 Contributing

1. Follow the development workflow
2. Write tests for new features
3. Use conventional commits
4. Document your code

---

**Created for DevSecOps Course Project**  
*Kultur, Processer och Automation*  
**Task #8**: Setup Python Project Files ✅
