@echo off
REM Student Performance Predictor - Vercel Deployment Setup Script (Windows)

echo ========================================
echo Student Performance Predictor
echo Vercel Deployment Setup
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)
python --version

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js
    pause
    exit /b 1
)
node --version

REM Check Git
echo Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Please install Git
    pause
    exit /b 1
)
git --version

echo.
echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Installing Node.js dependencies...
call npm install

echo.
echo Step 3: Training ML model...
python model_training.py

echo.
echo Step 4: Checking essential files...
if exist "saved_model.pkl" (
    echo OK: Model file exists: saved_model.pkl
) else (
    echo ERROR: Model file not found. Run: python model_training.py
    pause
    exit /b 1
)

if exist "vercel.json" (
    echo OK: Vercel configuration exists
) else (
    echo ERROR: vercel.json not found
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Initialize Git: git init
echo 2. Add files: git add .
echo 3. Commit: git commit -m "Prepare for Vercel deployment"
echo 4. Create GitHub repository and push
echo 5. Go to https://vercel.com/new and import your repo
echo.
echo Read VERCEL_DEPLOYMENT_GUIDE.md for detailed instructions
echo.
pause
