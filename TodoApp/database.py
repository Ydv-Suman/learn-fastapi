from sqlalchemy import create_engine    # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker    # pyright: ignore[reportMissingImports]
from sqlalchemy.ext.declarative import declarative_base  # pyright: ignore[reportMissingImports]

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
