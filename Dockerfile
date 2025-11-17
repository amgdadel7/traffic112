FROM python:3.7-slim

WORKDIR /app

# System deps (opencv/tensorflow may require libs)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install with timeout handling
COPY requirements-cloud.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip==22.3.1 setuptools==65.5.0 wheel \
    && pip install --no-cache-dir --timeout 1000 --retries 5 -r requirements.txt

# Copy application files
COPY . .

# Ensure label map is available
COPY mscoco_label_map.pbtxt ./

# Try to download model during build (optional - will download at runtime if fails)
# Model will be automatically downloaded by main.py at runtime if not present
RUN if curl -L --retry 3 --retry-delay 5 --max-time 180 --fail --silent --show-error \
        -o ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
        https://storage.googleapis.com/download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
        || curl -L --retry 3 --retry-delay 5 --max-time 180 --fail --silent --show-error \
        -o ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
        https://github.com/tensorflow/models/raw/master/research/object_detection/test_data/ssd_mobilenet_v1_coco_11_06_2017.tar.gz; then \
        tar -xzf ssd_mobilenet_v1_coco_11_06_2017.tar.gz && \
        rm ssd_mobilenet_v1_coco_11_06_2017.tar.gz && \
        echo "✅ Model downloaded and extracted successfully"; \
    else \
        echo "⚠️ Model download skipped - will be downloaded at runtime by main.py"; \
    fi || true

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

ENV PYTHONUNBUFFERED=1
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV PORT=8080

EXPOSE 8080

# Run FastAPI server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --log-level info"]

