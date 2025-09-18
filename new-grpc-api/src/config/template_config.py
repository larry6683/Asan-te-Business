"""
Configuration template. Copy this file to local_config.py and fill in your values.
"""
config = {
    "database": {
        "host": "DB_HOST",
        "port": 5432,
        "dbname": "DB_NAME",
        "user": "DB_USER",
        "password": "DB_PASSWORD"
    },
    "logging": {
        "level": "DEBUG",
        "file": "app.log"
    },
    "datasource": "mock"  # "mock" or "db"
}
