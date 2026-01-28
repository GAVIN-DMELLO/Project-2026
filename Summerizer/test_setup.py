"""
Test script to verify the backend setup
Run this after installing requirements to check if everything is working
"""

print("Testing Academic Summarizer Backend Setup")
print("=" * 50)

# Test 1: Import Flask
try:
    import flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import failed: {e}")

# Test 2: Import flask_cors
try:
    import flask_cors
    print("✓ Flask-CORS imported successfully")
except ImportError as e:
    print(f"✗ Flask-CORS import failed: {e}")

# Test 3: Import PyPDF2
try:
    import PyPDF2
    print("✓ PyPDF2 imported successfully")
except ImportError as e:
    print(f"✗ PyPDF2 import failed: {e}")

# Test 4: Import youtube_transcript_api
try:
    import youtube_transcript_api
    print("✓ youtube-transcript-api imported successfully")
except ImportError as e:
    print(f"✗ youtube-transcript-api import failed: {e}")

# Test 5: Import anthropic
try:
    import anthropic
    print("✓ Anthropic library imported successfully")
except ImportError as e:
    print(f"✗ Anthropic import failed: {e}")

# Test 6: Check for API key
import os
if os.environ.get("ANTHROPIC_API_KEY"):
    print("✓ ANTHROPIC_API_KEY environment variable is set")
else:
    print("⚠ ANTHROPIC_API_KEY not set (optional, basic mode will be used)")

# Test 7: Check if uploads directory can be created
try:
    os.makedirs('uploads', exist_ok=True)
    print("✓ Uploads directory accessible")
except Exception as e:
    print(f"✗ Cannot create uploads directory: {e}")

print("=" * 50)
print("Setup verification complete!")
print("\nIf all tests passed, you're ready to run:")
print("  python app.py")
