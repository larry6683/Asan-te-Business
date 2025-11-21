#!/bin/bash

# Predefined parameters for local development
# PostgreSQL Configuration
POSTGRES_USER={DB_USER}
POSTGRES_PASSWORD={DB_PASSWORD}
POSTGRES_DB={D}

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin@asante.com
PGADMIN_DEFAULT_PASSWORD=your_admin_password

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