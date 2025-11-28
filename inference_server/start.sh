#!/usr/bin/env bash
# Simple script to start the inference server

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/upgrading dependencies..."
pip install -q -r requirements.txt

echo "Starting inference server on port 8000..."
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
