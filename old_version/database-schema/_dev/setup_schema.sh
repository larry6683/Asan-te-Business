#!/bin/bash

# Script to create initial database for postgres
# AI Helped generate this script - no promises of perfection

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
EXTENSIONS_SCRIPT="migrations/00_initial_schema/01_extensions.sql"

echo "setup_schema for DEVELOPMENT"

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
# check_extension "pg_audit" || true
check_extension "pgcrypto" || true

print_message "extensions installed."

# Install extensions if needed and restart containers
if [ "$EXTENSIONS_INSTALLED" = false ]; then
    echo "Installing missing extensions..."
    
    # Execute the extensions script
    PGPASSWORD=$DB_PASSWORD psql \
        -h $DB_HOST \
        -U $DB_USER \
        -d $DB_NAME \
        -p $DB_PORT \
        -f "$EXTENSIONS_SCRIPT" \
        --set AUTOCOMMIT=on
    
    echo "Restarting Docker containers..."
    # Stop containers with timeout (30 seconds is usually sufficient for PostgreSQL)
    docker stop --time=30 $STACK_NAME-$POSTGRES_CONTAINER
    docker stop --time=15 $STACK_NAME-$PGADMIN_CONTAINER
    
    # Verify containers have actually stopped
    echo "Verifying containers have stopped..."
    while docker ps --filter "name=$STACK_NAME-$POSTGRES_CONTAINER" --filter "status=running" -q | grep -q .; do
        echo "Waiting for PostgreSQL container to stop..."
        sleep 2
    done
    
    while docker ps --filter "name=$STACK_NAME-$PGADMIN_CONTAINER" --filter "status=running" -q | grep -q .; do
        echo "Waiting for pgAdmin container to stop..."
        sleep 2
    done
    
    echo "Starting containers..."
    docker start $STACK_NAME-$POSTGRES_CONTAINER
    docker start $STACK_NAME-$PGADMIN_CONTAINER
    
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

# Execute all SQL scripts in the migrations directory except the extensions script
echo "Setting up the database schema..."

run_script() {
    local script_name=$1
    echo executing "$script_name"
    PGPASSWORD=$DB_PASSWORD psql -q \
        -h $DB_HOST \
        -U $DB_USER \
        -d $DB_NAME \
        -p $DB_PORT \
        -f "migrations/00_initial_schema/$script_name" \
        --set AUTOCOMMIT=on \
        --set client_min_messages=warning
}

run_script "02_create_schemas.sql"
print_message "schemas created."
echo

run_script "03_create_types.sql"
print_message "types created."
echo

run_script "04_create_tables.sql"
print_message "tables created."
echo

run_script "05_create_views.sql"
print_message "views created."
echo

run_script "06_create_functions.sql"
print_message "functions created."
echo

run_script "07_create_procedures.sql"
print_message "procedures created."
echo

run_script "08_create_triggers.sql"
print_message "triggers created."
echo

run_script "09_populate_data.sql"
print_message "data populated."
echo

echo "Database schema setup completed."

# sleep 20