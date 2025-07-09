#!/bin/bash
# Simple launcher for the Batch Image Rotator app

echo "🚀 Launching Batch Image Rotator..."

# Check if executable exists
if [ -f "dist/BatchImageRotator" ]; then
    echo "📁 Running standalone executable..."
    ./dist/BatchImageRotator
elif [ -d "dist/BatchImageRotator.app" ]; then
    echo "📁 Running Mac app bundle..."
    open dist/BatchImageRotator.app
else
    echo "❌ No executable found. Please build the app first:"
    echo "   python3 build_app.py"
    exit 1
fi 