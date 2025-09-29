#!/bin/bash
echo "========================================"
echo "Starting All gRPC Services"
echo "========================================"
echo ""

export PYTHONPATH="$PWD/src"

# Start services in background
echo "Starting User Service (port 50051)..."
python src/services/user/server.py &
USER_PID=$!

sleep 2

echo "Starting Business Service (port 50052)..."
python src/services/business/server.py &
BUSINESS_PID=$!

sleep 2

echo "Starting Beneficiary Service (port 50053)..."
python src/services/beneficiary/server.py &
BENEFICIARY_PID=$!

sleep 2

echo ""
echo "========================================"
echo "✓ All services started!"
echo "========================================"
echo ""
echo "Services running on:"
echo "  User Service:        localhost:50051"
echo "  Business Service:    localhost:50052"
echo "  Beneficiary Service: localhost:50053"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for all processes
wait $USER_PID $BUSINESS_PID $BENEFICIARY_PID
