@echo off
REM Start Docusaurus Frontend with Chatbot
echo.
echo ========================================
echo Docusaurus Book + Chatbot Startup
echo ========================================
echo.

cd docusaurus-book

echo Installing dependencies...
echo.
call npm install

echo.
echo ========================================
echo Starting Docusaurus...
echo ========================================
echo.
echo Your book will be available at: http://localhost:3000
echo Chatbot at: http://localhost:3000/chat
echo.

call npm start

pause
