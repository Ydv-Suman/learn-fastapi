from starlette.status import HTTP_204_NO_CONTENT
from .utils import *
from ..routers.admin import get_db, get_current_user
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/admin/todo/")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{'complete':False, 'title':'Learn to code!', 'description':'Need to learn everyday', 'priority': 5, 'id':1, 'owner_id':1}]

# Test admin to delete todo
def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db=TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model is None

# delete todo not found
def test_admin_delete_todo_not_found(test_todo):
    response = client.delete('/admin/todo/999')
    assert response.json()=={'detail':'Not Found'}