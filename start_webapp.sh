#!/bin/bash

# AI Band Generator Web App Startup Script

echo "🎸 Starting AI Band Generator Web App..."

# Check if virtual environment exists
if [ ! -d "ai_band_env" ]; then
    echo "❌ Virtual environment not found. Please run the following commands first:"
    echo "   python3 -m venv ai_band_env"
    echo "   source ai_band_env/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ai_band_env/bin/activate

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