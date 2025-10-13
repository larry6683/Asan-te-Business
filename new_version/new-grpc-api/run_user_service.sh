#!/bin/bash
echo "Starting User Service on port 50051..."
export PYTHONPATH="$PWD/src"
python src/services/user/server.py
