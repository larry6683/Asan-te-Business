#!/bin/bash

echo "========================================"
echo "Starting All gRPC Services"
echo "========================================"
echo ""

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Set PYTHONPATH
export PYTHONPATH="$PWD/src"

# Test database connection first
echo "Testing database connection..."
python test_db_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Database connection test failed!"
    echo "  Please check your database configuration and ensure PostgreSQL is running."
    exit 1
fi

echo ""
echo "Starting services..."
echo ""

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
echo "Database:"
echo "  Host: $DB_HOST"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap Ctrl+C to kill all services
trap "echo ''; echo 'Stopping services...'; kill $USER_PID $BUSINESS_PID $BENEFICIARY_PID; exit 0" INT

# Wait for all processes
wait $USER_PID $BUSINESS_PID $BENEFICIARY_PID
