from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy import update, delete, text
from typing import Optional, List, TypeVar, Generic, Type
from pydantic import BaseModel
from uuid import UUID
from database.models import Base
from config import settings
import logging
logger = logging.getLogger(__name__)
# Generic type for the model
T = TypeVar("T", bound=Base)

class AsyncDatabaseClient:
    def __init__(self, db_url: str):
        """Initialize the async database client with the database URL."""
        self.engine = create_async_engine(db_url, echo=True, future=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        """Get an async database session."""
        return self.async_session()

    async def create(self, model: Type[T], data: BaseModel) -> T:
        """Create a new record in the database."""
        async with self.get_session() as session:
            db_item = model(**data.dict())
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
            return db_item

    async def close(self):
        """Close the database engine."""
        await self.engine.dispose()

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
# Create async session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# DB dependency for endpoints
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def refresh_db():
    client = AsyncDatabaseClient(settings.DATABASE_URL)
    sql_refresh = Path(__file__).parent.parent / settings.SQL_REFRESH
    queries = None
    if sql_refresh.exists():
        sql_refreshes =  sql_refresh.read_text()
        queries = sql_refreshes.split(";")
    try:
        async with client.engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            for query in queries:
                    query = query.strip()
                    if query:
                        await conn.execute(text(query))
            await conn.commit()
            await client.close()
            logger.info("refresh continuous aggregate successfully.")
    except Exception as e:
        logger.error(f"Error during database refresh continuous aggregate: {e}")