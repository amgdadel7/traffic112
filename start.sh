#!/bin/bash
# Startup script with protobuf fix

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONUNBUFFERED=1

echo "Starting Traffic Light Detection API with protobuf fix..."
python main.py