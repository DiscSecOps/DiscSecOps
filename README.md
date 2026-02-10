# Social App - DevSecOps Project

## Project Overview

A modern social web application built with React, FastAPI, and DevSecOps practices. This project focuses on continuous integration, automated testing, and secure deployment.

## 🛠️ Development Environment

This project is built using **Visual Studio Code Dev Containers**. This ensures that everyone working on the project uses the exact same OS, tools, and dependencies (Python, Node.js, Playwright browsers, etc.) without needing to install them manually on their local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

1.  **Container Runtime** (Choose one):
    * [**Docker Desktop**](https://www.docker.com/products/docker-desktop/)
    * [**Rancher Desktop**](https://rancherdesktop.io/) (Ensure `dockerd` (moby) is selected in Kubernetes Settings if using this)
2.  [**Visual Studio Code**](https://code.visualstudio.com/)
3.  **Dev Containers Extension** for VS Code (id: `ms-vscode-remote.remote-containers`)

## 🚀 Quick Start: Dev Container

This project is designed to run in a VS Code Dev Container. This ensures you have Python, Node.js, Postgres, and all tools pre-installed.

1. Open Docker Desktop (or Rancher Desktop)
2. Open the project root in VS Code.
3. When prompted, click "Reopen in Container". 
4. Wait for the build to finish. The environment will automatically run make install to set up dependencies.

## Project Structure

```
/
├── frontend/                    # React application with Vite
│   ├── src/                     # Source code
│   ├── node_modules/            # Frontend dependencies
│   ├── package.json             # Frontend dependencies and scripts
│   ├── vite.config.js           # Vite configuration
│   ├── vitest.config.js         # Vitest configuration
│   └── index.html  
├── features/                    # 
├── backend/
│   ├── .venv/                    # Virtual environment (managed by uv)
│   ├── app/                      # Application source code
│   ├── tests/                    # Test suite
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore rules
│   ├── pyproject.toml            # Project configuration & dependencies
│   └── uv.lock                   # Exact dependency versions
├── .github/workflows/            # CI/CD pipelines
└── README.md                     # This file
```

### Frontend Tech Stack

- **React 19** with Vite
- **React Router DOM** v6
- **Axios** for HTTP requests
- **Vitest** + Testing Library (unit/integration)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev  # [http://localhost:3000]
```

### Unit/Integration Tests

```bash
cd frontend
npm test  # Vitest watch mode
npm run test:run  # Single run
```

### E2E Tests (Playwright BDD)

npm run test:e2e        # Runs all .feature files
npm run test:e2e:ui     # Interactive UI

### API:

http://localhost:3000/login
http://localhost:3000/register
http://localhost:3000/dashboard

## Testing Strategy

Vitest: Unit and integration tests for React components

Located in frontend/src/tests/ or alongside components

Uses @testing-library/react for component testing ***npm*** install @testing-library/jest-dom

Uses jsdom for browser environment simulation

Playwright: End-to-end tests

Located in tests/e2e/ directory

Tests complete user flows

Runs in real browsers (Chromium)

## Backend Setup (Future)


## CI/CD Pipeline

GitHub Actions workflow located in .github/workflows/frontend-ci.yml:

Runs on push to main/develop branches and pull requests

Installs dependencies

Runs Vitest unit tests

Runs Playwright E2E tests

Builds production bundle

Development Workflow
All frontend development happens in frontend/ directory

Write tests alongside features (TDD approach)

Push changes to trigger CI pipeline

Merge to main after passing tests

Getting Started
Prerequisites
Node.js 18 or higher

npm 9 or higher

## Clone the repository

git clone <https://github.com/DiscSecOps/DiscSecOps>

## Install dependencies

npm install

## Start development server frontend
cd /workspace/frontend
npm run dev

## Start development server backend
cd /workspace/backend
uv run uvicorn app.main:app --reload --port 5000

Backend: http://localhost:5000/health

Frontend: http://localhost:3000

API Docs: http://localhost:5000/docs

## Run tests (in another terminal)

npm test
Project Status
✅ Frontend setup complete with testing infrastructure
🔜 Backend development
🔜 Database integration
🔜 Authentication system
🔜 Deployment configuration

Notes
All frontend commands must be executed from the frontend directory

Playwright browsers are installed automatically on first test run

The project follows DevSecOps principles with security integrated from the start

Feature development uses slicing methodology for incremental delivery

Contributors
Camelia Ciuca
Haidar Alany
Mattias Hammarhorn
Richard Orme
Shahzad Babar

License
MIT

## 🎯 For Frontend Developers (Simplified Commands)

### Only 3 commands you need:

```bash
# 1. Install once
make install

# 2. Start development (in separate terminals)
make run-backend    # Terminal 1 - API on http://localhost:5000
make run-frontend   # Terminal 2 - App on http://localhost:3000

# 3. Run tests (optional)
make test-frontend-unit