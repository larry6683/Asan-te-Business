"""
Configuration template. Copy this file to local_config.py and fill in your values.
"""
config = {
    "database": {
        "host": "DB_HOST",
        "port": 0000,
        "dbname": "DB_NAME",
        "username": "DB_USER",
        "password": "DB_PASSWORD"
    },
    "logging": {
        "level": "DEBUG",
        "file": "app.log"
    },
    "datascource": "mock",  # "mock" or "db"
}
