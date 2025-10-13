# Dev Setup for SQLAlchemy Database Project with Docker Container

## Files

- **`.env`** - stores default configuration for a docker env setup
- **`template.env`** - template for creating your .env file  
- **`compose.yaml`** - docker configuration for PostgreSQL instance with pgAdmin
- **`setup-postgres-dev.sh`** - sets up postgres/pgadmin container with configuration from .env file
- **`setup_network.sh`** - creates Docker network for containers
- **`setup_schema.sh`** - creates database schema using SQLAlchemy models  
- **`create_seed_data.sh`** - creates test data using Python scripts
- **`reset_seed_data.sh`** - clears and recreates test data
- **`init-scripts/01-privileges.sql`** - database user privileges for Docker initialization

## Prerequisites

### Install Required Software

1. **Docker Desktop**
   - Download and install Docker Desktop
   - Restart computer after installing for the first time
   - Start Docker Desktop

2. **PostgreSQL CLI Tools** (optional, for troubleshooting)
   - Download installer from: `https://www.enterprisedb.com/downloads/postgres-postgresql-downloads`
   - Choose to only install CLI tools
   - **Windows users**: Add postgres bin folder to your PATH environment variable:
     - `%PROGRAMFILES%\Postgresql\17\bin`

3. **Python 3.8+** with pip
   - Your SQLAlchemy database layer requires Python

## Setup Steps

### 1. Initial Docker Setup

```bash
# Create Docker network (run once)
bash ./setup_network.sh

# OR manually:
docker network create --driver bridge asante-network
```

### 2. Create Environment File

```bash
# Copy template and customize
cp template.env .env

# Edit .env with your preferred settings
# Default values work fine for development
```

**Sample .env contents:**
```
POSTGRES_USER=asante_dev
POSTGRES_PW=password
POSTGRES_DB=postgres
PGLADMIN_MAIL=admin@admin.com
PGLADMIN_PW=password
```

### 3. Start Database Containers  

```bash
# From the _dev directory
bash ./setup-postgres-dev.sh
```

This will:
- Check if Docker is running
- Validate your .env file
- Start PostgreSQL and pgAdmin containers
- Set up database privileges

### 4. Create Database Schema

```bash
# From the _dev directory  
bash ./setup_schema.sh
```

This will:
- Check PostgreSQL extensions (pgcrypto)
- Create all tables using SQLAlchemy models
- Populate reference data (user types, business sizes, causes, etc.)
- Create test seed data (3 businesses with users)

## Database Access

### pgAdmin Web Interface

1. Navigate to `http://localhost:5050`
2. Login with credentials from your .env file:
   - **Email**: `admin@admin.com` 
   - **Password**: `password`
3. Add server connection:
   - **General tab**: Name = `postgres` (or anything you prefer)
   - **Connection tab**:
     - Host name/address: `postgres`
     - Port: `5432`
     - Username: `asante_dev` 
     - Password: `password`
     - Toggle "Save password" on

### Verify Installation

1. In pgAdmin, expand: `postgres > databases > postgres > schemas > public > tables`
2. You should see all database tables listed
3. Run test query: `SELECT * FROM app_user` - should return test users

## Data Management

### Create Test Data

```bash
# From project root
./_dev/create_seed_data.sh
```

This creates:
- **Eco Solutions Inc.** (Seattle, WA) - Environmental causes
- **Tech Innovations Ltd** (San Francisco, CA) - Education causes  
- **Local Harvest Co-op** (Portland, OR) - Community causes
- 4 users per business (2 admins, 2 team members)
- Social media profiles, cause preferences, shops, impact links

### Reset Test Data

```bash
# From project root  
./_dev/reset_seed_data.sh
```

This will:
1. Clear existing test data
2. Recreate fresh test data
3. Use this if you encounter data conflicts

### Verify Data Quickly

Execute in pgAdmin query tool:
```sql
-- Check users
SELECT * FROM app_user;

-- Check businesses  
SELECT * FROM business;

-- Check business users
SELECT b.business_name, au.email 
FROM business b
JOIN business_user bu ON b.business_id = bu.business_id
JOIN app_user au ON bu.app_user_id = au.app_user_id;
```

## Troubleshooting

### Container Issues

```bash
# Check container status
docker ps

# Restart containers if needed
docker compose restart

# View container logs
docker logs postgres
docker logs pgadmin
```

### Extension Issues

If you see pgcrypto errors:
1. Execute in pgAdmin query tool: `CREATE EXTENSION IF NOT EXISTS pgcrypto;`
2. Restart containers: `docker compose restart`
3. Re-run setup: `bash ./setup_schema.sh`

### Connection Issues

- Ensure Docker containers are running: `docker ps`
- Check Docker Desktop is started
- Verify .env file has correct credentials
- Wait 30 seconds after starting containers for PostgreSQL to be ready

### Python/Import Issues

- Ensure you're running scripts from the correct directory
- For `setup_schema.sh` and data scripts: run from project root
- Python needs to find your `database_layer` package

## Advanced Usage

### Custom Database Connection

Scripts use default connection from .env, but you can override:

```bash
# Set custom database URL in script or environment
export DATABASE_URL="postgresql://user:pass@host:port/database"
```

### Development Workflow

1. **One-time setup**: `setup-postgres-dev.sh`
2. **Schema changes**: `setup_schema.sh` (recreates all tables)
3. **Data reset**: `reset_seed_data.sh` (for clean test data)
4. **Add test data**: `create_seed_data.sh` (if no seed data exists)

### pgAdmin Preferences  

Customize pgAdmin interface:
1. Go to pgAdmin home
2. Click Files → Preferences  
3. Go to Misc → User Interface
4. Set Theme to "Dark" (optional)

## Architecture Notes

This setup uses:
- **PostgreSQL** for the database
- **SQLAlchemy ORM** instead of raw SQL migrations
- **Python scripts** for data population instead of SQL scripts
- **Docker** for consistent development environment
- **pgAdmin** for database administration UI

The SQLAlchemy models replace the original SQL table definitions while maintaining the same database structure and relationships.