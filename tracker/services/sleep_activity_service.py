from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, true
from database.models import SleepActivity
from schemas.sleep_activity import SleepActivityCreate, SleepActivityUpdate

class SleepActivityService:
    @staticmethod
    async def create_sleep_activity(db: AsyncSession, sleep_activity_data: SleepActivityCreate):
        sleep_activity = SleepActivity(**sleep_activity_data.dict())
        db.add(sleep_activity)
        await db.commit()
        await db.refresh(sleep_activity)
        return sleep_activity

    @staticmethod
    async def get_sleep_activity(db: AsyncSession, user_uuid: UUID, start_time: datetime = None, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(SleepActivity)
            .where(SleepActivity.user_uuid == user_uuid)
            .where((func.date(SleepActivity.start_time) == start_time) if start_time else true())
            .order_by(desc(SleepActivity.start_time))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_sleep_activity(
        db: AsyncSession,
        user_uuid: UUID,
        start_time: datetime,
        sleep_activity_data: SleepActivityUpdate
    ):
        # Filter out None values
        update_sleep_activity_data = {
            k: v for k, v in sleep_activity_data.model_dump(exclude_unset=True).items() if v is not None
            }
        if not update_sleep_activity_data:
            # No updates provided
            query = select(SleepActivity).where(
                SleepActivity.user_uuid == user_uuid,
                SleepActivity.start_time == start_time
            )
            result = await db.execute(query)
            return result.scalars().first()
        query = (
            update(SleepActivity)
            .where(
                SleepActivity.user_uuid == user_uuid,
                SleepActivity.start_time == start_time
            )
            .values(**update_sleep_activity_data)
            .returning(SleepActivity)
        )
        result = await db.execute(query)
        await db.commit()
        update_sleep_activity = result.scalar_one_or_none()
        if not update_sleep_activity:
            raise HTTPException(status_code=404, detail="Sleep Activity not found")
        await db.refresh(update_sleep_activity)
        return update_sleep_activity

    @staticmethod
    async def delete_sleep_activity(db: AsyncSession, user_uuid: UUID, start_time: datetime):
        query = (
            delete(SleepActivity)
            .where(
                SleepActivity.user_uuid == user_uuid,
                SleepActivity.start_time == start_time
            )
            .returning(SleepActivity)
        )
        result = await db.execute(query)
        sleep_activity = result.scalar_one_or_none()
        await db.commit()
        return sleep_activity
