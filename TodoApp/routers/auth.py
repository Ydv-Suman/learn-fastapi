from datetime import timedelta, datetime, timezone
from typing import Annotated, Optional
from fastapi import  APIRouter, Depends, HTTPException, Request
from starlette import status
from pydantic import BaseModel
from ..database import SessionLocal
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from ..models import Users
from passlib.context import CryptContext # pyright: ignore[reportMissingModuleSource]
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError # pyright: ignore[reportMissingModuleSource]
from fastapi.templating import Jinja2Templates
from pathlib import Path


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRETKEY = '7c2804e7e11c73816347cdf55f0a2bef21ceb073ae70be0c07c054a1e470b4ef'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
Oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token', auto_error=False)

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number:str


class Token(BaseModel):
    access_token: str
    token_type: str

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,  Depends(get_db)]


BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

## Pages ##
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html", {"request":request})

@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse("register.html", {"request":request})



def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id:int, role:str, expire_delta:timedelta):
    encode={'sub':username, 'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRETKEY, algorithm=ALGORITHM)

async def get_current_user(request: Request, token: Optional[str] = Depends(Oauth2_bearer)):
    # Try to get token from Authorization header first
    token_value = token
    
    # If not in header, try to get from cookies (for browser navigation)
    if not token_value:
        token_value = request.cookies.get('access_token')
    
    if not token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    
    try:
        payload = jwt.decode(token_value, SECRETKEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id':user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, 
                Create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=Create_user_request.email,
        username =Create_user_request.username,
        first_name=Create_user_request.first_name,
        last_name=Create_user_request.last_name,
        role=Create_user_request.role,
        hashed_password=bcrypt_context.hash(Create_user_request.password),
        is_active=True,
        phone_number=Create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()



@router.post("/token", response_model=Token)
def login_for_access_token(
                            form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
                            db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

