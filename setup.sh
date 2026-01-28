#!/bin/bash
# Setup script for World Economic Simulator

set -e  # Exit on error

echo "Setting up World Economic Simulator..."

# Install Python dependencies
echo "Installing Python dependencies..."
if ! pip3 install -r requirements.txt; then
    echo "Error: Failed to install Python dependencies"
    exit 1
fi

# Install Node dependencies
echo "Installing Node dependencies..."
cd dashboard
if ! npm install; then
    echo "Error: Failed to install Node dependencies"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application, run: ./start.sh"
