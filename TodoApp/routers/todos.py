# import dependencies
from typing import Annotated

from pydantic import BaseModel, Field
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from fastapi import APIRouter, Depends, HTTPException, Query, status, Path

from models import Todos
from database import Base, SessionLocal, engine
from .auth import get_current_user


router = APIRouter()


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,  Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



# Request model
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# Get all todos
@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


# Get todo by id
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def filter_with_id(todo_id: Annotated[int, Path(gt=0)], user:user_dependency, db: db_dependency):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# Create todo
@router.post("/createTodo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, todo_add: TodoRequest, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    todo_model = Todos(**todo_add.dict(), owner_id=user.get('id'))  # pyright: ignore[reportDeprecated]
    db.add(todo_model)
    db.commit()


# Update todo
@router.put("/todo/updateTodo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(todo_update: TodoRequest, db:db_dependency, user:user_dependency, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")
    todo_model.title = todo_update.title
    todo_model.description = todo_update.description
    todo_model.priority = todo_update.priority
    todo_model.complete = todo_update.complete
    db.add(todo_model)
    db.commit()

# Delete todo
@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependency, user:user_dependency, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    todo_model =db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()