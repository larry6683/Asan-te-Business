import psycopg
from config.config import Config

class DBUtils:
    @staticmethod
    def get_connection():
        return psycopg.connect(**Config.get_database_config(), autocommit=False)
