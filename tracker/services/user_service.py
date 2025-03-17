from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, true
from database.models import User
from schemas.users import UserCreate, UserUpdate

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate):
        user = User(**user_data.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user(db: AsyncSession, user_uuid: UUID  = None, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(User)
            .where((User.user_uuid == user_uuid) if user_uuid else true())
            .offset(skip)
            .limit(limit)
            )
        return result.scalars().all()

    @staticmethod
    async def update_user(db: AsyncSession, user_uuid: UUID, user_data: UserUpdate):
        # Filter out None values
        update_data = {k: v for k, v in user_data.model_dump(exclude_unset=True).items() if v is not None}
        if not update_data:
            # No updates provided
            query = select(User).where(User.user_uuid == user_uuid)
            result = await db.execute(query)
            return result.scalars().first()
        query = update(User).where(User.user_uuid == user_uuid).values(**update_data).returning(User)
        result = await db.execute(query)
        await db.commit()
        update_users = result.scalar_one_or_none()
        if not update_users:
            raise HTTPException(status_code=404, detail="User not found")
        await db.refresh(update_users)
        return update_users

    @staticmethod
    async def delete_user(db: AsyncSession, user_uuid: UUID):
        query = delete(User).where(User.user_uuid == user_uuid).returning(User)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        await db.commit()
        return user
