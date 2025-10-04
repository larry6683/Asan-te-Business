#!/bin/bash
echo "Starting Auth Service on port 50054..."
export PYTHONPATH="$PWD/src"
python src/services/auth/server.py
