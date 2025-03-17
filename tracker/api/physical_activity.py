from typing import List, Any, Union
from uuid import UUID
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.dbclient import get_db, refresh_db
from schemas.physical_activity import PhysicalActivityCreate, PhysicalActivityUpdate, PhysicalActivityResponse
from services.physical_activity_service import PhysicalActivityService

physical_activity_router = APIRouter()

@physical_activity_router.post("/", response_model=PhysicalActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_physical_activity(physical_activity_data: PhysicalActivityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new physical activity record"""
    result = await PhysicalActivityService.create_physical_activity(db, physical_activity_data)
    if result:
        await refresh_db()
    return result

@physical_activity_router.get("/{user_uuid}", response_model=List[PhysicalActivityResponse])
async def read_physical_activity_by_user(
    user_uuid: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all physical activities for a specific user"""
    return await PhysicalActivityService.get_physical_activity(db, user_uuid, skip=skip, limit=limit)

@physical_activity_router.get("/{user_uuid}/{date}", response_model=List[PhysicalActivityResponse])
async def read_physical_activity_by_user_by_date(
    user_uuid: UUID,
    date: datetime | date,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific physical activity by user UUID and activity date"""
    physical_activity = await PhysicalActivityService.get_physical_activity(db, user_uuid, start_time=date)
    if physical_activity is None or len(physical_activity) <= 0:
        raise HTTPException(status_code=404, detail="Physical activity not found")
    return physical_activity

@physical_activity_router.patch("/{user_uuid}/update", response_model=PhysicalActivityResponse)
async def update_physical_activity(
    user_uuid: UUID,
    start_time: datetime = Query(...),
    physical_activity_data: PhysicalActivityUpdate = None,
    db: AsyncSession = Depends(get_db)
):
    """Update a physical activity"""
    physical_activity = await PhysicalActivityService.update_physical_activity(db, user_uuid, start_time, physical_activity_data)
    if physical_activity is None:
        raise HTTPException(status_code=404, detail="Physical activity not found")
    await refresh_db()
    return physical_activity

@physical_activity_router.delete("/{user_uuid}/delete", response_model=PhysicalActivityResponse)
async def delete_physical_activity(
    user_uuid: UUID,
    start_time: datetime = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Delete a physical activity"""
    physical_activity = await PhysicalActivityService.delete_physical_activity(db, user_uuid, start_time)
    if physical_activity is None:
        raise HTTPException(status_code=404, detail="Physical activity not found")
    await refresh_db()
    return physical_activity
