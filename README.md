# Social App - DevSecOps Project

## Project Overview

A modern social web application built with React, FastAPI, and DevSecOps practices. This project focuses on continuous integration, automated testing, and secure deployment.

## Project Structure

text
social-app-devsecops/
├── frontend/                    # React application with Vite
│   ├── src/                    # Source code
│   ├── node_modules/           # Frontend dependencies
│   ├── package.json           # Frontend dependencies and scripts
│   ├── vite.config.js         # Vite configuration
│   ├── vitest.config.js       # Vitest configuration
│   └── index.html  
    ├── tests/
            e2e           # Entry point
├── backend/                    # FastAPI application (to be developed)
                     # Playwright E2E tests
├── .github/workflows/         # CI/CD pipelines
└── README.md                  # This file

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

## Start development server

npm run dev

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
npm run test:e2e     # Run Playwright E2E tests ***Test*** development server on [http://localhost:3001]
npm run test:e2e:ui  # Run Playwright with UI mode
npm run test:e2e:headed  # Run Playwright in headed browser

## Testing for organization

Testing
