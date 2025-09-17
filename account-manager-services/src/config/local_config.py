"""
Configuration. Do not commit this file to source control.
"""
config = {
    "database": {
        # "host": "postgres", # use for db integration
        "host": "localhost", # use for mock testing
        "port": 5432,
        "dbname": "postgres",
        "user": "asante_dev",
        "password": "password"
    },
    "logging": {
        "level": "DEBUG",
        "file": "app.log"
    },
    "datasource": "mock" # options: "mock" (for using mock data), "db" (for using database)
}
