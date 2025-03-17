from typing import List
from uuid import UUID
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.dbclient import get_db, refresh_db
from schemas.blood_tests import BloodTestCreate, BloodTestUpdate, BloodTestResponse
from services.blood_tests_service import BloodTestsService

blood_tests_router = APIRouter()

@blood_tests_router.post("/", response_model=BloodTestResponse, status_code=status.HTTP_201_CREATED)
async def create_blood_tests(blood_tests_data: BloodTestCreate, db: AsyncSession = Depends(get_db)):
    """Create a new Blood tests record"""
    result = await BloodTestsService.create_blood_tests(db, blood_tests_data)
    if result:
        await refresh_db()
    return result


@blood_tests_router.get("/{user_uuid}", response_model=List[BloodTestResponse])
async def read_all_blood_tests_by_user(
    user_uuid: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all Blood Tests for a specific user"""
    return await BloodTestsService.get_blood_tests(db, user_uuid, skip=skip, limit=limit)

@blood_tests_router.get("/{user_uuid}/{test_date}", response_model=List[BloodTestResponse])
async def read_blood_tests_by_user_by_date(
    user_uuid: UUID,
    test_date: datetime | date,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific blood tests by user UUID and start time"""
    blood_tests = await BloodTestsService.get_blood_tests(db, user_uuid, test_date)
    if blood_tests is None or len(blood_tests) <= 0:
        raise HTTPException(status_code=404, detail="Blood tests not found")
    return blood_tests

@blood_tests_router.patch("/{user_uuid}/{test_date}/update", response_model=BloodTestResponse)
async def update_blood_tests(
    user_uuid: UUID,
    test_date: datetime,
    blood_tests_data: BloodTestUpdate = None,
    db: AsyncSession = Depends(get_db)
):
    """Update a blood tests"""
    blood_tests = await BloodTestsService.update_blood_tests(db, user_uuid, test_date, blood_tests_data)
    if blood_tests is None:
        raise HTTPException(status_code=404, detail="Blood tests not found")
    await refresh_db()
    return blood_tests

@blood_tests_router.delete("/{user_uuid}/delete", response_model=BloodTestResponse)
async def delete_blood_tests(
    user_uuid: UUID,
    test_date: datetime = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Delete a blood tests"""
    blood_tests = await BloodTestsService.delete_blood_tests(db, user_uuid, test_date)
    if blood_tests is None:
        raise HTTPException(status_code=404, detail="Blood tests not found")
    await refresh_db()
    return blood_tests
