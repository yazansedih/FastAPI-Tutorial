from fastapi import FastAPI, Depends
from app.routes import tasks, users
from app.auth import get_current_user, router as auth_router

app = FastAPI(
    title="Task Management API",
    description="A simple task management system with user authentication",
    version="1.0.0"
)

# Auth routes (signup/login/logout) - grouped under "Auth"
app.include_router(auth_router, tags=["Auth"])

# User routes - grouped under "Users" (protected)
app.include_router(
    users.router, 
    prefix="/api", 
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

# Task routes - grouped under "Tasks" (protected)
app.include_router(
    tasks.router, 
    prefix="/api", 
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)

@app.get("/")
def root():
    return {"message": "Welcome to Task Management API"}