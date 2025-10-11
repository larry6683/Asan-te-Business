#!/bin/bash

# NOTE: This script is intended for development purposes only.
# It is not recommended for production use.
# Generated with AI assistance. No promises of perfection.

# PostgreSQL and pgAdmin Development Environment Setup Script
# Compatible with Linux, macOS, and Windows (Git Bash/WSL)

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display messages
print_message() {
  echo -e "${GREEN}==>${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}WARNING:${NC} $1"
}

print_error() {
  echo -e "${RED}ERROR:${NC} $1"
}

# Check if Docker is installed
check_docker() {
  if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    echo "Visit https://docs.docker.com/get-docker/ for installation instructions."
    exit 1
  fi
  
  if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running or you don't have permission to use Docker."
    echo "Please start Docker and make sure you have the necessary permissions."
    exit 1
  fi
}

# Check if Docker Compose is available
check_docker_compose() {
  if ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not available. Please install Docker Compose."
    echo "Visit https://docs.docker.com/compose/install/ for installation instructions."
    exit 1
  fi
}

# Check if environment file exists
check_env_file() {
  if [ ! -f .env ]; then
    print_error ".env file not found. Please create an .env file before running this script."
    echo "You can copy template.env to .env and modify it with your preferred credentials."
    exit 1
  else
    print_message ".env file found. Using existing configuration."
  fi
}

# Check if Docker Compose file exists
check_compose_file() {
  if [ ! -f compose.yaml ]; then
    print_error "compose.yaml file not found. Please create a compose.yaml file before running this script."
    exit 1
  else
    print_message "compose.yaml file found."
    
    # Check if the compose file has the minimal required services
    if ! grep -q "postgres:" compose.yaml || ! grep -q "pgadmin:" compose.yaml; then
      print_warning "The existing compose.yaml file might not have both postgres and pgadmin services."
      echo "Please check it manually to ensure it has both services configured correctly."
    fi
  fi
}

# Create the initialization scripts directory
create_init_scripts_dir() {
  if [ ! -d init-scripts ]; then
    print_message "Creating directory for initialization scripts..."
    mkdir -p init-scripts
    print_message "Directory created: init-scripts/"
    
    # Create a minimal initialization script with grants only
    if [ ! -f "init-scripts/01-privileges.sql" ]; then
      print_message "Creating initialization script for privileges..."
      cat > init-scripts/01-privileges.sql << EOF
-- privileges for default user in development environment

-- This script will be executed when the PostgreSQL container is first created

-- Grant comprehensive privileges to the default user
-- First, grant all privileges on database
GRANT ALL PRIVILEGES ON DATABASE \${POSTGRES_DB} TO \${POSTGRES_USER};

-- Connect to the specific database to grant schema-level permissions
\connect \${POSTGRES_DB}

-- Make user a superuser for development purposes
-- This allows full control over all database objects
ALTER USER \${POSTGRES_USER} WITH SUPERUSER;

-- Grant permissions to create schemas
GRANT CREATE ON DATABASE \${POSTGRES_DB} TO \${POSTGRES_USER};

-- For public schema (created by default)
GRANT ALL PRIVILEGES ON SCHEMA public TO \${POSTGRES_USER};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \${POSTGRES_USER};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \${POSTGRES_USER};
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO \${POSTGRES_USER};
GRANT ALL PRIVILEGES ON ALL PROCEDURES IN SCHEMA public TO \${POSTGRES_USER};
GRANT ALL PRIVILEGES ON ALL TYPES IN SCHEMA public TO \${POSTGRES_USER};

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON FUNCTIONS TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON PROCEDURES TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TYPES TO \${POSTGRES_USER};

-- Grant specific privileges needed for triggers and stored procedures
GRANT TRIGGER ON ALL TABLES IN SCHEMA public TO \${POSTGRES_USER};
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO \${POSTGRES_USER};
GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA public TO \${POSTGRES_USER};

-- Ensure user has privileges for future triggers
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT TRIGGER ON TABLES TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT EXECUTE ON FUNCTIONS TO \${POSTGRES_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT EXECUTE ON PROCEDURES TO \${POSTGRES_USER};

-- Grant usage on all sequences (for serial/identity columns)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO \${POSTGRES_USER};
EOF
      print_message "Privileges initialization script created."
    fi
  else
    print_message "init-scripts directory already exists."
  fi
}

# Start the containers
start_containers() {
  print_message "Starting PostgreSQL and pgAdmin containers..."
  docker compose up -d
  
  if [ $? -eq 0 ]; then
    print_message "Containers started successfully!"
  else
    print_error "Error starting containers. Please check the Docker Compose file and try again."
    exit 1
  fi
}

# Print usage information
print_usage_info() {
  echo
  print_message "PostgreSQL and pgAdmin are now ready for use!"
  echo
  echo "PostgreSQL is available at localhost:5432"
  echo "  • Username: as specified in your .env file (POSTGRES_USER)"
  echo "  • Password: as specified in your .env file (POSTGRES_PW)"
  echo "  • Database: as specified in your .env file (POSTGRES_DB)"
  echo
  echo "pgAdmin is available at http://localhost:5050"
  echo "  • Email: as specified in your .env file (PGADMIN_MAIL)"
  echo "  • Password: as specified in your .env file (PGADMIN_PW)"
  echo
  echo "To configure pgAdmin to connect to your PostgreSQL database:"
  echo "  1. Log in to pgAdmin"
  echo "  2. Right-click on 'Servers' and select 'Create' > 'Server...'"
  echo "  3. In the 'General' tab, enter a name for your server (e.g., 'Local Development')"
  echo "  4. In the 'Connection' tab, enter:"
  echo "     • Host name/address: postgres"
  echo "     • Port: 5432"
  echo "     • Username and Password: as specified in your .env file"
  echo "  5. Click 'Save'"
  echo
  echo "To stop the containers:"
  echo "  docker compose stop"
  echo
  echo "To stop and remove the containers (data will be preserved in volumes):"
  echo "  docker compose down"
  echo
  echo "To stop and remove the containers along with the volumes (this will delete all data):"
  echo "  docker compose down -v"
  echo
}

# Main execution
main() {
  print_message "Setting up PostgreSQL and pgAdmin development environment..."
  
  check_docker
  check_docker_compose
  check_env_file
  check_compose_file
  create_init_scripts_dir
  
  # Ask if the user wants to start the containers now
  read -p "Do you want to start the containers now? (y/n): " start_now
  if [[ $start_now =~ ^[Yy]$ ]]; then
    start_containers
    print_usage_info
  else
    print_message "Setup completed without starting containers."
    echo "To start the containers later, run: docker compose up -d"
  fi
}

# Run the main function
main

echo setup complete.
# sleep 7