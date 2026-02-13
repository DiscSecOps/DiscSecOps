#!/bin/bash
# Generate Secure Secrets for Environment Configuration
# Cross-platform script for Linux/Mac/Windows (Git Bash)

set -e

echo ""
echo "================================"
echo "Secret Generator for DevSecOps"
echo "================================"
echo ""

echo "Generating cryptographically secure secrets..."
echo ""

# Generate secrets using OpenSSL (available in most environments)
if command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -base64 32)
    SESSION_SECRET_KEY=$(openssl rand -base64 32)
    
    echo "Copy these to your backend/.env file:"
    echo ""
    echo "SECRET_KEY=$SECRET_KEY"
    echo "SESSION_SECRET_KEY=$SESSION_SECRET_KEY"
    echo ""
elif command -v python3 &> /dev/null; then
    # Fallback to Python if OpenSSL not available
    echo "Using Python for secret generation..."
    python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe(32)}'); print(f'SESSION_SECRET_KEY={secrets.token_urlsafe(32)}')"
    echo ""
else
    echo "❌ Error: Neither OpenSSL nor Python3 found!"
    echo "   Please install one of them to generate secrets."
    exit 1
fi

echo "================================"
echo "Security Best Practices"
echo "================================"
echo ""
echo "[OK] Use these generated secrets in your .env file"
echo "[OK] NEVER commit .env files to git"
echo "[OK] Rotate secrets every 30-90 days"
echo "[OK] Use different secrets for dev/staging/prod"
echo "[NO] Don't share secrets via Slack/Email"
echo "[NO] Don't use weak secrets like 'secret123'"
echo ""
echo "✨ Secrets generated successfully!"
echo ""
