# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    age: int
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    age: int

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True

