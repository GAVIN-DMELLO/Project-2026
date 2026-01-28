#!/bin/bash

echo "=========================================="
echo "Academic Summarizer - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 detected"

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. (Optional) Set your Claude API key:"
echo "   export ANTHROPIC_API_KEY='your-api-key-here'"
echo ""
echo "2. Start the backend server:"
echo "   python app.py"
echo ""
echo "3. Open frontend/index.html in your browser"
echo ""
echo "=========================================="
