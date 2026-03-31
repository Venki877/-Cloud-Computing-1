#!/bin/bash

# Student Performance Predictor - Vercel Deployment Setup Script
# This script prepares your project for Vercel deployment

echo "🚀 Student Performance Predictor - Vercel Setup"
echo "================================================"
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi
python --version

# Check Node.js
echo "✓ Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js"
    exit 1
fi
node --version

# Check Git
echo "✓ Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi
git --version

echo ""
echo "Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Installing Node.js dependencies..."
npm install

echo ""
echo "Step 3: Training ML model..."
python model_training.py

echo ""
echo "Step 4: Checking essential files..."
if [ -f "saved_model.pkl" ]; then
    echo "✅ Model file exists: saved_model.pkl"
else
    echo "❌ Model file not found. Please run: python model_training.py"
    exit 1
fi

if [ -f "vercel.json" ]; then
    echo "✅ Vercel configuration exists"
else
    echo "❌ vercel.json not found"
    exit 1
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Initialize Git (if not already): git init"
echo "2. Add all files: git add ."
echo "3. Commit: git commit -m 'Prepare for Vercel deployment'"
echo "4. Create GitHub repository and push"
echo "5. Go to https://vercel.com/new and import your repo"
echo ""
echo "For detailed instructions, read: VERCEL_DEPLOYMENT_GUIDE.md"
