#!/bin/bash

echo "========================================"
echo "Starting All gRPC Services"
echo "========================================"
echo ""

# Function to load environment variables
load_env() {
    if [ -f .env ]; then
        echo "Loading environment from .env file..."
        # Use set -a to export all variables
        set -a
        source .env
        set +a
        echo "✓ Environment loaded"
    else
        echo "✗ No .env file found!"
        # Load the created file
        set -a
        source .env
        set +a
    fi
}

# Load environment variables
load_env

# Set PYTHONPATH
export PYTHONPATH="$PWD/src"

# Display loaded configuration
echo ""
echo "Configuration Loaded:"
echo "===================="
echo "Database:"
echo "  Host: ${DB_HOST:-NOT SET}"
echo "  Port: ${DB_PORT:-NOT SET}"
echo "  Database: ${DB_NAME:-NOT SET}"
echo "  User: ${DB_USER:-NOT SET}"
echo "  Password: ${DB_PASSWORD:+[SET]}"
echo ""
echo "Service Ports:"
echo "  User Service:        ${USER_SERVICE_PORT:-NOT SET}"
echo "  Business Service:    ${BUSINESS_SERVICE_PORT:-NOT SET}"
echo "  Beneficiary Service: ${BENEFICIARY_SERVICE_PORT:-NOT SET}"
echo "  Analytics Service:   ${ANALYTICS_SERVICE_PORT:-NOT SET}"
echo ""

# Test database connection first
echo "Testing database connection..."
python test_db_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Database connection test failed!"
    echo "  Please check your database configuration and ensure PostgreSQL is running."
    echo ""
    echo "To fix this:"
    echo "1. Check if PostgreSQL is running: sudo service postgresql status"
    echo "2. Verify credentials in .env file"
    echo "3. Ensure database exists: psql -U ${DB_USER} -d ${DB_NAME} -h ${DB_HOST}"
    exit 1
fi

echo ""
echo "Starting services..."
echo ""

# Start services in background
echo "Starting User Service (port ${USER_SERVICE_PORT})..."
python src/services/user/server.py &
USER_PID=$!

sleep 2

echo "Starting Business Service (port ${BUSINESS_SERVICE_PORT})..."
python src/services/business/server.py &
BUSINESS_PID=$!

sleep 2

echo "Starting Beneficiary Service (port ${BENEFICIARY_SERVICE_PORT})..."
python src/services/beneficiary/server.py &
BENEFICIARY_PID=$!

sleep 2

echo "Starting Analytics Service (port ${ANALYTICS_SERVICE_PORT})..."
python src/services/analytics/server.py &
ANALYTICS_PID=$!

sleep 2

echo ""
echo "========================================"
echo "✓ All services started!"
echo "========================================"
echo ""
echo "Services running on:"
echo "  User Service:        localhost:${USER_SERVICE_PORT}"
echo "  Business Service:    localhost:${BUSINESS_SERVICE_PORT}"
echo "  Beneficiary Service: localhost:${BENEFICIARY_SERVICE_PORT}"
echo "  Analytics Service:   localhost:${ANALYTICS_SERVICE_PORT}"
echo ""
echo "Database:"
echo "  Host: ${DB_HOST}"
echo "  Port: ${DB_PORT}"
echo "  Database: ${DB_NAME}"
echo "  User: ${DB_USER}"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap Ctrl+C to kill all services
trap "echo ''; echo 'Stopping services...'; kill $USER_PID $BUSINESS_PID $BENEFICIARY_PID $ANALYTICS_PID 2>/dev/null; exit 0" INT

# Wait for all processes
wait $USER_PID $BUSINESS_PID $BENEFICIARY_PID $ANALYTICS_PID