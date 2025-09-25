import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# Add the database schema path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_schema_path = os.path.join(os.path.dirname(current_dir), '/new_version/database_schema_sqlalchemy')
if os.path.exists(db_schema_path):
    sys.path.insert(0, db_schema_path)

try:
    from database_layer.models import Base
    from config.config import Config
    SQLALCHEMY_AVAILABLE = True
except ImportError as e:
    print(f"SQLAlchemy not available: {e}")
    SQLALCHEMY_AVAILABLE = False
    Base = None

class DatabaseConnection:
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def initialize(cls):
        """Initialize database connection"""
        if not SQLALCHEMY_AVAILABLE:
            print("SQLAlchemy not available, using mock mode")
            return
            
        if cls._engine is None:
            try:
                # Get database config
                db_config = Config.get_database_config()
                
                # Create connection string
                database_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
                
                # Create engine
                cls._engine = create_engine(database_url)
                cls._SessionLocal = sessionmaker(bind=cls._engine)
                
                print(f"Database initialized: {db_config['host']}:{db_config['port']}/{db_config['dbname']}")
            except Exception as e:
                print(f"Database initialization failed: {e}")
                cls._engine = None
                cls._SessionLocal = None
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Session:
        """Get database session with automatic cleanup"""
        if cls._SessionLocal is None:
            cls.initialize()
        
        if cls._SessionLocal is None:
            raise Exception("Database not available")
            
        session = cls._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_engine(cls):
        """Get database engine"""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
