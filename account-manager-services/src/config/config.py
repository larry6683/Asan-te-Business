loaded = False
try:
    from config import local_config as config
    loaded = True
except ImportError:
    pass

class Config:
    @staticmethod
    def get_database_config():
        if not loaded:
            raise ImportError("Configuration not loaded. Ensure local_config.py is available.")
        
        config_dict = config.config["database"]

        return {
            "host": config_dict["host"],
            "port": config_dict["port"],
            "dbname": config_dict["dbname"],
            "user": config_dict["user"],
            "password": config_dict["password"]
        }
    
    @staticmethod
    def get_logging_config():
        if not loaded:
            return False
        
        return config.config["logging"]

    @staticmethod
    def use_db():
        if not loaded:
            raise ImportError("Configuration not loaded. Ensure local_config.py is available.")
        
        if config.config["datasource"] == "mock":
            return False
        elif config.config["datasource"] == "db":
            return True
        else:
            raise ValueError("Invalid datasource configuration. Expected 'mock' or 'db'.")
