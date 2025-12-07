@echo off
REM Start RAG Chatbot Backend
echo.
echo ========================================
echo RAG Chatbot Backend Startup
echo ========================================
echo.

cd backend

echo Installing Python packages...
echo.
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo.
echo ========================================
echo Starting FastAPI Server...
echo ========================================
echo.
echo API will be available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause
