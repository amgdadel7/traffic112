#!/bin/bash
# Startup script for Render deployment

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONUNBUFFERED=1

# Get port from environment variable (Render sets this automatically)
PORT=${PORT:-10000}

echo "🚦 Starting Traffic Light Detection API on Render..."
echo "📡 API will be available on port: $PORT"
echo "📚 API Documentation: /docs"
echo ""

# Run with uvicorn (Render will set PORT automatically)
python -m uvicorn main:app --host 0.0.0.0 --port $PORT

