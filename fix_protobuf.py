#!/usr/bin/env python3
"""
Quick fix for protobuf compatibility issues
"""
import os
import subprocess
import sys

def fix_protobuf():
    """Fix protobuf compatibility issues"""
    print("Fixing protobuf compatibility issues...")
    
    # Set environment variable
    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
    
    # Downgrade protobuf
    print("Downgrading protobuf to 3.20.3...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'protobuf==3.20.3'], check=True)
        print("✓ Protobuf downgraded successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to downgrade protobuf: {e}")
        return False
    
    print("✓ Protobuf fix completed!")
    return True

if __name__ == "__main__":
    if fix_protobuf():
        print("\nNow try running: python main.py")
    else:
        print("\nFix failed. Please check the error messages above.")