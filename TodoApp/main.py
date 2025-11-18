from typing import Annotated
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from fastapi import FastAPI, Depends
import models
from models import Todos
from database import Base, SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,  Depends(get_db)]

@app.get("/")
def read_all(db: db_dependency):
    return db.query(Todos).all()