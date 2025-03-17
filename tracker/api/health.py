from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date, datetime
from services.health_service import HealthService
from schemas.health import TimeFrame, HealthMetricCategory, HealthScoreWeights
from typing import List, Optional
from database.dbclient import get_db

health_router = APIRouter()


@health_router.get("/{user_uuid}/metrics")
async def get_health_metrics_by_user(user_uuid: UUID, db: AsyncSession = Depends(get_db)):
    """Get the latest available health metrics for a user."""

    data = await HealthService.get_health_metrics(db, user_uuid)
    if not data:
        raise HTTPException(status_code=404, detail="User data not found")
    return data

@health_router.get("/{user_uuid}/{recorded}/metrics")
async def get_health_metrics_by_user_by_date(
    user_uuid: UUID,
    recorded: Optional[datetime|date],
    db: AsyncSession = Depends(get_db)
    ):
    """Get the latest available health metrics for a user as of a specific date."""
    data = await HealthService.get_health_metrics(db, user_uuid, recorded)
    if not data:
        raise HTTPException(status_code=404, detail="User data not found for the given date")
    return data

@health_router.get("/{user_uuid}/score")
async def get_health_score_by_user(
    user_uuid: UUID,  
    db: AsyncSession = Depends(get_db)
    ):
    """Calculate an overall health score based on latest available health metrics compared to other user averages.
        Score ranges from 0-100, with higher being better."""
    data = await HealthService.get_health_score(db, user_uuid)
    if not data:
        raise HTTPException(status_code=404, detail="User data not found for the given user")
    return data

@health_router.get("/{user_uuid}/{recorded}/score")
async def get_health_score_by_user_by_date(
    user_uuid: UUID, 
    recorded: datetime|date,
    db: AsyncSession = Depends(get_db)
    ):
    data = await HealthService.get_health_score(db, user_uuid, recorded)
    if not data:
        raise HTTPException(status_code=404, detail="User data not found for the given date")
    return data


# @health_router.get("/{user_uuid}/{recorded}/score")
# async def get_health_score_by_date(user_uuid: UUID, recorded: date, db: AsyncSession = Depends(get_db)):
#     data = await HealthService.get_health_score_by_date(db, user_uuid, recorded)
#     if not data:
#         raise HTTPException(status_code=404, detail="User data not found for the given date")
#     return data
