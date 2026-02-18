#!/usr/bin/env python3
"""
Generate Secure Secrets for Environment Configuration
Cross-platform secret generation (works on Linux, Mac, Windows)
"""

import secrets
import sys


def generate_secret(length=32):
    """Generate a cryptographically secure random secret."""
    return secrets.token_urlsafe(length)


def main():
    print("\n" + "=" * 50)
    print("Secret Generator for DevSecOps")
    print("=" * 50 + "\n")
    
    print("Generating cryptographically secure secrets...\n")
    
    # Generate secrets
    secret_key = generate_secret(32)
    session_secret_key = generate_secret(32)
    
    print("Copy these to your backend/.env file:\n")
    print(f"SECRET_KEY={secret_key}")
    print(f"SESSION_SECRET_KEY={session_secret_key}")
    
    print("\n" + "=" * 50)
    print("Alternative: Using OpenSSL")
    print("=" * 50 + "\n")
    
    print("If you prefer OpenSSL, run:")
    print("  openssl rand -base64 32\n")
    
    print("=" * 50)
    print("Security Best Practices")
    print("=" * 50 + "\n")
    
    print("[OK] Use these generated secrets in your .env file")
    print("[OK] NEVER commit .env files to git")
    print("[OK] Rotate secrets every 30-90 days")
    print("[OK] Use different secrets for dev/staging/prod")
    print("[NO] Don't share secrets via Slack/Email")
    print("[NO] Don't use weak secrets like 'secret123'")
    
    print("\nSecrets generated successfully!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
