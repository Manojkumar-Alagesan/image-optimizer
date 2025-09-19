#!/bin/bash

# Build script for creating Mac Silicon standalone application
echo "🚀 Building Image Optimizer for Mac Silicon..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script must be run on macOS"
    exit 1
fi

# Check if we're on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "⚠️  Warning: Building on non-Apple Silicon Mac. App will be Intel-based."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec~

# Build the application
echo "🔨 Building standalone application..."
pyinstaller image_optimizer.spec

# Check if build was successful
if [ -d "dist/ImageOptimizer.app" ]; then
    echo "✅ Build successful!"
    echo "📱 Your standalone Mac app is located at: dist/ImageOptimizer.app"
    echo ""
    echo "🔧 To install:"
    echo "   1. Copy dist/ImageOptimizer.app to /Applications/"
    echo "   2. Right-click and select 'Open' the first time (to bypass Gatekeeper)"
    echo ""
    echo "📦 App size: $(du -sh dist/ImageOptimizer.app | cut -f1)"

    # Optional: Open the dist folder
    read -p "📂 Open dist folder? (y/n): " open_folder
    if [[ $open_folder == "y" || $open_folder == "Y" ]]; then
        open dist/
    fi
else
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi

echo "🎉 Done!"