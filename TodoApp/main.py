# import dependencies
from pathlib import Path
from fastapi import FastAPI, Request, status, HTTPException
from .models import Base
from .database import engine
from fastapi.staticfiles import StaticFiles
from .routers import auth, todos, admin, users
from .routers.auth import get_current_user
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Get the directory where this file is located
BASE_DIR = Path(__file__).parent
#templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")))
@app.get("/")
async def root_redirect(request: Request):
    try:
        token = request.cookies.get('access_token')
        await get_current_user(request, token=token)
        return RedirectResponse("/todos/todo-page", status_code=status.HTTP_302_FOUND)
    except HTTPException:
        return RedirectResponse("/auth/login-page", status_code=status.HTTP_302_FOUND)



@app.get("/healthy")
def health_check():
    return {'status': 'healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
