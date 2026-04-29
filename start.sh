#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "Starting Pi Streamer..."
python3 pi_streamer.py
