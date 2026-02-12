# Quick Setup Guide for Frontend Team
# Run this in PowerShell from the frontend directory

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Frontend Environment Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if .env already exists
if (Test-Path ".env") {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
    Write-Host "   Review and update if needed`n" -ForegroundColor Yellow
} else {
    # Create .env from .env.example
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env from .env.example" -ForegroundColor Green
        Write-Host "   You can modify it for your local setup`n" -ForegroundColor Yellow
    } else {
        Write-Host "❌ .env.example not found!" -ForegroundColor Red
        Write-Host "   Please create it first`n" -ForegroundColor Red
        exit 1
    }
}

# Display current configuration
Write-Host "Current Configuration:" -ForegroundColor Cyan
Write-Host "---------------------" -ForegroundColor Cyan
Get-Content .env | Where-Object { $_ -notmatch '^#' -and $_ -ne '' } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan
Write-Host "1. Install dependencies:  npm install" -ForegroundColor White
Write-Host "2. Start dev server:      npm run dev" -ForegroundColor White
Write-Host "3. Frontend will run on:  http://localhost:3000" -ForegroundColor Green
Write-Host "4. Make sure backend is running on port 8000`n" -ForegroundColor Yellow

Write-Host "✨ Setup complete!" -ForegroundColor Green
