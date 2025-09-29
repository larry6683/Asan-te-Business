#!/bin/bash
echo "Starting Beneficiary Service on port 50053..."
export PYTHONPATH="$PWD/src"
python src/services/beneficiary/server.py
