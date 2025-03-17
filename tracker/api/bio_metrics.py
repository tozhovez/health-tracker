from typing import List
from uuid import UUID
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.dbclient import get_db, refresh_db
from schemas.bio_metrics import BioMetricCreate, BioMetricUpdate, BioMetricResponse
from services.bio_metrics_service import BioMetricsService

bio_metrics_router = APIRouter()

@bio_metrics_router.post("/", response_model=BioMetricResponse, status_code=status.HTTP_201_CREATED)
async def create_bio_metrics(bio_metrics_data: BioMetricCreate, db: AsyncSession = Depends(get_db)):
    """Create a new biometrics data record"""
    result = await BioMetricsService.create_bio_metrics(db, bio_metrics_data)
    if result:
        await refresh_db()
    return result

@bio_metrics_router.get("/{user_uuid}", response_model=List[BioMetricResponse])
async def read_all_bio_metrics_by_user(
    user_uuid: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all biometrics for a specific user"""
    return await BioMetricsService.get_bio_metrics(db, user_uuid, skip=skip, limit=limit)

@bio_metrics_router.get("/{user_uuid}/{recorded}", response_model=List[BioMetricResponse])
async def read_bio_metrics_by_user_by_date(
    user_uuid: UUID,
    recorded: datetime | date,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific bio metrics by user UUID and start time"""
    bio_metrics = await BioMetricsService.get_bio_metrics(db, user_uuid, recorded)
    if bio_metrics is None or len(bio_metrics) <= 0:
        raise HTTPException(status_code=404, detail="Biometrics data not found")
    return bio_metrics

@bio_metrics_router.patch("/{user_uuid}/{recorded}/update", response_model=BioMetricResponse)
async def update_bio_metrics(
    user_uuid: UUID,
    recorded: datetime,
    bio_metrics_data: BioMetricUpdate = None,
    db: AsyncSession = Depends(get_db)
):
    """Update a biometrics data"""
    bio_metrics = await BioMetricsService.update_bio_metrics(db, user_uuid, recorded, bio_metrics_data)
    if bio_metrics is None:
        raise HTTPException(status_code=404, detail="Biometrics data not found")
    await refresh_db()
    return bio_metrics

@bio_metrics_router.delete("/{user_uuid}/delete", response_model=BioMetricResponse)
async def delete_bio_metrics(
    user_uuid: UUID,
    recorded: datetime = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Delete a biometrics data"""
    bio_metrics = await BioMetricsService.delete_bio_metrics(db, user_uuid, recorded)
    if bio_metrics is None:
        raise HTTPException(status_code=404, detail="Biometrics data not found")
    await refresh_db()
    return bio_metrics
