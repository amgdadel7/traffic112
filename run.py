#!/usr/bin/env python3
"""
Script to run the FastAPI application locally
"""
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

