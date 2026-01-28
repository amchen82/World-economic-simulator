#!/bin/bash
# Setup script for World Economic Simulator

echo "Setting up World Economic Simulator..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node dependencies
echo "Installing Node dependencies..."
cd dashboard
npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application, run: ./start.sh"
