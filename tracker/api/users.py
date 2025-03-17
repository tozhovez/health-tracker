from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.dbclient import get_db, refresh_db
from schemas.users import UserCreate, UserUpdate, UserResponse
from services.user_service import UserService

users_router = APIRouter()

@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    return await UserService.create_user(db, user_data)

@users_router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all users with pagination"""
    return await UserService.get_user(db, skip=skip, limit=limit)

@users_router.get("/{user_uuid}", response_model=UserResponse)
async def read_user(user_uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific user by UUID"""
    user = await UserService.get_user(db, user_uuid)
    if user is None or len(user) <= 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user.pop()

@users_router.patch("/{user_uuid}", response_model=UserResponse)
async def update_user(user_uuid: UUID, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    """Update a user"""
    user = await UserService.update_user(db, user_uuid, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.delete("/{user_uuid}", response_model=UserResponse)
async def delete_user(user_uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a user"""
    user = await UserService.delete_user(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await refresh_db()
    return user
