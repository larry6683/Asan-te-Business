#!/bin/bash

# Script to create initial database for postgres using SQLAlchemy
# Updated to use SQLAlchemy models instead of SQL migration files

GREEN='\033[0;32m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${GREEN}==>${NC} $1"
}

# Predefined parameters for local development
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="asante_dev"
DB_PASSWORD="password"
STACK_NAME="postgres_dev"
POSTGRES_CONTAINER="postgres"
PGADMIN_CONTAINER="pgadmin"

echo "setup_schema for DEVELOPMENT using SQLAlchemy"

# Check if required extensions are installed
echo "Checking for required extensions..."
EXTENSIONS_INSTALLED=true

check_extension() {
    local ext_name=$1
    echo "Checking for extension: $ext_name"
    
    # Query PostgreSQL to check if the extension exists and is installed
    INSTALLED=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -p $DB_PORT -t -c "SELECT COUNT(*) FROM pg_extension WHERE extname = '$ext_name';")
    
    # Trim whitespace from result
    INSTALLED=$(echo $INSTALLED | xargs)
    
    if [ "$INSTALLED" -eq "0" ]; then
        echo "Extension $ext_name is NOT installed"
        EXTENSIONS_INSTALLED=false
        return 1
    else
        echo "Extension $ext_name is already installed"
        return 0
    fi
}

# Check for required extensions
check_extension "pgcrypto" || true

print_message "extensions checked."

# Install extensions if needed and restart containers
if [ "$EXTENSIONS_INSTALLED" = false ]; then
    echo "Installing missing extensions..."
    
    # Install pgcrypto extension directly
    PGPASSWORD=$DB_PASSWORD psql \
        -h $DB_HOST \
        -U $DB_USER \
        -d $DB_NAME \
        -p $DB_PORT \
        -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;" \
        --set AUTOCOMMIT=on
    
    echo "Restarting Docker containers..."
    # Stop containers with timeout (30 seconds is usually sufficient for PostgreSQL)
    docker stop --time=30 $STACK_NAME-$POSTGRES_CONTAINER
    docker stop --time=15 $STACK_NAME-$PGLADMIN_CONTAINER
    
    # Verify containers have actually stopped
    echo "Verifying containers have stopped..."
    while docker ps --filter "name=$STACK_NAME-$POSTGRES_CONTAINER" --filter "status=running" -q | grep -q .; do
        echo "Waiting for PostgreSQL container to stop..."
        sleep 2
    done
    
    while docker ps --filter "name=$STACK_NAME-$PGLADMIN_CONTAINER" --filter "status=running" -q | grep -q .; do
        echo "Waiting for pgAdmin container to stop..."
        sleep 2
    done
    
    echo "Starting containers..."
    docker start $STACK_NAME-$POSTGRES_CONTAINER
    docker start $STACK_NAME-$PGLADMIN_CONTAINER
    
    echo "Waiting for PostgreSQL to be ready..."
    # Wait for PostgreSQL to become available
    max_attempts=30
    counter=0
    echo "Waiting for PostgreSQL to accept connections..."
    while ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -p $DB_PORT -c "SELECT 1" >/dev/null 2>&1; do
        counter=$((counter+1))
        if [ $counter -ge $max_attempts ]; then
            echo "PostgreSQL did not become available in time. Exiting."
            exit 1
        fi
        echo "Waiting... ($counter/$max_attempts)"
        sleep 2
    done
    
    echo "PostgreSQL is ready."
fi

# Setup database schema using SQLAlchemy instead of SQL migration files
echo "Setting up the database schema using SQLAlchemy..."

# Navigate to parent directory and run setup_database.py
cd ..

# Check if setup_database.py exists in current directory
if [ -f "setup_database.py" ]; then
    echo "Running setup_database.py..."
    python setup_database.py
elif [ -f "database_layer/setup_database.py" ]; then
    echo "Running database_layer/setup_database.py..."
    python database_layer/setup_database.py
else
    echo "Error: Could not find setup_database.py"
    echo "Looked in current directory and database_layer/ subdirectory"
    exit 1
fi

if [ $? -eq 0 ]; then
    print_message "SQLAlchemy schema setup completed successfully!"
    echo
    print_message "What was created:"
    echo "  - All SQLAlchemy tables"
    echo "  - Reference data (user types, business sizes, causes, etc.)"
    echo "  - Test seed data (3 businesses with users)"
    echo "  - Hash functions are working"
else
    echo "Error: Database schema setup failed"
    exit 1
fi

echo "Database schema setup completed."

# Navigate back to _dev directory
cd _dev