#!/bin/bash

echo "🚀 Starting Dropship Intelligence Platform..."

# Kill any existing processes
echo "🔄 Stopping any existing processes..."
pkill -f "python.*main" 2>/dev/null
pkill -f "next.*dev" 2>/dev/null

# Start backend
echo "🔧 Starting backend server..."
source venv/bin/activate
python -m backend.main &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
npm run dev &
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
echo "🎉 Dropship Intelligence Platform is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
wait 