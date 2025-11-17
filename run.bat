@echo off
REM Script to run FastAPI application on Windows
echo Starting Traffic Light Detection API...
echo.
echo The API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause

