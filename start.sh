#!/bin/bash
# Start script for World Economic Simulator

echo "Starting World Economic Simulator..."

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down services..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
    fi
    if [ ! -z "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null
    fi
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT SIGTERM

# Start the API server in the background
echo "Starting API server on port 5000..."
cd "$(dirname "$0")"
python3 api/server.py &
API_PID=$!

# Wait for API to be ready
echo "Waiting for API to be ready..."
sleep 3

# Start the dashboard
echo "Starting dashboard on port 3000..."
cd dashboard
npm start &
DASHBOARD_PID=$!

echo "API PID: $API_PID"
echo "Dashboard PID: $DASHBOARD_PID"
echo ""
echo "✅ World Economic Simulator is running!"
echo "   API: http://localhost:5000"
echo "   Dashboard: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $API_PID $DASHBOARD_PID
