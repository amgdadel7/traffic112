#!/usr/bin/env python3
"""
Script to run the FastAPI application
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Render sets this) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Disable reload in production (Render sets RENDER environment variable)
    is_production = os.environ.get("RENDER") is not None or os.environ.get("PORT") is not None
    reload = not is_production
    
    # Run the FastAPI app
    uvicorn.run(
        "main1:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )

