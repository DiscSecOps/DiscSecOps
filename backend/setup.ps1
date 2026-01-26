# Quick Start Script for Backend Setup
# Run this script to set up your development environment

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "DevSecOps Backend Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host $pythonVersion -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "Installing development dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

# Create .env file
Write-Host ""
if (Test-Path .env) {
    Write-Host ".env file already exists. Skipping..." -ForegroundColor Green
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANT: Edit .env file and update SECRET_KEY!" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✅" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and update SECRET_KEY" -ForegroundColor White
Write-Host "2. Run tests: pytest" -ForegroundColor White
Write-Host "3. Start server: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "4. Visit: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
