# Dev Setup for testing database project with a docker container

## files

- `.env`
  - stores default configuration for a docker env setup
- `compose.yaml`
  - the docker configuration for setting up your postgres instance with pgadmin
- `setup_script.sh`
  - sets up a postgres/pgadmin container with configuration defined in a .env file.

## prelim setup

On windows you can just execute the script. If on mac/linux you will need to set execution priv on the script or run it with bash

  1. priv method
    - `chmod +x {script_name}.sh`
    - `./setup-postgres-dev.sh`
  2. bash method
    - `bash ./setup-postgres-dev.sh`
  3. install psql cli
    - download installer from  
    `https://www.enterprisedb.com/downloads/postgres-postgresql-downloads`
    - choose to only install cli tools
    - on windows you will need to add postgres bin folder to your PATH environment variable. something like this
      - `%PROGRAMFILES%\Postgresql\17\bin`

## setup

  1. install docker.
    - I'm not going to describe this.
    - restart computer after installing for the first time
    - start docker desktop
  1. execute: `docker network create --driver bridge asante-network`
  1. create .env file. sample below.
  1. make you working dir _dev: `cd _dev`
  1. run `./_dev/setup_postgres_dev.sh`
    - you may need to restart container for extension installation
  1. go back to project root dir, exec if needed: `cd ..`
  1. run schema setup: `./_dev/setup_schema.sh`
  1. follow the logging in + connection instructions below!  

### sample .env

`
POSTGRES_USER=asante_dev
POSTGRES_PW=password
POSTGRES_DB=postgres
PGADMIN_MAIL=admin@admin.com
PGADMIN_PW=password
`

## logging in + connecting to pgadmin/database

1. connect to pgadmin by going to `localhost:5050`
1. login with values set in your .env file. i.e.
    - username: `admin@admin.com`
    - password: `password`
1. Click on server -> add server in pgadmin, fill in connection info as follows:
    - general tab
      - name: `postgres` (or anything you like, asante is more flavorful)
    - connection:
      - Host name/address: `postgres`
      - Port: `5432`
      - Username: `asante_dev`
      - password: `password`
      - toggle save password on

## Verification

1. expand postgres -> databases -> postgres -> schemas -> public -> tables
    - you should see all the tables here.

## Populate seed data

1. there may be a bug with the setup db script, execute this in pgadmin query tool and restart your containers
    - `CREATE EXTENSION IF NOT EXISTS pgcrypto;`
1. if you have not yet restarted your containers, do so now to ensure extensions are installed.
1. execute from root dir: `./_dev/create_seed_data.sh`
1. if you continuously run into errors - consider running `./_dev/reset_seed_data.sh`
1. if you need to reset your seed data for testing, consider running the script mentioned in previous step.

### Verify seed data quickly

  1. exec `select * from app_user` in the query tool. you should have results.
    - you can also query other tables

## Preferences

you can directly modify the pgadmin configuration by:

1. go to pgadmin home
1. click on files -> preferences
1. go to misc -> User Interface
1. find "Theme" and set it to "Dark"
