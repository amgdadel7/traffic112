#!/bin/bash
# Script to test Traffic Light Detection API
# Usage: bash test_api.sh [image_file]

API_URL="https://traffic112.onrender.com"
IMAGE_FILE="${1:-test_image.jpg}"

echo "🧪 Testing Traffic Light Detection API"
echo "======================================"
echo ""

# Check if image file exists
if [ ! -f "$IMAGE_FILE" ]; then
    echo "❌ Image file not found: $IMAGE_FILE"
    echo "   Usage: bash test_api.sh [image_file]"
    echo "   Example: bash test_api.sh my_image.jpg"
    exit 1
fi

echo "📋 Step 1: Health Check"
echo "----------------------"
curl -s "$API_URL/health" | python -m json.tool 2>/dev/null || curl -s "$API_URL/health"
echo ""
echo ""

echo "📋 Step 2: Model Status"
echo "----------------------"
curl -s "$API_URL/model-status" | python -m json.tool 2>/dev/null || curl -s "$API_URL/model-status"
echo ""
echo ""

echo "📋 Step 3: Testing Detection"
echo "----------------------"
echo "Uploading: $IMAGE_FILE"
echo ""

RESPONSE=$(curl -s -X POST \
  "$API_URL/detect" \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F "file=@$IMAGE_FILE")

# Try to format as JSON, fallback to raw output
echo "$RESPONSE" | python -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

# Check if response contains error
if echo "$RESPONSE" | grep -q "error\|Error\|detail"; then
    echo "⚠️  Error detected in response"
else
    echo "✅ Request completed successfully"
fi

