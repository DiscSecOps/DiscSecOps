# Root Makefile

.PHONY: install install-backend install-frontend test-backend lint-backend format-backend security-backend run-backend run-frontend clean help

# -- Installation (Handles both stacks) --
install: install-backend install-frontend

install-backend:
	@echo "🚀 Installing Backend dependencies..."
	cd backend && uv sync

install-frontend:
	@echo "🚀 Installing Frontend dependencies..."
	cd frontend && npm install	

# -- Backend Commands --
test-backend:
	@echo "🧪 Running Backend Tests..."
	cd backend && uv run pytest

lint-backend:
	@echo "🔍 Running Linters (Ruff + Mypy)..."
	cd backend && uv run ruff check .
	cd backend && uv run mypy .

format-backend:
	@echo "🎨 Formatting Code (Ruff)..."
	cd backend && uv run ruff format .

security-backend:
	@echo "🛡️ Running Security Scans (Bandit + Safety)..."
	cd backend && uv run bandit -c pyproject.toml -r .
	# cd backend && uv run safety scan

# -- Execution --
run-backend:
	@echo "🐍 Starting FastAPI Backend..."
	# --host 0.0.0.0 is crucial for Docker/DevContainers so you can access it from Windows	
	cd backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	@echo "⚛️ Starting React Frontend..."
	cd frontend && npm start

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
	@echo "  make test-backend - Run backend tests (pytest)"
	@echo "  make lint-backend - Run backend linters (ruff, mypy)"
	@echo "  make format-backend - Format backend code (ruff)"
	@echo "  make security-backend - Run security scans (bandit, safety)"
	@echo "  make run-backend - Start FastAPI server (accessible outside container)"
	@echo "  make run-frontend - Start React dev server"
	@echo "  make clean - Remove artifacts and virtual environments"