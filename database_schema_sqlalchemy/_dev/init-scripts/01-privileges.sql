-- privileges for default user in development environment
-- Note: This uses postgres default database during initialization

-- Grant all privileges on the default postgres database
GRANT ALL PRIVILEGES ON DATABASE postgres TO asante_dev;

-- Connect to postgres database
\c postgres

-- Make user a superuser for development purposes
ALTER USER asante_dev WITH SUPERUSER;

-- Grant permissions on public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO asante_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO asante_dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO asante_dev;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO asante_dev;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO asante_dev;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO asante_dev;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO asante_dev;
