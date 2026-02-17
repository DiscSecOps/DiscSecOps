#!/bin/bash
# Frontend Environment Setup Script
# Cross-platform setup for Linux/Mac/Windows (Git Bash)

set -e

echo ""
echo "================================"
echo "Frontend Environment Setup"
echo "================================"
echo ""

# Check if .env.example exists
if [ ! -f ".env.example" ]; then
    echo "❌ .env.example not found!"
    echo "   Please create it first"
    echo ""
    exit 1
fi

# Check if .env already exists
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
    echo "   Review and update if needed"
    echo ""
else
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created successfully!"
    echo ""
fi

# Display current configuration
echo "Current Configuration:"
echo "---------------------"
if [ -f ".env" ]; then
    grep "^VITE_" .env | while IFS= read -r line; do
        echo "  $line"
    done
else
    echo "  No .env file found"
fi

echo ""
echo "================================"
echo "Next Steps:"
echo "================================"
echo ""
echo "1. Install dependencies:  npm install"
echo "2. Start dev server:      npm run dev"
echo "3. Frontend will run on:  http://localhost:3000"
echo "4. Make sure backend is running on port 8000"
echo ""
echo "✨ Setup complete!"
echo ""
