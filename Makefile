# ============================================================================
# ROOT MAKEFILE - Full Stack Project (FastAPI + React)
# ============================================================================
# This Makefile manages both backend (Python/FastAPI) and frontend (React/TypeScript)
# from a single location.
#
# Project structure:
# ├── backend/         # FastAPI + Python
# ├── frontend/        # React + JavaScript  
# ├── Makefile         # THIS FILE
# └── generate-secrets.py
# ============================================================================

# ============================================================================
# CONFIGURATION
# ============================================================================
# Default ports
BACKEND_PORT = 8000
FRONTEND_PORT = 3000

-include ./backend/.env
export

# ============================================================================
# INSTALLATION
# ============================================================================
.PHONY: install install-backend install-frontend

install: install-backend install-frontend
	@echo "✅ All dependencies installed!"

install-backend:
	@echo "🐍 Installing Backend..."
	cd backend && uv sync
	cd backend && uv run alembic upgrade head
	@echo "✅ Backend ready!"

install-frontend:
	@echo "⚛️ Installing Frontend..."
	cd frontend && npm install
	@echo "✅ Frontend ready!"

# ============================================================================
# DATABASE (Development)
# ============================================================================
.PHONY: migrate-backend seed-database db-reset db-refresh

migrate-backend:
	@echo "🔄 Running migrations..."
	cd backend && uv run alembic upgrade head

seed-database:
	@echo "🌱 Seeding database..."
	cd backend && uv run python scripts/create_test_users.py

db-reset:
	@echo "⚠️  Resetting database..."
	cd backend && uv run python scripts/reset_db.py

db-refresh: db-reset migrate-backend seed-database
	@echo "🔄 Database refresh complete"

# ============================================================================
# BACKEND TESTS
# ============================================================================
.PHONY: test-backend-unit test-backend-integration test-backend-all
.PHONY: lint-backend lint-backend-fix format-backend security-backend

test-backend-unit:
	@echo "🧪 Backend Unit Tests..."
	cd backend && uv run pytest tests/unit/ -v
	@echo "✅ Unit tests passed"

test-backend-integration:
	@echo "🔗 Backend Integration Tests..."
	cd backend && uv run pytest tests/integration/ -v
	@echo "✅ Integration tests passed"

test-backend-all: test-backend-unit test-backend-integration
	@echo "✅ All backend tests passed"

lint-backend:
	@echo "🔍 Linting backend..."
	cd backend && uv run ruff check .
	cd backend && uv run mypy .
	@echo "✅ Linting complete"

lint-backend-fix:
	@echo "🔧 Fixing backend linting..."
	cd backend && uv run ruff check --fix .
	cd backend && uv run ruff format .
	@echo "✅ Fixing complete"

format-backend:
	@echo "🎨 Formatting backend..."
	cd backend && uv run ruff format .
	@echo "✅ Formatting complete"

security-backend:
	@echo "🛡️ Scanning backend security..."
	cd backend && uv run bandit -c pyproject.toml -r .
	@echo "✅ Security scan complete"

# ============================================================================
# FRONTEND TESTS
# ============================================================================
.PHONY: test-frontend-unit test-frontend-integration test-frontend-all
.PHONY: test-frontend-watch test-frontend-coverage
.PHONY: lint-frontend lint-frontend-fix audit-frontend

test-frontend-unit:
	@echo "🧪 Frontend Unit Tests..."
	cd frontend && npm run test:unit
	@echo "✅ Unit tests passed"

test-frontend-integration:
	@echo "🔗 Frontend Integration Tests..."
	cd frontend && npm run test:integration
	@echo "✅ Integration tests passed"

test-frontend-all:
	@echo "🧪 Frontend All Tests..."
	cd frontend && npm run test:run
	@echo "✅ All tests passed"

test-frontend-watch:
	@echo "👀 Frontend Watch Mode..."
	cd frontend && npm run test:watch

test-frontend-coverage:
	@echo "📊 Frontend Coverage..."
	cd frontend && npm run test:coverage

lint-frontend:
	@echo "🔍 Linting frontend..."
	cd frontend && npm run lint
	@echo "✅ Linting complete"

lint-frontend-fix:
	@echo "🔧 Fixing frontend linting..."
	cd frontend && npm run lint -- --fix
	@echo "✅ Fixing complete"

audit-frontend:
	@echo "🛡️ Auditing frontend dependencies..."
	cd frontend && npm audit --audit-level=high || true
	@echo "✅ Audit complete"

# ============================================================================
# E2E TESTS (Playwright)
# ============================================================================
.PHONY: install-playwright test-e2e test-e2e-headed

install-playwright:
	@echo "🎭 Installing Playwright..."
	cd backend && uv run python -m playwright install --with-deps chromium
	@echo "✅ Playwright installed"

## End-to-End Testing (Playwright)
# Note: E2E tests are in backend/ because they use Python + Playwright bindings
test-e2e: ## Run E2E tests in headless mode (for CI)
	@echo "🎭 Running E2E Tests..."
	cd backend && uv run pytest tests/e2e/step_test/ -v
	@echo "✅ E2E tests complete"

test-e2e-headed: ## Run E2E tests with visible browser (for local debugging)
	@echo "🎭 Running Headed E2E Tests..."
	cd backend && uv run pytest tests/e2e/step_test/ --headed --slowmo 500 -v
	@echo "✅ Headed E2E tests complete"
# ============================================================================
# RUN SERVERS
# ============================================================================
.PHONY: run-backend run-frontend

run-backend:
	@echo "🐍 Starting Backend (port $(BACKEND_PORT))..."
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

run-frontend:
	@echo "⚛️ Starting Frontend (port $(FRONTEND_PORT))..."
	cd frontend && npm run dev

# ============================================================================
# UTILITIES
# ============================================================================
.PHONY: clean help

clean:
	@echo "🧹 Cleaning up..."
	cd backend && rm -rf .venv .pytest_cache .ruff_cache .mypy_cache __pycache__ .coverage htmlcov
	cd frontend && rm -rf node_modules build dist node_modules/.cache node_modules/.vitest .vitest
	@echo "✅ Cleanup complete"

help:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║     🚀 AVAILABLE COMMANDS                                    ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 INSTALLATION: install install-backend install-frontend"
	@echo ""
	@echo "🗄️  DATABASE: migrate-backend seed-database db-reset db-refresh"
	@echo ""
	@echo "🧪 BACKEND TESTS: test-backend-unit test-backend-integration test-backend-all"
	@echo "🔍 BACKEND LINT: lint-backend lint-backend-fix format-backend security-backend"
	@echo ""
	@echo "⚛️ FRONTEND TESTS: test-frontend-unit test-frontend-integration test-frontend-all"
	@echo "🔍 FRONTEND LINT: lint-frontend lint-frontend-fix audit-frontend"
	@echo "👀 FRONTEND WATCH: test-frontend-watch test-frontend-coverage"
	@echo ""
	@echo "🎭 E2E TESTS: install-playwright test-e2e test-e2e-headed"
	@echo ""
	@echo "🚀 RUN: run-backend run-frontend"
	@echo ""
	@echo "🧹 CLEAN: clean"