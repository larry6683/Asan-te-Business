#!/bin/bash
echo "Starting Business Service on port 50052..."
export PYTHONPATH="$PWD/src"
python src/services/business/server.py
