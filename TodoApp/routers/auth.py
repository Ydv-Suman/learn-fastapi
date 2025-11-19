from fastapi import  APIRouter

router = APIRouter()

@router.get('/auth')
def getuser():
    return {'user': 'authenticated'}