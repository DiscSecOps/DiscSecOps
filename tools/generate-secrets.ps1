# Generate Secure Secrets for Environment Configuration
# Run this script to generate cryptographically secure secrets for your .env file

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Secret Generator for DevSecOps" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Generating cryptographically secure secrets...`n" -ForegroundColor Yellow

# Generate SECRET_KEY (for JWT) - PowerShell 5.1 compatible
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$bytes1 = New-Object byte[] 32
$rng.GetBytes($bytes1)
$secretKey = [System.Convert]::ToBase64String($bytes1)

# Generate SESSION_SECRET_KEY (for sessions)
$bytes2 = New-Object byte[] 32
$rng.GetBytes($bytes2)
$sessionSecretKey = [System.Convert]::ToBase64String($bytes2)

Write-Host "Copy these to your backend/.env file:`n" -ForegroundColor Green

Write-Host "SECRET_KEY=" -NoNewline -ForegroundColor White
Write-Host $secretKey -ForegroundColor Yellow

Write-Host "SESSION_SECRET_KEY=" -NoNewline -ForegroundColor White
Write-Host $sessionSecretKey -ForegroundColor Yellow

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Alternative: Using OpenSSL" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "If you have Git Bash or WSL, you can also use:" -ForegroundColor Gray
Write-Host "  openssl rand -hex 32`n" -ForegroundColor White

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Security Best Practices" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "[OK] Use these generated secrets in your .env file" -ForegroundColor Green
Write-Host "[OK] NEVER commit .env files to git" -ForegroundColor Green
Write-Host "[OK] Rotate secrets every 30-90 days" -ForegroundColor Green
Write-Host "[OK] Use different secrets for dev/staging/prod" -ForegroundColor Green
Write-Host "[NO] Don't share secrets via Slack/Email" -ForegroundColor Red
Write-Host "[NO] Don't use weak secrets like 'secret123'" -ForegroundColor Red

Write-Host "Secrets generated successfully!`n" -ForegroundColor Green
