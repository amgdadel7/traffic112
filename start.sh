#!/bin/bash
# Startup script for FastAPI application

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONUNBUFFERED=1

echo "🚦 Starting Traffic Light Detection API..."
echo "📡 API will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""

# Run with uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload