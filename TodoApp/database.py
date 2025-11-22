from sqlalchemy import create_engine    # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker    # pyright: ignore[reportMissingImports]
from sqlalchemy.ext.declarative import declarative_base  # pyright: ignore[reportMissingImports]

import os
from dotenv import load_dotenv


# Determine which database to use based on environment

# For sqlite
if os.getenv("TESTING"):
    # Use SQLite for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"  # to connect sqlite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}   # connect arg is only for sqlite
    )
else:
    # Use PostgreSQL for production/development
    load_dotenv()
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


"""
for MySQL
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root/suman123@127.0.0.1:3306/TodoApplicationDatabase'  #password@location/database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
