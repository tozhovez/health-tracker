from typing import List
from uuid import UUID
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.dbclient import get_db, refresh_db
from schemas.sleep_activity import SleepActivityCreate, SleepActivityUpdate, SleepActivityResponse
from services.sleep_activity_service import SleepActivityService

sleep_activity_router = APIRouter()

@sleep_activity_router.post("/", response_model=SleepActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_sleep_activity(sleep_activity_data: SleepActivityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new sleep activity record"""
    result =  await SleepActivityService.create_sleep_activity(db, sleep_activity_data)
    if result:
        await refresh_db()
    return result

@sleep_activity_router.get("/{user_uuid}", response_model=List[SleepActivityResponse])
async def read_sleep_activity_by_user(
    user_uuid: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all sleep activities for a specific user"""
    return await SleepActivityService.get_sleep_activity(db, user_uuid, skip=skip, limit=limit)

@sleep_activity_router.get("/{user_uuid}/{date}", response_model=List[SleepActivityResponse])
async def read_sleep_activity_by_user_by_date(
    user_uuid: UUID,
    date: datetime | date,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific sleep activity by user UUID and activity date"""
    sleep_activity = await SleepActivityService.get_sleep_activity(db, user_uuid, start_time=date)
    if sleep_activity is None or len(sleep_activity) <= 0:
        raise HTTPException(status_code=404, detail="Sleep activity not found")
    return sleep_activity

@sleep_activity_router.patch("/user/{user_uuid}/update", response_model=SleepActivityResponse)
async def update_sleep_activity(
    user_uuid: UUID,
    start_time: datetime = Query(...),
    sleep_activity_data: SleepActivityUpdate = None,
    db: AsyncSession = Depends(get_db)
):
    """Update a sleep activity"""
    sleep_activity = await SleepActivityService.update_sleep_activity(db, user_uuid, start_time, sleep_activity_data)
    if sleep_activity is None:
        raise HTTPException(status_code=404, detail="Sleep activity not found")
    await refresh_db()
    return sleep_activity

@sleep_activity_router.delete("/user/{user_uuid}/delete", response_model=SleepActivityResponse)
async def delete_sleep_activity(
    user_uuid: UUID,
    start_time: datetime = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Delete a sleep activity"""
    sleep_activity = await SleepActivityService.delete_sleep_activity(db, user_uuid, start_time)
    if sleep_activity is None:
        raise HTTPException(status_code=404, detail="Sleep activity not found")
    await refresh_db()
    return sleep_activity
