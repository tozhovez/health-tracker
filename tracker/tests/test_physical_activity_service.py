import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import PhysicalActivity
from schemas.physical_activity import PhysicalActivityCreate, PhysicalActivityUpdate
from tracker.services.physical_activity_service import PhysicalActivityService

@pytest.mark.asyncio
async def test_create_physical_activity(async_session: AsyncSession):
    physical_activity_data = PhysicalActivityCreate(
        user_uuid=uuid4(),
        start_time=datetime.now(),
        end_time=datetime.now(),
        activity_type="running",
        duration=30,
        distance=5.0
    )
    physical_activity = await PhysicalActivityService.create_physical_activity(async_session, physical_activity_data)
    assert physical_activity.id is not None
    assert physical_activity.user_uuid == physical_activity_data.user_uuid

@pytest.mark.asyncio
async def test_get_physical_activity(async_session: AsyncSession):
    user_uuid = uuid4()
    start_time = datetime.now()
    physical_activity_data = PhysicalActivityCreate(
        user_uuid=user_uuid,
        start_time=start_time,
        end_time=datetime.now(),
        activity_type="running",
        duration=30,
        distance=5.0
    )
    await PhysicalActivityService.create_physical_activity(async_session, physical_activity_data)
    activities = await PhysicalActivityService.get_physical_activity(async_session, user_uuid, start_time)
    assert len(activities) == 1
    assert activities[0].user_uuid == user_uuid

@pytest.mark.asyncio
async def test_update_physical_activity(async_session: AsyncSession):
    user_uuid = uuid4()
    start_time = datetime.now()
    physical_activity_data = PhysicalActivityCreate(
        user_uuid=user_uuid,
        start_time=start_time,
        end_time=datetime.now(),
        activity_type="running",
        duration=30,
        distance=5.0
    )
    await PhysicalActivityService.create_physical_activity(async_session, physical_activity_data)
    update_data = PhysicalActivityUpdate(
        activity_type="cycling",
        duration=45
    )
    updated_activity = await PhysicalActivityService.update_physical_activity(async_session, user_uuid, start_time, update_data)
    assert updated_activity.activity_type == "cycling"
    assert updated_activity.duration == 45

@pytest.mark.asyncio
async def test_delete_physical_activity(async_session: AsyncSession):
    user_uuid = uuid4()
    start_time = datetime.now()
    physical_activity_data = PhysicalActivityCreate(
        user_uuid=user_uuid,
        start_time=start_time,
        end_time=datetime.now(),
        activity_type="running",
        duration=30,
        distance=5.0
    )
    await PhysicalActivityService.create_physical_activity(async_session, physical_activity_data)
    deleted_activity = await PhysicalActivityService.delete_physical_activity(async_session, user_uuid, start_time)
    assert deleted_activity is not None
    assert deleted_activity.user_uuid == user_uuid
    result = await async_session.execute(select(PhysicalActivity).where(PhysicalActivity.user_uuid == user_uuid))
    activities = result.scalars().all()
    assert len(activities) == 0