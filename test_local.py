#!/usr/bin/env python3
"""
Test script to test the API locally
"""
import requests
import base64
import json

# Test health endpoint
print("🔍 Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Status: {response.status_code}")
    print(f"📋 Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("⚠️  Make sure the server is running: python run.py")

