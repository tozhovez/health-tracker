from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, true, text
from database.models import BioMetric
from schemas.bio_metrics import BioMetricCreate, BioMetricUpdate

class BioMetricsService:
    @staticmethod
    async def create_bio_metrics(db: AsyncSession, bio_metrics_data: BioMetricCreate):
        bio_metrics = BioMetric(**bio_metrics_data.dict())
        db.add(bio_metrics)
        await db.commit()
        await db.refresh(bio_metrics)
        return bio_metrics

    @staticmethod
    async def get_bio_metrics(db: AsyncSession, user_uuid: UUID, recorded: datetime = None, skip: int = 0, limit: int = 100):
        # Обновление агрегатов
        result = await db.execute(
            select(BioMetric)
            .where(BioMetric.user_uuid == user_uuid)
            .where((func.date(BioMetric.recorded) == recorded) if recorded else true())
            .order_by(desc(BioMetric.recorded))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_bio_metrics(
        db: AsyncSession,
        user_uuid: UUID,
        recorded: datetime,
        bio_metrics_data: BioMetricUpdate
    ):
        # Filter out None values
        update_bio_metrics_data = {
            k: v for k, v in bio_metrics_data.model_dump(exclude_unset=True).items() if v is not None
            }
        if not update_bio_metrics_data:
            # No updates provided
            query = select(BioMetric).where(
                BioMetric.user_uuid == user_uuid,
                BioMetric.recorded == recorded
            )
            result = await db.execute(query)
            return result.scalars().first()
        query = (
            update(BioMetric)
            .where(
                BioMetric.user_uuid == user_uuid,
                BioMetric.recorded == recorded
            )
            .values(**update_bio_metrics_data)
            .returning(BioMetric)
        )
        result = await db.execute(query)
        await db.commit()
        
        updated_bio_metrics = result.scalar_one_or_none()
        if not updated_bio_metrics:
            raise HTTPException(status_code=404, detail="Bio metrics not found")
        await db.refresh(updated_bio_metrics)
        return updated_bio_metrics

    @staticmethod
    async def delete_bio_metrics(db: AsyncSession, user_uuid: UUID, recorded: datetime):
        query = (
            delete(BioMetric)
            .where(
                BioMetric.user_uuid == user_uuid,
                BioMetric.recorded == recorded
            )
            .returning(BioMetric)
        )
        result = await db.execute(query)
        bio_metrics = result.scalar_one_or_none()
        await db.commit()
        return bio_metrics
    
    


        