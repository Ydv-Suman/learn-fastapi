from sqlalchemy import create_engine  # pyright: ignore[reportMissingImports]
from sqlalchemy.pool import StaticPool  # pyright: ignore[reportMissingImports]
from ..database import Base
from sqlalchemy.orm import sessionmaker  # pyright: ignore[reportMissingImports]
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:suman123@localhost/TestTodoDatabase'

engine= create_engine(SQLALCHEMY_DATABASE_URL, poolclass = StaticPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.creater_all(bind=engine)