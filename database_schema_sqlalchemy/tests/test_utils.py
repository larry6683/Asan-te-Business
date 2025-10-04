# database_layer/tests/test_utils.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from database_layer.src.public.tables import Base
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

def enable_foreign_keys(dbapi_connection, connection_record):
    """Enable foreign key constraints for SQLite"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_test_session(database_url='sqlite:///:memory:', echo=True):
    """
    Create a test database session with foreign keys enabled.
    Works identically for SQLite and PostgreSQL.
    """
    engine = create_engine(database_url, echo=echo)
    
    # Enable foreign keys for SQLite
    if database_url.startswith('sqlite'):
        event.listen(engine, "connect", enable_foreign_keys)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    return engine, session