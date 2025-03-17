from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, true
from database.models import BloodTest
from schemas.blood_tests import BloodTestCreate, BloodTestUpdate

class BloodTestsService:
    @staticmethod
    async def create_blood_tests(db: AsyncSession, blood_tests_data: BloodTestCreate):
        blood_tests = BloodTest(**blood_tests_data.model_dump())
        db.add(blood_tests)
        await db.commit()
        await db.refresh(blood_tests)
        return blood_tests

    @staticmethod
    async def get_blood_tests(db: AsyncSession, user_uuid: UUID, test_date: datetime = None, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(BloodTest)
            .where(BloodTest.user_uuid == user_uuid)
            .where((func.date(BloodTest.test_date) == test_date) if test_date else true())
            .order_by(desc(BloodTest.test_date))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_blood_tests(
        db: AsyncSession,
        user_uuid: UUID,
        test_date: datetime,
        blood_tests_data: BloodTestUpdate
    ):
        if blood_tests_data is None:
            raise HTTPException(status_code=400, detail="No update data provided")
        # Filter out None values
        update_data = {
            k: v for k, v in blood_tests_data.model_dump(exclude_unset=True).items() if v is not None
            }
        if not update_data:
            # No updates provided
            query = select(BloodTest).where(
                BloodTest.user_uuid == user_uuid,
                BloodTest.test_date == test_date
            )
            result = await db.execute(query)
            return result.scalars().first()
        query = (
            update(BloodTest)
            .where(
                BloodTest.user_uuid == user_uuid,
                BloodTest.test_date == test_date
            )
            .values(**update_data)
            .returning(BloodTest)
        )
        result = await db.execute(query)
        await db.commit()
        updated_blood_test = result.scalar_one_or_none()
        if not updated_blood_test:
            raise HTTPException(status_code=404, detail="Blood test not found")
        await db.refresh(updated_blood_test)
        return updated_blood_test


    @staticmethod
    async def delete_blood_tests(db: AsyncSession, user_uuid: UUID, test_date: datetime):
        query = (
            delete(BloodTest)
            .where(
                BloodTest.user_uuid == user_uuid,
                BloodTest.test_date == test_date
            )
            .returning(BloodTest)
        )
        result = await db.execute(query)
        blood_test = result.scalar_one_or_none()  #  BloodTest
        await db.commit()
        return blood_test
