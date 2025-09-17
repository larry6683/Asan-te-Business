# account-manager-services

## Running the services

1. create venv:
    - `python -m venv venv`
1. activate venv:
    - Windows: `./venv/scripts/activate`
    - Mac: `source ./venv/bin/activate`
1. install packages:
    - `pip install -r requirements.txt`
1. exec codegen
    - `./tools/run_codegen.sh`
1. execute a run script inside the tools/run folder:
    - `./tools/run/te_credit_account_balance.sh` for te_credit_account_balance
    - `./tools/run/run_all.sh` for all services

## Creating docker & running docker containers

- to connect with database make sure to create docker network:
  `docker network create --driver bridge asante-network`
  
### Running with docker compose

- run in detached mode: `docker compose up -d`
  - run only a certain profile: `docker compose --profile dev up -d`
  - if you get an error "no service selected", try specifying a profile.
- stop without removing: `docker compose stop`
- build/rebuild without restart: `docker compose build`
- build & restart: `docker compose up -d --build`
- remove images and containers: `docker compose down --rmi local`
- view all logs: `docker compose logs -f`
- view logs of specific service: `docker compose logs -f create_resource get_resource`
