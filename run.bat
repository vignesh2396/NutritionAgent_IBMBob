@echo off
:: ============================================================
:: NutriBot — Agentic AI Nutritionist
:: Powered by Google Gemini + IBM Granite-style Guardrails
:: Windows Launcher Script
:: ============================================================
:: This script:
::   1. Checks Python is installed
::   2. Installs required packages from requirements.txt
::   3. Verifies GEMINI_API_KEY in .env
::   4. Launches the Streamlit web application
:: ============================================================

title NutriBot — Agentic AI Nutritionist

echo.
echo  ====================================================
echo   NutriBot — Agentic AI Nutritionist
echo   Powered by Google Gemini + IBM Granite Guardrails
echo  ====================================================
echo.

:: ── Step 1: Verify Python ────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found.

:: ── Step 2: Install / upgrade pip ────────────────────────────
echo.
echo [STEP 1/3] Installing / verifying dependencies...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNING] Could not upgrade pip. Continuing...
)

:: ── Step 3: Install requirements ─────────────────────────────
pip install -r requirements.txt --prefer-binary --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install requirements.
    echo Please check your internet connection and requirements.txt
    pause
    exit /b 1
)
echo [OK] All dependencies installed.

:: ── Step 4: Check .env file for GEMINI_API_KEY ────────────────
echo.
echo [STEP 2/3] Checking credentials...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [INFO] Created .env from template.
    )
    echo.
    echo  ┌────────────────────────────────────────────────────┐
    echo  │  ACTION REQUIRED: Add your Gemini API Key           │
    echo  │                                                      │
    echo  │  1. Open the file: .env (in this folder)            │
    echo  │  2. Set the value:                                   │
    echo  │     GEMINI_API_KEY=your_actual_api_key_here         │
    echo  │                                                      │
    echo  │  Get your free Gemini API key from:                 │
    echo  │  https://aistudio.google.com/app/apikey             │
    echo  │                                                      │
    echo  │  OR enter the key directly in the app sidebar.      │
    echo  └────────────────────────────────────────────────────┘
    echo.
) else (
    findstr /i "GEMINI_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] .env exists but GEMINI_API_KEY not found.
        echo Please add:  GEMINI_API_KEY=your_key_here  to .env
    ) else (
        echo [OK] .env found with GEMINI_API_KEY.
    )
)

:: ── Step 5: Create plans directory ───────────────────────────
if not exist "plans" (
    mkdir plans
    echo [OK] Created plans/ directory for saving nutrition plans.
)

:: ── Step 6: Launch Streamlit ──────────────────────────────────
echo.
echo [STEP 3/3] Launching NutriBot web application...
echo.
echo  ====================================================
echo   App will open at: http://localhost:8501
echo   Press Ctrl+C in this window to stop the server
echo  ====================================================
echo.

:: Open browser after a short delay (background)
start /b cmd /c "timeout /t 4 >nul && start http://localhost:8501"

:: Start Streamlit
streamlit run app.py --server.headless false --browser.gatherUsageStats false

if errorlevel 1 (
    echo.
    echo [ERROR] Streamlit failed to start.
    echo Try running manually: streamlit run app.py
    pause
)
