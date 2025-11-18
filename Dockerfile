# Use Python 3.9 as specified in render.yaml
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including OpenCV requirements
# Update package lists
RUN apt-get update

# Install essential build tools first
RUN apt-get install -y --no-install-recommends \
    build-essential \
    curl

# Install OpenCV dependencies
RUN apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Health check (Render has its own health check via healthCheckPath in render.yaml)
# Using fixed port 8000 for Docker health check, but app listens on PORT env var
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "run.py"]

