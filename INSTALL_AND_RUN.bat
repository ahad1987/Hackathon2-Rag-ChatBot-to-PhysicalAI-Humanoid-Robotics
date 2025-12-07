@echo off
REM Install dependencies and run chatbot backend
echo.
echo ========================================
echo RAG Chatbot - Quick Install & Run
echo ========================================
echo.

REM Try minimal requirements first
cd backend

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet

echo Installing Python packages (minimal version)...
python -m pip install -r requirements-minimal.txt

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Issue with minimal install, trying full requirements...
    python -m pip install -r requirements.txt
)

echo.
echo ========================================
echo ✅ Installation Complete!
echo ========================================
echo.
echo Starting Backend API...
echo.
echo 🌐 API will run on: http://localhost:8000
echo 📚 API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause
