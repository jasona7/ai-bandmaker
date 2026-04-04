#!/bin/bash

# AI Band Generator Web App Startup Script

echo "🎸 Starting AI Band Generator Web App..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    VENV_DIR="venv"
elif [ -d "ai_band_env" ]; then
    VENV_DIR="ai_band_env"
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    VENV_DIR="venv"
    source "$VENV_DIR/bin/activate"
    pip install -r requirements.txt
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set!"
    echo "   Please set your OpenAI API key:"
    echo "   export OPENAI_API_KEY='your_api_key_here'"
    echo ""
    echo "   The app will start but band generation will fail without a valid API key."
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Start the Flask app
echo "🚀 Starting Flask development server..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "⭐ To stop the server, press Ctrl+C"
echo ""

python app.py