#!/usr/bin/env python3
"""
Fix TensorFlow compatibility issues by replacing tf.gfile with tf.io.gfile
"""

import os
import re

def fix_tf_compatibility():
    """Fix tf.gfile references in utils files"""
    
    # Files to fix
    files_to_fix = [
        'utils/label_map_util.py',
        'utils/visualization_utils.py', 
        'utils/dataset_util.py',
        'utils/config_util.py',
        'utils/category_util.py'
    ]
    
    # Patterns to replace
    replacements = [
        (r'tf\.gfile\.GFile', 'tf.io.gfile.GFile'),
        (r'tf\.gfile\.Open', 'tf.io.gfile.GFile'),
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"🔧 Fixing {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed {file_path}")
            else:
                print(f"⏭️ No changes needed for {file_path}")
        else:
            print(f"❌ File not found: {file_path}")

if __name__ == "__main__":
    print("🚀 Starting TensorFlow compatibility fixes...")
    fix_tf_compatibility()
    print("✅ All fixes completed!")