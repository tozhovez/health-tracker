from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, true
from database.models import PhysicalActivity
from schemas.physical_activity import PhysicalActivityCreate, PhysicalActivityUpdate

class PhysicalActivityService:
    @staticmethod
    async def create_physical_activity(db: AsyncSession, physical_activity_data: PhysicalActivityCreate):
        physical_activity = PhysicalActivity(**physical_activity_data.dict())
        db.add(physical_activity)
        await db.commit()
        await db.refresh(physical_activity)
        return physical_activity

    @staticmethod
    async def get_physical_activity(db: AsyncSession, user_uuid: UUID, start_time: datetime = None, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(PhysicalActivity)
            .where(PhysicalActivity.user_uuid == user_uuid)
            .where((func.date(PhysicalActivity.start_time) == start_time) if start_time else true())
            .order_by(desc(PhysicalActivity.start_time))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_physical_activity(
        db: AsyncSession,
        user_uuid: UUID,
        start_time: datetime,
        physical_activity_data: PhysicalActivityUpdate
    ):
        # Filter out None values
        update_physical_activity_data = {
            k: v for k, v in physical_activity_data.model_dump(exclude_unset=True).items() if v is not None
            }

        if not update_physical_activity_data:
            # No updates provided
            query = select(PhysicalActivity).where(
                PhysicalActivity.user_uuid == user_uuid,
                PhysicalActivity.start_time == start_time
            )
            result = await db.execute(query)
            return result.scalars().first()
        query = (
            update(PhysicalActivity)
            .where(
                PhysicalActivity.user_uuid == user_uuid,
                PhysicalActivity.start_time == start_time
            )
            .values(**update_physical_activity_data)
            .returning(PhysicalActivity)
        )
        result = await db.execute(query)
        await db.commit()      
        updated_physical_activity = result.scalar_one_or_none()
        if not updated_physical_activity:
            raise HTTPException(status_code=404, detail="Physical_activity not found")
        await db.refresh(updated_physical_activity)
        return updated_physical_activity

    @staticmethod
    async def delete_physical_activity(db: AsyncSession, user_uuid: UUID, start_time: datetime):
        query = (
            delete(PhysicalActivity)
            .where(
                PhysicalActivity.user_uuid == user_uuid,
                PhysicalActivity.start_time == start_time
            )
            .returning(PhysicalActivity)
        )
        result = await db.execute(query)
        physical_activity = result.scalar_one_or_none()
        await db.commit()
        return physical_activity
    
