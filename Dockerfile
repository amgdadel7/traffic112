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

# Download and extract the model during build
# Use --no-same-owner to avoid chown errors on restricted filesystems (e.g. Render)
RUN curl -L -o ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    https://storage.googleapis.com/download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz && \
    tar --no-same-owner --no-same-permissions -xzf ssd_mobilenet_v1_coco_11_06_2017.tar.gz && \
    rm ssd_mobilenet_v1_coco_11_06_2017.tar.gz && \
    echo "✅ Model downloaded and extracted successfully"

# Verify model files exist
RUN ls -la ssd_mobilenet_v1_coco_11_06_2017/ && \
    test -f ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb && \
    echo "✅ Model files verified in Docker image"

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

ENV PYTHONUNBUFFERED=1
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV PORT=8080

EXPOSE 8080

# Run FastAPI server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --log-level info"]

