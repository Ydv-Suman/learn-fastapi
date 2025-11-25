# import dependencies
from typing import Annotated
from pathlib import Path

from pydantic import BaseModel, Field
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_302_FOUND

from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from fastapi import APIRouter, Depends, HTTPException, Query, status, Path as PathParam, Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..models import Todos
from ..database import Base, SessionLocal, engine
from .auth import get_current_user


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


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



def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

## Pages
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency, user: user_dependency):
    try:
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id==user.get('id')).all()
        return templates.TemplateResponse("todo.html", {"request":request, "todos": todos, "user": user})
    except:
        return redirect_to_login()
    




# Get all todos
@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


# Get todo by id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def filter_with_id(todo_id: Annotated[int, PathParam(gt=0)], user:user_dependency, db: db_dependency):
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
@router.put("/updateTodo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(todo_update: TodoRequest, db:db_dependency, user:user_dependency, todo_id: Annotated[int, PathParam(gt=0)]):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_model.title = todo_update.title
    todo_model.description = todo_update.description
    todo_model.priority = todo_update.priority
    todo_model.complete = todo_update.complete
    db.add(todo_model)
    db.commit()

# Delete todo
@router.delete('/deleteTodo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependency, user:user_dependency, todo_id: Annotated[int, PathParam(gt=0)]):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication  Failed")
    todo_model =db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()