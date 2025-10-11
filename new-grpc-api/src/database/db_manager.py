# Import config first to set up paths
from config.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

class DatabaseManager:
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def initialize(cls):
        if cls._engine is None:
            database_url = Config.get_database_url()
            cls._engine = create_engine(database_url, echo=False)
            cls._SessionLocal = sessionmaker(bind=cls._engine)
            print(f'Database connected: {Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}')
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Session:
        if cls._SessionLocal is None:
            cls.initialize()
        
        session = cls._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
