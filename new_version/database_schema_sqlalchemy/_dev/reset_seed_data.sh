#!/bin/bash

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

echo "Creating seed data for DEVELOPMENT"

run_seed_script() {
    local script_name=$1
    echo executing "$script_name"
    
    # Navigate to project root and run Python equivalent
    cd ..
    python -c "
import sys
sys.path.insert(0, '.')
from database_layer.scripts.seed_data.${script_name%.*} import ${script_name%.*}
${script_name%.*}('postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}')
"
    cd _dev
}

run_migration_script() {
    local script_name=$1
    echo executing "$script_name"
    
    # Navigate to project root and run Python equivalent
    cd ..
    python -c "
import sys
sys.path.insert(0, '.')
from database_layer.scripts.seed_data.public_seed_data import create_seed_data
create_seed_data('postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}')
"
    cd _dev
}

run_seed_script "clear_db_data.sql"
echo "Seed data for all schemas cleared."

run_migration_script "01_public_seed_data.sql"
echo "Seed data for public schema created."

# sleep 10