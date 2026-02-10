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
│   ├── src/                    # Source code
│   ├── node_modules/           # Frontend dependencies
│   ├── package.json           # Frontend dependencies and scripts
│   ├── vite.config.js         # Vite configuration
│   ├── vitest.config.js       # Vitest configuration
│   └── index.html  
    ├── tests/
            e2e           # Entry point
├── backend/
│   ├── .venv/                    # Virtual environment (managed by uv)
│   ├── app/                      # Application source code
│   ├── tests/                    # Test suite
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore rules
│   ├── pyproject.toml            # Project configuration & dependencies
│   └── uv.lock                   # Exact dependency versions
                     # Playwright E2E tests
├── .github/workflows/         # CI/CD pipelines
└── README.md                  # This file
```

## Frontend Setup

***Technologies*** Used
React 19 - [https://tyronneratcliff.com/install-react-using-vite/#:~:text=npm%20create%20vite%40latest%20%28or%20yarn%20create%20vite%20or,This%20is%20the%20name%20of%20your%20project%20directory].

Frontend library

Vite - Build tool and dev server ***npm*** create vite@latest my-react-app -- --template react

React Router DOM - Navigation ***npm*** install react-router-dom

Axios - HTTP client for API calls [https://axios-http.com/docs/intro] ***npm*** install axios

Vitest - Unit and integration testing ***npm*** install -D vitest

Playwright - End-to-end testing ***npm*** init playwright@latest

Testing Library - React component testing

## Installation (Frontend Only)

All commands must be run from the frontend directory:

cd frontend
´´´bash
    npm install
´´´
Available Scripts (Run from frontend directory)

### Development

´´´´bash
npm run dev          # Start development server on [http://localhost:3000] // // vite.config.js
npm run preview      # Preview production build

### Building

´´´bash
npm run build        # Create production build
npm run lint         # Run ESLint

## Testing

´´´bash
npm test             # Run Vitest in watch mode
npm run test:run     # Run Vitest once ***npm*** install -D vitest
npm run test:e2e     # Run Playwright E2E tests ***npm*** init playwright@latest
npm run test:e2e:ui  # Run Playwright with UI mode
npm run test:e2e:headed  # Run Playwright in headed browser

## Testing Strategy

Vitest: Unit and integration tests for React components

Located in frontend/src/tests/ or alongside components

Uses @testing-library/react for component testing ***npm*** install @testing-library/jest-dom

Uses jsdom for browser environment simulation

Playwright: End-to-end tests

Located in tests/e2e/ directory

Tests complete user flows

Runs in real browsers (Chromium, Firefox, WebKit)

## Backend Setup (Future)

The backend will be developed using:

FastAPI - Python web framework

PostgreSQL - Database

Pytest - Backend testing

SQLAlchemy - ORM

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

Quick Start
bash

## Clone the repository

git clone <repository-url>
cd social-app-devsecops/frontend

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
[Your Name/Team Name]

License
[Your License]

Installation (Frontend Only)
All commands must be run from the frontend directory:

bash
cd frontend
npm install
Available Scripts (Run from frontend directory)
Development
bash
npm run dev          # Start development server on [http://localhost:3000]
npm run preview      # Preview production build
Building
bash
npm run build        # Create production build
npm run lint         # Run ESLint
Testing
bash
npm test             # Run Vitest in watch mode
npm run test:run     # Run Vitest once
npm run test:e2e     # Run Playwright E2E tests ***Test*** development server on [http://localhost:3000]
npm run test:e2e:ui  # Run Playwright with UI mode
npm run test:e2e:headed  # Run Playwright in headed browser

## Testing for organization

Testing with container 
