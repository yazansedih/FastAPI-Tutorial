from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_current_user, hash_password
from app.schemas import UserResponse, UserUpdate
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[UserResponse], summary="Get all users")
def get_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse, summary="Get user by ID")
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put("/users/{user_id}", response_model=UserResponse, summary="Update user")
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.username = updated_user.username
    user.email = updated_user.email
    user.first_name = updated_user.first_name
    user.last_name = updated_user.last_name
    user.age = updated_user.age
    user.password = hash_password(updated_user.password)

    db.commit()
    db.refresh(user)

    return user

@router.delete("/users/{user_id}", summary="Delete user")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"detail": f"User {user.username} deleted successfully"}
