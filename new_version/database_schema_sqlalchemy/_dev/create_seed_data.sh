#!/bin/bash

# Predefined parameters for local development
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="asante_dev"
DB_PASSWORD="password"

echo "Creating seed data for DEVELOPMENT"

# Navigate to parent directory to run Python seed data
cd ..

echo "executing public_seed_data.py"

# Run the Python seed data creation
python -c "
import sys
sys.path.insert(0, '.')
from database_layer.scripts.seed_data.public_seed_data import create_seed_data
create_seed_data('postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}')
"

if [ $? -eq 0 ]; then
    echo "Seed data for public schema created."
else
    echo "Error: Failed to create seed data"
    exit 1
fi

# Navigate back to _dev directory
cd _dev