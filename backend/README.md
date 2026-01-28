# DevSecOps Social Application - Backend

Python backend environment setup for the DevSecOps Social Application project.

## 📋 Project Overview

This is the Python backend environment setup for a social application project following DevSecOps principles.

## 🏗️ Project Structure

```
backend/
├── .venv/                    # Virtual environment (managed by uv)
├── app/                      # Application source code
├── tests/                    # Test suite
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── pyproject.toml            # Project configuration & dependencies
└── uv.lock                   # Exact dependency versions
```

(Note: The Makefile and .devcontainer configuration reside in the project root)

## 🚀 Quick Start

### Option 1: Dev Container (Recommended)
This project is designed to run in a VS Code Dev Container. This ensures you have Python, Node.js, Postgres, and all tools pre-installed.

Open the project root in VS Code.

When prompted, click "Reopen in Container".

Wait for the build to finish. The environment will automatically run make install to set up dependencies.

### Option 2: Manual Setup (Local)
If you prefer running locally, you must have uv installed.

### Install dependencies: (Run from the project root)

```Bash
make install-backend
```

### Create environment file:

```Bash
cd backend
cp .env.example .env
# Edit .env to set your DATABASE_URL and SECRET_KEY
```

## 🧪 Testing
We use pytest via the root Makefile.

### Run tests:

```Bash
make test-backend
```
(Runs pytest with coverage reports automatically)


## 🔒 Security

### Environment Variables
Never commit .env file with real secrets! Use .env.example as template.

### Security Tools
We use Bandit (SAST) and Safety (SCA).

### Run full security scan:

```Bash
make security-backend
```

## 📊 Code Quality
We use Ruff (an ultra-fast replacement for Black, Flake8, and Isort) and Mypy for type checking.

### Format code (Fix style issues):

```Bash
make format-backend
```

### Lint code (Check for errors & types):

````Bash
make lint-backend
```

## 🎯 Development Workflow

1. **Create feature branch** from main
2. **Implement feature** with testsRun tests: make test
3. **Check code quality:** make lint-backend
4. **Security scan:** make security-backend
5. **Commit and push** to feature branch
6. **Create Pull Request** (CI will run these same checks automatically)
7. **Code review** by team
8. **Merge** to main

## 🛠️ Technology Stack

- **Containerization:** Docker Dev Containers (Playwright Base)
- **Dependency Manager:** uv (replaces pip/poetry)
- **Framework:** FastAPI 
- **Server:** Uvicorn
- **Authentication:** PyJWT (Modern replacement for python-jose)
- **Password Hashing:** pwdlib + argon2 (Modern replacement for passlib)
- **Validation:** Pydantic v2
- **Database:** SQLAlchemy (SQLite for dev, PostgreSQL for prod)
- **Testing:** pytest
- **Code Quality:** Ruff (replaces black/flake8/isort) + mypy
- **Security:** bandit, safety

## 📖 Next Steps

1.  ✅ Environment setup completed (Issue #8)
2.  ✅ Modernized stack (uv, ruff, devcontainers)
3.  🔄 Create application structure
4.  🔄 Implement database models
5.  🔄 Implement authentication
6.  🔄 Implement user management
7.  🔄 Implement circles functionality
8.  🔄 Setup CI/CD pipeline
9.  🔄 Add Docker configuration
10. 🔄 Deploy to production

## 🤝 Contributing

1. Follow the development workflow
2. Write tests for new features
3. Use conventional commits
4. Document your code

---

**Created for DevSecOps Course Project**  
*Kultur, Processer och Automation*  
**Task #8**: Setup Python Project Files ✅
