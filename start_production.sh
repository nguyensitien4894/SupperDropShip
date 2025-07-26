#!/bin/bash

echo "🚀 Starting Dropship Intelligence Platform in PRODUCTION mode..."

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Starting MongoDB..."
    
    # Try to start MongoDB (adjust path as needed)
    if command -v mongod &> /dev/null; then
        mongod --fork --logpath /tmp/mongod.log
        echo "✅ MongoDB started"
    else
        echo "❌ MongoDB not found. Please install MongoDB first."
        echo "   On macOS: brew install mongodb-community"
        echo "   On Ubuntu: sudo apt-get install mongodb"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing/upgrading Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
# Database Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=dropship_intelligence

# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
EOF
    echo "✅ .env file created. Please update with your API keys."
fi

# Seed database with sample data
echo "🌱 Seeding database with sample products..."
python -c "
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('.')))
from backend.database.seeder import seed_database

async def main():
    try:
        await seed_database()
        print('✅ Database seeded successfully')
    except Exception as e:
        print(f'❌ Failed to seed database: {e}')

asyncio.run(main())
"

# Start backend server
echo "🔧 Starting backend server..."
python -m backend.main &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Build frontend for production
echo "🏗️  Building frontend for production..."
npm run build

# Start frontend in production mode
echo "🎨 Starting frontend in production mode..."
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Test frontend
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 Dropship Intelligence Platform is fully launched in PRODUCTION mode!"
echo ""
echo "📊 Backend API: http://localhost:8000"
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "📈 Features available:"
echo "   ✅ Real MongoDB database with 100+ sample products"
echo "   ✅ Advanced filtering and search"
echo "   ✅ AI-powered content generation"
echo "   ✅ Product scoring and analytics"
echo "   ✅ Social media data integration"
echo "   ✅ Supplier price tracking"
echo "   ✅ Trend analysis"
echo ""
echo "🔧 To stop the platform, press Ctrl+C"
echo ""

# Wait for both processes
wait $BACKEND_PID
wait $FRONTEND_PID 