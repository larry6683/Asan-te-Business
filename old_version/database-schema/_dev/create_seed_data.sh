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

run_script() {
    local script_name=$1
    echo executing "$script_name"
    PGPASSWORD=$DB_PASSWORD psql -q \
        -h $DB_HOST \
        -U $DB_USER \
        -d $DB_NAME \
        -p $DB_PORT \
        -f "scripts/seed_data/$script_name" \
        --set AUTOCOMMIT=on \
        --set client_min_messages=warning
}

run_script 01_public_seed_data.sql
echo "Seed data for public schema created."
