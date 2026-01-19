#!/bin/bash
# Quick Start Script for Nepal Telco Churn Prediction

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🇳🇵 Nepal Telco Churn Prediction System - Quick Start    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check virtual environment
echo "📦 Setting up virtual environment..."
if [ ! -d "tf_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv tf_venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source tf_venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create logs directory
mkdir -p logs
echo "📁 Created logs directory"
echo ""

# Display startup options
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 Ready to Run!                                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose how to run the application:"
echo ""
echo "1️⃣  Run Streamlit UI Only:"
echo "    python main.py --ui"
echo ""
echo "2️⃣  Run FastAPI Backend Only:"
echo "    python main.py --api"
echo ""
echo "3️⃣  Run Both (Recommended):"
echo "    python main.py --both"
echo ""
echo "4️⃣  Custom API Port:"
echo "    python main.py --api --port 9000"
echo ""
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🌐 UI URL: http://localhost:8501"
echo ""
echo "💡 Tip: Use 'python main.py --help' for more options"
echo ""
