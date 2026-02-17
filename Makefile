# Root Makefile

.PHONY: install install-backend install-frontend seed-database install-playwright test-backend lint-backend migrate-backend format-backend security-backend run-backend run-backend-for-ci clean help

# -- Installation (Handles both stacks) --
install: install-backend install-frontend

install-backend:
	@echo "🚀 Installing Backend dependencies..."
	cd backend && uv sync
	@echo "🔄 Running Backend Migrations..."
	cd backend && uv run alembic upgrade head

install-frontend:
	@echo "🚀 Installing Frontend dependencies..."
	cd frontend && npm install

# -- Testing and Quality Control --
seed-database:
	@echo "🌱 Seeding Backend Database..."
	cd backend && uv run python scripts/create_test_users.py

install-playwright:
	@echo "🎭 Installing Playwright Browsers..."
	cd frontend && npx playwright install --with-deps	

test-backend:
	@echo "🧪 Running Backend Tests..."
	cd backend && uv run pytest

lint-backend:
	@echo "🔍 Running Linters (Ruff + Mypy)..."
	cd backend && uv run ruff check .
	cd backend && uv run mypy .

migrate-backend:
	@echo "🔄 Running Backend Migrations..."
	cd backend && uv run alembic upgrade head

lint-frontend:
	@echo "🔍 Running Linter (eslint)..."
	cd frontend && npm run lint

format-backend:
	@echo "🎨 Formatting Code (Ruff)..."
	cd backend && uv run ruff format .

security-backend:
	@echo "🛡️ Running Security Scans (Bandit + Safety)..."
	cd backend && uv run bandit -c pyproject.toml -r .
	# cd backend && uv run safety scan

test-frontend-unit:
	@echo "🧪 Running Frontend Unit Tests (Vitest)..."
	cd frontend && npm run test:run

test-e2e:
	@echo "🎭 Running E2E Tests..."
	cd frontend && npm run test:e2e

test-e2e-ui:
	@echo "📺 Running Headed Tests (Check Port 6080)..."
	# We manually set DISPLAY to :1 (the default for desktop-lite)
	cd frontend && DISPLAY=:1 LIBGL_ALWAYS_SOFTWARE=1 npm run test:e2e:ui

test-e2e-headed:
	@echo "🎭 Running Headed Tests (Virtual Screen)..."
	# We wrap the npm command inside xvfb-run
	cd frontend && xvfb-run --auto-servernum --server-args="-screen 0 1280x960x24" npm run test:e2e:headed

# -- Execution --
run-backend:
	@echo "🐍 Starting FastAPI Backend..."
	# --host 0.0.0.0 is crucial for Docker/DevContainers so you can access it from Windows	
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-backend-for-ci:
	@echo "🐍 Starting FastAPI Backend for CI..."
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
          
	echo "Waiting for backend to start..."
	sleep 10

run-frontend:
	@echo "⚛️ Starting React Frontend..."
	cd frontend && npm run dev

# -- Environment Setup --
.PHONY: setup-env secrets

setup-env:
	@echo "🔧 Setting up environment files..."
	@if [ ! -f backend/.env ]; then \
		echo "📋 Creating backend/.env from template..."; \
		cp backend/.env.example backend/.env; \
		echo "✅ backend/.env created. Please update with real secrets!"; \
	else \
		echo "✅ backend/.env already exists"; \
	fi
	@if [ ! -f frontend/.env ]; then \
		echo "📋 Creating frontend/.env from template..."; \
		cp frontend/.env.example frontend/.env; \
		echo "✅ frontend/.env created"; \
	else \
		echo "✅ frontend/.env already exists"; \
	fi
	@echo ""
	@echo "🔐 Next: Generate secrets using:"
	@echo "   make secrets"
	@echo "   OR: python3 generate-secrets.py"
	@echo "   OR: bash generate-secrets.sh"

secrets:
	@echo "🔐 Generating secure secrets..."
	@python3 generate-secrets.py

# -- Maintenance --
clean:
	@echo "🧹 Cleaning up artifacts..."
	cd backend && rm -rf .venv .pytest_cache .ruff_cache .mypy_cache __pycache__
	cd frontend && rm -rf node_modules build

help:
	@echo "Available commands:"
	@echo "  make install - Install both backend and frontend dependencies"
	@echo "  make install-backend - Install both backend and frontend dependencies"
	@echo "  make install-frontend - Install both backend and frontend dependencies"
	@echo "  make setup-env - Setup .env files from templates"
	@echo "  make secrets - Generate secure secrets for .env"
	@echo "  make seed-database - Seed the backend database with test data"
	@echo "  make install-playwright - Install Playwright browsers (for E2E tests)"
	@echo "  make test-backend - Run backend tests (pytest)"
	@echo "  make test-frontend-unit - Run frontend tests (Vitest)"
	@echo "  make test-e2e - Run end-to-end tests (Playwright)"
	@echo "  make test-e2e-ui - Run headed end-to-end tests (Playwright with UI via VNC on port localhost:6080)"
	@echo "  make test-e2e-headed - Run headed end-to-end tests (Playwright with virtual screen)"	
	@echo "  make lint-backend - Run backend linters (ruff, mypy)"
	@echo "  make migrate-backend - Run alembic migrations"
	@echo "  make lint-frontend - Run frontend linters (eslint)"
	@echo "  make format-backend - Format backend code (ruff)"
	@echo "  make security-backend - Run security scans (bandit, safety)"
	@echo "  make run-backend - Start FastAPI server (accessible outside container)"
	@echo "  make run-backend-for-ci - Start FastAPI server for CI (runs in background)"
	@echo "  make run-frontend - Start React dev server"
	@echo "  make clean - Remove artifacts and virtual environments"