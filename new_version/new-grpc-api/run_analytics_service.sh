#!/bin/bash
echo "Starting Analytics Service on port 50054..."
export PYTHONPATH="$PWD/src"
python src/services/analytics/server.py