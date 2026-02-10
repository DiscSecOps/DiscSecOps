# Start Backend Server with PostgreSQL
$env:DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5433/app_db"
Write-Host "Starting backend server on http://127.0.0.1:8000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
py -3.14 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
