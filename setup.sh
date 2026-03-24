#!/bin/bash
# Quick setup script for TaskAPI
# Run this once after cloning the repo

echo "Setting up TaskAPI..."

# Create virtual environment
python -m venv venv
echo "Virtual environment created."

# Activate it
source venv/bin/activate 2>/dev/null || venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
echo "Dependencies installed."

# Copy env file if not already present
if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env file created. Please open it and set a strong SECRET_KEY."
fi

echo ""
echo "Setup complete! Run the server with:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Then open: http://localhost:8000/docs"
