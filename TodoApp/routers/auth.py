from typing import Annotated
from fastapi import  APIRouter, Depends
from starlette import status
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from models import Users
from passlib.context import CryptContext # pyright: ignore[reportMissingModuleSource]
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,  Depends(get_db)]


def authnicate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post('/auth', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, 
                Create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=Create_user_request.email,
        username =Create_user_request.username,
        first_name=Create_user_request.first_name,
        last_name=Create_user_request.last_name,
        role=Create_user_request.role,
        hashed_password=bcrypt_context.hash(Create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()





@router.post("/token")
def login_for_access_token(
                            form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
                            db:db_dependency):
    user = authnicate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    return "Successful Authentication"