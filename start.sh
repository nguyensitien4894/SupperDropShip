#!/bin/bash

echo "🚀 Starting Dropship Intelligence Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database Configuration
MONGODB_URI=mongodb://localhost:27017/dropship_intelligence
REDIS_URL=redis://localhost:6379

# API Keys (Add your own keys here)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
TIKTOK_API_KEY=your_tiktok_api_key_here

# Server Configuration
PORT=8000
NODE_ENV=development

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Dropship Intelligence

# Cron Job Configuration
CRON_ENABLED=true
CRON_TIMEZONE=UTC

# Logging
LOG_LEVEL=info
LOG_FILE=logs/app.log
EOF
    echo "✅ .env file created. Please add your API keys to the .env file."
fi

echo ""
echo "🎉 Setup complete! To start the platform:"
echo ""
echo "1. Start the backend:"
echo "   cd backend && python main.py"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open your browser to:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "📚 For more information, see the README.md file." 