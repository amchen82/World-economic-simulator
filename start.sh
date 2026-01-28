#!/bin/bash
# Start script for World Economic Simulator

echo "Starting World Economic Simulator..."

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
