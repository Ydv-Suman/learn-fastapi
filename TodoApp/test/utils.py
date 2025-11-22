import os
# Set testing environment BEFORE any imports that use the database
os.environ["TESTING"] = "1"

from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from sqlalchemy import create_engine, text  # pyright: ignore[reportMissingImports]
from sqlalchemy.pool import StaticPool  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient
from fastapi import status

from ..database import Base
from ..main import app
from ..models import Todos

import pytest  # pyright: ignore[reportMissingImports]


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test_todosapp.db'

engine= create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass = StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'suman', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()   # use testing db otherwise it will delete the everything from original database
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()