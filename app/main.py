from fastapi import FastAPI, Depends
from app.routes import tasks
from app.auth import get_current_user, router as auth_router

app = FastAPI()

# Auth endpoints
app.include_router(auth_router)

# Protected task routes
app.include_router(tasks.router, dependencies=[Depends(get_current_user)])
