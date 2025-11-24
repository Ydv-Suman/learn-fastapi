import time
from uu import decode

from pydantic import Secret
from .utils import *
from ..routers.auth import authenticate_user, get_db, create_access_token, SECRETKEY, ALGORITHM, get_current_user
from fastapi import HTTPException, status
from jose import jwt  # pyright: ignore[reportMissingModuleSource]
from datetime import timedelta
import pytest  # pyright: ignore[reportMissingImports]
from TodoApp.routers import auth

app.dependency_overrides[get_db] = override_get_db

def test_authenticateUser(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existing_user = authenticate_user('wrongUserName', 'testpassword', db)
    assert non_existing_user is False

    wrong_password_user = authenticate_user(test_user.username, 'falsepassword', db)
    assert wrong_password_user is False

# test for create access token
def test_create_access_token():
    username='testuser'
    user_id=1
    role='user'
    expires_delta=timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM], options={'verify_signature': False})
    assert decoded_token['sub'] == username
    assert decoded_token['id']==user_id
    assert decoded_token['role']==role


# test for get current user valid token
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRETKEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'id': 1, 'role': 'admin'}  # Missing 'sub' field
    token = jwt.encode(encode, SECRETKEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate user.'