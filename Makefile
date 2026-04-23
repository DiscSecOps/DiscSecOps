# ============================================================================
# ROOT MAKEFILE - Full Stack Project (FastAPI + React)
# ============================================================================
# This Makefile manages both backend (Python/FastAPI) and frontend (React/JavaScript)
# from a single location.
#
# Project structure:
# ├── backend/		 # FastAPI + Python
# ├── frontend/		# React + JavaScript  
# ├── Makefile		 # THIS FILE
# └── generate-secrets.py
# ============================================================================

# ============================================================================
# CONFIGURATION
# ============================================================================
BACKEND_PORT = 8000
FRONTEND_PORT = 3000

-include ./backend/.env
export
# ============================================================================
# INSTALLATION COMMANDS
# ============================================================================
.PHONY: install install-backend install-frontend install-playwright install-playwright-deps-only

install: install-backend install-frontend
	@echo "✅ All dependencies installed successfully!"

install-backend:
	@echo "🐍 Installing Backend dependencies..."
	cd backend && uv sync
	@echo "🔄 Running database migrations..."
	cd backend && uv run alembic upgrade head
	@echo "✅ Backend ready!"

install-frontend:
	@echo "⚛️ Installing Frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend ready!"

install-playwright:
	@echo "🎭 Installing Playwright Browsers..."
	cd backend && uv run python -m playwright install --with-deps chromium
	@echo "✅ Playwright installed"

install-playwright-deps-only:
	@echo "🎭 Installing Playwright System Dependencies..."
	cd backend && uv run python -m playwright install-deps chromium
	@echo "✅ Playwright dependencies installed"

# ============================================================================
# DATABASE COMMANDS
# ============================================================================
.PHONY: migrate-backend seed-database db-reset db-refresh

migrate-backend:
	@echo "🔄 Running migrations..."
	cd backend && uv run alembic upgrade head

seed-database:
	@echo "🌱 Seeding database..."
	cd backend && uv run python scripts/create_test_users.py
	@echo "✅ Test data added"

db-reset:
	@echo "⚠️  Resetting database..."
	cd backend && uv run python scripts/reset_db.py
	@echo "✅ Database reset complete"

db-refresh: db-reset migrate-backend seed-database
	@echo "🔄 Database refresh complete"

# ============================================================================
# TESTING & QUALITY CONTROL
# ============================================================================
.PHONY: test-backend lint-backend security-backend format-backend
.PHONY: test-frontend-unit lint-frontend audit-frontend
.PHONY: test-e2e test-e2e-headed

test-backend:
	@echo "🧪 Running Backend Tests..."
	cd backend && uv run pytest tests/unit/ -v
	cd backend && uv run pytest tests/integration/ -v
	@echo "✅ Backend tests passed"

lint-backend:
	@echo "🔍 Linting backend..."
	cd backend && uv run ruff check . --fix
	cd backend && uv run mypy .
	@echo "✅ Backend linting complete"

security-backend:
	@echo "🛡️ Scanning backend security..."
	cd backend && uv run bandit -c pyproject.toml -r .
	@echo "✅ Backend security scan complete"

format-backend:
	@echo "🎨 Formatting backend code..."
	cd backend && uv run ruff format .
	@echo "✅ Backend formatting complete"

test-frontend-unit:
	@echo "🧪 Running Frontend Unit Tests..."
	cd frontend && npm run test:run
	@echo "✅ Frontend unit tests passed"

lint-frontend:
	@echo "🔍 Linting frontend..."
	cd frontend && npm run lint
	@echo "✅ Frontend linting complete"

audit-frontend:
	@echo "🛡️ Auditing frontend dependencies..."
	cd frontend && npm audit --omit=dev --audit-level=high
	@echo "✅ Frontend audit complete"

test-e2e:
	@echo "🎭 Running E2E Tests..."
	cd backend && uv run pytest tests/e2e/step_defs/ -v
	@echo "✅ E2E tests complete"

test-e2e-headed:
	@echo "🎭 Running Headed E2E Tests..."
	cd backend && DISPLAY=:1 uv run pytest tests/e2e/step_defs --headed --slowmo 1500 -v
	@echo "✅ Headed E2E tests complete"

# ============================================================================
# APPLICATION EXECUTION
# ============================================================================
.PHONY: run-backend run-backend-for-ci run-test-backend run-frontend run-playwright-codegen

run-backend:
	@echo "🐍 Starting Backend on port $(BACKEND_PORT)..."
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

run-backend-for-ci:
	@echo "🐍 Starting Backend for CI..."
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port $(BACKEND_PORT) &
	@echo "⏳ Waiting for backend to start..."
	sleep 10
	@echo "✅ Backend running on port $(BACKEND_PORT)"

run-test-backend:
	@echo "🐍 Starting Backend with TEST database..."
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port $(BACKEND_PORT)

run-frontend:
	@echo "⚛️ Starting Frontend on port $(FRONTEND_PORT)..."
	cd frontend && npm run dev

run-playwright-codegen:
	@echo "🎬 Starting Playwright Code Generator..."
	@echo "📌 Make sure frontend is running on port $(FRONTEND_PORT)"
	cd backend && uv run playwright codegen http://localhost:$(FRONTEND_PORT)

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
.PHONY: setup-env secrets

setup-env:
	@echo "🔧 Setting up environment files..."
	@if [ ! -f backend/.env ]; then \
		echo "📋 Creating backend/.env from template..."; \
		cp backend/.env.example backend/.env; \
		echo "✅ backend/.env created. Update with real secrets!"; \
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
	@echo "🔐 Next step: Generate secure secrets with:"
	@echo "   make secrets"

secrets:
	@echo "🔐 Generating secure secrets..."
	@python3 generate-secrets.py
	@echo "✅ Secrets generated. Check your .env files!"

# ============================================================================
# MAINTENANCE
# ============================================================================
.PHONY: sync

sync: ## Sync backend & frontend dependencies after pulling changes
	@echo "🔄 Syncing backend dependencies..."
	cd backend && uv sync
	@echo "🔄 Syncing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies are now in sync!"
# ----------------------------------------------------------------------------
# Cleanup and utility commands
# ----------------------------------------------------------------------------

.PHONY: clean help

clean:
	@echo "🧹 Cleaning up..."
	cd backend && rm -rf .venv .pytest_cache .ruff_cache .mypy_cache __pycache__
	cd frontend && rm -rf node_modules build dist
	@echo "✅ Cleanup complete"

help:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║	 🚀 AVAILABLE COMMANDS - Full Stack Project			   ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 INSTALLATION:"
	@grep -h -E '^install[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🗄️  DATABASE:"
	@grep -h -E '^(db|migrate|seed)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🧪 TESTING & QUALITY:"
	@grep -h -E '^(test|lint|security|format|audit)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🚀 RUN APPLICATION:"
	@grep -h -E '^run[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🔧 ENVIRONMENT:"
	@grep -h -E '^(setup|secrets)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@grep -h -E '^(clean|help)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-25s\033[0m %s\n", $$1, $$2}'
