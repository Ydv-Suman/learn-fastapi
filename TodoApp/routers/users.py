# import dependencies
from email.policy import default
from typing import Annotated

from pydantic import BaseModel, Field
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from fastapi import APIRouter, Depends, HTTPException, Query, status, Path

from ..models import Todos, Users
from ..database import Base, SessionLocal, engine
from .auth import get_current_user

from passlib.context import CryptContext  # pyright: ignore[reportMissingModuleSource]

router = APIRouter(
    prefix='/user',
    tags=['user']
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
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Path(min_length=6)



@router.get("/", status_code=status.HTTP_200_OK)
def get_user(user:user_dependency, db:db_dependency):
    if user is None :
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/changePassword', status_code=status.HTTP_204_NO_CONTENT)
def Change_password(user: user_dependency, db:db_dependency, user_verification:UserVerification):
    if user is None :
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id== user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

# update user with phone number
@router.put('/updatePhoneNumber', status_code=status.HTTP_204_NO_CONTENT)
def update_phone_number(user:user_dependency, db:db_dependency, phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()