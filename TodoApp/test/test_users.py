from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import  status


app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# test for get user
def test_get_user(test_user):
    response = client.get('/user/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] =='sumantest'
    assert response.json()['email'] =='sumantest@gmail.com'
    assert response.json()['first_name'] =='Sumantest'
    assert response.json()['last_name'] =='Yadavtest'
    assert response.json()['role'] =='admin'
    assert response.json()['phone_number'] =='1(111)111-1111'


# test for changing password
def test_change_password_success(test_user):
    response = client.put("/user/changePassword", json={"password": "testpassword", "new_password": "new_test_password"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

# test for changing password that is failed
def test_change_password_fail(test_user):
    response = client.put("/user/changePassword", json={"password": "password", "new_password": "new_test_password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

# test to change phone number
def test_change_phone_number_success(test_user):
    response = client.put('/user/updatePhoneNumber', params={"phone_number": "1(222)222-2222"})
    assert response.status_code == status.HTTP_204_NO_CONTENT